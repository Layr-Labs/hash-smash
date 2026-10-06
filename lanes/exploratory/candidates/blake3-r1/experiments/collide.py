"""Emit the fixed blake3-r1 collision witness for every requested trial.

Deterministic stdlib-only program for the organizer's bounded Docker
executor (python-message-pairs-v1, full-collision event). The witness pair
was discovered once by an offline Z3 search; this program only replays the
stored bytes so the organizer independently recomputes both digests.
"""
import json
import sys

MSG_A_HEX = "00" * 64
MSG_B_HEX = (
    "40e88e6cf0fc0a3a56ee4f6d75b50fb07a836a7c75ad3b17"
    "ca278663d0e9884c511ec7c503e24b10fa65e612aaad1d14"
    "30c353e769a772cefd94e2dc25367353"
)


def main():
    request = json.load(sys.stdin)
    rows = []
    for trial in request["trials"]:
        rows.append({
            "trial": trial["trial"],
            "message_a_hex": MSG_A_HEX,
            "message_b_hex": MSG_B_HEX,
        })
    json.dump({"schema_version": 1, "trials": rows}, sys.stdout, sort_keys=True)


main()
