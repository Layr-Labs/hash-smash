"""Configuration and deterministic aggregation for independent judge panels."""

from __future__ import annotations

import json
import math
import re
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Callable, Mapping

from .prompts import STRATEGY_FILES
from .provider_adapter import OpenRouterClient, REASONING_EFFORTS
from .run_review import run_mvp
from .schema_validation import ReviewValidationError, validate_review


DEFAULT_COMMITTEE_PATH = Path(__file__).resolve().with_name("committees") / "committee-v1.json"
DEFAULT_BEDROCK_COMMITTEE_PATH = (
    Path(__file__).resolve().with_name("committees") / "committee-bedrock-v1.json"
)
MEMBER_ID_RE = re.compile(r"[a-z0-9][a-z0-9-]{0,63}\Z")


@dataclass(frozen=True)
class CommitteeMember:
    id: str
    model: str
    strategy: str
    reasoning_effort: str | None
    temperature: float | None
    max_tokens: int
    timeout_seconds: float
    max_attempts: int


@dataclass(frozen=True)
class CommitteePolicy:
    minimum_completed_members: int
    minimum_qualified_members: int
    technical_blocker_veto: bool
    clarification_veto: bool


@dataclass(frozen=True)
class CommitteeConfig:
    schema_version: str
    committee_id: str
    members: tuple[CommitteeMember, ...]
    policy: CommitteePolicy


def _exact_keys(value: Mapping[str, Any], required: set[str], path: str) -> None:
    missing = required - set(value)
    extra = set(value) - required
    if missing:
        raise ValueError(f"{path}: missing fields: {', '.join(sorted(missing))}")
    if extra:
        raise ValueError(f"{path}: unknown fields: {', '.join(sorted(extra))}")


def load_committee(path: Path | str = DEFAULT_COMMITTEE_PATH) -> CommitteeConfig:
    with Path(path).open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("committee: root must be an object")
    _exact_keys(value, {"schema_version", "committee_id", "members", "policy"}, "committee")
    if value["schema_version"] != "committee-v1":
        raise ValueError("committee.schema_version must equal 'committee-v1'")
    committee_id = value["committee_id"]
    if not isinstance(committee_id, str) or not MEMBER_ID_RE.fullmatch(committee_id):
        raise ValueError("committee.committee_id is invalid")

    raw_members = value["members"]
    if not isinstance(raw_members, list) or not 1 <= len(raw_members) <= 8:
        raise ValueError("committee.members must contain between 1 and 8 members")
    members: list[CommitteeMember] = []
    seen: set[str] = set()
    for index, raw in enumerate(raw_members):
        path_text = f"committee.members[{index}]"
        if not isinstance(raw, dict):
            raise ValueError(f"{path_text} must be an object")
        _exact_keys(
            raw,
            {
                "id",
                "model",
                "strategy",
                "reasoning_effort",
                "temperature",
                "max_tokens",
                "timeout_seconds",
                "max_attempts",
            },
            path_text,
        )
        member_id = raw["id"]
        if not isinstance(member_id, str) or not MEMBER_ID_RE.fullmatch(member_id):
            raise ValueError(f"{path_text}.id is invalid")
        if member_id in seen:
            raise ValueError(f"{path_text}.id must be unique")
        seen.add(member_id)
        model = raw["model"]
        if not isinstance(model, str) or not model or len(model) > 256:
            raise ValueError(f"{path_text}.model is invalid")
        strategy = raw["strategy"]
        if strategy not in STRATEGY_FILES:
            raise ValueError(f"{path_text}.strategy is unknown")
        effort = raw["reasoning_effort"]
        if effort is not None and effort not in REASONING_EFFORTS:
            raise ValueError(f"{path_text}.reasoning_effort is invalid")
        temperature = raw["temperature"]
        if temperature is not None:
            if (
                isinstance(temperature, bool)
                or not isinstance(temperature, (int, float))
                or not math.isfinite(float(temperature))
                or not 0 <= float(temperature) <= 2
            ):
                raise ValueError(f"{path_text}.temperature must be null or between 0 and 2")
            temperature = float(temperature)
        max_tokens = raw["max_tokens"]
        if isinstance(max_tokens, bool) or not isinstance(max_tokens, int) or not 1024 <= max_tokens <= 131072:
            raise ValueError(f"{path_text}.max_tokens must be between 1024 and 131072")
        timeout_seconds = raw["timeout_seconds"]
        if (
            isinstance(timeout_seconds, bool)
            or not isinstance(timeout_seconds, (int, float))
            or not math.isfinite(float(timeout_seconds))
            or not 10 <= float(timeout_seconds) <= 600
        ):
            raise ValueError(f"{path_text}.timeout_seconds must be between 10 and 600")
        max_attempts = raw["max_attempts"]
        if isinstance(max_attempts, bool) or not isinstance(max_attempts, int) or not 1 <= max_attempts <= 5:
            raise ValueError(f"{path_text}.max_attempts must be between 1 and 5")
        members.append(
            CommitteeMember(
                member_id,
                model,
                strategy,
                effort,
                temperature,
                max_tokens,
                float(timeout_seconds),
                max_attempts,
            )
        )

    raw_policy = value["policy"]
    if not isinstance(raw_policy, dict):
        raise ValueError("committee.policy must be an object")
    _exact_keys(
        raw_policy,
        {
            "minimum_completed_members",
            "minimum_qualified_members",
            "technical_blocker_veto",
            "clarification_veto",
        },
        "committee.policy",
    )
    for field in ("minimum_completed_members", "minimum_qualified_members"):
        number = raw_policy[field]
        if isinstance(number, bool) or not isinstance(number, int) or not 1 <= number <= len(members):
            raise ValueError(f"committee.policy.{field} must be between 1 and member count")
    for field in ("technical_blocker_veto", "clarification_veto"):
        if not isinstance(raw_policy[field], bool):
            raise ValueError(f"committee.policy.{field} must be boolean")
    if raw_policy["minimum_qualified_members"] > raw_policy["minimum_completed_members"]:
        raise ValueError("minimum_qualified_members cannot exceed minimum_completed_members")

    return CommitteeConfig(
        schema_version=value["schema_version"],
        committee_id=committee_id,
        members=tuple(members),
        policy=CommitteePolicy(**raw_policy),
    )


