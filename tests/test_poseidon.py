"""Official Orchard Poseidon vectors, pinned deployed constants and domain gates."""

import json
from pathlib import Path
import unittest
from unittest.mock import patch

from verifier import poseidon
from verifier.hash_functions import digest

FIXTURE = json.loads((Path(__file__).parent / "fixtures/orchard-poseidon-vectors.json").read_text())


def element(encoded: str) -> int:
    """Decode the fixture's canonical 32-byte little-endian hex encoding."""
    return int.from_bytes(bytes.fromhex(encoded), "little")


def reference_prefix(message: bytes, rounds: int) -> bytes:
    """Independent restatement of the round definition, not the code under test.

    Written directly from the deployed schedule: four leading full rounds,
    56 partial rounds, four trailing full rounds, each round adding its
    constants, applying x^5, then multiplying by the MDS matrix. The S-box uses
    pow() rather than the implementation's three-multiplication chain.
    """
    modulus = int(FIXTURE["field_modulus_hex"], 16)
    constants = [[element(value) for value in row] for row in FIXTURE["round_constants"]]
    mds = [[element(value) for value in row] for row in FIXTURE["mds"]]
    capacity = int(FIXTURE["capacity_element_hex"], 16)
    leading = FIXTURE["full_rounds"] // 2
    state = [
        int.from_bytes(message[0:32], "little"),
        int.from_bytes(message[32:64], "little"),
        capacity,
    ]
    for index in range(rounds):
        row = constants[index]
        if index < leading or index >= leading + FIXTURE["partial_rounds"]:
            state = [pow((state[i] + row[i]) % modulus, 5, modulus) for i in range(3)]
        else:
            state = [(state[i] + row[i]) % modulus for i in range(3)]
            state[0] = pow(state[0], 5, modulus)
        state = [sum(mds[i][j] * state[j] for j in range(3)) % modulus for i in range(3)]
    return state[0].to_bytes(32, "little")


class PoseidonVectorTests(unittest.TestCase):
    def test_official_permutation_vectors(self):
        vectors = FIXTURE["permutation_vectors"]
        self.assertEqual(len(vectors), 11)
        for index, vector in enumerate(vectors):
            with self.subTest(vector=index):
                initial = [element(value) for value in vector["initial_state"]]
                expected = [element(value) for value in vector["final_state"]]
                self.assertEqual(poseidon.permutation(initial), expected)

    def test_official_hash_vectors(self):
        vectors = FIXTURE["hash_vectors"]
        self.assertEqual(len(vectors), 11)
        for index, vector in enumerate(vectors):
            with self.subTest(vector=index):
                message = bytes.fromhex(vector["message"])
                self.assertEqual(digest(message, "poseidon", 64).hex(), vector["digest"])

    def test_hash_equals_permuting_the_deployed_initial_state(self):
        # The relation upstream's own orchard_spec_equivalence test asserts.
        for vector in FIXTURE["hash_vectors"]:
            message = bytes.fromhex(vector["message"])
            state = [
                int.from_bytes(message[0:32], "little"),
                int.from_bytes(message[32:64], "little"),
                poseidon.CAPACITY_ELEMENT,
            ]
            self.assertEqual(
                poseidon.permutation(state)[0].to_bytes(32, "little").hex(), vector["digest"]
            )


