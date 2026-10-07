"""Advisory exporter checks using organizer fixtures only; no agent reviews."""

from contextlib import ExitStack, redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import export_review_packet as exporter
from tests.helpers import candidate_fixture
from tests.test_experiments import addition, program
from verifier.errors import VerificationError
from verifier.experiment_evidence import execute
from verifier.intake import validate_candidate
from verifier.io import atomic_write_json, canonical_json_bytes, sha256_bytes


class ReviewPacketTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="hashsmash-packet-test-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.track = exporter.active_track("sha256-r31-exploratory")
        self.candidate = candidate_fixture(self.root, self.track)

    def build(self, **kwargs):
        return exporter.build_packet(self.track, candidate=self.candidate, **kwargs)

    def experiment(self, manifest, source=None):
        claim = json.loads((self.candidate / "claim.json").read_text())
        claim["experiment_manifest"] = "experiments/manifest.json"
        atomic_write_json(self.candidate / "claim.json", claim)
        atomic_write_json(self.candidate / "experiments/manifest.json", manifest)
        if source is not None:
            (self.candidate / manifest["experiments"][0]["program"]).write_text(source)

    def report(self):
        intake = validate_candidate(self.candidate, track=self.track)
        # This one-bit, organizer-owned built-in fixture invokes no participant code.
        report = execute(self.candidate, intake, self.track)
        path = self.root / "experiment-report.json"
        atomic_write_json(path, report)
        return path

    def test_ready_snapshot_is_bound_deterministic_and_uses_current_roles(self):
        packet = self.build()
        self.assertEqual(packet, self.build())
        self.assertTrue(packet["advisory_only"])
        evidence = packet["evidence"]
        self.assertEqual(packet["binding"], exporter.evidence_binding(evidence))
        submission = evidence["submission"]
        self.assertEqual(submission["experiment_report"]["status"], "not_requested")
        self.assertEqual(submission["intake_report"]["package_sha256"],
                         submission["certificate_report"]["package_sha256"])
        self.assertIn("000001 | # Mock-only fixture", submission["proof_markdown_line_numbered"])
        self.assertEqual(set(packet["roles"]), set(exporter.INITIAL_STAGES))
        for stage, role in packet["roles"].items():
            self.assertEqual(role["system_prompt"], exporter.load_system_prompt(stage, role["strategy"]))
            self.assertEqual(role["output_schema"], exporter._schema_for_stage(stage))
            self.assertNotIn("binding", role["output_schema"]["properties"])

    def test_export_never_executes_programs_or_contacts_providers(self):
        sentinel = self.root / "EXECUTED"
        source = f"from pathlib import Path\nPath({str(sentinel)!r}).write_text('bad')\n"
        self.experiment(program(), source)
        blocked = ["subprocess.run", "subprocess.Popen", "urllib.request.urlopen",
                   "socket.create_connection", "experiments.run_experiments",
                   "verifier.experiment_evidence.run_experiments"]
        with ExitStack() as stack:
            for name in blocked:
                stack.enter_context(patch(name, side_effect=AssertionError(f"unexpected {name}")))
            stack.enter_context(patch.dict("os.environ", {"OPENROUTER_API_KEY": "DO-NOT-COPY-TEST-SECRET"}))
            packet = self.build()
        self.assertFalse(sentinel.exists())
        self.assertNotIn("DO-NOT-COPY-TEST-SECRET", json.dumps(packet))
        submission = packet["evidence"]["submission"]
        self.assertEqual(submission["experiment_report"]["status"], "not_executed")
        self.assertIsNone(submission["experiment_report"]["execution"])
        self.assertEqual(submission["untrusted_experiment_source_texts"]["experiments/probe.py"], source)

    def test_draft_does_not_reach_certificate_or_prompt_preparation(self):
        claim = json.loads((self.candidate / "claim.json").read_text())
        claim["submission_state"] = "draft"
        atomic_write_json(self.candidate / "claim.json", claim)
        with patch.object(exporter, "verify_certificates") as certificates:
            with self.assertRaisesRegex(VerificationError, "draft"):
                self.build()
        certificates.assert_not_called()

    def test_undeclared_secret_file_and_symlink_are_rejected(self):
        path = self.candidate / ".env"
        path.write_text("not-a-real-secret")
        with self.assertRaisesRegex(VerificationError, "unexpected file"):
            self.build()
        path.unlink()
        proof = self.candidate / "proof.md"
        proof.unlink()
        proof.symlink_to(self.root / "missing-proof")
        with self.assertRaisesRegex(VerificationError, "symlink"):
            self.build()

    def test_invalid_certificates_block_export(self):
        (self.candidate / "certificates/a.bin").write_bytes(b"same")
        (self.candidate / "certificates/b.bin").write_bytes(b"same")
        atomic_write_json(self.candidate / "certificates/manifest.json", {
            "schema_version": 2, "certificates": [{
                "id": "bad", "type": "hash-collision-witness-v2",
                "target_profile": self.track.profile_id,
                "message_a": "certificates/a.bin", "message_b": "certificates/b.bin",
                "expected_digest": "0" * 64,
            }],
        })
        with self.assertRaisesRegex(VerificationError, "messages must differ"):
            self.build()

    def test_original_edit_while_snapshot_is_checked_is_rejected(self):
        original = exporter.verify_certificates
        def mutate(*args, **kwargs):
            result = original(*args, **kwargs)
            (self.candidate / "proof.md").write_text("# Changed during export\n")
            return result
        with patch.object(exporter, "verify_certificates", side_effect=mutate):
            with self.assertRaisesRegex(VerificationError, "changed during export"):
                self.build()

    def test_file_change_after_intake_is_rejected(self):
        original = exporter._scan_candidate
        def mutate(path):
            (path / "proof.md").write_text("# Changed after intake\n")
            return original(path)
        with patch.object(exporter, "_scan_candidate", side_effect=mutate):
            with self.assertRaisesRegex(VerificationError, "changed during export"):
                self.build()

    def test_target_change_during_export_is_rejected(self):
        original = exporter.verify_certificates
        def stale(*args, **kwargs):
            result = original(*args, **kwargs)
            return {**result, "target_config_sha256": "0" * 64}
        with patch.object(exporter, "verify_certificates", side_effect=stale):
            with self.assertRaisesRegex(VerificationError, "changed during export"):
                self.build()

    def test_explicit_report_has_checked_bindings_and_clear_provenance_limit(self):
        self.experiment(addition())
        report_path = self.report()
        packet = self.build(experiment_report=report_path)
        report = packet["evidence"]["submission"]["experiment_report"]
        self.assertEqual(report["status"], "passed")
        self.assertEqual(report["execution"]["view_kind"], "judge-evidence-view-v1")
        self.assertEqual(packet["experiment_evidence"]["source"], "caller_supplied")
        self.assertIn("not authenticated", packet["experiment_evidence"]["limitation"])
        self.assertNotIn(str(report_path), json.dumps(packet))

    def test_advisory_experiment_view_keeps_review_inside_packet(self):
        self.experiment(addition())
        report_path = self.report()
        original_report = report_path.read_bytes()
        trusted_view = exporter.judge_view(json.loads(original_report)["execution"])
        packet = self.build(experiment_report=report_path)
        view = packet["evidence"]["submission"]["experiment_report"]["execution"]
        limitations = view["view_limitations"]
        self.assertNotIn("Consult the full trusted report", limitations)
        self.assertIn("This packet does not include the full experiment report", limitations)
        self.assertIn("Review only this packet", limitations)
        self.assertIn("do not open .yukon/work, score files, or any other on-disk report", limitations)
        self.assertIn("Raw message pairs and numeric participant observations are omitted", limitations)
        self.assertIn("Summaries do not establish algorithm cost, independent trials or extrapolation", limitations)
        self.assertIn("Consult the full trusted report", trusted_view["view_limitations"])
        self.assertEqual({**view, "view_limitations": trusted_view["view_limitations"]}, trusted_view)
        self.assertEqual(report_path.read_bytes(), original_report)
        self.assertEqual(packet["binding"], exporter.evidence_binding(packet["evidence"]))

    def test_stale_explicit_report_is_rejected(self):
        self.experiment(addition())
        report_path = self.report()
        (self.candidate / "proof.md").write_text("# Revised fixture\n")
        with self.assertRaisesRegex(VerificationError, "stale experiment evidence"):
            self.build(experiment_report=report_path)

    def test_symlink_report_is_rejected(self):
        self.experiment(addition())
        report_path = self.report()
        link = self.root / "linked-report"
        link.symlink_to(report_path)
        with self.assertRaisesRegex(VerificationError, "regular file"):
            self.build(experiment_report=link)

    def test_fresh_output_is_private_hash_checked_and_preserves_existing_files(self):
        packet = self.build()
        before = {str(p): p.read_bytes() for p in self.candidate.rglob("*") if p.is_file()}
        existing = self.root / "official-output"
        existing.mkdir()
        (existing / "score.json").write_text("preserve")
        with self.assertRaisesRegex(VerificationError, "never overwritten"):
            exporter.write_packet(packet, candidate=self.candidate, output_dir=existing)
        self.assertEqual((existing / "score.json").read_text(), "preserve")
        output = exporter.write_packet(packet, candidate=self.candidate, output_dir=self.root / "packet")
        self.assertEqual(output.stat().st_mode & 0o777, 0o700)
        manifest = json.loads((output / "manifest.json").read_text())
        for name, digest in manifest["files"].items():
            self.assertEqual(sha256_bytes((output / name).read_bytes()), digest)
        self.assertEqual(before, {str(p): p.read_bytes() for p in self.candidate.rglob("*") if p.is_file()})
        self.assertEqual(set(p.name for p in output.iterdir()), {"packet.json", "REVIEW.md", "manifest.json"})

    def test_output_in_repository_or_candidate_is_rejected(self):
        packet = self.build()
        for path in [exporter.ROOT / "new-review", self.candidate / "new-review"]:
            with self.subTest(path=path), self.assertRaisesRegex(VerificationError, "outside"):
                exporter.write_packet(packet, candidate=self.candidate, output_dir=path)
            self.assertFalse(path.exists())

    def test_temporary_directory_inside_candidate_is_rejected(self):
        with patch.object(exporter.tempfile, "gettempdir", return_value=str(self.candidate)):
            with self.assertRaisesRegex(VerificationError, "outside"):
                self.build()

    def test_inactive_track_cannot_export(self):
        log = io.StringIO()
        with redirect_stderr(log):
            self.assertEqual(exporter.main(["--track", "sha256-r31-rigorous"]), 2)
        self.assertIn("active full track ID", log.getvalue())

    def test_cli_writes_packet_for_active_organizer_fixture(self):
        # No production candidate is read: only path selection is replaced.
        class Selected:
            candidate = self.candidate
            id = self.track.id
        packet = self.build()
        log = io.StringIO()
        output = self.root / "cli-packet"
        with patch.object(exporter, "active_track", return_value=Selected()), \
             patch.object(exporter, "build_packet", return_value=packet), redirect_stdout(log):
            result = exporter.main(["--track", self.track.id, "--output-dir", str(output)])
        self.assertEqual(result, 0)
        self.assertIn(str(output), log.getvalue())
        self.assertIn("Advisory only", log.getvalue())
        self.assertEqual((output / "packet.json").read_bytes(), canonical_json_bytes(packet))


if __name__ == "__main__":
    unittest.main()
