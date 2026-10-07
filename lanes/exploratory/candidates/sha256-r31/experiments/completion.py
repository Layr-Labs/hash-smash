"""sha256-r31: seeded completion (step C4) of fixed accepted matches.

For each organizer trial nonce, take the accepted match of the stored pair, draw E13 and
E15 candidates from SHAKE-256(nonce), and return the two 128-byte messages of the first
completion that passes the step 14-17 difference checks. A failed search returns nulls.
"""
import hashlib
import json
import sys

M = 0xFFFFFFFF
K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
     0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
     0xe49b69c1]
D = {5: 0xfffff006, 6: 0x002087f1, 7: 0x4fefb5fa, 8: 0x28011100, 9: 0x00008004}


def ror(x, n):
    return ((x >> n) | (x << (32 - n))) & M


def bs0(x):
    return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22)


def bs1(x):
    return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25)


def ss0(x):
    return ror(x, 7) ^ ror(x, 18) ^ (x >> 3)


def ss1(x):
    return ror(x, 17) ^ ror(x, 19) ^ (x >> 10)


def ch(x, y, z):
    return (x & y) ^ (~x & z & M)


def maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)


# Our own starting solution S (z3, proof Section 7.1), steps 9..12, both copies.
A = {9: 0x53a8814f, 10: 0x200b1769, 11: 0xdf4a7a71, 12: 0xcf7d7a3b}
E = {9: 0x61d553d1, 10: 0xf02293fa, 11: 0xaa370c18, 12: 0xf1e5b1ec}
AB = {9: 0x53a8814f, 10: 0x200b976d, 11: 0xdf4a7a71, 12: 0xcf7d7a3b}
EB = {9: 0x61d553d9, 10: 0xdfa31402, 11: 0xbaf70c10, 12: 0xf1e531e4}

# Accepted matches: (first block M0, second-block words W0..W12, W14) with W16 in G16 chosen.
PREFIXES = [
    ([0xe7f5ce55, 0x1741facd, 0x279a66b6, 0x8a38d7c6, 0xcc332e48, 0xed9dd62a, 0x6b76b5f7, 0x3aa91ac9, 0x1ca8034e, 0xb4a9ad70, 0x5b8eeceb, 0x50a7afad, 0x07617b89, 0x719682b5, 0x394303d8, 0x00459adb],
     [0x1e2dbac8, 0x05e61a5e, 0xcd7fcb49, 0x9db00a7a, 0x186cabb0, 0xf7efd9c2, 0x2a442578, 0x023cd6eb, 0xf71d59bf, 0x876b73db, 0xed1499e4, 0x7173c145, 0x0ba5f907],
     0x05848707),
]


class Stream:
    def __init__(self, seed):
        self.seed = seed
        self.block = 0
        self.buf = b""
        self.pos = 0

    def word(self):
        if self.pos + 4 > len(self.buf):
            self.buf = hashlib.shake_256(self.seed + self.block.to_bytes(8, "big")).digest(4096)
            self.block += 1
            self.pos = 0
        x = int.from_bytes(self.buf[self.pos:self.pos + 4], "big")
        self.pos += 4
        return x


def complete(w, w14, stream):
    g = (ss1(w14) + w[9] + ss0(w[1]) + w[0]) & M
    b13 = (A[9] + E[9] + bs1(E[12]) + ch(E[12], E[11], E[10]) + K[13]) & M
    a13c = (bs0(A[12]) + maj(A[12], A[11], A[10]) - A[9]) & M
    for _ in range(1 << 14):
        e13 = (stream.word() & ~0x10c08000 & M) | 0x00408000
        e14 = (A[10] + E[10] + bs1(e13) + ch(e13, E[12], E[11]) + K[14] + w14) & M
        e14b = (AB[10] + EB[10] + bs1(e13) + ch(e13, EB[12], EB[11]) + K[14] + w14) & M
        if (e14b - e14) & M != 0x8004:
            continue
        a13 = (e13 + a13c) & M
        a14 = (e14 - A[10] + bs0(a13) + maj(a13, A[12], A[11])) & M
        a14b = (e14b - AB[10] + bs0(a13) + maj(a13, AB[12], AB[11])) & M
        if a14 != a14b:
            continue
        f15 = (A[11] + E[11] + bs1(e14) + ch(e14, e13, E[12]) + K[15]) & M
        f15b = (AB[11] + EB[11] + bs1(e14b) + ch(e14b, e13, EB[12]) + K[15]) & M
        if f15 != f15b:
            continue
        for _ in range(1 << 8):
            e15 = (stream.word() & ~0x00008004 & M) | 0x00000004
            e16 = (A[12] + E[12] + bs1(e15) + ch(e15, e14, e13) + K[16] + g) & M
            e16b = (AB[12] + EB[12] + bs1(e15) + ch(e15, e14b, e13) + K[16] + g + D[9]) & M
            if e16 != e16b:
                continue
            if ch(e16, e15, e14) != ch(e16, e15, e14b):
                continue
            return (e13 - b13) & M, (e15 - f15) & M
    return None


def words_to_bytes(ws):
    return b"".join(x.to_bytes(4, "big") for x in ws)


def main():
    req = json.loads(sys.stdin.read())
    out = []
    for t in req["trials"]:
        m0, w, w14 = PREFIXES[t["trial"] % len(PREFIXES)]
        stream = Stream(bytes.fromhex(t["seed"]) + b"r31-completion")
        res = complete(w, w14, stream)
        if res is None:
            out.append({"trial": t["trial"], "message_a_hex": None, "message_b_hex": None})
            continue
        w13, w15 = res
        m1 = list(w[:13]) + [w13, w14, w15]
        m1b = list(m1)
        for i, d in D.items():
            m1b[i] = (m1b[i] + d) & M
        out.append({"trial": t["trial"],
                    "message_a_hex": (words_to_bytes(m0) + words_to_bytes(m1)).hex(),
                    "message_b_hex": (words_to_bytes(m0) + words_to_bytes(m1b)).hex()})
    sys.stdout.write(json.dumps({"schema_version": 1, "trials": out}, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
