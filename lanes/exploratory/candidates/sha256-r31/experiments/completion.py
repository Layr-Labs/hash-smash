"""sha256-r31: seeded completion (step C4) of fixed accepted matches.

For each organizer seed, pick an accepted match (prefix) by trial index, draw E13 and
E15 candidates from SHAKE-256(seed), and return the two 128-byte messages of the first
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


# Starting solution (both copies), steps 9..12, read off the published ASIACRYPT 2024 pair.
A = {9: 0x4f5af3a8, 10: 0x4b9e4fb8, 11: 0x83e817e6, 12: 0x2be31c3f}
E = {9: 0x61c171d3, 10: 0xf02293fa, 11: 0xaa270418, 12: 0xb1f7f9e8}
AB = {9: 0x4f5af3a8, 10: 0x4b9ecfbc, 11: 0x83e817e6, 12: 0x2be31c3f}
EB = {9: 0x61c171db, 10: 0xdfa31402, 11: 0xbae70410, 12: 0xb1f779e0}

# Accepted matches: (first block M0, second-block words W0..W12, W14) with W16 in G16 chosen.
PREFIXES = [
    ([0x116ea499, 0x88c615bc, 0xd08e5d69, 0x2e2c45e7, 0x1e24036b, 0x3c901634, 0xbee5b003, 0xedbd23bf, 0xc57b8553, 0x14b16470, 0xad99b788, 0xb5b33cfb, 0x9830ebc8, 0x988306cc, 0x93a61b60, 0x0040b130],
     [0x1aeca717, 0x7359f369, 0x5e2ecdf3, 0x52f74740, 0xa81916cc, 0x8090da83, 0xb8c3557a, 0x215af20a, 0x9ba486ee, 0xeb830a58, 0x66add94a, 0x9669232d, 0x45271fa5],
     0x6912669a),
    ([0x3f6087af, 0xceeb7f7f, 0x4503c34b, 0x63e30909, 0xf8c44f1c, 0x53aed299, 0x79611354, 0x337b6eff, 0x8b36a2e4, 0xd3df2ab3, 0x1d4ced40, 0x94977e78, 0x998ba6b3, 0x744219ff, 0x3cd8043b, 0x00b30c8f],
     [0xcfda47d4, 0x6db6fa30, 0x87439ec4, 0x58afa37a, 0x409c4805, 0x9a27fd2e, 0x22434754, 0x8eb557cb, 0x3056bb2e, 0xeb830a58, 0x66add94a, 0x9669232d, 0x45271fa5],
     0xe23aacf5),
    ([0x8ce3f805, 0x5c401aed, 0x579e5f7f, 0xbc3116cb, 0xca189b3c, 0xeb75f04c, 0x958f0a0e, 0x7760b082, 0xdcd5027d, 0x32260ad6, 0x7b12b659, 0xeee66518, 0xad7f88dd, 0xf8ad20bb, 0x7ae40ffd, 0x21609249],
     [0x9abdeb1b, 0x1f195f41, 0x5a7210c1, 0x55614f13, 0xa2269dd1, 0xbe888a61, 0x359257d4, 0xadf3737b, 0x9f0484a6, 0xeb830a58, 0x66add94a, 0x9669232d, 0x45271fa5],
     0x428bbce3),
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
