"""Unkeyed BLAKE3-256 with prefix reduction in every compression.

The standard chunk tree, counters, flags, feed-forward and root output are
preserved. This organizer reference accepts complete byte messages; it is not
a compression-only target. See target-profiles/blake3-r{1,2}-prefix-v1.json.
"""

import struct

IV = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
      0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)
PERMUTATION = (2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8)
CHUNK_START, CHUNK_END, PARENT, ROOT = 1, 2, 4, 8
MASK = 0xFFFFFFFF


def _ror(value, count):
    return ((value >> count) | (value << (32 - count))) & MASK


def _g(v, a, b, c, d, x, y):
    v[a] = (v[a] + v[b] + x) & MASK
    v[d] = _ror(v[d] ^ v[a], 16)
    v[c] = (v[c] + v[d]) & MASK
    v[b] = _ror(v[b] ^ v[c], 12)
    v[a] = (v[a] + v[b] + y) & MASK
    v[d] = _ror(v[d] ^ v[a], 8)
    v[c] = (v[c] + v[d]) & MASK
    v[b] = _ror(v[b] ^ v[c], 7)


def _compress(cv, words, counter, block_len, flags, rounds):
    v = list(cv) + list(IV[:4]) + [counter & MASK, counter >> 32, block_len, flags]
    m = list(words)
    for _ in range(rounds):
        _g(v, 0, 4, 8, 12, m[0], m[1])
        _g(v, 1, 5, 9, 13, m[2], m[3])
        _g(v, 2, 6, 10, 14, m[4], m[5])
        _g(v, 3, 7, 11, 15, m[6], m[7])
        _g(v, 0, 5, 10, 15, m[8], m[9])
        _g(v, 1, 6, 11, 12, m[10], m[11])
        _g(v, 2, 7, 8, 13, m[12], m[13])
        _g(v, 3, 4, 9, 14, m[14], m[15])
        m = [m[i] for i in PERMUTATION]
    return tuple(v[i] ^ v[i + 8] for i in range(8)) + tuple(v[i + 8] ^ cv[i] for i in range(8))


def _chunk_output(chunk, counter, rounds):
    cv = IV
    # Keep the last block as an output descriptor: ROOT must be applied to
    # that compression itself, rather than hashing an already produced CV.
    last_offset = max(0, (len(chunk) - 1) // 64 * 64)
    for offset in range(0, last_offset + 1, 64):
        block = chunk[offset:offset + 64]
        flags = CHUNK_START if offset == 0 else 0
        words = struct.unpack("<16I", block.ljust(64, b"\0"))
        if offset == last_offset:
            return cv, words, counter, len(block), flags | CHUNK_END
        cv = _compress(cv, words, counter, 64, flags, rounds)[:8]


def _parent_output(left, right):
    return IV, left + right, 0, 64, PARENT


def blake3(data: bytes, rounds: int = 7) -> bytes:
    """Return the first 32 standard unkeyed root-output bytes."""
    if type(rounds) is not int or not 1 <= rounds <= 7:
        raise ValueError("unsupported BLAKE3 prefix round count")
    if not isinstance(data, bytes) or len(data) >= 1 << 61:
        raise ValueError("requires bytes with bit length less than 2^64")
    chunk_count = max(1, (len(data) + 1023) // 1024)
    stack = []
    for counter in range(chunk_count - 1):
        output = _chunk_output(data[counter * 1024:(counter + 1) * 1024], counter, rounds)
        cv = _compress(*output, rounds)[:8]
        total = counter + 1
        while total & 1 == 0:
            cv = _compress(*_parent_output(stack.pop(), cv), rounds)[:8]
            total >>= 1
        stack.append(cv)
    output = _chunk_output(data[(chunk_count - 1) * 1024:], chunk_count - 1, rounds)
    while stack:
        output = _parent_output(stack.pop(), _compress(*output, rounds)[:8])
    cv, words, _, block_len, flags = output
    root_words = _compress(cv, words, 0, block_len, flags | ROOT, rounds)
    return struct.pack("<8I", *root_words[:8])
