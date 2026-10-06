# -*- coding: utf-8 -*-
"""Phases 2 and 3 of the two-block attack (proof.md Sections 5 and 7), replayed on stored first blocks.

Each record below holds a first block M0 that our own full run of the attack found to be prefix-valid
with c18 in S, the starting point that accepted it (Appendix A of proof.md) and the tuple (W7, W8).
For every organizer seed this program picks one record, re-checks the starting-point identities,
recomputes the chaining value of M0, repeats every exact test of a trial on it (tuple conditions, key,
W6, W5), rebuilds W0..W6, and runs the completion search of Section 7 with all offsets drawn from the
seed and with the caps of the proof. It returns the two 128-byte messages only if their second-block
outputs are equal. It does not search for first blocks. Only the standard library is used.
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
# The differential structure (proof.md Section 3).
D5, D6, D7, D8, D9 = 0xfffff006, 0x002087f1, 0x4fefb5fa, 0x28011100, 0x00008004
C5, C6, C7, C8, C9 = 0xd0018020, 0x00000ffa, 0xffdf780f, 0xb00fca02, 0xd7feef00
D16, D18, X18, DA10 = 0x00008004, 0xffff7ffc, 0x2ffe7fe0, 0x00008004
XA = {5: 0x000017fa, 6: 0x00800001, 7: 0x11201005, 8: 0x00000004, 10: 0x00008004}
XE = {5: 0x0000303e, 6: 0x00088001, 7: 0xd0880489, 8: 0x4d008804, 9: 0x00000008, 10: 0x2f8187f8,
      11: 0x10c00008, 12: 0x00008008}
G16 = [(hi << 28) | lo for hi in range(16) for lo in (0x31bbffc, 0x64bbffe, 0x9b3bffd, 0xce3bfff)]
WEYL = 0x9e3779b9
CAP13 = 1 << 18      # values of x per g
CAP15 = 1 << 12      # values of z per accepted x
CAPZ = 1 << 18       # values of z per call
# Records: A1..A12 E5..E12 of the starting point, the 16 words of M0, then W7 and W8.
RECORDS = [
    "71d3e17d 6737297a 2488cfa1 7f91b574 056fb3fe 0e9f46f8 812af9be e0660c0e 1ce26643 5ea34c00 00889dbc 3de8ed04 1d1fa7dd afe878e7 4c97cbe5 946f8048 61c511d1 7026b3fa 2a372418 31f7d9e9 e7a8a824 0fda2248 2a5280f9 2cf4781f d3f83c22 56c853ab 6fe0766d c98f9f1a 82ee673f b427012b 1dc18f98 ee4e6269 a33ad3f0 c65ad75b bae96ec5 0a176b32 aff3777a e0dd59fb",
    "0dac657a 60e82779 1b790fa1 de81b574 052fb3fe 0e9e46f8 8d2a79b6 8a346bdc 78a6034b 460e40e0 d8acef7d bee5c34f 1d1fa7dd afe878e7 4c97cbe5 946f8048 41d111d1 7006b3fa ec2f0419 31f3e1e8 f7e7a493 078a567c d1c205a2 eadf4869 773d10ab 3cbb1eef 8b722c9f 972c8e99 0f7feab4 941539c6 8d302f5d 11fb55a5 024493c8 0fef7649 0f7bff19 97cf7e67 afd3772b 9e0a6c33",
    "66325c3e 71672779 a6958fa1 2fa1b574 052fb3fe 069b46f8 092af9be 4e65cdee b6ade53d eb6775ba 1a3a7e11 fd3b7b73 1d1fa7dd afe878e7 4c97cbe5 947f8048 41d511d1 f00293fa aa272419 3173c9e9 5bfe9297 f36d82b2 a89a13ba 35fb5759 c68f7582 085be33c 305a7513 c2134482 717c8d89 438091d3 49c0a924 848083be 9c4d0a7d 5ee892ae 80db62c9 a1298a4e a95bf22b e6d91973",
    "7f00a63f 6c92da07 54963413 917566c3 fa9053ff 33fe554a 8bf1120c 35ca95f7 c3db9b1e c65074e2 7f7a44a8 751573c2 1d1fa7dd afe878e7 4c97cbe5 947f8048 41d501d1 7006b3fa ec3f1c1c 0ff5ea0a 2726a4bc c978cbe1 792646c0 d513ca57 f1593a21 6ec40ef8 c1275eca 7aa7b31c 6be6a28d 4c48c97c b24acef0 472be348 1cb7fad0 b007164b 29b21bf8 f6bd3f65 001cd28b 32b6bb6e",
    "4f04bc36 51452779 26818fa1 4b92b574 052fb3fe 069b46f8 892ef9be 2265cc0e dea98335 3bbd593b 0ff83ae3 41492679 1d1fa7dd afe878e7 4c97cbe5 946f8048 61d111d1 f02293fa 6c270418 4fe7da0e f3e3d61d a72ad2a8 a3d7799d 1b1005ce 840b13d2 12ee05b3 f53a87a7 f2805522 ed1369c1 e3f64fb7 9019d463 e85a79e1 9069341f ea9ed455 1e9c98a6 68915c08 883dd2fb 351a3b3b",
    "8f30bcb6 51652779 26918fa1 4ba2b574 052fb3fe 069b46f8 892ef9be 2265cc0e dea98335 bbc1793b c0bb4243 d75f037b 1d1fa7dd afe878e7 4c97cbe5 947f8048 61d111d1 7026b3fa 6c3f0418 0fe1b20e cad6279a e357e6d8 48312566 4f361605 aa4c86ea d200d67a 35dbd2bf 0f700e72 6405a314 9e422b77 b2ee606b 479d0bb0 bbcb5f62 a65b1928 6cdba212 c36dd30f 217af27a 75191d3b",
    "42524fa6 ce34c202 a506b412 d06666c3 fa9053fb f1ee5d4e 87f09384 379f76cd 85945b3a af865ab2 f2faeb6e 2e4efd1d 1d1fa7dd afe878e7 4c97cbe5 947f8048 41d101d3 f00293fa 6c370418 b1f381e9 5a399fe9 f8580794 f596dfb0 ab7611d5 f4a86d9a e0e2bcaa 000f4303 502f8cce e4a6fd6c 62b8cfc1 d5410b8b 2e962db5 56b3c41a bfeaf63d 2943b3e2 7663930f 06b457fa 3cd48064",
    "8dec17b0 ae54da07 ba277412 3b1266c3 fa9053ff dbba554a 83f0138c b1df96bf 030bbaf4 11b11858 bab04f61 28637e49 1d1fa7dd afe878e7 4c97cbe5 946b8048 41d161d1 7006b3fa 2a371c19 f1f5b9e8 3183702c 7a8e00d7 0ecb0d0e a6eddb93 6d70a340 29830049 fc9e8af1 ce29b871 60f9183c 85dc672c 4f3936a0 d4bbc217 478d0c79 dd490bdf d2cd44b2 c56fa392 8a3dd6ca 20b4bbec",
    "5fdf9014 f642da07 e141b412 a22166c3 fa9053ff bbbb554a 0ff59204 f39077e5 85067bca a2da6f49 7b0aad6c 1df48454 1d1fa7dd afe878e7 4c97cbe5 946b8048 41d161d1 7006b3fa 6c27141d 0f65ca0f 651160fd 9dfee534 57b7133a 69f05603 43166ca5 61525e4c 1c1b1ccd a8679755 e2022c48 44a1ab5f 2e0a703f a7c9cc87 17507840 3ccc3f1d acf39023 f0602517 8c9553ca 2714bb2c",
    "8e23f6ab 47642779 1594cfa1 44e2b574 052fb3fe 0e9f46f8 852ef9be 2c262bde b6276d47 1faf4b92 0b74de11 0615ed31 1d1fa7dd afe878e7 4c97cbe5 947f8048 61d121d1 7026b3fa ec270419 b1e7a1ed 3d6251c6 8e115899 c71f32a2 f0bd15b9 06dd8cb0 fb548cf4 d6d9f78a 78b553c6 a71f2000 a25aedd3 7dc4a61b b5334f9f daad8d66 079eb1cf 04bfe915 02d5f32a 215af26b e6591533",
    "103a514b 8e93da07 8992b413 726266c3 fa9053ff 3bfb554a 07f19204 b59eb7e5 87c3dcf0 850600d1 279b0515 90af7fdc 1d1fa7dd afe878e7 4c97cbe5 947b8048 a1c301d1 7026b3fa 2a371418 b16f89ed 24e6eae1 ab48f4de 8723b44f 610275e5 7a3e1a4f 3d7b708b 0f5e75d2 0e0f0c04 9a849b9e 6864eaf2 92b281de ccc16b23 7139d7b2 10335cba 2708e886 d8237e03 8a3dd6cb 30b6bbee",
    "b64d2742 d1492779 fb880fa1 8e92b574 052fb3fe 0e9e46f8 ad2a79b6 e2246c5c b6af448b 7c7b2422 45c9a18d 3fd0e554 1d1fa7dd afe878e7 4c97cbe5 946f8048 41d111d1 7006b3fa aa271419 316bb9ec 53d7336c 8ddcbd97 e6a6973b e4bfbb64 1ec7a58b a3febd08 f865a219 5036f874 c8fea690 ca5dd5e6 236bf05a 3b63c44f 9471ed71 7ea5b194 40f2a751 d1681dbb aff3772a 735d5533",
    "49cdf9f2 6f97297a 27d58fa1 bce1b574 056fb3fe 069b46f8 852af9be a4222bfe 3ee26b4f 29fa2a3b 06f587d1 436bcbab 1d1fa7dd afe878e7 4c97cbe5 947f8048 41d561d1 7006b3fa ec2f2c18 0f71ba0b c50ed168 a2e77926 9e465769 3d8cea96 f23b613c 06e13455 0d374e24 fd6ccf27 ac202750 e159f722 3158ca8e 32369acb 35cfd6c2 2f1cf0cf 1237988a b23ae25e 25d2733a 71d919fb",
    "fe1dac81 cf5a297a 85954fa1 dea2b574 056fb3fe 069a46f8 2d2a79b6 aa246e5c 346144eb 04df38e1 9c56941e 794bce3e 1d1fa7dd afe878e7 4c97cbe5 947f8048 41d151d1 7006b3fa aa3f3419 b167e9ed 1f9e05be 42b0856f db432295 6189e635 1e00b9d0 fe2823a5 c7d249bc f8cb4cb0 52eb9e27 c4fefef2 3e74f980 e4048dee 44ceecd8 f8c242df fc21fa1e e8488de1 8cb553aa 9f5dffb3",
    "84dac774 0218c003 09fff412 c32666c3 fad053fb 99ea5d4e 03f59204 b3ded7f5 c30b92e0 63874978 57d07def 5b1d38a5 1d1fa7dd afe878e7 4c97cbe5 947f8048 81d711d3 f00293fa 2a2f0c19 4fff9a0b 799d0965 3a8de9b5 1cf764ca 802a393a ccb0c846 ce0b7cca 95ba590c 85a8f06f 8fc2d542 07aff0bc b02721e2 16e826c9 241b31e0 c3ce3934 12be0411 ee20f7ac 8eb5578a 3056b32c",
]


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


def compress(h, m):
    """The 31-step compression function with feed-forward."""
    w = list(m)
    for t in range(16, 31):
        w.append((s1(w[t - 2]) + w[t - 7] + s0(w[t - 15]) + w[t - 16]) & M)
    a, b, c, d, e, f, g, hh = h
    for t in range(31):
        t1 = (hh + S1(e) + ch(e, f, g) + K[t] + w[t]) & M
        t2 = (S0(a) + maj(a, b, c)) & M
        hh, g, f, e, d, c, b, a = g, f, e, (d + t1) & M, c, b, a, (t1 + t2) & M
    return [(x + y) & M for x, y in zip(h, (a, b, c, d, e, f, g, hh))]


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


class Coins:
    """Fresh 32-bit words for one trial: word number i is the first four bytes of SHA-256(seed || i)."""

    def __init__(self, seed):
        self.seed = seed
        self.i = 0

    def word(self):
        v = hashlib.sha256(self.seed + self.i.to_bytes(4, "big")).digest()
        self.i += 1
        return int.from_bytes(v[:4], "big")


def starting_point(words):
    """State words of both messages and W9..W12; None unless identities (P1)..(P5) hold exactly."""
    a = dict(zip(range(1, 13), words[:12]))
    e = dict(zip(range(5, 13), words[12:20]))
    ap = {t: a[t] ^ XA.get(t, 0) for t in a}
    ep = {t: e[t] ^ XE[t] for t in e}
    for t in range(5, 13):
        if a[t] != (e[t] - a[t - 4] + S0(a[t - 1]) + maj(a[t - 1], a[t - 2], a[t - 3])) & M:
            return None
        if ap[t] != (ep[t] - ap[t - 4] + S0(ap[t - 1]) + maj(ap[t - 1], ap[t - 2], ap[t - 3])) & M:
            return None
    w = {}
    for t in range(9, 13):
        w[t] = (e[t] - a[t - 4] - e[t - 4] - S1(e[t - 1]) - ch(e[t - 1], e[t - 2], e[t - 3]) - K[t]) & M
        wp = (ep[t] - ap[t - 4] - ep[t - 4] - S1(ep[t - 1]) - ch(ep[t - 1], ep[t - 2], ep[t - 3]) - K[t]) & M
        if wp != (w[t] + (D9 if t == 9 else 0)) & M:
            return None
    if (s0((w[9] + D9) & M) - s0(w[9])) & M != C9:
        return None
    b8 = (e[8] - S1(e[7]) - ch(e[7], e[6], e[5])) & M
    b8p = (ep[8] - S1(ep[7]) - ch(ep[7], ep[6], ep[5])) & M
    if (b8p - b8) & M != D8 or (ep[5] - e[5]) & M != D5:
        return None
    if (a[9] + e[9] + S1(e[12]) + ch(e[12], e[11], e[10])) & M != \
            (ap[9] + ep[9] + S1(ep[12]) + ch(ep[12], ep[11], ep[10])) & M:
        return None
    if maj(a[12], a[11], a[10]) != maj(ap[12], ap[11], ap[10]):
        return None
    if (ap[10] - a[10]) & M != DA10 or (DA10 + D18) & M != 0:
        return None
    return a, ap, e, ep, w


def prefix(sp, cv, w7, w8):
    """One trial of Section 5 for the tuple (W7, W8): returns W0..W8, or None if any test fails."""
    a, ap, e, ep, _ = sp
    am1, am2, am3, am4, em1, em2, em3, em4 = cv
    if (s0((w8 + D8) & M) - s0(w8)) & M != C8 or (s0((w7 + D7) & M) - s0(w7)) & M != C7:
        return None                                                           # W8 in V8, W7 in V7
    e4 = (e[8] - a[4] - S1(e[7]) - ch(e[7], e[6], e[5]) - K[8] - w8) & M
    if (ch(ep[6], ep[5], e4) - ch(e[6], e[5], e4)) & M != (ep[7] - e[7] - S1(ep[6]) + S1(e[6]) - D7) & M:
        return None                                                           # (F7)
    e3 = (e[7] - a[3] - S1(e[6]) - ch(e[6], e[5], e4) - K[7] - w7) & M
    if (ch(ep[5], e4, e3) - ch(e[5], e4, e3)) & M != (ep[6] - e[6] - S1(ep[5]) + S1(e[5]) - D6) & M:
        return None                                                           # (F6)
    a0 = (e4 - a[4] + S0(a[3]) + maj(a[3], a[2], a[1])) & M
    if (e3 - a[3] + S0(a[2]) + maj(a[2], a[1], a0)) & M != am1:
        return None                                                           # the key is A_-1
    e2 = (a[2] + am2 - S0(a[1]) - maj(a[1], a0, am1)) & M
    w6 = (e[6] - a[2] - e2 - S1(e[5]) - ch(e[5], e4, e3) - K[6]) & M
    if (s0((w6 + D6) & M) - s0(w6)) & M != C6:
        return None                                                           # W6 in V6
    e1 = (a[1] + am3 - S0(a0) - maj(a0, am1, am2)) & M
    w5 = (e[5] - a[1] - e1 - S1(e4) - ch(e4, e3, e2) - K[5]) & M
    if (s0((w5 + D5) & M) - s0(w5)) & M != C5:
        return None                                                           # W5 in V5
    e0 = (a0 + am4 - S0(am1) - maj(am1, am2, am3)) & M
    w0 = (e0 - am4 - em4 - S1(em1) - ch(em1, em2, em3) - K[0]) & M
    w1 = (e1 - am3 - em3 - S1(e0) - ch(e0, em1, em2) - K[1]) & M
    w2 = (e2 - am2 - em2 - S1(e1) - ch(e1, e0, em1) - K[2]) & M
    w3 = (e3 - am1 - em1 - S1(e2) - ch(e2, e1, e0) - K[3]) & M
    w4 = (e4 - a0 - e0 - S1(e3) - ch(e3, e2, e1) - K[4]) & M
    return [w0, w1, w2, w3, w4, w5, w6, w7, w8]


def complete(sp, c16, c18, coins, inv):
    """Phase 3 (Section 7). Returns (W13, W14, W15) or None, and the numbers of x and z values tried."""
    a, ap, e, ep, _ = sp
    b13 = (a[9] + e[9] + S1(e[12]) + ch(e[12], e[11], e[10]) + K[13]) & M
    k14 = (a[10] + e[10] + K[14]) & M
    k14p = (ap[10] + ep[10] + K[14]) & M
    e11, e12, e11p, e12p = e[11], e[12], ep[11], ep[12]
    m14, m14p = e12 ^ e11, e12p ^ e11p          # Ch(x, E12, E11) = E11 ^ (x & (E12 ^ E11))
    nx = nz = 0
    for g in G16:
        w18 = (s1(g) + c18) & M
        if (s1((w18 + D18) & M) - s1(w18)) & M != X18:
            continue                                                          # W18 must lie in G18
        y0 = (g - c16) & M
        w14 = 0
        for c in range(32):
            w14 |= (bin(inv[c] & y0).count("1") & 1) << c
        base = (k14 + w14) & M
        basep = (k14p + w14) & M
        r13 = coins.word()
        for i in range(CAP13):
            x = (r13 + i * WEYL) & M
            nx += 1
            c = e11 ^ (x & m14)
            cp = e11p ^ (x & m14p)
            if (basep + cp - base - c) & M != DA10:
                continue                                                      # (C14)
            sx = S1(x)
            y = (base + sx + c) & M
            yp = (basep + sx + cp) & M
            x15 = (e11 + S1(y) + ch(y, x, e12)) & M
            if x15 != (e11p + S1(yp) + ch(yp, x, e12p)) & M:
                continue                                                      # (C15)
            r15 = coins.word()
            for k in range(CAP15):
                z = (r15 + k * WEYL) & M
                nz += 1
                if nz > CAPZ:
                    return None, nx, nz
                y16 = (e12 + ch(z, y, x)) & M
                if y16 != (e12p + ch(z, yp, x) + D16) & M:
                    continue                                                  # (C16)
                u = (a[12] + y16 + S1(z) + K[16] + g) & M
                if ch(u, z, y) != ch(u, z, yp):
                    continue                                                  # (C17)
                return ((x - b13) & M, w14, (z - a[11] - x15 - K[15]) & M), nx, nz
    return None, nx, nz


def main():
    request = json.load(sys.stdin)
    inv = s1_inverse_table()
    assert all((s1((g + D16) & M) - s1(g)) & M == D18 for g in G16)
    records = [[int(v, 16) for v in r.split()] for r in RECORDS]
    rows = []
    for item in request["trials"]:
        coins = Coins(bytes.fromhex(item["seed"]))
        idx = coins.word() % len(records)
        rec = records[idx]
        m0, w7, w8 = rec[20:36], rec[36], rec[37]
        row = {"trial": item["trial"], "message_a_hex": None, "message_b_hex": None,
               "observations": {"record": idx, "x_tries": 0, "z_tries": 0}}
        sp = starting_point(rec[:20])
        cv = compress(IV, m0)
        pre = prefix(sp, cv, w7, w8) if sp else None
        if pre:
            w = sp[4]
            m1 = pre + [w[9], w[10], w[11], w[12]]
            c16 = (m1[9] + s0(m1[1]) + m1[0]) & M
            c18 = (m1[11] + s0(m1[3]) + m1[2]) & M
            found, nx, nz = complete(sp, c16, c18, coins, inv)
            row["observations"]["x_tries"] = nx
            row["observations"]["z_tries"] = nz
            if found:
                m1 = m1 + list(found)
                m1p = list(m1)
                for t, dt in ((5, D5), (6, D6), (7, D7), (8, D8), (9, D9)):
                    m1p[t] = (m1p[t] + dt) & M
                if compress(cv, m1) == compress(cv, m1p):
                    row["message_a_hex"] = b"".join(v.to_bytes(4, "big") for v in m0 + m1).hex()
                    row["message_b_hex"] = b"".join(v.to_bytes(4, "big") for v in m0 + m1p).hex()
        rows.append(row)
    json.dump({"schema_version": 1, "trials": rows}, sys.stdout, separators=(",", ":"))


main()
