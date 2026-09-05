"""The root import must retain the paired GitHub Actions execution contract."""

from pathlib import Path
import unittest

from scripts.validate_frontier_config import validate_configuration
from verifier.frontier_tracks import frontier_tracks


ROOT = Path(__file__).resolve().parents[1]


class YukonContractTests(unittest.TestCase):
    def test_one_import_routes_every_track_to_a_dispatchable_workflow(self):
        configuration = validate_configuration()
        self.assertEqual(configuration["yukon_challenges"], 1)
        self.assertEqual(configuration["runnable_tracks"], 16)
        self.assertEqual(configuration["pending_tracks"], 12)
        for track in frontier_tracks():
            workflow = (ROOT / ".github/workflows" / f"{track.id}.yml").read_text()
            self.assertIn("workflow_dispatch:", workflow)
            self.assertIn("uses: ./.github/workflows/paired-review.yml", workflow)

    def test_root_score_artifact_and_secret_free_intake_and_score_are_preserved(self):
        workflow = (ROOT / ".github/workflows/paired-review.yml").read_text()
        intake, rest = workflow.split("jobs:\n", 1)[1].split("  judge:\n", 1)
        judge, score = rest.split("  score:\n", 1)
        for secret in ("OPENROUTER_API_KEY", "AWS_BEARER_TOKEN_BEDROCK"):
            self.assertNotIn(secret, intake)
            self.assertNotIn(secret, score)
            self.assertIn(secret, judge)
        bedrock, openrouter = judge.split("      - name: Benchmark Amazon Bedrock paired review\n", 1)[1].split(
            "      - name: Benchmark OpenRouter paired review\n", 1)
        self.assertNotIn("OPENROUTER_API_KEY", bedrock)
        self.assertNotIn("AWS_BEARER_TOKEN_BEDROCK", openrouter)
        self.assertIn('scripts/check-frontier-surface.py --track "$HASHSMASH_SELECTED_TRACK"', intake)
        self.assertIn("needs: intake", judge)
        self.assertIn("needs: judge", score)
        self.assertIn("--benchmark-root .", score)
        self.assertIn('--score-path "lanes/$HASHSMASH_SCORE_LANE/.yukon/scores/$HASHSMASH_SELECTED_TRACK.json"', score)
        self.assertIn("path: ${{ runner.temp }}/yukon-score-artifact/", score)
        self.assertIn("include-hidden-files: true", score)
        self.assertIn("if-no-files-found: error", score)
        self.assertNotIn("persist-credentials: true", workflow)


if __name__ == "__main__":
    unittest.main()
