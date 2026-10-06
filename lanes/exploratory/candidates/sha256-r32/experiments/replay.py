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


def verify_grouped_and_prefilter(seed_hex: str) -> dict[str, int]:
    buf = hashlib.shake_256(bytes.fromhex(seed_hex)).digest(80)
    words = list(struct.unpack(">16I", buf[:64]))
    w_base = list(words) + [0] * 16
    w_base[16] = (small_sigma1(w_base[14]) + w_base[9] + small_sigma0(w_base[1]) + w_base[0]) & MASK32
    w_base[18] = (small_sigma1(w_base[16]) + w_base[11] + small_sigma0(w_base[3]) + w_base[2]) & MASK32
    w_base[20] = (small_sigma1(w_base[18]) + w_base[13] + small_sigma0(w_base[5]) + w_base[4]) & MASK32

    a, b, c, d, e, f, g, h = IV
    for step in range(15):
        t1 = (h + big_sigma1(e) + choose(e, f, g) + K[step] + w_base[step]) & MASK32
        t2_val = t2(a, b, c)
        a, b, c, d, e, f, g, h = (t1 + t2_val) & MASK32, a, b, c, (d + t1) & MASK32, e, f, g
    state15_base = (a, b, c, d, e, f, g, h)
    t1_15_const = (h + big_sigma1(e) + choose(e, f, g) + K[15]) & MASK32
    t2_15_const = t2(a, b, c)

    inc_matches = 0
    group_hits = 0
    for j in range(64):
        w15 = (words[15] + j) & MASK32
        w = list(w_base)
        w[15] = w15
        for step in (17, 19, *range(21, 32)):
            w[step] = (small_sigma1(w[step - 2]) + w[step - 7]
                       + small_sigma0(w[step - 15]) + w[step - 16]) & MASK32
        a, b, c, d, e, f, g, h = state15_base
        t1 = (t1_15_const + w15) & MASK32
        a, b, c, d, e, f, g, h = (t1 + t2_15_const) & MASK32, a, b, c, (d + t1) & MASK32, e, f, g
        for step in range(16, 32):
            t1 = (h + big_sigma1(e) + choose(e, f, g) + K[step] + w[step]) & MASK32
            t2_val = t2(a, b, c)
            a, b, c, d, e, f, g, h = (t1 + t2_val) & MASK32, a, b, c, (d + t1) & MASK32, e, f, g
        inc_cv = tuple((old + new) & MASK32 for old, new in zip(IV, (a, b, c, d, e, f, g, h)))
        if j < 16:
            block = struct.pack(">16I", *(words[:15] + [w15]))
            require(compress32(IV, block) == inc_cv, "grouped C_32 incremental mismatch")
            inc_matches += 1
        if (inc_cv[0] >> 28) == 0 and (inc_cv[1] & 0x20000000) == 0:
            group_hits += 1

    # Verify Step-2 algebraic pre-filter identities on seeded words and the witness
    w4_sample, w5_sample, w6_sample = struct.unpack(">3I", buf[64:76])
    w12_val, w12p_val = 0x41B22A2C, 0x45F2222C
    w13_val, w13p_val = 0x6D12F88A, 0x4D12F88A
    pass_a = 1 if (w4_sample & 0x20000000) == 0 else 0
    w4p = w4_sample ^ 0x20000000
    pass_b = 1 if ((small_sigma0(w4p) + w12p_val) & MASK32) == ((small_sigma0(w4_sample) + w12_val) & MASK32) else 0
    pass_c = 1 if (w5_sample & 0x04400800) == 0x04400000 else 0
    pass_d = 1 if (w6_sample & 0x20000000) == 0 else 0
    w5p = w5_sample ^ 0x04400800
    w6p = w6_sample ^ 0x20000000
    pass_f = 1 if ((small_sigma0(w6p) + w5p) & MASK32) == ((small_sigma0(w6_sample) + w5_sample) & MASK32) else 0
    dw20 = ((w13p_val - w13_val) + (small_sigma0(w5p) - small_sigma0(w5_sample)) + (w4p - w4_sample)) & MASK32
    pass_g = 1 if dw20 == 0x017F8000 else 0

    return {
        "grouped_c32_verified": inc_matches,
        "group_hits_64": group_hits,
        "group_pairs_64": (group_hits * (group_hits - 1)) // 2,
        "prefilter_flags": (pass_a << 5) | (pass_b << 4) | (pass_c << 3) | (pass_d << 2) | (pass_f << 1) | pass_g,
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
            "observations": verify_grouped_and_prefilter(trial["seed"]),
        }
        for trial in request["trials"]
    ]
    json.dump({"schema_version": 1, "trials": trials}, sys.stdout,
              separators=(",", ":"), sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()

