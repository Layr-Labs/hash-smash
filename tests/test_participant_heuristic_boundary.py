"""Exercise shell phase separation without reading the user's environment file.

The wrapper is copied to an organizer temporary project, with fake Python and a
synthetic .env containing a non-secret sentinel. No Docker/provider is contacted.
"""

from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
WRAPPER = ROOT / "scripts/run-participant-heuristic.sh"


class ParticipantHeuristicBoundaryTests(unittest.TestCase):
    def exercise(self, *, failure=None, arguments=()):
        with tempfile.TemporaryDirectory(prefix="hashsmash-phase-test-") as temporary:
            root = Path(temporary)
            (root / "scripts").mkdir()
            (root / ".yukon").mkdir()
            (root / "bin").mkdir()
            wrapper = root / "scripts/run-participant-heuristic.sh"
            shutil.copyfile(WRAPPER, wrapper)
            # Entirely synthetic test input. The repository's real .env is
            # never read, copied, printed, or passed to this subprocess.
            (root / ".env").write_text("export AWS_BEARER_TOKEN_BEDROCK=fixture-local-only\n")
            setup = root / ".yukon/setup.sh"
            setup.write_text('''#!/usr/bin/env bash
set -eu
test -z "${AWS_BEARER_TOKEN_BEDROCK+x}"
test -z "${OPENROUTER_API_KEY+x}"
test -z "${AWS_SECRET_ACCESS_KEY+x}"
echo setup >> "$HASHSMASH_PHASE_TEST_LOG"
test "${HASHSMASH_PHASE_TEST_FAILURE:-}" != setup
''')
            fake_python = root / "bin/python3"
            fake_python.write_text('''#!/usr/bin/env bash
set -eu
if [[ "$1" == -c ]]; then
  echo fixture-run
  exit 0
fi
phase="$2"
case "$phase" in
  prepare)
    test -z "${AWS_BEARER_TOKEN_BEDROCK+x}"
    test -z "${OPENROUTER_API_KEY+x}"
    test -z "${AWS_SECRET_ACCESS_KEY+x}"
    test -z "${GITHUB_TOKEN+x}"
    echo prepare >> "$HASHSMASH_PHASE_TEST_LOG"
    test "${HASHSMASH_PHASE_TEST_FAILURE:-}" != prepare
    ;;
  review)
    test "${AWS_BEARER_TOKEN_BEDROCK:-}" == fixture-local-only
    echo review >> "$HASHSMASH_PHASE_TEST_LOG"
    ;;
  *) exit 70 ;;
esac
''')
            fake_python.chmod(0o755)
            log = root / "phases.txt"
            environment = {
                "PATH": str(root / "bin") + ":/usr/bin:/bin",
                "HASHSMASH_PHASE_TEST_LOG": str(log),
                "HASHSMASH_PHASE_TEST_FAILURE": failure or "",
                "AWS_BEARER_TOKEN_BEDROCK": "fixture-inherited",
                "OPENROUTER_API_KEY": "fixture-inherited",
                "AWS_SECRET_ACCESS_KEY": "fixture-inherited",
                "GITHUB_TOKEN": "fixture-inherited",
            }
            result = subprocess.run(["/bin/bash", str(wrapper), *arguments], env=environment,
                                    capture_output=True, text=True, check=False)
            self.assertNotIn("fixture-local-only", result.stdout + result.stderr)
            self.assertNotIn("fixture-inherited", result.stdout + result.stderr)
            return result.returncode, log.read_text().splitlines() if log.exists() else []

    def test_credentials_are_absent_until_after_preparation(self):
        status, phases = self.exercise()
        self.assertEqual(status, 0)
        self.assertEqual(phases, ["setup", "prepare", "review"])

    def test_failed_setup_or_sandbox_preparation_never_reaches_live_review(self):
        for failed, expected in (("setup", ["setup"]), ("prepare", ["setup", "prepare"])):
            with self.subTest(failed=failed):
                status, phases = self.exercise(failure=failed)
                self.assertNotEqual(status, 0)
                self.assertEqual(phases, expected)

    def test_wrapper_rejects_redirecting_review_to_another_run(self):
        for arguments in (("--run-directory", "unexpected"), ("--run-directory=unexpected",)):
            status, phases = self.exercise(arguments=arguments)
            self.assertEqual(status, 2)
            self.assertEqual(phases, [])


if __name__ == "__main__":
    unittest.main()
