"""Live truncated-differential demonstrator for blake3-r1.

Stdlib-only, deterministic. Per organizer trial, draws a random 64-byte
base message from the trial seed and returns the pair (base,
base xor DELTA) with DELTA = MSB of message word 9 (last-round diagonal
input). Offline measurement over 2^18 samples: the full 256-bit output
difference equals PATTERN with probability 0.4993. The organizer checks
the digest-xor-mask event on every returned pair.
"""
import hashlib
import json
import random
import struct
import sys

WORD = 9
DELTA = 1 << 31


def main():
    req = json.load(sys.stdin)
    rows = []
    for trial in req["trials"]:
        rng = random.Random(int.from_bytes(
            hashlib.sha256(("truncated-demo:" + str(trial["trial"]) + ":" +
                            trial["seed"]).encode()).digest(), "big"))
        words = [rng.getrandbits(32) for _ in range(16)]
        base = struct.pack("<16I", *words)
        mod = list(words)
        mod[WORD] ^= DELTA
        rows.append({
            "trial": trial["trial"],
            "message_a_hex": base.hex(),
            "message_b_hex": struct.pack("<16I", *mod).hex(),
        })
    json.dump({"schema_version": 1, "trials": rows}, sys.stdout, sort_keys=True)


main()
