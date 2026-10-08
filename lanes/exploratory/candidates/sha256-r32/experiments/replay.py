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

    # Lazy extraction (this version): the batch extracts only CV1[0] per lane;
    # CV1[1..7] of one lane are extracted from the stored out7 words only for a
    # trial whose bucket is nonempty.
    lazy = Swar7Counter()
    lazy.section = "extract"
    first_words = [lazy.bit_and(lazy.shr(out7[0], LANE_BITS7 * l), MASK32) for l in range(LANES7)]
    require(lazy.ops["extract"] == 14, "unexpected lazy batch extraction count")
    for l in range(LANES7):
        before = lazy.ops["extract"]
        rest = [lazy.bit_and(lazy.shr(out7[j], LANE_BITS7 * l), MASK32) for j in range(1, 8)]
        require(lazy.ops["extract"] - before == 14, "unexpected deferred extraction count")
        require((first_words[l], *rest) == scalar_cvs7[l], "lazy CV1 extraction mismatch")
    return {
        "lazy_cv_extract_ops": lazy.ops["extract"],
        "swar8_c32_verified": 8,
        "swar7_c32_verified": 7,
        "swar7_arithmetic_ops": sum(m.ops.values()),
        "swar7_schedule_ops": m.ops["schedule"],
        "swar7_rounds_ops": m.ops["rounds"],
        "swar7_max_lane_bits": m.max_lane.bit_length(),
    }


# Stages 16 and 17 of Step 3 in seven 36-bit lanes (proof Section 4, item 3).
# Per W14 group of 2^14 P4 rows, the builder packs ten streams, seven rows per
# word: XE = E16-W16, XE' = E16'-W16, XA = A16-E16, XA' = A16'-E16',
# Z = A13+E13+K17+s1(W15), Z' = A13'+E13'+K17+s1(W15), E14, E15, A14, A15.
# The last word of a group holds four rows and three zero padding lanes.
ROWS16 = {
    "E14": "=0=100110000000=101=0000=110===0", "E15": "=1====0011===u10001=011===0n===1",
    "A14": "==u=============================", "A15": "=" * 32,
    "E16": "======u=n====1==n=====0===01====", "A16": "=" * 32,
    "E17": "======0=0====1==0==========1====", "A17": "=" * 32,
    "E13": "=n1111uu1n00000u1u0=nnn01111010n",
}
STAGE16_GROUP_ROWS = 1 << 14
A13_FIXED = (A_FIXED[1][9], A_FIXED[0][9])
E13_FIXED = (E_FIXED[1][5], E_FIXED[0][5])


def row_flip_mask(row: str) -> int:
    return sum(1 << (31 - k) for k, symbol in enumerate(row) if symbol in "nu")


def replicate7(word: int) -> int:
    return sum((word & MASK32) << (LANE_BITS7 * l) for l in range(LANES7))


FL = {name: row_flip_mask(row) for name, row in ROWS16.items()}
FL7 = {name: replicate7(value) for name, value in FL.items()}
NA13 = tuple((-a) & MASK32 for a in A13_FIXED)
NA13_7 = tuple(replicate7(v) for v in NA13)
GUARD7 = sum(1 << (LANE_BITS7 * l + 32) for l in range(LANES7))
LANE_GUARD7 = tuple(1 << (LANE_BITS7 * l + 32) for l in range(LANES7))


