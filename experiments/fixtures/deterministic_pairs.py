"""Organizer smoke fixture, never used as a solver submission or attack claim."""

import hashlib
import json
import sys

request = json.load(sys.stdin)
rows = []
for trial in request["trials"]:
    message = hashlib.sha256(bytes.fromhex(trial["seed"])).digest()
    other = bytes([message[0] ^ 1]) + message[1:]
    rows.append({
        "trial": trial["trial"], "message_a_hex": message.hex(),
        "message_b_hex": other.hex(),
    })
json.dump({"schema_version": 1, "trials": rows}, sys.stdout, sort_keys=True)
