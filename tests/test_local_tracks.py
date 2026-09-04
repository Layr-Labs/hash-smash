from concurrent.futures import ThreadPoolExecutor
from contextlib import redirect_stdout
from copy import deepcopy
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from judge.aggregate import aggregate_reviews
from judge.bedrock_adapter import BedrockClient, BedrockConfig
from judge.prompts import load_system_prompt
from judge.tests.helpers import review
from judge.tests.test_bedrock_adapter import FakeTransport, sol_response
from scripts import hashsmash_pipeline as pipeline
from scripts import local_tracks
from scripts.local_state import TrackBusyError, track_session
from verifier.certificates import verify_certificates
from verifier.errors import VerificationError
from verifier.hash_functions import digest, FULL_ROUNDS, IV, MASK
from verifier.intake import validate_candidate
from verifier.io import atomic_write_json
from verifier.schema_validation import validate_claim, validate_manifest
from verifier.score import build_score
from verifier.tracks import ROOT, all_tracks, get_track


def candidate_fixture(root, track, *, ready=True):
    candidate = root / "inputs" / track.id
    candidate.mkdir(parents=True)
    claim = track.draft_claim()
    claim["submission_state"] = "ready" if ready else "draft"
    # Deliberately not a proved attack: only fake-provider tests accept this text.
    atomic_write_json(candidate / "claim.json", claim)
    (candidate / "proof.md").write_text("# Mock-only fixture\nNot a cryptanalytic proof.\n")
    atomic_write_json(candidate / "certificates" / "manifest.json", {"schema_version": 2, "certificates": []})
    return candidate


def witness(candidate, track, *, message_b=None):
    a = bytes(40)
    b = bytes(32) + b"\x01" + bytes(7) if message_b is None else message_b
    (candidate / "certificates" / "a.bin").write_bytes(a)
    (candidate / "certificates" / "b.bin").write_bytes(b)
    certificate = {"id": "toy-control", "type": "hash-collision-witness-v2",
                   "target_profile": track.profile_id, "message_a": "certificates/a.bin",
                   "message_b": "certificates/b.bin", "expected_digest": digest(a, track.algorithm, track.rounds).hex()}
    atomic_write_json(candidate / "certificates" / "manifest.json", {"schema_version": 2, "certificates": [certificate]})
    return certificate


def reviews_for(track, claim):
    results = {}
    for stage in ("triage", "correctness", "complexity"):
        result = review(stage)
        result["claim"].update(target_profile=track.profile_id, rounds=track.rounds, restrictions=claim["restrictions"])
        if stage == "complexity":
            costs = dict(claim["claim"])
            costs["normalized_score_log2"] = costs["time_log2"] + costs["memory_log2_bytes"]
            result["submitted_cost"] = deepcopy(costs)
            result["recomputed_cost"] = deepcopy(costs)
            result["calculation_trace"] = ["Mock provider only; this does not qualify a real attack."]
        results[stage] = result
    return results


