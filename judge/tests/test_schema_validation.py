from __future__ import annotations

import unittest

from judge.schema_validation import ReviewValidationError, validate_review
from judge.tests.helpers import review


class SchemaValidationTests(unittest.TestCase):
    def test_accepts_each_stage_shape(self) -> None:
        for stage in ("triage", "correctness", "complexity", "adversarial", "synthesis"):
            with self.subTest(stage=stage):
                self.assertEqual(validate_review(review(stage))["stage"], stage)

    def test_rejects_unknown_property(self) -> None:
        value = review("triage")
        value["model_says_correct"] = True
        with self.assertRaisesRegex(ReviewValidationError, "unknown properties"):
            validate_review(value)

    def test_rejects_positive_verdict_with_fatal_issue(self) -> None:
        value = review("correctness")
        value["issues"] = [
            {
                "severity": "fatal",
                "category": "correctness",
                "description": "A central transition is invalid.",
                "evidence": ["proof.md:L20"],
            }
        ]
        with self.assertRaisesRegex(ReviewValidationError, "positive verdict contradicts"):
            validate_review(value)

    def test_rejects_unsupported_without_fatal_issue(self) -> None:
        value = review("correctness")
        value["verdict"] = "unsupported"
        with self.assertRaisesRegex(ReviewValidationError, "requires a cited fatal issue"):
            validate_review(value)

    def test_rejects_inconsistent_normalized_score(self) -> None:
        value = review("complexity")
        value["recomputed_cost"]["normalized_score_log2"] = 104.0
        value["verdict"] = "unclear"
        value["questions_for_author"] = ["Please reconcile the score."]
        with self.assertRaisesRegex(ReviewValidationError, "must equal"):
            validate_review(value)

    def test_rejects_supported_cost_disagreement(self) -> None:
        value = review("complexity")
        value["recomputed_cost"]["time_log2"] = 70.0
        value["recomputed_cost"]["normalized_score_log2"] = 104.0
        with self.assertRaisesRegex(ReviewValidationError, "cost discrepancy"):
            validate_review(value)

    def test_accepts_supported_conservative_resource_bounds(self) -> None:
        value = review("complexity")
        value["recomputed_cost"]["time_log2"] = 68.0
        value["recomputed_cost"]["success_probability"] = 0.6
        value["recomputed_cost"]["normalized_score_log2"] = 102.0
        self.assertEqual(validate_review(value)["verdict"], "supported")

    def test_rejects_injection_flag_without_grounded_issue(self) -> None:
        value = review("triage")
        value["prompt_injection_detected"] = True
        with self.assertRaisesRegex(ReviewValidationError, "prompt_injection issue"):
            validate_review(value)

    def test_rejects_boolean_as_number(self) -> None:
        value = review("complexity")
        value["confidence"] = True
        with self.assertRaisesRegex(ReviewValidationError, "expected number"):
            validate_review(value)


if __name__ == "__main__":
    unittest.main()
