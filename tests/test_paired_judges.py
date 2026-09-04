from __future__ import annotations

from copy import deepcopy
import json
import unittest

from judge.lanes import INITIAL_STAGES, LANE_STAGES, OBLIGATIONS, load_lane_schema, validate_lane_review
from judge.paired_review import aggregate_paired_reviews, evidence_binding, run_paired_review, select_lane_aggregate
from judge.prompts import build_messages, load_system_prompt
from judge.provider_adapter import JudgeInfraError, ReviewResult
from judge.schema_validation import ReviewValidationError, review_schema_for_stage, validate_review


def fixture_evidence() -> dict:
    """Organizer-owned analytic fixture: never read a mutable solver candidate."""
    claim = {
        "schema_version": 3, "submission_state": "ready", "lane": "exploratory",
        "target_profile": "organizer-fixture-v1", "attack_class": "ordinary-collision", "rounds": 2,
        "claim": {
            "time_log2": 10.0, "time_unit": "target-compressions", "memory_log2_bytes": 8.0,
            "data_log2": 0.0, "preprocessing_log2": 0.0, "success_probability": 0.5,
            "nonuniform_advice_log2_bytes": 0.0,
        },
        "restrictions": [], "heuristics": [], "baseline_improved": "organizer-fixture-reference",
    }
    return {
        "schema_version": "hashsmash-evidence-v1",
        "submission": {
            "intake_report": {
                "status": "mechanically_valid", "submission_state": "ready", "claim": claim,
                "track": {"target_profile": "organizer-fixture-v1", "attack_class": "ordinary-collision", "rounds": 2},
                "package_sha256": "a" * 64, "target_config_sha256": "b" * 64,
            },
            "certificate_report": {"status": "passed", "package_sha256": "a" * 64, "target_config_sha256": "b" * 64},
            "proof_markdown_line_numbered": "L1\tAn organizer analytic fixture, not a real attack claim.",
        },
        "benchmark": {"target_profile": {"id": "organizer-fixture-v1"}},
    }


def fixture_review(stage: str, evidence: dict) -> dict:
    binding = evidence.get("review_context", {}).get("binding") or evidence_binding(evidence)
    result = {
        "schema_version": "review-lanes-v1", "stage": stage, "binding": deepcopy(binding),
        "summary": "Organizer synthetic decision fixture.",
        "obligations": [
            {"id": key, "status": "supported", "explanation": "Discharged by fixture.", "evidence": ["proof.md:L1"]}
            for key in OBLIGATIONS[stage]
        ],
        "heuristics": [], "findings": [], "cost_reconstruction": None,
        "challenge_resolutions": [], "prompt_injection_detected": False,
    }
    if stage == "lane_cost":
        cost = deepcopy(evidence["submission"]["intake_report"]["claim"]["claim"])
        cost.update(normalized_score_log2=cost["time_log2"] + cost["memory_log2_bytes"], calculation_trace=["10 + 8 = 18"])
        result["cost_reconstruction"] = cost
    for finding_id in evidence.get("review_context", {}).get("fatal_findings", {}):
        result["challenge_resolutions"].append({
            "finding_id": finding_id, "result": "unresolved", "explanation": "Fixture leaves objection unresolved.",
            "evidence": ["proof.md:L1"], "obligations_discharged": [],
        })
    return result


def add_fatal(review: dict) -> None:
    review["obligations"][0]["status"] = "fatal"
    review["findings"].append({
        "id": "collision-error", "severity": "fatal", "category": "counterexample",
        "statement": "A fixture critic alleges a concrete counterexample.",
        "obligation_ids": [review["obligations"][0]["id"]], "heuristic_ids": [], "evidence": ["proof.md:L1"],
    })


class FixtureClient:
    def __init__(self, mutate=None):
        self.mutate = mutate
        self.calls = []

    def review(self, stage, evidence):
        self.calls.append((stage, deepcopy(evidence)))
        review = fixture_review(stage, evidence)
        if self.mutate:
            self.mutate(stage, review, evidence)
        return ReviewResult(review, {"provider": "offline-organizer-fixture", "requested_model": "fixture"})


