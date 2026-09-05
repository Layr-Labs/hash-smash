from __future__ import annotations

import unittest

from judge.lanes import LANE_STAGES
from judge.schema_validation import ReviewValidationError, validate_review
from judge.tests.helpers import review


class SchemaValidationTests(unittest.TestCase):
    def test_accepts_each_stage_shape(self) -> None:
        for stage in LANE_STAGES:
            with self.subTest(stage=stage):
                self.assertEqual(validate_review(review(stage))["stage"], stage)

    def test_rejects_unknown_property(self) -> None:
        value = review("lane_evaluability")
        value["model_says_correct"] = True
        with self.assertRaisesRegex(ReviewValidationError, "unknown properties"):
            validate_review(value)

    def test_rejects_fatal_obligation_without_linked_finding(self) -> None:
        value = review("lane_cryptanalysis")
        value["obligations"][0]["status"] = "fatal"
        with self.assertRaisesRegex(ReviewValidationError, "linked, cited fatal finding"):
            validate_review(value)

    def test_rejects_inconsistent_normalized_score(self) -> None:
        value = review("lane_cost")
        value["cost_reconstruction"]["normalized_score_log2"] += 1
        with self.assertRaisesRegex(ReviewValidationError, "must equal"):
            validate_review(value)

    def test_rejects_cost_in_other_stage(self) -> None:
        value = review("lane_cryptanalysis")
        value["cost_reconstruction"] = review("lane_cost")["cost_reconstruction"]
        with self.assertRaisesRegex(ReviewValidationError, "only to lane_cost"):
            validate_review(value)

    def test_rejects_injection_flag_without_grounded_finding(self) -> None:
        value = review("lane_evaluability")
        value["prompt_injection_detected"] = True
        with self.assertRaisesRegex(ReviewValidationError, "requires a cited finding"):
            validate_review(value)

    def test_rejects_boolean_and_nonfinite_numbers(self) -> None:
        for number in (True, float("nan"), float("inf")):
            with self.subTest(number=number):
                value = review("lane_cost")
                value["cost_reconstruction"]["time_log2"] = number
                with self.assertRaises(ReviewValidationError):
                    validate_review(value)

    def test_rejects_mismatched_stage(self) -> None:
        with self.assertRaisesRegex(ReviewValidationError, "does not match"):
            validate_review(review("lane_cost"), expected_stage="lane_evaluability")

    def test_rejects_legacy_schema(self) -> None:
        value = review("lane_evaluability")
        value["schema_version"] = "review-v1"
        with self.assertRaises(ReviewValidationError):
            validate_review(value)


if __name__ == "__main__":
    unittest.main()