class PoseidonParameterTests(unittest.TestCase):
    def test_deployed_constants_match_the_pinned_source(self):
        constants = [[element(value) for value in row] for row in FIXTURE["round_constants"]]
        mds = [[element(value) for value in row] for row in FIXTURE["mds"]]
        self.assertEqual(len(constants), 64)
        self.assertEqual(sum(len(row) for row in constants), 192)
        self.assertEqual([list(row) for row in poseidon.ROUND_CONSTANTS], constants)
        self.assertEqual([list(row) for row in poseidon.MDS], mds)
        self.assertEqual(poseidon.MODULUS, int(FIXTURE["field_modulus_hex"], 16))
        self.assertEqual(poseidon.CAPACITY_ELEMENT, int(FIXTURE["capacity_element_hex"], 16))
        self.assertEqual(poseidon.CAPACITY_ELEMENT, 2 << 64)

    def test_every_constant_is_a_canonical_field_element(self):
        for row in poseidon.ROUND_CONSTANTS + poseidon.MDS:
            for value in row:
                self.assertTrue(0 <= value < poseidon.MODULUS)

    def test_round_schedule_matches_the_deployment(self):
        self.assertEqual((poseidon.FULL_ROUNDS, poseidon.PARTIAL_ROUNDS), (8, 56))
        self.assertEqual(poseidon.TOTAL_ROUNDS, 64)
        full = [index for index in range(64) if poseidon.is_full_round(index)]
        self.assertEqual(full, [0, 1, 2, 3, 60, 61, 62, 63])
        self.assertEqual(64 - len(full), 56)

    def test_sbox_is_the_fifth_power(self):
        for value in (0, 1, 2, 7, poseidon.MODULUS - 1, poseidon.ROUND_CONSTANTS[0][0]):
            self.assertEqual(
                poseidon._sbox(value), pow(value, poseidon.SBOX_EXPONENT, poseidon.MODULUS)
            )

    def test_output_space_is_the_field_not_the_encoding(self):
        # 32 bytes of encoding, but the output space is p, about 2^254.
        self.assertLess(poseidon.MODULUS, 1 << 255)
        self.assertGreater(poseidon.MODULUS, 1 << 254)


class PoseidonDomainTests(unittest.TestCase):
    def encode(self, first: int, second: int) -> bytes:
        return first.to_bytes(32, "little") + second.to_bytes(32, "little")

    def test_domain_failures_use_the_dedicated_error_but_stay_value_errors(self):
        canonical = self.encode(1, 2)
        shifted = self.encode(1 + poseidon.MODULUS, 2)
        for data in (shifted, bytes(63), b"", "x" * 64):
            with self.subTest(case=type(data).__name__ + str(len(data))):
                with self.assertRaises(poseidon.MessageDomainError):
                    poseidon.decode_message(data)
        self.assertTrue(issubclass(poseidon.MessageDomainError, ValueError))
        # A configuration fault is a plain ValueError, not a domain failure.
        with self.assertRaises(ValueError) as caught:
            digest(canonical, "poseidon", 0)
        self.assertNotIsInstance(caught.exception, poseidon.MessageDomainError)

    def test_non_canonical_field_elements_are_rejected(self):
        modulus = poseidon.MODULUS
        for offending in (modulus, modulus + 1, (1 << 256) - 1):
            for position in (0, 1):
                values = [1, 1]
                values[position] = offending
                with self.subTest(offending=hex(offending), position=position):
                    with self.assertRaises(ValueError):
                        digest(self.encode(*values), "poseidon", 64)

    def test_a_shifted_encoding_would_otherwise_be_a_trivial_collision(self):
        # x and x + p reduce to the same field element, so accepting the second
        # encoding would hand out a collision for free. It must be rejected.
        canonical = self.encode(1, 2)
        shifted = self.encode(1 + poseidon.MODULUS, 2)
        self.assertNotEqual(canonical, shifted)
        self.assertEqual(
            int.from_bytes(shifted[0:32], "little") % poseidon.MODULUS,
            int.from_bytes(canonical[0:32], "little") % poseidon.MODULUS,
        )
        self.assertEqual(len(digest(canonical, "poseidon", 64)), 32)
        with self.assertRaises(ValueError):
            digest(shifted, "poseidon", 64)

    def test_wrong_message_lengths_are_rejected(self):
        for length in (0, 1, 31, 32, 33, 63, 65, 96, 128):
            with self.subTest(length=length):
                with self.assertRaises(ValueError):
                    digest(bytes(length), "poseidon", 64)

    def test_non_bytes_messages_are_rejected(self):
        for data in (None, "a" * 64, bytearray(64), [0] * 64, memoryview(bytes(64))):
            with self.subTest(data=type(data).__name__):
                with self.assertRaises(ValueError):
                    digest(data, "poseidon", 64)

    def test_invalid_round_counts_fail_closed(self):
        message = self.encode(1, 2)
        for rounds in (0, -1, 65, 100, True, 1.0, "1", None):
            with self.subTest(rounds=rounds):
                with self.assertRaises(ValueError):
                    digest(message, "poseidon", rounds)

    def test_permutation_rejects_malformed_states(self):
        for state in ([1, 2], [1, 2, 3, 4], [1, 2, poseidon.MODULUS], [1, 2, -1], [1, 2, True]):
            with self.subTest(state=state):
                with self.assertRaises(ValueError):
                    poseidon.permutation(state)


