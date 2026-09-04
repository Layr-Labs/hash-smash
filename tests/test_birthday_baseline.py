"""Small-n calibration of organizer code, NOT validation of participant programs.

Do not import, interpret, or execute candidate/proof.md. Nor should these tests pin
candidate content: Yukon participants must remain free to replace the baseline.
Synthetic digest functions are test fixtures, not SHA-1 collision certificates.
"""
from __future__ import annotations

import hashlib
import unittest
from fractions import Fraction

from calibration.birthday_wordram import (
    DOMAIN, FIXED_LAYOUT, FIXED_WORDS, MAX_TEST_RECORDS, PROGRAM_TEXT, WORD_MASK,
    assemble, memory_upper_bound, run_small, time_upper_bound,
)


def nonce_of(record):
    return int.from_bytes(record[20:], "big")


class BirthdayBaselineTests(unittest.TestCase):
    def test_message_encoding_and_one_block_padding(self):
        self.assertEqual(len(DOMAIN), 22)
        k0 = int.from_bytes(DOMAIN[:16], "big")
        k1 = int.from_bytes(DOMAIN[16:], "big") << 80
        for nonce in (0, 1, 65535, 65536, (1 << 80) - 1):
            words = (k0, k1 | (nonce >> 16), (nonce & 65535) << 112)
            slot = b"".join(w.to_bytes(16, "big") for w in words)
            message = DOMAIN + nonce.to_bytes(12, "big")
            self.assertEqual(slot[:34], message)
            self.assertEqual(slot[34:], bytes(14))
            padded = message + b"\x80" + bytes(21) + (272).to_bytes(8, "big")
            self.assertEqual(len(padded), 64)

    def test_real_sha1_records_and_no_hit(self):
        for n in (1, 2, 17):
            with self.subTest(n=n):
                result = run_small(n)
                expected = [
                    hashlib.sha1(DOMAIN + i.to_bytes(12, "big"), usedforsecurity=False).digest()
                    + i.to_bytes(12, "big") for i in range(n)
                ]
                self.assertEqual(result.records(), sorted(expected, key=lambda r: r[:20]))
                self.assertEqual(result.hash_calls, n)
                self.assertEqual(result.messages, ())
                self.assertEqual([result.memory[a] for a in (534, 535, 536)], [0, 0, 0])

    def test_each_of_twenty_digest_bytes_is_a_sort_key(self):
        for position in range(20):
            def digest(message):
                i = int.from_bytes(message[22:], "big")
                return bytes(position) + bytes([3 - i]) + bytes(19 - position)

            with self.subTest(position=position):
                result = run_small(4, digest)
                self.assertEqual([nonce_of(r) for r in result.records()], [3, 2, 1, 0])
                self.assertEqual(result.messages, ())

    def test_scatter_is_stable_and_preserves_complete_records(self):
        def digest(message):
            return (int.from_bytes(message[22:], "big") % 3).to_bytes(20, "big")

        result = run_small(19, digest)
        expected = [digest(DOMAIN + i.to_bytes(12, "big")) + i.to_bytes(12, "big")
                    for i in range(19)]
        self.assertEqual(result.records(), sorted(expected, key=lambda r: r[:20]))
        self.assertEqual(sorted(nonce_of(r) for r in result.records()), list(range(19)))
        self.assertEqual(result.hash_calls, 21)
        self.assertEqual(result.messages, (DOMAIN + bytes(12), DOMAIN + (3).to_bytes(12, "big")))

    def test_collision_is_rehashed_and_returned_in_fixed_slots(self):
        result = run_small(7, lambda message: bytes(20))
        self.assertEqual(result.hash_calls, 9)
        self.assertEqual(result.messages, (DOMAIN + bytes(12), DOMAIN + (1).to_bytes(12, "big")))
        self.assertEqual([result.memory[a] for a in (534, 535, 536)], [1, 34, 34])
        self.assertEqual(result.block_steps["verify_build"], 20)
        self.assertEqual(result.block_steps["success"], 4)

    def test_inconsistent_synthetic_rehash_does_not_return_success(self):
        calls = 0

        def inconsistent_digest(message):
            nonlocal calls
            calls += 1
            return bytes(20) if calls <= 2 else calls.to_bytes(20, "big")

        result = run_small(2, inconsistent_digest)
        self.assertEqual(result.hash_calls, 4)
        self.assertEqual(result.messages, ())
        self.assertEqual(result.memory[534], 0)

    def test_sha_suffix_results_are_canonically_zero_extended(self):
        digest = bytes.fromhex("80" + "00"*15 + "ff"*4)
        result = run_small(2, lambda message: digest)
        for register in ("lo", "l0", "l1"):
            self.assertEqual(result.registers[register], (1 << 32)-1)
            self.assertEqual(result.registers[register] >> 32, 0)
        self.assertEqual(result.registers["hi"], 1 << 127)
        self.assertEqual(result.memory[534], 1)
        self.assertEqual(result.hash_calls, 4)

    def test_exact_generation_and_sort_instruction_counts(self):
        for n in (1, 2, 17, 256):
            result = run_small(n)
            counts = result.block_steps
            self.assertEqual(counts["start"], 5)
            self.assertEqual(sum(counts.get(b, 0) for b in ("fill_init", "fill_test", "fill_body")), 18*n+4)
            self.assertEqual(counts["sort_init"] + counts["pass_test"], 45)
            self.assertEqual(counts["pass_setup"], 20*5)
            for prefix, expected in (("zero", 1539), ("hist", 13*n+4),
                                     ("prefix", 2308), ("scatter", 21*n+4)):
                self.assertEqual(sum(counts.get(prefix+suffix, 0) for suffix in ("_init", "_test", "_body")), 20*expected)
            self.assertEqual(counts["pass_end"], 20*4)
            sort_blocks = ("sort_init", "pass_test", "pass_setup", "pass_end",
                           "zero_init", "zero_test", "zero_body", "hist_init", "hist_test", "hist_body",
                           "prefix_init", "prefix_test", "prefix_body", "scatter_init", "scatter_test", "scatter_body")
            self.assertEqual(sum(counts[b] for b in sort_blocks), 680*n+77325)
            self.assertLessEqual(result.steps, time_upper_bound(n))

    def test_worst_case_scan_compares_both_digest_words(self):
        n = 17
        result = run_small(n, lambda m: int.from_bytes(m[22:], "big").to_bytes(20, "big"))
        counts = result.block_steps
        self.assertEqual(counts["scan_body"], 13*(n-1))
        self.assertEqual(sum(counts[b] for b in ("scan_init", "scan_test", "scan_body", "scan_next")), 18*(n-1)+4)
        self.assertEqual(result.steps, 716*n+77324)
        self.assertEqual(time_upper_bound(n) - result.steps, 28)

    def test_buffers_descriptors_and_allocation(self):
        for n in (1, 17):
            result = run_small(n)
            self.assertEqual(result.memory[672], FIXED_WORDS)
            self.assertEqual(result.memory[673], FIXED_WORDS + 2*n)
            self.assertEqual(result.registers["src"], result.memory[672])
            self.assertEqual(result.allocated_words, FIXED_WORDS + 4*n)
            self.assertEqual(result.allocated_words*16, memory_upper_bound(n))
            for address in range(FIXED_WORDS, result.allocated_words):
                self.assertIn(address, result.memory)
            self.assertTrue(all(0 <= address < result.allocated_words for address in result.memory))
            self.assertTrue(all(0 <= word <= WORD_MASK for word in result.memory.values()))

    def test_fixed_memory_layout_includes_padding(self):
        frontier = 0
        for start, end, _ in FIXED_LAYOUT:
            self.assertEqual(start, frontier)
            self.assertGreater(end, start)
            frontier = end
        self.assertEqual(frontier, FIXED_WORDS)
        self.assertEqual(FIXED_WORDS*16, 65536)
        self.assertEqual(80+5+5+4+4+16+14, 128)  # SHA workspace, not additional buffers.

    def test_static_program_and_registers_fit_reservations(self):
        instructions, labels = assemble()
        self.assertEqual(len(instructions), 149)
        self.assertLessEqual(len(instructions)*4, 1024)
        registers = set()
        for _, tokens in instructions:
            self.assertLessEqual(len(tokens), 4)  # opcode and <=3 word operands
            for token in tokens[1:]:
                if token.isdecimal():
                    self.assertLessEqual(int(token), WORD_MASK)
                elif token not in labels and token not in {"N", "K0", "K1", "MASK96"}:
                    registers.add(token)
        self.assertEqual(len(registers), 36)
        self.assertLessEqual(len(registers)+8, 64)  # PC, frontier, opcode/operand latches, flags
        self.assertTrue(PROGRAM_TEXT.endswith("HALT\n"))

    def test_full_size_symbolic_resource_bounds(self):
        n = 1 << 80
        self.assertEqual(time_upper_bound(n), 716*n+77352)
        self.assertLess(time_upper_bound(n), 1 << 91)
        self.assertLess(time_upper_bound(n), 1 << 92)
        self.assertEqual(memory_upper_bound(n), (1 << 86)+(1 << 16))
        self.assertLess(memory_upper_bound(n), 1 << 87)
        self.assertLess(FIXED_WORDS+4*n, 1 << 128)
        self.assertLess(n, 1 << 96)

    def test_success_threshold_uses_exact_finite_n_inequality(self):
        n = 1 << 80
        x = Fraction(n*(n-1), 2*(1 << 160))
        self.assertEqual(x, Fraction(1, 2)-Fraction(1, 1 << 81))
        lower = Fraction(499, 1000)
        self.assertGreater(x, lower)
        cubic = 1+lower+lower**2/2+lower**3/6
        self.assertEqual(cubic, Fraction(9865254499, 6000000000))
        self.assertGreater(cubic, Fraction(100, 61))

    def test_reference_rejects_large_runs_and_bad_digests(self):
        for n in (0, -1, True, 1.5, MAX_TEST_RECORDS+1, 1 << 80):
            with self.assertRaises(ValueError):
                run_small(n)
        for bad_digest in (b"short", "x"*20, bytes(21)):
            with self.assertRaises(ValueError):
                run_small(1, lambda message: bad_digest)


if __name__ == "__main__":
    unittest.main()
