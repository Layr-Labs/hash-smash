#!/usr/bin/env python3
"""Build or replay the bounded SHA-256/32 retained-witness certificate."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import sys
from typing import Any

MASK32 = (1 << 32) - 1
IV = (
    0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
    0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19,
)
K = (
    0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5,
    0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5,
    0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3,
    0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174,
    0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC,
    0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
    0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7,
    0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967,
)

# The fixed trail states used by step2_tuple, copied as constants so the replay
# does not execute or import participant attack code. These are ref.h indices
# 8..17 (A steps 4..13) and 12..17 (E steps 8..13).
A_FIXED = (
    (0xB8560DBB, 0x677E1E2A, 0x9BCF7BBE, 0xF8677AD6, 0x4A299906,
     0x44D24AB4, 0x39781650, 0x6C206D58, 0x35C5C2B8, 0x0508C8F0),
    (0x98560DBB, 0x633B16BA, 0x9BCF7BBE, 0xF8677AD6, 0x4A299906,
     0x44F24AB5, 0x39781650, 0x6422EDC8, 0x574542B8, 0x0508C8F0),
)
E_FIXED = (
    (0x11CAE594, 0xD504BF23, 0x7F27D24C, 0xBF893F69, 0x2300F189, 0xFCC08EF5),
    (0xF1CAE594, 0xD0E1B7B4, 0xBF27D74C, 0xB78BBFD9, 0x3FFFD0F9, 0xBF81C0F4),
)
DM_E4 = 0x20000000
DM_W7 = 0x0101108A
DM_W8 = 0x00080C00

CHUNK = 34
BASE_SEED = 202610040000
SEED = 202610040034
COUNTER = 2149248237
LOCAL_TUPLE = 15529
PROCESSED_BEFORE = 14224648
TAIL_INDEX = 131794
TAILS_PER_TUPLE = 196608
PAIR_ORDINAL = 3053257426
TUPLE_RECORD_BYTES = 112
TAIL_RECORD_BYTES = 48
EXPECTED_DIGEST = "f8a3db111360e5ed2e63041ecfa82b01c95a25882910bc0f21671949296a4e77"

EXPECTED = {
    "config": "4a86485d80c3609aa488590273f9aa6b0150120c07a5ce16b620a1bb9e969a22",
    "auditor": "e53f50ee913194b8200a37814d50da6d4aee7bdbf5864a33303c243374788269",
    "terminal_audit": "181b7fe2ba0ce6cfa0bc2733dc6e3f18f385524f1e9100ec7fd05604adf74097",
    "provenance_json": "0083ce59d8b48f325f881a5c16ac325d72c732fbb64f7dac32acba6133bc0685",
    "runner": "4aa2673044202dce8a4da370ab512b8a5ff23cfcc9ac16a179a19a9490595786",
    "organizer_hash_functions": "514fa8ab8a461e4a41080efa27b4ba2a3b499eeedf0a2d2346e6562835d040f5",
    "tuple_file": "c3ea41e428beae328693cef62f32beb8f7753f2a7def98280ecd5cf847ba86ad",
    "tail_file": "1f9f5ba23eff6200ec28c8a57dbce3124d1e8ad3662a5d5b178d5aaf49db18bf",
    "found": "7391e0efe2593fa286e1d67bf512dd5d826c35d4448da3d9690fbc812593b173",
    "pair": "a86aa32fd30b94970ac68ff5067ce40bc759c302507ccdf588dcc6948afeab00",
    "winning_manifest": "1caff8d836e64a58943fbdba16614a8bcf3c40f90e17128b12e50e5ada7cb9ee",
    "tuple_reference": "fe5f32e11caaa550094eae6c7405fb35990f7b9df88fb99d10781df751a55142",
    "step3_receipt": "82e75ba282dc7368d53336232d66cb5dfc6032c448337cbefeb01eca4097e26e",
    "verifier_receipt": "0ca68fe2f14ea4fc5e1d52767f2df0d53d0339ad3359c0815ae203551608cf4c",
    "verification_log": "c2d4e24dfcfefc3ab6e9aed7b58a42e3ff7602a120a547ab02a42d012f66456e",
}
SOURCE_FILES = {
    "attack/c/attack.h": "ace9a72063af7aeec2671f0a2bf32c0e2c21529204b4fdf574672e73bebc0b2c",
    "attack/c/match.c": "4b36aade8a99ded5bfbf153236d8fc88c5db3337c95ff7b96870958f20bfb1fc",
    "attack/c/ref.h": "830a9370e2979b69d4a90bcfbb3eb6ab0a7bd1c398ffe465de9353d727b78672",
    "attack/c/sha.h": "e6085ee7b4ddb912e1310e4b559adf7ebfc947fb8b50f945d7655893e3fda8dc",
    "attack/c/step3.c": "46e93017899e0854f1461e0f6585f4a8cba219b8459ebc938e48cce9bea4b9fc",
    "attack/runner/run_record.sh": EXPECTED["runner"],
    "organizer/verifier/hash_functions.py": EXPECTED["organizer_hash_functions"],
}
TABLE_FILES = {
    "tab2c.bitmap": (536870912, "98fd6221c12edd1910c6b3f8e54c167d590b040602176bfe997992ac5e41c4f2"),
    "tab2c.off": (268435460, "c025cccce8276fef4062b913569040062d3173ff987a9c8c2e9173b8ed00158e"),
    "tab2c.ent": (4873838592, "9d330d0310ab72f641f7aa498a5abc8fc4417fea13e434a6aff9e5d50df7b652"),
    "tab2c.combos": (7471104, "950182cf28c7cb0a46da2af44b7579cdc84829faaf5ad17167d86c399db6369c"),
    "tab2c.lefts": (2174496, "d608b5967525856cb22b609c0bf1b98163860050fd1bd84cb9402d6e17677b34"),
    "tab2c.v7": (2097152, "9e033b43a9c60faf309deda1e7407e6206ac6205c8e22a8399133c7ff9f36d56"),
}
CAMPAIGN_ARTIFACTS = {
    "FOUND": EXPECTED["found"],
    "verified-pairs.txt": EXPECTED["pair"],
    "winning/chunk-34.manifest.tsv": EXPECTED["winning_manifest"],
    "winning/chunk-34.tuple-reference.tsv": EXPECTED["tuple_reference"],
    "audit/operations/step3-attempt-70.tsv": EXPECTED["step3_receipt"],
    "audit/verifiers/verifier-attempt-70.tsv": EXPECTED["verifier_receipt"],
    "verification-attempt-70.log": EXPECTED["verification_log"],
}
CLAIM_SCOPE = {
    "target_profile": "sha256-r32-prefix-v1",
    "algorithm": "SHA-256",
    "compression_steps_per_padded_block": 32,
    "iv": "fixed FIPS 180-4 IV",
    "padding": "standard SHA-256 Merkle-Damgard padding",
    "notion": "ordinary collision",
    "message_bytes_each": 128,
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def read_slice(path: Path, offset: int, size: int) -> bytes:
    with path.open("rb") as stream:
        stream.seek(offset)
        value = stream.read(size)
    require(len(value) == size, f"short read: {path.name}@{offset}+{size}")
    return value


def slice_record(logical_path: str, offset: int, value: bytes) -> dict[str, Any]:
    return {
        "logical_path": logical_path,
        "offset": offset,
        "size_bytes": len(value),
        "sha256": sha256_bytes(value),
        "hex": value.hex(),
    }


def ror(value: int, count: int) -> int:
    return ((value >> count) | (value << (32 - count))) & MASK32


def big_sigma0(value: int) -> int:
    return ror(value, 2) ^ ror(value, 13) ^ ror(value, 22)


def big_sigma1(value: int) -> int:
    return ror(value, 6) ^ ror(value, 11) ^ ror(value, 25)


def small_sigma0(value: int) -> int:
    return ror(value, 7) ^ ror(value, 18) ^ (value >> 3)


def small_sigma1(value: int) -> int:
    return ror(value, 17) ^ ror(value, 19) ^ (value >> 10)


def choose(x: int, y: int, z: int) -> int:
    return ((x & y) ^ (~x & z)) & MASK32


def majority(x: int, y: int, z: int) -> int:
    return (x & y) ^ (x & z) ^ (y & z)


def t2(a: int, b: int, c: int) -> int:
    return (big_sigma0(a) + majority(a, b, c)) & MASK32


def compress32(state: tuple[int, ...], block: bytes) -> tuple[int, ...]:
    require(len(block) == 64, "compression block must be 64 bytes")
    words = list(struct.unpack(">16I", block))
    for index in range(16, 32):
        words.append((small_sigma1(words[index - 2]) + words[index - 7]
                      + small_sigma0(words[index - 15]) + words[index - 16]) & MASK32)
    a, b, c, d, e, f, g, h = state
    for index in range(32):
        first = (h + big_sigma1(e) + choose(e, f, g) + K[index] + words[index]) & MASK32
        second = (big_sigma0(a) + majority(a, b, c)) & MASK32
        a, b, c, d, e, f, g, h = (
            (first + second) & MASK32, a, b, c, (d + first) & MASK32, e, f, g,
        )
    return tuple((old + new) & MASK32 for old, new in zip(state, (a, b, c, d, e, f, g, h)))


def full_message_digest32(data: bytes) -> tuple[bytes, bytes, list[tuple[int, ...]]]:
    padding = b"\x80" + bytes((55 - len(data)) % 64) + (8 * len(data)).to_bytes(8, "big")
    padded = data + padding
    state = IV
    states: list[tuple[int, ...]] = []
    for offset in range(0, len(padded), 64):
        state = compress32(state, padded[offset:offset + 64])
        states.append(state)
    digest = b"".join(word.to_bytes(4, "big") for word in state)
    return digest, padding, states


def trace16(state: tuple[int, ...], words: list[int]) -> tuple[dict[int, int], dict[int, int]]:
    require(len(words) == 16, "trace requires 16 message words")
    a = {-4: state[3], -3: state[2], -2: state[1], -1: state[0]}
    e = {-4: state[7], -3: state[6], -2: state[5], -1: state[4]}
    for index in range(16):
        e[index] = (a[index - 4] + e[index - 4] + big_sigma1(e[index - 1])
                    + choose(e[index - 1], e[index - 2], e[index - 3])
                    + K[index] + words[index]) & MASK32
        a[index] = (e[index] - a[index - 4]
                    + t2(a[index - 1], a[index - 2], a[index - 3])) & MASK32
    return a, e


def splitmix_prefix(seed: int) -> list[int]:
    state = seed
    words: list[int] = []
    for _ in range(7):
        state = (state + 0x9E3779B97F4A7C15) & ((1 << 64) - 1)
        value = state
        value = ((value ^ (value >> 30)) * 0xBF58476D1CE4E5B9) & ((1 << 64) - 1)
        value = ((value ^ (value >> 27)) * 0x94D049BB133111EB) & ((1 << 64) - 1)
        value ^= value >> 31
        words.extend((value >> 32, value & MASK32))
    return words


def derive_witness(tuple_record: bytes, table_slices: dict[str, bytes], tail_record: bytes) -> dict[str, Any]:
    require(len(tuple_record) == TUPLE_RECORD_BYTES, "wrong tuple record size")
    unpacked = struct.unpack("<Q8IQ16I", tuple_record)
    counter = unpacked[0]
    cv = tuple(unpacked[1:9])
    entry = unpacked[9]
    stored_m0 = list(unpacked[10:])

    expected_m0 = splitmix_prefix(SEED) + [counter >> 32, counter & MASK32]
    require(counter == COUNTER, "tuple counter mismatch")
    require(stored_m0 == expected_m0, "tuple M0 does not derive from seed/counter")
    m0_block = struct.pack(">16I", *stored_m0)
    computed_cv = compress32(IV, m0_block)
    require(computed_cv == cv, "stored tuple CV is not C32(IV, M0)")

    bitmap = table_slices["bitmap"]
    offsets = struct.unpack("<2I", table_slices["off"])
    entries = struct.unpack(f"<{len(table_slices['ent']) // 8}Q", table_slices["ent"])
    left = struct.unpack("<4I", table_slices["lefts"])
    combo = struct.unpack("<3I", table_slices["combos"])
    v7 = struct.unpack("<I", table_slices["v7"])[0]
    tail = struct.unpack("<12I", tail_record)

    key = cv[0]
    bucket = key >> 6
    bucket_start, bucket_end = offsets
    require(len(bitmap) == 1 and ((bitmap[0] >> (key & 7)) & 1) == 1, "table bitmap rejects CV key")
    require(bucket_end - bucket_start == len(entries), "bucket offsets disagree with entry slice")
    require(bucket_end - bucket_start <= 736, "bucket exceeds sealed max-bucket ceiling")
    positions = [bucket_start + i for i, value in enumerate(entries) if value == entry]
    require(positions == [550758655], "tuple entry is not uniquely present at sealed bucket position")

    low6 = entry >> 40
    left_index = (entry >> 19) & ((1 << 21) - 1)
    v7_index = entry & ((1 << 19) - 1)
    require(low6 == (key & 63), "entry low-six projection mismatch")
    require(left_index == 9264 and v7_index == 255574, "entry record coordinates changed")
    combo_index, w8, e4, a0 = left
    require(combo_index == 333531, "combo index changed")
    require(tail[10:] == (0, 0), "tail padding words are nonzero")

    branches: list[list[int]] = []
    tail_state_checks: list[dict[str, list[str]]] = []
    for branch in (0, 1):
        a = {-4: cv[3], -3: cv[2], -2: cv[1], -1: cv[0]}
        e = {-4: cv[7], -3: cv[6], -2: cv[5], -1: cv[4]}
        a[0] = a0
        a[1], a[2], a[3] = combo
        for step, value in enumerate(A_FIXED[branch], 4):
            a[step] = value
        for step, value in enumerate(E_FIXED[branch], 8):
            e[step] = value
        for step in range(7, 4, -1):
            e[step] = (a[step] + a[step - 4] - t2(a[step - 1], a[step - 2], a[step - 3])) & MASK32
        e[4] = e4 ^ (DM_E4 if branch else 0)
        expected_w7 = v7 ^ (DM_W7 if branch else 0)
        expected_w8 = w8 ^ (DM_W8 if branch else 0)
        e[3] = (e[7] - a[3] - big_sigma1(e[6]) - choose(e[6], e[5], e[4])
                - K[7] - expected_w7) & MASK32
        for step in range(3):
            e[step] = (a[step] + a[step - 4] - t2(a[step - 1], a[step - 2], a[step - 3])) & MASK32
        words: list[int] = []
        for step in range(14):
            words.append((e[step] - a[step - 4] - e[step - 4] - big_sigma1(e[step - 1])
                          - choose(e[step - 1], e[step - 2], e[step - 3]) - K[step]) & MASK32)
        require(words[7] == expected_w7 and words[8] == expected_w8, "table W7/W8 projection mismatch")
        words.extend(tail[:2])

        traced_a, traced_e = trace16(cv, words)
        expected_states = tail[2:6] if branch == 0 else tail[6:10]
        actual_states = (traced_a[14], traced_e[14], traced_a[15], traced_e[15])
        require(actual_states == expected_states, "tail A/E state projection mismatch")
        branches.append(words)
        tail_state_checks.append({
            "expected": [f"{word:08x}" for word in expected_states],
            "computed": [f"{word:08x}" for word in actual_states],
        })

    message_a = m0_block + struct.pack(">16I", *branches[0])
    message_b = m0_block + struct.pack(">16I", *branches[1])
    require(message_a != message_b, "derived messages are equal")
    digest_a, padding_a, states_a = full_message_digest32(message_a)
    digest_b, padding_b, states_b = full_message_digest32(message_b)
    require(padding_a == padding_b and len(padding_a) == 64, "unexpected standard padding")
    require(states_a[0] == states_b[0] == cv, "first-block state mismatch")
    require(states_a[1] == states_b[1], "second-block states do not collide")
    require(digest_a == digest_b and digest_a.hex() == EXPECTED_DIGEST, "full-message C32 digest mismatch")

    return {
        "counter": counter,
        "cv": list(cv),
        "entry": entry,
        "m0_words": stored_m0,
        "branch_words": branches,
        "tail_words": list(tail),
        "tail_state_checks": tail_state_checks,
        "message_a": message_a,
        "message_b": message_b,
        "padding": padding_a,
        "states_a": states_a,
        "states_b": states_b,
        "digest": digest_a,
        "table_projection": {
            "key": key,
            "bitmap_offset": key >> 3,
            "bucket": bucket,
            "bucket_start": bucket_start,
            "bucket_end": bucket_end,
            "entry_position": positions[0],
            "entry_low6": low6,
            "left_index": left_index,
            "v7_index": v7_index,
            "combo_index": combo_index,
        },
    }


# Immutable certificate payload. Only its committed byte slices are consumed by
# the organizer experiment; no campaign filesystem is available or consulted.
EMBEDDED_CERTIFICATE = json.loads('{"bindings":{"auditor":{"artifact":"evidence/sealed-auditor.py","sha256":"e53f50ee913194b8200a37814d50da6d4aee7bdbf5864a33303c243374788269","size_bytes":324716},"campaign_artifacts":{"FOUND":{"sha256":"7391e0efe2593fa286e1d67bf512dd5d826c35d4448da3d9690fbc812593b173","size_bytes":1693},"audit/operations/step3-attempt-70.tsv":{"sha256":"82e75ba282dc7368d53336232d66cb5dfc6032c448337cbefeb01eca4097e26e","size_bytes":872},"audit/verifiers/verifier-attempt-70.tsv":{"sha256":"0ca68fe2f14ea4fc5e1d52767f2df0d53d0339ad3359c0815ae203551608cf4c","size_bytes":714},"verification-attempt-70.log":{"sha256":"c2d4e24dfcfefc3ab6e9aed7b58a42e3ff7602a120a547ab02a42d012f66456e","size_bytes":582},"verified-pairs.txt":{"sha256":"a86aa32fd30b94970ac68ff5067ce40bc759c302507ccdf588dcc6948afeab00","size_bytes":504},"winning/chunk-34.manifest.tsv":{"sha256":"1caff8d836e64a58943fbdba16614a8bcf3c40f90e17128b12e50e5ada7cb9ee","size_bytes":861},"winning/chunk-34.tuple-reference.tsv":{"sha256":"fe5f32e11caaa550094eae6c7405fb35990f7b9df88fb99d10781df751a55142","size_bytes":496}},"campaign_provenance":{"logical_path":"attack/provenance.json","organizer_base_commit":"fc56c3fa38ac40043d8291649c78148bc4872995","provenance_commit":"d9afb19649446dc89c92c484e82e17139a4d52e8","sha256":"0083ce59d8b48f325f881a5c16ac325d72c732fbb64f7dac32acba6133bc0685"},"config":{"artifact":"evidence/config.tsv","sha256":"4a86485d80c3609aa488590273f9aa6b0150120c07a5ce16b620a1bb9e969a22","size_bytes":2889},"replay_source":{"artifact":"replay.py","sha256":"49d89cdec78081ae6358a69d92a62612afb68a730da11cfe8cf89d7963ba6ee0","size_bytes":39191},"source_files":{"attack/c/attack.h":{"sha256":"ace9a72063af7aeec2671f0a2bf32c0e2c21529204b4fdf574672e73bebc0b2c","size_bytes":7402},"attack/c/match.c":{"sha256":"4b36aade8a99ded5bfbf153236d8fc88c5db3337c95ff7b96870958f20bfb1fc","size_bytes":20159},"attack/c/ref.h":{"sha256":"830a9370e2979b69d4a90bcfbb3eb6ab0a7bd1c398ffe465de9353d727b78672","size_bytes":13480},"attack/c/sha.h":{"sha256":"e6085ee7b4ddb912e1310e4b559adf7ebfc947fb8b50f945d7655893e3fda8dc","size_bytes":1833},"attack/c/step3.c":{"sha256":"46e93017899e0854f1461e0f6585f4a8cba219b8459ebc938e48cce9bea4b9fc","size_bytes":12490},"attack/runner/run_record.sh":{"sha256":"4aa2673044202dce8a4da370ab512b8a5ff23cfcc9ac16a179a19a9490595786","size_bytes":90469},"organizer/verifier/hash_functions.py":{"sha256":"514fa8ab8a461e4a41080efa27b4ba2a3b499eeedf0a2d2346e6562835d040f5","size_bytes":5749}},"terminal_audit":{"artifact":"evidence/terminal-audit.json","sha256":"181b7fe2ba0ce6cfa0bc2733dc6e3f18f385524f1e9100ec7fd05604adf74097","size_bytes":26487}},"checks":[{"id":"sealed-bindings","status":"PASS"},{"id":"retained-tuple-full-hash-offset-record","status":"PASS"},{"id":"seed-counter-and-paid-range","status":"PASS"},{"id":"sealed-table-entry-and-tail-membership","status":"PASS"},{"id":"independent-step2-message-reconstruction","status":"PASS"},{"id":"fixed-iv-standard-padding-c32-collision","status":"PASS"},{"id":"pinned-organizer-reference-cross-check","status":"PASS"},{"id":"emitted-pair-and-terminal-audit-agreement","status":"PASS"}],"claim_scope":{"algorithm":"SHA-256","compression_steps_per_padded_block":32,"iv":"fixed FIPS 180-4 IV","message_bytes_each":128,"notion":"ordinary collision","padding":"standard SHA-256 Merkle-Damgard padding","target_profile":"sha256-r32-prefix-v1"},"coordinates":{"base_seed":202610040000,"chunk":34,"counter":2149248237,"counter_limit_exclusive":68719476736,"global_tuple_index_zero_based":14240177,"local_tuple_index_zero_based":15529,"pair_ordinal_zero_based":3053257426,"processed_tuple_records_before_chunk":14224648,"seed":202610040034,"tail_index_zero_based":131794,"tails_per_tuple":196608,"tuple_record_cap_exclusive":1073741824},"derivation":{"first_block_cv":["e890c4ba","6bce94e6","47a0b812","c5ef36b2","ec7b7814","91cf09df","a9717904","494bc86f"],"first_block_words":["04a9b33e","6ea679aa","89f6fb3b","f530dfa8","c5828a5e","385388a4","0dbcd14f","77252e33","4fef2ad0","809de1a4","a3b955b6","3a95b0cc","5cadb080","01a17ef2","00000000","801aeced"],"post_second_block_common_state":["79389eeb","882fc938","62f355f8","3ebb8d51","4d0b99ce","a01e12ed","7058785b","dae69307"],"second_block_a_words":["e37cab30","5f4048fd","95caa0fc","87591d98","fb8464a3","399cc8f3","6c91c8c4","7d608f34","4ee37252","58e49d82","10746273","a96ce154","45f2222c","4d12f88a","d2701ece","17d9748f"],"second_block_b_words":["e37cab30","5f4048fd","95caa0fc","87591d98","db8464a3","3ddcc0f3","4c91c8c4","7c619fbe","4eeb7e52","58e49d82","10746273","a96ce154","41b22a2c","6d12f88a","d2701ece","17d9748f"],"standard_padding_block_hex":"80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000400","tail_state_checks":[{"computed":["046c2d84","b301a06e","63a3c9fe","ecea3695"],"expected":["046c2d84","b301a06e","63a3c9fe","ecea3695"]},{"computed":["246c2d84","b301a06e","63a3c9fe","ecee3685"],"expected":["246c2d84","b301a06e","63a3c9fe","ecee3685"]}]},"kind":"hashsmash-sha256-r32-witness-certificate-v1","limitations":["This certificate verifies one retained witness and its paid-range coordinates; it does not certify the claimed time, memory, advice, preprocessing, or success-probability accounting.","The 5.69 GB sealed lookup-table corpus is not fully rehashed here. Exact consumed slices are embedded and hashed; full-file hashes are inherited from the hash-bound provenance and terminal audit. The 46.9 MB tuple file and 9.4 MB tail file are fully rehashed.","The replay does not rerun the 2,405,181,685,760 first-block trials or 2,799,733,071,213 tuple-tail trials recorded by the terminal audit."],"membership":{"large_table_files":{"tab2c.bitmap":{"binding":"sealed attack/provenance.json plus exact embedded slice","full_hash_recomputed":false,"sha256":"98fd6221c12edd1910c6b3f8e54c167d590b040602176bfe997992ac5e41c4f2","size_bytes":536870912},"tab2c.combos":{"binding":"sealed attack/provenance.json plus exact embedded slice","full_hash_recomputed":false,"sha256":"950182cf28c7cb0a46da2af44b7579cdc84829faaf5ad17167d86c399db6369c","size_bytes":7471104},"tab2c.ent":{"binding":"sealed attack/provenance.json plus exact embedded slice","full_hash_recomputed":false,"sha256":"9d330d0310ab72f641f7aa498a5abc8fc4417fea13e434a6aff9e5d50df7b652","size_bytes":4873838592},"tab2c.lefts":{"binding":"sealed attack/provenance.json plus exact embedded slice","full_hash_recomputed":false,"sha256":"d608b5967525856cb22b609c0bf1b98163860050fd1bd84cb9402d6e17677b34","size_bytes":2174496},"tab2c.off":{"binding":"sealed attack/provenance.json plus exact embedded slice","full_hash_recomputed":false,"sha256":"c025cccce8276fef4062b913569040062d3173ff987a9c8c2e9173b8ed00158e","size_bytes":268435460},"tab2c.v7":{"binding":"sealed attack/provenance.json plus exact embedded slice","full_hash_recomputed":false,"sha256":"9e033b43a9c60faf309deda1e7407e6206ac6205c8e22a8399133c7ff9f36d56","size_bytes":2097152}},"slices":{"bitmap":{"hex":"66","logical_path":"attack/data/tab2c.bitmap","offset":487725207,"sha256":"252f10c83610ebca1a059c0bae8255eba2f95be4d1d7bcfa89d7248a82d9f111","size_bytes":1},"combos":{"hex":"fc3c8465001c9a583ff02191","logical_path":"attack/data/tab2c.combos","offset":4002372,"sha256":"83b07f07c7c3dc0b89f60996eb4e5416605e5be7a87efba11284b83a828d47f3","size_bytes":12},"ent_bucket":{"hex":"57d603200139000057e683210139000057d603230139000057d643230139000057e603250139000057e643250139000056d60320013a000056e68321013a000056d60323013a000056d64323013a000056e60325013a000056e64325013a000055d60320013d000055e68321013d000055d60323013d000055d64323013d000055e60325013d000055e64325013d000054d60320013e000054e68321013e000054d60323013e000054d64323013e000054e60325013e000054e64325013e0000","logical_path":"attack/data/tab2c.ent","offset":4406069184,"sha256":"0c693bf2212298f07bbdc3382e9aaec5fb85bdec865e281f40aa36c721c3507b","size_bytes":192},"lefts":{"hex":"db1605005272e34e3b0ef229004890a5","logical_path":"attack/data/tab2c.lefts","offset":148224,"sha256":"0e03a0cf0da9781c6c0082ffef14a961cd8e3b348e58c244ff5864acfa39cca8","size_bytes":16},"off":{"hex":"f8e8d32010e9d320","logical_path":"attack/data/tab2c.off","offset":243862600,"sha256":"9bd70a7164f1c913d56ce753ef657441cf877e5da0f87368a5cafc7c7251f7e7","size_bytes":8},"tail":{"hex":"ce1e70d28f74d917842d6c046ea001b3fec9a3639536eaec842d6c246ea001b3fec9a3638536eeec0000000000000000","logical_path":"attack/data/tails.bin","offset":6326112,"sha256":"99aede8f45b63b1d4e30f610e66e913378da989021fb2ff70d4d643d848f20ae","size_bytes":48},"tuple":{"hex":"edec1a8000000000bac490e8e694ce6b12b8a047b236efc514787becdf09cf91047971a96fc84b4956e68321013a00003eb3a904aa79a66e3bfbf689a8df30f55e8a82c5a48853384fd1bc0d332e2577d02aef4fa4e19d80b655b9a3ccb0953a80b0ad5cf27ea10100000000edec1a80","logical_path":"run/pending/chunk-34/full.tuples.bin","offset":1739248,"sha256":"d650d9eb55ae375e9380583c28fd92e37ef31fa8540ff2d7b10a20cc7cb0c51e","size_bytes":112},"v7":{"hex":"348f607d","logical_path":"attack/data/tab2c.v7","offset":1022296,"sha256":"de37a1af6eb38acc68c0ba9bd1d2fd6f5dcb53dc7104dc62ef396806492361ef","size_bytes":4}},"table_projection":{"bitmap_offset":487725207,"bucket":60965650,"bucket_end":550758672,"bucket_start":550758648,"combo_index":333531,"entry_low6":58,"entry_position":550758655,"key":3901801658,"left_index":9264,"v7_index":255574},"tail_file":{"full_hash_recomputed":true,"logical_path":"attack/data/tails.bin","sha256":"1f9f5ba23eff6200ec28c8a57dbce3124d1e8ad3662a5d5b178d5aaf49db18bf","size_bytes":9437184},"tuple_file":{"full_hash_recomputed":true,"logical_path":"run/pending/chunk-34/full.tuples.bin","sha256":"c3ea41e428beae328693cef62f32beb8f7753f2a7def98280ecd5cf847ba86ad","size_bytes":46881968}},"schema_version":1,"status":"PASS","witness":{"common_digest_hex":"f8a3db111360e5ed2e63041ecfa82b01c95a25882910bc0f21671949296a4e77","distinct":true,"message_a_hex":"04a9b33e6ea679aa89f6fb3bf530dfa8c5828a5e385388a40dbcd14f77252e334fef2ad0809de1a4a3b955b63a95b0cc5cadb08001a17ef200000000801aecede37cab305f4048fd95caa0fc87591d98fb8464a3399cc8f36c91c8c47d608f344ee3725258e49d8210746273a96ce15445f2222c4d12f88ad2701ece17d9748f","message_a_sha256":"92e9ab74fd94956893727406209e64ed6645d3af8748c56a8bc45096b7f33a84","message_b_hex":"04a9b33e6ea679aa89f6fb3bf530dfa8c5828a5e385388a40dbcd14f77252e334fef2ad0809de1a4a3b955b63a95b0cc5cadb08001a17ef200000000801aecede37cab305f4048fd95caa0fc87591d98db8464a33ddcc0f34c91c8c47c619fbe4eeb7e5258e49d8210746273a96ce15441b22a2c6d12f88ad2701ece17d9748f","message_b_sha256":"0a3f5c00ffacbceda4fa2dd7092b59b01a34ca865ca589c30c9d8b3858c80da8","organizer_reference_digest_a_hex":"f8a3db111360e5ed2e63041ecfa82b01c95a25882910bc0f21671949296a4e77","organizer_reference_digest_b_hex":"f8a3db111360e5ed2e63041ecfa82b01c95a25882910bc0f21671949296a4e77"}}')


def embedded_slice(name: str) -> bytes:
    record = EMBEDDED_CERTIFICATE["membership"]["slices"][name]
    value = bytes.fromhex(record["hex"])
    require(len(value) == record["size_bytes"], f"embedded slice size mismatch: {name}")
    require(sha256_bytes(value) == record["sha256"], f"embedded slice hash mismatch: {name}")
    return value


def derive_embedded_witness() -> tuple[bytes, bytes]:
    certificate = EMBEDDED_CERTIFICATE
    require(certificate.get("schema_version") == 1, "wrong embedded certificate schema")
    require(certificate.get("kind") == "hashsmash-sha256-r32-witness-certificate-v1",
            "wrong embedded certificate kind")
    require(certificate.get("status") == "PASS", "embedded certificate is not PASS")
    require(certificate.get("claim_scope") == CLAIM_SCOPE, "embedded claim scope mismatch")

    table_slices = {
        "bitmap": embedded_slice("bitmap"),
        "off": embedded_slice("off"),
        "ent": embedded_slice("ent_bucket"),
        "lefts": embedded_slice("lefts"),
        "combos": embedded_slice("combos"),
        "v7": embedded_slice("v7"),
    }
    derived = derive_witness(
        embedded_slice("tuple"), table_slices, embedded_slice("tail")
    )
    first, second = derived["message_a"], derived["message_b"]
    witness = certificate["witness"]
    require(first != second, "derived messages are equal")
    require(derived["digest"].hex() == EXPECTED_DIGEST, "derived digest changed")
    require(first.hex() == witness["message_a_hex"], "derived message A changed")
    require(second.hex() == witness["message_b_hex"], "derived message B changed")
    require(sha256_bytes(first) == witness["message_a_sha256"], "message A binding changed")
    require(sha256_bytes(second) == witness["message_b_sha256"], "message B binding changed")
    require(certificate["membership"]["table_projection"] == derived["table_projection"],
            "table projection changed")
    return first, second


M_256 = (1 << 256) - 1
M_31 = int("7fffffff" * 8, 16)
M_MSB = int("80000000" * 8, 16)

# This Python evaluator is a finite functional spot-check, not a source-operator
# cost trace.  Its explicit M_256 truncations emulate automatic fixed-width
# word-RAM register truncation, and its locally constructed shift masks represent
# fixed public constants loaded once by the abstract algorithm.


def add32x8(x: int, y: int) -> int:
    return (((x & M_31) + (y & M_31)) ^ ((x ^ y) & M_MSB)) & M_256


def csa32x8(x: int, y: int, z: int) -> tuple[int, int]:
    t = x ^ y
    s = t ^ z
    c = (((x & y) | (t & z)) & M_31) << 1
    return s & M_256, c & M_256


def shr32x8(x: int, k: int) -> int:
    mask_lane = (1 << (32 - k)) - 1
    mask256 = sum(mask_lane << (32 * l) for l in range(8))
    return (x >> k) & mask256


def rotr32x8(x: int, r: int) -> int:
    mask_lo = (1 << (32 - r)) - 1
    mask_hi = ((1 << 32) - 1) ^ mask_lo
    m_lo256 = sum(mask_lo << (32 * l) for l in range(8))
    m_hi256 = sum(mask_hi << (32 * l) for l in range(8))
    return (((x >> r) & m_lo256) | ((x << (32 - r)) & m_hi256)) & M_256


def swar_small_sigma0(x: int) -> int:
    return rotr32x8(x, 7) ^ rotr32x8(x, 18) ^ shr32x8(x, 3)


def swar_small_sigma1(x: int) -> int:
    return rotr32x8(x, 17) ^ rotr32x8(x, 19) ^ shr32x8(x, 10)


def swar_big_sigma0(x: int) -> int:
    return rotr32x8(x, 2) ^ rotr32x8(x, 13) ^ rotr32x8(x, 22)


def swar_big_sigma1(x: int) -> int:
    return rotr32x8(x, 6) ^ rotr32x8(x, 11) ^ rotr32x8(x, 25)


def pack8(lanes: list[int] | tuple[int, ...]) -> int:
    return sum((lanes[l] & MASK32) << (32 * l) for l in range(8))


def unpack8(word256: int) -> tuple[int, ...]:
    return tuple((word256 >> (32 * l)) & MASK32 for l in range(8))


LANES7, LANE_BITS7 = 7, 36
M_32x7 = sum(MASK32 << (LANE_BITS7 * l) for l in range(LANES7))


def shr_mask7(k: int) -> int:
    lane_m = (1 << (32 - k)) - 1
    return sum(lane_m << (LANE_BITS7 * l) for l in range(LANES7))


def rotr_masks7(r: int) -> tuple[int, int]:
    lo = (1 << (32 - r)) - 1
    hi = MASK32 ^ lo
    return (
        sum(lo << (LANE_BITS7 * l) for l in range(LANES7)),
        sum(hi << (LANE_BITS7 * l) for l in range(LANES7)),
    )


SHR_MASKS7 = {k: shr_mask7(k) for k in (3, 10)}
ROTR_MASKS7 = {r: rotr_masks7(r) for r in (2, 6, 7, 11, 13, 17, 18, 19, 22, 25)}
IV7 = [sum(w << (LANE_BITS7 * l) for l in range(LANES7)) for w in IV]
K7 = [sum(w << (LANE_BITS7 * l) for l in range(LANES7)) for w in K]


class Swar7Counter:
    def __init__(self) -> None:
        self.ops = {
            "rand_and_mask": 0,
            "schedule": 0,
            "rounds": 0,
            "feedforward": 0,
            "extract": 0,
        }
        self.section = "rand_and_mask"
        self.max_lane = 0

    def _record(self, val: int) -> int:
        res = val & M_256
        for l in range(LANES7):
            lv = (res >> (LANE_BITS7 * l)) & ((1 << LANE_BITS7) - 1)
            if lv > self.max_lane:
                self.max_lane = lv
        self.ops[self.section] += 1
        return res

    def rand256(self, raw: int) -> int:
        return self._record(raw)

    def add(self, a: int, b: int) -> int:
        return self._record(a + b)

    def xor(self, a: int, b: int) -> int:
        return self._record(a ^ b)

    def bit_and(self, a: int, b: int) -> int:
        return self._record(a & b)

    def bit_or(self, a: int, b: int) -> int:
        return self._record(a | b)

    def shl(self, a: int, k: int) -> int:
        return self._record(a << k)

    def shr(self, a: int, k: int) -> int:
        return self._record(a >> k)

    def rotr(self, x: int, r: int) -> int:
        m_lo, m_hi = ROTR_MASKS7[r]
        lo = self.bit_and(self.shr(x, r), m_lo)
        hi = self.bit_and(self.shl(x, 32 - r), m_hi)
        return self.bit_or(lo, hi)

    def shr_lane(self, x: int, k: int) -> int:
        return self.bit_and(self.shr(x, k), SHR_MASKS7[k])

    def small_sigma0(self, x: int) -> int:
        return self.xor(self.xor(self.rotr(x, 7), self.rotr(x, 18)), self.shr_lane(x, 3))

    def small_sigma1(self, x: int) -> int:
        return self.xor(self.xor(self.rotr(x, 17), self.rotr(x, 19)), self.shr_lane(x, 10))

    def big_sigma0(self, x: int) -> int:
        return self.xor(self.xor(self.rotr(x, 2), self.rotr(x, 13)), self.rotr(x, 22))

    def big_sigma1(self, x: int) -> int:
        return self.xor(self.xor(self.rotr(x, 6), self.rotr(x, 11)), self.rotr(x, 25))


# The charged batch on the cost model's 256-bit word RAM with 64 registers (the machine of the
# promoted blake3-r2 52bb50ee and of our r31 028aa8d0).  Every value is a register; a load or a
# store costs the access plus one address operation.  Values are SSA names; the peak number of
# simultaneously live names must stay within 64.
class Reg64:
    def __init__(self) -> None:
        self.ops = {"arith": 0, "load": 0, "store": 0, "addr": 0}
        self.section = "rand_and_mask"
        self.sections: dict[str, int] = {}
        self.max_sum = 0
        self.t = 0
        self.val: list[int] = []
        self.born: list[int] = []
        self.last: list[int] = []

    def _def(self, value: int, *srcs: int) -> int:
        self.t += 1
        for v in srcs:
            self.last[v] = self.t
        self.val.append(value & M_256)
        self.born.append(self.t)
        self.last.append(self.t)
        return len(self.val) - 1

    def _arith(self, value: int, *srcs: int) -> int:
        self.ops["arith"] += 1
        self.sections[self.section] = self.sections.get(self.section, 0) + 1
        return self._def(value, *srcs)

    def rand(self, raw: int) -> int:
        return self._arith(raw)

    def load(self, value: int) -> int:
        self.ops["load"] += 1
        self.ops["addr"] += 1
        return self._def(value)

    def store(self, v: int) -> None:
        self.ops["store"] += 1
        self.ops["addr"] += 1
        self.t += 1
        self.last[v] = self.t

    def add(self, a: int, b: int) -> int:
        x, y = self.val[a], self.val[b]
        out = self._arith(x + y, a, b)
        lane = (1 << LANE_BITS7) - 1
        for l in range(LANES7):
            s = ((x >> (LANE_BITS7 * l)) & lane) + ((y >> (LANE_BITS7 * l)) & lane)
            require(s == (self.val[out] >> (LANE_BITS7 * l)) & lane, "64-register lane carry")
            self.max_sum = max(self.max_sum, s)
        return out

    def xor(self, a: int, b: int) -> int:
        return self._arith(self.val[a] ^ self.val[b], a, b)

    def band(self, a: int, b: int) -> int:
        return self._arith(self.val[a] & self.val[b], a, b)

    def shr(self, a: int, k: int) -> int:
        return self._arith(self.val[a] >> k, a)

    def shl(self, a: int, k: int) -> int:
        return self._arith(self.val[a] << k, a)

    def peak_live(self) -> int:
        delta = [0] * (self.t + 2)
        for b, l in zip(self.born, self.last):
            delta[b] += 1
            delta[l + 1] -= 1
        live = peak = 0
        for d in delta:
            live += d
            peak = max(peak, live)
        return peak


REG64_PERSISTENT = 8


def replicate7(word: int) -> int:
    return sum((word & MASK32) << (LANE_BITS7 * l) for l in range(LANES7))


def lane_lo(r: int) -> int:
    return replicate7((1 << (32 - r)) - 1)


def lane_hi(r: int) -> int:
    return replicate7(((1 << r) - 1) << (32 - r))


def merged_mask_ok(terms, mask_lo: int, mask_hi: int) -> None:
    """One mask serves several shifted copies of a lane value whose guard bits are 0: every term is
    correct or zero on every kept bit, and every correct bit of every term is kept (r31 028aa8d0)."""
    keep = range(mask_lo, mask_hi + 1)
    for kind, r in terms:
        good, zero = (range(0, 32 - r), range(32 - r, 36 - r)) if kind == "R" else (range(32 - r, 32), range(28 - r, 32 - r))
        require(set(good) <= set(keep), "merged mask drops a correct bit")
        require(all(p in good or p in zero for p in keep), "merged mask keeps a wrong bit")


merged_mask_ok([("R", 17), ("R", 19)], 0, 14)
merged_mask_ok([("L", 17), ("L", 19)], 13, 31)
merged_mask_ok([("R", 3), ("R", 7)], 0, 28)


def verify_reg64_batch(raw_words: list[int], scalar_cvs7: list[tuple[int, ...]]) -> dict[str, int]:
    g = Reg64()
    mask = {"M": g.load(M_32x7)}
    for r in (2, 13, 22, 6, 11, 25):
        mask[f"LO{r}"], mask[f"HI{r}"] = g.load(lane_lo(r)), g.load(lane_hi(r))
    for name, value in (("LO17", lane_lo(17)), ("HI19", lane_hi(19)), ("LO10", lane_lo(10)), ("LO3", lane_lo(3)),
                        ("HI7", lane_hi(7)), ("LO18", lane_lo(18)), ("HI18", lane_hi(18))):
        mask[name] = g.load(value)
    M = mask["M"]

    def rot(x: int, r: int) -> int:
        return g.xor(g.band(g.shr(x, r), mask[f"LO{r}"]), g.band(g.shl(x, 32 - r), mask[f"HI{r}"]))

    def big0(x: int) -> int:
        return g.xor(g.xor(rot(x, 2), rot(x, 13)), rot(x, 22))

    def big1(x: int) -> int:
        return g.xor(g.xor(rot(x, 6), rot(x, 11)), rot(x, 25))

    def small1(x: int) -> int:
        right = g.band(g.xor(g.shr(x, 17), g.shr(x, 19)), mask["LO17"])
        left = g.band(g.xor(g.shl(x, 15), g.shl(x, 13)), mask["HI19"])
        return g.xor(g.xor(right, left), g.band(g.shr(x, 10), mask["LO10"]))

    def small0(x: int) -> int:
        a = g.band(g.xor(g.shr(x, 3), g.shr(x, 7)), mask["LO3"])
        b = g.band(g.shl(x, 25), mask["HI7"])
        c = g.band(g.shr(x, 18), mask["LO18"])
        d = g.band(g.shl(x, 14), mask["HI18"])
        return g.xor(g.xor(g.xor(a, b), c), d)

    a0, b0, c0, d0, e0, f0, g0, h0 = IV
    w: dict[int, int] = {}
    g.section = "rand_and_mask"
    for i in range(16):
        w[i] = g.band(g.rand(raw_words[i]), M)
        g.store(w[i])                       # M0 is kept: the winning trial must output it

    def word(i: int) -> int:
        if i >= 16 and i not in w:
            g.section = "schedule"
            t = g.add(g.add(g.add(small1(w[i - 2]), w[i - 7]), small0(w[i - 15])), w[i - 16])
            w[i] = g.band(t, M)
            g.section = "rounds"
        return w[i]

    g.section = "rounds"
    t1 = g.add(g.load(replicate7(h0 + big_sigma1(e0) + choose(e0, f0, g0) + K[0])), word(0))
    e_n = g.band(g.add(g.load(replicate7(d0)), t1), M)
    a_n = g.band(g.add(t1, g.load(replicate7(big_sigma0(a0) + majority(a0, b0, c0)))), M)
    sa, se = a_n, e_n
    S1 = big1(se)
    ch = g.xor(g.load(replicate7(f0)), g.band(se, g.load(replicate7(e0 ^ f0))))
    S0 = big0(sa)
    mj = g.xor(g.band(sa, g.load(replicate7(a0 ^ b0))), g.load(replicate7(a0 & b0)))
    t1 = g.add(g.add(g.add(g.load(replicate7(g0 + K[1])), S1), ch), word(1))
    e_n = g.band(g.add(g.load(replicate7(c0)), t1), M)
    a_n = g.band(g.add(g.add(t1, S0), mj), M)
    A0, B0, E0 = g.load(replicate7(a0)), g.load(replicate7(b0)), g.load(replicate7(e0))
    sa, sb, sc, sd, se, sf, sg = a_n, sa, A0, B0, e_n, se, E0
    S1 = big1(se)
    ch = g.xor(sg, g.band(se, g.xor(sf, sg)))
    S0 = big0(sa)
    xab = g.xor(sa, sb)
    mj = g.xor(sb, g.band(xab, g.xor(sb, sc)))
    t1 = g.add(g.add(g.add(g.load(replicate7(f0 + K[2])), S1), ch), word(2))
    e_n = g.band(g.add(sd, t1), M)
    a_n = g.band(g.add(g.add(t1, S0), mj), M)
    prev_ab = xab
    sa, sb, sc, sd, se, sf, sg, sh = a_n, sa, sb, sc, e_n, se, sf, sg
    for i in range(3, 32):
        S1 = big1(se)
        ch = g.xor(sg, g.band(se, g.xor(sf, sg)))
        S0 = big0(sa)
        xab = g.xor(sa, sb)
        mj = g.xor(sb, g.band(xab, prev_ab))
        t1 = g.add(g.add(g.add(g.add(sh, S1), ch), g.load(K7[i])), word(i))
        e_n = g.band(g.add(sd, t1), M)
        a_n = g.band(g.add(g.add(t1, S0), mj), M)
        prev_ab = xab
        sa, sb, sc, sd, se, sf, sg, sh = a_n, sa, sb, sc, e_n, se, sf, sg
    g.section = "feedforward"
    state = (sa, sb, sc, sd, se, sf, sg, sh)
    out = [g.band(g.add(g.load(IV7[j]), state[j]), M) for j in range(8)]
    g.section = "extract"
    cv0 = []
    m32 = g.load(MASK32)
    for l in range(LANES7):
        cv0.append(g.band(g.shr(out[0], LANE_BITS7 * l), m32))
    for v in cv0:
        g.store(v)
    for j in range(1, 8):
        g.store(out[j])
    stored = [g.val[out[j]] for j in range(8)]
    for l in range(LANES7):
        got = (g.val[cv0[l]],) + tuple((stored[j] >> (LANE_BITS7 * l)) & MASK32 for j in range(1, 8))
        require(got == scalar_cvs7[l], "64-register 7-lane SWAR C_32 mismatch")
    require(g.sections == {"rand_and_mask": 32, "schedule": 464, "rounds": 1521, "feedforward": 16, "extract": 14},
            f"unexpected 64-register arithmetic counts: {g.sections}")
    require(g.ops == {"arith": 2047, "load": 71, "store": 30, "addr": 101},
            f"unexpected 64-register op counts: {g.ops}")
    # Registers held across the batch: one table base, the batch counter, the outer loop's work counter, cap, trial
    # counter, offset-array base and TAB2 base, and one address temporary.
    require(g.peak_live() + REG64_PERSISTENT <= 64, f"64-register batch needs {g.peak_live()} + {REG64_PERSISTENT}")
    require(g.max_sum < (1 << LANE_BITS7), "64-register lane sum reached 2^36")
    return {"reg64_arith_ops": g.ops["arith"], "reg64_traffic_ops": g.ops["load"] + g.ops["store"] + g.ops["addr"],
            "reg64_peak_live": g.peak_live(), "reg64_max_lane_sum_bits": g.max_sum.bit_length()}


# PC-4 of the table builder, itemised (proof Section 8.1, "PC-4 itemised"): the literal per-(LEFT row, W7) predicates
# AeqP(3,3), EeqP(7,7) and the sigma0 cancellation do not depend on w7 once w7 has the fixed signs of L7, and the
# hoisted e3 = X - w7, am1 = e3 + Y equal the literal ones.  Checked on organizer-seeded random rows: each residual
# (left side minus right side of the test) must be identical for two different sign-valid w7.
PC4_ROWS = {
    "A3": "=" * 32, "Am1": "=" * 32, "E3": "=====1=====011======0======0====",
    "E4": "==n0=0=1===100=0==0=1===0==1=0=1", "E5": "01011u001n=nuu=11000n=1=101u=100",
    "E6": "101n=0=1=1=n1111==n0u===n=0n=n=u", "E7": "10u0=1=101==00=n==0=0===0==0=0=0",
    "W7": "=======n=======u===u====u=1=u=u=", "W8": "============u=======uu==========",
}


def pc4_flip(row: str) -> int:
    return sum(1 << (31 - k) for k, c in enumerate(row) if c in "nu")


def pc4_signs(row: str) -> tuple[int, int]:
    mask = value = 0
    for k, c in enumerate(row):
        if c in "nu":
            mask |= 1 << (31 - k)
            if c == "u":
                value |= 1 << (31 - k)
    return mask, value


def verify_pc4_hoist(seed_hex: str, rows: int = 64) -> dict[str, int]:
    fl = {name: pc4_flip(row) for name, row in PC4_ROWS.items()}
    require(fl["A3"] == fl["Am1"] == fl["E3"] == 0, "rows A3, A[-1], E3 must carry no difference")
    smask, svalue = pc4_signs(PC4_ROWS["W7"])
    stream = hashlib.shake_256(bytes.fromhex(seed_hex) + b"pc4").digest(48 * rows)
    for t in range(rows):
        a0, a1, a2, a3, e4, e5, e6, e7, w8, r1, r2, _ = struct.unpack(">12I", stream[48 * t:48 * t + 48])
        w7s = [(r & ~smask & MASK32) | svalue for r in (r1, r2)]
        require(w7s[0] != w7s[1], "need two different w7")
        e4p, e5p, e6p, e7p = e4 ^ fl["E4"], e5 ^ fl["E5"], e6 ^ fl["E6"], e7 ^ fl["E7"]
        w8p = w8 ^ fl["W8"]
        X = (e7 - a3 - big_sigma1(e6) - choose(e6, e5, e4) - K[7]) & MASK32
        Y = (big_sigma0(a2) + majority(a2, a1, a0) - a3) & MASK32
        residuals = []
        for w7 in w7s:
            w7p = w7 ^ fl["W7"]
            e3 = (e7 - a3 - w7 - big_sigma1(e6) - choose(e6, e5, e4) - K[7]) & MASK32
            am1 = (e3 - a3 + big_sigma0(a2) + majority(a2, a1, a0)) & MASK32
            require(e3 == (X - w7) & MASK32 and am1 == (e3 + Y) & MASK32, "hoisted e3/am1 differ")
            e3p, am1p = e3 ^ fl["E3"], am1 ^ fl["Am1"]
            a3_calc = (e3p - am1p + big_sigma0(a2) + majority(a2, a1, a0)) & MASK32
            e7_calc = (a3 + e3p + big_sigma1(e6p) + choose(e6p, e5p, e4p) + K[7] + w7p) & MASK32
            cancel = (small_sigma0(w8p) + w7p - small_sigma0(w8) - w7) & MASK32
            residuals.append(((a3_calc ^ a3 ^ fl["A3"]), (e7_calc - e7p) & MASK32, cancel))
        require(residuals[0] == residuals[1], "a PC-4 row predicate depends on w7")
    return {"l1_pc4_rows_checked": rows}

# Step 2 from the record word (proof Sections 4, 8 B): only the low 32 bits of a register matter, so values are masked
# only before a right shift or a full compare; every operation is counted, a load with its address operation.
STEP2_ROWS = {"W4": "==n" + "=" * 29, "W5": "=====u===u==========n===========", "W6": "==n" + "=" * 29,
              "W12": "=====n===n==========u===========", "W13": "==u" + "=" * 29,
              "W20": "=====0=nn=====0=u=1============="}
ADVICE_W12 = 0x41B22A2C
STEP2_CHARGES = {"preamble": 21, "t1": 48, "t2": 47, "t3": 47}


def modular_d(row: str) -> int:
    return sum((1 << (31 - k)) if c == "n" else -(1 << (31 - k)) for k, c in enumerate(row) if c in "nu") & MASK32


# v11 (proof Section 4): W' = W + D for words 4..6, no sign tests, (b') (g') (f'): s0(W + D) - s0(W) = T.
D4, D5, D6 = (modular_d(STEP2_ROWS[w]) for w in ("W4", "W5", "W6"))
T4 = (ADVICE_W12 - (ADVICE_W12 ^ pc4_flip(STEP2_ROWS["W12"]))) & MASK32
T5 = (modular_d(STEP2_ROWS["W20"]) - modular_d(STEP2_ROWS["W13"]) - D4) & MASK32
T6 = -D5 & MASK32
require((D4, D5, D6, T4, T5, T6) == (0x20000000, 0xFBC00800, 0x20000000, 0xFBC00800, 0x017F8000, 0x043FF800),
        "relaxed Step-2 constants")


def record_word0(a0: int, a1: int, a2: int, e3: int, e4: int, e5: int, e6: int, am1: int) -> int:
    fields = (
        (a1 - big_sigma0(a0) - (a0 & am1)) & MASK32,                              # R1
        a0 ^ am1,                                                                  # Q1
        (a2 - big_sigma0(a1) - majority(a1, a0, am1)) & MASK32,                   # R2
        e3,                                                                        # E3
        (e4 - 2 * a0 + big_sigma0(am1) - big_sigma1(e3) - K[4]) & MASK32,        # R4
        (e5 - a1 - big_sigma1(e4) - (e4 & e3) - K[5]) & MASK32,                   # R5
        ~e4 & MASK32,                                                              # N4
        (e6 - a2 - big_sigma1(e5) - choose(e5, e4, e3) - K[6]) & MASK32,          # R6
    )
    return sum(v << (32 * i) for i, v in enumerate(fields))


class Step2Prog:
    def __init__(self) -> None:
        self.ops: dict[str, int] = {}
        self.tranche = ""

    def _n(self, value: int, n: int = 1) -> int:
        self.ops[self.tranche] = self.ops.get(self.tranche, 0) + n
        return value & M_256

    def load(self, value: int) -> int:
        return self._n(value, 2)

    def add(self, x: int, y: int) -> int:
        return self._n(x + y)

    def sub(self, x: int, y: int) -> int:
        return self._n(x - y)

    def band(self, x: int, y: int) -> int:
        return self._n(x & y)

    def xor(self, x: int, y: int) -> int:
        return self._n(x ^ y)

    def shr(self, x: int, k: int) -> int:
        return self._n(x >> k)

    def shl(self, x: int, k: int) -> int:
        return self._n(x << k)

    def sigma0(self, x: int) -> int:
        require(x == x & MASK32, "sigma0 input must be masked")
        return self._n(small_sigma0(x), 14)

    def test(self, x: int, y: int) -> bool:
        require(x == x & MASK32 and y == y & MASK32, "compared values must be masked")
        self._n(0, 2)  # compare and branch
        return x == y

    def cap_check(self, env: int, counter: int) -> int:
        # the work counter advances by exactly the tranche's charge
        require(env == STEP2_CHARGES[self.tranche], "cap-check envelope differs from the charge")
        counter = self.add(counter, env)
        self._n(0, 2)  # compare with the cap, branch
        return counter


# v13: D = 2^29 gives x + D = x xor Delta, Delta >> 29 in {1, 3, 7, 15}: one table load replaces a sigma0.
SIG0_DELTA = {k: small_sigma0((k << 29) & MASK32) for k in (1, 3, 7, 15)}


def relaxed_ok(x: int, d: int, t: int) -> bool:
    return (small_sigma0((x + d) & MASK32) - small_sigma0(x)) & MASK32 == t


def step2_tranches(g: Step2Prog, vectors: list[int], lane: int, am1: int, word0: int) -> dict[str, int]:
    one, counter = 1, 0
    g.tranche = "preamble"
    v1, v2, v3 = (g.load(vectors[j]) for j in (1, 2, 3))
    s = g.add(g.shl(lane, 5), g.shl(lane, 2))
    b, c, d = g.shr(v1, s), g.shr(v2, s), g.shr(v3, s)
    k0 = g.sub(d, g.xor(b, g.band(g.xor(am1, b), g.xor(b, c))))
    env48, env47 = g.load(48), g.load(47)

    def relaxed_test(x: int, dd: int, tt: int) -> bool:
        xm = g.band(x, MASK32)
        sx = g.sigma0(xm)
        if dd == 1 << 29:
            delta = g.xor(g.add(xm, g.shl(one, 29)), xm)     # D = 1 << 29 from the register holding 1
            off = g.shr(delta, 24)                          # entry offset 32 (Delta >> 29)
            require(off >> 5 in SIG0_DELTA and off & 31 == 0, "unexpected Delta")
            g.add(g.load(0), off)                           # table base, address
            sp = g.xor(sx, g._n(SIG0_DELTA[off >> 5]))      # the entry's load
        else:
            sp = g.sigma0(g.band(g.add(xm, g.load(dd)), MASK32))
        return g.test(g.band(g.sub(sp, sx), MASK32), g.load(tt))

    g.tranche = "t1"
    counter = g.cap_check(env48, counter)
    w = g.load(word0)
    q1, r2, e3, r4 = g.shr(w, 32), g.shr(w, 64), g.shr(w, 96), g.shr(w, 128)
    e1 = g.sub(g.add(w, c), g.band(b, q1))
    e2 = g.add(r2, b)
    w4 = g.sub(g.sub(r4, k0), g.xor(e1, g.band(e3, g.xor(e2, e1))))
    pass_b = relaxed_test(w4, D4, T4)
    g.tranche = "t2"
    counter = g.cap_check(env47, counter)
    w5 = g.sub(g.sub(g.shr(w, 160), e1), g.band(g.shr(w, 192), e2))
    pass_g = relaxed_test(w5, D5, T5)
    g.tranche = "t3"
    counter = g.cap_check(env47, counter)
    w6 = g.sub(g.shr(w, 224), e2)
    pass_f = relaxed_test(w6, D6, T6)
    return {"b": b & MASK32, "c": c & MASK32, "d": d & MASK32, "E1": e1 & MASK32, "E2": e2 & MASK32,
            "W4": w4 & MASK32, "W5": w5 & MASK32, "W6": w6 & MASK32, "pass": (pass_b, pass_g, pass_f)}


def step2_direct(cv: tuple[int, ...], a0: int, a1: int, a2: int, e3: int, e4: int, e5: int, e6: int) -> dict:
    am1, am2, am3, am4 = cv[:4]
    e0 = (a0 + am4 - big_sigma0(am1) - majority(am1, am2, am3)) & MASK32
    e1 = (a1 + am3 - big_sigma0(a0) - majority(a0, am1, am2)) & MASK32
    e2 = (a2 + am2 - big_sigma0(a1) - majority(a1, a0, am1)) & MASK32
    w4 = (e4 - a0 - e0 - big_sigma1(e3) - choose(e3, e2, e1) - K[4]) & MASK32
    w5 = (e5 - a1 - e1 - big_sigma1(e4) - choose(e4, e3, e2) - K[5]) & MASK32
    w6 = (e6 - a2 - e2 - big_sigma1(e5) - choose(e5, e4, e3) - K[6]) & MASK32
    passes = (relaxed_ok(w4, D4, T4), relaxed_ok(w5, D5, T5), relaxed_ok(w6, D6, T6))
    return {"E1": e1, "E2": e2, "W4": w4, "W5": w5, "W6": w6, "pass": passes}


def char_inclusion_checks(stream: bytes) -> int:
    n = 0
    for i in range(0, len(stream) - 3, 4):
        x = struct.unpack(">I", stream[i:i + 4])[0]
        for hi in (0, 1, 3, 7):                             # every carry length of x + 2^29
            y = (x & ~(7 << 29) & MASK32) | (hi << 29)
            dl = ((y + (1 << 29)) ^ y) >> 29
            require(small_sigma0((y + (1 << 29)) & MASK32) == small_sigma0(y) ^ SIG0_DELTA[dl], "sigma0 table")
        for row, dd, tt in (("W4", D4, T4), ("W5", D5, T5), ("W6", D6, T6)):
            m, v = pc4_signs(STEP2_ROWS[row])
            y = (x & ~m & MASK32) | v
            fl = pc4_flip(STEP2_ROWS[row])
            require((y + dd) & MASK32 == y ^ fl, "W + D differs from W xor FL on a characteristic word")
            require(relaxed_ok(y, dd, tt) == ((small_sigma0(y ^ fl) - small_sigma0(y)) & MASK32 == tt),
                    "relaxed test differs from the characteristic test on a characteristic word")
            n += 1
    return n


def verify_step2_fields(seed_hex: str, vectors: list[int], cvs7: list[tuple[int, ...]]) -> dict[str, int]:
    stream = hashlib.shake_256(bytes.fromhex(seed_hex) + b"step2").digest(28 * LANES7)
    cases = []
    for l in range(LANES7):
        tup = struct.unpack(">7I", stream[28 * l:28 * l + 28])
        cases.append((vectors, l, cvs7[l], tup, None))
    der = EMBEDDED_CERTIFICATE["derivation"]
    cv = tuple(int(x, 16) for x in der["first_block_cv"])
    w = [int(x, 16) for x in der["second_block_b_words"]]          # unprimed (S's M'_1 naming, Section 2)
    wp = [int(x, 16) for x in der["second_block_a_words"]]
    a, e = list(cv[3::-1]), list(cv[7:3:-1])                     # A[-4..-1], E[-4..-1]
    for i in range(7):
        t1 = (e[i] + big_sigma1(e[i + 3]) + choose(e[i + 3], e[i + 2], e[i + 1]) + K[i] + w[i]) & MASK32
        e.append((a[i] + t1) & MASK32)
        a.append((t1 + big_sigma0(a[i + 3]) + majority(a[i + 3], a[i + 2], a[i + 1])) & MASK32)
    cert = (a[4], a[5], a[6], e[7], e[8], e[9], e[10])           # A0, A1, A2, E3, E4, E5, E6
    rnd = struct.unpack(">8I", hashlib.shake_256(bytes.fromhex(seed_hex) + b"step2-lanes").digest(32))
    cert_vecs = [sum(((cv[j] if l == 3 else rnd[(j + l) % 8]) << (LANE_BITS7 * l)) for l in range(LANES7))
                 for j in range(8)]
    cases.append((cert_vecs, 3, cv, cert, w))
    for vecs, lane, cvl, tup, words in cases:
        g = Step2Prog()
        a0, a1, a2, e3, e4, e5, e6 = tup
        got = step2_tranches(g, vecs, lane, cvl[0], record_word0(a0, a1, a2, e3, e4, e5, e6, cvl[0]))
        want = step2_direct(cvl, *tup)
        require((got["b"], got["c"], got["d"]) == cvl[1:4], "preamble CV1[1..3] mismatch")
        require(all(got[k] == want[k] for k in want), "record-word Step 2 differs from the E/W equations")
        require(g.ops == {"preamble": 21, "t1": 48, "t2": 47, "t3": 35}, f"Step-2 op counts {g.ops}")
        require(all(g.ops[k] <= STEP2_CHARGES[k] for k in g.ops), "Step-2 tranche exceeds its charge")
        if words is not None:
            require((got["W4"], got["W5"], got["W6"]) == tuple(words[4:7]) and all(got["pass"]),
                    "certificate tuple fails the record-word Step 2")
            require(all((wp[i] - words[i]) & MASK32 == dd for i, dd in ((4, D4), (5, D5), (6, D6))),
                    "certified pair's words 4..6 differ by D")
    def trace(words16: list[int]) -> tuple[list[int], list[int], list[int]]:
        ws = list(words16)
        for i in range(16, 32):
            ws.append((small_sigma1(ws[i - 2]) + ws[i - 7] + small_sigma0(ws[i - 15]) + ws[i - 16]) & MASK32)
        aa, ee = list(cv[3::-1]), list(cv[7:3:-1])
        for i in range(23):
            t1 = (ee[i] + big_sigma1(ee[i + 3]) + choose(ee[i + 3], ee[i + 2], ee[i + 1]) + K[i] + ws[i]) & MASK32
            ee.append((aa[i] + t1) & MASK32)
            aa.append((t1 + big_sigma0(aa[i + 3]) + majority(aa[i + 3], aa[i + 2], aa[i + 1])) & MASK32)
        return aa, ee, ws
    ua, ue, uw = trace(w)
    pa, pe, pw = trace(wp)
    require(ua[20] == pa[20]                                    # v14: stage 16 is A16' = A16 only
            and all(ua[i + 4] == pa[i + 4] for i in (17, 18, 19, 20, 21, 22)) and ue[21] == pe[21]
            and all(ue[i + 4] == pe[i + 4] for i in (19, 20, 21, 22)) and uw[24] == pw[24] and uw[29] == pw[29],
            "certified pair fails the relaxed Step-3 conditions")
    incl = char_inclusion_checks(hashlib.shake_256(bytes.fromhex(seed_hex) + b"relaxed").digest(4 * 64))
    return {"step2_record_word_checks": len(cases) + incl}


def verify_swar8_c32(seed_hex: str) -> dict[str, int]:
    buf = hashlib.shake_256(bytes.fromhex(seed_hex)).digest(8 * 64)
    blocks = [buf[l * 64:(l + 1) * 64] for l in range(8)]
    scalar_cvs = [compress32(IV, blk) for blk in blocks]
    lane_words = [struct.unpack(">16I", blk) for blk in blocks]
    w256 = [pack8([lane_words[l][i] for l in range(8)]) for i in range(16)] + [0] * 16
    for i in range(16, 32):
        t0 = add32x8(swar_small_sigma1(w256[i - 2]), w256[i - 7])
        t1 = add32x8(swar_small_sigma0(w256[i - 15]), w256[i - 16])
        w256[i] = add32x8(t0, t1)
    a, b, c, d, e, f, g, h = (pack8([iv_w] * 8) for iv_w in IV)
    for i in range(32):
        k_vec = pack8([K[i]] * 8)
        ch = (e & f) ^ ((~e & M_256) & g)
        maj = (a & b) ^ (a & c) ^ (b & c)
        s0, c0 = csa32x8(h, swar_big_sigma1(e), ch)
        kw = add32x8(k_vec, w256[i])
        s1, c1 = csa32x8(s0, c0, kw)
        t1_vec = add32x8(s1, c1)
        t2_vec = add32x8(swar_big_sigma0(a), maj)
        a, b, c, d, e, f, g, h = (
            add32x8(t1_vec, t2_vec), a, b, c, add32x8(d, t1_vec), e, f, g
        )
    out256 = [add32x8(pack8([iv_w] * 8), st_w) for iv_w, st_w in zip(IV, (a, b, c, d, e, f, g, h))]
    swar_cvs = [tuple((out256[j] >> (32 * l)) & MASK32 for j in range(8)) for l in range(8)]
    require(swar_cvs == scalar_cvs, "8-lane SWAR C_32 mismatch")

    raw_words = [
        int.from_bytes(hashlib.shake_256(bytes.fromhex(seed_hex) + bytes([i])).digest(32), "big")
        for i in range(16)
    ]
    m = Swar7Counter()
    m.section = "rand_and_mask"
    w7 = [0] * 32
    for i in range(16):
        rw = m.rand256(raw_words[i])
        w7[i] = m.bit_and(rw, M_32x7)
    blocks7 = [
        struct.pack(">16I", *[(w7[i] >> (LANE_BITS7 * l)) & MASK32 for i in range(16)])
        for l in range(LANES7)
    ]
    scalar_cvs7 = [compress32(IV, blk) for blk in blocks7]

    m.section = "schedule"
    for i in range(16, 32):
        s1 = m.small_sigma1(w7[i - 2])
        s0 = m.small_sigma0(w7[i - 15])
        t = m.add(m.add(m.add(s1, w7[i - 7]), s0), w7[i - 16])
        w7[i] = m.bit_and(t, M_32x7)

    m.section = "rounds"
    a7, b7, c7, d7, e7, f7, g7, h7 = IV7
    for i in range(32):
        S1 = m.big_sigma1(e7)
        ch7 = m.xor(m.bit_and(e7, f7), m.bit_and(m.xor(e7, M_32x7), g7))
        S0 = m.big_sigma0(a7)
        maj7 = m.xor(m.xor(m.bit_and(a7, b7), m.bit_and(a7, c7)), m.bit_and(b7, c7))
        t1_7 = m.add(m.add(m.add(m.add(h7, S1), ch7), K7[i]), w7[i])
        e7_new = m.bit_and(m.add(d7, t1_7), M_32x7)
        a7_new = m.bit_and(m.add(m.add(t1_7, S0), maj7), M_32x7)
        a7, b7, c7, d7, e7, f7, g7, h7 = a7_new, a7, b7, c7, e7_new, e7, f7, g7

    m.section = "feedforward"
    state_out7 = (a7, b7, c7, d7, e7, f7, g7, h7)
    out7 = [m.bit_and(m.add(IV7[j], state_out7[j]), M_32x7) for j in range(8)]

    m.section = "extract"
    swar_cvs7 = []
    for l in range(LANES7):
        row = []
        for j in range(8):
            shifted = m.shr(out7[j], LANE_BITS7 * l)
            row.append(m.bit_and(shifted, MASK32))
        swar_cvs7.append(tuple(row))

    require(swar_cvs7 == scalar_cvs7, "7-lane 36-bit SWAR C_32 mismatch")
    require(m.ops == {
        "rand_and_mask": 32,
        "schedule": 512,
        "rounds": 1664,
        "feedforward": 16,
        "extract": 112,
    }, f"unexpected 7-lane SWAR op counts: {m.ops}")
    require(sum(m.ops.values()) == 2336, "unexpected 7-lane SWAR total op count")
    require(m.max_lane < (1 << LANE_BITS7), "36-bit lane overflow")
    # Optimised 7-lane rounds actually charged (Section 8 A): round-0 constant folding, partial folding in
    # rounds 1-2, IF as g ^ (e & (f ^ g)), MAJ as b ^ ((a ^ b) & (b ^ c)) reusing the previous round's a ^ b.
    def bc7(v: int) -> int:
        return sum((v & MASK32) << (LANE_BITS7 * l) for l in range(LANES7))
    a0, b0, c0, d0, e0, f0, g0, h0 = IV
    q = Swar7Counter()
    q.section = "rand_and_mask"
    v7 = [0] * 32
    for i in range(16):
        v7[i] = q.bit_and(q.rand256(raw_words[i]), M_32x7)
    q.section = "schedule"
    for i in range(16, 32):
        s1 = q.small_sigma1(v7[i - 2])
        s0 = q.small_sigma0(v7[i - 15])
        v7[i] = q.bit_and(q.add(q.add(q.add(s1, v7[i - 7]), s0), v7[i - 16]), M_32x7)
    require(v7 == w7, "optimised schedule differs")
    q.section = "rounds"
    t1o = q.add(bc7(h0 + big_sigma1(e0) + choose(e0, f0, g0) + K[0]), v7[0])
    e_n = q.bit_and(q.add(bc7(d0), t1o), M_32x7)
    a_n = q.bit_and(q.add(t1o, bc7(big_sigma0(a0) + majority(a0, b0, c0))), M_32x7)
    sa, sb, sc, sd, se, sf, sg, sh = a_n, bc7(a0), bc7(b0), bc7(c0), e_n, bc7(e0), bc7(f0), bc7(g0)
    S1o = q.big_sigma1(se)
    cho = q.xor(bc7(f0), q.bit_and(se, bc7(e0 ^ f0)))
    S0o = q.big_sigma0(sa)
    mjo = q.xor(q.bit_and(sa, bc7(a0 ^ b0)), bc7(a0 & b0))
    t1o = q.add(q.add(q.add(bc7(g0 + K[1]), S1o), cho), v7[1])
    e_n = q.bit_and(q.add(bc7(c0), t1o), M_32x7)
    a_n = q.bit_and(q.add(q.add(t1o, S0o), mjo), M_32x7)
    sa, sb, sc, sd, se, sf, sg, sh = a_n, sa, sb, sc, e_n, se, sf, sg
    S1o = q.big_sigma1(se)
    cho = q.xor(sg, q.bit_and(se, q.xor(sf, sg)))
    S0o = q.big_sigma0(sa)
    xab = q.xor(sa, sb)
    mjo = q.xor(sb, q.bit_and(xab, q.xor(sb, sc)))
    t1o = q.add(q.add(q.add(bc7(f0 + K[2]), S1o), cho), v7[2])
    e_n = q.bit_and(q.add(sd, t1o), M_32x7)
    a_n = q.bit_and(q.add(q.add(t1o, S0o), mjo), M_32x7)
    prev_ab = xab
    sa, sb, sc, sd, se, sf, sg, sh = a_n, sa, sb, sc, e_n, se, sf, sg
    for i in range(3, 32):
        S1o = q.big_sigma1(se)
        cho = q.xor(sg, q.bit_and(se, q.xor(sf, sg)))
        S0o = q.big_sigma0(sa)
        xab = q.xor(sa, sb)
        mjo = q.xor(sb, q.bit_and(xab, prev_ab))
        t1o = q.add(q.add(q.add(q.add(sh, S1o), cho), K7[i]), v7[i])
        e_n = q.bit_and(q.add(sd, t1o), M_32x7)
        a_n = q.bit_and(q.add(q.add(t1o, S0o), mjo), M_32x7)
        prev_ab = xab
        sa, sb, sc, sd, se, sf, sg, sh = a_n, sa, sb, sc, e_n, se, sf, sg
    q.section = "feedforward"
    sto = (sa, sb, sc, sd, se, sf, sg, sh)
    outo = [q.bit_and(q.add(IV7[j], sto[j]), M_32x7) for j in range(8)]
    q.section = "extract"
    opt_cvs7 = [tuple(q.bit_and(q.shr(outo[j], LANE_BITS7 * l), MASK32) for j in range(8)) for l in range(LANES7)]
    require(opt_cvs7 == scalar_cvs7, "optimised 7-lane SWAR C_32 mismatch")
    require(q.ops == {
        "rand_and_mask": 32,
        "schedule": 512,
        "rounds": 1521,
        "feedforward": 16,
        "extract": 112,
    }, f"unexpected optimised 7-lane SWAR op counts: {q.ops}")
    require(sum(q.ops.values()) == 2193, "unexpected optimised 7-lane SWAR total op count")

    # Lazy extraction: the batch extracts only CV1[0] per lane from outo[0]; CV1[1..7]
    # of one lane are extracted from the stored outo words only for a trial whose
    # bucket is nonempty.
    lazy = Swar7Counter()
    lazy.section = "extract"
    first_words = [lazy.bit_and(lazy.shr(outo[0], LANE_BITS7 * l), MASK32) for l in range(LANES7)]
    require(lazy.ops["extract"] == 14, "unexpected lazy batch extraction count")
    for l in range(LANES7):
        before = lazy.ops["extract"]
        rest = [lazy.bit_and(lazy.shr(outo[j], LANE_BITS7 * l), MASK32) for j in range(1, 8)]
        require(lazy.ops["extract"] - before == 14, "unexpected deferred extraction count")
        require((first_words[l], *rest) == scalar_cvs7[l], "lazy CV1 extraction mismatch")

    reg64 = verify_reg64_batch(raw_words, scalar_cvs7)
    return {
        **reg64,
        **verify_pc4_hoist(seed_hex),
        **verify_step2_fields(seed_hex, outo, opt_cvs7),
        "swar8_c32_verified": 8,
        "swar7_c32_verified": 7,
        "swar7_arithmetic_ops": sum(m.ops.values()),
        "swar7_schedule_ops": m.ops["schedule"],
        "swar7_rounds_ops": m.ops["rounds"],
        "swar7_max_lane_bits": m.max_lane.bit_length(),
        "lazy_cv_extract_ops": lazy.ops["extract"],
        "swar7_opt_c32_verified": 7,
        "swar7_opt_arithmetic_ops": sum(q.ops.values()),
        "swar7_opt_rounds_ops": q.ops["rounds"],
    }


def main() -> None:
    request = json.load(sys.stdin)
    require(request.get("schema_version") == 1, "unexpected organizer schema")
    require(request.get("target_profile") == "sha256-r32-prefix-v1",
            "unexpected organizer target")
    require(request.get("event") == {"kind": "full-collision"},
            "unexpected organizer event")
    require(type(request.get("trials")) is list, "organizer trials must be a list")

    # Reconstruct once per organizer request from the committed record slices.
    first, second = derive_embedded_witness()
    trials = [
        {
            "trial": trial["trial"],
            "message_a_hex": first.hex(),
            "message_b_hex": second.hex(),
            "observations": verify_swar8_c32(trial["seed"]),
        }
        for trial in request["trials"]
    ]
    json.dump({"schema_version": 1, "trials": trials}, sys.stdout,
              separators=(",", ":"), sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
