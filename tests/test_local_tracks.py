"""Track isolation and history tests using organizer-owned paired fixtures."""

from concurrent.futures import ThreadPoolExecutor
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts import hashsmash_pipeline as pipeline
from scripts import local_tracks
from scripts.local_state import TrackBusyError, track_session
from tests.helpers import candidate_fixture
from verifier.frontier_tracks import ROOT, get_frontier_track
from verifier.intake import validate_candidate
from verifier.io import atomic_write_json


class LocalTrackTests(unittest.TestCase):
    def test_parallel_intakes_do_not_share_paths_or_delete_sibling_scores(self):
        tracks = (get_frontier_track("md5-s63-exploratory"), get_frontier_track("sha256-r31-rigorous"))
        with tempfile.TemporaryDirectory() as tmp, redirect_stdout(io.StringIO()):
            root = Path(tmp)
            paths = [pipeline.RunPaths.for_track(t, state_root=root, candidate=candidate_fixture(root, t)) for t in tracks]
            with ThreadPoolExecutor(max_workers=2) as executor:
                self.assertEqual(list(executor.map(pipeline.run_intake, paths)), [0, 0])
            for p in paths:
                self.assertEqual(json.loads(p.evidence.read_text())["benchmark"]["track_id"], p.track.id)
            atomic_write_json(paths[1].score, {"score": 123})
            pipeline.run_intake(paths[0])
            self.assertTrue(paths[1].score.exists())

    def test_run_lock_is_per_track_and_archives_only_known_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = pipeline.RunPaths.for_track(get_frontier_track("md5-s63-exploratory"), state_root=Path(tmp))
            with track_session(p, "intake") as record:
                atomic_write_json(p.work / "intake-report.json", {"mock": True})
                (p.work / ".env").write_text("DO NOT ARCHIVE")
                with self.assertRaises(TrackBusyError):
                    with track_session(p, "all"):
                        pass
                sibling = pipeline.RunPaths.for_track(get_frontier_track("sha1-r79-exploratory"), state_root=Path(tmp))
                with track_session(sibling, "intake") as other:
                    other["exit_code"] = 2
                record["exit_code"] = 2
            archive = list((p.reports / "runs").glob("*/run.json"))
            self.assertEqual(len(archive), 1)
            self.assertEqual(json.loads(archive[0].read_text())["exit_code"], 2)
            self.assertEqual({f.name for f in archive[0].parent.iterdir()}, {"run.json", "intake-report.json"})

    def test_history_status_ignores_failed_or_wrong_target_scores(self):
        track = get_frontier_track("md5-s63-exploratory")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            candidate = candidate_fixture(root, track)
            # Use the public path shape with an isolated root; no mutable solver file.
            p = pipeline.RunPaths.for_track(track, state_root=root / ".yukon", candidate=candidate)
            intake = validate_candidate(candidate, track=track)
            metrics = {"trackId": track.id, "reviewStatus": track.accepted_status,
                       "targetConfigSha256": track.config_sha256(), "inputPackageSha256": intake["package_sha256"]}
            for name, exit_code, configuration, score in (("valid", 0, track.config_sha256(), 100),
                                                         ("failed", 3, track.config_sha256(), 1),
                                                         ("wrong-target", 0, "0"*64, 0)):
                archive = p.reports / "runs" / name
                atomic_write_json(archive / "run.json", {"run_id": name, "command": "all", "exit_code": exit_code})
                atomic_write_json(archive / "score.json", {"score": score, "metrics": dict(metrics, targetConfigSha256=configuration)})
            with patch.object(type(track), "state_root", root / ".yukon"), patch.object(type(track), "candidate", candidate):
                result = local_tracks.status(track)
                self.assertIsNone(result["qualified_baseline"])
                self.assertEqual(result["best_ai_reviewed"]["score"], 100)
                self.assertTrue(result["best_ai_reviewed"]["current_candidate"])
                (candidate / "proof.md").write_text("# New draft after the historical result\n")
                self.assertFalse(local_tracks.status(track)["best_ai_reviewed"]["current_candidate"])

    def test_explicit_intake_cli_archives_draft_without_score_or_provider(self):
        track = get_frontier_track("md5-s63-exploratory")
        with tempfile.TemporaryDirectory() as tmp, redirect_stdout(io.StringIO()):
            root = Path(tmp)
            candidate = candidate_fixture(root, track, ready=False)
            p = pipeline.RunPaths.for_track(track, state_root=root, candidate=candidate)
            with patch.object(pipeline.RunPaths, "for_track", return_value=p), patch.object(pipeline, "_provider_from_env") as provider:
                self.assertEqual(pipeline.main(["all", "--track", track.id]), 2)
                provider.assert_not_called()
            records = list((p.reports / "runs").glob("*/run.json"))
            self.assertEqual(len(records), 1)
            self.assertEqual(json.loads(records[0].read_text())["exit_code"], 2)
            self.assertFalse(p.score.exists())

    def test_credential_free_cli_lists_and_shows_without_reading_mutable_candidates(self):
        for arguments in (("list",), ("show", "sha256-r31-rigorous")):
            result = subprocess.run([sys.executable, "scripts/local_tracks.py", *arguments], cwd=ROOT,
                                    capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("sha256-r31-rigorous", result.stdout)


if __name__ == "__main__":
    unittest.main()
