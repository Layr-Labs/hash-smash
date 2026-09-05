"""Organizer-owned paired candidate fixtures; never copied from solver drafts."""

from verifier.io import atomic_write_json


def candidate_fixture(root, track, *, ready=True):
    candidate = root / "inputs" / track.id
    candidate.mkdir(parents=True)
    claim = track.draft_claim()
    claim["submission_state"] = "ready" if ready else "draft"
    # Deliberately not a proved attack: only fake-provider tests accept this text.
    atomic_write_json(candidate / "claim.json", claim)
    (candidate / "proof.md").write_text("# Mock-only fixture\nNot a cryptanalytic proof.\n")
    atomic_write_json(candidate / "certificates" / "manifest.json", {"schema_version": 2, "certificates": []})
    return candidate
