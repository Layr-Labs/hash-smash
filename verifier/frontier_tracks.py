"""Paired research lanes selected by the organizer, independent of solver input."""

from dataclasses import dataclass
from pathlib import Path
import re

from .errors import VerificationError
from .io import canonical_json_bytes, load_json_bytes, sha256_bytes

ROOT = Path(__file__).resolve().parents[1]

CATALOG_PATH = ROOT / "tracks" / "frontier-v1.json"
LANES = {"exploratory": "plausible_not_refuted", "rigorous": "ai_rigor_qualified"}


def catalog() -> dict:
    data = load_json_bytes(CATALOG_PATH.read_bytes(), str(CATALOG_PATH))
    if (not isinstance(data, dict) or data.get("schema_version") != 1
            or not isinstance(data.get("families"), list) or len(data["families"]) != 7):
        raise VerificationError("frontier catalog must describe seven algorithm families")
    ids = set()
    for family in data["families"]:
        key = family.get("id")
        if not isinstance(key, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", key) or key in ids:
            raise VerificationError("invalid or duplicate frontier family")
        ids.add(key)
        pair = family.get("round_pair")
        if pair is None:
            if family.get("selection_status") != "needs_definition":
                raise VerificationError("missing rounds require needs_definition status")
            continue
        if (not isinstance(pair, list) or len(pair) != 2
                or any(type(r) is not int for r in pair) or pair[0] < 1
                or pair[1] != pair[0] + 1 or pair[1] > family["full_rounds"]):
            raise VerificationError("frontier round pair must be consecutive valid round counts")
        if family.get("selection_status") not in ("selected", "full_round_control"):
            raise VerificationError("unconfirmed frontier family cannot become a runnable track")
        if family["selection_status"] == "full_round_control" and family.get("first_unbroken_round") is not None:
            raise VerificationError("broken full-round controls have no first-unbroken round")
        if family["selection_status"] == "selected" and family.get("first_unbroken_round") != pair[1]:
            raise VerificationError("selected frontier boundary must match upper round count")
    return data


@dataclass(frozen=True)
class LaneTrack:
    id: str
    algorithm: str
    rounds: int
    difficulty: str
    purpose: str
    lane: str
    target_id: str
    output_bits: int
    nominal_security_bits: int
    selection_status: str
    boundary_role: str

    @property
    def challenge_root(self) -> Path:
        return ROOT / "lanes" / self.lane

    @property
    def candidate(self) -> Path:
        return self.challenge_root / "candidates" / self.target_id

    @property
    def state_root(self) -> Path:
        return self.challenge_root / ".yukon"

    @property
    def profile_id(self) -> str:
        return f"{self.target_id}-prefix-v1"

    @property
    def digest_bits(self) -> int:
        return self.output_bits

    @property
    def profile_path(self) -> Path:
        return ROOT / "target-profiles" / f"{self.profile_id}.json"

    @property
    def cost_path(self) -> Path:
        return ROOT / "cost-models" / "collision-frontier-v3.json"

    @property
    def reference_id(self) -> str:
        return f"{self.target_id}-nominal-v2"

    @property
    def accepted_status(self) -> str:
        return LANES[self.lane]

    @property
    def nominal_score(self) -> float:
        return float(self.nominal_security_bits)

    def draft_claim(self) -> dict:
        """Organizer template, independent of the mutable solver candidate."""
        return {
            "schema_version": 3, "submission_state": "draft", "target_profile": self.profile_id,
            "attack_class": "ordinary-collision", "rounds": self.rounds,
            "claim": {"time_log2": self.digest_bits / 2, "time_unit": "target-compressions",
                      "memory_log2_bytes": 0, "data_log2": self.digest_bits / 2,
                      "preprocessing_log2": 0, "success_probability": 0.39,
                      "nonuniform_advice_log2_bytes": 0},
            "restrictions": [], "baseline_improved": self.reference_id,
            "certificate_manifest": "certificates/manifest.json",
            "lane": self.lane, "heuristics": [],
        }

    def benchmark(self) -> dict:
        profile = load_json_bytes(self.profile_path.read_bytes(), str(self.profile_path))
        cost = load_json_bytes(self.cost_path.read_bytes(), str(self.cost_path))
        if (profile.get("id"), profile.get("algorithm"), profile.get("rounds"), profile.get("digest_bits")) != (
            self.profile_id, self.algorithm, self.rounds, self.digest_bits,
        ):
            raise VerificationError(f"{self.id}: frontier registry/profile mismatch")
        if cost.get("id") != "collision-frontier-v3":
            raise VerificationError("unexpected frontier cost model")
        # Bind every organizer experiment/checker implementation, including dependencies.
        implementation_files = sorted((ROOT / "verifier").glob("*.py"))
        implementation_files += sorted((ROOT / "experiments").glob("*.py"))
        implementations = {str(path.relative_to(ROOT)): sha256_bytes(path.read_bytes())
                           for path in implementation_files}
        policies = sorted((ROOT / "judge" / "policies").glob("*lanes*.md"))
        if not policies:
            raise VerificationError("paired lane policy is not installed")
        policy_files = policies + [ROOT / "judge" / name for name in (
            "paired_review.py", "lanes.py", "schema_validation.py", "prompts.py", "role_committee.py")]
        policy_files += sorted((ROOT / "judge" / "prompts").glob("lane-*-v1.md"))
        policy_files += [ROOT / "judge" / "prompts" / "paired-common-v1.md"]
        policy_files += sorted((ROOT / "judge" / "strategies").glob("*.md"))
        policy_files += [ROOT / "schemas" / name for name in (
            "review-lanes-v1.schema.json", "claim-frontier-v3.schema.json", "experiment-manifest-v1.schema.json")]
        return {
            "track_id": self.id, "lane": self.lane, "target_id": self.target_id,
            "target_profile": profile, "cost_model": cost,
            "reference_checker_sha256": sha256_bytes(canonical_json_bytes(implementations)),
            "qualification_policy": {
                "id": "paired-lanes-v1", "lane": self.lane,
                "pass_status": self.accepted_status,
                "sha256": sha256_bytes(canonical_json_bytes({
                    str(path.relative_to(ROOT)): sha256_bytes(path.read_bytes()) for path in policy_files})),
            },
            "selection": {"status": self.selection_status, "boundary_role": self.boundary_role},
            "frontier": {
                "id": self.reference_id, "status": "nominal-reference-only",
                "is_qualified_baseline": False, "target_profile": self.profile_id,
                "rounds": self.rounds, "digest_bits": self.digest_bits,
                "nominal_collision_security_bits": self.nominal_security_bits,
                "score": self.nominal_score,
                "note": "Organizer nominal security exponent, matching the mockup. It is neither an executed or qualified baseline nor a proved time-memory bound; byte and instruction constants require accounting in each submission.",
            },
        }

    def config_sha256(self) -> str:
        return sha256_bytes(canonical_json_bytes(self.benchmark()))


def frontier_tracks() -> tuple[LaneTrack, ...]:
    result = []
    for family in catalog()["families"]:
        if family["round_pair"] is None:
            continue
        for index, rounds in enumerate(family["round_pair"]):
            target = f"{family['id']}-{'s' if family['algorithm'] == 'md5' else 'r'}{rounds}"
            for lane in LANES:
                result.append(LaneTrack(
                    id=f"{target}-{lane}", algorithm=family["algorithm"], rounds=rounds,
                    difficulty="frontier", purpose=family["selection_note"], lane=lane,
                    target_id=target, output_bits=family["digest_bits"],
                    nominal_security_bits=family["nominal_security_bits"],
                    selection_status=family["selection_status"],
                    boundary_role=("predecessor", "boundary")[index] if family["selection_status"] == "selected"
                    else ("penultimate-control", "full-round-control")[index],
                ))
    return tuple(result)


def get_frontier_track(track_id: str) -> LaneTrack:
    for track in frontier_tracks():
        if track.id == track_id:
            return track
    raise VerificationError(f"unknown or not-yet-defined frontier track: {track_id!r}")


def planned_slots() -> list[dict]:
    """All 28 requested slots, without inventing numbers for unresolved targets."""
    return [{"family": f["id"], "lane": lane, "position": position,
             "rounds": f["round_pair"][index] if f["round_pair"] else None,
             "selection_status": f["selection_status"], "note": f["selection_note"]}
            for f in catalog()["families"]
            for index, position in enumerate(("lower", "upper")) for lane in LANES]
