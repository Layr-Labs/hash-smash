"""Closed-form collision generator for blake3-r1-prefix-v1.

Implements steps 1-3 of the algorithm in proof.md, Section 3. The organizer
request is read from stdin and one message pair is returned per trial: a
23-byte message and a 24-byte message. Each 32-byte trial seed is expanded
with SHAKE-256 into the single 256-bit coin word R. Only the standard library
is used; there is no OS randomness, wall time or ambient state. The program
never evaluates the target hash: the returned pairs collide by the identity
proved in proof.md, and the organizer runner recomputes both digests.
"""

import hashlib
import json
import struct
import sys

MASK = 0xFFFFFFFF
IV2 = 0x3C6EF372
IV6 = 0x1F83D9AB
K = (IV2 + IV6) & MASK  # v[2] + v[6] before the call G(2,6,10,14,w4,w5)
SHORT = 23
LONG = 24


def pair(seed):
    coins = hashlib.shake_256(seed).digest(32)
    # Step 1: w[0..5] are lanes 0..5 of R; the top byte of w5 is cleared so
    # that the first message has exactly 23 bytes of content.
    w = list(struct.unpack("<6I", coins[:24]))
    x = w[4]
    y = w[5] & 0x00FFFFFF

    # Step 2: cancel the block-length difference inside the one call that
    # reads it. a1 is the value of v[2] after the first addition of the call.
    a1 = (K + x) & MASK
    a1_other = a1 ^ SHORT ^ LONG
    x_other = (a1_other - K) & MASK
    y_other = (y + a1 - a1_other) & MASK

    # Step 3: the two messages share words 0..3 and differ in length and in
    # words 4 and 5.
    first = struct.pack("<6I", w[0], w[1], w[2], w[3], x, y)[:SHORT]
    second = struct.pack("<6I", w[0], w[1], w[2], w[3], x_other, y_other)
    return first, second


def main():
    request = json.load(sys.stdin)
    if request["schema_version"] != 1 or request["target_profile"] != "blake3-r1-prefix-v1":
        raise ValueError("unexpected organizer target")
    if request["event"] != {"kind": "full-collision"}:
        raise ValueError("unexpected organizer event")
    trials = []
    for trial in request["trials"]:
        first, second = pair(bytes.fromhex(trial["seed"]))
        trials.append({"trial": trial["trial"], "message_a_hex": first.hex(), "message_b_hex": second.hex()})
    json.dump({"schema_version": 1, "trials": trials}, sys.stdout, separators=(",", ":"), sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
