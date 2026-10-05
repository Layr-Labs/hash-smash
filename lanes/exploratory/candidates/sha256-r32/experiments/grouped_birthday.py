"""Scaled replay of the grouped 32-round SHA-256 birthday search.

Messages are 55 bytes, so each is one padded block: words W0..W12 form a group
prefix drawn from the trial seed, W13 = (u << 8) | 0x80 carries the 24-bit
inner variable u, W14 = 0 and W15 = 440 are padding. Digest words are computed
only by the grouped partial evaluator below: group setup once, then the
708-operation inner body per u (rounds 13..30). It returns the six digest
words H1, H2, H3, H5, H6, H7 (state after round 30 plus the IV; H0 and H4 need
round 31 and are not computed). The organizer's independent digest check of
every returned pair therefore also validates this evaluator. Masks select bits
of these six words only.

The inner body uses three standard software identities that lower its counted
word-operation cost without changing any computed value (proof.md Section 4):
rotations inside S0, S1, s0, s1 are left unmasked because they feed only into
modular additions whose results are masked; Ch is g ^ (e & (f ^ g)); and Maj
is b ^ ((a ^ b) & (b ^ c)) with (b ^ c) carried from the previous round's
(a ^ b). Every value produced equals the reference digest word, which the
organizer re-checks.

Experiment ids select the structure:
  s256-grouped-spread : 16 groups x 32 consecutive u values (u = 0..31)
  s256-single-group   : 1 group x 512 consecutive u values (u = 0..511)
Both use N_t = 512 = 2^(w/2) samples for a w = 18-bit masked event, the
scaled analogue of N = 2^128 = 2^(256/2). Under the random-function model a
trial succeeds with probability 1 - prod_{i<512}(1 - i/2^18) = 0.39307...
All N_t samples are evaluated. The first masked match is returned (else two
nulls); untrusted observations report its 1-based sample index (0 if none) and
the number of masked-equal pairs (expected 0.4990 per trial at random).
"""

import hashlib
import json
import struct
import sys

M = 0xFFFFFFFF
IV = (0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
      0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19)
K = (0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
     0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
     0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
     0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967)
SAMPLES = 512
LAYOUT = {"s256-grouped-spread": (16, 32), "s256-single-group": (1, 512)}


def rorm(x, r):
    return ((x >> r) | (x << (32 - r))) & M


def roru(x, r):                       # unmasked rotation (clean low 32 bits)
    return (x >> r) | (x << (32 - r))


def S0(a): return roru(a, 2) ^ roru(a, 13) ^ roru(a, 22)
def S1(e): return roru(e, 6) ^ roru(e, 11) ^ roru(e, 25)
def s0(x): return roru(x, 7) ^ roru(x, 18) ^ (x >> 3)
def s1(x): return roru(x, 17) ^ roru(x, 19) ^ (x >> 10)
def ch(e, f, g): return g ^ (e & (f ^ g))


def setup(w):
    """w: prefix words W0..W12. Group-invariant work (masked reference form)."""
    ws = dict(enumerate(w))
    ws[14], ws[15] = 0, 440
    a, b, c, d, e, f, g, h = IV
    for i in range(13):                               # rounds 0..12 (masked reference)
        t1 = (h + (rorm(e, 6) ^ rorm(e, 11) ^ rorm(e, 25)) + ((e & f) ^ (~e & g)) + ws[i] + K[i]) & M
        t2 = (rorm(a, 2) ^ rorm(a, 13) ^ rorm(a, 22)) + ((a & b) ^ (a & c) ^ (b & c))
        a, b, c, d, e, f, g, h = (t1 + t2) & M, a, b, c, (d + t1) & M, e, f, g
    for t in (16, 17, 18, 19, 21, 23, 25):            # independent of W13
        ws[t] = (s1(ws[t - 2]) + ws[t - 7] + s0(ws[t - 15]) + ws[t - 16]) & M
    T13 = h + (rorm(e, 6) ^ rorm(e, 11) ^ rorm(e, 25)) + ((e & f) ^ (~e & g)) + K[13]
    A13 = T13 + (rorm(a, 2) ^ rorm(a, 13) ^ rorm(a, 22)) + ((a & b) ^ (a & c) ^ (b & c))
    return (A13, d + T13, a, b, c, e, f, g,
            a | b, a & b,
            tuple(ws[t] + K[t] for t in (14, 15, 16, 17, 18, 19, 21, 23, 25)),
            (s1(ws[18]) + s0(ws[5]) + ws[4]) & M,     # P20: W20 = (P20 + W13) & M
            (ws[15] + s0(ws[7]) + ws[6]) & M,         # P22
            (ws[17] + s0(ws[9]) + ws[8]) & M,         # P24
            (ws[19] + s0(ws[11]) + ws[10]) & M,       # P26
            (s1(ws[25]) + s0(ws[12]) + ws[11]) & M,   # P27
            (ws[21] + ws[12]) & M,                    # P28
            s0(ws[14]) & M,                           # P29
            (ws[23] + s0(ws[15]) + ws[14]) & M)       # P30


