"""Scaled slice-collision experiment for sha256-r32 (single 55-byte block).

For every requested trial this program draws N = 2^(w/2) pseudo-random
55-byte messages from the trial seed (w = popcount of the event mask),
computes the exact 32-round SHA-256 digest of each, and returns the first
pair of distinct messages whose masked digest bits agree. The host recomputes
the mask event for every returned pair. A trial succeeds with probability
about 1 - exp(-1/2) = 0.393 if the masked slice behaves like a uniform
w-bit value. Only the standard library is used.
"""
import hashlib
import json
import sys

M = 0xFFFFFFFF
K = (
    0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5, 0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5,
    0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3, 0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174,
    0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC, 0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
    0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7, 0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967,
)
IV = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)


def digest32(message: bytes) -> int:
    """Complete FIPS 180-4 SHA-256 truncated to its first 32 rounds, one block."""
    assert len(message) == 55
    block = message + b"\x80" + (440).to_bytes(8, "big")
    w = [int.from_bytes(block[4 * i:4 * i + 4], "big") for i in range(16)]
    for t in range(16, 32):
        x = w[t - 15]
        y = w[t - 2]
        s0 = ((x >> 7) | (x << 25)) ^ ((x >> 18) | (x << 14)) ^ (x >> 3)
        s1 = ((y >> 17) | (y << 15)) ^ ((y >> 19) | (y << 13)) ^ (y >> 10)
        w.append((w[t - 16] + (s0 & M) + w[t - 7] + (s1 & M)) & M)
    a, b, c, d, e, f, g, h = IV
    for t in range(32):
        s1 = ((e >> 6) | (e << 26)) ^ ((e >> 11) | (e << 21)) ^ ((e >> 25) | (e << 7))
        t1 = (h + (s1 & M) + ((e & f) ^ (~e & g)) + K[t] + w[t]) & M
        s0 = ((a >> 2) | (a << 30)) ^ ((a >> 13) | (a << 19)) ^ ((a >> 22) | (a << 10))
        t2 = ((s0 & M) + ((a & b) ^ (a & c) ^ (b & c))) & M
        a, b, c, d, e, f, g, h = (t1 + t2) & M, a, b, c, (d + t1) & M, e, f, g
    out = 0
    for init, word in zip(IV, (a, b, c, d, e, f, g, h)):
        out = (out << 32) | ((init + word) & M)
    return out


def sample(seed: str, index: int) -> bytes:
    base = bytes.fromhex(seed) + index.to_bytes(8, "big")
    return (hashlib.sha256(base + b"\x00").digest() + hashlib.sha256(base + b"\x01").digest())[:55]


def run_trial(seed: str, mask: int, count: int):
    seen = {}
    for index in range(count):
        message = sample(seed, index)
        key = digest32(message) & mask
        earlier = seen.get(key)
        if earlier is not None and earlier != message:
            return earlier, message
        seen[key] = message
    return None, None


def main() -> None:
    request = json.load(sys.stdin)
    event = request["event"]
    mask = int(event["mask_hex"], 16)
    width = bin(mask).count("1")
    count = 1 << (width // 2)
    trials = []
    for item in request["trials"]:
        first, second = run_trial(item["seed"], mask, count)
        trials.append({
            "trial": item["trial"],
            "message_a_hex": None if first is None else first.hex(),
            "message_b_hex": None if second is None else second.hex(),
            "observations": {"samples": count, "mask_bits": width},
        })
    json.dump({"schema_version": 1, "trials": trials}, sys.stdout)


if __name__ == "__main__":
    main()
