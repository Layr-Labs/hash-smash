"""Organizer-only migration regressions; never execute or evaluate solver content."""

from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
from decimal import Decimal, localcontext
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import export_review_packet, import_yukon_dev, hashsmash_pipeline as pipeline
from scripts.reference_operation_costs import reference_costs
from scripts.validate_frontier_config import import_tracks, validate_configuration
from tests.helpers import candidate_fixture
from tests.test_frontier_pipeline import fake_provider
from verifier import frontier_tracks as registry, hash_functions
from verifier.schema_validation import validate_claim
from verifier.errors import VerificationError
from verifier.intake import validate_candidate
from verifier.io import atomic_write_json

ROOT = registry.ROOT
NEW_IDS = {f"sha256-r{r}-exploratory" for r in (37, 38)}
OLD_IDS = {f"sha256-r{r}-{lane}" for r in (31, 32) for lane in registry.LANES}


def independent_sha256(message, rounds):
    """FIPS 180-4 sections 4.2.2, 5 and 6.2, with a prefix round limit.

    Independent test oracle: derive constants from primes (not production tables),
    expand all 64 words, and use a list state instead of the production core.
    Full-round answers are cross-checked against hashlib below. Reduced answers
    check round choice, chaining, feed-forward, padding and full serialization.
    """
    primes = [n for n in range(2, 312) if all(n % d for d in range(2, int(n**0.5) + 1))]
    with localcontext() as ctx:
        ctx.prec = 80
        def fraction_word(value):
            return int((value - int(value)) * (1 << 32))
        state = [fraction_word(Decimal(p).sqrt()) for p in primes[:8]]
        constants = [fraction_word(Decimal(p) ** (Decimal(1) / 3)) for p in primes[:64]]
    mask = (1 << 32) - 1
    def rotate(value, bits):
        return ((value >> bits) | (value << (32 - bits))) & mask
    padded = bytearray(message)
    padded.append(128)
    while len(padded) % 64 != 56:
        padded.append(0)
    padded.extend((len(message) * 8).to_bytes(8, "big"))
    for start in range(0, len(padded), 64):
        block = padded[start:start + 64]
        words = [int.from_bytes(block[i:i + 4], "big") for i in range(0, 64, 4)]
        for index in range(16, 64):
            x, y = words[index - 15], words[index - 2]
            words.append((words[index - 16] + words[index - 7]
                          + (rotate(x, 7) ^ rotate(x, 18) ^ (x >> 3))
                          + (rotate(y, 17) ^ rotate(y, 19) ^ (y >> 10))) & mask)
        working = state[:]
        for index in range(rounds):
            a, b, c, d, e, f, g, h = working
            temp1 = (h + (rotate(e, 6) ^ rotate(e, 11) ^ rotate(e, 25))
                     + ((e & f) ^ ((mask ^ e) & g)) + constants[index] + words[index]) & mask
            temp2 = ((rotate(a, 2) ^ rotate(a, 13) ^ rotate(a, 22))
                     + ((a & b) ^ (a & c) ^ (b & c))) & mask
            working = [(temp1 + temp2) & mask, a, b, c, (d + temp1) & mask, e, f, g]
        state = [(a + b) & mask for a, b in zip(state, working)]
    return b"".join(value.to_bytes(4, "big") for value in state)


