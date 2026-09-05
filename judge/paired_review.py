"""A shared review dossier with deterministic exploratory and rigorous decisions.

Provider calls remain behind ReviewClient.review(stage, evidence). Applications
can supply a different model/strategy client per role without changing acceptance
rules. No participant code runs in this module.
"""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from typing import Any, Mapping

from .lanes import CHALLENGE_STAGES, INITIAL_STAGES, LANE_STAGES, POLICY_ID, validate_lane_review
from .provider_adapter import JudgeInfraError, ReviewClient
from .schema_validation import ReviewValidationError

SUCCESS_STATUSES = {"plausible_not_refuted", "ai_rigor_qualified"}


def _hash(value: Any) -> str:
    # Match the repository's canonical_json_bytes, including its final newline.
    text = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False) + "\n"
    return sha256(text.encode("ascii")).hexdigest()


def evidence_binding(evidence: Mapping[str, Any]) -> dict[str, str]:
    intake = evidence["submission"]["intake_report"]
    return {
        "claim_sha256": _hash(intake["claim"]),
        "package_sha256": intake["package_sha256"],
        "target_config_sha256": intake["target_config_sha256"],
        "evidence_sha256": _hash(evidence),
    }


def _gate_evidence(evidence: Mapping[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    try:
        submission = evidence["submission"]
        intake = submission["intake_report"]
        claim = intake["claim"]
        if intake.get("status") != "mechanically_valid":
            return None, "mechanical intake has not passed"
        if intake.get("submission_state") != "ready" or claim.get("submission_state") != "ready":
            return None, "draft submissions cannot reach paired judges"
        for field in ("target_profile", "attack_class", "rounds"):
            if claim[field] != intake["track"][field]:
                return None, f"claim differs from the selected target at {field}"
        certificate = submission["certificate_report"]
        if certificate.get("status") != "passed":
            return None, "certificate verification has not passed"
        for field in ("package_sha256", "target_config_sha256"):
            value = intake[field]
            if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
                return None, f"invalid intake {field}"
            if certificate.get(field) != value:
                return None, f"certificate report {field} is stale"
        if "review_context" in evidence:
            return None, "input evidence cannot supply judge review_context"
        # The pipeline authenticates runner provenance before building this
        # organizer envelope. This check catches stale reports, not forgery of
        # the entire trusted envelope by a malicious caller.
        experiment = submission.get("experiment_report")
        if claim.get("experiment_manifest") and experiment is None:
            return None, "declared experiment is missing its organizer execution report"
        if experiment is not None:
            if claim.get("experiment_manifest") and experiment.get("status") != "passed":
                return None, "declared experiment must have a passed organizer execution report"
            if experiment.get("status") not in {"passed", "not_requested"}:
                return None, "deterministic experiment execution has not passed"
            for field in ("package_sha256", "target_config_sha256"):
                if experiment.get(field) != intake[field]:
                    return None, f"experiment report {field} is stale"
        return dict(claim), None
    except (KeyError, TypeError, AttributeError):
        return None, "trusted evidence envelope is incomplete"


def _decision(status: str, reasons: list[str]) -> dict[str, Any]:
    return {"status": status, "eligible": status in SUCCESS_STATUSES, "reasons": reasons}


def _fatal_findings(reviews: Mapping[str, Mapping[str, Any]]) -> dict[str, dict[str, Any]]:
    findings: dict[str, dict[str, Any]] = {}
    for stage in INITIAL_STAGES:
        for finding in reviews.get(stage, {}).get("findings", []):
            if finding["severity"] == "fatal":
                key = f"{stage}/{finding['id']}"
                findings[key] = {
                    **finding, "finding_id": key, "source_stage": stage,
                    "obligation_refs": [f"{stage}/{item}" for item in finding["obligation_ids"]],
                }
    return findings


def _validate_context(
    review: Mapping[str, Any], binding: Mapping[str, str],
    fatal_findings: Mapping[str, Mapping[str, Any]],
    claim: Mapping[str, Any],
) -> None:
    if review["binding"] != binding:
        raise ReviewValidationError("review binding does not match exact submitted evidence")
    if review["stage"] == "lane_cost":
        obligation_status = {item["id"]: item["status"] for item in review["obligations"]}
        for obligation in _cost_discrepancies(review, claim):
            linked_fatal = any(
                finding["severity"] == "fatal" and obligation in finding["obligation_ids"]
                for finding in review["findings"]
            )
            if obligation_status[obligation] == "supported" and not linked_fatal:
                raise ReviewValidationError(
                    "supported reconstructed cost contradicts submitted bound without a linked fatal finding"
                )
    if review["stage"] in CHALLENGE_STAGES:
        resolutions = review["challenge_resolutions"]
        if {item["finding_id"] for item in resolutions} != set(fatal_findings):
            raise ReviewValidationError("challenge review must resolve exactly all supplied fatal findings")
        for item in resolutions:
            permitted = fatal_findings[item["finding_id"]]["obligation_refs"]
            if not set(item["obligations_discharged"]) <= set(permitted):
                raise ReviewValidationError("adjudicator cannot discharge unrelated obligations")


def _cost_discrepancies(review: Mapping[str, Any], claim: Mapping[str, Any]) -> set[str]:
    cost = review["cost_reconstruction"]
    submitted = claim["claim"]
    discrepancies = set()
    if cost["time_unit"] != submitted["time_unit"]:
        discrepancies.add("time_bound")
    for field, obligation in (
        ("time_log2", "time_bound"), ("memory_log2_bytes", "memory_bound"),
        ("data_log2", "data_preprocessing_advice"), ("preprocessing_log2", "data_preprocessing_advice"),
        ("nonuniform_advice_log2_bytes", "data_preprocessing_advice"),
    ):
        if cost[field] > submitted[field] + 1e-6:
            discrepancies.add(obligation)
    if cost["success_probability"] + 1e-6 < submitted["success_probability"]:
        discrepancies.add("success_budget")
    return discrepancies


def _heuristic_assessments(reviews: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    """Keep critic records intact while reporting adjudicated heuristic states."""
    resolutions = {item["finding_id"]: item for item in reviews.get("lane_adjudicator", {}).get("challenge_resolutions", [])}
    assessments = {}
    for stage in INITIAL_STAGES:
        review = reviews.get(stage, {})
        for heuristic in review.get("heuristics", []):
            ref = f"{stage}/heuristic/{heuristic['id']}"
            linked = [f"{stage}/{finding['id']}" for finding in review.get("findings", [])
                      if finding["severity"] == "fatal" and heuristic["id"] in finding["heuristic_ids"]]
            effective = heuristic["status"]
            if effective == "refuted":
                outcomes = [resolutions.get(key, {}).get("result", "unresolved") for key in linked]
                if "confirmed" in outcomes:
                    effective = "refuted"
                elif outcomes and all(outcome == "refuted" for outcome in outcomes):
                    effective = "pending_reassessment"
                else:
                    effective = "unresolved_refutation"
            assessments[ref] = {
                "review_status": heuristic["status"], "effective_status": effective,
                "linked_fatal_findings": linked,
            }
    return assessments


def aggregate_paired_reviews(
    reviews: Mapping[str, Any], *, binding: Mapping[str, str], claim: Mapping[str, Any],
    infrastructure_failures: Mapping[str, str] | None = None,
) -> dict[str, dict[str, Any]]:
    """Revalidate all records, then apply the two policies without model voting."""
    failures = dict(infrastructure_failures or {})
    validated: dict[str, Any] = {}
    if set(reviews) - set(LANE_STAGES):
        failures["unexpected_stage"] = "unknown review stage"
    for stage in INITIAL_STAGES:
        try:
            validated[stage] = validate_lane_review(reviews[stage], expected_stage=stage)
            _validate_context(validated[stage], binding, {}, claim)
        except (KeyError, TypeError, ValueError):
            failures[stage] = "missing, invalid, or mismatched independent review"
    fatal = _fatal_findings(validated)
    if fatal:
        for stage in CHALLENGE_STAGES:
            try:
                validated[stage] = validate_lane_review(reviews[stage], expected_stage=stage)
                _validate_context(validated[stage], binding, fatal, claim)
            except (KeyError, TypeError, ValueError):
                failures[stage] = "missing, invalid, or mismatched challenge review"
    elif any(stage in reviews for stage in CHALLENGE_STAGES):
        failures["unexpected_challenge"] = "challenge review supplied without a fatal finding"
    if failures:
        reasons = [f"{stage}: {reason}" for stage, reason in sorted(failures.items())]
        return {lane: _decision("infra_failed", reasons) for lane in ("exploratory", "rigorous")}

    declared_heuristics = {item["id"] for item in claim.get("heuristics", [])}
    for stage in ("lane_cryptanalysis", "lane_experiments"):
        recorded = {item["id"] for item in validated[stage]["heuristics"]}
        if not declared_heuristics <= recorded:
            return {lane: _decision("infra_failed", [f"{stage}: declared heuristic omitted from review"])
                    for lane in ("exploratory", "rigorous")}

    resolutions = {item["finding_id"]: item for item in validated.get("lane_adjudicator", {}).get("challenge_resolutions", [])}
    confirmed = [key for key, item in resolutions.items() if item["result"] == "confirmed"]
    if confirmed:
        return {lane: _decision("refuted", confirmed) for lane in ("exploratory", "rigorous")}
    discharged = {ref for item in resolutions.values() for ref in item["obligations_discharged"]}
    evaluability_gaps = [
        f"lane_evaluability/{item['id']}"
        for item in validated["lane_evaluability"]["obligations"]
        if item["status"] != "supported" and f"lane_evaluability/{item['id']}" not in discharged
    ]
    unsupported = [
        f"{stage}/heuristic/{item['id']}"
        for stage in INITIAL_STAGES for item in validated[stage]["heuristics"]
        if item["status"] == "unsupported"
    ]
    if evaluability_gaps or unsupported:
        reasons = evaluability_gaps + unsupported
        return {lane: _decision("not_evaluable", reasons) for lane in ("exploratory", "rigorous")}

    unresolved = []
    heuristic_assessments = _heuristic_assessments(validated)
    all_heuristics = {item["id"] for stage in INITIAL_STAGES for item in validated[stage]["heuristics"]}
    for stage in ("lane_cryptanalysis", "lane_experiments"):
        reviewed_heuristics = {item["id"] for item in validated[stage]["heuristics"]}
        unresolved.extend(f"{stage}/unreviewed-heuristic/{key}" for key in sorted(all_heuristics - reviewed_heuristics))
    for stage in INITIAL_STAGES:
        review = validated[stage]
        for item in review["obligations"]:
            ref = f"{stage}/{item['id']}"
            if item["status"] not in {"supported", "not_applicable"} and ref not in discharged:
                unresolved.append(ref)
        for item in review["heuristics"]:
            ref = f"{stage}/heuristic/{item['id']}"
            effective = heuristic_assessments[ref]["effective_status"]
            if effective != "established":
                unresolved.append(f"{ref}: {effective}")
        for item in review["findings"]:
            ref = f"{stage}/{item['id']}"
            if item["severity"] == "material":
                unresolved.append(ref)
            elif item["severity"] == "fatal" and resolutions[ref]["result"] != "refuted":
                unresolved.append(ref)
    if _cost_discrepancies(validated["lane_cost"], claim):
        unresolved.append("reconstructed resources do not support the submitted bounds")
    return {
        "exploratory": _decision("plausible_not_refuted", sorted(set(unresolved))),
        "rigorous": _decision("not_qualified" if unresolved else "ai_rigor_qualified", sorted(set(unresolved))),
    }


def run_paired_review(
    evidence: Mapping[str, Any], client: ReviewClient,
    *, role_clients: Mapping[str, ReviewClient] | None = None,
) -> dict[str, Any]:
    """Review one immutable package for both lanes, optionally using a role committee.

    Four initial roles receive the same evidence independently. Only a cited fatal
    finding triggers a defender and adjudicator. Failed calls never imply either
    acceptance or a mathematical refutation.
    """
    role_clients = dict(role_clients or {})
    if set(role_clients) - set(LANE_STAGES):
        raise ValueError("role_clients contains an unknown paired review stage")
    claim, gate_error = _gate_evidence(evidence)
    dossier: dict[str, Any] = {
        "schema_version": "judge-paired-dossier-v1", "policy_id": POLICY_ID,
        "claim": claim, "binding": None, "reviews": {}, "provenance": {},
        "infrastructure_failures": {}, "heuristic_assessments": {},
    }
    if gate_error:
        dossier["lanes"] = {lane: _decision("not_evaluable", [gate_error]) for lane in ("exploratory", "rigorous")}
        return dossier
    binding = evidence_binding(evidence)
    dossier["binding"] = binding
    baseline = deepcopy(dict(evidence))

    def call(stage: str, fatal: Mapping[str, Any] | None = None) -> None:
        context: dict[str, Any] = {"policy_id": POLICY_ID, "binding": dict(binding)}
        if fatal:
            context["fatal_findings"] = deepcopy(dict(fatal))
            if stage == "lane_adjudicator":
                context["defender_review"] = deepcopy(dossier["reviews"]["lane_defender"])
        payload = deepcopy(baseline)
        payload["review_context"] = context
        try:
            result = role_clients.get(stage, client).review(stage, payload)
            review = validate_lane_review(result.review, expected_stage=stage)
            _validate_context(review, binding, fatal or {}, claim)
            dossier["reviews"][stage] = deepcopy(review)
            dossier["provenance"][stage] = deepcopy(result.provenance)
        except (JudgeInfraError, ReviewValidationError, TypeError, KeyError) as exc:
            # Never serialize provider exceptions, which could contain request
            # bodies or credentials from an alternate implementation.
            dossier["infrastructure_failures"][stage] = f"{type(exc).__name__}: review did not validate"

    for stage in INITIAL_STAGES:
        call(stage)
    fatal = _fatal_findings(dossier["reviews"])
    if fatal and not dossier["infrastructure_failures"]:
        call("lane_defender", fatal)
        if "lane_defender" in dossier["reviews"]:
            call("lane_adjudicator", fatal)
    dossier["lanes"] = aggregate_paired_reviews(
        dossier["reviews"], binding=binding, claim=claim,
        infrastructure_failures=dossier["infrastructure_failures"],
    )
    dossier["heuristic_assessments"] = _heuristic_assessments(dossier["reviews"])
    return dossier


def select_lane_aggregate(dossier: Mapping[str, Any], lane: str) -> dict[str, Any]:
    """Create the selected lane's score-gate input without accepting a model score."""
    if lane not in {"exploratory", "rigorous"}:
        raise ValueError("unknown judge lane")
    selected = dossier["lanes"][lane]
    binding = dossier["binding"] or {}
    return {
        **selected, "lane": lane, "policy_id": POLICY_ID,
        "claim": dossier["claim"],
        "input_package_sha256": binding.get("package_sha256"),
        "target_config_sha256": binding.get("target_config_sha256"),
        "evidence_sha256": binding.get("evidence_sha256"),
        "claim_sha256": binding.get("claim_sha256"),
    }
