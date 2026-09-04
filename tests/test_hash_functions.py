"""Independent reference vectors shared by paired hash targets."""

import hashlib
import unittest

from verifier.hash_functions import digest, FULL_ROUNDS, IV, MASK


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