def member_client_config(base: Any, member: CommitteeMember) -> Any:
    return replace(
        base,
        model=member.model,
        strategy=member.strategy,
        reasoning_effort=member.reasoning_effort,
        temperature=member.temperature,
        max_tokens=member.max_tokens,
        timeout_seconds=member.timeout_seconds,
        max_attempts=member.max_attempts,
        app_title=f"HashSmash AI Judge / {member.id}",
    )


def _claim_key(aggregate: Mapping[str, Any]) -> tuple[Any, ...] | None:
    claim = aggregate.get("claim")
    if not isinstance(claim, Mapping):
        return None
    restrictions = claim.get("restrictions")
    if not isinstance(restrictions, list):
        return None
    return (
        claim.get("target_profile"),
        claim.get("attack_class"),
        claim.get("rounds"),
        tuple(restrictions),
    )


def aggregate_committee(
    member_dossiers: Mapping[str, Mapping[str, Any]],
    config: CommitteeConfig,
) -> dict[str, Any]:
    expected_ids = {member.id for member in config.members}
    if set(member_dossiers) != expected_ids:
        return {
            "status": "judge_infra_failed",
            "reasons": ["committee dossier does not contain exactly the configured members"],
            "claim": None,
            "recomputed_cost": None,
            "member_statuses": {},
        }

    statuses: dict[str, str] = {}
    aggregates: dict[str, Mapping[str, Any]] = {}
    assumption_vetoes: list[str] = []
    for member in config.members:
        dossier = member_dossiers[member.id]
        # Qualification policy is not a configurable voting preference. Check even
        # partial panels: a transport failure in one stage cannot erase another
        # stage's valid finding of an unproved premise.
        reviews = dossier.get("reviews", {})
        if isinstance(reviews, Mapping):
            for stage in ("triage", "correctness", "complexity"):
                record = reviews.get(stage)
                if not isinstance(record, Mapping):
                    continue
                try:
                    reviewed = validate_review(dict(record), expected_stage=stage)
                except (ReviewValidationError, TypeError, ValueError):
                    continue
                if reviewed["assumptions"] or any(
                    issue["category"] == "unproved_assumption" for issue in reviewed["issues"]
                ):
                    assumption_vetoes.append(f"{member.id}/{stage}")
        aggregate = dossier.get("aggregate")
        if not isinstance(aggregate, Mapping):
            statuses[member.id] = "judge_infra_failed"
            continue
        status = aggregate.get("status")
        if status not in {
            "ai_qualified",
            "clarification_required",
            "technical_blocker",
            "judge_infra_failed",
        }:
            statuses[member.id] = "judge_infra_failed"
            continue
        statuses[member.id] = status
        aggregates[member.id] = aggregate

    completed = sum(status != "judge_infra_failed" for status in statuses.values())
    qualified = sum(status == "ai_qualified" for status in statuses.values())
    blockers = [member_id for member_id, status in statuses.items() if status == "technical_blocker"]
    clarifications = [
        member_id for member_id, status in statuses.items() if status == "clarification_required"
    ]
    failures = [member_id for member_id, status in statuses.items() if status == "judge_infra_failed"]

    usable_claims = {
        member_id: _claim_key(aggregate)
        for member_id, aggregate in aggregates.items()
        if statuses[member_id] != "judge_infra_failed"
    }
    nonnull_claims = {claim for claim in usable_claims.values() if claim is not None}
    claim_disagreement = len(nonnull_claims) > 1 or any(
        claim is None for claim in usable_claims.values()
    )

    if completed < config.policy.minimum_completed_members:
        status = "judge_infra_failed"
        reasons = [
            f"only {completed} committee members completed; "
            f"{config.policy.minimum_completed_members} required"
        ]
        if failures:
            reasons.append(f"infrastructure failures: {', '.join(failures)}")
    elif blockers and config.policy.technical_blocker_veto:
        status = "technical_blocker"
        reasons = [f"technical-blocker veto from: {', '.join(blockers)}"]
    elif assumption_vetoes:
        status = "clarification_required"
        reasons = [f"unconditional-v1 unproved-assumption veto from: {', '.join(assumption_vetoes)}"]
    elif clarifications and config.policy.clarification_veto:
        status = "clarification_required"
        reasons = [f"clarification veto from: {', '.join(clarifications)}"]
    elif claim_disagreement:
        status = "clarification_required"
        reasons = ["completed committee members reconstructed different claims"]
    elif qualified >= config.policy.minimum_qualified_members:
        status = "ai_qualified"
        reasons = [
            f"{qualified} committee members qualified the same claim; "
            f"threshold {config.policy.minimum_qualified_members}"
        ]
    elif blockers:
        status = "technical_blocker"
        reasons = [f"qualification threshold not met; blockers from: {', '.join(blockers)}"]
    else:
        status = "clarification_required"
        reasons = [
            f"only {qualified} committee members qualified; "
            f"{config.policy.minimum_qualified_members} required"
        ]

    selected = next(
        (aggregates[member.id] for member in config.members if statuses[member.id] == "ai_qualified"),
        None,
    )
    if selected is None:
        selected = next(iter(aggregates.values()), None)
    return {
        "status": status,
        "reasons": reasons,
        "claim": selected.get("claim") if selected else None,
        "recomputed_cost": selected.get("recomputed_cost") if selected else None,
        "member_statuses": statuses,
    }


def run_committee(
    evidence: Mapping[str, Any],
    config: CommitteeConfig,
    base_config: Any,
    *,
    client_factory: Callable[[Any], Any] = OpenRouterClient,
    progress: Callable[[str, str], None] | None = None,
) -> dict[str, Any]:
    def run_member(member: CommitteeMember) -> dict[str, Any]:
        if progress is not None:
            progress(member.id, "started")
        client = client_factory(member_client_config(base_config, member))
        result = run_mvp(evidence, client)
        if progress is not None:
            progress(member.id, result["aggregate"]["status"])
        return result

    # Members never see one another's output. Parallelizing only across members keeps
    # each member's triage/correctness/complexity sequence intact while bounding wall
    # time near the slowest full panel instead of the sum of all panels.
    with ThreadPoolExecutor(
        max_workers=len(config.members), thread_name_prefix="hashsmash-judge"
    ) as executor:
        futures = {member.id: executor.submit(run_member, member) for member in config.members}
        member_dossiers = {
            member.id: futures[member.id].result() for member in config.members
        }
    return {
        "schema_version": "committee-dossier-v1",
        "committee_id": config.committee_id,
        "aggregate": aggregate_committee(member_dossiers, config),
        "members": member_dossiers,
    }
