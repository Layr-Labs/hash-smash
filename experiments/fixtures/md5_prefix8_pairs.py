"""Organizer positive control: only modifies an unused MD5 prefix-eight word.

Each message is 48 bytes and pads to one block. Byte 40 is in message word 10,
which is not used by MD5's first eight steps. This is a small-instance executor
test, not evidence for any live frontier round.
"""

import hashlib
import json
import sys

request = json.load(sys.stdin)
rows = []
for trial in request["trials"]:
    message = hashlib.sha512(bytes.fromhex(trial["seed"])).digest()[:48]
    other = message[:40] + bytes([message[40] ^ 1]) + message[41:]
    rows.append({
        "trial": trial["trial"], "message_a_hex": message.hex(),
        "message_b_hex": other.hex(),
    })
json.dump({"schema_version": 1, "trials": rows}, sys.stdout, sort_keys=True)
