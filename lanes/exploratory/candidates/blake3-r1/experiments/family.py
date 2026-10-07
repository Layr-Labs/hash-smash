"""Second-message generator for blake3-r1-prefix-v1: the family of proof.md Section 9.

For each organizer trial the seed is expanded with SHAKE-256 into a length n in 0..63, a second length n2 with
max(n + 1, 24) <= n2 <= 64, and n message bytes. The program returns that n-byte message and the n2-byte
message of Corollary 1: the same zero-filled block with words 4 and 5 replaced as in the Lemma of proof.md
Section 2. Only the standard library is used; there is no OS randomness, wall time or ambient state. The
program never evaluates the target hash: the organizer runner recomputes both digests.
"""

import hashlib
import json
import struct
import sys

MASK = 0xFFFFFFFF
IV2 = 0x3C6EF372
IV6 = 0x1F83D9AB
K = (IV2 + IV6) & MASK  # v[2] + v[6] before the call G(2,6,10,14,w4,w5) of a one-block message


def second_message(first, n2):
    n = len(first)
    block = first + bytes(64 - n)  # the zero-filled block of the first message
    x, y = struct.unpack("<2I", block[16:24])
    a1 = (K + x) & MASK
    a1_other = a1 ^ n ^ n2
    x_other = (a1_other - K) & MASK
    y_other = (y + a1 - a1_other) & MASK
    # n2 >= 24 keeps both replaced words inside the message; n2 > n keeps every byte from n2 on equal to zero.
    return (block[:16] + struct.pack("<2I", x_other, y_other) + block[24:])[:n2]


def pair(seed):
    coins = hashlib.shake_256(seed).digest(66)
    n = coins[0] % 64
    low = max(n + 1, 24)
    n2 = low + coins[1] % (65 - low)
    first = coins[2:2 + n]
    return first, second_message(first, n2)


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
