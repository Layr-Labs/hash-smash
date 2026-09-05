"""End-to-end paired-lane tests using organizer fixtures and fake reviewers only.

No mutable solver draft is read, modified or submitted to a provider. The optional
Docker case executes an organizer probe and makes no cryptanalytic claim.
"""

from contextlib import contextmanager, redirect_stderr, redirect_stdout
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from judge.bedrock_adapter import BedrockConfig
from judge.lanes import INITIAL_STAGES, LANE_STAGES
from scripts import hashsmash_pipeline as pipeline
from scripts.stage_yukon_score import stage_score
from tests.test_experiments import addition, program
from tests.helpers import candidate_fixture
from tests.test_paired_judges import FixtureClient, add_fatal
from verifier.errors import VerificationError
from verifier.frontier_tracks import catalog, frontier_tracks, planned_slots
from verifier.intake import validate_candidate
from verifier.io import atomic_write_json, sha256_bytes
from verifier.frontier_tracks import ROOT, get_frontier_track


def read_json(path):
    return json.loads(path.read_text())


def add_experiment(candidate, manifest, source=None, *, heuristic=False):
    claim = read_json(candidate / "claim.json")
    claim["experiment_manifest"] = "experiments/manifest.json"
    if heuristic:
        claim["heuristics"] = [{
            "id": "h1", "statement": "Organizer fixture local calibration premise.",
            "role": "score-critical", "scope": "One-bit finite addition space.",
            "extrapolation": "None asserted by this test; fake reviews exercise routing only.",
            "evidence_ids": ["experiment:" + manifest["experiments"][0]["id"]],
            "limitations": "A fixture is not a complete collision attack or cost proof.",
        }]
    atomic_write_json(candidate / "claim.json", claim)
    atomic_write_json(candidate / "experiments" / "manifest.json", manifest)
    if source is not None:
        (candidate / manifest["experiments"][0]["program"]).write_bytes(source)


def establish_fixture_heuristics(stage, review, evidence):
    if stage in {"lane_cryptanalysis", "lane_experiments"}:
        review["heuristics"] = [{
            "id": h["id"], "statement": h["statement"], "status": "established",
            "tested_scope": h["scope"], "extrapolated_scope": h["extrapolation"],
            "sensitivity": "Organizer synthetic reviewer, no scientific assertion.",
            "evidence": h["evidence_ids"],
        } for h in evidence["submission"]["intake_report"]["claim"]["heuristics"]]


@contextmanager
def fake_provider(mutate=None, *, mode="single", factory=None):
    client = FixtureClient(mutate)
    config = BedrockConfig(api_key="offline-fixture-no-credential", model="us.openai.gpt-5.6-sol")
    maker = factory or (lambda _: client)
    with patch.dict(os.environ, {"HASHSMASH_JUDGE_MODE": mode}, clear=False), \
         patch.object(pipeline, "_provider_from_env", return_value=("bedrock", config, maker)) as provider:
        yield client, provider


class FrontierPipelineTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="hashsmash-frontier-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.log = io.StringIO()
        self.stdout = redirect_stdout(self.log)
        self.stderr = redirect_stderr(self.log)
        self.stdout.__enter__()
        self.stderr.__enter__()
        self.addCleanup(self.stdout.__exit__, None, None, None)
        self.addCleanup(self.stderr.__exit__, None, None, None)

    def paths(self, track_id="sha256-r31-exploratory", *, ready=True, suffix=""):
        track = get_frontier_track(track_id)
        root = self.root / suffix if suffix else self.root
        candidate = candidate_fixture(root, track, ready=ready)
        return pipeline.RunPaths.for_track(track, state_root=root / "state", candidate=candidate)

    def test_every_active_track_runs_end_to_end_with_independent_bound_outputs(self):
        tracks = frontier_tracks()
        self.assertEqual(len(tracks), 16)
        manifest = read_json(ROOT / "benchmark.json")
        atomic_write_json(self.root / "benchmark.json", manifest)
        manifest_tracks = {row["name"]: row for row in manifest["tracks"]}
        outputs, configs, packages = set(), set(), set()
        for track in tracks:
            with self.subTest(track=track.id):
                paths = self.paths(track.id)
                paths = pipeline.RunPaths.for_track(
                    track, state_root=self.root / track.state_root.relative_to(ROOT),
                    candidate=paths.candidate,
                )
                with fake_provider() as (client, _):
                    self.assertEqual(pipeline.run_all(paths), 0)
                score, aggregate = read_json(paths.score), read_json(paths.aggregate)
                self.assertEqual(score["score"], track.nominal_score)
                self.assertEqual(score["metrics"]["reviewStatus"], track.accepted_status)
                self.assertEqual(score["metrics"]["lane"], track.lane)
                self.assertFalse(score["metrics"]["referenceIsQualifiedBaseline"])
                self.assertFalse(score["metrics"]["improvesNominalReference"])
                self.assertFalse(score["metrics"]["humanAccepted"])
                self.assertEqual(aggregate["target_config_sha256"], track.config_sha256())
                self.assertEqual([stage for stage, _ in client.calls], list(INITIAL_STAGES))
                # Exercise the actual manifest-to-pipeline-to-upload handoff for
                # every track. Yukon reads this exact ZIP entry, including lanes/.
                score_path = manifest_tracks[track.id]["scorePath"]
                artifact = self.root / "artifacts" / track.id
                staged = stage_score(self.root, score_path, artifact)
                archive = io.BytesIO()
                with zipfile.ZipFile(archive, "w") as zipped:
                    zipped.write(staged, staged.relative_to(artifact).as_posix())
                with zipfile.ZipFile(archive) as zipped:
                    self.assertEqual(zipped.namelist(), [score_path])
                    self.assertEqual(json.loads(zipped.read(score_path)), score)
                outputs.add(paths.score)
                configs.add(score["metrics"]["targetConfigSha256"])
                packages.add(score["metrics"]["inputPackageSha256"])
        self.assertEqual(len(outputs), 16)
        self.assertEqual(len(configs), 16)
        self.assertEqual(len(packages), 16)

    def test_catalog_and_yukon_manifests_preserve_pending_slots_and_literal_routes(self):
        slots = planned_slots()
        self.assertEqual(len(slots), 28)
        self.assertEqual(sum(slot["rounds"] is None for slot in slots), 12)
        families = {family["id"]: family for family in catalog()["families"]}
        self.assertEqual(families["sha256"]["round_pair"], [31, 32])
        for family in ("md5", "sha1"):
            self.assertEqual(families[family]["selection_status"], "full_round_control")
            self.assertIsNone(families[family]["first_unbroken_round"])
        manifest_ids = set()
        manifest = read_json(ROOT / "benchmark.json")
        self.assertEqual(manifest["schemaVersion"], 2)
        self.assertEqual(manifest["name"], "hashsmash")
        self.assertEqual(len(manifest["tracks"]), 16)
        for row in manifest["tracks"]:
            track = get_frontier_track(row["name"])
            self.assertEqual(row["benchmarkCommand"], ["python3", "scripts/hashsmash_pipeline.py", "all", "--track", track.id])
            self.assertEqual(row["setupCommand"], ["bash", ".yukon/setup.sh"])
            self.assertEqual(row["editablePaths"], [f"lanes/{track.lane}/candidates/{track.target_id}"])
            self.assertEqual((ROOT / row["scorePath"]).resolve(), pipeline.RunPaths.for_track(track).score.resolve())
            self.assertEqual(row["runner"]["workflow"], track.id + ".yml")
            self.assertEqual(row["direction"], "-")
            manifest_ids.add(track.id)
        for lane in ("exploratory", "rigorous"):
            self.assertFalse((ROOT / "lanes" / lane / "benchmark.json").exists())
        self.assertEqual(manifest_ids, {track.id for track in frontier_tracks()})
        for undefined in (
            "poseidon-r8-exploratory", "blake3-r6-rigorous", "keccak800-r6-exploratory",
            "md5-s8", "md5-s24", "md5-s64", "sha1-r8", "sha1-r40", "sha1-r80",
            "sha256-r8", "sha256-r24", "sha256-r64",
        ):
            with self.subTest(undefined=undefined), self.assertRaises(VerificationError):
                get_frontier_track(undefined)

    def test_supported_baseline_above_nominal_can_score_without_claiming_improvement(self):
        for lane in ("exploratory", "rigorous"):
            with self.subTest(lane=lane):
                paths = self.paths(f"sha1-r80-{lane}")
                claim = read_json(paths.candidate / "claim.json")
                claim["claim"].update(time_log2=94, memory_log2_bytes=88)
                atomic_write_json(paths.candidate / "claim.json", claim)
                self.assertEqual(claim["baseline_improved"], paths.track.reference_id)
                with fake_provider():
                    self.assertEqual(pipeline.run_all(paths), 0)
                score = read_json(paths.score)
                self.assertEqual(score["score"], 182)
                self.assertEqual(score["metrics"]["nominalReferenceScore"], 80)
                self.assertFalse(score["metrics"]["improvesNominalReference"])
                self.assertFalse(score["metrics"]["referenceIsQualifiedBaseline"])

    def test_material_false_comparison_is_not_filtered_out_as_reference_metadata(self):
        paths = self.paths("sha1-r80-rigorous")
        claim = read_json(paths.candidate / "claim.json")
        claim["claim"].update(time_log2=94, memory_log2_bytes=88)
        atomic_write_json(paths.candidate / "claim.json", claim)
        (paths.candidate / "proof.md").write_text(
            "Organizer negative fixture: falsely asserts that 182 is less than 80.\n"
        )

        def false_comparison(stage, review, _):
            if stage == "lane_evaluability":
                review["findings"].append({
                    "id": "EVAL-001", "severity": "material", "category": "invalid_inference",
                    "statement": "The explicit comparison 182 < 80 is false.",
                    "obligation_ids": ["evidence_relevant"], "heuristic_ids": [],
                    "evidence": ["proof.md:L1"],
                })

        with fake_provider(false_comparison):
            self.assertEqual(pipeline.run_all(paths), 2)
        self.assertEqual(read_json(paths.aggregate)["reasons"], ["lane_evaluability/EVAL-001"])
        self.assertFalse(paths.score.exists())

    def test_exact_experiment_and_declared_heuristic_reach_both_reviews_and_score(self):
        paths = self.paths("sha256-r31-rigorous")
        add_experiment(paths.candidate, addition(), heuristic=True)
        with fake_provider(establish_fixture_heuristics) as (client, _):
            self.assertEqual(pipeline.run_all(paths), 0)
        full = read_json(paths.work / "experiment-report.json")["execution"]
        measured = full["experiments"][0]
        self.assertEqual(measured["probability"], {"numerator": 4, "denominator": 4})
        self.assertEqual(full["sources"], [])
        for stage, payload in client.calls:
            view = payload["submission"]["experiment_report"]["execution"]
            self.assertEqual(view["view_kind"], "judge-evidence-view-v1")
            self.assertEqual(view["full_report_sha256"], full["report_sha256"])
        self.assertEqual(read_json(paths.score)["metrics"]["reviewStatus"], "ai_rigor_qualified")

    def test_dangling_experiment_or_proof_reference_rejected_before_any_provider(self):
        for reference in ("experiment:undeclared", "proof:999", "proof:2-1"):
            with self.subTest(reference=reference):
                paths = self.paths(suffix=reference.replace(":", "-"))
                add_experiment(paths.candidate, addition(), heuristic=True)
                claim = read_json(paths.candidate / "claim.json")
                claim["heuristics"][0]["evidence_ids"] = [reference]
                atomic_write_json(paths.candidate / "claim.json", claim)
                with fake_provider() as (client, provider):
                    self.assertEqual(pipeline._execute("all", paths), 2)
                provider.assert_not_called()
                self.assertEqual(client.calls, [])
                self.assertFalse(paths.score.exists())

    def test_reviewers_must_cover_every_declared_heuristic(self):
        paths = self.paths()
        add_experiment(paths.candidate, addition(), heuristic=True)
        with fake_provider() as (client, _):
            self.assertEqual(pipeline.run_all(paths), 3)
        self.assertTrue(client.calls)
        self.assertFalse(paths.score.exists())
        self.assertEqual(read_json(paths.aggregate)["status"], "infra_failed")

    def test_same_unresolved_material_obligation_scores_only_exploratory(self):
        def unresolved(stage, review, _):
            if stage == "lane_cryptanalysis":
                review["obligations"][1]["status"] = "unresolved"
        for lane, expected in (("exploratory", 0), ("rigorous", 2)):
            with self.subTest(lane=lane):
                paths = self.paths(f"sha256-r31-{lane}")
                with fake_provider(unresolved):
                    self.assertEqual(pipeline.run_all(paths), expected)
                self.assertEqual(paths.score.exists(), lane == "exploratory")
                if lane == "rigorous":
                    self.assertEqual(read_json(paths.aggregate)["status"], "not_qualified")

    def test_draft_python_never_executes_or_reaches_provider_or_emits_score(self):
        paths = self.paths(ready=False)
        add_experiment(paths.candidate, program(), b"raise RuntimeError('must never execute')\n")
        with patch("verifier.experiment_evidence.run_experiments", side_effect=AssertionError("draft execution")) as executor, fake_provider() as (client, provider):
            self.assertEqual(pipeline.run_all(paths), 2)
        executor.assert_not_called()
        provider.assert_not_called()
        self.assertEqual(client.calls, [])
        self.assertFalse(paths.score.exists())
        self.assertEqual(read_json(paths.work / "experiment-report.json")["status"], "draft_not_submitted")

    def test_changed_python_source_is_blocked_before_provider(self):
        paths = self.paths()
        add_experiment(paths.candidate, program(), b"# immutable organizer fixture\npass\n")
        raw = json.dumps({"schema_version": 1, "trials": [{"trial": i, "message_a_hex": None, "message_b_hex": None} for i in range(256)]}).encode()
        with patch("experiments.runner._run_docker", return_value=raw):
            self.assertEqual(pipeline.run_intake(paths), 0)
        (paths.candidate / "experiments/probe.py").write_bytes(b"# changed after intake\npass\n")
        with fake_provider() as (client, provider), patch("experiments.runner._run_docker", side_effect=AssertionError("re-execution")):
            self.assertEqual(pipeline._execute("judge", paths), 2)
        provider.assert_not_called()
        self.assertEqual(client.calls, [])
        self.assertFalse(paths.score.exists())

    def test_modified_experiment_report_is_blocked_before_provider(self):
        paths = self.paths()
        add_experiment(paths.candidate, addition())
        self.assertEqual(pipeline.run_intake(paths), 0)
        report_path = paths.work / "experiment-report.json"
        report = read_json(report_path)
        report["execution"]["experiments"][0]["successes"] = 0
        atomic_write_json(report_path, report)
        with fake_provider() as (_, provider):
            self.assertEqual(pipeline._execute("judge", paths), 2)
        provider.assert_not_called()
        self.assertFalse(paths.score.exists())

    def test_claim_or_dossier_tamper_after_judgment_blocks_score_and_clears_stale_file(self):
        for kind in ("claim", "review", "configuration", "aggregate_lane"):
            with self.subTest(kind=kind):
                paths = self.paths(suffix=kind)
                with fake_provider():
                    self.assertEqual(pipeline.run_all(paths), 0)
                if kind == "claim":
                    target = paths.candidate / "claim.json"
                    content = read_json(target)
                    content["claim"]["time_log2"] -= 1
                elif kind == "aggregate_lane":
                    target = paths.aggregate
                    content = read_json(target)
                    content["lane"] = "rigorous"
                else:
                    target = paths.dossier
                    content = read_json(target)
                    if kind == "review":
                        content["reviews"]["lane_cryptanalysis"]["obligations"][0]["status"] = "unresolved"
                    else:
                        content["judge_configuration"]["judge"]["model"] = "altered-model"
                atomic_write_json(target, content)
                with patch.object(pipeline, "_provider_from_env", side_effect=AssertionError("unexpected provider")), patch("verifier.experiment_evidence.run_experiments", side_effect=AssertionError("unexpected execution")):
                    self.assertEqual(pipeline._execute("score", paths), 2)
                self.assertFalse(paths.score.exists())

    def test_wrong_lane_legacy_schema_and_undeclared_files_fail_intake(self):
        for kind in ("wrong_lane", "legacy_schema", "undeclared_manifest", "extra_file", "symlink"):
            with self.subTest(kind=kind):
                paths = self.paths(suffix=kind)
                claim = read_json(paths.candidate / "claim.json")
                if kind == "wrong_lane":
                    claim["lane"] = "rigorous"
                elif kind == "legacy_schema":
                    claim["schema_version"] = 2
                elif kind == "undeclared_manifest":
                    atomic_write_json(paths.candidate / "experiments/manifest.json", addition())
                elif kind == "extra_file":
                    (paths.candidate / "unexpected.py").write_text("# not executed\n")
                else:
                    (paths.candidate / "proof.md").unlink()
                    (paths.candidate / "proof.md").symlink_to(paths.candidate / "claim.json")
                atomic_write_json(paths.candidate / "claim.json", claim)
                with self.assertRaises(VerificationError):
                    validate_candidate(paths.candidate, track=paths.track)

    def test_judge_and_score_validate_stored_experiments_without_reexecution(self):
        paths = self.paths()
        add_experiment(paths.candidate, addition())
        self.assertEqual(pipeline.run_intake(paths), 0)
        before = (paths.work / "experiment-report.json").read_bytes()
        with patch("verifier.experiment_evidence.run_experiments", side_effect=AssertionError("experiments rerun in judge or score")) as executor, fake_provider():
            self.assertEqual(pipeline.run_judge(paths), 0)
            self.assertEqual(pipeline.run_score(paths), 0)
        executor.assert_not_called()
        self.assertEqual((paths.work / "experiment-report.json").read_bytes(), before)

    def test_six_role_committee_uses_effective_models_and_pins_strategies(self):
        from judge import role_committee
        paths = self.paths()
        profile = read_json(ROOT / "judge/committees/paired-roles-v1.json")
        profile["roles"]["lane_experiments"]["model"] = "global.openai.gpt-5.6-sol"
        directory = self.root / "committee"
        directory.mkdir()
        committee_path = directory / "roles.json"
        atomic_write_json(committee_path, profile)
        made = []
        def alleged_fatal(stage, review, _):
            if stage == "lane_cryptanalysis":
                add_fatal(review)
        def factory(config):
            client = FixtureClient(alleged_fatal)
            made.append((config, client))
            return client
        with patch.object(role_committee, "DIRECTORY", directory), patch.dict(os.environ, {"HASHSMASH_ROLE_COMMITTEE_PATH": str(committee_path)}), fake_provider(mode="committee", factory=factory):
            self.assertEqual(pipeline.run_all(paths), 0)
        calls = {stage: config for config, client in made for stage, _ in client.calls}
        self.assertEqual(set(calls), set(LANE_STAGES))
        self.assertEqual(calls["lane_experiments"].model, "global.openai.gpt-5.6-sol")
        self.assertEqual(calls["lane_cryptanalysis"].strategy, "formal-proof-v1")
        record = read_json(paths.dossier)["judge_configuration"]["role_committee"]
        self.assertEqual(record["profile_sha256"], sha256_bytes(committee_path.read_bytes()))
        self.assertEqual(set(record["roles"]), set(LANE_STAGES))
        self.assertTrue(all(len(role["system_prompt_sha256"]) == 64 for role in record["roles"].values()))
        self.assertNotIn("offline-fixture-no-credential", paths.dossier.read_text())

    @unittest.skipUnless(os.environ.get("HASHSMASH_TEST_DOCKER") == "1", "opt-in isolated organizer Docker integration")
    def test_real_docker_selected_sha256_mask_event_through_fake_judge_and_score(self):
        paths = self.paths()
        event = {"kind": "digest-xor-mask", "mask_hex": "00" * 31 + "01", "expected_hex": "00" * 32}
        source = (ROOT / "experiments/fixtures/deterministic_pairs.py").read_bytes()
        add_experiment(paths.candidate, program(event=event), source)
        with fake_provider():
            self.assertEqual(pipeline.run_all(paths), 0)
        execution = read_json(paths.work / "experiment-report.json")["execution"]
        measured = execution["experiments"][0]
        self.assertEqual(execution["target_profile"], "sha256-r31-prefix-v1")
        self.assertGreater(measured["successes"], 0)
        self.assertLess(measured["successes"], measured["trials"])
        self.assertFalse(any(row["full_collision"] for row in measured["checked_trials"]))
        view = read_json(paths.evidence)["submission"]["experiment_report"]["execution"]
        self.assertEqual(view["full_report_sha256"], execution["report_sha256"])
        self.assertNotIn("checked_trials", view["experiments"][0])
        self.assertTrue(paths.score.exists())


if __name__ == "__main__":
    unittest.main()