class PairedJudgeTests(unittest.TestCase):
    def test_all_roles_receive_nominal_reference_semantics_as_trusted_instructions(self):
        for stage in LANE_STAGES:
            with self.subTest(stage=stage):
                messages = build_messages(stage, fixture_evidence())
                self.assertEqual(messages[0]["role"], "system")
                instructions = " ".join(messages[0]["content"].split())
                self.assertIn("baseline_improved is a schema-required reference identifier", instructions)
                self.assertIn("does not assert improvement", instructions)
                self.assertIn("An explicit false comparison", instructions)
        self.assertNotIn("schema-required reference identifier", load_system_prompt("correctness"))

    def test_analytic_pass_runs_four_independent_reviews(self):
        client = FixtureClient()
        dossier = run_paired_review(fixture_evidence(), client)
        self.assertEqual(dossier["lanes"]["exploratory"]["status"], "plausible_not_refuted")
        self.assertEqual(dossier["lanes"]["rigorous"]["status"], "ai_rigor_qualified")
        self.assertEqual([stage for stage, _ in client.calls], list(INITIAL_STAGES))
        self.assertTrue(all("fatal_findings" not in evidence["review_context"] for _, evidence in client.calls))
        aggregate = select_lane_aggregate(dossier, "rigorous")
        self.assertEqual(aggregate["input_package_sha256"], "a" * 64)
        self.assertNotIn("score", aggregate)

    def test_unresolved_material_obligation_passes_only_exploratory(self):
        def mutate(stage, review, _):
            if stage == "lane_cryptanalysis":
                review["obligations"][1]["status"] = "unresolved"
        dossier = run_paired_review(fixture_evidence(), FixtureClient(mutate))
        self.assertTrue(dossier["lanes"]["exploratory"]["eligible"])
        self.assertEqual(dossier["lanes"]["rigorous"]["status"], "not_qualified")

    def test_unevaluable_is_not_labeled_false(self):
        def mutate(stage, review, _):
            if stage == "lane_evaluability":
                review["obligations"][1]["status"] = "unresolved"
        dossier = run_paired_review(fixture_evidence(), FixtureClient(mutate))
        self.assertEqual(dossier["lanes"]["exploratory"]["status"], "not_evaluable")

    def test_confirmed_fatal_requires_defender_then_adjudicator(self):
        def mutate(stage, review, evidence):
            if stage == "lane_cryptanalysis":
                add_fatal(review)
            if stage == "lane_adjudicator":
                self.assertIn("defender_review", evidence["review_context"])
                review["challenge_resolutions"][0]["result"] = "confirmed"
        client = FixtureClient(mutate)
        dossier = run_paired_review(fixture_evidence(), client)
        self.assertEqual([stage for stage, _ in client.calls][-2:], ["lane_defender", "lane_adjudicator"])
        self.assertEqual(dossier["lanes"]["exploratory"]["status"], "refuted")

    def test_unresolved_fatal_allegation_passes_exploratory(self):
        client = FixtureClient(lambda stage, review, _: add_fatal(review) if stage == "lane_cryptanalysis" else None)
        dossier = run_paired_review(fixture_evidence(), client)
        self.assertTrue(dossier["lanes"]["exploratory"]["eligible"])
        self.assertFalse(dossier["lanes"]["rigorous"]["eligible"])

    def test_dismissed_fatal_needs_explicit_discharge_for_rigorous(self):
        def mutate(stage, review, evidence):
            if stage == "lane_cryptanalysis":
                add_fatal(review)
            if stage == "lane_adjudicator":
                resolution = review["challenge_resolutions"][0]
                resolution["result"] = "refuted"
                resolution["obligations_discharged"] = ["lane_cryptanalysis/collision_correctness"]
        dossier = run_paired_review(fixture_evidence(), FixtureClient(mutate))
        self.assertTrue(dossier["lanes"]["rigorous"]["eligible"])

    def test_missing_challenge_or_new_last_stage_accusation_fails_closed(self):
        def mutate(stage, review, _):
            if stage == "lane_cryptanalysis":
                add_fatal(review)
            if stage == "lane_adjudicator":
                review["challenge_resolutions"] = []
        dossier = run_paired_review(fixture_evidence(), FixtureClient(mutate))
        self.assertEqual(dossier["lanes"]["exploratory"]["status"], "infra_failed")

    def test_binding_mismatch_is_infrastructure_failure(self):
        def mutate(stage, review, _):
            if stage == "lane_cost":
                review["binding"]["claim_sha256"] = "c" * 64
        dossier = run_paired_review(fixture_evidence(), FixtureClient(mutate))
        self.assertEqual(dossier["lanes"]["rigorous"]["status"], "infra_failed")

    def test_full_claim_cost_is_in_binding(self):
        first = fixture_evidence()
        second = deepcopy(first)
        second["submission"]["intake_report"]["claim"]["claim"]["time_log2"] += 1
        self.assertNotEqual(evidence_binding(first)["claim_sha256"], evidence_binding(second)["claim_sha256"])

    def test_drafts_and_stale_experiments_never_reach_provider(self):
        for stale in (False, True):
            evidence = fixture_evidence()
            if stale:
                evidence["submission"]["experiment_report"] = {"status": "passed", "package_sha256": "c" * 64, "target_config_sha256": "b" * 64}
            else:
                evidence["submission"]["intake_report"]["submission_state"] = "draft"
            client = FixtureClient()
            dossier = run_paired_review(evidence, client)
            self.assertEqual(client.calls, [])
            self.assertFalse(dossier["lanes"]["exploratory"]["eligible"])

    def test_infra_error_redacts_provider_exception_text(self):
        def mutate(stage, review, _):
            if stage == "lane_cost":
                raise JudgeInfraError("secret fixture API value must never appear")
        dossier = run_paired_review(fixture_evidence(), FixtureClient(mutate))
        self.assertNotIn("secret fixture", json.dumps(dossier))
        self.assertEqual(dossier["lanes"]["exploratory"]["status"], "infra_failed")

    def test_heuristic_coverage_is_required_and_plausibility_not_rigor(self):
        evidence = fixture_evidence()
        evidence["submission"]["intake_report"]["claim"]["heuristics"] = [{"id": "h1"}]
        omitted = run_paired_review(evidence, FixtureClient())
        self.assertEqual(omitted["lanes"]["exploratory"]["status"], "infra_failed")
        def mutate(stage, review, _):
            if stage in {"lane_cryptanalysis", "lane_experiments"}:
                review["heuristics"] = [{
                    "id": "h1", "statement": "Fixture approximation.", "status": "plausible",
                    "tested_scope": "Small instance", "extrapolated_scope": "Larger instance",
                    "sensitivity": "Uncertain factor", "evidence": ["proof.md:L1"],
                }]
        dossier = run_paired_review(evidence, FixtureClient(mutate))
        self.assertTrue(dossier["lanes"]["exploratory"]["eligible"])
        self.assertFalse(dossier["lanes"]["rigorous"]["eligible"])

    def test_established_heuristics_can_pass_rigorous(self):
        evidence = fixture_evidence()
        evidence["submission"]["intake_report"]["claim"]["heuristics"] = [{"id": "h1"}]
        def mutate(stage, review, _):
            if stage in {"lane_cryptanalysis", "lane_experiments"}:
                review["heuristics"] = [{
                    "id": "h1", "statement": "Calibrated approximation.", "status": "established",
                    "tested_scope": "Claimed regime", "extrapolated_scope": "None",
                    "sensitivity": "Conservative interval", "evidence": ["proof.md:L1"],
                }]
        self.assertTrue(run_paired_review(evidence, FixtureClient(mutate))["lanes"]["rigorous"]["eligible"])

    def test_cost_disagreement_prevents_rigorous_acceptance(self):
        def mutate(stage, review, _):
            if stage == "lane_cost":
                review["cost_reconstruction"]["time_log2"] = 11
                review["cost_reconstruction"]["normalized_score_log2"] = 19
        dossier = run_paired_review(fixture_evidence(), FixtureClient(mutate))
        self.assertFalse(dossier["lanes"]["rigorous"]["eligible"])
        self.assertEqual(dossier["lanes"]["exploratory"]["status"], "infra_failed")

    def test_supported_cost_contradictions_cannot_receive_exploratory_score(self):
        fields = {
            "time_log2": 11.0, "memory_log2_bytes": 9.0, "data_log2": 1.0,
            "preprocessing_log2": 1.0, "nonuniform_advice_log2_bytes": 1.0,
            "success_probability": 0.25, "time_unit": "wrong-units",
        }
        for field, value in fields.items():
            with self.subTest(field=field):
                def mutate(stage, review, _):
                    if stage == "lane_cost":
                        cost = review["cost_reconstruction"]
                        cost[field] = value
                        cost["normalized_score_log2"] = cost["time_log2"] + cost["memory_log2_bytes"]
                client = FixtureClient(mutate)
                dossier = run_paired_review(fixture_evidence(), client)
                self.assertEqual(dossier["lanes"]["exploratory"]["status"], "infra_failed")
                self.assertFalse(dossier["lanes"]["exploratory"]["eligible"])
                self.assertEqual(len(client.calls), 4)

    def test_uncertain_cost_reconstruction_remains_exploratory(self):
        def mutate(stage, review, _):
            if stage == "lane_cost":
                review["cost_reconstruction"]["time_log2"] = 11
                review["cost_reconstruction"]["normalized_score_log2"] = 19
                review["obligations"][0]["status"] = "unresolved"
        dossier = run_paired_review(fixture_evidence(), FixtureClient(mutate))
        self.assertTrue(dossier["lanes"]["exploratory"]["eligible"])
        self.assertFalse(dossier["lanes"]["rigorous"]["eligible"])

    def test_cited_fatal_cost_discrepancy_reaches_defender_and_adjudicator(self):
        def mutate(stage, review, _):
            if stage == "lane_cost":
                review["cost_reconstruction"]["time_log2"] = 11
                review["cost_reconstruction"]["normalized_score_log2"] = 19
                add_fatal(review)
            if stage == "lane_adjudicator":
                review["challenge_resolutions"][0]["result"] = "confirmed"
        client = FixtureClient(mutate)
        dossier = run_paired_review(fixture_evidence(), client)
        self.assertEqual(dossier["lanes"]["exploratory"]["status"], "refuted")
        self.assertEqual(len(client.calls), 6)

    def test_declared_experiment_cannot_use_not_requested_report(self):
        evidence = fixture_evidence()
        evidence["submission"]["intake_report"]["claim"]["experiment_manifest"] = "experiments/manifest.json"
        evidence["submission"]["experiment_report"] = {
            "status": "not_requested", "package_sha256": "a" * 64, "target_config_sha256": "b" * 64,
        }
        client = FixtureClient()
        dossier = run_paired_review(evidence, client)
        self.assertEqual(client.calls, [])
        self.assertEqual(dossier["lanes"]["exploratory"]["status"], "not_evaluable")

    def test_refuted_heuristic_cannot_borrow_unrelated_fatal_finding(self):
        review = fixture_review("lane_cryptanalysis", fixture_evidence())
        for key, status in (("h1", "refuted"), ("h2", "established")):
            review["heuristics"].append({
                "id": key, "statement": "Organizer heuristic fixture.", "status": status,
                "tested_scope": "Claimed regime", "extrapolated_scope": "None",
                "sensitivity": "Bounded", "evidence": ["proof.md:L1"],
            })
        add_fatal(review)
        review["findings"][0]["heuristic_ids"] = ["h2"]
        with self.assertRaises(ReviewValidationError):
            validate_lane_review(review)

    def test_dismissed_heuristic_refutation_requires_reassessment(self):
        evidence = fixture_evidence()
        evidence["submission"]["intake_report"]["claim"]["heuristics"] = [{"id": "h1"}]
        def mutate(stage, review, _):
            if stage in {"lane_cryptanalysis", "lane_experiments"}:
                review["heuristics"] = [{
                    "id": "h1", "statement": "Organizer heuristic fixture.",
                    "status": "refuted" if stage == "lane_cryptanalysis" else "established",
                    "tested_scope": "Claimed regime", "extrapolated_scope": "None",
                    "sensitivity": "Bounded", "evidence": ["proof.md:L1"],
                }]
            if stage == "lane_cryptanalysis":
                add_fatal(review)
                review["findings"][0]["heuristic_ids"] = ["h1"]
            if stage == "lane_adjudicator":
                resolution = review["challenge_resolutions"][0]
                resolution["result"] = "refuted"
                resolution["obligations_discharged"] = ["lane_cryptanalysis/collision_correctness"]
        dossier = run_paired_review(evidence, FixtureClient(mutate))
        self.assertTrue(dossier["lanes"]["exploratory"]["eligible"])
        self.assertFalse(dossier["lanes"]["rigorous"]["eligible"])
        assessment = dossier["heuristic_assessments"]["lane_cryptanalysis/heuristic/h1"]
        self.assertEqual(assessment["review_status"], "refuted")
        self.assertEqual(assessment["effective_status"], "pending_reassessment")
        self.assertIn("pending_reassessment", " ".join(dossier["lanes"]["rigorous"]["reasons"]))

    def test_different_role_clients_are_used(self):
        default, specialized = FixtureClient(), FixtureClient()
        run_paired_review(fixture_evidence(), default, role_clients={"lane_experiments": specialized})
        self.assertEqual([stage for stage, _ in specialized.calls], ["lane_experiments"])
        self.assertNotIn("lane_experiments", [stage for stage, _ in default.calls])

    def test_schema_does_not_allow_epistemic_confidence(self):
        review = fixture_review("lane_cost", fixture_evidence())
        review["confidence"] = 0.99
        with self.assertRaises(ReviewValidationError):
            validate_lane_review(review)

    def test_schema_requires_obligations_and_fatal_citations(self):
        review = fixture_review("lane_cryptanalysis", fixture_evidence())
        review["obligations"] = []
        with self.assertRaises(ReviewValidationError):
            validate_lane_review(review)
        review = fixture_review("lane_cryptanalysis", fixture_evidence())
        review["obligations"][0]["status"] = "fatal"
        with self.assertRaises(ReviewValidationError):
            validate_lane_review(review)

    def test_legacy_dispatch_remains_separate(self):
        self.assertEqual(review_schema_for_stage("lane_cost"), load_lane_schema())
        self.assertIn("unconditional-v1", load_system_prompt("correctness"))
        paired = load_system_prompt("lane_cryptanalysis")
        self.assertIn("Heuristics are permitted", paired)
        self.assertNotIn("Additional unproved", paired)
        validate_review(fixture_review("lane_cost", fixture_evidence()), expected_stage="lane_cost")

    def test_all_provider_backends_use_paired_schema_and_parse_without_legacy_fields(self):
        from judge.bedrock_adapter import BedrockClient, BedrockConfig
        from judge.provider_adapter import OpenRouterClient, OpenRouterConfig
        from judge.tests.helpers import provider_response
        from judge.tests.test_bedrock_adapter import FakeTransport, bedrock_response, sol_response

        evidence = fixture_evidence()
        record = fixture_review("lane_cost", evidence)
        configurations = [
            (OpenRouterClient, OpenRouterConfig(api_key="organizer-fixture", max_attempts=1), provider_response(record)),
            (BedrockClient, BedrockConfig(api_key="organizer-fixture", max_attempts=1), bedrock_response(record)),
            (BedrockClient, BedrockConfig(api_key="organizer-fixture", model="us.openai.gpt-5.6-sol", max_attempts=1), sol_response(record)),
        ]
        for factory, config, response in configurations:
            with self.subTest(factory=factory.__name__, model=config.model):
                transport = FakeTransport([response])
                provider = factory(config, transport=transport, sleeper=lambda _: None)
                result = provider.review("lane_cost", evidence)
                self.assertEqual(result.review, record)
                body = json.loads(transport.calls[0]["body"])
                serialized = json.dumps(body)
                self.assertIn("review-lanes-v1", serialized)
                self.assertNotIn("qualification_policy: unconditional-v1", serialized)


if __name__ == "__main__":
    unittest.main()
