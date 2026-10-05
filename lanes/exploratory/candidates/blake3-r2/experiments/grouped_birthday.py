"""Scaled grouped birthday search on 2-round BLAKE3 (python-message-pairs-v1).

Digests are computed by m15-amortised partial evaluation of the exact 2-round
root compression. Organizer seeds expand to group prefixes. Checked events are
digest-xor-mask (20 bits) with N_t^2/2^w = 1 for the spread layout.

Experiment ids:
  b3r2-grouped-spread — 32 groups x 32 m15 values
  b3r2-single-group   — 1 group, m15 = 0..1023
"""

from __future__ import annotations

import hashlib
import json
import struct
import sys

MASK = 0xFFFFFFFF
IV = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
      0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)
PERM = (2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8)
SCHEDULE = [
    (0, 4, 8, 12, 0, 1), (1, 5, 9, 13, 2, 3), (2, 6, 10, 14, 4, 5), (3, 7, 11, 15, 6, 7),
    (0, 5, 10, 15, 8, 9), (1, 6, 11, 12, 10, 11), (2, 7, 8, 13, 12, 13), (3, 4, 9, 14, 14, 15),
]
FLAGS = 1 | 2 | 8


def _ror(v: int, n: int) -> int:
    return ((v >> n) | (v << (32 - n))) & MASK


def _g(v, a, b, c, d, x, y) -> None:
    v[a] = (v[a] + v[b] + x) & MASK
    v[d] = _ror(v[d] ^ v[a], 16)
    v[c] = (v[c] + v[d]) & MASK
    v[b] = _ror(v[b] ^ v[c], 12)
    v[a] = (v[a] + v[b] + y) & MASK
    v[d] = _ror(v[d] ^ v[a], 8)
    v[c] = (v[c] + v[d]) & MASK
    v[b] = _ror(v[b] ^ v[c], 7)


def _g_first_half(v, a, b, c, d, x) -> None:
    v[a] = (v[a] + v[b] + x) & MASK
    v[d] = _ror(v[d] ^ v[a], 16)
    v[c] = (v[c] + v[d]) & MASK
    v[b] = _ror(v[b] ^ v[c], 12)


def _g_second_half(v, a, b, c, d, y) -> None:
    v[a] = (v[a] + v[b] + y) & MASK
    v[d] = _ror(v[d] ^ v[a], 8)
    v[c] = (v[c] + v[d]) & MASK
    v[b] = _ror(v[b] ^ v[c], 7)


def _init() -> list:
    return list(IV) + list(IV[:4]) + [0, 0, 64, FLAGS]


def group_setup(m014: list) -> tuple:
    m = list(m014) + [0]
    v = _init()
    for a, b, c, d, x, y in SCHEDULE[:7]:
        _g(v, a, b, c, d, m[x], m[y])
    a, b, c, d, x, y = SCHEDULE[7]
    _g_first_half(v, a, b, c, d, m[x])
    mp = [m[i] for i in PERM]
    a1 = (v[1] + v[5] + mp[2]) & MASK
    d1 = _ror(v[13] ^ a1, 16)
    a1c2 = (v[2] + v[6] + mp[4]) & MASK
    return v, (a1, d1, a1c2)


def digest_for(m014: list, m15: int, mid: list, inv: tuple) -> bytes:
    v = list(mid)
    _g_second_half(v, 3, 4, 9, 14, m15)
    m = list(m014) + [m15]
    mp = [m[i] for i in PERM]
    a1, d1, a1c2 = inv
    _g(v, 0, 4, 8, 12, mp[0], mp[1])
    v[1], v[13] = a1, d1
    v[9] = (v[9] + v[13]) & MASK
    v[5] = _ror(v[5] ^ v[9], 12)
    _g_second_half(v, 1, 5, 9, 13, mp[3])
    v[2] = a1c2
    v[14] = _ror(v[14] ^ v[2], 16)
    v[10] = (v[10] + v[14]) & MASK
    v[6] = _ror(v[6] ^ v[10], 12)
    _g_second_half(v, 2, 6, 10, 14, mp[5])
    _g(v, 3, 7, 11, 15, mp[6], mp[7])
    for a, b, c, d, x, y in SCHEDULE[4:]:
        _g(v, a, b, c, d, mp[x], mp[y])
    out = [(v[i] ^ v[i + 8]) & MASK for i in range(8)]
    return struct.pack("<8I", *out)


def message_bytes(m014: list, m15: int) -> bytes:
    return struct.pack("<16I", *(list(m014) + [m15]))


def expand_prefixes(seed_hex: str, n_groups: int) -> list:
    """Deterministic stream of n_groups prefixes (15 u32 each) from seed."""
    raw = bytes.fromhex(seed_hex)
    out = []
    counter = 0
    while len(out) < n_groups:
        block = hashlib.sha256(raw + counter.to_bytes(4, "little")).digest()
        counter += 1
        words = list(struct.unpack("<8I", block))
        # need 15 words per group: take from successive blocks
        while len(words) < 15:
            block = hashlib.sha256(raw + counter.to_bytes(4, "little")).digest()
            counter += 1
            words.extend(struct.unpack("<8I", block))
        out.append(words[:15])
    return out


def mask_key_spread(dig: bytes) -> int:
    """20-bit key matching mask ff000000 ff000000 0f000000 on LE digest words."""
    o = struct.unpack("<8I", dig)
    return (o[0] & 0xFF) | ((o[1] & 0xFF) << 8) | ((o[2] & 0xF) << 16)


def mask_key_single(dig: bytes) -> int:
    """20-bit key matching mask on o3,o4,o5 low bits."""
    o = struct.unpack("<8I", dig)
    return (o[3] & 0xFF) | ((o[4] & 0xFF) << 8) | ((o[5] & 0xF) << 16)


def find_pair(prefixes: list, n_y: int, key_fn) -> tuple:
    bags: dict = {}
    for m014 in prefixes:
        mid, inv = group_setup(m014)
        for y in range(n_y):
            dig = digest_for(m014, y, mid, inv)
            key = key_fn(dig)
            msg = message_bytes(m014, y)
            if key in bags and bags[key] != msg:
                return bags[key].hex(), msg.hex()
            bags[key] = msg
    return None, None


def run_trial(experiment_id: str, seed_hex: str) -> tuple:
    if experiment_id == "b3r2-grouped-spread":
        prefixes = expand_prefixes(seed_hex, 32)
        return find_pair(prefixes, 32, mask_key_spread)
    if experiment_id == "b3r2-single-group":
        prefixes = expand_prefixes(seed_hex, 1)
        return find_pair(prefixes, 1024, mask_key_single)
    return None, None


def main() -> None:
    request = json.load(sys.stdin)
    exp_id = request.get("experiment_id", "")
    rows = []
    for trial in request["trials"]:
        a_hex, b_hex = run_trial(exp_id, trial["seed"])
        rows.append({
            "trial": trial["trial"],
            "message_a_hex": a_hex,
            "message_b_hex": b_hex,
        })
    json.dump({"schema_version": 1, "trials": rows}, sys.stdout, sort_keys=True)


if __name__ == "__main__":
    main()
