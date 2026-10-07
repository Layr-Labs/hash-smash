"""Scaled grouped birthday on 2-round BLAKE3 (python-message-pairs-v1).

Digests via m15-amortised partial evaluation. Organizer seeds expand to prefixes.
Checked events are digest-xor-mask with N_t^2/2^w = 1 (matched birthday scaling).

Experiments:
  b3r2-grouped-spread      — 32x32, 20-bit mask (lanes o0,o1,o2)
  b3r2-single-group        — 1x256, 16-bit mask (lanes o3,o4); structured stress
  b3r2-grouped-spread-16   — 16x16, 16-bit mask; smaller matched scale
  (the former 64x64 / 24-bit b3r2-grouped-spread-24 was dropped: it ran ~9-11s
  per 256 trials on host, too close to the organizer's 20s Docker timeout.)

Hot-path notes (wall-clock): digests stay bit-identical to the prior program;
message bytes are materialized only on a hit; key is taken from raw output
words without struct.pack. Goal: every config <=6s per 256 trials on host (20s Docker timeout).
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
    return v, (a1, d1, a1c2), mp


def digest_words(m15: int, mid: list, inv: tuple, mp_base: list) -> list:
    """Return 8 digest lanes; mp_base is PERM(m014||0) with slot 14 overwritten."""
    v = mid[:]  # mid is not reused after; still copy for safety across y
    _g_second_half(v, 3, 4, 9, 14, m15)
    mp = mp_base[:]
    mp[14] = m15
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
    return [v[i] ^ v[i + 8] for i in range(8)]


def digest_for(m014: list, m15: int, mid: list, inv: tuple) -> bytes:
    """Public helper retained for bit-exact checks vs prior program."""
    _mid, _inv, mp = group_setup(m014) if inv is None else (mid, inv, None)
    if mp is None:
        m = list(m014) + [0]
        mp = [m[i] for i in PERM]
    out = digest_words(m15, list(mid), inv, mp)
    return struct.pack("<8I", *[x & MASK for x in out])


def message_bytes(m014: list, m15: int) -> bytes:
    return struct.pack("<16I", *(list(m014) + [m15]))


def expand_prefixes(seed_hex: str, n_groups: int) -> list:
    raw = bytes.fromhex(seed_hex)
    out = []
    counter = 0
    while len(out) < n_groups:
        words = []
        while len(words) < 15:
            block = hashlib.sha256(raw + counter.to_bytes(4, "little")).digest()
            counter += 1
            words.extend(struct.unpack("<8I", block))
        out.append(words[:15])
    return out


def key_spread20_words(o: list) -> int:
    return (o[0] & 0xFF) | ((o[1] & 0xFF) << 8) | ((o[2] & 0xF) << 16)


def key_single20_words(o: list) -> int:
    return (o[3] & 0xFF) | ((o[4] & 0xFF) << 8) | ((o[5] & 0xF) << 16)


def key_single16_words(o: list) -> int:
    return (o[3] & 0xFF) | ((o[4] & 0xFF) << 8)


def key_spread16_words(o: list) -> int:
    return (o[0] & 0xFF) | ((o[1] & 0xFF) << 8)


def key_spread24_words(o: list) -> int:
    return (o[0] & 0xFF) | ((o[1] & 0xFF) << 8) | ((o[2] & 0xFF) << 16)


# byte-digest wrappers (tests / external)
def key_spread20(dig: bytes) -> int:
    return key_spread20_words(list(struct.unpack("<8I", dig)))


def key_single20(dig: bytes) -> int:
    return key_single20_words(list(struct.unpack("<8I", dig)))


def key_spread16(dig: bytes) -> int:
    return key_spread16_words(list(struct.unpack("<8I", dig)))


def key_spread24(dig: bytes) -> int:
    return key_spread24_words(list(struct.unpack("<8I", dig)))


def find_pair(prefixes: list, n_y: int, key_fn_words) -> tuple:
    bags: dict = {}
    inserts = 0
    for gi, m014 in enumerate(prefixes):
        mid, inv, mp = group_setup(m014)
        for y in range(n_y):
            out = digest_words(y, mid, inv, mp)
            key = key_fn_words(out)
            inserts += 1
            prev = bags.get(key)
            if prev is not None and prev != (gi, y):
                a = message_bytes(prefixes[prev[0]], prev[1]).hex()
                b = message_bytes(m014, y).hex()
                return a, b, {"messages": inserts, "table_keys": len(bags) + 1}
            bags[key] = (gi, y)
    return None, None, {"messages": inserts, "table_keys": len(bags)}


CONFIGS = {
    "b3r2-grouped-spread": (32, 32, key_spread20_words),
    "b3r2-single-group": (1, 256, key_single16_words),
    "b3r2-grouped-spread-16": (16, 16, key_spread16_words),
}


def run_trial(experiment_id: str, seed_hex: str) -> tuple:
    if experiment_id not in CONFIGS:
        return None, None, {}
    n_g, n_y, key_fn = CONFIGS[experiment_id]
    prefixes = expand_prefixes(seed_hex, n_g)
    a, b, obs = find_pair(prefixes, n_y, key_fn)
    return a, b, obs


def main() -> None:
    request = json.load(sys.stdin)
    exp_id = request.get("experiment_id", "")
    rows = []
    for trial in request["trials"]:
        a_hex, b_hex, obs = run_trial(exp_id, trial["seed"])
        row = {
            "trial": trial["trial"],
            "message_a_hex": a_hex,
            "message_b_hex": b_hex,
        }
        if obs:
            row["observations"] = obs
        rows.append(row)
    json.dump({"schema_version": 1, "trials": rows}, sys.stdout, sort_keys=True)


if __name__ == "__main__":
    main()
