from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import scripts.hashsmash_pipeline as pipeline
from judge.bedrock_adapter import BedrockClient, BedrockConfig, bedrock_system_prompt
from judge.provider_adapter import OpenRouterClient, OpenRouterConfig
from judge.tests.test_bedrock_adapter import FakeTransport, sol_response
from verifier.io import sha256_bytes


ROOT = Path(__file__).resolve().parents[1]


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
        self.assertEqual(safe["prompt_sha256"]["triage"], sha256_bytes(bedrock_system_prompt(config, "triage").encode()))
        self.assertNotIn("secret", json.dumps(safe))

    def test_sol_failed_judge_removes_stale_score(self) -> None:
        config = BedrockConfig(api_key="secret", model="us.openai.gpt-5.6-sol", max_attempts=1)
        transport = FakeTransport([sol_response(status="incomplete")] * 3)
        with tempfile.TemporaryDirectory() as temporary:
            report_root = Path(temporary)
            score_path = report_root / "score.json"
            score_path.write_text('{"score": 179}')
            with patch.multiple(
                pipeline,
                SCORE_PATH=score_path,
                DOSSIER_PATH=report_root / "dossier.json",
                AGGREGATE_PATH=report_root / "aggregate.json",
            ), patch.object(pipeline, "_load_json", return_value={}), patch.object(
                pipeline, "_provider_from_env",
                return_value=("bedrock", config, lambda cfg: BedrockClient(cfg, transport=transport)),
            ), patch.dict("os.environ", {"HASHSMASH_JUDGE_MODE": "single"}), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(pipeline.run_judge(), 3)
            self.assertFalse(score_path.exists())
            self.assertEqual(json.loads((report_root / "aggregate.json").read_text())["status"], "judge_infra_failed")

    def test_checked_in_candidate_passes_end_to_end_intake(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            generated_root = Path(temporary)
            work_root = generated_root / "work"
            report_root = generated_root / "reports"
            score_path = generated_root / "score.json"
            evidence_path = work_root / "judge-evidence.json"
            generated_files = (
                score_path,
                work_root / "intake-report.json",
                work_root / "proof-numbered.md",
                work_root / "certificate-report.json",
                evidence_path,
                report_root / "judge-dossier.json",
                report_root / "aggregate.json",
            )
            stdout = io.StringIO()
            with patch.multiple(
                pipeline,
                WORK_ROOT=work_root,
                REPORT_ROOT=report_root,
                SCORE_PATH=score_path,
                EVIDENCE_PATH=evidence_path,
                DOSSIER_PATH=report_root / "judge-dossier.json",
                AGGREGATE_PATH=report_root / "aggregate.json",
                GENERATED_FILES=generated_files,
            ), contextlib.redirect_stdout(stdout):
                self.assertEqual(pipeline.run_intake(), 0)
            output = json.loads(stdout.getvalue())
            evidence = json.loads(evidence_path.read_text(encoding="utf-8"))

        self.assertEqual(output["status"], "mechanically_valid")
        self.assertEqual(evidence["schema_version"], "hashsmash-evidence-v1")
        self.assertIn("000001 |", evidence["submission"]["proof_markdown_line_numbered"])


if __name__ == "__main__":
    unittest.main()