class Stage16Counter(Swar7Counter):
    SECTIONS = ("broadcast", "load16", "lane16", "load17", "lane17", "scan", "extract")

    def __init__(self) -> None:
        super().__init__()
        self.ops = dict.fromkeys(self.SECTIONS, 0)
        self.section = "broadcast"
        self.max_sum = 0

    def add(self, a: int, b: int) -> int:
        result = self._record(a + b)
        require(result >> (LANE_BITS7 * LANES7) == 0, "lane sum above bit 251")
        lane_mask = (1 << LANE_BITS7) - 1
        for l in range(LANES7):
            shift = LANE_BITS7 * l
            lane = (result >> shift) & lane_mask
            require(lane == ((a >> shift) & lane_mask) + ((b >> shift) & lane_mask), "inter-lane carry")
            self.max_sum = max(self.max_sum, lane)
        return result

    def load(self, row: tuple[int, ...], index: int) -> int:
        self.ops[self.section] += 1
        return row[index]

    def choose(self, e: int, f: int, g: int) -> int:
        return self.xor(self.bit_and(e, f), self.bit_and(self.xor(e, M_32x7), g))

    def majority(self, a: int, b: int, c: int) -> int:
        return self.xor(self.xor(self.bit_and(a, b), self.bit_and(a, c)), self.bit_and(b, c))

    def broadcast(self, word: int) -> int:
        x = self.bit_or(word, self.shl(word, LANE_BITS7))
        x = self.bit_or(x, self.shl(x, 2 * LANE_BITS7))
        x = self.bit_or(x, self.shl(x, 4 * LANE_BITS7))
        return self.bit_and(x, M_32x7)


def stage1617_scalar(w16: int, c17: int, row: tuple[int, ...]) -> tuple[bool, bool, tuple[int, ...]]:
    xe, xep, xa, xap, z, zp, e14, e15, a14, a15 = row
    e16 = (xe + w16) & MASK32
    e16p = (xep + w16) & MASK32
    a16 = (xa + e16) & MASK32
    a16p = (xap + e16p) & MASK32
    pass16 = (e16 ^ e16p) == FL["E16"] and (a16 ^ a16p) == FL["A16"]
    e14p, e15p = e14 ^ FL["E14"], e15 ^ FL["E15"]
    a14p, a15p = a14 ^ FL["A14"], a15 ^ FL["A15"]
    e17 = (z + c17 + big_sigma1(e16) + choose(e16, e15, e14)) & MASK32
    e17p = (zp + c17 + big_sigma1(e16p) + choose(e16p, e15p, e14p)) & MASK32
    a17 = (e17 + NA13[0] + t2(a16, a15, a14)) & MASK32
    a17p = (e17p + NA13[1] + t2(a16p, a15p, a14p)) & MASK32
    pass17 = pass16 and (e17 ^ e17p) == FL["E17"] and (a17 ^ a17p) == FL["A17"]
    return pass16, pass17, (e16, e16p, a16, a16p, e17, e17p, a17, a17p)


