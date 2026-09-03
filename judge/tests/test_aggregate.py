from __future__ import annotations

import unittest

from judge.aggregate import aggregate_reviews
from judge.tests.helpers import review


def complete_reviews():
    return {stage: review(stage) for stage in ("triage", "correctness", "complexity")}


class AggregateTests(unittest.TestCase):
    def test_qualified_when_all_required_reviews_support_exact_claim(self) -> None:
        result = aggregate_reviews(complete_reviews())
        self.assertEqual(result["status"], "ai_qualified")
        self.assertEqual(result["recomputed_cost"]["normalized_score_log2"], 103.0)

    def test_material_issue_requires_clarification(self) -> None:
        reviews = complete_reviews()
        reviews["correctness"]["verdict"] = "unclear"
        reviews["correctness"]["issues"] = [
            {
                "severity": "material",
                "category": "missing_argument",
                "description": "A probability premise is not justified.",
                "evidence": ["proof.md:L30-L35"],
            }
        ]
        result = aggregate_reviews(reviews)
        self.assertEqual(result["status"], "clarification_required")

    def test_fatal_issue_is_technical_blocker(self) -> None:
        reviews = complete_reviews()
        reviews["correctness"]["verdict"] = "unsupported"
        reviews["correctness"]["issues"] = [
            {
                "severity": "fatal",
                "category": "collision_relation",
                "description": "The outputs are only a near-collision.",
                "evidence": ["proof.md:L41-L47"],
            }
        ]
        result = aggregate_reviews(reviews)
        self.assertEqual(result["status"], "technical_blocker")

    def test_missing_or_invalid_review_is_infrastructure_failure(self) -> None:
        reviews = complete_reviews()
        del reviews["complexity"]
        result = aggregate_reviews(reviews)
        self.assertEqual(result["status"], "judge_infra_failed")

    def test_reconstructed_claim_disagreement_requires_clarification(self) -> None:
        reviews = complete_reviews()
        reviews["correctness"]["claim"]["rounds"] = 79
        result = aggregate_reviews(reviews)
        self.assertEqual(result["status"], "clarification_required")

    def test_declared_restrictions_come_from_deterministic_intake(self) -> None:
        reviews = complete_reviews()
        reviews["triage"]["claim"]["restrictions"] = ["triage paraphrase"]
        reviews["correctness"]["claim"]["restrictions"] = ["correctness paraphrase"]
        reviews["complexity"]["claim"]["restrictions"] = ["complexity paraphrase"]
        expected = {
            "target_profile": "sha1-fips180-4-v1",
            "attack_class": "ordinary-collision",
            "rounds": 80,
            "restrictions": ["exact submitted restriction"],
        }
        result = aggregate_reviews(reviews, expected_claim=expected)
        self.assertEqual(result["status"], "ai_qualified")
        self.assertEqual(result["claim"]["restrictions"], ["exact submitted restriction"])

    def test_confidence_does_not_affect_outcome(self) -> None:
        reviews = complete_reviews()
        for value in reviews.values():
            value["confidence"] = 0.0
        result = aggregate_reviews(reviews)
        self.assertEqual(result["status"], "ai_qualified")


if __name__ == "__main__":
    unittest.main()