class PoseidonPrefixRoundTests(unittest.TestCase):
    MESSAGE = (7).to_bytes(32, "little") + (11).to_bytes(32, "little")

    def test_rounds_one_and_two_match_an_independent_reference(self):
        for rounds in (1, 2):
            with self.subTest(rounds=rounds):
                self.assertEqual(
                    digest(self.MESSAGE, "poseidon", rounds), reference_prefix(self.MESSAGE, rounds)
                )

    def test_every_prefix_matches_the_independent_reference(self):
        # The implementation must already support any prefix from 1 to 64,
        # so a later round pair needs no code change.
        for rounds in range(1, 65):
            with self.subTest(rounds=rounds):
                self.assertEqual(
                    digest(self.MESSAGE, "poseidon", rounds), reference_prefix(self.MESSAGE, rounds)
                )

    def test_prefixes_are_distinct_from_each_other_and_from_the_deployment(self):
        digests = {rounds: digest(self.MESSAGE, "poseidon", rounds) for rounds in (1, 2, 64)}
        self.assertNotEqual(digests[1], digests[2])
        self.assertNotEqual(digests[1], digests[64])
        self.assertNotEqual(digests[2], digests[64])
        self.assertEqual({len(value) for value in digests.values()}, {32})

    def test_the_first_two_rounds_are_full_rounds(self):
        # Rounds 1 and 2 apply the S-box to all three elements.
        self.assertTrue(poseidon.is_full_round(0))
        self.assertTrue(poseidon.is_full_round(1))


class PoseidonTrackTests(unittest.TestCase):
    def tracks(self):
        from verifier.frontier_tracks import get_frontier_track

        return [get_frontier_track(f"poseidon-r{rounds}-exploratory") for rounds in (1, 2)]

    def test_both_targets_resolve_with_the_expected_identity(self):
        for rounds, track in zip((1, 2), self.tracks()):
            with self.subTest(rounds=rounds):
                self.assertEqual(track.target_id, f"poseidon-r{rounds}")
                self.assertEqual(track.profile_id, f"poseidon-r{rounds}-prefix-v1")
                self.assertEqual(track.reference_id, f"poseidon-r{rounds}-nominal-v2")
                self.assertEqual(track.algorithm, "poseidon")
                self.assertEqual(track.rounds, rounds)
                self.assertEqual(track.lane, "exploratory")
                self.assertEqual(track.selection_status, "organizer_selected")
                self.assertFalse(track.retired)

    def test_exploration_pair_asserts_no_first_unbroken_boundary(self):
        roles = [track.boundary_role for track in self.tracks()]
        self.assertEqual(roles, ["lower-exploration", "upper-exploration"])

    def test_nominal_reference_is_the_field_exponent_not_half_the_encoding(self):
        for track in self.tracks():
            with self.subTest(track=track.id):
                self.assertEqual(track.digest_bits, 256)
                self.assertEqual(track.nominal_security_bits, 127)
                self.assertEqual(track.nominal_score, 127.0)
                # The draft template must agree with the published reference.
                self.assertEqual(track.draft_claim()["claim"]["time_log2"], 127.0)
                frontier = track.benchmark()["frontier"]
                self.assertEqual(frontier["nominal_collision_security_bits"], 127)
                self.assertEqual(frontier["score"], 127.0)
                self.assertFalse(frontier["is_qualified_baseline"])

    def test_cost_weights_use_the_published_field_operation_price(self):
        for expected, track in zip((27, 54), self.tracks()):
            with self.subTest(track=track.id):
                weights = track.benchmark()["cost_model"]["operation_weights"]
                self.assertEqual(weights, {"target_compression": 1.0, "word_operation": 1 / expected})

    def test_no_rigorous_poseidon_lane_exists(self):
        from verifier.errors import VerificationError
        from verifier.frontier_tracks import frontier_tracks, get_frontier_track

        poseidon_tracks = [t.id for t in frontier_tracks() if t.algorithm == "poseidon"]
        self.assertEqual(poseidon_tracks, ["poseidon-r1-exploratory", "poseidon-r2-exploratory"])
        for undefined in ("poseidon-r1-rigorous", "poseidon-r2-rigorous", "poseidon-r8-exploratory"):
            with self.subTest(undefined=undefined), self.assertRaises(VerificationError):
                get_frontier_track(undefined)

    def test_profile_round_selection_states_the_prefix_convention(self):
        from verifier.io import load_json_bytes

        for track in self.tracks():
            profile = load_json_bytes(track.profile_path.read_bytes(), str(track.profile_path))
            with self.subTest(track=track.id):
                self.assertEqual(profile["digest_bits"], 256)
                self.assertEqual(profile["rounds"], track.rounds)
                self.assertEqual(profile["full_rounds"], 64)
                self.assertIn("R_F=8/R_P=56", profile["round_selection"])
                self.assertIn("64 bytes", profile["message_domain"])
                self.assertIn("x + p", profile["message_domain"])
                self.assertEqual(profile["reference_implementation"], "verifier/poseidon.py:poseidon")


