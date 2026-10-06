# -*- coding: utf-8 -*-
"""Organizer-run completion experiment (proof.md, Section 8), standard library only.

The three prefixes below are the first blocks M0 and second-block words W0..W12 of the three
collisions that the full algorithm found from random first blocks (certificates found-1..3).
For each organizer trial, the program picks prefix (trial mod 3), recomputes the step-12 states
of both messages from M0 and W0..W12, and re-runs the capped completion search of Section 8
with starting offsets derived from the organizer seed, producing new words W13, W14, W15.
It returns the two 128-byte messages M0||M1 and M0||M1'. It does not run the first-block search.
"""
import hashlib
import json
import sys

MASK = 0xFFFFFFFF
K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
     0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
     0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
     0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351]
IV = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
D = {5: 0xfffff006, 6: 0x002087f1, 7: 0x4fefb5fa, 8: 0x28011100, 9: 0x00008004}
WEYL = 0x9e3779b9
XCAP = 1 << 20
ZCAP = 1 << 20
PREFIXES = [
    ("422fe6edb13db2a8dd39995575c307b9770ee870033e7fb3d83717da52d64ca4"
     "3b7ae995a0495594aeb69ff0b1cccf4d19b31d8ccb8d0ac991eab62db350c374",
     "1cb1412633f615f94c9a6b06245d7ef3f6ed3bf3fe208b613957475827f2771a"
     "e0919de11d6935f281ddd25a4c984e9fddb4f6c8"),
    ("dcf4a3e7fc6664c530d0fe566ce9b07fe98afe3d3d8ed18e1a200a1f28170ac4"
     "226f311e81ece3b3b2a935eebed5a535f40f137946a69e2b3dbcd89ac9f68234",
     "90640b5d070151d15a50c2a0505fe087414376f38cde8ee037d007588a1dd69b"
     "63dd5d732a5e7c319bd8c40c5f07de71f2508f85"),
    ("70127198832b7ebb1c175711411f77a9454dffb00d242beb54f022eef0ef09e6"
     "ca0d5b057de8fe757d341c2fdd3a44dade8684b1c6df8ef65fb2a2d364acdf2f",
     "c13a049ec631c957cbad3a4bfe1cafd251ac6657cf4689202d55411c25d2736a"
     "76519129156935f281ddd05a4ca04e9fe1acd5c8"),
]


def rotr(x, n):
    return ((x >> n) | (x << (32 - n))) & MASK


def S0(x):
    return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22)


def S1(x):
    return rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25)


def s0(x):
    return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)


def s1(x):
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)


def ch(e, f, g):
    return g ^ (e & (f ^ g))


def maj(a, b, c):
    return (a & b) ^ (a & c) ^ (b & c)


def words(hexstr):
    b = bytes.fromhex(hexstr)
    return [int.from_bytes(b[i:i + 4], "big") for i in range(0, len(b), 4)]


def compress(h, w16):
    w = list(w16)
    for t in range(16, 31):
        w.append((s1(w[t - 2]) + w[t - 7] + s0(w[t - 15]) + w[t - 16]) & MASK)
    a, b, c, d, e, f, g, hh = h
    for t in range(31):
        t1 = (hh + S1(e) + ch(e, f, g) + K[t] + w[t]) & MASK
        t2 = (S0(a) + maj(a, b, c)) & MASK
        hh, g, f, e, d, c, b, a = g, f, e, (d + t1) & MASK, c, b, a, (t1 + t2) & MASK
    return [(x + y) & MASK for x, y in zip(h, [a, b, c, d, e, f, g, hh])]


def states12(cv, w13):
    """A[t], E[t] for t = -4..12 after running steps 0..12 with words w13[0..12]."""
    A = {-1: cv[0], -2: cv[1], -3: cv[2], -4: cv[3]}
    E = {-1: cv[4], -2: cv[5], -3: cv[6], -4: cv[7]}
    for t in range(13):
        t1 = (A[t - 4] + E[t - 4] + S1(E[t - 1]) + ch(E[t - 1], E[t - 2], E[t - 3]) + K[t] + w13[t]) & MASK
        E[t] = t1
        A[t] = (t1 - A[t - 4] + S0(A[t - 1]) + maj(A[t - 1], A[t - 2], A[t - 3])) & MASK
    return A, E


