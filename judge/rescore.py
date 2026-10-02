"""Organizer-pinned reorg judgments: historical reasoning and a new final result."""

from copy import deepcopy
import json
from pathlib import Path

from verifier.costs import UNIT_WEIGHTS, validate_weights
from verifier.errors import VerificationError
from verifier.io import canonical_json_bytes, load_json_bytes, sha256_bytes
from verifier.schema_validation import require_sha256
from .paired_review import evidence_binding, select_lane_aggregate
from .schema_validation import _validate

ROOT = Path(__file__).resolve().parents[1]
ARCHIVES = ROOT / ".yukon/work/rescore-archives"
PLAN = ROOT / "reorg/plan.json"


def digest(value):
    return sha256_bytes(canonical_json_bytes(value))


def review_schema():
    schema = json.loads((ROOT / "schemas/review-rescore-v2.schema.json").read_text())
    paired = json.loads((ROOT / "schemas/review-lanes-v1.schema.json").read_text())
    schema["properties"]["binding"] = paired["properties"]["binding"]
    return schema


def validate_review(review, evidence=None):
    """Validate a new result, never replay historical review rules."""
    _validate(review, review_schema(), "$")
    for key, value in review["binding"].items():
        require_sha256(value, "binding." + key)
    if evidence is not None and review["binding"] != evidence_binding(evidence):
        raise VerificationError("reorg judgment has a mismatched binding")
    if (review["status"] == "complete") != (review["time_log2"] is not None):
        raise VerificationError("accepted reorg judgments require a score; other outcomes require null")
    return review


def scoring_policy(evidence):
    """Public accounting version and effective target prices, independent of judge hashes."""
    model = evidence["benchmark"]["cost_model"]
    return {"id": model["id"], "operation_weights": validate_weights(model.get("operation_weights", dict(UNIT_WEIGHTS)))}


def score_reference(judgments):
    """Use the latest accepted judgment, or the original submitted bound."""
    return next((packet for packet in reversed(judgments)
                 if packet["dossier"]["lanes"][packet["evidence"]["benchmark"]["lane"]]["eligible"]),
                judgments[0])


def recorded_bound(packet):
    dossier = packet["dossier"]
    value = (dossier["rescore"]["review"]["time_log2"] if "rescore" in dossier
             else dossier["claim"]["claim"]["time_log2"])
    _validate(value, {"type": "number", "minimum": 0}, "$.recorded_bound")
    return value


def review_lanes(review, evidence):
    """Only the selected lane receives a current qualification decision."""
    selected = evidence["benchmark"]["lane"]
    accepted = review["status"] == "complete"
    status = (evidence["benchmark"]["qualification_policy"]["pass_status"] if accepted
              else "reorg_rejected" if review["status"] == "rejected" else "rescore_needs_evidence")
    return {
        lane: ({"status": status, "eligible": accepted,
                "reasons": [] if accepted else review["calculation_trace"]}
               if lane == selected else
               {"status": "not_reviewed", "eligible": False,
                "reasons": ["This reorg reviewed only the selected lane; sibling judgments remain in history."]})
        for lane in ("exploratory", "rigorous")
    }


def find_source(track, package_sha256):
    """Only protected organizer configuration can select a previous judgment."""
    if not PLAN.exists():
        return None
    plan = load_json_bytes(PLAN.read_bytes(), str(PLAN))
    if not isinstance(plan, dict) or set(plan) != {"entries"} or not isinstance(plan["entries"], list):
        raise VerificationError("rescore plan must contain entries")
    selected, seen = None, set()
    for entry in plan["entries"]:
        if not isinstance(entry, dict) or set(entry) != {
            "track_id", "package_sha256", "source", "source_config_sha256", "destination_config_sha256",
        }:
            raise VerificationError("invalid rescore plan entry")
        for key in ("package_sha256", "source", "source_config_sha256", "destination_config_sha256"):
            require_sha256(entry[key], "rescore." + key)
        key = (entry["track_id"], entry["package_sha256"])
        if key in seen:
            raise VerificationError("duplicate rescore plan entry")
        seen.add(key)
        if key == (track.id, package_sha256):
            if entry["destination_config_sha256"] != track.config_sha256():
                raise VerificationError("rescore plan does not authorize the current configuration")
            selected = entry
    return selected


def load_archive(source, archive_root=None):
    require_sha256(source, "rescore.source")
    root = ARCHIVES if archive_root is None else archive_root
    path = root / (source + ".json")
    if not path.exists():
        raise VerificationError("missing prior judgment; restore its pinned workflow artifact before rescoring")
    if path.is_symlink() or path.stat().st_size > 4 * 1024 * 1024:
        raise VerificationError("invalid rescore archive file")
    packet = load_json_bytes(path.read_bytes(), str(path))
    if not isinstance(packet, dict) or set(packet) != {"evidence", "dossier"} or digest(packet) != source:
        raise VerificationError("rescore archive checksum mismatch")
    return packet


def _same_submission(current, previous):
    a, b = current["submission"]["intake_report"], previous["submission"]["intake_report"]
    if a["claim"] != b["claim"] or a["package_sha256"] != b["package_sha256"]:
        raise VerificationError("reorg history changed the submission")
    for key in ("track_id", "lane", "target_id", "target_profile"):
        if current["benchmark"][key] != previous["benchmark"][key]:
            raise VerificationError("reorg history changed the target or lane")


