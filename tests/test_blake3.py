"""Official full-round vectors and prefix vectors from the independent Rust reference."""

import json
from pathlib import Path
import unittest
from unittest.mock import patch

from verifier import blake3
from verifier.hash_functions import digest


class Blake3Tests(unittest.TestCase):
    def test_official_and_independent_prefix_vectors(self):
        vectors = json.loads((Path(__file__).parent / "fixtures/blake3-vectors.json").read_text())
        for item in vectors:
            with self.subTest(rounds=item["rounds"], length=item["length"]):
                data = bytes(i % 251 for i in range(item["length"]))
                self.assertEqual(digest(data, "blake3", item["rounds"]).hex(), item["digest"])

    def test_every_chunk_parent_and_root_compression_is_reduced(self):
        for rounds in (1, 2):
            with patch.object(blake3, "_compress", wraps=blake3._compress) as compress:
                blake3.blake3(bytes(3073), rounds)
            self.assertTrue(all(call.args[-1] == rounds for call in compress.call_args_list))
            flags = [call.args[-2] for call in compress.call_args_list]
            self.assertIn(blake3.PARENT, flags)
            self.assertEqual(flags[-1], blake3.PARENT | blake3.ROOT)

    def test_single_block_hash_is_one_root_compression(self):
        for length in (0, 1, 63, 64):
            with patch.object(blake3, "_compress", wraps=blake3._compress) as compress:
                blake3.blake3(bytes(length), 1)
            compress.assert_called_once()
            self.assertEqual(compress.call_args.args[2:], (0, length, 11, 1))

    def test_invalid_input_and_rounds_fail_closed(self):
        for rounds in (0, -1, 8, True, 1.0, "1", None):
            with self.assertRaises(ValueError):
                blake3.blake3(b"abc", rounds)
        for data in ("abc", bytearray(b"abc"), None):
            with self.assertRaises(ValueError):
                blake3.blake3(data)


if __name__ == "__main__":
    unittest.main()