def rnd(st, kw, bxc):
    """Reduced round. Returns (new state, a ^ b) for the carried Maj term."""
    a, b, c, d, e, f, g, h = st
    t1 = h + S1(e) + ch(e, f, g) + kw
    axb = a ^ b
    mj = b ^ (axb & bxc)                              # Maj via carried (b ^ c) = bxc
    t2 = S0(a) + mj
    return ((t1 + t2) & M, a, b, c, (d + t1) & M, e, f, g), axb


def inner(p, u):
    """State words (A30, A29, A28, E30, E29, E28) after round 30, 708 ops."""
    (A13, D13, a12, b12, c12, e12, f12, g12, bc14, band14, kw,
     P20, P22, P24, P26, P27, P28, P29, P30) = p
    kw14, kw15, kw16, kw17, kw18, kw19, kw21, kw23, kw25 = kw
    w13 = (u << 8) | 0x80
    a14 = (A13 + w13) & M                              # round 13 (4 ops)
    e14 = (D13 + w13) & M
    t1 = g12 + S1(e14) + ch(e14, e12, f12) + kw14      # round 14, Maj via precomputed b|c, b&c
    t2 = S0(a14) + ((a14 & bc14) | band14)
    st = ((t1 + t2) & M, a14, a12, b12, (c12 + t1) & M, e14, e12, f12)
    bxc = st[1] ^ st[2]                                # (b ^ c) for round 15
    for k in (kw15, kw16, kw17, kw18, kw19):           # rounds 15..19
        st, bxc = rnd(st, k, bxc)
    w20 = (P20 + w13) & M
    st, bxc = rnd(st, w20 + K[20], bxc)
    st, bxc = rnd(st, kw21, bxc)
    w22 = (s1(w20) + P22) & M
    st, bxc = rnd(st, w22 + K[22], bxc)
    st, bxc = rnd(st, kw23, bxc)
    w24 = (s1(w22) + P24) & M
    st, bxc = rnd(st, w24 + K[24], bxc)
    st, bxc = rnd(st, kw25, bxc)
    w26 = (s1(w24) + P26) & M
    st, bxc = rnd(st, w26 + K[26], bxc)
    w27 = (w20 + P27) & M
    st, bxc = rnd(st, w27 + K[27], bxc)
    w28 = (s1(w26) + s0(w13) + P28) & M
    st, bxc = rnd(st, w28 + K[28], bxc)
    w29 = (s1(w27) + w22 + w13 + P29) & M
    st, bxc = rnd(st, w29 + K[29], bxc)
    w30 = (s1(w28) + P30) & M
    st, bxc = rnd(st, w30 + K[30], bxc)
    return st[0], st[1], st[2], st[4], st[5], st[6]


def prefix(seed, group):
    data = hashlib.shake_256(b"s256-grouped-prefix|" + seed + struct.pack("<I", group)).digest(52)
    return list(struct.unpack(">13I", data))


def message(words, u):
    return struct.pack(">13I", *words) + struct.pack(">I", (u << 8) | 0x80)[:3]


def trial(seed, groups, per_group, mask):
    """mask: 8 big-endian digest mask words; words 0 and 4 must be zero."""
    seen = {}
    first = (None, None, 0)
    pairs = 0
    for g in range(groups):
        words = prefix(seed, g)
        p = setup(words)
        for u in range(per_group):
            a30, a29, a28, e30, e29, e28 = inner(p, u)
            h = (0, (IV[1] + a30) & M, (IV[2] + a29) & M, (IV[3] + a28) & M,
                 0, (IV[5] + e30) & M, (IV[6] + e29) & M, (IV[7] + e28) & M)
            key = tuple(h[i] & mask[i] for i in range(8))
            msg = message(words, u)
            bucket = seen.setdefault(key, [])
            if bucket and first[0] is None:
                first = (bucket[0].hex(), msg.hex(), g * per_group + u + 1)
            pairs += len(bucket)
            bucket.append(msg)
    return first[0], first[1], first[2], pairs


def main():
    request = json.loads(sys.stdin.read())
    groups, per_group = LAYOUT[request["experiment_id"]]
    assert groups * per_group == SAMPLES
    mask = struct.unpack(">8I", bytes.fromhex(request["event"]["mask_hex"]))
    assert mask[0] == 0 and mask[4] == 0
    out = []
    for item in request["trials"]:
        a, b, first_index, pairs = trial(bytes.fromhex(item["seed"]), groups, per_group, mask)
        out.append({"trial": item["trial"], "message_a_hex": a, "message_b_hex": b,
                    "observations": {"first_match_sample": first_index, "masked_pairs": pairs}})
    sys.stdout.write(json.dumps({"schema_version": 1, "trials": out}, separators=(",", ":")))


if __name__ == "__main__":
    main()
