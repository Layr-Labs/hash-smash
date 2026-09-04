"""Provider configuration and paired pipeline command boundaries."""

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import scripts.hashsmash_pipeline as pipeline
from judge.bedrock_adapter import BedrockClient, BedrockConfig, bedrock_system_prompt
from judge.provider_adapter import JudgeInfraError, OpenRouterClient, OpenRouterConfig
from tests.helpers import candidate_fixture
from verifier.frontier_tracks import get_frontier_track
from verifier.io import sha256_bytes


class PipelineIntegrationTests(unittest.TestCase):
    def test_provider_selection_supports_openrouter_and_bedrock(self) -> None:
        with patch.dict(
            "os.environ",
            {"OPENROUTER_API_KEY": "openrouter-key"},
            clear=True,
        ):
            name, config, factory = pipeline._provider_from_env()
        self.assertEqual(name, "openrouter")
        self.assertIsInstance(config, OpenRouterConfig)
        self.assertIs(factory, OpenRouterClient)

        with patch.dict(
            "os.environ",
            {
                "HASHSMASH_JUDGE_PROVIDER": "bedrock",
                "AWS_BEARER_TOKEN_BEDROCK": "bedrock-key",
            },
            clear=True,
        ):
            name, config, factory = pipeline._provider_from_env()
        self.assertEqual(name, "bedrock")
        self.assertIsInstance(config, BedrockConfig)
        self.assertIs(factory, BedrockClient)

    def test_unknown_provider_is_rejected(self) -> None:
        with patch.dict(
            "os.environ",
            {"HASHSMASH_JUDGE_PROVIDER": "unknown"},
            clear=True,
        ):
            with self.assertRaisesRegex(ValueError, "openrouter.*bedrock"):
                pipeline._provider_from_env()

    def test_bedrock_safe_configuration_does_not_retain_key(self) -> None:
        safe = pipeline._safe_config(BedrockConfig(api_key="bedrock-super-secret"))
        self.assertNotIn("api_key", safe)
        self.assertNotIn("bedrock-super-secret", json.dumps(safe))
        self.assertEqual(safe["region"], "us-east-1")
        self.assertIn("prompt_sha256", safe)

    def test_sol_configuration_hashes_effective_output_instructions(self) -> None:
        config = BedrockConfig(api_key="secret", model="us.openai.gpt-5.6-sol")
        safe = pipeline._safe_config(config)
        self.assertEqual(safe["api"], "responses")
        self.assertEqual(safe["endpoint"], config.endpoint)
        self.assertEqual(safe["prompt_sha256"]["lane_evaluability"], sha256_bytes(bedrock_system_prompt(config, "lane_evaluability").encode()))
        self.assertNotIn("secret", json.dumps(safe))

    def test_track_selection_is_required_and_retired_tracks_are_rejected(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
            pipeline.main(["all"])
        self.assertEqual(error.exception.code, 2)
        for track_id in ("sha1-r80", "md5-s8", "blake3-exploratory"):
            with contextlib.redirect_stderr(io.StringIO()), patch.object(pipeline, "_provider_from_env") as provider:
                self.assertEqual(pipeline.main(["all", "--track", track_id]), 3)
                provider.assert_not_called()

    def test_failed_judge_removes_stale_score(self):
        class FailedClient:
            def review(self, stage, evidence):
                raise JudgeInfraError("Organizer offline transport failure")

        track = get_frontier_track("sha256-r31-exploratory")
        config = BedrockConfig(api_key="offline-fixture")
        with tempfile.TemporaryDirectory() as temporary, contextlib.redirect_stdout(io.StringIO()):
            root = Path(temporary)
            candidate = candidate_fixture(root, track)
            paths = pipeline.RunPaths.for_track(track, state_root=root / "state", candidate=candidate)
            self.assertEqual(pipeline.run_intake(paths), 0)
            paths.score.parent.mkdir(parents=True, exist_ok=True)
            paths.score.write_text('{"score": 179}')
            with patch.object(pipeline, "_provider_from_env",
                              return_value=("bedrock", config, lambda _: FailedClient())), \
                 patch.dict("os.environ", {"HASHSMASH_JUDGE_MODE": "single"}):
                self.assertEqual(pipeline.run_judge(paths), 3)
            self.assertFalse(paths.score.exists())
            self.assertEqual(json.loads(paths.aggregate.read_text())["status"], "infra_failed")


if __name__ == "__main__":
    unittest.main()
