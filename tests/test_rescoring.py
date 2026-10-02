"""Reorg judgment and accounting boundaries, using organizer fixtures and fake judges."""

from copy import deepcopy
import json
import shutil
import unittest
from unittest.mock import patch

from judge import rescore
from judge.provider_adapter import ReviewResult
from scripts.archive_review import archive
from scripts.reference_operation_costs import reference_costs
from scripts import hashsmash_pipeline as pipeline
from scripts import rescore_artifacts
from tests import test_frontier_pipeline as fixtures
from tests.test_frontier_pipeline import fake_provider, read_json
from verifier.errors import VerificationError
from verifier.frontier_tracks import LaneTrack, ROOT, frontier_tracks
from verifier.io import atomic_write_json
from verifier.costs import UNIT_WEIGHTS
from verifier.schema_validation import validate_claim


class CostClient:
    def __init__(self, time_log2=None, mutate=None):
        self.calls, self.time_log2, self.mutate = [], time_log2, mutate

    def review(self, stage, evidence):
        self.calls.append((stage, deepcopy(evidence)))
        review = {"schema_version": "review-rescore-v2", "stage": stage,
                  "binding": evidence["review_context"]["binding"], "status": "complete",
                  "time_log2": self.time_log2 if self.time_log2 is not None else evidence["review_context"]["previous_score"],
                  "calculation_trace": ["Reprice the same organizer fixture bounds."]}
        if self.mutate:
            self.mutate(review)
        return ReviewResult(review, {"provider": "offline-organizer-fixture"})


