"""OpenAI pipeline/committee/CLI integration with organizer packages and fake HTTP."""
from contextlib import redirect_stdout, redirect_stderr
from dataclasses import replace
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from judge.lanes import INITIAL_STAGES, LANE_STAGES
from judge.openai_adapter import OpenAIClient, OpenAIConfig, openai_contract_provenance
from judge.role_committee import build_role_clients
from judge.tests.test_openai_adapter import MODEL, KEY, response, wire_record
from scripts import hashsmash_pipeline as pipeline
from scripts import calibrate_paired_judges as calibration
from scripts import test_participant_heuristic as participant
from tests.helpers import candidate_fixture
from tests.test_paired_calibration import OfflineCalibrationClient
from verifier.errors import VerificationError
from verifier.frontier_tracks import get_frontier_track


class FixtureTransport:
    def __init__(self, fail=False):
        self.calls = []
        self.fail = fail

    def request(self, url, *, headers, body, timeout_seconds):
        payload = json.loads(body)
        stage = payload["text"]["format"]["name"].removeprefix("hashsmash_").removesuffix("_review_v1")
        evidence = json.loads(payload["input"][0]["content"])["evidence"]
        self.calls.append(stage)
        return response(wire_record(stage, evidence), status="incomplete" if self.fail else "completed")


