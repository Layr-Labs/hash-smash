"""Finite implementation evidence; run only in the organizer's executor.

The attack proof uses ideal independent words and full 256-bit digests.
This probe uses deterministic SHAKE input and a 16-bit mask of the exact
two-round digest. It does not claim a full collision or measure attack cost.
"""

import hashlib
import itertools
import json
import math
import struct
import sys
from fractions import Fraction


IV = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
      0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)
PERM = (2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8)
MASK32 = (1 << 32) - 1


def digest33(message):
    """Exact complete target on this domain, not a compression-only hash."""
    assert len(message) == 33
    words = list(struct.unpack('<16I', message + bytes(31)))
    state = list(IV) + list(IV[:4]) + [0, 0, 33, 11]

    def ror(value, amount):
        return ((value >> amount) | (value << (32 - amount))) & MASK32

    def g(a, b, c, d, x, y):
        state[a] = (state[a] + state[b] + x) & MASK32
        state[d] = ror(state[d] ^ state[a], 16)
        state[c] = (state[c] + state[d]) & MASK32
        state[b] = ror(state[b] ^ state[c], 12)
        state[a] = (state[a] + state[b] + y) & MASK32
        state[d] = ror(state[d] ^ state[a], 8)
        state[c] = (state[c] + state[d]) & MASK32
        state[b] = ror(state[b] ^ state[c], 7)

    for round_index in range(2):
        g(0, 4, 8, 12, words[0], words[1])
        g(1, 5, 9, 13, words[2], words[3])
        g(2, 6, 10, 14, words[4], words[5])
        g(3, 7, 11, 15, words[6], words[7])
        g(0, 5, 10, 15, words[8], words[9])
        g(1, 6, 11, 12, words[10], words[11])
        g(2, 7, 8, 13, words[12], words[13])
        g(3, 4, 9, 14, words[14], words[15])
        if round_index == 0:
            words = [words[p] for p in PERM]
    return struct.pack('<8I', *(state[j] ^ state[j + 8] for j in range(8)))


def detect(keys, messages, half_bits):
    """Same single-partition/tag algorithm as the proof, at a finite size."""
    size = 1 << half_bits
    mask = size - 1
    assert len(keys) == len(messages) < size
    counts = [0] * size
    table = [0] * size
    for h in keys:
        assert 0 <= h < size * size
        counts[h & mask] += 1
    running = 0
    for b in range(size):
        count = counts[b]
        counts[b] = running
        running += count
    packed = [None] * len(keys)
    for i, h in enumerate(keys):
        b = h & mask
        p = counts[b]
        assert packed[p] is None
        packed[p] = (h & (mask << half_bits)) | i
        counts[b] = p + 1
    p = 0
    for b in range(size):
        end = counts[b]
        tag = b << half_bits
        while p < end:
            record = packed[p]
            a, i = record >> half_bits, record & mask
            old = table[a]
            old_id = old & mask
            if old_id != 0 and old >> half_bits == b:
                j = old_id - 1
                if messages[i] != messages[j]:
                    assert keys[i] == keys[j]
                    return i, j
            else:
                table[a] = tag | (i + 1)
            p += 1
    assert p == len(keys)
    return None


def check_case(keys, messages, half_bits=3):
    expected = any(keys[i] == keys[j] and messages[i] != messages[j]
                   for i in range(len(keys)) for j in range(i))
    found = detect(keys, messages, half_bits)
    assert (found is not None) == expected
    if found is not None:
        i, j = found
        assert messages[i] != messages[j] and keys[i] == keys[j]


def selfcheck():
    checks = 0
    for keys in itertools.product((0, 1, 8, 9), repeat=5):
        check_case(keys, list(range(5)))
        checks += 1
    for mapping in itertools.product((0, 1, 8, 9), repeat=3):
        for messages in itertools.product(range(3), repeat=5):
            check_case([mapping[m] for m in messages], messages)
            checks += 1
    cases = [
        ([0, 8, 16, 24, 32, 40, 48], list(range(7))),
        ([0, 1, 2, 3, 4, 5, 6], list(range(7))),
        ([0, 1, 2, 3, 4, 5, 5], list(range(7))),
        ([0, 0, 0, 0, 0, 0, 0], list(range(7))),
        ([0, 0, 0, 0, 0, 0, 0], [0] * 7),
        ([0, 0, 0, 0, 0, 0, 0], [0] * 6 + [1]),
        ([63, 63, 0, 0, 9, 9, 63], [0, 0, 1, 1, 2, 2, 3]),
    ]
    for keys, messages in cases:
        check_case(keys, messages)
        checks += 1
    k = 1 << 128
    n = 511 << 119
    q = 1 << 256
    x = Fraction(249, 500)
    assert Fraction(n * (n - 1), 2 * q) > x
    series = sum(x ** j / math.factorial(j) for j in range(6))
    lower = 1 - 1 / series - Fraction(1, 512)
    assert lower == Fraction(411002016533346913, 1053058771947306496)
    assert lower > Fraction(39, 100)
    coefficient = Fraction(5513627, 3522560)
    work = Fraction(n + 2) + (Fraction(216) * n + Fraction(10, 32) * n
                              + 28 * k + (1 << 40)) / 430
    assert work == coefficient * k + 2 + Fraction(1 << 40, 430)
    assert work < Fraction(783, 500) * k
    assert 783 ** 20 < (1 << 13) * 500 ** 20
    assert Fraction(8 * k + (1 << 40), 430) < (1 << 123)
    assert 97 * n + 64 * k + (1 << 24) < (1 << 136)
    return checks


def main():
    request = json.load(sys.stdin)
    assert request['schema_version'] == 1
    assert request['target_profile'] == 'blake3-r2-prefix-v1'
    checks = selfcheck()
    results = []
    for trial in request['trials']:
        seed = bytes.fromhex(trial['seed'])
        data = hashlib.shake_256(b'partition-detector-v1' + seed).digest(33 * 255)
        messages = [data[i * 33:(i + 1) * 33] for i in range(255)]
        digests = [digest33(m) for m in messages]
        keys = [int.from_bytes(h[:2], 'little') for h in digests]
        found = detect(keys, messages, 8)
        # A separate dictionary oracle checks completeness on the whole sample.
        seen = {}
        expected = False
        for key, message in zip(keys, messages):
            if key in seen and seen[key] != message:
                expected = True
            else:
                seen[key] = message
        assert expected == (found is not None)
        row = {'trial': trial['trial'], 'message_a_hex': None,
               'message_b_hex': None,
               'observations': {'samples': 255, 'finite_cases_checked': checks,
                                'masked_match': int(found is not None)}}
        if found is not None:
            i, j = found
            assert messages[i] != messages[j] and digests[i][:2] == digests[j][:2]
            row['message_a_hex'] = messages[i].hex()
            row['message_b_hex'] = messages[j].hex()
        results.append(row)
    print(json.dumps({'schema_version': 1, 'trials': results}, sort_keys=True))


if __name__ == '__main__':
    main()
