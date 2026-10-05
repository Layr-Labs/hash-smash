"""Scaled salted distinguished-point rho walk on 2-round BLAKE3.

Inert judge evidence: a complete scaled copy of the attack in proof.md on a
16-bit point space. Organizer seeds expand to salt and start. The checked
event is digest-xor-mask on the first 16 digest bits.

Fixed parameters (chosen before production runs):
  BITS=16, N=2^16, distinguished iff low 2 bits of the point are 0 (theta=2^-2),
  k'=2^8, g=2^5, k=k'+g, D_max=2^12, gap=2*g.
  Relocation caps match the full-scale claim: fail if lambda>k'; lockstep <=k'.

Disclosed mismatch: g/k' = 2^-3 here versus 2^-88 at full scale.
"""

from __future__ import annotations

import json
import struct
import sys

ROUNDS = 2
BITS = 16
N = 1 << BITS
THETA_BITS = 2
K_PRIME = 1 << (BITS // 2)
G = 1 << 5
K = K_PRIME + G  # matches full-scale k = k' + g (not k' + 2g)
D_MAX = 1 << 12
GAP = 2 * G
MASK16 = 0xFFFF

IV = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
      0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)
PERM = (2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8)
FLAGS = 1 | 2 | 8  # CHUNK_START | CHUNK_END | ROOT
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
    # Sparse embedding (word0=point, word1=salt) — disclosed scale limitation.
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


def seed_words(seed_hex: str) -> tuple[int, int]:
    raw = bytes.fromhex(seed_hex)
    if len(raw) < 32:
        raw = raw.ljust(32, b"\0")
    a = int.from_bytes(raw[0:16], "little")
    b = int.from_bytes(raw[16:32], "little")
    a = (a ^ (a >> 17) ^ 0x9E3779B97F4A7C15) & ((1 << 128) - 1)
    b = (b ^ (b >> 19) ^ 0xBF58476D1CE4E5B9) & ((1 << 128) - 1)
    return a & MASK16, b & MASK16


def run_trial(seed_hex: str):
    salt, x0 = seed_words(seed_hex)
    records = [(x0, 0)]
    x = x0
    for i in range(1, K + 1):
        x = f_map(x, salt)
        if is_dp(x):
            records.append((x, i))
            if len(records) > D_MAX:
                return None, None

    # Sort-and-scan first revisit (matches proof Step 2–3), not first-seen dict order.
    ordered = sorted(records, key=lambda r: (r[0], r[1]))
    collide = None
    for i in range(1, len(ordered)):
        if ordered[i][0] == ordered[i - 1][0]:
            i_star, j_star = ordered[i - 1][1], ordered[i][1]
            if i_star > j_star:
                i_star, j_star = j_star, i_star
            # Prefer the pair with minimal j* among equal values; scan is already
            # ordered by value then index, so the first hit is the earliest j*.
            collide = (i_star, j_star)
            break
    if collide is None:
        return None, None
    i_star, j_star = collide
    if i_star == 0:
        return None, None
    lam = j_star - i_star
    if lam <= 0 or lam > K_PRIME:
        return None, None

    def predecessor(target_idx: int):
        prev = None
        for val, idx in records:
            if idx < target_idx:
                prev = (val, idx)
            elif idx == target_idx:
                return prev
        return prev

    pi = predecessor(i_star)
    pj = predecessor(j_star)
    if pi is None or pj is None:
        return None, None
    if (i_star - pi[1]) > GAP or (j_star - pj[1]) > GAP:
        return None, None

    # Birthday-scale relocation caps matching proof Step 5: lambda<=k', lockstep<=k'.
    a = x0
    b = x0
    for _ in range(lam):
        b = f_map(b, salt)
    for _ in range(K_PRIME):
        na = f_map(a, salt)
        nb = f_map(b, salt)
        if na == nb:
            if a != b:
                ma = message_bytes(a, salt)
                mb = message_bytes(b, salt)
                if ma != mb:
                    return ma.hex(), mb.hex()
            return None, None
        a, b = na, nb
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
