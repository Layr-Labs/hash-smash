from fractions import Fraction
from itertools import combinations, product
from math import prod
import unittest

from calibration.birthday_probability import (
    no_output_collision_probability, rational_success_lower_bound,
)


class ConcreteBirthdayProbabilityTests(unittest.TestCase):
    def test_uniform_outputs_maximize_no_collision_on_small_finite_domains(self):
        # Exhaust all fiber histograms of maps from 6 inputs to 3 outputs.
        for draws in range(1, 4):
            uniform = prod(Fraction(3-i, 3) for i in range(draws))
            self.assertEqual(no_output_collision_probability((2, 2, 2), draws), uniform)
            for a in range(7):
                for b in range(7-a):
                    self.assertLessEqual(no_output_collision_probability((a, b, 6-a-b), draws), uniform)

    def test_nontrivial_collision_bound_against_exhaustive_iid_samples(self):
        draws, domain, outputs = 3, 6, 3
        uniform_no_collision = prod(Fraction(outputs-i, outputs) for i in range(draws))
        union_lower = 1-uniform_no_collision-Fraction(draws*(draws-1), 2*domain)
        pairs = tuple(combinations(range(draws), 2))
        for a in range(7):
            for b in range(7-a):
                mapping = (0,)*a+(1,)*b+(2,)*(6-a-b)
                successes = sum(
                    any(sample[i] != sample[j] and mapping[sample[i]] == mapping[sample[j]]
                        for i, j in pairs)
                    for sample in product(range(domain), repeat=draws)
                )
                probability = Fraction(successes, domain**draws)
                self.assertGreaterEqual(probability, union_lower)
                self.assertGreaterEqual(probability, rational_success_lower_bound(draws, outputs, domain))

    def test_repeated_inputs_are_not_hash_collisions(self):
        # Injective functions can repeat outputs only by repeating the same input.
        self.assertLess(no_output_collision_probability((1, 1, 1), 2), 1)
        self.assertEqual(rational_success_lower_bound(2, 3, 3), 0)

    def test_full_size_bound_without_a_sha1_uniformity_assumption(self):
        draws, outputs, domain = 1 << 80, 1 << 160, 1 << 192
        self.assertGreater(rational_success_lower_bound(draws, outputs, domain), Fraction(39, 100))
        self.assertLess(Fraction(draws*(draws-1), 2*domain), Fraction(1, 1 << 33))
        x = Fraction(499, 1000)
        cubic = 1+x+x*x/2+x*x*x/6
        self.assertLess(1/cubic, Fraction(609, 1000))
        self.assertGreater(Fraction(391, 1000)-Fraction(1, 1 << 33), Fraction(39, 100))

    def test_proposed_message_and_record_sizes_fit_but_do_not_prove_runtime(self):
        # Feasibility checks for a future instruction schedule, not a score.
        self.assertEqual(22+24+1+9+8, 64)
        self.assertEqual(20+24, 44)
        self.assertLess(2*48*(1 << 80)+65536, 1 << 87)

    def test_invalid_sizes_and_boundary_cases(self):
        self.assertEqual(no_output_collision_probability((1, 1), 0), 1)
        self.assertEqual(no_output_collision_probability((1, 1), 3), 0)
        self.assertEqual(rational_success_lower_bound(1, 2, 4), 0)
        for sizes in ((True, 2, 4), (0, 2, 4), (2, -1, 4), (2, 2, 0)):
            with self.assertRaises(ValueError):
                rational_success_lower_bound(*sizes)
        for histogram in ((), (0, 0), (-1, 2), (True, 2)):
            with self.assertRaises(ValueError):
                no_output_collision_probability(histogram, 2)


if __name__ == "__main__":
    unittest.main()
