"""Replay of the single fresh-seed K-scan witness as pure embedded constants.

Participant program for kind python-message-pairs-v1: runs ONLY inside the
organizer networkless Docker sandbox. Reads one JSON request on stdin, writes
exactly one JSON document on stdout. Stdlib only; no file opens, no OS
randomness, no wall time. Every requested trial returns the same pair: the
first collision (trial index 2,685,579,961 = 2^31.3226) of the ONE fresh-seed
r31k K-scan charged in proof.md Section 3 (committed seed d5003c531ddf9d2a).
Messages are m0||m1 and m0||m1p, 128 bytes each; the organizer independently
recomputes both reduced-round digests and checks full equality plus message
distinctness. This evidences the collision relation of the construction only;
the attack cost is charged in proof.md, not here.
"""

import hashlib
import json
import sys

DOMAIN = b"HS-R31-WITNESS-REPLAY-V2"

# (m0, m1, m1p) as hex; each message is m0||m1 or m0||m1p, 128 bytes total.
WITNESSES = (
    ("31e466210c5e0cee8c92620bf2c932e2591e8e7f66aba6b6c5d7a1ce4271f854f79d392119de3876693dda454e12edbc412bef069bc22aa20b77d0130012b2b9",
     "76e3309715169879f84b370638a51c9120ed81ff06a2bca21756157406b457ba661915bf954a6452051063193a9ff24b4a4a9bfb5cf1caacd77b3aeed59e04dc",
     "76e3309715169879f84b370638a51c9120ed81ff06a2aca817769d6556a40db48e1a26bf954ae456051063193a9ff24b4a4a9bfb5cf1caacd77b3aeed59e04dc"),
    # digest (organizer-recomputed; cross-reference):
    # 8fc6cd1173ce63e44082ce6e3674737547649efc9f0d2651a35ff2153d871b53
)


def pair_for(seed_hex, trial_index):
    h = hashlib.sha256(
        DOMAIN + bytes.fromhex(seed_hex) + trial_index.to_bytes(4, "little")
    ).digest()
    m0, m1, m1p = WITNESSES[int.from_bytes(h[:4], "big") % len(WITNESSES)]
    return bytes.fromhex(m0 + m1), bytes.fromhex(m0 + m1p)


def main():
    request = json.load(sys.stdin)
    if request["schema_version"] != 1:
        raise ValueError("unexpected schema")
    if request["target_profile"] != "sha256-r31-prefix-v1":
        raise ValueError("unexpected organizer target")
    if request["event"] != {"kind": "full-collision"}:
        raise ValueError("unexpected organizer event")
    trials = []
    for trial in request["trials"]:
        a, b = pair_for(trial["seed"], trial["trial"])
        trials.append({
            "trial": trial["trial"],
            "message_a_hex": a.hex(),
            "message_b_hex": b.hex(),
        })
    json.dump({"schema_version": 1, "trials": trials}, sys.stdout,
              separators=(",", ":"), sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
