"""Phase 3 (completion) of the sha256-r31 two-block attack, run on the published prefix.

Own implementation for sha256-r31-exploratory (proof.md Section 7). Fixed inputs:
the published first block M0 and second-block words W0..W12 of the Li-Liu-Wang-
Dong-Sun pair. For each organizer seed the search offsets for E13 and E15 are
derived from the seed (SHAKE-256), the capped completion search chooses
(W13, W14, W15), and the program returns M0||M1 and M0||M1' (M1' = M1 plus the
fixed differences in words 5..9). The organizer re-hashes every returned pair.
Phases 1 and 2 (table, first-block search) are not executed here.
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
     0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351)
M0 = (0x8ce3f805, 0x5c401aed, 0x579e5f7f, 0xbc3116cb, 0xca189b3c, 0xeb75f04c, 0x958f0a0e, 0x7760b082,
      0xdcd5027d, 0x32260ad6, 0x7b12b659, 0xeee66518, 0xad7f88dd, 0xf8ad20bb, 0x7ae40ffd, 0x21609249)
PREFIX = (0x9abdeb1b, 0x1f195f41, 0x5a7210c1, 0x55614f13, 0xa2269dd1, 0xbe888a61, 0x359257d4,
          0xadf3737b, 0x9f0484a6, 0xeb830a58, 0x66add94a, 0x9669232d, 0x45271fa5)
DIFF = {5: 0xfffff006, 6: 0x002087f1, 7: 0x4fefb5fa, 8: 0x28011100, 9: 0x00008004}
D16, D18, X18 = 0x00008004, 0xffff7ffc, 0x2ffe7fe0
STEP = 0x9e3779b9
CAP_X, CAP_Z_PER_X, CAP_Z = 1 << 18, 1 << 12, 1 << 18


def ror(x, r):
    return ((x >> r) | (x << (32 - r))) & M


def S0(x):
    return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22)


def S1(x):
    return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25)


def s0(x):
    return ror(x, 7) ^ ror(x, 18) ^ (x >> 3)


def s1(x):
    return ror(x, 17) ^ ror(x, 19) ^ (x >> 10)


def ch(e, f, g):
    return (e & f) ^ (~e & g & M)


def maj(a, b, c):
    return (a & b) ^ (a & c) ^ (b & c)


def first13(cv, w):
    """Run steps 0..12 from cv; return A[t], E[t] for t = -4..12 as dicts."""
    a, b, c, d, e, f, g, h = cv
    A = {-1: a, -2: b, -3: c, -4: d}
    E = {-1: e, -2: f, -3: g, -4: h}
    for t in range(13):
        t1 = (h + S1(e) + ch(e, f, g) + K[t] + w[t]) & M
        t2 = (S0(a) + maj(a, b, c)) & M
        h, g, f, e, d, c, b, a = g, f, e, (d + t1) & M, c, b, a, (t1 + t2) & M
        A[t], E[t] = a, e
    return A, E


def compress_cv(w):
    a, b, c, d, e, f, g, h = IV
    w = list(w)
    for t in range(16, 31):
        w.append((s1(w[t - 2]) + w[t - 7] + s0(w[t - 15]) + w[t - 16]) & M)
    for t in range(31):
        t1 = (h + S1(e) + ch(e, f, g) + K[t] + w[t]) & M
        t2 = (S0(a) + maj(a, b, c)) & M
        h, g, f, e, d, c, b, a = g, f, e, (d + t1) & M, c, b, a, (t1 + t2) & M
    return tuple((x + y) & M for x, y in zip(IV, (a, b, c, d, e, f, g, h)))


def s1_inverse_table():
    # s1 is GF(2)-linear and invertible on 32-bit words: solve s1(x) = e_i by elimination.
    rows = [[s1(1 << i), 1 << i] for i in range(32)]
    for bit in range(32):
        p = next(i for i in range(bit, 32) if (rows[i][0] >> bit) & 1)
        rows[bit], rows[p] = rows[p], rows[bit]
        for i in range(32):
            if i != bit and (rows[i][0] >> bit) & 1:
                rows[i][0] ^= rows[bit][0]
                rows[i][1] ^= rows[bit][1]
    return [rows[i][1] for i in range(32)]


INV = s1_inverse_table()


def s1_inv(y):
    r = 0
    for i in range(32):
        if (y >> i) & 1:
            r ^= INV[i]
    return r


def g16_list():
    # G16 = { (h<<28) | lo : h in 0..15, lo in four fixed values }; checked by the defining relation.
    out = []
    for hi in range(16):
        for lo in (0x031bbffc, 0x064bbffe, 0x09b3bffd, 0x0ce3bfff):
            g = (hi << 28) | lo
            if (s1((g + D16) & M) - s1(g)) & M == D18:
                out.append(g)
    return out


G16 = g16_list()


def complete(A, E, A2, E2, c16, c18, r13, r15):
    zeta = 0
    for g in G16:
        w18 = (s1(g) + c18) & M
        if (s1((w18 + D18) & M) - s1(w18)) & M != X18:
            continue
        w14 = s1_inv((g - c16) & M)
        k14 = (A[10] + E[10] + K[14] + w14) & M
        k14p = (A2[10] + E2[10] + K[14] + w14) & M
        for i in range(CAP_X):
            x = (r13 + i * STEP) & M
            sx = S1(x)
            y = (k14 + sx + ch(x, E[12], E[11])) & M
            yp = (k14p + sx + ch(x, E2[12], E2[11])) & M
            if (yp - y) & M != 0x00008004:
                continue
            if (E[11] + S1(y) + ch(y, x, E[12])) & M != (E2[11] + S1(yp) + ch(yp, x, E2[12])) & M:
                continue
            for k in range(CAP_Z_PER_X):
                if zeta >= CAP_Z:
                    return None
                zeta += 1
                z = (r15 + k * STEP) & M
                c1, c2 = ch(z, y, x), ch(z, yp, x)
                if (E[12] + c1) & M != (E2[12] + c2 + D16) & M:
                    continue
                u = (A[12] + E[12] + c1 + S1(z) + K[16] + g) & M
                if ch(u, z, y) != ch(u, z, yp):
                    continue
                w13 = (x - (A[9] + E[9] + S1(E[12]) + ch(E[12], E[11], E[10]) + K[13])) & M
                w15 = (z - (A[11] + E[11] + S1(y) + ch(y, x, E[12]) + K[15])) & M
                return w13, w14, w15
    return None


def main():
    request = json.loads(sys.stdin.read())
    cv = compress_cv(M0)
    w = list(PREFIX)
    w2 = [(w[i] + DIFF.get(i, 0)) & M for i in range(13)]
    A, E = first13(cv, w)
    A2, E2 = first13(cv, w2)
    c16 = (w[9] + s0(w[1]) + w[0]) & M
    c18 = (w[11] + s0(w[3]) + w[2]) & M
    out = []
    for item in request["trials"]:
        seed = bytes.fromhex(item["seed"])
        r13, r15 = struct.unpack(">II", hashlib.shake_256(b"r31-completion|" + seed).digest(8))
        res = complete(A, E, A2, E2, c16, c18, r13, r15)
        if res is None:
            out.append({"trial": item["trial"], "message_a_hex": None, "message_b_hex": None})
            continue
        m1 = w + list(res)
        m1p = w2 + list(res)
        ma = struct.pack(">16I", *M0) + struct.pack(">16I", *m1)
        mb = struct.pack(">16I", *M0) + struct.pack(">16I", *m1p)
        out.append({"trial": item["trial"], "message_a_hex": ma.hex(), "message_b_hex": mb.hex()})
    sys.stdout.write(json.dumps({"schema_version": 1, "trials": out}, separators=(",", ":")))


if __name__ == "__main__":
    main()
