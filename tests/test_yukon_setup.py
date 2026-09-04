"""Organizer-only checks for artifact packaging and dev import boundaries."""

from contextlib import redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
from urllib import error
import zipfile

from scripts import import_yukon_dev as dev
from scripts.stage_yukon_score import stage_score


class ScoreArtifactTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.benchmark = self.root / "benchmark"
        self.benchmark.mkdir()

    def fixture(self, path, value=b'{"score": 12.5, "metrics": {"fixture": true}}'):
        row = {"scorePath": path, "editablePaths": ["candidates/sha256-r31"]}
        manifest = {"schemaVersion": 2, "tracks": [row]}
        (self.benchmark / "benchmark.json").write_text(json.dumps(manifest))
        source = self.benchmark / path
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_bytes(value)
        return source

    def test_uploaded_directory_preserves_exact_manifest_entry_and_only_score(self):
        path = ".yukon/scores/sha256-r31-exploratory.json"
        source = self.fixture(path)
        destination = self.root / "paired"
        stage_score(self.benchmark, path, destination)
        archive = io.BytesIO()
        with zipfile.ZipFile(archive, "w") as zipped:
            for item in destination.rglob("*"):
                if item.is_file():
                    zipped.write(item, str(item.relative_to(destination)))
        with zipfile.ZipFile(archive) as zipped:
            self.assertEqual(zipped.namelist(), [path])
            self.assertEqual(zipped.read(path), source.read_bytes())

    def test_retired_pilot_manifest_cannot_create_an_artifact(self):
        path = ".yukon/score.json"
        self.fixture(path)
        (self.benchmark / "benchmark.json").write_text(json.dumps({
            "schemaVersion": 1, "scorePath": path, "editablePaths": ["candidate"],
        }))
        with self.assertRaises(ValueError):
            stage_score(self.benchmark, path, self.root / "artifact")
        self.assertFalse((self.root / "artifact").exists())

    def test_invalid_scores_cannot_create_an_artifact(self):
        for value in [b'{"score":true}', b'{"score":NaN}', b'{"score":1e999}', b'{"metrics":{}}']:
            self.fixture(".yukon/score.json", value)
            with self.assertRaises(ValueError):
                stage_score(self.benchmark, ".yukon/score.json", self.root / "artifact")
            self.assertFalse((self.root / "artifact").exists())

    def test_symlinks_undeclared_paths_and_reused_directories_are_rejected(self):
        source = self.fixture(".yukon/score.json")
        for path in ["../score.json", ".yukon/missing.json"]:
            with self.assertRaises(ValueError):
                stage_score(self.benchmark, path, self.root / "artifact")
        source.unlink()
        source.symlink_to(self.benchmark / "benchmark.json")
        with self.assertRaises(ValueError):
            stage_score(self.benchmark, ".yukon/score.json", self.root / "artifact")
        source.unlink()
        source.write_text('{"score": 1}')
        destination = self.root / "artifact"
        destination.mkdir()
        marker = destination / "old-file"
        marker.write_text("keep")
        with self.assertRaises(FileExistsError):
            stage_score(self.benchmark, ".yukon/score.json", destination)
        self.assertEqual(marker.read_text(), "keep")


class DevImportTests(unittest.TestCase):
    def test_leaf_requests_are_explicit_and_cannot_select_legacy_or_prod(self):
        for lane in ("exploratory", "rigorous"):
            payload = dev.import_request(lane)
            self.assertEqual(payload["rootDir"], "lanes/" + lane)
            self.assertEqual(payload["sourceBranch"], "main")
            self.assertEqual(payload["sourceUrl"], "https://github.com/Layr-Labs/hash-smash")
        with self.assertRaises(dev.ImportFailure):
            dev.import_request("legacy")
        self.assertEqual(dev.API_URL, "https://yukon-api-dev.fly.dev")

    def test_default_plan_and_draft_guard_make_no_network_calls(self):
        for args, expected in [([], 0), (["--submit"], 2)]:
            with patch.object(dev, "draft_tracks", return_value=["fixture-draft"]), \
                    patch.object(dev, "DevClient") as client, \
                    redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                self.assertEqual(dev.main(["--lane", "exploratory", *args]), expected)
                client.assert_not_called()

    def test_import_submits_once_and_never_opens(self):
        client = Mock()
        client.call.return_value = {"tracks": [{"id": "fixture-id", "name": "fixture/track"}]}
        with patch.object(dev, "draft_tracks", return_value=[]), \
                patch.object(dev, "importer_token", return_value="fixture-token"), \
                patch.object(dev, "DevClient", return_value=client), redirect_stdout(io.StringIO()):
            self.assertEqual(dev.main(["--lane", "rigorous", "--submit"]), 0)
        client.call.assert_called_once_with("/api/benchmarks", dev.import_request("rigorous"))

    def test_uncertain_import_is_not_retried_and_does_not_disclose_token(self):
        client = dev.DevClient("fixture-private-token")
        client.opener = Mock()
        client.opener.open.side_effect = error.URLError("fixture-private-token")
        with self.assertRaises(dev.ImportFailure) as caught:
            client.call("/api/benchmarks", dev.import_request("exploratory"))
        self.assertIn("unknown", str(caught.exception))
        self.assertNotIn("fixture-private-token", str(caught.exception))
        client.opener.open.assert_called_once()
        req = client.opener.open.call_args.args[0]
        self.assertEqual(req.full_url, dev.API_URL + "/api/benchmarks")

    def test_auth_redirects_are_not_followed(self):
        self.assertIsNone(dev.NoRedirect().redirect_request(None, None, 302, "", {}, "https://example.com"))

    def test_failed_baseline_is_reported_without_open_or_reimport(self):
        client = Mock()
        client.call.return_value = {"benchmark": {"id": "fixture-id", "name": "fixture/track", "status": "failed"}}
        with redirect_stdout(io.StringIO()):
            self.assertEqual(dev.wait_for_baselines(client, [{"id": "fixture-id"}], 10), 2)
        client.call.assert_called_once_with("/api/benchmarks/fixture-id")


if __name__ == "__main__":
    unittest.main()
