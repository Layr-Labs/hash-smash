"""Scaled replay of the 8-way SWAR-packed two-round BLAKE3 birthday search.

Each trial draws N_t independent uniform 64-byte single-block messages from the
organizer seed (SHAKE-256) and hashes them ONLY through the submitted 8-way SWAR
packed evaluator: eight messages are packed into 256-bit words as eight disjoint
32-bit lanes, the two-round compression is run with per-field carry-isolated
addition (padd), masked 32-bit rotation (pror) and field-wise XOR, and lane j's
256-bit digest is unpacked from the eight output words o0..o7 = v[i]^v[i+8]. The
organizer re-verifies every returned pair against verifier/blake3.py:blake3(.,2),
so a returned masked match also certifies the packed evaluator on those inputs.

The masked birthday event is the scaled analogue of the full attack. With
N_t = 1024 = 2^10 messages and a w = 20-bit digest mask, N_t^2 / 2^w = 1 =
N^2 / 2^256 at the full width N = 2^128. Under the independent-uniform model
(heuristic H1) a trial has a masked collision with probability
1 - prod_{i<1024}(1 - i/2^20) = 0.39327..., the same birthday value the attack's
table events use. All N_t samples are evaluated; the first masked-equal pair is
returned (else two nulls). Untrusted observations report the 1-based sample
index of that first match (0 if none) and the number of masked-equal pairs.

Experiment ids select the message layout and reuse the same evaluator:
  b3r2-swar-birthday  : N_t independent messages, 20-bit mask spread over o0..o7
  b3r2-swar-lowbits   : same N_t messages, 20-bit mask concentrated in o0,o1
"""

import hashlib
import json
import struct
import sys

MASK256 = (1 << 256) - 1
IV = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
      0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)
PERMUTATION = (2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8)
SAMPLES = 1024


def _broadcast(v32):
    r = 0
    for j in range(8):
        r |= (v32 & 0xFFFFFFFF) << (32 * j)
    return r


_H = _broadcast(0x80000000)
_NOTH = _broadcast(0x7FFFFFFF)


def _rotmasks(r):
    rmask = _broadcast((1 << (32 - r)) - 1)
    lmask = _broadcast(((1 << r) - 1) << (32 - r))
    return rmask, lmask


_ROT = {r: _rotmasks(r) for r in (16, 12, 8, 7)}


def _padd(x, y):
    a = x & _NOTH
    b = y & _NOTH
    s = (a + b) & MASK256
    h = (x ^ y) & _H
    return s ^ h


def _pror(x, r):
    rmask, lmask = _ROT[r]
    t1 = (x >> r) & rmask
    t3 = ((x << (32 - r)) & MASK256) & lmask
    return t1 | t3


def _g(v, a, b, c, d, x, y):
    v[a] = _padd(_padd(v[a], v[b]), x)
    v[d] = _pror(v[d] ^ v[a], 16)
    v[c] = _padd(v[c], v[d])
    v[b] = _pror(v[b] ^ v[c], 12)
    v[a] = _padd(_padd(v[a], v[b]), y)
    v[d] = _pror(v[d] ^ v[a], 8)
    v[c] = _padd(v[c], v[d])
    v[b] = _pror(v[b] ^ v[c], 7)


def _compress_packed(msg_words):
    """msg_words: 16 packed 256-bit words. Returns 8 packed output words o0..o7."""
    v = [_broadcast(x) for x in IV] + [_broadcast(x) for x in IV[:4]] + \
        [_broadcast(0), _broadcast(0), _broadcast(64), _broadcast(11)]
    m = list(msg_words)
    for _ in range(2):
        _g(v, 0, 4, 8, 12, m[0], m[1])
        _g(v, 1, 5, 9, 13, m[2], m[3])
        _g(v, 2, 6, 10, 14, m[4], m[5])
        _g(v, 3, 7, 11, 15, m[6], m[7])
        _g(v, 0, 5, 10, 15, m[8], m[9])
        _g(v, 1, 6, 11, 12, m[10], m[11])
        _g(v, 2, 7, 8, 13, m[12], m[13])
        _g(v, 3, 4, 9, 14, m[14], m[15])
        m = [m[i] for i in PERMUTATION]
    return [v[i] ^ v[i + 8] for i in range(8)]


def _digests_via_swar(messages):
    """messages: list of 64-byte strings (len divisible by 8). Returns list of 32-byte digests."""
    out = []
    for base in range(0, len(messages), 8):
        group = messages[base:base + 8]
        words = [struct.unpack("<16I", m) for m in group]
        packed = []
        for w in range(16):
            acc = 0
            for j in range(8):
                acc |= words[j][w] << (32 * j)
            packed.append(acc)
        o = _compress_packed(packed)
        for j in range(8):
            out.append(b"".join(
                struct.pack("<I", (o[i] >> (32 * j)) & 0xFFFFFFFF) for i in range(8)))
    return out


def _messages(seed, count):
    raw = hashlib.shake_256(b"b3r2-swar-msg|" + seed).digest(64 * count)
    return [raw[i * 64:(i + 1) * 64] for i in range(count)]


def _trial(seed, mask):
    messages = _messages(seed, SAMPLES)
    digests = _digests_via_swar(messages)
    seen = {}
    first = (None, None, 0)
    pairs = 0
    for idx in range(SAMPLES):
        d = int.from_bytes(digests[idx], "big") & mask
        bucket = seen.setdefault(d, [])
        if bucket:
            pairs += len(bucket)
            if first[0] is None:
                first = (messages[bucket[0]].hex(), messages[idx].hex(), idx + 1)
        bucket.append(idx)
    return first[0], first[1], first[2], pairs


def main():
    request = json.loads(sys.stdin.read())
    mask = int(request["event"]["mask_hex"], 16)
    out = []
    for item in request["trials"]:
        a, b, first_index, pairs = _trial(bytes.fromhex(item["seed"]), mask)
        out.append({"trial": item["trial"], "message_a_hex": a, "message_b_hex": b,
                    "observations": {"first_match_sample": first_index, "masked_pairs": pairs}})
    sys.stdout.write(json.dumps({"schema_version": 1, "trials": out}, separators=(",", ":")))


if __name__ == "__main__":
    main()