def _transition(current, previous, authorization):
    a, b = current["submission"]["intake_report"], previous["submission"]["intake_report"]
    expected = {
        "track_id": current["benchmark"]["track_id"], "package_sha256": a["package_sha256"],
        "source": current["rescore_source"], "source_config_sha256": b["target_config_sha256"],
        "destination_config_sha256": a["target_config_sha256"],
    }
    if authorization != expected:
        raise VerificationError("reorg transition is not authorized for this exact submission")
    _same_submission(current, previous)
    # Prevent an unversioned accounting change from silently preserving a score.
    old_model, new_model = previous["benchmark"]["cost_model"], current["benchmark"]["cost_model"]
    if old_model["id"] == new_model["id"]:
        for field in ("score", "time_unit", "minimum_success_probability", "primitive_operations",
                      "total_time_includes", "probability_space", "memory_scoring", "parallel_computation"):
            if old_model.get(field) != new_model.get(field):
                raise VerificationError("changed accounting rules require a new public cost-model ID")


def _check_integrity(packet):
    evidence, dossier = packet["evidence"], packet["dossier"]
    binding = evidence_binding(evidence)
    if (dossier["binding"] != binding or dossier["claim"] != evidence["submission"]["intake_report"]["claim"]
            or digest(evidence["benchmark"]) != binding["target_config_sha256"]):
        raise VerificationError("archived review does not bind its evidence")
    aggregate = dossier["aggregate"]
    config_hash = digest(dossier["judge_configuration"])
    core = {k: v for k, v in dossier.items() if k not in {"aggregate", "judge_configuration"}}
    core["judge_configuration_sha256"] = config_hash
    if (aggregate.get("judge_config_sha256") != config_hash or aggregate.get("dossier_sha256") != digest(core)
            or aggregate.get("judge_evidence_sha256") != digest(evidence)):
        raise VerificationError("archived dossier/configuration integrity mismatch")
    selected = select_lane_aggregate(dossier, evidence["benchmark"]["lane"])
    if any(aggregate.get(k) != v for k, v in selected.items()):
        raise VerificationError("archived aggregate differs from its dossier")


def verify_packet(packet, archive_root=None):
    """Verify pinned artifacts and submission identity; return oldest first.

    Historical conclusions are evidence, not inputs to today's review validators.
    Ledger-based reorgs are deliberately excluded: start from the original review.
    """
    judgments = []
    while True:
        if len(judgments) >= 32:
            raise VerificationError("rescore history exceeds 32 records")
        _check_integrity(packet)
        judgments.append(packet)
        record = packet["dossier"].get("rescore")
        if record is None:
            if packet["dossier"]["schema_version"] != "judge-paired-dossier-v1" or "rescore_source" in packet["evidence"]:
                raise VerificationError("reorg history must start from an original ordinary judgment")
            return list(reversed(judgments))
        if record["review"].get("schema_version") != "review-rescore-v2":
            raise VerificationError("ledger-based reorg judgments are excluded; pin the original ordinary judgment instead")
        previous = load_archive(packet["evidence"]["rescore_source"], archive_root)
        _same_submission(packet["evidence"], previous["evidence"])
        packet = previous


def history_packets(source, archive_root=None):
    return {digest(packet): packet for packet in verify_packet(load_archive(source, archive_root), archive_root)}


def context(evidence, authorization, archive_root=None):
    previous = load_archive(evidence["rescore_source"], archive_root)
    judgments = verify_packet(previous, archive_root)
    _transition(evidence, previous["evidence"], authorization)
    scored = score_reference(judgments)
    return {
        "binding": evidence_binding(evidence),
        "judgments": [{"benchmark": p["evidence"]["benchmark"], "dossier": p["dossier"]} for p in judgments],
        "experiment_report": judgments[0]["evidence"]["submission"].get("experiment_report"),
        "previous_score": recorded_bound(scored),
        "score_policy_changed": scoring_policy(evidence) != scoring_policy(scored["evidence"]),
    }


def score_result(evidence, dossier, archive_root=None):
    """Validate this run's result before it can emit a score."""
    record = dossier["rescore"]
    supplied = context(evidence, record["authorization"], archive_root)
    review = validate_review(record["review"], evidence)
    if dossier["lanes"] != review_lanes(review, evidence):
        raise VerificationError("reorg decisions differ from the current judgment")
    if review["status"] != "complete":
        raise VerificationError("reorg judgment did not accept the submission; no score is available")
    if not supplied["score_policy_changed"] and review["time_log2"] != supplied["previous_score"]:
        raise VerificationError("unchanged scoring policy must preserve the previous score")
    return {"time_log2": review["time_log2"], "source": evidence["rescore_source"],
            "previous_score": supplied["previous_score"], "score_policy_changed": supplied["score_policy_changed"],
            "declared_cost_model": supplied["judgments"][0]["benchmark"]["cost_model"]}


def run_review(evidence, authorization, client, archive_root=None):
    supplied = context(evidence, authorization, archive_root)
    payload = {**deepcopy(evidence), "review_context": supplied}
    if len(canonical_json_bytes(payload)) > 2 * 1024 * 1024:
        raise VerificationError("reorg judgment history exceeds the 2 MiB evidence budget")
    result = client.review("lane_rescore", payload)
    if isinstance(result.review, dict) and result.review.get("status") == "complete" and not supplied["score_policy_changed"]:
        result.review["time_log2"] = supplied["previous_score"]
    validate_review(result.review, evidence)
    return {
        "schema_version": "judge-rescore-dossier-v1", "policy_id": evidence["benchmark"]["qualification_policy"]["id"],
        "binding": evidence_binding(evidence), "claim": deepcopy(evidence["submission"]["intake_report"]["claim"]),
        "lanes": review_lanes(result.review, evidence), "heuristic_assessments": {},
        "rescore": {"authorization": authorization, "review": result.review, "provenance": result.provenance},
    }