class RescoringTests(unittest.TestCase):
    setUp = fixtures.FrontierPipelineTests.setUp
    paths = fixtures.FrontierPipelineTests.paths

    def source(self, *, rigorous=False, rejected=False):
        lane = "rigorous" if rigorous else "exploratory"
        paths = self.paths("sha256-r31-" + lane)
        old = paths.track.benchmark()
        old["cost_model"] = read_json(ROOT / "cost-models/collision-frontier-v4.json")
        def old_review(stage, review, _):
            if rejected and stage == "lane_evaluability":
                review["obligations"][1]["status"] = "unresolved"
        with patch.object(LaneTrack, "benchmark", return_value=old), fake_provider(old_review):
            self.assertEqual(pipeline.run_all(paths), 2 if rejected else 0)
        self.archives = paths.rescore_archives
        self.plan = self.root / "plan.json"
        self.enterContext(patch.object(rescore, "ARCHIVES", self.archives))
        self.enterContext(patch.object(rescore, "PLAN", self.plan))
        entry = archive(paths.evidence, paths.dossier, self.archives)
        atomic_write_json(self.plan, {"entries": [entry]})
        return paths, entry

    def run_cost(self, paths, client):
        with fake_provider(factory=lambda _: client), \
                patch.object(pipeline, "execute_experiments", side_effect=AssertionError("must inherit experiments")):
            self.assertEqual(pipeline.run_all(paths), 0)

    def review_artifact(self, paths, name):
        downloaded = self.root / name
        evidence = downloaded / "runs/fixture/judge-evidence.json"
        evidence.parent.mkdir(parents=True)
        shutil.copyfile(paths.evidence, evidence)
        shutil.copyfile(paths.dossier, downloaded / "judge-dossier.json")
        if paths.rescore_history.exists():
            shutil.copyfile(paths.rescore_history, downloaded / "rescore-history.json")
        return downloaded

    def test_workflow_artifact_carries_history_after_original_expires(self):
        paths, entry = self.source()
        original = self.review_artifact(paths, "original")
        shutil.rmtree(self.archives)
        rescore_artifacts.restore(paths, original)
        self.run_cost(paths, CostClient(21.0))
        self.assertEqual(set(read_json(paths.rescore_history)), {entry["source"]})
        second = archive(paths.evidence, paths.dossier, self.archives)
        latest = self.review_artifact(paths, "latest")
        shutil.rmtree(original)
        shutil.rmtree(self.archives)
        repinned = archive(latest / "runs/fixture/judge-evidence.json", latest / "judge-dossier.json",
                           self.root / "operator-cache")
        self.assertEqual(repinned, second)
        atomic_write_json(self.plan, {"entries": [second]})
        rescore_artifacts.restore(paths, latest)
        self.assertEqual({p.stem for p in self.archives.glob("*.json")}, {entry["source"], second["source"]})
        client = CostClient(21.0)
        self.run_cost(paths, client)
        self.assertEqual([stage for stage, _ in client.calls], ["lane_rescore"])
        self.assertEqual(len(client.calls[0][1]["review_context"]["judgments"]), 2)
        self.assertEqual(set(read_json(paths.rescore_history)), {entry["source"], second["source"]})

    def test_missing_or_changed_workflow_artifact_fails_before_review(self):
        paths, entry = self.source()
        downloaded = self.review_artifact(paths, "downloaded")
        shutil.rmtree(self.archives)
        with self.assertRaisesRegex(VerificationError, "missing prior judgment"):
            pipeline.run_intake(paths)
        with self.assertRaisesRegex(VerificationError, "missing or oversized"):
            rescore_artifacts.restore(paths, self.root / "expired")
        evidence = downloaded / "runs/fixture/judge-evidence.json"
        changed = read_json(evidence)
        changed["submission"]["proof_markdown_line_numbered"] += "tampered"
        atomic_write_json(evidence, changed)
        with self.assertRaisesRegex(VerificationError, "pinned packet checksum"):
            rescore_artifacts.restore(paths, downloaded)
        self.assertFalse(self.archives.exists())

    def test_latest_artifact_requires_its_complete_untampered_history(self):
        paths, _ = self.source()
        self.run_cost(paths, CostClient(21.0))
        second = archive(paths.evidence, paths.dossier, self.archives)
        downloaded = self.review_artifact(paths, "downloaded")
        atomic_write_json(self.plan, {"entries": [second]})
        shutil.rmtree(self.archives)
        history_file = downloaded / "rescore-history.json"
        history = read_json(history_file)
        history_file.unlink()
        with self.assertRaisesRegex(VerificationError, "missing prior judgment"):
            rescore_artifacts.restore(paths, downloaded)
        next(iter(history.values()))["evidence"]["schema_version"] = "tampered"
        atomic_write_json(history_file, history)
        with self.assertRaisesRegex(VerificationError, "history checksum"):
            rescore_artifacts.restore(paths, downloaded)
        self.assertFalse(self.archives.exists())

    def test_only_pinned_packages_select_positive_immutable_artifact_ids(self):
        paths, entry = self.source()
        references = self.root / "artifacts.json"
        with patch.object(rescore_artifacts, "ARTIFACTS", references):
            atomic_write_json(references, {entry["source"]: {"run_id": 42, "artifact_id": 73}})
            self.assertEqual(rescore_artifacts.selection(paths), entry)
            self.assertEqual(rescore_artifacts.artifact_reference(entry), {"run_id": 42, "artifact_id": 73})
            for bad in ({}, {entry["source"]: {"run_id": 42, "artifact_id": "73\n"}},
                        {entry["source"]: {"run_id": 42, "artifact_id": True}}):
                atomic_write_json(references, bad)
                with self.assertRaises(VerificationError):
                    rescore_artifacts.artifact_reference(entry)
            atomic_write_json(self.plan, {"entries": []})
            references.unlink()
            self.assertIsNone(rescore_artifacts.selection(paths))

    def test_retiring_completed_plan_routes_same_package_to_ordinary_review(self):
        paths, entry = self.source()
        entry["destination_config_sha256"] = "c" * 64
        atomic_write_json(self.plan, {"entries": [entry]})
        with self.assertRaisesRegex(VerificationError, "does not authorize"):
            rescore_artifacts.selection(paths)

        historical_plan = self.root / "history/completed-plan.json"
        historical_plan.parent.mkdir()
        historical_plan.write_bytes(self.plan.read_bytes())
        atomic_write_json(self.plan, {"entries": []})
        candidate_before = (paths.candidate / "claim.json").read_bytes()
        with patch.object(rescore, "load_archive", side_effect=AssertionError("retired history loaded")), \
                fake_provider() as (client, _):
            self.assertIsNone(rescore_artifacts.selection(paths))
            self.assertEqual(pipeline.run_all(paths), 0)

        self.assertEqual([stage for stage, _ in client.calls], list(fixtures.INITIAL_STAGES))
        self.assertNotIn("rescore_source", read_json(paths.evidence))
        self.assertNotIn("rescore", read_json(paths.dossier))
        self.assertNotIn("rescoreMode", read_json(paths.score)["metrics"])
        self.assertEqual(read_json(historical_plan), {"entries": [entry]})
        self.assertEqual((paths.candidate / "claim.json").read_bytes(), candidate_before)

    def test_reorg_supplies_original_reasoning_and_only_calls_one_judge(self):
        paths, entry = self.source()
        anchor = rescore.load_archive(entry["source"])
        client = CostClient(21.0)
        self.run_cost(paths, client)
        self.assertEqual([stage for stage, _ in client.calls], ["lane_rescore"])
        supplied = client.calls[0][1]["review_context"]
        self.assertEqual(supplied["judgments"][0]["dossier"], anchor["dossier"])
        self.assertEqual(len(supplied["judgments"]), 1)
        self.assertEqual(supplied["experiment_report"], anchor["evidence"]["submission"]["experiment_report"])
        self.assertEqual(client.calls[0][1]["submission"]["proof_markdown_line_numbered"],
                         anchor["evidence"]["submission"]["proof_markdown_line_numbered"])
        result = read_json(paths.score)
        expected = 21.0
        self.assertAlmostEqual(result["score"], expected)
        self.assertEqual(result["metrics"]["declaredTimeLog2"], 128)
        self.assertEqual(result["metrics"]["declaredOperationWeights"], UNIT_WEIGHTS)
        self.assertNotIn("preprocessingLog2", result["metrics"])
        self.assertEqual(result["metrics"]["declaredPreprocessingLog2"], 0)
        self.assertEqual(result["metrics"]["rescoreSourceSha256"], entry["source"])
        self.assertEqual(read_json(paths.dossier)["lanes"]["exploratory"], anchor["dossier"]["lanes"]["exploratory"])
        self.assertEqual(read_json(paths.dossier)["lanes"]["rigorous"]["status"], "not_reviewed")
        self.assertNotIn("resourceLedger", result["metrics"])
        self.assertEqual(result["metrics"]["rescoreMode"], "policy_change")

    def test_repeated_reorgs_reuse_reasoning_and_retain_history(self):
        paths, entry = self.source()
        self.run_cost(paths, CostClient(21.0))
        entry2 = archive(paths.evidence, paths.dossier, self.archives)
        updated = paths.track.benchmark()
        updated["cost_model"]["reference_operation_costs"]["sha256-r31"] = 1070
        updated["cost_model"]["operation_weights"]["word_operation"] = 1 / 1070
        with patch.object(LaneTrack, "benchmark", return_value=updated):
            entry2["destination_config_sha256"] = paths.track.config_sha256()
            atomic_write_json(self.plan, {"entries": [entry2]})
            client = CostClient(21.0)
            self.run_cost(paths, client)
            supplied = client.calls[0][1]["review_context"]
            self.assertEqual(supplied["judgments"][0]["dossier"], rescore.load_archive(entry["source"])["dossier"])
            self.assertEqual(len(supplied["judgments"]), 2)
            self.assertEqual(supplied["judgments"][1]["dossier"]["rescore"]["review"]["time_log2"], 21.0)
            self.assertEqual(read_json(paths.score)["score"], 21.0)
            self.assertTrue(supplied["score_policy_changed"])
        updated["qualification_policy"]["sha256"] = "e" * 64
        with patch.object(LaneTrack, "benchmark", return_value=updated):
            entry2["destination_config_sha256"] = paths.track.config_sha256()
            atomic_write_json(self.plan, {"entries": [entry2]})
            # A new prompt/configuration pin does not itself change the score policy.
            self.run_cost(paths, CostClient(21.0))
            self.assertEqual(read_json(paths.score)["score"], 21.0)
            self.assertEqual(read_json(paths.score)["metrics"]["rescoreMode"], "policy_change")

    def test_opaque_legacy_bound_survives_discount_without_fabricated_counts(self):
        paths, _ = self.source()
        self.run_cost(paths, CostClient())
        result = read_json(paths.score)
        self.assertEqual(result["score"], 128)
        self.assertNotIn("resourceLedger", result["metrics"])

    def test_same_policy_preserves_latest_score_even_if_reviewer_tightens_it(self):
        paths, _ = self.source()
        self.run_cost(paths, CostClient(66.28))
        entry = archive(paths.evidence, paths.dossier, self.archives)
        changed = paths.track.benchmark()
        changed["qualification_policy"]["sha256"] = "e" * 64
        with patch.object(LaneTrack, "benchmark", return_value=changed):
            entry["destination_config_sha256"] = paths.track.config_sha256()
            atomic_write_json(self.plan, {"entries": [entry]})
            client = CostClient(64)
            self.run_cost(paths, client)
            result = read_json(paths.score)
            self.assertEqual(result["score"], 66.28)
            self.assertEqual(result["metrics"]["rescoreMode"], "preserve_score")
            self.assertFalse(client.calls[0][1]["review_context"]["score_policy_changed"])
            self.assertEqual(read_json(paths.dossier)["rescore"]["review"]["time_log2"], 66.28)

    def test_same_policy_preserves_original_claim_on_first_reorg(self):
        paths, _ = self.source()
        # Make a fresh ordinary v5 judgment, then pin it for an unrelated reorg.
        atomic_write_json(self.plan, {"entries": []})
        with fake_provider():
            self.assertEqual(pipeline.run_all(paths), 0)
        entry = archive(paths.evidence, paths.dossier, self.archives)
        atomic_write_json(self.plan, {"entries": [entry]})
        self.run_cost(paths, CostClient(100))
        self.assertEqual(read_json(paths.score)["score"], 128)
        self.assertEqual(read_json(paths.score)["metrics"]["rescoreMode"], "preserve_score")

    def test_policy_identity_ignores_other_targets_and_judge_configuration(self):
        evidence = {"benchmark": self.paths().track.benchmark()}
        changed = deepcopy(evidence)
        changed["benchmark"]["cost_model"]["reference_operation_costs"]["md5-s63"] += 1
        changed["benchmark"]["qualification_policy"]["sha256"] = "f" * 64
        self.assertEqual(rescore.scoring_policy(evidence), rescore.scoring_policy(changed))
        changed["benchmark"]["cost_model"]["operation_weights"]["word_operation"] *= 2
        self.assertNotEqual(rescore.scoring_policy(evidence), rescore.scoring_policy(changed))
        changed = deepcopy(evidence)
        changed["benchmark"]["cost_model"]["id"] = "collision-frontier-v6"
        self.assertNotEqual(rescore.scoring_policy(evidence), rescore.scoring_policy(changed))

    def reject_reorg_then_reconsider(self, *, change_prices):
        paths, _ = self.source()
        self.run_cost(paths, CostClient(66.28))
        prior = read_json(paths.dossier)
        entry = archive(paths.evidence, paths.dossier, self.archives)
        changed = paths.track.benchmark()
        changed["qualification_policy"]["sha256"] = "e" * 64
        if change_prices:
            changed["cost_model"]["operation_weights"]["word_operation"] *= 2
        with patch.object(LaneTrack, "benchmark", return_value=changed):
            entry["destination_config_sha256"] = paths.track.config_sha256()
            atomic_write_json(self.plan, {"entries": [entry]})
            client = CostClient(mutate=lambda r: r.update(
                status="rejected", time_log2=None,
                calculation_trace=["The previous argument does not meet the current criterion; proof.md:L1-L2."]))
            with fake_provider(factory=lambda _: client):
                self.assertEqual(pipeline.run_all(paths), 2)
            supplied = client.calls[0][1]["review_context"]
            self.assertEqual(supplied["judgments"][-1]["dossier"], prior)
            self.assertEqual(supplied["score_policy_changed"], change_prices)
            dossier = read_json(paths.dossier)
            self.assertEqual(dossier["aggregate"]["status"], "reorg_rejected")
            self.assertFalse(dossier["lanes"]["exploratory"]["eligible"])
            self.assertEqual(dossier["lanes"]["rigorous"]["status"], "not_reviewed")
            self.assertFalse(paths.score.exists())
            with self.assertRaises(VerificationError):
                pipeline.run_score(paths)
            self.assertFalse(paths.score.exists())

            # A rejection is a full historical judgment, not an infrastructure failure.
            latest = archive(paths.evidence, paths.dossier, self.archives)
            atomic_write_json(self.plan, {"entries": [latest]})
            reconsidered = CostClient(12)
            self.run_cost(paths, reconsidered)
            supplied = reconsidered.calls[0][1]["review_context"]
            self.assertEqual(supplied["judgments"][-1]["dossier"]["rescore"]["review"]["status"], "rejected")
            self.assertEqual(read_json(paths.score)["score"], 12 if change_prices else 66.28)

    def test_validity_prompt_change_can_reject_and_accept_without_repricing(self):
        self.reject_reorg_then_reconsider(change_prices=False)

    def test_price_change_can_reject_and_later_accept_with_a_revised_score(self):
        self.reject_reorg_then_reconsider(change_prices=True)

    def test_stale_pin_and_nonpricing_semantic_change_fail_before_model_call(self):
        paths, entry = self.source()
        self.run_cost(paths, CostClient(21.0))
        entry = archive(paths.evidence, paths.dossier, self.archives)
        atomic_write_json(self.plan, {"entries": [entry]})
        changed = paths.track.benchmark()
        changed["cost_model"]["minimum_success_probability"] = 0.2
        with patch.object(LaneTrack, "benchmark", return_value=changed):
            with self.assertRaisesRegex(VerificationError, "current configuration"):
                pipeline.run_intake(paths)
            entry["destination_config_sha256"] = paths.track.config_sha256()
            atomic_write_json(self.plan, {"entries": [entry]})
            with self.assertRaisesRegex(VerificationError, "new public cost-model ID"):
                pipeline.run_intake(paths)

    def test_archive_tampering_and_duplicate_pins_are_rejected(self):
        paths, entry = self.source()
        archive_path = self.archives / (entry["source"] + ".json")
        packet = read_json(archive_path)
        packet["dossier"]["claim"]["claim"]["success_probability"] = 1
        atomic_write_json(archive_path, packet)
        with self.assertRaisesRegex(VerificationError, "checksum mismatch"):
            pipeline.run_intake(paths)
        atomic_write_json(self.plan, {"entries": [entry, entry]})
        with self.assertRaisesRegex(VerificationError, "duplicate"):
            pipeline.run_intake(paths)

    def test_tampered_historical_decision_fails_integrity_checks(self):
        paths, entry = self.source()
        packet = rescore.load_archive(entry["source"])
        packet["dossier"]["lanes"]["exploratory"]["eligible"] = False
        # Recorded decisions remain covered by the trusted artifact seal.
        with self.assertRaises(VerificationError):
            rescore.verify_packet(packet)

    def test_historical_judgment_does_not_have_to_pass_todays_validators(self):
        paths, _ = self.source()
        with patch("judge.paired_review.aggregate_paired_reviews", side_effect=AssertionError("must not replay old qualification")):
            self.run_cost(paths, CostClient(66.28))
        self.assertEqual(read_json(paths.score)["score"], 66.28)

    def test_original_rejection_can_supply_reasoning_for_a_new_decision(self):
        paths, _ = self.source(rejected=True)
        client = CostClient(66.28)
        self.run_cost(paths, client)
        previous = client.calls[0][1]["review_context"]["judgments"][0]["dossier"]
        self.assertEqual(previous["aggregate"]["status"], "not_evaluable")
        self.assertEqual(read_json(paths.score)["score"], 66.28)

    def test_ledger_reorg_is_excluded_instead_of_reinterpreted(self):
        paths, _ = self.source()
        self.run_cost(paths, CostClient(66.28))
        packet = {"evidence": read_json(paths.evidence), "dossier": read_json(paths.dossier)}
        dossier = packet["dossier"]
        dossier["rescore"]["review"]["schema_version"] = "review-rescore-v1"
        core = {k: v for k, v in dossier.items() if k not in {"aggregate", "judge_configuration"}}
        core["judge_configuration_sha256"] = rescore.digest(dossier["judge_configuration"])
        dossier["aggregate"]["dossier_sha256"] = rescore.digest(core)
        with self.assertRaisesRegex(VerificationError, "pin the original ordinary judgment"):
            rescore.verify_packet(packet, self.archives)

    def test_final_score_gate_still_enforces_the_new_result(self):
        paths, _ = self.source()
        self.run_cost(paths, CostClient(66.28))
        latest = archive(paths.evidence, paths.dossier, self.archives)
        atomic_write_json(self.plan, {"entries": [latest]})
        self.run_cost(paths, CostClient(20))
        evidence, dossier = read_json(paths.evidence), read_json(paths.dossier)
        dossier["rescore"]["review"]["time_log2"] = 20
        with self.assertRaisesRegex(VerificationError, "preserve the previous score"):
            rescore.score_result(evidence, dossier, self.archives)
        dossier["rescore"]["review"]["binding"]["package_sha256"] = "0" * 64
        with self.assertRaisesRegex(VerificationError, "mismatched binding"):
            rescore.score_result(evidence, dossier, self.archives)

    def test_incomplete_cost_review_retains_history_and_emits_no_score(self):
        paths, entry = self.source()
        anchor = rescore.load_archive(entry["source"])
        client = CostClient(mutate=lambda review: review.update(status="needs_evidence", time_log2=None))
        with fake_provider(factory=lambda _: client):
            self.assertEqual(pipeline.run_all(paths), 2)
        self.assertFalse(paths.score.exists())
        self.assertEqual(read_json(paths.aggregate)["status"], "rescore_needs_evidence")
        self.assertEqual(read_json(paths.dossier)["rescore"]["review"]["status"], "needs_evidence")
        self.assertEqual(rescore.load_archive(entry["source"]), anchor)

    def test_reorg_cannot_add_success_probability_or_emit_invalid_score(self):
        paths, _ = self.source(rigorous=True)
        self.assertEqual(pipeline.run_intake(paths), 0)
        evidence = read_json(paths.evidence)
        for mutation in (lambda r: r.update(success_probability=1),
                         lambda r: r.update(time_log2=float("nan")),
                         lambda r: r.update(time_log2=10**1000),
                         lambda r: r.update(time_log2=True)):
            client = CostClient(21.0, mutation)
            with self.assertRaises(ValueError):
                rescore.run_review(evidence, rescore.find_source(paths.track, evidence["submission"]["intake_report"]["package_sha256"]), client)

    def test_obsolete_solver_ledger_has_a_clear_intake_error(self):
        paths = self.paths()
        claim = read_json(paths.candidate / "claim.json")
        validate_claim(claim, track=paths.track)
        claim["resource_ledger"] = {"obsolete": "Remove this field and explain the calculation in proof.md."}
        with self.assertRaisesRegex(VerificationError, "resource_ledger"):
            validate_claim(claim, track=paths.track)

    def test_every_active_target_has_a_reproducible_price(self):
        estimates = reference_costs()
        self.assertEqual(estimates, read_json(ROOT / "cost-models/collision-frontier-v5.json")["reference_operation_costs"])
        for track in frontier_tracks():
            weights = track.benchmark()["cost_model"]["operation_weights"]
            self.assertEqual(weights["target_compression"], 1)
            self.assertEqual(weights["word_operation"], 1 / estimates[track.target_id])

    def test_provider_boundaries_support_final_cost_reviews_and_reject_bad_scores(self):
        from judge.tests import test_provider_adapter as openrouter, test_bedrock_adapter as bedrock
        from judge.tests.helpers import provider_response
        from judge.provider_adapter import JudgeInfraError, _schema_for_stage
        from judge.tests.helpers import fixture_evidence
        evidence = {"review_context": {"binding": rescore.evidence_binding(fixture_evidence())}}
        record = CostClient(21.0).review("lane_rescore", evidence).review
        schema = _schema_for_stage("lane_rescore")
        self.assertNotIn("$ref", json.dumps(schema))
        for make_client, response in ((openrouter.client, provider_response),
                                      (bedrock.client, bedrock.bedrock_response),
                                      (bedrock.sol_client, bedrock.sol_response)):
            transport = openrouter.FakeTransport([response(record)])
            result = make_client(transport).review("lane_rescore", evidence)
            self.assertEqual(result.review, record)
            body = json.loads(transport.calls[0]["body"])
            self.assertNotIn("tools", body)
            self.assertIn("previous_score", json.dumps(body))
            for status in ("rejected", "needs_evidence"):
                declined = {**record, "status": status, "time_log2": None}
                transport = openrouter.FakeTransport([response(declined)])
                result = make_client(transport).review("lane_rescore", evidence)
                self.assertEqual(result.review, declined)
                self.assertEqual(len(transport.calls), 1)
            bad = deepcopy(record)
            bad["time_log2"] = -1
            with self.assertRaises(JudgeInfraError):
                make_client(openrouter.FakeTransport([response(bad)] * 3)).review("lane_rescore", evidence)
