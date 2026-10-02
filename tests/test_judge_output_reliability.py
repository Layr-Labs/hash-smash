"""Failure recovery without changing qualification, using organizer fixtures."""

import json
import unittest
from pathlib import Path
from unittest.mock import patch

from judge.lanes import LANE_STAGES
from judge.paired_review import run_paired_review
from judge.provider_adapter import JudgeInfraError, _schema_for_stage
from judge.tests.helpers import fixture_evidence, review, add_fatal
from judge.tests.test_bedrock_adapter import FakeTransport, sol_client, sol_response


def text_response(text):
    return sol_response(output=[{"type": "message", "role": "assistant", "status": "completed",
                                "content": [{"type": "output_text", "text": text}]}])


class JudgeOutputReliabilityTests(unittest.TestCase):
    def test_reorg_receives_current_validity_instructions_not_only_their_hash(self):
        from judge.prompts import load_system_prompt
        original = Path.read_text

        def changed_prompt(path, *args, **kwargs):
            text = original(path, *args, **kwargs)
            if path.name == "lane-cryptanalysis-v1.md":
                text += "\nOrganizer fixture: assess the newly required validity condition."
            return text

        with patch.object(Path, "read_text", changed_prompt):
            prompt = load_system_prompt("lane_rescore")
        self.assertIn("assess the newly required validity condition", prompt)
        self.assertIn("old judgment is reusable reasoning, not a binding verdict", prompt)
        self.assertGreater(prompt.index("REORG PROCEDURE"), prompt.index("newly required validity condition"))

    def test_wire_contract_contains_only_role_outputs(self):
        for stage in (*LANE_STAGES, "lane_rescore"):
            schema = _schema_for_stage(stage)
            for generated in ("binding", "stage", "schema_version", "prompt_injection_detected"):
                self.assertNotIn(generated, schema["properties"])
            self.assertNotIn("resource_ledger", json.dumps(schema))
            self.assertNotIn("normalized_score_log2", json.dumps(schema))
            if stage != "lane_cost":
                self.assertNotIn("cost_reconstruction", schema["properties"])

    def test_harness_attaches_binding_and_derived_score(self):
        record = review("lane_cost")
        for field in ("binding", "stage", "schema_version", "prompt_injection_detected", "challenge_resolutions"):
            record.pop(field)
        record["cost_reconstruction"].pop("normalized_score_log2")
        result = sol_client(FakeTransport([sol_response(record)])).review("lane_cost", fixture_evidence())
        self.assertEqual(result.review, review("lane_cost"))

    def test_json_retry_contains_location_and_keeps_a_valid_fatal_finding(self):
        rejected = review("lane_evaluability")
        add_fatal(rejected)
        transport = FakeTransport([text_response('{"summary":"unfinished"'), sol_response(rejected)])
        result = sol_client(transport, max_attempts=3).review("lane_evaluability", fixture_evidence())
        self.assertEqual(len(transport.calls), 2)
        self.assertEqual(result.review["findings"], rejected["findings"])
        details = result.provenance["retry_diagnostics"][0]
        self.assertEqual(details["category"], "invalid_json")
        self.assertIn("column", details)
        self.assertIn("invalid_json", json.loads(transport.calls[1]["body"])["instructions"])

    def test_context_contradiction_is_retried_within_the_same_budget(self):
        bad = review("lane_cost")
        bad["cost_reconstruction"]["time_log2"] += 1
        transport = FakeTransport([sol_response(bad), sol_response(review("lane_cost"))])
        result = sol_client(transport, max_attempts=2).review("lane_cost", fixture_evidence())
        self.assertEqual(result.provenance["attempts"], 2)
        self.assertIn("contradicts submitted bound", result.provenance["retry_diagnostics"][0]["message"])

    def test_exhaustion_retains_safe_errors_and_never_a_score(self):
        broken = text_response('{"summary":"private response contents"')
        transport = FakeTransport([broken, broken])
        with self.assertRaises(JudgeInfraError) as caught:
            sol_client(transport, max_attempts=2).review("lane_cost", fixture_evidence())
        error = caught.exception
        self.assertEqual(error.attempts, 2)
        self.assertEqual(len(error.diagnostics), 2)
        self.assertNotIn("private response contents", json.dumps(error.diagnostics))
        self.assertNotIn("test-bedrock-secret", json.dumps(error.diagnostics))
        self.assertEqual(error.diagnostics[-1]["request_id"], "aws-sol-123")

        class FailedClient:
            def review(self, stage, evidence):
                raise error

        dossier = run_paired_review(fixture_evidence(), FailedClient())
        self.assertEqual(dossier["lanes"]["exploratory"]["status"], "infra_failed")
        self.assertIn("invalid_json", dossier["infrastructure_failures"]["lane_cost"])
        self.assertEqual(dossier["failure_diagnostics"]["lane_cost"]["attempts"], 2)

    def test_omitted_heuristic_gets_feedback_instead_of_late_aggregation_failure(self):
        evidence = fixture_evidence()
        evidence["submission"]["intake_report"]["claim"]["heuristics"] = [{"id": "H-fixture"}]
        record = review("lane_cryptanalysis")
        transport = FakeTransport([sol_response(record), sol_response(record)])
        with self.assertRaises(JudgeInfraError) as caught:
            sol_client(transport, max_attempts=2).review("lane_cryptanalysis", evidence)
        self.assertIn("every declared heuristic", caught.exception.diagnostics[-1]["message"])
        self.assertEqual(len(transport.calls), 2)
