"""Scaled replay of the grouped 2-round BLAKE3 birthday search.

Each trial runs the submitted algorithm's exact evaluation path at a reduced
output width. Messages are single 64-byte blocks: words m0..m14 form a group
prefix drawn from the trial seed, and the inner variable is y = m15. Digests are
computed only by the grouped partial evaluator below (group setup once, then the
247-operation inner body per y), never by a full reference compression, so the
organizer's independent digest check also validates that evaluator.

Experiment ids select the structure:
  b3r2-grouped-spread : 32 groups x 32 consecutive y values (y = 0..31)
  b3r2-single-group   : 1 group x 1024 consecutive y values (y = 0..1023)
Both use N_t = 1024 = 2^(w/2) samples for a w = 20-bit masked event, the exact
scaled analogue of N = 2^128 = 2^(256/2) in the full attack. Under the
random-function model a trial succeeds with probability
1 - prod_{i<1024}(1 - i/2^20) = 0.39327...
All N_t samples are evaluated. The first masked match (in evaluation order) is
returned, otherwise both messages are null; the untrusted observations report
its 1-based sample index (0 if none) and the number of masked-equal pairs among
all N_t samples (expected C(1024,2)/2^20 = 0.4995 per trial at random).
"""

import hashlib
import json
import struct
import sys

IV = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
      0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)
M = 0xFFFFFFFF
SAMPLES = 1024
LAYOUT = {"b3r2-grouped-spread": (32, 32), "b3r2-single-group": (1, 1024)}


def ror(x, r):
    return ((x >> r) | (x << (32 - r))) & M


def G(v, a, b, c, d, x, y):
    v[a] = (v[a] + v[b] + x) & M
    v[d] = ror(v[d] ^ v[a], 16)
    v[c] = (v[c] + v[d]) & M
    v[b] = ror(v[b] ^ v[c], 12)
    v[a] = (v[a] + v[b] + y) & M
    v[d] = ror(v[d] ^ v[a], 8)
    v[c] = (v[c] + v[d]) & M
    v[b] = ror(v[b] ^ v[c], 7)


def setup(m):
    """Group-invariant work for prefix words m[0..14] (flags 11, len 64, counter 0)."""
    v = list(IV) + list(IV[:4]) + [0, 0, 64, 11]
    G(v, 0, 4, 8, 12, m[0], m[1]); G(v, 1, 5, 9, 13, m[2], m[3])
    G(v, 2, 6, 10, 14, m[4], m[5]); G(v, 3, 7, 11, 15, m[6], m[7])
    G(v, 0, 5, 10, 15, m[8], m[9]); G(v, 1, 6, 11, 12, m[10], m[11])
    G(v, 2, 7, 8, 13, m[12], m[13])
    a1 = (v[3] + v[4] + m[14]) & M          # diagonal 3, first half (x = m14)
    d1 = ror(v[14] ^ a1, 16)
    c1 = (v[9] + d1) & M
    b1 = ror(v[4] ^ c1, 12)
    col1_a = (v[1] + v[5] + m[3]) & M        # round-2 column 1: only c varies
    col1_d = ror(v[13] ^ col1_a, 16)
    col2_a = (v[2] + v[6] + m[7]) & M        # round-2 column 2: only d varies
    return (a1 + b1, d1, c1, b1,
            v[0] + m[2], v[12], v[8], m[6],
            col1_d, col1_a + m[10], v[5],
            col2_a, col2_a + m[0], v[10], v[6],
            v[7] + m[4], v[15], v[11], v[7], m[13],
            m[1], m[11], m[12], m[5], m[9], m[14], m[8])


def inner(p, y):
    """Digest words o0..o7 for message (prefix, m15 = y)."""
    (AB, D1, C1, B1, P0, v12, v8, m6, d1_1, Q1, v5, a1_2, Q2, v10, v6,
     P3, v15, v11, v7, m13, m1, m11, m12, m5, m9, m14, m8) = p
    a3 = (AB + y) & M                        # diagonal 3, second half (y = m15)
    d14 = ror(D1 ^ a3, 8)
    c9 = (C1 + d14) & M
    b4 = ror(B1 ^ c9, 7)
    v = [0] * 16
    a = (P0 + b4) & M                        # column 0 (m2, m6)
    d = ror(v12 ^ a, 16); c = (v8 + d) & M; b = ror(b4 ^ c, 12)
    a = (a + b + m6) & M; d = ror(d ^ a, 8); c = (c + d) & M; b = ror(b ^ c, 7)
    v[0], v[4], v[8], v[12] = a, b, c, d
    c = (c9 + d1_1) & M                      # column 1 (m3, m10)
    b = ror(v5 ^ c, 12); a = (Q1 + b) & M
    d = ror(d1_1 ^ a, 8); c = (c + d) & M; b = ror(b ^ c, 7)
    v[1], v[5], v[9], v[13] = a, b, c, d
    d = ror(d14 ^ a1_2, 16)                  # column 2 (m7, m0)
    c = (v10 + d) & M; b = ror(v6 ^ c, 12); a = (Q2 + b) & M
    d = ror(d ^ a, 8); c = (c + d) & M; b = ror(b ^ c, 7)
    v[2], v[6], v[10], v[14] = a, b, c, d
    a = (a3 + P3) & M                        # column 3 (m4, m13)
    d = ror(v15 ^ a, 16); c = (v11 + d) & M; b = ror(v7 ^ c, 12)
    a = (a + b + m13) & M; d = ror(d ^ a, 8); c = (c + d) & M; b = ror(b ^ c, 7)
    v[3], v[7], v[11], v[15] = a, b, c, d
    G(v, 0, 5, 10, 15, m1, m11)              # round-2 diagonals
    G(v, 1, 6, 11, 12, m12, m5)
    G(v, 2, 7, 8, 13, m9, m14)
    G(v, 3, 4, 9, 14, y, m8)
    return [v[i] ^ v[i + 8] for i in range(8)]


def prefix(seed, group):
    data = hashlib.shake_256(b"b3r2-grouped-prefix|" + seed + struct.pack("<I", group)).digest(60)
    return list(struct.unpack("<15I", data))


def trial(seed, groups, per_group, mask_words):
    """Return the first masked match and the number of masked-equal pairs."""
    seen = {}
    first = (None, None, 0)
    pairs = 0
    for g in range(groups):
        words = prefix(seed, g)
        p = setup(words)
        for y in range(per_group):
            o = inner(p, y)
            key = tuple(o[i] & mask_words[i] for i in range(8))
            message = struct.pack("<16I", *words, y)
            bucket = seen.setdefault(key, [])
            if bucket and first[0] is None:
                first = (bucket[0].hex(), message.hex(), g * per_group + y + 1)
            pairs += len(bucket)
            bucket.append(message)
    return first[0], first[1], first[2], pairs


def main():
    request = json.loads(sys.stdin.read())
    groups, per_group = LAYOUT[request["experiment_id"]]
    assert groups * per_group == SAMPLES
    mask = bytes.fromhex(request["event"]["mask_hex"])
    mask_words = struct.unpack("<8I", mask)
    out = []
    for item in request["trials"]:
        a, b, first_index, pairs = trial(bytes.fromhex(item["seed"]), groups, per_group, mask_words)
        out.append({"trial": item["trial"], "message_a_hex": a, "message_b_hex": b,
                    "observations": {"first_match_sample": first_index, "masked_pairs": pairs}})
    sys.stdout.write(json.dumps({"schema_version": 1, "trials": out}, separators=(",", ":")))


if __name__ == "__main__":
    main()
