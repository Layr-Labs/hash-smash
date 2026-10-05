# -*- coding: utf-8 -*-
"""Completion step of the two-block attack (proof.md Section 7), run on the published prefix.

For every organizer seed this program keeps the published first block and the published
second-block words W0..W12, draws fresh starting offsets from the seed, and searches for new
(W13, W14, W15) with the exact tests of Section 7. It returns the resulting pair of 128-byte
messages. It does not search for first blocks: the matching phase (about 2^47.8 compressions)
is not run here. Only the standard library is used.
"""
import hashlib
import json
import sys

M = 0xFFFFFFFF
K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
     0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
     0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
     0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351]
IV = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
M0 = [0x8ce3f805, 0x5c401aed, 0x579e5f7f, 0xbc3116cb, 0xca189b3c, 0xeb75f04c, 0x958f0a0e, 0x7760b082,
      0xdcd5027d, 0x32260ad6, 0x7b12b659, 0xeee66518, 0xad7f88dd, 0xf8ad20bb, 0x7ae40ffd, 0x21609249]
M1 = [0x9abdeb1b, 0x1f195f41, 0x5a7210c1, 0x55614f13, 0xa2269dd1, 0xbe888a61, 0x359257d4, 0xadf3737b,
      0x9f0484a6, 0xeb830a58, 0x66add94a, 0x9669232d, 0x45271fa5, 0xb8f69585, 0x428bbce3, 0x0703b904]
M1P = [0x9abdeb1b, 0x1f195f41, 0x5a7210c1, 0x55614f13, 0xa2269dd1, 0xbe887a67, 0x35b2dfc5, 0xfde32975,
       0xc70595a6, 0xeb838a5c, 0x66add94a, 0x9669232d, 0x45271fa5, 0xb8f69585, 0x428bbce3, 0x0703b904]
WEYL = 0x9e3779b9
CAP13 = 1 << 18
CAP15 = 1 << 12


def rotr(x, n):
    return ((x >> n) | (x << (32 - n))) & M


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


def trace(h, m):
    """31 steps from chaining value h; returns the output and the lists A[i+4], E[i+4], W[i]."""
    w = list(m)
    for t in range(16, 31):
        w.append((s1(w[t - 2]) + w[t - 7] + s0(w[t - 15]) + w[t - 16]) & M)
    a, b, c, d, e, f, g, hh = h
    A = [d, c, b, a]
    E = [hh, g, f, e]
    for t in range(31):
        t1 = (hh + S1(e) + ch(e, f, g) + K[t] + w[t]) & M
        t2 = (S0(a) + maj(a, b, c)) & M
        hh, g, f, e, d, c, b, a = g, f, e, (d + t1) & M, c, b, a, (t1 + t2) & M
        A.append(a)
        E.append(e)
    out = [(x + y) & M for x, y in zip(h, (a, b, c, d, e, f, g, hh))]
    return out, A, E, w


def s1_inverse_table():
    """Rows r[c] with input bit c = parity(r[c] & y) for y = s1(x); Gaussian elimination over GF(2)."""
    rows = []
    for i in range(32):
        mask = 0
        for j in range(32):
            if (s1(1 << j) >> i) & 1:
                mask |= 1 << j
        rows.append([mask, 1 << i])
    for c in range(32):
        p = c
        while not (rows[p][0] >> c) & 1:
            p += 1
        rows[c], rows[p] = rows[p], rows[c]
        for r in range(32):
            if r != c and (rows[r][0] >> c) & 1:
                rows[r][0] ^= rows[c][0]
                rows[r][1] ^= rows[c][1]
    return [row[1] for row in rows]


def main():
    request = json.load(sys.stdin)
    cv1 = trace(IV, M0)[0]
    out, A, E, W = trace(cv1, M1)
    outp, Ap, Ep, Wp = trace(cv1, M1P)
    assert out == outp
    a = lambda i: A[i + 4]
    e = lambda i: E[i + 4]
    ap = lambda i: Ap[i + 4]
    ep = lambda i: Ep[i + 4]
    d16 = (Wp[16] - W[16]) & M
    d18 = (Wp[18] - W[18]) & M
    x18 = (s1(Wp[18]) - s1(W[18])) & M
    da10 = (ap(10) - a(10)) & M
    inv = s1_inverse_table()
    c16 = (W[9] + s0(W[1]) + W[0]) & M
    c18 = (W[11] + s0(W[3]) + W[2]) & M
    # G16: all w with s1(w + d16) - s1(w) = d18 (64 values; the membership test is re-checked here)
    g16 = [(hi << 28) | lo for hi in range(16) for lo in (0x31bbffc, 0x64bbffe, 0x9b3bffd, 0xce3bfff)]
    assert all((s1((g + d16) & M) - s1(g)) & M == d18 for g in g16)
    good = []
    for g in g16:
        w18 = (s1(g) + c18) & M
        if (s1((w18 + d18) & M) - s1(w18)) & M == x18:
            y = (g - c16) & M
            w14 = 0
            for c in range(32):
                w14 |= (bin(inv[c] & y).count("1") & 1) << c
            assert s1(w14) == y
            good.append((g, w14))

    b13 = (a(9) + e(9) + S1(e(12)) + ch(e(12), e(11), e(10)) + K[13]) & M
    k14 = (a(10) + e(10) + K[14]) & M
    k14p = (ap(10) + ep(10) + K[14]) & M
    e11, e12, e11p, e12p = e(11), e(12), ep(11), ep(12)
    m14, m14p = e12 ^ e11, e12p ^ e11p
    a11, a12 = a(11), a(12)

    rows = []
    for item in request["trials"]:
        seed = hashlib.sha256(bytes.fromhex(item["seed"])).digest()
        r13 = int.from_bytes(seed[0:4], "big")
        r15 = int.from_bytes(seed[4:8], "big")
        found = None
        tries13 = tries15 = 0
        for g, w14 in good:
            base = (k14 + w14) & M
            basep = (k14p + w14) & M
            for i in range(CAP13):
                x = (r13 + i * WEYL) & M
                tries13 += 1
                c = e11 ^ (x & m14)
                cp = e11p ^ (x & m14p)
                if (basep + cp - base - c) & M != da10:
                    continue
                sx = S1(x)
                y14 = (base + sx + c) & M
                y14p = (basep + sx + cp) & M
                x15 = (e11 + S1(y14) + ch(y14, x, e12)) & M
                if x15 != (e11p + S1(y14p) + ch(y14p, x, e12p)) & M:
                    continue
                for k in range(CAP15):
                    z = (r15 + k * WEYL) & M
                    tries15 += 1
                    y16 = (e12 + ch(z, y14, x)) & M
                    if y16 != (e12p + ch(z, y14p, x) + d16) & M:
                        continue
                    e16 = (a12 + y16 + S1(z) + K[16] + g) & M
                    if ch(e16, z, y14) != ch(e16, z, y14p):
                        continue
                    found = ((x - b13) & M, w14, (z - a11 - x15 - K[15]) & M)
                    break
                if found:
                    break
            if found:
                break
        row = {"trial": item["trial"], "message_a_hex": None, "message_b_hex": None,
               "observations": {"e13_tries": tries13, "e15_tries": tries15}}
        if found:
            ma = M0 + M1[:13] + list(found)
            mb = M0 + M1P[:13] + list(found)
            row["message_a_hex"] = b"".join(v.to_bytes(4, "big") for v in ma).hex()
            row["message_b_hex"] = b"".join(v.to_bytes(4, "big") for v in mb).hex()
        rows.append(row)
    json.dump({"schema_version": 1, "trials": rows}, sys.stdout, separators=(",", ":"))


main()