class PoseidonCertificateTests(unittest.TestCase):
    """The verifier itself must refuse a non-canonical witness."""

    def build(self, directory, message_a, message_b):
        from verifier.frontier_tracks import get_frontier_track
        from verifier.io import atomic_write_json

        track = get_frontier_track("poseidon-r1-exploratory")
        candidate = Path(directory) / "candidate"
        (candidate / "certificates").mkdir(parents=True)
        claim = track.draft_claim()
        claim["submission_state"] = "ready"
        atomic_write_json(candidate / "claim.json", claim)
        (candidate / "proof.md").write_text("# Fixture\nNot a cryptanalytic proof.\n")
        expected = digest(message_a, "poseidon", 1).hex()
        atomic_write_json(candidate / "certificates" / "manifest.json", {
            "schema_version": 2,
            "certificates": [{
                "id": "witness-1",
                "type": "hash-collision-witness-v2",
                "target_profile": track.profile_id,
                "message_a": "certificates/a.bin",
                "message_b": "certificates/b.bin",
                "expected_digest": expected,
            }],
        })
        (candidate / "certificates" / "a.bin").write_bytes(message_a)
        (candidate / "certificates" / "b.bin").write_bytes(message_b)
        return candidate, track

    def test_a_shifted_encoding_is_refused_as_a_collision(self):
        import tempfile

        from verifier.certificates import verify_certificates
        from verifier.errors import VerificationError
        from verifier import poseidon as module

        canonical = (1).to_bytes(32, "little") + (2).to_bytes(32, "little")
        shifted = (1 + module.MODULUS).to_bytes(32, "little") + (2).to_bytes(32, "little")
        with tempfile.TemporaryDirectory() as directory:
            candidate, track = self.build(directory, canonical, shifted)
            with self.assertRaisesRegex(VerificationError, "message domain"):
                verify_certificates(candidate, track=track)

    def test_a_wrong_length_witness_is_refused(self):
        import tempfile

        from verifier.certificates import verify_certificates
        from verifier.errors import VerificationError

        canonical = (1).to_bytes(32, "little") + (2).to_bytes(32, "little")
        with tempfile.TemporaryDirectory() as directory:
            candidate, track = self.build(directory, canonical, bytes(63))
            with self.assertRaisesRegex(VerificationError, "message domain"):
                verify_certificates(candidate, track=track)

    def test_a_configuration_error_is_not_relabeled_as_a_domain_error(self):
        import tempfile

        from verifier.certificates import verify_certificates
        from verifier.errors import VerificationError

        canonical = (1).to_bytes(32, "little") + (2).to_bytes(32, "little")
        other = (3).to_bytes(32, "little") + (4).to_bytes(32, "little")
        with tempfile.TemporaryDirectory() as directory:
            candidate, track = self.build(directory, canonical, other)
            # An unsupported round count is a harness configuration fault, not a
            # rejected witness, so it must not surface as a domain failure.
            with patch(
                "verifier.certificates.digest",
                side_effect=ValueError("unsupported algorithm or round count"),
            ):
                with self.assertRaises(ValueError) as caught:
                    verify_certificates(candidate, track=track)
            self.assertNotIsInstance(caught.exception, VerificationError)
            self.assertNotIn("message domain", str(caught.exception))

    def test_a_genuine_equal_digest_pair_still_verifies(self):
        import tempfile

        from verifier.certificates import verify_certificates

        # Not a real collision: the same digest is asserted for two distinct
        # canonical messages only to confirm the gate above is not blanket.
        canonical = (1).to_bytes(32, "little") + (2).to_bytes(32, "little")
        other = (3).to_bytes(32, "little") + (4).to_bytes(32, "little")
        with tempfile.TemporaryDirectory() as directory:
            candidate, track = self.build(directory, canonical, other)
            with patch(
                "verifier.certificates.digest",
                return_value=bytes.fromhex(digest(canonical, "poseidon", 1).hex()),
            ):
                report = verify_certificates(candidate, track=track)
            self.assertEqual(report["certificates"][0]["status"], "verified")


