#!/usr/bin/env python3
"""Scaled grouped birthday probes for 2-round BLAKE3.

The program is deterministic from the organizer seed. It searches a tiny
analogue of the submitted message family and returns one masked pair, or two
nulls. It does not claim an attack cost.
"""

import hashlib
import json
import struct
import sys

M = 0xFFFFFFFF
IV = (
    0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
    0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19,
)
PERM = (2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8)


def ror(v, n):
    return ((v >> n) | (v << (32 - n))) & M


def g(v, a, b, c, d, x, y):
    v[a] = (v[a] + v[b] + x) & M
    v[d] = ror(v[d] ^ v[a], 16)
    v[c] = (v[c] + v[d]) & M
    v[b] = ror(v[b] ^ v[c], 12)
    v[a] = (v[a] + v[b] + y) & M
    v[d] = ror(v[d] ^ v[a], 8)
    v[c] = (v[c] + v[d]) & M
    v[b] = ror(v[b] ^ v[c], 7)


def digest_bytes(words):
    v = list(IV) + list(IV[:4]) + [0, 0, 64, 11]
    m = list(words)
    for _ in range(2):
        g(v, 0, 4, 8, 12, m[0], m[1])
        g(v, 1, 5, 9, 13, m[2], m[3])
        g(v, 2, 6, 10, 14, m[4], m[5])
        g(v, 3, 7, 11, 15, m[6], m[7])
        g(v, 0, 5, 10, 15, m[8], m[9])
        g(v, 1, 6, 11, 12, m[10], m[11])
        g(v, 2, 7, 8, 13, m[12], m[13])
        g(v, 3, 4, 9, 14, m[14], m[15])
        m = [m[i] for i in PERM]
    out = [v[i] ^ v[i + 8] for i in range(8)]
    return struct.pack("<8I", *out)


def word32(seed, counter):
    block = hashlib.sha256(seed + counter.to_bytes(4, "little")).digest()
    return int.from_bytes(block[:4], "little")


def search(seed, one_group, mask):
    seen = {}
    if one_group:
        groups, width = 1, 1024
    else:
        groups, width = 32, 32
    for group in range(groups):
        prefix = [word32(seed, group * 16 + i) for i in range(15)]
        for t in range(width):
            raw = struct.pack("<16I", *(prefix + [t & M]))
            key = int.from_bytes(digest_bytes(prefix + [t & M]), "big") & mask
            prior = seen.get(key)
            if prior is not None and prior != raw:
                return prior, raw
            seen[key] = raw
    return None, None


def main():
    request = json.load(sys.stdin)
    mask = int(request["event"]["mask_hex"], 16)
    one_group = request["experiment_id"] == "b3r2-one-group"
    rows = []
    for trial in request["trials"]:
        left, right = search(bytes.fromhex(trial["seed"]), one_group, mask)
        if left is None:
            rows.append({
                "trial": trial["trial"],
                "message_a_hex": None,
                "message_b_hex": None,
            })
        else:
            rows.append({
                "trial": trial["trial"],
                "message_a_hex": left.hex(),
                "message_b_hex": right.hex(),
                "observations": {"messages": 1024, "mask_bits": 20},
            })
    json.dump({"schema_version": 1, "trials": rows}, sys.stdout, separators=(",", ":"))


if __name__ == "__main__":
    main()
