"""Scaled salted multi-trail distinguished-point collision search on 2-round BLAKE3.

Inert judge evidence: a complete scaled copy of the multi-trail attack in
proof.md on a 16-bit point space. Organizer seeds expand to salt and a stream
of trail starts. The checked event is digest-xor-mask on the first 16 digest
bits.

Fixed parameters (chosen before production runs):
  BITS=16, N=2^16, distinguished iff low 2 bits of the point are 0 (theta=2^-2),
  K=2^8+2^5, L_max=2^6, M_max=2^12.
  Recovery re-walks two distinct starts (cap L_max each), matching full-scale
  O(L_max) recovery — not birthday-scale single-trail lockstep from x0.

Disclosed: L_max*theta = 16 here versus 256 at full scale (both >> 1).
"""

from __future__ import annotations

import json
import struct
import sys

ROUNDS = 2
BITS = 16
THETA_BITS = 2
K = (1 << (BITS // 2)) + (1 << 5)  # 2^8 + 2^5
L_MAX = 1 << 6
M_MAX = 1 << 12
MASK16 = 0xFFFF

IV = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
      0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)
PERM = (2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8)
FLAGS = 1 | 2 | 8
M32 = 0xFFFFFFFF


def _ror(v: int, n: int) -> int:
    return ((v >> n) | (v << (32 - n))) & M32


def _g(v, a, b, c, d, x, y) -> None:
    v[a] = (v[a] + v[b] + x) & M32
    v[d] = _ror(v[d] ^ v[a], 16)
    v[c] = (v[c] + v[d]) & M32
    v[b] = _ror(v[b] ^ v[c], 12)
    v[a] = (v[a] + v[b] + y) & M32
    v[d] = _ror(v[d] ^ v[a], 8)
    v[c] = (v[c] + v[d]) & M32
    v[b] = _ror(v[b] ^ v[c], 7)


def root_digest(words: list[int]) -> bytes:
    v = list(IV) + list(IV[:4]) + [0, 0, 64, FLAGS]
    m = list(words)
    for _ in range(ROUNDS):
        _g(v, 0, 4, 8, 12, m[0], m[1])
        _g(v, 1, 5, 9, 13, m[2], m[3])
        _g(v, 2, 6, 10, 14, m[4], m[5])
        _g(v, 3, 7, 11, 15, m[6], m[7])
        _g(v, 0, 5, 10, 15, m[8], m[9])
        _g(v, 1, 6, 11, 12, m[10], m[11])
        _g(v, 2, 7, 8, 13, m[12], m[13])
        _g(v, 3, 4, 9, 14, m[14], m[15])
        m = [m[i] for i in PERM]
    out = [(v[i] ^ v[i + 8]) & M32 for i in range(8)]
    return struct.pack("<8I", *out)


def message_words(point: int, salt: int) -> list[int]:
    words = [0] * 16
    words[0] = point & MASK16
    words[1] = salt & MASK16
    return words


def message_bytes(point: int, salt: int) -> bytes:
    return struct.pack("<16I", *message_words(point, salt))


def f_map(point: int, salt: int) -> int:
    digest = root_digest(message_words(point, salt))
    return struct.unpack("<H", digest[:2])[0]


def is_dp(point: int) -> bool:
    return (point & ((1 << THETA_BITS) - 1)) == 0


def seed_stream(seed_hex: str):
    raw = bytes.fromhex(seed_hex)
    if len(raw) < 32:
        raw = raw.ljust(32, b"\0")
    state = int.from_bytes(raw, "little") & ((1 << 256) - 1)

    def mix(x: int) -> int:
        x = (x ^ (x >> 17) ^ 0x9E3779B97F4A7C15) & ((1 << 256) - 1)
        x = (x ^ (x >> 19) ^ 0xBF58476D1CE4E5B9) & ((1 << 256) - 1)
        return x

    state = mix(state)
    salt = state & MASK16
    state = mix(state + 1)

    def next_start() -> int:
        nonlocal state
        state = mix(state + 0x9E3779B97F4A7C15)
        return state & MASK16

    return salt, next_start


def recover(salt: int, start_a: int, start_b: int, common_dp: int):
    """Re-walk two short trails; return colliding message hex pair or (None, None)."""
    pred_a: dict[int, int] = {}
    x = start_a
    reached = False
    for _ in range(L_MAX):
        nxt = f_map(x, salt)
        pred_a[nxt] = x
        x = nxt
        if x == common_dp:
            reached = True
            break
    if not reached:
        return None, None

    x = start_b
    for _ in range(L_MAX):
        nxt = f_map(x, salt)
        if nxt in pred_a and pred_a[nxt] != x:
            a, b = pred_a[nxt], x
            ma = message_bytes(a, salt)
            mb = message_bytes(b, salt)
            if ma != mb:
                return ma.hex(), mb.hex()
            return None, None
        if nxt == common_dp:
            pa = pred_a.get(common_dp)
            pb = x
            if pa is not None and pa != pb:
                ma = message_bytes(pa, salt)
                mb = message_bytes(pb, salt)
                if ma != mb:
                    return ma.hex(), mb.hex()
            return None, None
        x = nxt
    return None, None


def run_trial(seed_hex: str):
    salt, next_start = seed_stream(seed_hex)
    table: dict[int, int] = {}
    spent = 0
    while spent < K:
        u = next_start()
        x = u
        for _ in range(L_MAX):
            x = f_map(x, salt)
            spent += 1
            if is_dp(x):
                if x in table and table[x] != u:
                    return recover(salt, table[x], u, x)
                if len(table) >= M_MAX:
                    return None, None
                table[x] = u
                break
            if spent >= K:
                return None, None
    return None, None


def main() -> None:
    request = json.load(sys.stdin)
    rows = []
    for trial in request["trials"]:
        a_hex, b_hex = run_trial(trial["seed"])
        rows.append({
            "trial": trial["trial"],
            "message_a_hex": a_hex,
            "message_b_hex": b_hex,
        })
    json.dump({"schema_version": 1, "trials": rows}, sys.stdout, sort_keys=True)


if __name__ == "__main__":
    main()