class HashReferenceTests(unittest.TestCase):
    def test_full_hashes_match_independent_hashlib_at_padding_boundaries(self):
        for algorithm, rounds in FULL_ROUNDS.items():
            for length in (0, 1, 3, 31, 40, 55, 56, 63, 64, 65, 119, 120, 127, 128, 1000):
                with self.subTest(algorithm=algorithm, length=length):
                    message = bytes(i % 251 for i in range(length))
                    self.assertEqual(digest(message, algorithm, rounds), hashlib.new(algorithm, message, usedforsecurity=False).digest())

    def test_reduced_sha_against_nist_intermediate_states_plus_feed_forward(self):
        # NIST SHA1.pdf / SHA256.pdf "abc" example, t=7, t=39 / t=23.
        # These external intermediate states test round truncation independently
        # of comparing the reference implementation to itself.
        vectors = (
            ("sha1", 8, "9E8C07D4 993E30C1 0FF1F290 B3F52677 F3763846"),
            ("sha1", 40, "32DE1CBA 4C986405 F718E5CF 03D447F6 F72EEC32"),
            ("sha256", 8, "85A07B5F E5030380 2B4209F5 04409A6A 0C657A79 9B27A401 714260AD 43ADA245"),
            ("sha256", 24, "C5D53D8D A7A3623F C2606D6D 9DC68B63 AA47C347 49F5114A E1257970 8ADA8930"),
        )
        for algorithm, rounds, working in vectors:
            words = (int(word, 16) for word in working.split())
            expected = b"".join(((a+b) & MASK).to_bytes(4, "big") for a, b in zip(IV[algorithm], words))
            self.assertEqual(digest(b"abc", algorithm, rounds), expected)

    def test_shallow_controls_have_real_full_message_collisions_not_full_round_collisions(self):
        a, b = bytes(40), bytes(32) + b"\x01" + bytes(7)
        for algorithm, full in FULL_ROUNDS.items():
            self.assertEqual(digest(a, algorithm, 8), digest(b, algorithm, 8))
            self.assertNotEqual(digest(a, algorithm, full), digest(b, algorithm, full))
            # Difference is in an ignored first-block word. Equality must persist
            # through a second block under the same reduced compression semantics.
            a2, b2 = a + bytes(70), b + bytes(70)
            self.assertEqual(digest(a2, algorithm, 8), digest(b2, algorithm, 8))

    def test_invalid_hash_parameters(self):
        for algorithm, rounds in (("unknown", 8), ("md5", 65), ("sha1", 0), ("sha256", True)):
            with self.assertRaises(ValueError):
                digest(b"", algorithm, rounds)
        with self.assertRaises(ValueError):
            digest("not bytes", "sha1", 80)

    def test_reduced_md5_against_direct_rfc_register_update_order(self):
        # Independent state layout: update A,D,C,B in place (RFC 1321), rather
        # than the production loop's rotating tuple. Full constants are also
        # covered independently by hashlib comparisons above.
        from struct import unpack
        from verifier.hash_functions import MD5_K
        for steps in (8, 24):
            for data in (b"abc", bytes(range(55)), bytes(range(128))):
                padded = data+b"\x80"+bytes((55-len(data)) % 64)+(8*len(data)).to_bytes(8, "little")
                state = list(IV["md5"])
                for offset in range(0, len(padded), 64):
                    words = unpack("<16I", padded[offset:offset+64])
                    work = state.copy()
                    for i in range(steps):
                        index = (-i) % 4
                        a, b, c, d = (work[(index+j) % 4] for j in range(4))
                        if i < 16:
                            f, g, s = (b & c) | (~b & d), i, (7, 12, 17, 22)[i % 4]
                        else:
                            f, g, s = (b & d) | (c & ~d), (1+5*(i-16)) % 16, (5, 9, 14, 20)[i % 4]
                        value = (a+f+words[g]+MD5_K[i]) & MASK
                        work[index] = (b+((value << s) | (value >> (32-s)))) & MASK
                    state = [(a+b) & MASK for a, b in zip(state, work)]
                expected = b"".join(word.to_bytes(4, "little") for word in state)
                self.assertEqual(digest(data, "md5", steps), expected)


