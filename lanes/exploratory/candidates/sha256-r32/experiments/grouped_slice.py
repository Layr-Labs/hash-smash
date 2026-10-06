"""Grouped early-abort evaluator experiment for sha256-r32 (55-byte single block).

A group fixes message words W0..W12 (416 bits). A message in the group appends a 24 bit
value y, so W13 = (y << 8) | 0x80, W14 = 0, W15 = 440 and the message is
W0..W12 (52 bytes) || y (3 bytes). The evaluator below shares rounds 0..12 and the
y-independent schedule words across a group and stops after round 30. It returns the
six reduced state words (A30, A29, A28, E30, E29, E28), which fix digest words
H1, H2, H3, H5, H6, H7 (digest word = IV word + state word). The event mask must lie
inside those six digest words.

Each trial uses one of two layouts, chosen by the number of groups:
  groups = 16, 32 consecutive y values per group (spread layout),
  groups = 1, 512 consecutive y values (single group layout).
512 messages per trial and an 18 bit mask give model success 1 - exp(-1/2) = 0.393.
Only the standard library is used.
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


def R(x, n):
    return ((x >> n) | (x << (32 - n))) & M


def s0(x):
    return R(x, 7) ^ R(x, 18) ^ (x >> 3)


def s1(x):
    return R(x, 17) ^ R(x, 19) ^ (x >> 10)


def S0(x):
    return R(x, 2) ^ R(x, 13) ^ R(x, 22)


def S1(x):
    return R(x, 6) ^ R(x, 11) ^ R(x, 25)


def setup_group(w):
    """Group constants: state after round 12 and every y independent schedule summand."""
    a, b, c, d, e, f, g, h = IV
    for t in range(13):
        t1 = (h + S1(e) + (g ^ (e & (f ^ g))) + K[t] + w[t]) & M
        t2 = (S0(a) + (b ^ ((a ^ b) & (b ^ c)))) & M
        a, b, c, d, e, f, g, h = (t1 + t2) & M, a, b, c, (d + t1) & M, e, f, g
    c16 = (w[0] + s0(w[1]) + w[9] + s1(0)) & M
    c17 = (w[1] + s0(w[2]) + w[10] + s1(440)) & M
    c18 = (w[2] + s0(w[3]) + w[11] + s1(c16)) & M
    c19 = (w[3] + s0(w[4]) + w[12] + s1(c17)) & M
    c21 = (w[5] + s0(w[6]) + 0 + s1(c19)) & M
    c23 = (w[7] + s0(w[8]) + c16 + s1(c21)) & M
    c25 = (w[9] + s0(w[10]) + c18 + s1(c23)) & M
    pre = {
        20: (w[4] + s0(w[5]) + s1(c18)) & M,
        22: (w[6] + s0(w[7]) + 440) & M,
        24: (w[8] + s0(w[9]) + c17) & M,
        26: (w[10] + s0(w[11]) + c19) & M,
        27: (w[11] + s0(w[12]) + s1(c25)) & M,
        28: (w[12] + c21) & M,
        29: 0,
        30: (s0(440) + c23) & M,
    }
    const = {14: 0, 15: 440, 16: c16, 17: c17, 18: c18, 19: c19, 21: c21, 23: c23, 25: c25}
    return (a, b, c, d, e, f, g, h), pre, const


def key_words(group, y):
    state, pre, const = group
    w13 = (y << 8) | 0x80
    w = {13: w13}
    w[20] = (pre[20] + w13) & M
    w[22] = (pre[22] + s1(w[20])) & M
    w[24] = (pre[24] + s1(w[22])) & M
    w[26] = (pre[26] + s1(w[24])) & M
    w[27] = (pre[27] + w[20]) & M
    w[28] = (pre[28] + s0(w13) + s1(w[26])) & M
    w[29] = (pre[29] + w13 + w[22] + s1(w[27])) & M
    w[30] = (pre[30] + s1(w[28])) & M
    a, b, c, d, e, f, g, h = state
    for t in range(13, 31):
        wt = w[t] if t in w else const[t]
        t1 = (h + S1(e) + (g ^ (e & (f ^ g))) + K[t] + wt) & M
        t2 = (S0(a) + (b ^ ((a ^ b) & (b ^ c)))) & M
        a, b, c, d, e, f, g, h = (t1 + t2) & M, a, b, c, (d + t1) & M, e, f, g
    return a, b, c, e, f, g


def digest_prefix(key):
    """Digest words H1, H2, H3, H5, H6, H7 from the key words, as one integer with
    the same bit positions as the 256 bit digest (other words zero)."""
    a30, a29, a28, e30, e29, e28 = key
    words = {1: (IV[1] + a30) & M, 2: (IV[2] + a29) & M, 3: (IV[3] + a28) & M,
             5: (IV[5] + e30) & M, 6: (IV[6] + e29) & M, 7: (IV[7] + e28) & M}
    out = 0
    for index in range(8):
        out = (out << 32) | words.get(index, 0)
    return out


def group_words(seed, g):
    base = bytes.fromhex(seed) + g.to_bytes(4, "big")
    raw = b"".join(hashlib.sha256(base + bytes([j])).digest() for j in range(2))[:52]
    return [int.from_bytes(raw[4 * i:4 * i + 4], "big") for i in range(13)], raw


def run_trial(seed, mask, groups, per_group):
    seen = {}
    for g in range(groups):
        words, raw = group_words(seed, g)
        group = setup_group(words)
        for y in range(per_group):
            value = digest_prefix(key_words(group, y)) & mask
            message = raw + y.to_bytes(3, "big")
            earlier = seen.get(value)
            if earlier is not None and earlier != message:
                return earlier, message
            seen[value] = message
    return None, None


def main():
    request = json.load(sys.stdin)
    mask = int(request["event"]["mask_hex"], 16)
    layout = request["experiment_id"]
    groups, per_group = (16, 32) if layout.endswith("spread") else (1, 512)
    trials = []
    for item in request["trials"]:
        first, second = run_trial(item["seed"], mask, groups, per_group)
        trials.append({
            "trial": item["trial"],
            "message_a_hex": None if first is None else first.hex(),
            "message_b_hex": None if second is None else second.hex(),
            "observations": {"groups": groups, "per_group": per_group},
        })
    json.dump({"schema_version": 1, "trials": trials}, sys.stdout)


if __name__ == "__main__":
    main()