def s1_inverse_table():
    rows = [0] * 32
    for j in range(32):
        col = s1(1 << j)
        for i in range(32):
            if col >> i & 1:
                rows[i] |= 1 << j
    rows = [rows[i] | (1 << (32 + i)) for i in range(32)]
    for col in range(32):
        p = next(r for r in range(col, 32) if rows[r] >> col & 1)
        rows[p], rows[col] = rows[col], rows[p]
        for r in range(32):
            if r != col and rows[r] >> col & 1:
                rows[r] ^= rows[col]
    return [rows[j] >> 32 for j in range(32)]


INV = s1_inverse_table()


def s1inv(y):
    x = 0
    for j in range(32):
        if bin(INV[j] & y).count("1") & 1:
            x |= 1 << j
    return x


def g16_set():
    out = []
    for h in range(16):
        for lo in (0x031bbffc, 0x064bbffe, 0x09b3bffd, 0x0ce3bfff):
            out.append((h << 28) | lo)
    return out


G16 = g16_set()


def in_g18(w):
    return ((s1((w + 0xffff7ffc) & MASK) - s1(w)) & MASK) == 0x2ffe7fe0


def complete(m0, w13, seed_bytes):
    cv = compress(IV, m0)
    w13p = [(x + D.get(i, 0)) & MASK for i, x in enumerate(w13)]
    A, E = states12(cv, w13)
    Ap, Ep = states12(cv, w13p)
    c16 = (w13[9] + s0(w13[1]) + w13[0]) & MASK
    c18 = (w13[11] + s0(w13[3]) + w13[2]) & MASK
    dE10 = (Ep[10] - E[10]) & MASK
    stream = hashlib.shake_256(seed_bytes).digest(8 * 64)
    xb, zb, k = XCAP, ZCAP, 0
    for g in G16:
        w18 = (s1(g) + c18) & MASK
        if not in_g18(w18):
            continue
        w14 = s1inv((g - c16) & MASK)
        xr = int.from_bytes(stream[4 * k:4 * k + 4], "big")
        zr0 = int.from_bytes(stream[4 * k + 256:4 * k + 260], "big")
        k += 1
        i = 0
        while xb > 0:
            x = (xr + i * WEYL) & MASK
            i += 1
            xb -= 1
            if (dE10 + ch(x, Ep[12], Ep[11]) - ch(x, E[12], E[11])) & MASK:
                continue
            y = (A[10] + E[10] + S1(x) + ch(x, E[12], E[11]) + K[14] + w14) & MASK
            yp = (y + 0x8004) & MASK
            if (E[11] + S1(y) + ch(y, x, E[12])) & MASK != (Ep[11] + S1(yp) + ch(yp, x, Ep[12])) & MASK:
                continue
            zr = (zr0 + i * 0x7f4a7c15) & MASK
            for kk in range(64):
                if zb <= 0:
                    break
                z = (zr + kk * WEYL) & MASK
                zb -= 1
                if (E[12] + ch(z, y, x)) & MASK != (Ep[12] + ch(z, yp, x) + D[9]) & MASK:
                    continue
                u = (A[12] + E[12] + S1(z) + ch(z, y, x) + K[16] + g) & MASK
                if ch(u, z, y) != ch(u, z, yp):
                    continue
                w = list(w13)
                w.append((x - (A[9] + E[9] + S1(E[12]) + ch(E[12], E[11], E[10]) + K[13])) & MASK)
                w.append(w14)
                w.append((z - (A[11] + E[11] + S1(y) + ch(y, x, E[12]) + K[15])) & MASK)
                wp = [(v + D.get(j, 0)) & MASK for j, v in enumerate(w)]
                a = b"".join(v.to_bytes(4, "big") for v in m0 + w)
                b = b"".join(v.to_bytes(4, "big") for v in m0 + wp)
                return a.hex(), b.hex()
        if xb <= 0:
            break
    return None, None


def main():
    req = json.loads(sys.stdin.read())
    out = []
    for tr in req["trials"]:
        m0hex, whex = PREFIXES[tr["trial"] % 3]
        a, b = complete(words(m0hex), words(whex), bytes.fromhex(tr["seed"]))
        out.append({"trial": tr["trial"], "message_a_hex": a, "message_b_hex": b})
    sys.stdout.write(json.dumps({"schema_version": 1, "trials": out}))


if __name__ == "__main__":
    main()
