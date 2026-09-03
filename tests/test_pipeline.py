from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import scripts.hashsmash_pipeline as pipeline
from judge.bedrock_adapter import BedrockClient, BedrockConfig
from judge.provider_adapter import OpenRouterClient, OpenRouterConfig


ROOT = Path(__file__).resolve().parents[1]


class PipelineIntegrationTests(unittest.TestCase):
    def test_manifest_has_yukon_score_contract(self) -> None:
        manifest = json.loads((ROOT / "benchmark.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["schemaVersion"], 1)
        self.assertEqual(manifest["direction"], "-")
        self.assertEqual(manifest["editablePaths"], ["candidate"])
        self.assertEqual(manifest["scorePath"], ".yukon/score.json")

    def test_workflow_is_manually_dispatchable_and_keeps_secret_out_of_intake(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "benchmark.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("workflow_dispatch:", workflow)
        intake_job, judge_job = workflow.split("  judge:\n", maxsplit=1)
        self.assertNotIn("OPENROUTER_API_KEY", intake_job)
        self.assertIn("OPENROUTER_API_KEY", judge_job)
        self.assertNotIn("AWS_BEARER_TOKEN_BEDROCK", intake_job)
        self.assertIn("AWS_BEARER_TOKEN_BEDROCK", judge_job)
        openrouter_step, bedrock_and_later = judge_job.split(
            "      - name: Benchmark Amazon Bedrock review\n", maxsplit=1
        )
        bedrock_step = bedrock_and_later.split(
            "      - name: Publish review summary\n", maxsplit=1
        )[0]
        self.assertNotIn("AWS_BEARER_TOKEN_BEDROCK", openrouter_step)
        self.assertNotIn("OPENROUTER_API_KEY", bedrock_step)

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
