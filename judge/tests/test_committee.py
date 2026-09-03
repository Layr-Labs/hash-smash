from __future__ import annotations

import json
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from judge.committee import (
    aggregate_committee,
    load_committee,
    member_client_config,
    run_committee,
)
from judge.bedrock_adapter import BedrockConfig
from judge.provider_adapter import OpenRouterClient, OpenRouterConfig
from judge.tests.helpers import provider_response, review


class FakeTransport:
    def __init__(self):
        self.responses = [
            provider_response(review(stage))
            for stage in ("triage", "correctness", "complexity")
        ]

    def request(self, url, *, headers, body, timeout_seconds):
        return self.responses.pop(0)


CLAIM = {
    "target_profile": "sha1-fips180-4-v1",
    "attack_class": "ordinary-collision",
    "rounds": 80,
    "summary": "Generic full-round collision search.",
    "restrictions": ["random-function heuristic"],
}


def dossier(status: str, *, claim=None):
    return {
        "aggregate": {
            "status": status,
            "reasons": [status],
            "claim": CLAIM if claim is None else claim,
            "recomputed_cost": None,
        }
    }


class CommitteeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = load_committee()

    def complete(self, status: str = "ai_qualified"):
        return {member.id: dossier(status) for member in self.config.members}

    def test_checked_in_committee_is_strict_and_diverse(self) -> None:
        self.assertEqual(self.config.schema_version, "committee-v1")
        self.assertEqual(len(self.config.members), 3)
        self.assertEqual(len({member.model for member in self.config.members}), 3)
        self.assertEqual(len({member.strategy for member in self.config.members}), 3)
        self.assertEqual(self.config.policy.minimum_qualified_members, 3)

    def test_checked_in_bedrock_committee_diversifies_strategies(self) -> None:
        path = Path(__file__).parents[1] / "committees" / "committee-bedrock-v1.json"
        config = load_committee(path)
        self.assertEqual(len(config.members), 3)
        self.assertEqual(len({member.model for member in config.members}), 1)
        self.assertEqual(len({member.strategy for member in config.members}), 3)
        self.assertEqual(config.policy.minimum_qualified_members, 3)

    def test_member_configuration_supports_bedrock(self) -> None:
        path = Path(__file__).parents[1] / "committees" / "committee-bedrock-v1.json"
        member = load_committee(path).members[0]
        configured = member_client_config(BedrockConfig(api_key="secret"), member)
        self.assertIsInstance(configured, BedrockConfig)
        self.assertEqual(configured.model, member.model)
        self.assertEqual(configured.strategy, member.strategy)
        self.assertNotIn("secret", repr(configured))

    def test_unknown_configuration_field_is_rejected(self) -> None:
        raw = json.loads(
            (Path(__file__).parents[1] / "committees" / "committee-v1.json").read_text()
        )
        raw["members"][0]["hidden"] = True
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "committee.json"
            path.write_text(json.dumps(raw))
            with self.assertRaisesRegex(ValueError, "unknown fields.*hidden"):
                load_committee(path)

    def test_unanimous_qualification(self) -> None:
        aggregate = aggregate_committee(self.complete(), self.config)
        self.assertEqual(aggregate["status"], "ai_qualified")
        self.assertEqual(set(aggregate["member_statuses"].values()), {"ai_qualified"})

    def test_blocker_and_clarification_vetoes(self) -> None:
        members = self.complete()
        members[self.config.members[0].id] = dossier("technical_blocker")
        self.assertEqual(
            aggregate_committee(members, self.config)["status"], "technical_blocker"
        )
        members = self.complete()
        members[self.config.members[1].id] = dossier("clarification_required")
        self.assertEqual(
            aggregate_committee(members, self.config)["status"], "clarification_required"
        )

    def test_missing_member_or_infrastructure_failure_fails_closed(self) -> None:
        members = self.complete()
        members[self.config.members[2].id] = dossier("judge_infra_failed")
        self.assertEqual(
            aggregate_committee(members, self.config)["status"], "judge_infra_failed"
        )
        del members[self.config.members[2].id]
        self.assertEqual(
            aggregate_committee(members, self.config)["status"], "judge_infra_failed"
        )

    def test_claim_disagreement_requires_clarification_without_vetoes(self) -> None:
        relaxed = replace(
            self.config,
            policy=replace(
                self.config.policy,
                technical_blocker_veto=False,
                clarification_veto=False,
            ),
        )
        members = self.complete()
        different = dict(CLAIM, rounds=79)
        members[self.config.members[0].id] = dossier("ai_qualified", claim=different)
        self.assertEqual(
            aggregate_committee(members, relaxed)["status"], "clarification_required"
        )

    def test_member_configuration_overrides_model_strategy_and_reasoning(self) -> None:
        base = OpenRouterConfig(api_key="secret")
        member = self.config.members[1]
        configured = member_client_config(base, member)
        self.assertEqual(configured.model, member.model)
        self.assertEqual(configured.strategy, member.strategy)
        self.assertEqual(configured.reasoning_effort, member.reasoning_effort)
        self.assertNotIn("secret", repr(configured))

    def test_committee_runner_executes_full_independent_panel_per_member(self) -> None:
        seen = []

        def factory(config):
            seen.append(config)
            return OpenRouterClient(config, transport=FakeTransport(), sleeper=lambda _: None)

        result = run_committee(
            {"proof_markdown": "proof"},
            self.config,
            OpenRouterConfig(api_key="secret"),
            client_factory=factory,
        )
        self.assertEqual(result["aggregate"]["status"], "ai_qualified")
        self.assertEqual(len(result["members"]), 3)
        self.assertEqual({config.model for config in seen}, {m.model for m in self.config.members})
        self.assertEqual(
            {config.strategy for config in seen}, {m.strategy for m in self.config.members}
        )


if __name__ == "__main__":
    unittest.main()
