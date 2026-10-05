"""Half-collisions of 2-round BLAKE3 and a small residual search.

Implements the constructions of proof.md for blake3-r2-prefix-v1. The
organizer request is read from stdin and one message pair is returned per
trial: a 60-byte message A and a 62-byte message B. Only the standard library
is used; there is no OS randomness, wall time or ambient state. The program
never calls a hash library: it evaluates the BLAKE3 quarter-round G directly,
and the organizer runner recomputes both complete digests.

Experiment "half-collision": steps S1-S3 of proof.md Section 4 for nine state
words taken from the seed. The proof predicts that digest words 0, 2, 5, 7 of
A and B are equal for every seed.

Experiment "residual-search": the search of proof.md Section 6 at toy scale.
For one context and one alpha taken from the seed it tries gamma = g0, g0+1,
... (at most LIMIT values) and returns the first pair whose residual has a zero
low byte in digest word 1, so that 136 digest bits agree. The number of
values tried is reported as an untrusted observation.
"""

import hashlib
import json
import struct
import sys

MASK = 0xFFFFFFFF
IV = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
      0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)
K = (IV[2] + IV[6]) & MASK
LEN_A, LEN_B = 60, 62
# The pinned round-1 column call C3 = G(3,7,11,15; w4, w13) of proof.md Section 3.
X3, X7, X11, X15 = 0x38C3F8FD, 0xDF3C0829, 0xF910A0E9, 0x16F60E91
W4, W13 = 0xE7FFFED8, 0x716F0D2F
W4B = (((W4 + K) & MASK) ^ LEN_A ^ LEN_B) - K & MASK
DELTA5 = (W4 - W4B) & MASK
FREE = (1, 2, 5, 6, 9, 10, 12, 13, 14)
LIMIT = 8192


def ror(v, n):
    return ((v >> n) | (v << (32 - n))) & MASK


def rol(v, n):
    return ((v << n) | (v >> (32 - n))) & MASK


def g(a, b, c, d, x, y):
    a = (a + b + x) & MASK; d = ror(d ^ a, 16); c = (c + d) & MASK; b = ror(b ^ c, 12)
    a = (a + b + y) & MASK; d = ror(d ^ a, 8); c = (c + d) & MASK; b = ror(b ^ c, 7)
    return a, b, c, d


def column_inverse(j, sb, sc, d0):
    """Round-0 column call j from its b and c outputs: returns (a out, d out, x, y)."""
    a0, b0, c0 = IV[j], IV[4 + j], IV[j]
    b1 = rol(sb, 7) ^ sc
    c1 = rol(b1, 12) ^ b0
    sd = (sc - c1) & MASK
    d1 = (c1 - c0) & MASK
    a1 = rol(d1, 16) ^ d0
    return rol(sd, 8) ^ d1, sd, (a1 - a0 - b0) & MASK, (rol(sd, 8) ^ d1) - a1 - b1 & MASK


def context(free):
    """Steps S1-S3: message words w, state X after round 0, state S after its column step."""
    X, S, w = [0] * 16, [0] * 16, [0] * 16
    for i, v in zip(FREE, free):
        X[i] = v
    X[3], X[7], X[11], X[15] = X3, X7, X11, X15
    w[4], w[13], w[15] = W4, W13, 0
    a1_c2 = (W4 + K) & MASK
    d1_c2 = ror(a1_c2 ^ LEN_A, 16)
    c1_c2 = (d1_c2 + IV[2]) & MASK
    b1_c2 = ror(c1_c2 ^ IV[6], 12)
    # D1 = G(1,6,11,12; w10, w11)
    b1_d1 = rol(X[6], 7) ^ X[11]
    c1_d1 = (X[11] - X[12]) & MASK
    d1_d1 = rol(X[12], 8) ^ X[1]
    S[6] = rol(b1_d1, 12) ^ c1_d1
    S[11] = (c1_d1 - d1_d1) & MASK
    S[10] = b1_c2 ^ rol(S[6], 7)
    # D0 = G(0,5,10,15; w8, w9); X0 is derived
    b1_d0 = rol(X[5], 7) ^ X[10]
    c1_d0 = (X[10] - X[15]) & MASK
    S[5] = rol(b1_d0, 12) ^ c1_d0
    d1_d0 = (c1_d0 - S[10]) & MASK
    X[0] = d1_d0 ^ rol(X[15], 8)
    # round-0 column call 2
    S[14] = (S[10] - c1_c2) & MASK
    S[2] = rol(S[14], 8) ^ d1_c2
    w[5] = (S[2] - a1_c2 - b1_c2) & MASK
    # D3 = G(3,4,9,14; w14, w15); X4 is derived
    d1_d3 = rol(X[14], 8) ^ X[3]
    a1_d3 = rol(d1_d3, 16) ^ S[14]
    b1_d3 = (X[3] - a1_d3 - w[15]) & MASK
    X[4] = ror(b1_d3 ^ X[9], 7)
    c1_d3 = (X[9] - X[14]) & MASK
    S[4] = rol(b1_d3, 12) ^ c1_d3
    S[9] = (c1_d3 - d1_d3) & MASK
    S[1], S[13], w[2], w[3] = column_inverse(1, S[5], S[9], 0)
    # D2 = G(2,7,8,13; w12, w13); X8 is derived
    d1_d2 = rol(X[13], 8) ^ X[2]
    a1_d2 = rol(d1_d2, 16) ^ S[13]
    b1_d2 = (X[2] - a1_d2 - w[13]) & MASK
    X[8] = b1_d2 ^ rol(X[7], 7)
    c1_d2 = (X[8] - X[13]) & MASK
    S[7] = rol(b1_d2, 12) ^ c1_d2
    S[8] = (c1_d2 - d1_d2) & MASK
    w[12] = (a1_d2 - S[2] - S[7]) & MASK
    S[0], S[12], w[0], w[1] = column_inverse(0, S[4], S[8], 0)
    S[3], S[15], w[6], w[7] = column_inverse(3, S[7], S[11], 11)
    a1_d0 = rol(d1_d0, 16) ^ S[15]
    w[8] = (a1_d0 - S[0] - S[5]) & MASK
    w[9] = (X[0] - a1_d0 - b1_d0) & MASK
    a1_d1 = rol(d1_d1, 16) ^ S[12]
    w[10] = (a1_d1 - S[1] - S[6]) & MASK
    w[11] = (X[1] - a1_d1 - b1_d1) & MASK
    w[14] = (a1_d3 - S[3] - S[4]) & MASK
    return X, S, w


