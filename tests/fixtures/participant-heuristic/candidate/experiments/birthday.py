"""Participant-interface fixture; execute ONLY in the organizer Docker sandbox.

This deliberately noncompetitive eight-step MD5 attack tests a success heuristic,
not a new cryptanalytic result. No output counter or timing is authoritative.
"""

import hashlib
import json
import sys

DOMAIN = b"HS-BATCH-v1"
BATCH_SIZE = 256


def message(value, counter):
    # Words 0..7 determine the first eight MD5 steps. Word 8 distinguishes
    # messages but is not read at this depth. Equal lengths give equal padding.
    return value.to_bytes(4, "little") + bytes(28) + counter.to_bytes(4, "little") + bytes(28)


def batch(seed):
    seen = []
    for counter in range(BATCH_SIZE):
        value = int.from_bytes(hashlib.sha256(DOMAIN + seed + counter.to_bytes(2, "little")).digest()[:2], "little")
        # Linear scan: bounded worst-case accounting, with no hash-table premise.
        for earlier, previous in enumerate(seen):
            if previous == value:
                return message(value, earlier).hex(), message(value, counter).hex()
        seen.append(value)
    return None, None


def main():
    request = json.load(sys.stdin)
    if request["schema_version"] != 1 or request["target_profile"] != "md5-s8-prefix-v1":
        raise ValueError("unexpected organizer target")
    if request["event"] != {"kind": "full-collision"}:
        raise ValueError("unexpected organizer event")
    trials = []
    for trial in request["trials"]:
        first, second = batch(bytes.fromhex(trial["seed"]))
        trials.append({"trial": trial["trial"], "message_a_hex": first, "message_b_hex": second})
    json.dump({"schema_version": 1, "trials": trials}, sys.stdout, separators=(",", ":"), sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
