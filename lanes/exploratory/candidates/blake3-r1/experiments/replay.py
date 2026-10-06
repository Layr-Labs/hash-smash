"""Deterministic fixed-witness transport for organizer isolation.

The HashSmash organizer runner evaluates this source in its isolated container.
It replays one public pair for every requested trial and provides evidence only
for the selected-target collision relation. It does not reproduce the SAT
construction search or provide attack-cost or probability evidence.

Message words are the z3 model of the collision search documented in proof.md.
"""

import json
import struct
import sys

IV = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
      0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)
PERMUTATION = (2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8)
CHUNK_START, CHUNK_END, PARENT, ROOT = 1, 2, 4, 8
MASK = 0xFFFFFFFF

M1_WORDS = (
    0x00000000, 0x00000000, 0x00000000, 0x00000000,
    0x00000000, 0x00000000, 0x00000000, 0x00000000,
    0x00000000, 0x00000000, 0x00000000, 0x00000000,
    0x00000000, 0x00000000, 0x00000000, 0x00000000,)
M2_WORDS = (
    0xE87690A4, 0xF128E859, 0x7B20970C, 0xCFA0E325,
    0x4740406A, 0x3FA680D2, 0x47F200E9, 0xC8EECCCD,
    0x9E912623, 0x5FBAD526, 0x4D2A3939, 0xDCB634C2,
    0xEBCE4390, 0x39F4ABC2, 0x3466C3AB, 0x1F4569E7,)


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


def _blake3_r1_single_block(block):
    words = struct.unpack("<16I", block)
    return _compress(IV, words, 0, 64, CHUNK_START | CHUNK_END | ROOT, 1)[:8]


def self_check():
    if _blake3_r1_single_block(b"\0" * 64) != (
        0x924A17E9, 0x5B44D964, 0x01A0D272, 0x3F28A25C,
        0xCB0E7C49, 0xB2E49E5D, 0xC6610D02, 0x88BAC908,
    ):
        raise ValueError("internal r1 core self-check failed")
    return {"self_check": "ok"}


def validate_request(request):
    if request.get("schema_version") != 1:
        raise ValueError("unsupported request schema")
    if request.get("target_profile") != "blake3-r1-prefix-v1":
        raise ValueError("unexpected target profile")
    event = request.get("event")
    if event != {"kind": "full-collision"}:
        raise ValueError("unexpected organizer event")
    if type(request.get("max_message_bytes")) is not int or request["max_message_bytes"] < 64:
        raise ValueError("organizer message budget is too small")
    if type(request.get("trials")) is not list:
        raise ValueError("organizer trials list required")
    for index, trial in enumerate(request["trials"]):
        if type(trial) is not dict or set(trial) != {"trial", "seed"}:
            raise ValueError("unexpected organizer trial")
        if type(trial["trial"]) is not int or trial["trial"] != index:
            raise ValueError("organizer trial order invalid")
        seed = trial["seed"]
        if type(seed) is not str or len(seed) != 64:
            raise ValueError("32-byte organizer seed hex required")
        try:
            decoded = bytes.fromhex(seed)
        except ValueError as error:
            raise ValueError("organizer seed hex invalid") from error
        if len(decoded) != 32 or seed != seed.lower():
            raise ValueError("lowercase 32-byte organizer seed hex required")


def main():
    request = json.load(sys.stdin)
    validate_request(request)
    observations = self_check()
    a = struct.pack("<16I", *M1_WORDS)
    b = struct.pack("<16I", *M2_WORDS)
    if a == b:
        raise ValueError("witness messages must be distinct")
    if _blake3_r1_single_block(a) != _blake3_r1_single_block(b):
        raise ValueError("witness digest mismatch")
    rows = [
        {
            "trial": trial["trial"],
            "message_a_hex": a.hex(),
            "message_b_hex": b.hex(),
            "observations": observations,
        }
        for trial in request["trials"]
    ]
    json.dump(
        {"schema_version": 1, "trials": rows},
        sys.stdout,
        separators=(",", ":"),
        sort_keys=True,
    )
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
