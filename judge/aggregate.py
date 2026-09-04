"""Trusted, deterministic aggregation of independent AI review records."""

from __future__ import annotations

from typing import Any, Mapping

from .schema_validation import ReviewValidationError, validate_review


REQUIRED_STAGES = ("triage", "correctness", "complexity")
OUTCOMES = {
    "ai_qualified",
    "clarification_required",
    "technical_blocker",
    "judge_infra_failed",
}


def _claim_key(review: Mapping[str, Any]) -> tuple[Any, ...]:
    claim = review["claim"]
    return (
        claim["target_profile"],
        claim["attack_class"],
        claim["rounds"],
    )


def aggregate_reviews(
    reviews: Mapping[str, Mapping[str, Any]],
    *,
    infrastructure_failures: Mapping[str, str] | None = None,
    expected_claim: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Map three independent reviews to one non-human review status.

    Invalid or absent model records are infrastructure failures, never proof
    rejections. Fatal, cited technical issues take precedence over clarification.
    Confidence is intentionally ignored.
    """

    failures = dict(infrastructure_failures or {})
    validated: dict[str, Mapping[str, Any]] = {}
    for stage in REQUIRED_STAGES:
        record = reviews.get(stage)
        if record is None:
            failures.setdefault(stage, "missing required review")
            continue
        try:
            validated[stage] = validate_review(dict(record), expected_stage=stage)
        except (ReviewValidationError, TypeError, ValueError) as exc:
            failures.setdefault(stage, f"invalid review record: {exc}")

    if failures:
        return {
            "status": "judge_infra_failed",
            "reasons": [f"{stage}: {reason}" for stage, reason in sorted(failures.items())],
            "claim": None,
            "recomputed_cost": None,
        }

    fatal_reasons: list[str] = []
    clarification_reasons: list[str] = []
    for stage in REQUIRED_STAGES:
        review = validated[stage]
        # unconditional-v1 reserves this array for unproved premises beyond the
        # common problem definition. A model cannot waive one with a positive vote.
        for assumption in review["assumptions"]:
            evidence = ", ".join(assumption["evidence"]) or "no evidence location supplied"
            clarification_reasons.append(
                f"{stage}: unproved assumption: {assumption['description']} ({evidence})"
            )
        for issue in review["issues"]:
            rendered = f"{stage}: {issue['description']}"
            if issue["severity"] == "fatal":
                fatal_reasons.append(rendered)
            elif issue["severity"] == "material":
                clarification_reasons.append(rendered)
            elif issue["category"] == "unproved_assumption":
                # Fail closed if the reviewer mislabels an explicit dependency minor.
                clarification_reasons.append(rendered)

    triage = validated["triage"]
    correctness = validated["correctness"]
    complexity = validated["complexity"]
    if triage["decision"] == "out_of_scope":
        fatal_reasons.append("triage: submission is outside the configured track")
    elif triage["decision"] == "clarification_needed":
        clarification_reasons.append("triage: author clarification is required")

    for stage, review in (("correctness", correctness), ("complexity", complexity)):
        if review["verdict"] == "unsupported":
            fatal_reasons.append(f"{stage}: specialist verdict is unsupported")
        elif review["verdict"] == "unclear":
            clarification_reasons.append(f"{stage}: specialist verdict is unclear")

    claim_keys = {_claim_key(review) for review in validated.values()}
    if len(claim_keys) != 1:
        clarification_reasons.append("specialists reconstructed different target claims")
    if expected_claim is not None:
        expected_key = (
            expected_claim.get("target_profile"),
            expected_claim.get("attack_class"),
            expected_claim.get("rounds"),
        )
        if any(key != expected_key for key in claim_keys):
            clarification_reasons.append(
                "a specialist reconstructed a target claim different from deterministic intake"
            )
        expected_cost = expected_claim.get("claim")
        if isinstance(expected_cost, Mapping):
            for field, value in expected_cost.items():
                if complexity["submitted_cost"].get(field) != value:
                    clarification_reasons.append(
                        f"complexity: submitted cost differs from deterministic intake at {field}"
                    )

    if fatal_reasons:
        status = "technical_blocker"
        reasons = list(dict.fromkeys(fatal_reasons + clarification_reasons))
    elif clarification_reasons:
        status = "clarification_required"
        reasons = list(dict.fromkeys(clarification_reasons))
    else:
        status = "ai_qualified"
        reasons = [
            "triage passed and both independent specialists support the same exact claim"
        ]

    output_claim = dict(complexity["claim"])
    if expected_claim is not None:
        # Track fields and declared restrictions are data, not model judgments. Hidden or
        # inferred restrictions belong in issues/assumptions instead of rewritten claim text.
        for field in ("target_profile", "attack_class", "rounds", "restrictions"):
            output_claim[field] = expected_claim[field]

    return {
        "status": status,
        "reasons": reasons,
        "claim": output_claim,
        "recomputed_cost": complexity["recomputed_cost"],
    }
