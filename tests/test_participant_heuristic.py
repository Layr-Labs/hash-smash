"""Participant Python -> trusted evidence -> paired review -> isolated score.

Offline cases replace only Docker transport and the external model. The opt-in
case executes the immutable participant fixture in the real bounded sandbox.
Participant source is never imported or executed by the host test process.
"""

from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
import hashlib
import io
import json
import os
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch

from experiments import ExperimentSetupError
from judge.bedrock_adapter import BedrockConfig
from judge.lanes import INITIAL_STAGES
from judge.provider_adapter import JudgeInfraError
from scripts import test_participant_heuristic as driver
from tests.test_paired_judges import FixtureClient
from verifier.errors import VerificationError
from verifier.hash_functions import digest
from verifier.io import atomic_write_json
from verifier.frontier_tracks import get_frontier_track


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode()


def reference_output(request):
    """Independent organizer reconstruction, NOT execution of submitted source.

    Use a dictionary rather than the submitted list scan. This checks the first
    duplicate and every failure as well as returned-pair validity. It does not
    validate the submitted algorithm's resource ledger or population heuristic.
    """
    rows = []
    for trial in request["trials"]:
        seed = bytes.fromhex(trial["seed"])
        first_seen = {}
        pair = (None, None)
        for counter in range(256):
            output = hashlib.sha256(b"HS-BATCH-v1" + seed + struct.pack("<H", counter)).digest()
            value = struct.unpack("<H", output[:2])[0]
            if value in first_seen:
                pair = tuple(struct.pack("<16I", value, *([0] * 7), index, *([0] * 7)).hex()
                             for index in (first_seen[value], counter))
                break
            first_seen[value] = counter
        rows.append({"trial": trial["trial"], "message_a_hex": pair[0], "message_b_hex": pair[1]})
    return {"schema_version": 1, "trials": rows}


def audit_saved_report(report):
    """Reconstruct all fixed seeds and outcomes, independently of runner helpers."""
    if report["target_profile"] != driver.TARGET_PROFILE or report["holdout_nonce"] is not None:
        raise AssertionError("unexpected calibration target or seed protocol")
    seed_material = canonical({"domain": "hashsmash-experiments-v1", "seed": report["seed"],
                               "holdout_nonce": None, "target_config_sha256": report["target_config_sha256"]})
    measured = report["experiments"][0]
    if measured["id"] != driver.EXPERIMENT_ID or measured["trials"] != 256:
        raise AssertionError("unexpected calibration trial set")
    request = {"trials": [{"trial": index, "seed": hashlib.sha256(
        seed_material + canonical([driver.EXPERIMENT_ID, index])).hexdigest()} for index in range(256)]}
    expected = reference_output(request)["trials"]
    actual = measured["checked_trials"]
    if len(actual) != len(expected):
        raise AssertionError("omitted trials")
    successes = 0
    for expected_row, row in zip(expected, actual):
        if row["trial"] != expected_row["trial"]:
            raise AssertionError("changed trial ordering")
        if expected_row["message_a_hex"] is None:
            if row.get("success") is not False or row.get("reason") != "no_pair_returned":
                raise AssertionError("incorrect failure outcome")
        else:
            for key in ("message_a_hex", "message_b_hex"):
                if row.get(key) != expected_row[key]:
                    raise AssertionError("first duplicate pair differs from reference")
            a, b = (bytes.fromhex(row[key]) for key in ("message_a_hex", "message_b_hex"))
            da, db = digest(a, "md5", 8), digest(b, "md5", 8)
            if (a == b or da != db or row.get("success") is not True
                    or row.get("full_collision") is not True
                    or row.get("digest_a_hex") != da.hex() or row.get("digest_b_hex") != db.hex()):
                raise AssertionError("incorrect full collision")
            successes += 1
    if successes != measured["successes"]:
        raise AssertionError("incorrect success count")
    return {"trials_checked": 256, "full_collisions": successes, "failures_checked": 256 - successes,
            "method": "Independent dictionary-based seed/sampler reconstruction and trusted full-digest check",
            "scope": "Finite execution outcomes only; no population probability or resource-cost proof"}


def plausible_fixture_review(stage, review, evidence):
    if stage in {"lane_cryptanalysis", "lane_experiments"}:
        review["heuristics"] = [{
            "id": item["id"], "statement": item["statement"], "status": "plausible",
            "tested_scope": item["scope"], "extrapolated_scope": item["extrapolation"],
            "sensitivity": "Offline routing fixture; finite observations do not establish the population lower bound.",
            "evidence": item["evidence_ids"],
        } for item in evidence["submission"]["intake_report"]["claim"]["heuristics"]]
    if stage == "lane_cost":
        review["cost_reconstruction"]["calculation_trace"] = ["Submitted upper bounds: 23 + 17 = 40."]


class ParticipantHeuristicTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="hashsmash-participant-test-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.run = self.root / "fresh-run"
        self.enterContext(patch.dict(os.environ, {**{key: "" for key in driver.CREDENTIAL_NAMES},
                                                 "HASHSMASH_EXPERIMENT_HOLDOUT_NONCE": ""}))
        os.environ.pop("HASHSMASH_EXPERIMENT_HOLDOUT_NONCE", None)
        self.log = io.StringIO()
        self.enterContext(redirect_stdout(self.log))
        self.enterContext(redirect_stderr(self.log))

    def prepare(self):
        calls = []
        def transport(source, request, limits, image):
            calls.append(deepcopy(request))
            self.assertEqual(source, (driver.FIXTURE_ROOT / "candidate/experiments/birthday.py").read_bytes())
            self.assertEqual(request["target_profile"], driver.TARGET_PROFILE)
            return canonical(reference_output(request))
        with patch("experiments.runner._run_docker", side_effect=transport):
            summary = driver.prepare_run(self.run)
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0], calls[1])
        return summary

    def review(self, mutate=plausible_fixture_review):
        client = FixtureClient(mutate)
        config = BedrockConfig(api_key="offline-fixture-not-a-secret", model="us.openai.gpt-5.6-sol")
        summary = driver.review_run(self.run, config=config, client_factory=lambda _: client)
        return summary, client

    def test_isolated_test_schema_changes_only_target_enum_and_is_not_registered(self):
        schema = json.loads((driver.REPO_ROOT / "schemas/claim-frontier-v3.schema.json").read_text())
        schema["properties"]["target_profile"]["enum"] = [driver.TARGET_PROFILE]
        self.assertEqual(driver.instantiated_claim_schema(), schema)
        with self.assertRaises(VerificationError):
            get_frontier_track(driver.TRACK_ID)
        paths = driver.paths_for(self.run)
        self.assertTrue(paths.candidate.is_relative_to(self.run))
        self.assertTrue(paths.score.is_relative_to(self.run))
        self.assertFalse(paths.score.is_relative_to(paths.candidate))

    def test_genuine_intake_saved_evidence_review_and_score_gates(self):
        summary = self.prepare()
        self.assertEqual(summary["trials"], 256)
        self.assertGreater(summary["full_collisions"], 0)
        self.assertGreater(summary["no_pair_returned"], 0)
        paths = driver.paths_for(self.run)
        report = json.loads((paths.work / "experiment-report.json").read_text())["execution"]
        audit = audit_saved_report(report)
        self.assertEqual(audit["full_collisions"], summary["full_collisions"])
        self.assertEqual(report["experiments"][0]["predicate_trust"], "organizer_recomputed")
        self.assertNotIn("interval", report["experiments"][0])
        evidence_before = paths.evidence.read_bytes()
        with patch("experiments.runner._run_docker", side_effect=AssertionError("review must not execute")) as execute:
            summary, client = self.review()
        execute.assert_not_called()
        self.assertEqual(paths.evidence.read_bytes(), evidence_before)
        result = summary["review"]
        self.assertTrue(result["outcome_matches_expected"])
        self.assertEqual(result["actual_stage_calls"], 4)
        self.assertEqual(result["score_exit_code"], 0)
        self.assertEqual([stage for stage, _ in client.calls], list(INITIAL_STAGES))
        for stage, evidence in client.calls:
            view = evidence["submission"]["experiment_report"]["execution"]
            self.assertEqual(view["full_report_sha256"], report["report_sha256"])
            self.assertEqual(view["experiments"][0]["successes"], summary["full_collisions"])
            self.assertEqual(view["sources"][0]["untrusted_source_text"], report["sources"][0]["untrusted_source_text"])
        score = json.loads(paths.score.read_text())
        self.assertEqual(score["score"], 40)
        self.assertFalse(score["metrics"]["humanAccepted"])
        self.assertEqual(score["metrics"]["trackId"], driver.TRACK_ID)
        dossier = json.loads(paths.dossier.read_text())
        self.assertEqual(dossier["judge_configuration"]["judge"]["max_attempts"], 1)
        self.assertNotIn("offline-fixture-not-a-secret", json.dumps(dossier))

    def test_all_known_credential_sources_rejected_before_preparation(self):
        for name in driver.CREDENTIAL_NAMES:
            with self.subTest(name=name), patch.dict(os.environ, {name: "offline-fixture"}):
                with self.assertRaisesRegex(VerificationError, "credential-bearing"):
                    driver.prepare_run(self.run)
                self.assertFalse(self.run.exists())

    def test_holdout_override_refused_and_existing_directory_not_overwritten(self):
        with patch.dict(os.environ, {"HASHSMASH_EXPERIMENT_HOLDOUT_NONCE": "unapproved-seed"}):
            with self.assertRaises(VerificationError):
                driver.prepare_run(self.run)
        self.run.mkdir()
        (self.run / "keep.txt").write_text("existing")
        with self.assertRaises(VerificationError):
            driver.prepare_run(self.run)
        self.assertEqual((self.run / "keep.txt").read_text(), "existing")

    def test_setup_failure_never_prepares_a_reviewable_artifact(self):
        with patch("experiments.runner._run_docker", side_effect=ExperimentSetupError("offline Docker unavailable")):
            with self.assertRaises(ExperimentSetupError):
                driver.prepare_run(self.run)
        with self.assertRaises(VerificationError):
            self.review()
        self.assertFalse(driver.paths_for(self.run).score.exists())

    def test_tampered_source_claim_report_evidence_or_schema_never_reaches_judge(self):
        for kind in ("source", "claim", "report", "evidence", "schema", "prepared"):
            with self.subTest(kind=kind):
                self.run = self.root / kind
                self.prepare()
                paths = driver.paths_for(self.run)
                if kind == "source":
                    with (paths.candidate / "experiments/birthday.py").open("a") as file:
                        file.write("\n# changed after preparation\n")
                else:
                    target = {"claim": paths.candidate / "claim.json", "report": paths.work / "experiment-report.json",
                              "evidence": paths.evidence, "schema": self.run / "claim-test-instance.schema.json",
                              "prepared": self.run / driver.PREPARE_FILENAME}[kind]
                    value = json.loads(target.read_text())
                    if kind == "claim":
                        value["claim"]["time_log2"] -= 1
                    elif kind == "report":
                        value["execution"]["experiments"][0]["successes"] += 1
                    elif kind == "prepared":
                        value["package_sha256"] = "0" * 64
                    else:
                        value["tampered"] = True
                    atomic_write_json(target, value)
                factory = unittest.mock.Mock(side_effect=AssertionError("provider must not be reached"))
                with self.assertRaises(VerificationError):
                    driver.review_run(self.run, client_factory=factory)
                factory.assert_not_called()
                self.assertFalse(paths.score.exists())

    def test_repeated_review_refused_and_original_dossier_preserved(self):
        self.prepare()
        self.review()
        before = driver.paths_for(self.run).dossier.read_bytes()
        with self.assertRaisesRegex(VerificationError, "already attempted"):
            self.review()
        self.assertEqual(driver.paths_for(self.run).dossier.read_bytes(), before)

    def test_not_evaluable_produces_no_diagnostic_score(self):
        self.prepare()
        def withheld(stage, review, evidence):
            plausible_fixture_review(stage, review, evidence)
            if stage == "lane_evaluability":
                review["obligations"][0]["status"] = "unresolved"
        result, _ = self.review(withheld)
        self.assertEqual(result["review"]["outcomes"]["exploratory"], "not_evaluable")
        self.assertFalse(result["review"]["diagnostic_score_emitted"])
        self.assertEqual(result["review"]["score_exit_code"], 2)

    def test_provider_failure_is_not_a_negative_scientific_result(self):
        self.prepare()
        def unavailable(stage, review, evidence):
            raise JudgeInfraError("offline provider failed")
        result, _ = self.review(unavailable)
        self.assertEqual(result["review"]["judge_exit_code"], 3)
        self.assertEqual(result["review"]["outcomes"]["exploratory"], "infra_failed")
        self.assertFalse(result["review"]["diagnostic_score_emitted"])

    def test_independent_audit_detects_suppressed_success(self):
        self.prepare()
        paths = driver.paths_for(self.run)
        report = json.loads((paths.work / "experiment-report.json").read_text())["execution"]
        measured = report["experiments"][0]
        index = next(i for i, row in enumerate(measured["checked_trials"]) if row["success"])
        measured["checked_trials"][index] = {"trial": index, "success": False, "reason": "no_pair_returned"}
        measured["successes"] -= 1
        with self.assertRaises(AssertionError):
            audit_saved_report(report)

    @unittest.skipUnless(os.environ.get("HASHSMASH_TEST_DOCKER") == "1", "opt-in real Docker integration")
    def test_real_participant_python_then_offline_judges(self):
        summary = driver.prepare_run(self.run)
        paths = driver.paths_for(self.run)
        report = json.loads((paths.work / "experiment-report.json").read_text())["execution"]
        audited = audit_saved_report(report)
        self.assertGreater(audited["full_collisions"], 0)
        self.assertGreater(audited["failures_checked"], 0)
        self.assertTrue(summary["reproducibility"]["stdout_byte_identical"])
        result, _ = self.review()
        self.assertTrue(result["review"]["outcome_matches_expected"])


if __name__ == "__main__":
    unittest.main()
