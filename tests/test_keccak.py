import hashlib
import unittest
from unittest.mock import patch

from verifier import keccak


def serialized_lanes(words: str, width: int) -> bytes:
    return b"".join(int(word, 16).to_bytes(width // 200, "little") for word in words.split())


# Published XKCP intermediate values, all-zero input, After iota at rounds
# 4/5 and final state. These pin PREFIX rounds, little-endian lane encoding,
# and the 800-bit permutation independently of the implementation.
# https://github.com/XKCP/XKCP/blob/master/tests/TestVectors/KeccakF-1600-IntermediateValues.txt
# https://github.com/XKCP/XKCP/blob/master/tests/TestVectors/KeccakF-800-IntermediateValues.txt
PREFIX_VECTORS = {
    (1600, 5): """
        6A00840802752A6F F9A9C3AB00C9C931 6DB98725571F1604 96BA275BA7474A93 9B5E7A3FEEB7E41E
        73FE33C9B1038C36 70E8B5D763274728 0FE03A842F22AFCB D95C0A4EC94AD619 E57A1A2BB2AE09C2
        2728E4F2B7AEEBE8 A81EDBEB54D20FE1 7AC22599684B0182 C17E6A6AB6526EB1 A1C3CEE067AB9F52
        B8E36F84D019B15F 1CF47F1F04738AD9 F377844620F2D499 105A64A116516B0E 965393CA1B42F1DB
        1C2C849D3FD29C1F AB89B3623F5F6964 916D0713D86ACC2A E5DC85FFAD78D9B0 650759748DF5EFE9
    """,
    (1600, 6): """
        43E30B96FF110A58 D642C7DF22B4173C BFD660DFE2E0051D A303B734F55677E6 37C05E405B01AF0C
        0B5033314F45C5CB 44F0FBF5606F647A 34FE5A6214181ED1 B42ABC5DE738DDD5 7A8E099FE258E5D8
        2D6CBEB27C4BC219 A58159B967A3AD93 A4036D7EAF457157 5F252E8E367F3DC8 5E8F6AD5D330526E
        4FCB128386812F6E 02C154103BD90DD0 375463E874AF271C 1CEE752EDB4B48F6 36E67B423707DCB0
        F36BA8B04378F57A CFCD9CECD3ADE3D5 7FC73C7B61494B4C B913D9D348A8E89A 1EDCA3008E4023A2
    """,
    (800, 5): """
        DE48707C E87E4AF4 2FBD59B9 775CAA7A 29B403CE
        1D68FD9B 18054C7C 4288E4F1 8B019A63 CCEB005E
        A03E64A8 B3CF6817 0288881D 85AD14BC 81283114
        5368C71A 6F3923CC 1F7F0619 F177369F 9BE4A20E
        2694298B 7EDE413E 1F987547 0AB21840 C11D23F4
    """,
    (800, 6): """
        44E4F979 7D630907 8C04B31C 897C2642 31979FBE
        5661F0E9 7C86B52C D8825173 E34104ED E0B22CBB
        D3514650 2CFF1251 9F37E6AA 55E6C83C 2490EAF7
        47B83436 7C45E3F9 D7972CF6 4F62ACA3 871DB6F0
        7AF3584A CA0DB7DD 36B86B5F 84996D92 DA2F88CF
    """,
    (800, 22): """
        E531D45D F404C6FB 23A0BF99 F1F8452F 51FFD042
        E539F578 F00B80A7 AF973664 BF5AF34C 227A2424
        88172715 9F685884 B15CD054 1BF4FC0E 6166FA91
        1A9E599A A3970A1F AB659687 AFAB8D68 E74B1015
        34001A98 4119EFF3 930A0E76 87B28070 11EFE996
    """,
}


class KeccakTests(unittest.TestCase):
    def test_permutations_match_xkcp_prefix_and_full_vectors(self):
        for (width, rounds), words in PREFIX_VECTORS.items():
            with self.subTest(width=width, rounds=rounds):
                self.assertEqual(
                    keccak.permutation(bytes(width // 8), width_bits=width, rounds=rounds),
                    serialized_lanes(words, width))

    def test_full_sha3_matches_hashlib_at_rate_and_padding_boundaries(self):
        for length in (0, 1, 3, 67, 68, 69, 134, 135, 136, 137, 270, 271, 272, 273, 1000):
            with self.subTest(length=length):
                message = bytes(i % 251 for i in range(length))
                self.assertEqual(keccak.sha3_256(message), hashlib.sha3_256(message).digest())

    def test_padding_and_reduction_apply_to_each_absorbed_block(self):
        # Observe inputs at the permutation boundary: this guards the distinct
        # rate/domain definitions and the easily confused last-byte padding.
        for function, width, rate, suffix in (
            (keccak.sha3_256, 1600, 136, 0x06),
            (keccak.keccak800, 800, 68, 0x01),
        ):
            for length in (0, rate - 1, rate, rate + 1, 2 * rate):
                with self.subTest(width=width, length=length):
                    observed = []

                    def capture(lanes, lane_bits, rounds):
                        observed.append((b"".join(x.to_bytes(lane_bits // 8, "little")
                                                  for x in lanes), lane_bits, rounds))
                        # Return a zero state so every absorbed block is visible.
                        lanes[:] = [0] * 25

                    with patch.object(keccak, "_permute_lanes", side_effect=capture):
                        self.assertEqual(function(bytes(length), rounds=5), bytes(32))
                    self.assertEqual(len(observed), length // rate + 1)
                    self.assertTrue(all(bits == width // 25 and rounds == 5
                                        for _, bits, rounds in observed))
                    final = bytearray(width // 8)
                    final[length % rate] = suffix
                    final[rate - 1] |= 0x80
                    self.assertEqual(observed[-1][0], bytes(final))
                    self.assertTrue(all(state == bytes(width // 8) for state, _, _ in observed[:-1]))

    def test_invalid_width_rounds_and_input_fail_closed(self):
        for function, full in ((keccak.sha3_256, 24), (keccak.keccak800, 22)):
            for rounds in (0, -1, full + 1, True, 1.0, "5", None):
                with self.subTest(function=function.__name__, rounds=rounds):
                    with self.assertRaises(ValueError):
                        function(b"abc", rounds)
            for data in ("abc", bytearray(b"abc"), None):
                with self.assertRaises(ValueError):
                    function(data)
        for width in (200, 400, True, 800.0, "800"):
            with self.assertRaises(ValueError):
                keccak.permutation(bytes(100), width_bits=width, rounds=5)
        for state in (bytes(99), bytes(101), bytearray(100), "00"):
            with self.assertRaises(ValueError):
                keccak.permutation(state, width_bits=800, rounds=5)


if __name__ == "__main__":
    unittest.main()
