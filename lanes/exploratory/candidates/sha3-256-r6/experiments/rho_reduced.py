"""Reduced-width evidence for proof.md's Floyd rho collision search.

Each trial runs exactly the algorithm of proof.md Section 3 (Floyd cycle
finding followed by tail location) on the iteration map x -> trunc16(H(enc(x))),
where H is complete 6-round SHA3-256 and enc(x) is the 32-byte little-endian
encoding, starting from the trial seed's low 16 bits. The returned pair is two
distinct 32-byte messages whose full digests agree on digest bits 0..15
(organizer-checked mask event). Python work is not the claimed cost.
"""
import json
import sys

RC = (0x0000000000000001, 0x0000000000008082, 0x800000000000808A,
      0x8000000080008000, 0x000000000000808B, 0x0000000080000001)
RHO = (0, 1, 62, 28, 27, 36, 44, 6, 55, 20, 3, 10, 43, 25, 39,
       41, 45, 15, 21, 8, 18, 2, 61, 56, 14)
M64 = (1 << 64) - 1


def rot(v, n):
    n %= 64
    return ((v << n) | (v >> ((64 - n) % 64))) & M64


def perm(A):
    for c in RC:
        P = [A[x] ^ A[x + 5] ^ A[x + 10] ^ A[x + 15] ^ A[x + 20] for x in range(5)]
        T = [P[(x - 1) % 5] ^ rot(P[(x + 1) % 5], 1) for x in range(5)]
        B = [0] * 25
        for y in range(5):
            for x in range(5):
                B[y + 5 * ((2 * x + 3 * y) % 5)] = rot(A[x + 5 * y] ^ T[x], RHO[x + 5 * y])
        for y in range(5):
            for x in range(5):
                A[x + 5 * y] = (B[x + 5 * y] ^ ((~B[(x + 1) % 5 + 5 * y]) & B[(x + 2) % 5 + 5 * y])) & M64
        A[0] ^= c


def sha3_r6(msg):
    block = bytearray(136)
    block[:len(msg)] = msg
    block[len(msg)] ^= 0x06
    block[135] ^= 0x80
    A = [int.from_bytes(block[8 * i:8 * i + 8], "little") for i in range(17)] + [0] * 8
    perm(A)
    return b"".join(a.to_bytes(8, "little") for a in A[:4])


def enc(x):
    return x.to_bytes(32, "little")


def f(x):
    return int.from_bytes(sha3_r6(enc(x))[:2], "little")


def rho(x0, cap):
    t, h, evals = f(x0), f(f(x0)), 3
    while t != h:
        t, h = f(t), f(f(h))
        evals += 3
        if evals > cap:
            return None, None, evals
    t = x0
    while True:
        ft, fh = f(t), f(h)
        evals += 2
        if ft == fh:
            break
        t, h = ft, fh
    if t == h:
        return None, None, evals
    return enc(t).hex(), enc(h).hex(), evals


def main():
    req = json.load(sys.stdin)
    out = []
    for tr in req["trials"]:
        x0 = int(tr["seed"], 16) & 0xFFFF
        a, b, ev = rho(x0, 5 * 2 ** 16)
        out.append({"trial": tr["trial"], "message_a_hex": a, "message_b_hex": b,
                    "observations": {"evaluations": ev}})
    print(json.dumps({"schema_version": 1, "trials": out}, sort_keys=True))


if __name__ == "__main__":
    main()
