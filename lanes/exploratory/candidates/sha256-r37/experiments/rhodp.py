"""Scaled single-walk distinguished-point search on truncated sha256-r37.

Reads one organizer request (JSON) on stdin and writes one JSON report. Each
trial runs the algorithm of proof.md Section 3 unchanged except for its width.
The walk state is an n-bit value x (n <= 16) and the iteration is

    g(x) = top n bits of H37(enc(x) || R),

where H37 is the complete 37-round SHA-256 target (standard IV, FIPS 180-4
padding, feed-forward) on a 48-byte message. As in the full attack, R is a
fresh 16-byte suffix per trial, so each trial walks its own map of the family.
enc(x) = TEMPLATE XOR spread(x) is 32 bytes: bit i of x flips bit (i // 8) of
big-endian message word (i % 8). TEMPLATE, R and the start point are derived
from the organizer trial seed. The walk budget is k = (65/64) * 2^(n/2), the
full attack's ratio to sqrt(2^n); the walk is cut off at k itself rather than
the full rule's k + L, so every success here is also a success of the full rule
on the same coins. A returned pair has distinct messages whose full digests
agree on the top n bits; the organizer recomputes that digest-xor-mask event.
Only the standard library is used; no OS randomness, clock or environment.
"""

import hashlib
import json
import sys

M32 = 0xFFFFFFFF
K37 = (
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354,
)
IV = (0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19)

# SPREAD[v][j] is bit j of the byte v; byte b of x lands at bit b of word j.
SPREAD = tuple(tuple(v >> j & 1 for j in range(8)) for v in range(256))

# experiment id -> (width n <= 16, DP bits d, run bound L, table capacity K)
PARAMS = {
    "rhodp-n12": (12, 1, 32, 256),
    "rhodp-n14": (14, 1, 32, 256),
    "rhodp-n16": (16, 2, 64, 512),
}


def h37(words16):
    """sha256-r37 compression of one padded block from the standard IV, with feed-forward."""
    w = list(words16)
    for i in range(16, 37):
        x, y = w[i - 15], w[i - 2]
        s0 = ((x >> 7 | x << 25) ^ (x >> 18 | x << 14) ^ (x >> 3)) & M32
        s1 = ((y >> 17 | y << 15) ^ (y >> 19 | y << 13) ^ (y >> 10)) & M32
        w.append((w[i - 16] + s0 + w[i - 7] + s1) & M32)
    a, b, c, d, e, f, g, h = IV
    for i in range(37):
        s1 = ((e >> 6 | e << 26) ^ (e >> 11 | e << 21) ^ (e >> 25 | e << 7)) & M32
        t1 = (h + s1 + ((e & f) ^ (~e & g)) + K37[i] + w[i]) & M32
        s0 = ((a >> 2 | a << 30) ^ (a >> 13 | a << 19) ^ (a >> 22 | a << 10)) & M32
        t2 = s0 + ((a & b) ^ (a & c) ^ (b & c))
        a, b, c, d, e, f, g, h = (t1 + t2) & M32, a, b, c, (d + t1) & M32, e, f, g
    return [(iv + v) & M32 for iv, v in zip(IV, (a, b, c, d, e, f, g, h))]


class Walk:
    def __init__(self, seed_hex, n):
        material = hashlib.shake_256(b"hashsmash-r37-rhodp-v2" + bytes.fromhex(seed_hex)).digest(56)
        words = [int.from_bytes(material[4 * j:4 * j + 4], "big") for j in range(12)]
        self.template, self.suffix = words[:8], words[8:12]
        # Padded block words 8..15 of a 48-byte message: R, 0x80 byte, zeros, bit length 384.
        self.tail = self.suffix + [0x80000000, 0, 0, 384]
        self.start = int.from_bytes(material[48:56], "big") & ((1 << n) - 1)
        self.n = n
        self.calls = 0

    def message_words(self, x):
        lo, hi = SPREAD[x & 0xFF], SPREAD[x >> 8 & 0xFF]
        return [t ^ a ^ b << 1 for t, a, b in zip(self.template, lo, hi)]

    def message_hex(self, x):
        return b"".join(v.to_bytes(4, "big") for v in self.message_words(x) + self.suffix).hex()

    def g(self, x):
        self.calls += 1
        return h37(self.message_words(x) + self.tail)[0] >> (32 - self.n)

    def advance(self, x, steps):
        for _ in range(steps):
            x = self.g(x)
        return x


def trial(seed_hex, n, d, run_bound, capacity):
    walk = Walk(seed_hex, n)
    tcap = 65 * (1 << (n // 2)) // 64
    table, position = [], {}          # (value, index) in index order; value -> slot
    x, t, hit = walk.start, 0, None
    while True:
        if x >> (n - d) == 0:          # distinguished: top d of n bits are zero
            hit = position.get(x)
            if hit is not None:
                break
            if len(table) == capacity:
                return None, {"failure_code": 2, "walk_steps": t}
            position[x] = len(table)
            table.append((x, t))
        if t == tcap:
            return None, {"failure_code": 1, "walk_steps": t}
        x, t = walk.g(x), t + 1
    s = table[hit][1]
    lam = t - s
    if hit > 0:
        vp, sp = table[hit - 1]
    else:
        vp, sp = walk.start, 0          # anchor: the start point at index 0
    tau = sp + lam
    if tau >= s:
        j = hit
        while j + 1 < len(table) and table[j + 1][1] <= tau:
            j += 1
        prep, base = tau - table[j][1], table[j][0]
    else:
        prep, base = lam, vp
    if prep > 2 * run_bound:
        return None, {"failure_code": 3, "walk_steps": t}
    a, b = vp, walk.advance(base, prep)
    if a == b:
        return None, {"failure_code": 4, "walk_steps": t}
    for q in range(run_bound):
        fa, fb = walk.g(a), walk.g(b)
        if fa == fb:
            return (walk.message_hex(a), walk.message_hex(b)), {
                "failure_code": 0, "walk_steps": t, "cycle_length": lam,
                "tail_upper": s, "lockstep_iterations": q + 1,
                "target_calls": walk.calls, "dp_stored": len(table)}
        a, b = fa, fb
    return None, {"failure_code": 5, "walk_steps": t}


def main():
    request = json.loads(sys.stdin.read())
    n, d, run_bound, capacity = PARAMS[request["experiment_id"]]
    rows = []
    for item in request["trials"]:
        pair, observations = trial(item["seed"], n, d, run_bound, capacity)
        a, b = pair if pair is not None else (None, None)
        rows.append({"trial": item["trial"], "message_a_hex": a, "message_b_hex": b,
                     "observations": observations})
    sys.stdout.write(json.dumps({"schema_version": 1, "trials": rows}, sort_keys=True))


if __name__ == "__main__":
    main()