class PoseidonReferenceCostTests(unittest.TestCase):
    def test_instrumented_field_operations_back_the_published_prices(self):
        from scripts.reference_operation_costs import poseidon_field_operations

        # Per full round: 3 constant additions, 3 S-boxes of 3 multiplications
        # each, and an MDS row cost of 3 multiplications plus 2 additions.
        self.assertEqual(poseidon_field_operations(1), {"mul": 18, "add": 9})
        self.assertEqual(poseidon_field_operations(2), {"mul": 36, "add": 18})
        # Cross-check at the deployed round count: 240 S-box and 576 MDS
        # multiplications, and 9 additions in each of 64 rounds.
        self.assertEqual(poseidon_field_operations(64), {"mul": 816, "add": 576})

    def test_published_prices_are_the_sum_of_both_field_operations(self):
        from scripts.reference_operation_costs import reference_costs

        prices = reference_costs()
        self.assertEqual(prices["poseidon-r1"], 27)
        self.assertEqual(prices["poseidon-r2"], 54)


class PoseidonNegativeControlTests(unittest.TestCase):
    """A wrong constant, capacity or round count must break the official vectors."""

    def official_hash_passes(self) -> bool:
        return all(
            digest(bytes.fromhex(vector["message"]), "poseidon", 64).hex() == vector["digest"]
            for vector in FIXTURE["hash_vectors"]
        )

    def test_controls_are_measured_against_a_passing_baseline(self):
        self.assertTrue(self.official_hash_passes())

    def test_a_changed_round_constant_breaks_the_vectors(self):
        mutated = list(poseidon.ROUND_CONSTANTS)
        row = list(mutated[0])
        row[0] = (row[0] + 1) % poseidon.MODULUS
        mutated[0] = tuple(row)
        with patch.object(poseidon, "ROUND_CONSTANTS", tuple(mutated)):
            self.assertFalse(self.official_hash_passes())

    def test_a_changed_mds_entry_breaks_the_vectors(self):
        mutated = [list(row) for row in poseidon.MDS]
        mutated[0][0] = (mutated[0][0] + 1) % poseidon.MODULUS
        with patch.object(poseidon, "MDS", tuple(tuple(row) for row in mutated)):
            self.assertFalse(self.official_hash_passes())

    def test_a_wrong_capacity_element_breaks_the_vectors(self):
        for wrong in (0, 1, 1 << 64, 3 << 64, 2 << 65):
            with self.subTest(capacity=hex(wrong)):
                with patch.object(poseidon, "CAPACITY_ELEMENT", wrong):
                    self.assertFalse(self.official_hash_passes())

    def test_a_wrong_round_count_breaks_the_vectors(self):
        for rounds in (1, 2, 32, 63):
            with self.subTest(rounds=rounds):
                self.assertFalse(
                    any(
                        digest(bytes.fromhex(vector["message"]), "poseidon", rounds).hex()
                        == vector["digest"]
                        for vector in FIXTURE["hash_vectors"]
                    )
                )

    def test_swapping_the_partial_round_schedule_breaks_the_vectors(self):
        # Applying the S-box to every element in a partial round is the most
        # likely transcription error; it must not reproduce the vectors.
        with patch.object(poseidon, "PARTIAL_ROUNDS", 0), patch.object(poseidon, "FULL_ROUNDS", 64):
            self.assertFalse(self.official_hash_passes())


if __name__ == "__main__":
    unittest.main()
