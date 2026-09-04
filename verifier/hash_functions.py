"""Organizer-owned reduced-round, full-message hash definitions.

MD5: RFC 1321. SHA-1/SHA-256: FIPS 180-4. Reduced variants execute the
first r compression steps on EVERY padded block, retaining IV and feed-forward.
This is a reference checker, not an attack or a participant-code executor.
"""

import struct

MASK = 0xffffffff
FULL_ROUNDS = {"md5": 64, "sha1": 80, "sha256": 64}
DIGEST_BITS = {"md5": 128, "sha1": 160, "sha256": 256}
MD5_K = (
    0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
    0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be, 0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
    0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa, 0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
    0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, 0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
    0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c, 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
    0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05, 0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
    0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039, 0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
    0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1, 0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391,
)
SHA256_K = (
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
)
IV = {
    "md5": (0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476),
    "sha1": (0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476, 0xc3d2e1f0),
    "sha256": (0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
               0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19),
}


def _rol(value: int, count: int) -> int:
    value &= MASK
    return ((value << count) | (value >> (32-count))) & MASK


def _ror(value: int, count: int) -> int:
    return _rol(value, 32-count)


def _compress(algorithm: str, state: tuple[int, ...], block: bytes, rounds: int) -> tuple[int, ...]:
    words = list(struct.unpack("<16I" if algorithm == "md5" else ">16I", block))
    if algorithm == "md5":
        a, b, c, d = state
        rotations = ((7, 12, 17, 22), (5, 9, 14, 20), (4, 11, 16, 23), (6, 10, 15, 21))
        for i in range(rounds):
            if i < 16:
                f, g = (b & c) | (~b & d), i
            elif i < 32:
                f, g = (d & b) | (~d & c), (5*i+1) % 16
            elif i < 48:
                f, g = b ^ c ^ d, (3*i+5) % 16
            else:
                f, g = c ^ (b | ~d), (7*i) % 16
            a, b, c, d = d, (b + _rol(a+f+MD5_K[i]+words[g], rotations[i//16][i%4])) & MASK, b, c
        working = (a, b, c, d)
    elif algorithm == "sha1":
        for i in range(16, rounds):
            words.append(_rol(words[i-3] ^ words[i-8] ^ words[i-14] ^ words[i-16], 1))
        a, b, c, d, e = state
        for i in range(rounds):
            if i < 20:
                f, k = (b & c) | (~b & d), 0x5a827999
            elif i < 40:
                f, k = b ^ c ^ d, 0x6ed9eba1
            elif i < 60:
                f, k = (b & c) | (b & d) | (c & d), 0x8f1bbcdc
            else:
                f, k = b ^ c ^ d, 0xca62c1d6
            a, b, c, d, e = (_rol(a, 5)+f+e+k+words[i]) & MASK, a, _rol(b, 30), c, d
        working = (a, b, c, d, e)
    else:
        for i in range(16, rounds):
            x, y = words[i-15], words[i-2]
            s0 = _ror(x, 7) ^ _ror(x, 18) ^ (x >> 3)
            s1 = _ror(y, 17) ^ _ror(y, 19) ^ (y >> 10)
            words.append((words[i-16]+s0+words[i-7]+s1) & MASK)
        a, b, c, d, e, f, g, h = state
        for i in range(rounds):
            s1 = _ror(e, 6) ^ _ror(e, 11) ^ _ror(e, 25)
            t1 = (h+s1+((e & f) ^ (~e & g))+SHA256_K[i]+words[i]) & MASK
            s0 = _ror(a, 2) ^ _ror(a, 13) ^ _ror(a, 22)
            t2 = (s0+((a & b) ^ (a & c) ^ (b & c))) & MASK
            a, b, c, d, e, f, g, h = (t1+t2) & MASK, a, b, c, (d+t1) & MASK, e, f, g
        working = (a, b, c, d, e, f, g, h)
    return tuple((old+new) & MASK for old, new in zip(state, working))


def digest(data: bytes, algorithm: str, rounds: int) -> bytes:
    """Hash bytes with the pinned prefix-step/full-message semantics."""
    if algorithm in ("sha3_256", "keccak800"):
        from .keccak import sha3_256, keccak800
        return {"sha3_256": sha3_256, "keccak800": keccak800}[algorithm](data, rounds)
    if algorithm not in FULL_ROUNDS or type(rounds) is not int or not 1 <= rounds <= FULL_ROUNDS[algorithm]:
        raise ValueError("unsupported algorithm or round count")
    if not isinstance(data, bytes) or len(data) >= 1 << 61:
        raise ValueError("requires bytes with bit length less than 2^64")
    endian = "little" if algorithm == "md5" else "big"
    padded = data + b"\x80" + bytes((55-len(data)) % 64) + (8*len(data)).to_bytes(8, endian)
    state = IV[algorithm]
    for offset in range(0, len(padded), 64):
        state = _compress(algorithm, state, padded[offset:offset+64], rounds)
    return b"".join(word.to_bytes(4, endian) for word in state)
