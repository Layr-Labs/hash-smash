"""Organizer-owned local track registry. Never infer a track from candidate text."""

from dataclasses import dataclass
from pathlib import Path
import re

from .errors import VerificationError
from .hash_functions import DIGEST_BITS, FULL_ROUNDS
from .io import canonical_json_bytes, load_json_bytes, sha256_bytes

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "tracks" / "registry.json"
TRACK_ID = re.compile(r"[a-z0-9]+-(?:r|s)[0-9]{1,2}\Z")


@dataclass(frozen=True)
class Track:
    id: str
    algorithm: str
    rounds: int
    difficulty: str
    purpose: str

    @property
    def profile_id(self) -> str:
        return f"{self.id}-prefix-v1"

    @property
    def digest_bits(self) -> int:
        return DIGEST_BITS[self.algorithm]

    @property
    def candidate(self) -> Path:
        return ROOT / "candidates" / self.id

    @property
    def profile_path(self) -> Path:
        return ROOT / "target-profiles" / f"{self.profile_id}.json"

    @property
    def cost_path(self) -> Path:
        return ROOT / "cost-models" / "collision-local-v2.json"

    @property
    def reference_id(self) -> str:
        return f"{self.id}-nominal-v1"

    def draft_claim(self) -> dict:
        """Organizer template, independent of the mutable solver candidate."""
        return {
            "schema_version": 2, "submission_state": "draft", "target_profile": self.profile_id,
            "attack_class": "ordinary-collision", "rounds": self.rounds,
            "claim": {"time_log2": self.digest_bits / 2, "time_unit": "target-compressions",
                      "memory_log2_bytes": self.digest_bits / 2, "data_log2": self.digest_bits / 2,
                      "preprocessing_log2": 0, "success_probability": 0.39,
                      "nonuniform_advice_log2_bytes": 0},
            "restrictions": [], "baseline_improved": self.reference_id,
            "certificate_manifest": "certificates/manifest.json",
        }

    def benchmark(self) -> dict:
        profile = load_json_bytes(self.profile_path.read_bytes(), str(self.profile_path))
        cost = load_json_bytes(self.cost_path.read_bytes(), str(self.cost_path))
        if (profile.get("id"), profile.get("algorithm"), profile.get("rounds"), profile.get("digest_bits")) != (
            self.profile_id, self.algorithm, self.rounds, self.digest_bits,
        ):
            raise VerificationError(f"{self.id}: registry/profile mismatch")
        if cost.get("id") != "collision-local-v2" or cost.get("time_unit") != "target-compressions":
            raise VerificationError("unexpected local cost model")
        return {
            "track_id": self.id,
            "target_profile": profile,
            "cost_model": cost,
            "reference_checker_sha256": sha256_bytes((ROOT / "verifier" / "hash_functions.py").read_bytes()),
            "qualification_policy": {
                "id": "unconditional-v1",
                "sha256": sha256_bytes((ROOT / "judge" / "policies" / "unconditional-v1.md").read_text().strip().encode()),
            },
            "frontier": {
                "id": self.reference_id,
                "status": "nominal-reference-only",
                "is_qualified_baseline": False,
                "target_profile": self.profile_id,
                "rounds": self.rounds,
                "digest_bits": self.digest_bits,
                "nominal_collision_work_log2": self.digest_bits / 2,
                "nominal_memory_log2_bytes": self.digest_bits / 2,
                "score": float(self.digest_bits),
                "note": "Output-width-derived starting target, not a proved attack, security bound, or accepted result. Ignores implementation/storage constants and actual cryptanalysis. Do not use as a lemma or assume its attainability.",
            },
        }

    def config_sha256(self) -> str:
        return sha256_bytes(canonical_json_bytes(self.benchmark()))


def all_tracks() -> tuple[Track, ...]:
    raw = load_json_bytes(REGISTRY_PATH.read_bytes(), str(REGISTRY_PATH))
    if not isinstance(raw, dict) or set(raw) != {"schema_version", "tracks"} or raw["schema_version"] != 1:
        raise VerificationError("invalid track registry")
    if not isinstance(raw["tracks"], list) or not 1 <= len(raw["tracks"]) <= 20:
        raise VerificationError("registry requires 1 to 20 tracks")
    tracks = []
    for row in raw["tracks"]:
        if not isinstance(row, dict) or set(row) != {"id", "algorithm", "rounds", "difficulty", "purpose"}:
            raise VerificationError("invalid track entry")
        if (not isinstance(row["id"], str) or not TRACK_ID.fullmatch(row["id"])
                or not isinstance(row["algorithm"], str) or row["algorithm"] not in FULL_ROUNDS
                or type(row["rounds"]) is not int or not 1 <= row["rounds"] <= FULL_ROUNDS[row["algorithm"]]
                or row["difficulty"] not in ("easy-control", "exploratory", "hard-endpoint")
                or not isinstance(row["purpose"], str) or not row["purpose"]):
            raise VerificationError("invalid track fields")
        expected_id = f"{row['algorithm']}-{'s' if row['algorithm'] == 'md5' else 'r'}{row['rounds']}"
        if row["id"] != expected_id:
            raise VerificationError("track id must match algorithm and round count")
        tracks.append(Track(**row))
    if len({t.id for t in tracks}) != len(tracks):
        raise VerificationError("duplicate track id")
    return tuple(tracks)


def get_track(track_id: str) -> Track:
    for track in all_tracks():
        if track.id == track_id:
            return track
    raise VerificationError(f"unknown local track: {track_id!r}")
