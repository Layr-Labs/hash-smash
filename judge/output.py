"""Small provider contract; bookkeeping belongs to the harness, not the judge."""

from copy import deepcopy
import json
import re

from .schema_validation import ReviewValidationError, validate_review


def complete_review(value, stage, evidence):
    """Attach request metadata and derived fields, never a substantive judgment."""
    if not isinstance(value, dict):
        raise ReviewValidationError("$: expected object")
    review = deepcopy(value)
    context = evidence.get("review_context", {})
    binding = context.get("binding")
    if binding is None and "submission" in evidence:
        from .paired_review import evidence_binding
        binding = evidence_binding(evidence)
    if binding is not None:
        review["binding"] = dict(binding)
    review["schema_version"] = "review-rescore-v2" if stage == "lane_rescore" else "review-lanes-v1"
    review["stage"] = stage
    if stage == "lane_rescore":
        if review.get("status") == "complete" and context.get("score_policy_changed") is False:
            review["time_log2"] = context["previous_score"]
        return review
    review["prompt_injection_detected"] = any(
        isinstance(finding, dict) and finding.get("category") == "prompt_injection"
        for finding in review.get("findings", [])
    )
    if stage != "lane_cost":
        review.setdefault("cost_reconstruction", None)
    elif isinstance(review.get("cost_reconstruction"), dict):
        cost = review["cost_reconstruction"]
        if "time_log2" in cost:
            cost["normalized_score_log2"] = cost["time_log2"]
    if stage in {"lane_defender", "lane_adjudicator"}:
        for key in ("obligations", "heuristics", "findings"):
            review.setdefault(key, [])
    else:
        review.setdefault("challenge_resolutions", [])
    return review


def validate_response(review, stage, evidence):
    """Include context and coverage checks in the provider's existing retry budget."""
    validate_review(review, expected_stage=stage)
    context = evidence.get("review_context", {})
    if stage == "lane_rescore":
        return
    if "submission" not in evidence:
        return  # Low-level adapter diagnostics need not contain a full submission.
    from .paired_review import _validate_context, evidence_binding
    claim = evidence["submission"]["intake_report"]["claim"]
    binding = context.get("binding") or evidence_binding(evidence)
    _validate_context(review, binding, context.get("fatal_findings", {}), claim)
    if stage in {"lane_cryptanalysis", "lane_experiments"}:
        if not {h["id"] for h in claim.get("heuristics", [])} <= {h["id"] for h in review["heuristics"]}:
            raise ReviewValidationError("$.heuristics: every declared heuristic must be reviewed")


def validation_detail(error):
    """Allow only validator-owned diagnostics, never arbitrary exception bodies."""
    if isinstance(error, json.JSONDecodeError):
        return {"category": "invalid_json", "message": error.msg,
                "line": error.lineno, "column": error.colno, "position": error.pos}
    if isinstance(error, ReviewValidationError):
        message = str(error)
        # Unknown property names are response content and might contain secrets.
        message = re.sub(r"unknown properties:.*", "unknown properties", message)
        return {"category": "invalid_review", "message": message[:400]}
    # These strings originate in our response-envelope parser, not the provider.
    known = {
        "response did not complete": "incomplete_response",
        "response reports an error or incomplete output": "incomplete_response",
        "completion did not finish with end_turn": "incomplete_response",
        "completion did not finish with stop": "incomplete_response",
        "unexpected tool, role, or incomplete message": "unexpected_output",
        "refused or non-text response": "refusal_or_nontext",
        "duplicate JSON property": "ambiguous_json",
        "non-finite JSON constant": "invalid_number",
        "expected exactly one JSON review": "unexpected_output",
        "response model does not match Sol": "unexpected_model",
    }
    if type(error) is ValueError and str(error) in known:
        return {"category": known[str(error)], "message": str(error)}
    if isinstance(error, KeyError):
        return {"category": "missing_response_field", "message": "Required response-envelope field is missing"}
    return {"category": "invalid_response", "message": "Response could not be read as a complete review"}


def retry_body(original, diagnostic):
    """Regenerate with trusted validator feedback; never request a different verdict."""
    body = json.loads(original)
    feedback = ("\n\nThe previous response could not be processed. Correct this output-contract "
                "error and return a complete review: " + json.dumps(diagnostic, ensure_ascii=True) +
                ". Preserve your substantive conclusions; a valid rejection is an acceptable result.")
    if "instructions" in body:
        body["instructions"] += feedback
    elif "system" in body:
        body["system"][0]["text"] += feedback
    else:
        body["messages"][0]["content"] += feedback
    return json.dumps(body, ensure_ascii=True, separators=(",", ":")).encode()