def messages(w):
    other = list(w)
    other[4] = W4B
    other[5] = (w[5] + DELTA5) & MASK
    return struct.pack("<16I", *w)[:LEN_A], struct.pack("<16I", *other)[:LEN_B]


def d0_family(S, alpha):
    """Words (w8, w9) of D0 giving c output alpha and d output X15: returns X0, X5, w8, w9."""
    c1 = (alpha - X15) & MASK
    d1 = (c1 - S[10]) & MASK
    x0 = rol(X15, 8) ^ d1
    b1 = ror(S[5] ^ c1, 12)
    a1 = rol(d1, 16) ^ S[15]
    return x0, ror(b1 ^ alpha, 7), (a1 - S[0] - S[5]) & MASK, (x0 - a1 - b1) & MASK


def d1_family(S, gamma):
    """Words (w10, w11) of D1 with first-half c value gamma and c output X11: returns X1, X6, X12, w10, w11."""
    x12 = (X11 - gamma) & MASK
    d1 = (gamma - S[11]) & MASK
    x1 = rol(x12, 8) ^ d1
    b1 = ror(S[6] ^ gamma, 12)
    a1 = rol(d1, 16) ^ S[12]
    return x1, ror(b1 ^ X11, 7), x12, (a1 - S[1] - S[6]) & MASK, (x1 - a1 - b1) & MASK


def residual_word1(X, w, x0, x5, alpha, w8, x1, x6, x12, w10, pinned):
    """Digest word 1 of A xor digest word 1 of B for one trial (round 1, partial)."""
    y3, y3b, y11, y11b = pinned
    c0 = g(x0, X[4], X[8], x12, w[2], w[6])
    c1 = g(x1, x5, X[9], X[13], w[3], w10)
    c2 = g(X[2], x6, alpha, X[14], w[7], w[0])
    y4, y12, y1, y9, y6, y14 = c0[1], c0[3], c1[0], c1[2], c2[1], c2[3]
    w5b = (w[5] + DELTA5) & MASK
    pa = g(y1, y6, y11, y12, w[12], w[5])
    pb = g(y1, y6, y11b, y12, w[12], w5b)
    qa = g(y3, y4, y9, y14, w[15], w8)
    qb = g(y3b, y4, y9, y14, w[15], w8)
    return pa[0] ^ qa[2] ^ pb[0] ^ qb[2]


def half_collision(seed):
    free = struct.unpack("<9I", hashlib.shake_256(seed).digest(36))
    _, _, w = context(free)
    return messages(w) + ({},)


def residual_search(seed):
    stream = struct.unpack("<11I", hashlib.shake_256(seed).digest(44))
    X, S, w = context(stream[:9])
    alpha, gamma0 = stream[9], stream[10]
    ca = g(X3, X7, X11, X15, W4, W13)
    cb = g(X3, X7, X11, X15, W4B, W13)
    pinned = (ca[0], cb[0], ca[2], cb[2])
    x0, x5, w8, w9 = d0_family(S, alpha)
    for step in range(LIMIT):
        x1, x6, x12, w10, w11 = d1_family(S, (gamma0 + step) & MASK)
        if residual_word1(X, w, x0, x5, alpha, w8, x1, x6, x12, w10, pinned) & 0xFF == 0:
            words = list(w)
            words[8], words[9], words[10], words[11] = w8, w9, w10, w11
            return messages(words) + ({"tries": step + 1},)
    return None, None, {"tries": LIMIT}


def main():
    request = json.load(sys.stdin)
    if request["schema_version"] != 1 or request["target_profile"] != "blake3-r2-prefix-v1":
        raise ValueError("unexpected organizer target")
    if request["event"].get("kind") != "digest-xor-mask":
        raise ValueError("unexpected organizer event")
    run = {"half-collision": half_collision, "residual-search": residual_search}[request["experiment_id"]]
    trials = []
    for trial in request["trials"]:
        first, second, observations = run(bytes.fromhex(trial["seed"]))
        row = {"trial": trial["trial"],
               "message_a_hex": None if first is None else first.hex(),
               "message_b_hex": None if second is None else second.hex()}
        if observations:
            row["observations"] = observations
        trials.append(row)
    json.dump({"schema_version": 1, "trials": trials}, sys.stdout, separators=(",", ":"), sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