class Sha256MigrationTests(unittest.TestCase):
    def test_only_two_new_lanes_and_four_preserved_historical_identities(self):
        tracks = registry.frontier_tracks()
        self.assertEqual(len(tracks), 26)
        self.assertEqual(len(registry.frontier_tracks(include_retired=False)), 22)
        self.assertEqual({t.id for t in tracks if t.retired}, OLD_IDS)
        active = {t.id for t in import_tracks()}
        self.assertEqual(active & {t.id for t in tracks if t.algorithm == "sha256"}, NEW_IDS | {f"sha256-r{r}-exploratory" for r in (31, 32)})
        self.assertTrue({f"sha256-r{r}-exploratory" for r in (31, 32)} <= active)
        for rounds in (37, 38):
            with self.assertRaises(VerificationError):
                registry.get_frontier_track(f"sha256-r{rounds}-rigorous")
            self.assertFalse((ROOT / f"lanes/rigorous/candidates/sha256-r{rounds}").exists())
        for track_id in OLD_IDS:
            track = registry.get_frontier_track(track_id)
            self.assertEqual(track.selection_status, "selected")
            self.assertEqual(track.boundary_role, "predecessor" if track.rounds == 31 else "boundary")
            self.assertEqual(track.profile_id, f"sha256-r{track.rounds}-prefix-v1")
            self.assertEqual(track.reference_id, f"sha256-r{track.rounds}-nominal-v2")
            if track.lane == "rigorous":
                with self.assertRaises(VerificationError):
                    export_review_packet.active_track(track_id)
            else:
                self.assertEqual(export_review_packet.active_track(track_id).id, track_id)
        for track_id in NEW_IDS:
            track = export_review_packet.active_track(track_id)
            self.assertEqual(track.selection_status, "organizer_selected")
            self.assertIn(track.boundary_role, ("lower-exploration", "upper-exploration"))

    def test_current_plans_exclude_history_and_unassigned_rigorous_lanes(self):
        status = validate_configuration()
        self.assertEqual(status, {"planned_tracks": 26, "runnable_tracks": 26,
                                 "retired_tracks": 4, "pending_tracks": 4,
                                 "import_tracks": 8, "yukon_challenges": 1})
        slots = registry.planned_slots()
        self.assertEqual({s["family"] for s in slots if s["rounds"] is None}, {"poseidon"})
        sha_slots = [s for s in slots if s["family"] == "sha256"]
        self.assertEqual([(s["rounds"], s["lane"]) for s in sha_slots], [(37, "exploratory"), (38, "exploratory")])
        with self.assertRaisesRegex(VerificationError, "unresolved"):
            validate_configuration(require_complete=True)

    def test_catalog_rejects_malformed_lanes_and_history(self):
        base = registry.catalog()
        mutations = []
        for lanes in ([], "exploratory", ["unknown"], ["exploratory", "exploratory"], [None], [{}]):
            mutations.append(lambda f, lanes=lanes: f.update(lanes=lanes))
            mutations.append(lambda f, lanes=lanes: f["historical_pairs"][0].update(lanes=lanes))
        for history in ({}, None, ["bad"], [{}]):
            mutations.append(lambda f, history=history: f.update(historical_pairs=history))
        mutations.extend([
            lambda f: f["historical_pairs"].append(deepcopy(f["historical_pairs"][0])),
            lambda f: f["historical_pairs"][0].update(round_pair=[37, 38], first_unbroken_round=38),
            lambda f: f["historical_pairs"][0].update(algorithm="sha1"),
            lambda f: f["historical_pairs"][0].update(round_pair=None),
            lambda f: f["historical_pairs"][0].update(round_pair=[31, 33]),
            lambda f: f["historical_pairs"][0].update(selection_status="unknown"),
            lambda f: f["historical_pairs"][0].update(selection_note=""),
            lambda f: f.update(first_unbroken_round=38),
        ])
        for index, mutate in enumerate(mutations):
            data = deepcopy(base)
            mutate(next(f for f in data["families"] if f["id"] == "sha256"))
            with self.subTest(index=index), patch.object(registry, "load_json_bytes", return_value=data):
                with self.assertRaises(VerificationError):
                    registry.catalog()

    def test_reference_costs_reproduce_old_and_new_prices(self):
        expected_old = {"md5-s63": 843, "md5-s64": 856, "sha1-r79": 1957, "sha1-r80": 1982,
                        "sha256-r31": 2140, "sha256-r32": 2224, "sha3-256-r5": 1355,
                        "sha3-256-r6": 1626, "keccak800-r5": 1355, "keccak800-r6": 1626,
                        "blake3-r1": 222, "blake3-r2": 430}
        prices = reference_costs()
        self.assertEqual(prices, {**expected_old, "sha256-r37": 2644, "sha256-r38": 2728})
        for track_id in NEW_IDS:
            track = registry.get_frontier_track(track_id)
            self.assertEqual(track.benchmark()["cost_model"]["operation_weights"],
                             {"target_compression": 1.0, "word_operation": 1 / prices[track.target_id]})

    def test_full_message_prefix_rounds_against_independent_reference(self):
        messages = [b"", b"abc"] + [bytes(i % 256 for i in range(n)) for n in (55, 56, 63, 64, 65, 119, 120, 128, 193)]
        for message in messages:
            with self.subTest(length=len(message)):
                self.assertEqual(independent_sha256(message, 64), hashlib.sha256(message).digest())
                results = []
                for rounds in (31, 32, 37, 38):
                    actual = hash_functions.digest(message, "sha256", rounds)
                    self.assertEqual(actual, independent_sha256(message, rounds))
                    self.assertEqual(len(actual), 32)
                    results.append(actual)
                self.assertEqual(len(set(results)), 4)

    def test_every_padded_block_uses_selected_round_count_and_chaining(self):
        for rounds in (37, 38):
            for length in (0, 55, 56, 64, 120, 193):
                with self.subTest(rounds=rounds, length=length):
                    original = hash_functions._compress
                    calls = []
                    def record(algorithm, state, block, count):
                        result = original(algorithm, state, block, count)
                        calls.append((state, block, count, result))
                        return result
                    message = bytes(length)
                    with patch.object(hash_functions, "_compress", side_effect=record):
                        digest = hash_functions.digest(message, "sha256", rounds)
                    self.assertEqual(len(calls), (length + 9 + 63) // 64)
                    self.assertEqual(calls[0][0], hash_functions.IV["sha256"])
                    for before, after in zip(calls, calls[1:]):
                        self.assertEqual(after[0], before[3])
                    self.assertTrue(all(call[2] == rounds for call in calls))
                    self.assertEqual(calls[-1][1][-8:], (length * 8).to_bytes(8, "big"))
                    self.assertEqual(digest, b"".join(w.to_bytes(4, "big") for w in calls[-1][3]))

    def test_new_claims_cannot_change_rounds_profile_lane_or_reference(self):
        for track_id in NEW_IDS:
            track = registry.get_frontier_track(track_id)
            for field, value in (("rounds", 31), ("target_profile", "sha256-r31-prefix-v1"),
                                 ("lane", "rigorous"), ("baseline_improved", "sha256-r31-nominal-v2")):
                claim = track.draft_claim()
                claim[field] = value
                with self.subTest(track=track_id, field=field), self.assertRaises(VerificationError):
                    validate_claim(claim, track=track)

    def test_new_drafts_stop_before_providers_and_never_score(self):
        for track_id in NEW_IDS:
            track = registry.get_frontier_track(track_id)
            with tempfile.TemporaryDirectory() as tmp, redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                root = Path(tmp)
                candidate = candidate_fixture(root, track, ready=False)
                paths = pipeline.RunPaths.for_track(track, state_root=root / "state", candidate=candidate)
                with patch.object(pipeline, "_provider_from_env") as provider:
                    self.assertEqual(pipeline._execute("all", paths), 2)
                    provider.assert_not_called()
                self.assertFalse(paths.score.exists())
                self.assertEqual(validate_candidate(candidate, track=track)["submission_state"], "draft")

    def test_import_draft_guard_uses_new_roster_before_credentials(self):
        # Mock only package reads; import routing and draft/readiness guard are real.
        def intake(candidate, *, track):
            return {"submission_state": "draft" if track.id in NEW_IDS else "ready"}
        with patch.object(import_yukon_dev, "validate_candidate", side_effect=intake), \
                patch.object(import_yukon_dev, "importer_token") as token, \
                patch.object(import_yukon_dev, "DevClient") as client, \
                redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            self.assertEqual(set(import_yukon_dev.draft_tracks()), NEW_IDS)
            self.assertEqual(import_yukon_dev.main(["--submit"]), 2)
            token.assert_not_called()
            client.assert_not_called()

    def test_transitive_shared_file_changes_remain_bound_for_all_existing_lanes(self):
        tracks = [t for t in registry.frontier_tracks() if t.id not in NEW_IDS]
        self.assertEqual(len(tracks), 24)
        originals = {t.id: t.config_sha256() for t in tracks}
        read_bytes = Path.read_bytes
        for relative in ("verifier/frontier_tracks.py", "schemas/claim-frontier-v3.schema.json",
                         "cost-models/collision-frontier-v5.json"):
            def change(path):
                content = read_bytes(path)
                if path == ROOT / relative:
                    if relative.startswith("cost-models/"):
                        cost = json.loads(content)
                        cost["reference_operation_costs"]["sha256-r37"] += 1
                        return json.dumps(cost).encode()
                    return content + b"\n"
                return content
            with self.subTest(file=relative), patch.object(Path, "read_bytes", change):
                for track in tracks:
                    self.assertNotEqual(track.config_sha256(), originals[track.id])

    def test_stale_configuration_still_blocks_scoring_new_lanes(self):
        for track_id in NEW_IDS:
            track = registry.get_frontier_track(track_id)
            with tempfile.TemporaryDirectory() as tmp, redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                root = Path(tmp)
                candidate = candidate_fixture(root, track)
                paths = pipeline.RunPaths.for_track(track, state_root=root / "state", candidate=candidate)
                with fake_provider():
                    self.assertEqual(pipeline.run_all(paths), 0)
                aggregate = json.loads(paths.aggregate.read_text())
                aggregate["target_config_sha256"] = "0" * 64
                atomic_write_json(paths.aggregate, aggregate)
                with patch.object(pipeline, "_provider_from_env") as provider:
                    self.assertEqual(pipeline._execute("score", paths), 2)
                    provider.assert_not_called()
                self.assertFalse(paths.score.exists())


if __name__ == "__main__":
    unittest.main()
