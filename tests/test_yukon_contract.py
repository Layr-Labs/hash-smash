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
        self.assertEqual(configuration["import_tracks"], 6)
        self.assertEqual(configuration["runnable_tracks"], 24)
        self.assertEqual(configuration["pending_tracks"], 4)
        for track in frontier_tracks():
            workflow = (ROOT / ".github/workflows" / f"{track.id}.yml").read_text()
            self.assertIn("workflow_dispatch:", workflow)
            self.assertIn("uses: ./.github/workflows/paired-review.yml", workflow)
            self.assertIn("OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}", workflow)

    def test_root_score_artifact_and_secret_free_intake_and_score_are_preserved(self):
        workflow = (ROOT / ".github/workflows/paired-review.yml").read_text()
        intake, rest = workflow.split("jobs:\n", 1)[1].split("  judge:\n", 1)
        judge, score = rest.split("  score:\n", 1)
        for secret in ("OPENROUTER_API_KEY", "AWS_BEARER_TOKEN_BEDROCK", "OPENAI_API_KEY"):
            self.assertNotIn(secret, intake)
            self.assertNotIn(secret, score)
            self.assertIn(secret, judge)
        providers = {"Amazon Bedrock": "AWS_BEARER_TOKEN_BEDROCK",
                     "OpenRouter": "OPENROUTER_API_KEY", "OpenAI": "OPENAI_API_KEY"}
        for provider, selected_key in providers.items():
            step = judge.split(f"      - name: Benchmark {provider} paired review\n", 1)[1].split("      - name:", 1)[0]
            self.assertIn(selected_key, step)
            for other_key in set(providers.values()) - {selected_key}:
                self.assertNotIn(other_key, step)
        self.assertIn("vars.HASHSMASH_JUDGE_PROVIDER == '' || vars.HASHSMASH_JUDGE_PROVIDER == 'openrouter'", judge)
        self.assertNotIn("vars.HASHSMASH_JUDGE_PROVIDER != 'bedrock'", judge)
        self.assertIn("openrouter|bedrock|openai)", judge)
        self.assertIn('*) echo "Unsupported HASHSMASH_JUDGE_PROVIDER" >&2; exit 2', judge)
        self.assertLess(judge.index("Validate judge provider"), judge.index("Benchmark Amazon Bedrock"))
        direct = judge.split("      - name: Benchmark OpenAI paired review\n", 1)[1].split("      - name:", 1)[0]
        self.assertIn("HASHSMASH_OPENAI_MODEL: ${{ vars.HASHSMASH_OPENAI_MODEL }}", direct)
        self.assertIn("HASHSMASH_REASONING_EFFORT: high", direct)
        self.assertIn('scripts/check-frontier-surface.py --track "$HASHSMASH_SELECTED_TRACK"', intake)
        self.assertIn("needs: intake", judge)
        self.assertIn("needs: judge", score)
        self.assertIn("--benchmark-root .", score)
        self.assertIn('--score-path "lanes/$HASHSMASH_SCORE_LANE/.yukon/scores/$HASHSMASH_SELECTED_TRACK.json"', score)
        self.assertIn("path: ${{ runner.temp }}/yukon-score-artifact/", score)
        self.assertIn("include-hidden-files: true", score)
        self.assertIn("if-no-files-found: error", score)
        self.assertNotIn("persist-credentials: true", workflow)

    def test_prior_artifact_download_is_pinned_and_its_token_stays_in_the_action(self):
        workflow = (ROOT / ".github/workflows/paired-review.yml").read_text()
        prior = workflow.split("      - name: Download pinned prior judgment\n")[1].split("      - name:")[0]
        self.assertIn("artifact-ids: ${{ steps.prior.outputs.artifact_id }}", prior)
        self.assertIn("run-id: ${{ steps.prior.outputs.run_id }}", prior)
        self.assertIn("github-token: ${{ github.token }}", prior)
        self.assertNotIn("run:", prior)
        self.assertEqual(workflow.count("${{ github.token }}"), 1)
        self.assertLess(workflow.index("Verify prior judgment"), workflow.index("Prepare isolated experiment runtime"))
        self.assertIn("actions: read", workflow)


if __name__ == "__main__":
    unittest.main()