def pack_stage16_group(rows: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    packed = []
    for start in range(0, len(rows), LANES7):
        chunk = rows[start:start + LANES7]
        chunk = chunk + [(0,) * 10] * (LANES7 - len(chunk))
        packed.append(tuple(
            sum(chunk[l][s] << (LANE_BITS7 * l) for l in range(LANES7)) for s in range(10)
        ))
    return packed


def stage1617_swar_group(m: Stage16Counter, w16: int, c17: int, packed: list[tuple[int, ...]]):
    m.section = "broadcast"
    w16_7 = m.broadcast(w16)
    c17_7 = m.broadcast(c17)
    masks16, masks17, passes = [], [], []
    for k, row in enumerate(packed):
        m.section = "load16"
        xe, xep, xa, xap = (m.load(row, s) for s in range(4))
        m.section = "lane16"
        e16 = m.add(xe, w16_7)
        e16p = m.add(xep, w16_7)
        a16 = m.add(xa, e16)
        a16p = m.add(xap, e16p)
        diff_e = m.xor(m.xor(e16, e16p), FL7["E16"])
        diff_a = m.xor(m.xor(a16, a16p), FL7["A16"])
        u = m.bit_and(m.bit_or(diff_e, diff_a), M_32x7)
        passed16 = m.xor(m.bit_and(m.add(u, M_32x7), GUARD7), GUARD7)
        masks16.append(passed16)
        if passed16 == 0:
            masks17.append(0)
            continue
        m.section = "load17"
        z, zp, e14, e15, a14, a15 = (m.load(row, s) for s in range(4, 10))
        m.section = "lane17"
        e14p, e15p = m.xor(e14, FL7["E14"]), m.xor(e15, FL7["E15"])
        a14p, a15p = m.xor(a14, FL7["A14"]), m.xor(a15, FL7["A15"])
        e16, e16p = m.bit_and(e16, M_32x7), m.bit_and(e16p, M_32x7)
        a16, a16p = m.bit_and(a16, M_32x7), m.bit_and(a16p, M_32x7)
        e17 = m.add(m.add(m.add(z, c17_7), m.big_sigma1(e16)), m.choose(e16, e15, e14))
        e17p = m.add(m.add(m.add(zp, c17_7), m.big_sigma1(e16p)), m.choose(e16p, e15p, e14p))
        a17 = m.add(m.add(m.add(e17, NA13_7[0]), m.big_sigma0(a16)), m.majority(a16, a15, a14))
        a17p = m.add(m.add(m.add(e17p, NA13_7[1]), m.big_sigma0(a16p)), m.majority(a16p, a15p, a14p))
        diff_e = m.xor(m.xor(e17, e17p), FL7["E17"])
        diff_a = m.xor(m.xor(a17, a17p), FL7["A17"])
        u = m.bit_and(m.bit_or(diff_e, diff_a), M_32x7)
        passed17 = m.bit_and(m.xor(m.bit_and(m.add(u, M_32x7), GUARD7), GUARD7), passed16)
        masks17.append(passed17)
        if passed17 == 0:
            continue
        for l in range(LANES7):
            m.section = "scan"
            if m.bit_and(passed17, LANE_GUARD7[l]) == 0:
                continue
            m.section = "extract"
            values = tuple(m.bit_and(m.shr(v, LANE_BITS7 * l), MASK32)
                           for v in (e16, e16p, a16, a16p, e17, e17p, a17, a17p))
            passes.append((k * LANES7 + l, values))
    return masks16, masks17, passes


def check_stage1617_group(m: Stage16Counter, w16: int, c17: int, rows: list[tuple[int, ...]]) -> dict[str, int]:
    before = dict(m.ops)
    packed = pack_stage16_group(rows)
    masks16, masks17, passes = stage1617_swar_group(m, w16, c17, packed)
    padded = rows + [(0,) * 10] * (len(packed) * LANES7 - len(rows))
    expected_passes = []
    for k in range(len(packed)):
        expected16 = expected17 = 0
        for l in range(LANES7):
            ok16, ok17, values = stage1617_scalar(w16, c17, padded[k * LANES7 + l])
            if ok16:
                require(k * LANES7 + l < len(rows), "stage-16 padding lane passed")
                expected16 |= LANE_GUARD7[l]
            if ok17:
                expected17 |= LANE_GUARD7[l]
                expected_passes.append((k * LANES7 + l, values))
        require(masks16[k] == expected16, "SWAR stage-16 pass mask differs from scalar tests")
        require(masks17[k] == expected17, "SWAR stage-17 pass mask differs from scalar tests")
    require(passes == expected_passes, "SWAR stage-17 extracted values differ from scalar values")
    words16 = len(packed)
    words17 = sum(1 for mask in masks16 if mask)
    scanned = sum(1 for mask in masks17 if mask)
    delta = {key: m.ops[key] - before[key] for key in m.ops}
    require(delta == {
        "broadcast": 14,
        "load16": 4 * words16,
        "lane16": 13 * words16,
        "load17": 6 * words17,
        "lane17": 116 * words17,
        "scan": LANES7 * scanned,
        "extract": 16 * len(passes),
    }, f"unexpected SWAR stage-16/17 op counts: {delta}")
    require(m.max_sum < (1 << 35), "SWAR stage-16/17 lane sum reached 2^35")
    return {"rows": len(rows), "words16": words16, "words17": words17,
            "passes16": sum(bin(mask).count("1") for mask in masks16), "passes17": len(passes)}


def stage1617_rows(stream: bytes, w16: int, c17: int, count: int) -> list[tuple[int, ...]]:
    """Random rows; rows built to pass stage 16 (kind 1) or both stages (2, 7); single-bit near misses at
    stage 17 (3, 4) and at stage 16 with the stage-17 equations satisfied (5, 6); carry stress (7)."""
    rows = []
    for i in range(count):
        chunk = stream[48 * i:48 * i + 48]
        kind, bit = chunk[0] % 8, chunk[1] % 32
        r = list(struct.unpack(">10I", chunk[4:44]))
        tweak = struct.unpack(">I", chunk[44:48])[0]
        if kind == 0:
            rows.append(tuple(r))
            continue
        if kind == 7:
            r = [MASK32 - (v & 0xFF) for v in r]
        e16, a16 = r[0], r[2]
        e16p = e16 ^ FL["E16"] ^ ((1 << bit) if kind == 5 else 0)
        a16p = a16 ^ FL["A16"] ^ ((1 << bit) if kind == 6 else 0)
        z, e14, e15, a14, a15 = r[4], r[6], r[7], r[8], r[9]
        zp = r[5]
        if kind >= 2:
            e14p, e15p = e14 ^ FL["E14"], e15 ^ FL["E15"]
            e17 = (z + c17 + big_sigma1(e16) + choose(e16, e15, e14)) & MASK32
            e17p = e17 ^ FL["E17"]
            zp = (e17p - c17 - big_sigma1(e16p) - choose(e16p, e15p, e14p)) & MASK32
            for attempt in range(64):
                a15 = (r[9] + attempt * 0x9E3779B9) & MASK32
                a17 = (e17 + NA13[0] + t2(a16, a15, a14)) & MASK32
                a17p = (e17p + NA13[1] + t2(a16p, a15 ^ FL["A15"], a14 ^ FL["A14"])) & MASK32
                if (a17 ^ a17p) == FL["A17"]:
                    break
            if kind == 3:
                zp ^= 1 << bit
            if kind == 4:
                a15 ^= 1 << (tweak % 32)
        rows.append(((e16 - w16) & MASK32, (e16p - w16) & MASK32, (a16 - e16) & MASK32,
                     (a16p - e16p) & MASK32, z, zp, e14, e15, a14, a15))
    return rows


def witness_stage1617_row(message_a: bytes, message_b: bytes):
    """Packed-stream values of the certified pair from the literal step equations; message_b is unprimed."""
    cv = compress32(IV, message_a[:64])
    traces = []
    for message in (message_b, message_a):
        w = list(struct.unpack(">16I", message[64:128]))
        for i in (16, 17):
            w.append((small_sigma1(w[i - 2]) + w[i - 7] + small_sigma0(w[i - 15]) + w[i - 16]) & MASK32)
        a = {-4: cv[3], -3: cv[2], -2: cv[1], -1: cv[0]}
        e = {-4: cv[7], -3: cv[6], -2: cv[5], -1: cv[4]}
        for i in range(18):
            e[i] = (a[i - 4] + e[i - 4] + big_sigma1(e[i - 1]) + choose(e[i - 1], e[i - 2], e[i - 3])
                    + K[i] + w[i]) & MASK32
            a[i] = (e[i] - a[i - 4] + t2(a[i - 1], a[i - 2], a[i - 3])) & MASK32
        traces.append((a, e, w))
    (a, e, w), (ap, ep, wp) = traces
    require(w[16:18] == wp[16:18] and w[15] == wp[15], "witness W15..W17 differ between branches")
    require((a[13], ap[13]) == A13_FIXED and (e[13], ep[13]) == E13_FIXED, "witness A13/E13 are not the advice")
    require(ep[13] == e[13] ^ FL["E13"] and ap[13] == a[13], "witness step-13 flips changed")
    require(all(xp == x ^ FL[name] for name, x, xp in
                (("E14", e[14], ep[14]), ("E15", e[15], ep[15]), ("A14", a[14], ap[14]), ("A15", a[15], ap[15]))),
            "witness step-14/15 flips changed")
    c17 = (w[10] + small_sigma0(w[2]) + w[1]) & MASK32
    require((c17 + small_sigma1(w[15])) & MASK32 == w[17], "W17 = c17 + s1(W15) failed")
    row = ((a[12] + e[12] + big_sigma1(e[15]) + choose(e[15], e[14], e[13]) + K[16]) & MASK32,
           (ap[12] + ep[12] + big_sigma1(ep[15]) + choose(ep[15], ep[14], ep[13]) + K[16]) & MASK32,
           (t2(a[15], a[14], a[13]) - a[12]) & MASK32,
           (t2(ap[15], ap[14], ap[13]) - ap[12]) & MASK32,
           (a[13] + e[13] + K[17] + small_sigma1(w[15])) & MASK32,
           (ap[13] + ep[13] + K[17] + small_sigma1(w[15])) & MASK32,
           e[14], e[15], a[14], a[15])
    values = (e[16], ep[16], a[16], ap[16], e[17], ep[17], a[17], ap[17])
    return w[16], c17, row, values


def verify_stage1617_swar(seed_hex: str, witness, full_group: bool) -> dict[str, Any]:
    require(FL["E16"] == 0x02808000 and FL["A16"] == 0 and FL["E13"] == 0x43414E01, "flip masks changed")
    stream = hashlib.shake_256(bytes.fromhex(seed_hex) + b"stage1617").digest(
        32 + 48 * ((STAGE16_GROUP_ROWS if full_group else 0) + 128))
    consts = list(struct.unpack(">8I", stream[:32]))
    consts[2] = MASK32
    body = stream[32:]
    w16_w, c17_w, row_w, values_w = witness
    groups = [(consts[0], consts[1], stage1617_rows(body, consts[0], consts[1], 40)),
              (consts[2], consts[3], stage1617_rows(body[1920:], consts[2], consts[3], 33))]
    rows_w = stage1617_rows(body[3600:], w16_w, c17_w, 12)
    rows_w[body[4300] % 12] = row_w
    groups.append((w16_w, c17_w, rows_w))
    if full_group:
        groups.append((consts[4], consts[5], stage1617_rows(body[6144:], consts[4], consts[5], STAGE16_GROUP_ROWS)))
    m = Stage16Counter()
    summary = {"rows": 0, "words16": 0, "words17": 0, "passes16": 0, "passes17": 0}
    for w16, c17, rows in groups:
        result = check_stage1617_group(m, w16, c17, rows)
        for key in summary:
            summary[key] += result[key]
    ok16, ok17, values = stage1617_scalar(w16_w, c17_w, row_w)
    require(ok16 and ok17 and values == values_w, "certified pair fails scalar stages 16-17")
    return {
        "stage1617_groups": len(groups),
        "stage1617_rows": summary["rows"],
        "stage16_packed_words": summary["words16"],
        "stage17_packed_words": summary["words17"],
        "stage16_passes": summary["passes16"],
        "stage17_passes": summary["passes17"],
        "stage1617_counted_ops": sum(m.ops.values()),
        "stage1617_max_lane_sum_bits": m.max_sum.bit_length(),
        "stage1617_witness_row_passes": True,
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
    witness1617 = witness_stage1617_row(first, second)
    trials = []
    for index, trial in enumerate(request["trials"]):
        observations = verify_swar8_c32(trial["seed"])
        observations.update(verify_stage1617_swar(trial["seed"], witness1617, full_group=index == 0))
        trials.append({
            "trial": trial["trial"],
            "message_a_hex": first.hex(),
            "message_b_hex": second.hex(),
            "observations": observations,
        })
    json.dump({"schema_version": 1, "trials": trials}, sys.stdout,
              separators=(",", ":"), sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