class OpenAIPipelineTests(unittest.TestCase):
    def test_explicit_selector_uses_only_openai_credentials_and_no_fallback(self):
        environment = {"HASHSMASH_JUDGE_PROVIDER": "openai", "OPENAI_API_KEY": KEY,
                       "HASHSMASH_OPENAI_MODEL": MODEL, "OPENROUTER_API_KEY": "other-key",
                       "AWS_BEARER_TOKEN_BEDROCK": "other-key"}
        with patch.dict("os.environ", environment, clear=True), \
             patch.object(pipeline.OpenRouterConfig, "from_env") as router, \
             patch.object(pipeline.BedrockConfig, "from_env") as bedrock:
            provider, config, factory = pipeline._provider_from_env()
            self.assertEqual(provider, "openai")
            self.assertEqual(config.api_key, KEY)
            self.assertIs(factory, OpenAIClient)
            router.assert_not_called(); bedrock.assert_not_called()
        environment.pop("OPENAI_API_KEY")
        with patch.dict("os.environ", environment, clear=True), self.assertRaisesRegex(ValueError, "OPENAI_API_KEY"):
            pipeline._provider_from_env()
        with patch.dict("os.environ", {"HASHSMASH_JUDGE_PROVIDER": "invalid"}, clear=True), \
             patch.object(OpenAIConfig, "from_env") as direct, self.assertRaises(ValueError):
            pipeline._provider_from_env()
        direct.assert_not_called()

    def test_safe_config_and_role_records_bind_effective_openai_contracts(self):
        config = OpenAIConfig(api_key=KEY, model=MODEL)
        safe = pipeline._safe_config(config)
        self.assertNotIn(KEY, json.dumps(safe))
        self.assertNotIn("api_key", safe)
        self.assertEqual(safe["endpoint"], "https://api.openai.com/v1/responses")
        self.assertEqual(safe["api"], "responses")
        self.assertFalse(safe["store"])
        with patch.dict("os.environ", {}, clear=True):
            clients, committee = build_role_clients(config, lambda value: value, mode="committee")
        self.assertEqual(set(clients), set(LANE_STAGES))
        for stage in (*LANE_STAGES, "lane_rescore"):
            self.assertEqual(safe["stage_contracts"][stage], openai_contract_provenance(config, stage))
        for stage, effective in clients.items():
            contract = openai_contract_provenance(effective, stage)
            self.assertEqual(effective.api_key, KEY)
            self.assertEqual(effective.model, MODEL)
            self.assertEqual(effective.reasoning_effort, "high")
            for name, digest in contract.items():
                self.assertEqual(committee["roles"][stage][name], digest)
        self.assertNotIn(KEY, json.dumps(committee))

    def test_real_adapter_flows_through_fixture_pipeline_and_failure_withholds_score(self):
        for fail in (False, True):
            with self.subTest(fail=fail), tempfile.TemporaryDirectory() as temporary, \
                 redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                root = Path(temporary)
                track = get_frontier_track("sha256-r31-exploratory")
                paths = pipeline.RunPaths.for_track(track, state_root=root / "state",
                                                    candidate=candidate_fixture(root, track))
                self.assertEqual(pipeline.run_intake(paths), 0)
                paths.score.parent.mkdir(parents=True, exist_ok=True)
                paths.score.write_text('{"score": 999}')
                transport = FixtureTransport(fail)
                config = OpenAIConfig(api_key=KEY, model=MODEL, max_attempts=1)
                def factory(effective):
                    return OpenAIClient(effective, transport=transport, sleeper=lambda _: None)
                with patch.object(pipeline, "_provider_from_env", return_value=("openai", config, factory)), \
                     patch.dict("os.environ", {"HASHSMASH_JUDGE_MODE": "committee"}, clear=True):
                    status = pipeline.run_judge(paths)
                self.assertEqual(status, 3 if fail else 0)
                self.assertFalse(paths.score.exists())
                score_status = pipeline._execute("score", paths)
                self.assertEqual(paths.score.exists(), not fail)
                self.assertEqual(score_status, 2 if fail else 0)
                dossier = json.loads(paths.dossier.read_text())
                self.assertNotIn(KEY, json.dumps(dossier))
                if not fail:
                    self.assertEqual(transport.calls, list(INITIAL_STAGES))
                    self.assertEqual(json.loads(paths.score.read_text())["score"], track.nominal_score)
                    # Altering direct-provider config invalidates the bound dossier/score.
                    dossier["judge_configuration"]["judge"]["model"] = "other-model"
                    paths.dossier.write_text(json.dumps(dossier))
                    self.assertEqual(pipeline._execute("score", paths), 2)
                    self.assertFalse(paths.score.exists())

    def test_malformed_key_failure_artifact_and_stdout_never_include_key(self):
        with tempfile.TemporaryDirectory() as temporary, redirect_stdout(io.StringIO()) as out:
            root = Path(temporary); track = get_frontier_track("sha256-r31-exploratory")
            paths = pipeline.RunPaths.for_track(track, state_root=root / "state", candidate=candidate_fixture(root, track))
            self.assertEqual(pipeline.run_intake(paths), 0)
            environment = {"HASHSMASH_JUDGE_PROVIDER": "openai", "OPENAI_API_KEY": "fixture-malformed-private\n",
                           "HASHSMASH_OPENAI_MODEL": MODEL}
            with patch.dict("os.environ", environment, clear=True), patch.object(pipeline, "OpenAIClient") as factory:
                self.assertEqual(pipeline.run_judge(paths), 3)
            factory.assert_not_called()
            self.assertFalse(paths.score.exists())
            for output in (out.getvalue(), paths.aggregate.read_text(), paths.dossier.read_text()):
                self.assertNotIn("fixture-malformed-private", output)

    def test_calibration_cli_openai_is_bounded_and_dry_run_does_not_load_keys(self):
        config = OpenAIConfig(api_key=KEY, model=MODEL)
        clients, written = [], []
        def factory(effective):
            item = OfflineCalibrationClient(effective); clients.append(item); return item
        with patch.dict("os.environ", {}, clear=True), \
             patch.object(calibration.OpenAIConfig, "from_env", return_value=config) as env, \
             patch.object(calibration, "OpenAIClient", side_effect=factory), \
             patch.object(calibration, "atomic_write_json", side_effect=lambda path, data: written.append(data)), \
             redirect_stdout(io.StringIO()):
            self.assertEqual(calibration.main(["--provider", "openai", "--dry-run"]), 0)
            env.assert_not_called()
            self.assertEqual(calibration.main(["--provider", "openai", "--mode", "single"]), 0)
        self.assertEqual(len(clients[0].calls), 4)
        self.assertEqual(clients[0].config.max_attempts, 1)
        self.assertNotIn(KEY, json.dumps(written))
        self.assertTrue(all(item["no_score_emitted"] for item in written))

    def test_unknown_calibration_environment_rejected_before_factory(self):
        with patch.dict("os.environ", {"HASHSMASH_JUDGE_PROVIDER": "unknown"}, clear=True), \
             patch.object(calibration.OpenRouterConfig, "from_env") as factory, \
             redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            calibration.main([])
        factory.assert_not_called()

    def test_openai_diagnostic_model_overrides_require_the_explicit_env_instead(self):
        with patch.object(calibration.OpenAIConfig, "from_env") as env, \
             redirect_stderr(io.StringIO()) as error, self.assertRaises(SystemExit):
            calibration.main(["--provider", "openai", "--model", MODEL])
        env.assert_not_called()
        self.assertIn("HASHSMASH_OPENAI_MODEL", error.getvalue())
        with patch.object(participant, "_load_prepared") as prepared, \
             self.assertRaisesRegex(ValueError, "HASHSMASH_OPENAI_MODEL"):
            participant.review_run(Path("unused"), provider="openai", model=MODEL)
        prepared.assert_not_called()

    def test_participant_prepare_rejects_openai_key(self):
        self.assertIn("OPENAI_API_KEY", participant.CREDENTIAL_NAMES)
        with patch.dict("os.environ", {"OPENAI_API_KEY": KEY}, clear=True), self.assertRaises(VerificationError):
            participant.prepare_run(None)


if __name__ == "__main__":
    unittest.main()
