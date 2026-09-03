"""Versioned prompt loading and inert evidence serialization."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping


PROMPT_DIR = Path(__file__).resolve().with_name("prompts")
STRATEGY_DIR = Path(__file__).resolve().with_name("strategies")
PROMPT_FILES = {
    "triage": "triage-v1.md",
    "correctness": "correctness-v1.md",
    "complexity": "complexity-v1.md",
    "adversarial": "adversarial-v1.md",
    "synthesis": "synthesis-v1.md",
}
STRATEGY_FILES = {
    "balanced-v1": "balanced-v1.md",
    "formal-proof-v1": "formal-proof-v1.md",
    "adversarial-v1": "adversarial-v1.md",
    "cost-skeptic-v1": "cost-skeptic-v1.md",
}
DEFAULT_STRATEGY = "formal-proof-v1"


def load_strategy_prompt(strategy: str) -> str:
    try:
        strategy_file = STRATEGY_FILES[strategy]
    except KeyError as exc:
        raise ValueError(f"unknown judge strategy: {strategy!r}") from exc
    return (STRATEGY_DIR / strategy_file).read_text(encoding="utf-8").strip()


def load_system_prompt(stage: str, strategy: str = DEFAULT_STRATEGY) -> str:
    """Return the common guardrails and the requested stage rubric."""

    try:
        stage_file = PROMPT_FILES[stage]
    except KeyError as exc:
        raise ValueError(f"unknown review stage: {stage!r}") from exc
    common = (PROMPT_DIR / "common-v1.md").read_text(encoding="utf-8").strip()
    strategy_prompt = load_strategy_prompt(strategy)
    rubric = (PROMPT_DIR / stage_file).read_text(encoding="utf-8").strip()
    return (
        f"{common}\n\nREVIEW STRATEGY: {strategy}\n\n{strategy_prompt}"
        f"\n\nREVIEW STAGE: {stage}\n\n{rubric}"
    )


def serialize_untrusted_evidence(stage: str, evidence: Mapping[str, Any]) -> str:
    """Serialize participant material as data, never as prompt instructions."""

    envelope = {
        "kind": "UNTRUSTED_EVIDENCE",
        "stage": stage,
        "evidence": evidence,
    }
    return json.dumps(envelope, ensure_ascii=True, sort_keys=True, separators=(",", ":"))


def build_messages(
    stage: str,
    evidence: Mapping[str, Any],
    strategy: str = DEFAULT_STRATEGY,
) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": load_system_prompt(stage, strategy)},
        {"role": "user", "content": serialize_untrusted_evidence(stage, evidence)},
    ]