class LocalTrackTests(unittest.TestCase):
    def test_registry_profiles_nominal_references_and_drafts(self):
        tracks = all_tracks()
        self.assertEqual(len(tracks), 9)
        self.assertEqual({t.algorithm for t in tracks}, {"md5", "sha1", "sha256"})
        for track in tracks:
            benchmark = track.benchmark()
            self.assertFalse(benchmark["frontier"]["is_qualified_baseline"])
            self.assertEqual(benchmark["frontier"]["score"], track.digest_bits)
            self.assertEqual(benchmark["target_profile"]["rounds"], track.rounds)
            self.assertEqual(validate_claim(track.draft_claim(), track=track)["submission_state"], "draft")
            with tempfile.TemporaryDirectory() as tmp:
                candidate = candidate_fixture(Path(tmp), track, ready=False)
                self.assertEqual(verify_certificates(candidate, track=track)["certificates"], [])
            self.assertNotIn("candidate", track.profile_path.parts)
            self.assertNotIn("candidates", track.profile_path.parts)

    def test_unknown_track_and_traversal_are_rejected(self):
        for track_id in ("../sha1-r8", "sha1-r9", "SHA1-r8", "md5-r8", ""):
            with self.assertRaises(VerificationError):
                get_track(track_id)

    def test_cross_track_claim_rounds_units_state_and_reference_are_rejected(self):
        track = get_track("sha256-r24")
        claim = track.draft_claim()
        for field, wrong in (("target_profile", "sha1-r40-prefix-v1"), ("rounds", 8),
                             ("submission_state", "qualified"), ("baseline_improved", "invented"),
                             ("schema_version", 1)):
            with self.subTest(field=field), self.assertRaises(VerificationError):
                validate_claim(dict(claim, **{field: wrong}), track=track)
        claim["claim"]["time_unit"] = "sha1-compressions"
        with self.assertRaises(VerificationError):
            validate_claim(claim, track=track)

    def test_selected_hash_collision_certificates_and_cross_track_rejection(self):
        for track_id in ("md5-s8", "sha1-r8", "sha256-r8"):
            track = get_track(track_id)
            with tempfile.TemporaryDirectory() as tmp:
                candidate = candidate_fixture(Path(tmp), track)
                certificate = witness(candidate, track)
                self.assertEqual(len(verify_certificates(candidate, track=track)["certificates"]), 1)
                wrong = dict(certificate, target_profile="sha1-r80-prefix-v1")
                with self.assertRaises(VerificationError):
                    validate_manifest({"schema_version": 2, "certificates": [wrong]}, track=track)
                witness(candidate, track, message_b=bytes(40))
                with self.assertRaisesRegex(VerificationError, "must differ"):
                    verify_certificates(candidate, track=track)
                witness(candidate, track, message_b=b"not a collision")
                with self.assertRaisesRegex(VerificationError, "does not match"):
                    verify_certificates(candidate, track=track)

    def test_draft_cannot_reach_provider_or_become_a_nominal_score(self):
        track = get_track("md5-s8")
        with tempfile.TemporaryDirectory() as tmp, patch.object(pipeline, "_provider_from_env") as provider, redirect_stdout(io.StringIO()):
            p = pipeline.RunPaths.for_track(track, state_root=Path(tmp), candidate=candidate_fixture(Path(tmp), track, ready=False))
            self.assertEqual(pipeline.run_all(p), 2)
            with self.assertRaisesRegex(VerificationError, "draft"):
                pipeline.run_judge(p)
            with self.assertRaisesRegex(VerificationError, "draft"):
                build_score(p.candidate, {"status": "ai_qualified"}, track=track)
            provider.assert_not_called()
            self.assertFalse(p.score.exists())

    def test_every_track_fake_bedrock_pipeline_and_isolated_score_contract(self):
        with tempfile.TemporaryDirectory() as tmp, redirect_stdout(io.StringIO()):
            root = Path(tmp)
            config = BedrockConfig(api_key="fake-test-key", model="us.openai.gpt-5.6-sol", max_attempts=1)
            seen_paths = set()
            for track in all_tracks():
                p = pipeline.RunPaths.for_track(track, state_root=root, candidate=candidate_fixture(root, track))
                claim = json.loads((p.candidate / "claim.json").read_text())
                reviews = reviews_for(track, claim)
                transport = FakeTransport([sol_response(reviews[stage]) for stage in ("triage", "correctness", "complexity")])
                with patch.object(pipeline, "_provider_from_env", return_value=(
                    "bedrock", config, lambda cfg: BedrockClient(cfg, transport=transport),
                )), patch.dict("os.environ", {"HASHSMASH_JUDGE_MODE": "single"}):
                    self.assertEqual(pipeline.run_all(p), 0)
                self.assertNotIn(p.score, seen_paths)
                seen_paths.add(p.score)
                score = json.loads(p.score.read_text())
                self.assertEqual(score["score"], track.digest_bits)
                self.assertFalse(score["metrics"]["referenceIsQualifiedBaseline"])
                self.assertFalse(score["metrics"]["improvesNominalReference"])
                self.assertEqual(score["metrics"]["trackId"], track.id)
                dossier = json.loads(p.dossier.read_text())
                self.assertEqual(dossier["judge_configuration"]["target_config_sha256"], track.config_sha256())
            self.assertEqual(len(list((root / "scores").glob("*.json"))), 9)

    def test_stale_candidate_evidence_and_configuration_fail_before_provider_or_score(self):
        track = get_track("sha1-r8")
        with tempfile.TemporaryDirectory() as tmp, redirect_stdout(io.StringIO()):
            p = pipeline.RunPaths.for_track(track, state_root=Path(tmp), candidate=candidate_fixture(Path(tmp), track))
            pipeline.run_intake(p)
            intake = validate_candidate(p.candidate, track=track)
            aggregate = {"status": "ai_qualified", "claim": intake["claim"],
                         "input_package_sha256": intake["package_sha256"], "target_config_sha256": track.config_sha256()}
            with self.assertRaisesRegex(VerificationError, "target configuration"):
                build_score(p.candidate, dict(aggregate, target_config_sha256="0"*64), track=track)
            (p.candidate / "proof.md").write_text("# Changed after review\n")
            with patch.object(pipeline, "_provider_from_env") as provider:
                with self.assertRaisesRegex(VerificationError, "numbered proof"):
                    pipeline.run_judge(p)
                provider.assert_not_called()
            with self.assertRaisesRegex(VerificationError, "candidate package"):
                build_score(p.candidate, aggregate, track=track)

    def test_cost_reconstruction_must_match_intake_not_another_tracks_nominal_values(self):
        track = get_track("sha256-r24")
        claim = track.draft_claim()
        reviews = reviews_for(track, claim)
        for cost in (reviews["complexity"]["submitted_cost"], reviews["complexity"]["recomputed_cost"]):
            cost["time_log2"] = 80
            cost["normalized_score_log2"] = 80 + cost["memory_log2_bytes"]
        result = aggregate_reviews(reviews, expected_claim=claim)
        self.assertEqual(result["status"], "clarification_required")
        self.assertTrue(any("submitted cost differs" in reason for reason in result["reasons"]))

    def test_bad_round_witness_cannot_be_relabelled_as_full_round(self):
        track = get_track("sha1-r80")
        with tempfile.TemporaryDirectory() as tmp:
            candidate = candidate_fixture(Path(tmp), track)
            certificate = witness(candidate, track)
            certificate["expected_digest"] = digest(bytes(40), "sha1", 8).hex()
            atomic_write_json(candidate / "certificates" / "manifest.json", {"schema_version": 2, "certificates": [certificate]})
            with self.assertRaisesRegex(VerificationError, "does not match"):
                verify_certificates(candidate, track=track)

    def test_parallel_intakes_do_not_share_paths_or_delete_sibling_scores(self):
        tracks = (get_track("md5-s8"), get_track("sha256-r8"))
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
            p = pipeline.RunPaths.for_track(get_track("md5-s8"), state_root=Path(tmp))
            with track_session(p, "intake") as record:
                atomic_write_json(p.work / "intake-report.json", {"mock": True})
                (p.work / ".env").write_text("DO NOT ARCHIVE")
                with self.assertRaises(TrackBusyError):
                    with track_session(p, "all"):
                        pass
                sibling = pipeline.RunPaths.for_track(get_track("sha1-r8"), state_root=Path(tmp))
                with track_session(sibling, "intake") as other:
                    other["exit_code"] = 2
                record["exit_code"] = 2
            archive = list((p.reports / "runs").glob("*/run.json"))
            self.assertEqual(len(archive), 1)
            self.assertEqual(json.loads(archive[0].read_text())["exit_code"], 2)
            self.assertEqual({f.name for f in archive[0].parent.iterdir()}, {"run.json", "intake-report.json"})

    def test_history_status_ignores_failed_or_wrong_target_scores(self):
        track = get_track("md5-s8")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            candidate = candidate_fixture(root, track)
            # Use the public path shape with an isolated root; no mutable solver file.
            p = pipeline.RunPaths.for_track(track, state_root=root / ".yukon", candidate=candidate)
            intake = validate_candidate(candidate, track=track)
            metrics = {"trackId": track.id, "reviewStatus": "ai_qualified",
                       "targetConfigSha256": track.config_sha256(), "inputPackageSha256": intake["package_sha256"]}
            for name, exit_code, configuration, score in (("valid", 0, track.config_sha256(), 100),
                                                         ("failed", 3, track.config_sha256(), 1),
                                                         ("wrong-target", 0, "0"*64, 0)):
                archive = p.reports / "runs" / name
                atomic_write_json(archive / "run.json", {"run_id": name, "command": "all", "exit_code": exit_code})
                atomic_write_json(archive / "score.json", {"score": score, "metrics": dict(metrics, targetConfigSha256=configuration)})
            with patch.object(local_tracks, "ROOT", root), patch.object(type(track), "candidate", candidate):
                result = local_tracks.status(track)
                self.assertIsNone(result["qualified_baseline"])
                self.assertEqual(result["best_ai_reviewed"]["score"], 100)
                self.assertTrue(result["best_ai_reviewed"]["current_candidate"])
                (candidate / "proof.md").write_text("# New draft after the historical result\n")
                self.assertFalse(local_tracks.status(track)["best_ai_reviewed"]["current_candidate"])

    def test_explicit_intake_cli_archives_draft_without_score_or_provider(self):
        track = get_track("md5-s8")
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

    def test_prompt_defines_nominal_reference_non_authority_and_selected_targets(self):
        prompt = load_system_prompt("complexity")
        self.assertIn("nominal-reference-only", prompt)
        self.assertIn("NOT an established attack", prompt)
        self.assertIn("prefix round range applies on every block", prompt)

    def test_credential_free_cli_lists_and_shows_without_reading_mutable_candidates(self):
        for arguments in (("list", "--collection", "legacy"), ("show", "sha256-r64")):
            result = subprocess.run([sys.executable, "scripts/local_tracks.py", *arguments], cwd=ROOT,
                                    capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("sha256-r64", result.stdout)


if __name__ == "__main__":
    unittest.main()
