"""Organizer-configured model and prompt strategy per paired-review role."""

from dataclasses import replace
from pathlib import Path
import hashlib
import json
import os

from .lanes import LANE_STAGES
from .prompts import load_system_prompt
from .bedrock_adapter import BedrockConfig, bedrock_system_prompt

DIRECTORY = Path(__file__).resolve().with_name("committees")


def build_role_clients(base_config, client_factory, *, mode: str):
    if mode == "single":
        return {}, {"mode": "single-model-independent-roles"}
    if mode != "committee":
        raise ValueError("HASHSMASH_JUDGE_MODE must be single or committee")
    path = Path(os.environ.get("HASHSMASH_ROLE_COMMITTEE_PATH", str(DIRECTORY / "paired-roles-v1.json"))).resolve()
    if path.parent != DIRECTORY.resolve():
        raise ValueError("role committee must be an organizer file directly under judge/committees")
    raw = path.read_bytes()
    config = json.loads(raw)
    if (not isinstance(config, dict) or set(config) != {"schema_version", "id", "roles"}
            or config["schema_version"] != 1 or not isinstance(config["roles"], dict)
            or set(config["roles"]) != set(LANE_STAGES)):
        raise ValueError("role committee must configure exactly all six paired judge roles")
    clients, records = {}, {}
    for stage in LANE_STAGES:
        spec = config["roles"][stage]
        if (not isinstance(spec, dict) or not spec
                or set(spec) - {"model", "strategy", "reasoning_effort", "max_tokens"}):
            raise ValueError("invalid role override; credentials and providers cannot be overridden")
        effective = replace(base_config, **spec)
        # Dataclass validation and prompt lookup validate every configured value.
        prompt = bedrock_system_prompt(effective, stage) if isinstance(effective, BedrockConfig) else load_system_prompt(stage, effective.strategy)
        clients[stage] = client_factory(effective)
        records[stage] = {
            "model": effective.model, "strategy": effective.strategy,
            "reasoning_effort": effective.reasoning_effort, "max_tokens": effective.max_tokens,
            "system_prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        }
    return clients, {"id": config["id"], "profile_sha256": hashlib.sha256(raw).hexdigest(),
                     "mode": "role-committee", "roles": records,
                     "aggregation": "shared proof obligations; no majority vote"}
