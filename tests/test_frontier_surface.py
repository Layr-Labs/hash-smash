"""Pinned Yukon overlays must not be compared against a moving sibling frontier."""

import importlib.util
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

from verifier.errors import VerificationError
from verifier.io import canonical_json_bytes
from verifier.schema_validation import validate_claim
from verifier.frontier_tracks import get_frontier_track


SPEC = importlib.util.spec_from_file_location("frontier_surface", Path(__file__).resolve().parents[1] / "scripts/check-frontier-surface.py")
surface = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(surface)


class FrontierSurfaceTests(unittest.TestCase):
    def check(self, delta, *, parents=None, run_error=None):
        sha, base = "a" * 40, "b" * 40
        with patch.dict("os.environ", {"GITHUB_REF": "refs/heads/submissions/test", "GITHUB_SHA": sha}), \
                patch("sys.argv", ["surface", "--track", "sha256-r31-exploratory"]), \
                patch.object(surface.subprocess, "run", side_effect=run_error) as run, \
                patch.object(surface.subprocess, "check_output", side_effect=[parents or f"{sha} {base}".encode(), delta]) as output:
            status = surface.main()
            self.assertEqual(output.call_args.args[0][-2:], [base, sha])
            self.assertIn("merge-base", run.call_args.args[0])
            self.assertIn("--is-ancestor", run.call_args.args[0])
            return status

    def test_checks_exact_overlay_after_main_advances(self):
        self.assertEqual(self.check(b"lanes/exploratory/candidates/sha256-r31/proof.md\0"), 0)

    def test_sibling_or_trusted_file_delta_rejected(self):
        for name in (b"lanes/rigorous/candidates/sha256-r31/proof.md\0", b"verifier/score.py\0",
                     b"lanes/exploratory/candidates/sha256-r31-evil/proof.md\0"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                self.check(name)

    def test_merge_commit_or_untrusted_base_rejected(self):
        with self.assertRaises(ValueError):
            self.check(b"", parents=("a" * 40 + " " + "b" * 40 + " " + "c" * 40).encode())
        with self.assertRaises(subprocess.CalledProcessError):
            self.check(b"", run_error=subprocess.CalledProcessError(1, "git"))

    def test_nonfinite_scalar_never_passes_intake_or_json_serialization(self):
        track = get_frontier_track("sha256-r31-exploratory")
        claim = track.draft_claim()
        claim["claim"].update(time_log2=1e308, memory_log2_bytes=1e308)
        with self.assertRaisesRegex(VerificationError, "score must be finite"):
            validate_claim(claim, track=track)
        claim["claim"]["time_log2"] = 10 ** 500
        with self.assertRaisesRegex(VerificationError, "finite"):
            validate_claim(claim, track=track)
        with self.assertRaises(ValueError):
            canonical_json_bytes({"score": float("inf")})


if __name__ == "__main__":
    unittest.main()
