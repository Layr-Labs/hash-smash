"""Deterministic fixed-witness transport for organizer isolation.

The HashSmash organizer runner evaluates this source in its isolated container.
The source replays one public pair for every requested trial and provides
evidence only for the selected-target collision relation. It does not reproduce
the historical search or provide attack-cost or probability evidence.
"""

import hashlib
import json
import sys


E_BASES = (0x1D1F97E3, 0xAD80F8E6, 0x9C1FCE6C, 0xD92B084C)
E_DELTAS = (0x0000303E, 0x00088001, 0xD0880489, 0x4D008804)
E_CHOICE_POSITIONS = (
    (11,),
    (8, 9, 16, 17, 21, 22, 25),
    (8, 22),
    (0, 9, 12, 14, 18, 20, 22),
)


def _uint32(value):
    if type(value) is not int or not 0 <= value < (1 << 32):
        raise ValueError("32-bit unsigned word required")
    return value


def expand_e_ranks(ranks):
    if type(ranks) is not tuple or len(ranks) != 4:
        raise ValueError("four E ranks required")
    words = []
    for rank, base, positions in zip(ranks, E_BASES, E_CHOICE_POSITIONS):
        if type(rank) is not int or not 0 <= rank < (1 << len(positions)):
            raise ValueError("E rank outside characteristic domain")
        word = base
        for index, position in enumerate(positions):
            word |= ((rank >> index) & 1) << position
        words.append(word)
    return tuple(words)


def _rank_e_word(word, base, positions):
    word = _uint32(word)
    choice_mask = sum(1 << position for position in positions)
    if word & ~choice_mask != base:
        raise ValueError("E word violates the fixed characteristic bits")
    return sum(((word >> position) & 1) << index
               for index, position in enumerate(positions))


def partner_e_words(e_words):
    if type(e_words) is not tuple or len(e_words) != 4:
        raise ValueError("four E words required")
    return tuple(_uint32(word) ^ delta
                 for word, delta in zip(e_words, E_DELTAS))


def pack_tuple(a_words, e_words):
    if type(a_words) is not tuple or len(a_words) != 6:
        raise ValueError("six A words required")
    if type(e_words) is not tuple or len(e_words) != 4:
        raise ValueError("four E words required")
    a_words = tuple(_uint32(word) for word in a_words)
    ranks = tuple(
        _rank_e_word(word, base, positions)
        for word, base, positions in zip(
            e_words, E_BASES, E_CHOICE_POSITIONS
        )
    )
    record = (
        (a_words[0] << 224)
        | (a_words[1] << 192)
        | (a_words[2] << 160)
        | (a_words[3] << 128)
        | (a_words[4] << 96)
        | (a_words[5] << 64)
        | (ranks[0] << 63)
        | (ranks[1] << 56)
        | (ranks[2] << 54)
        | (ranks[3] << 47)
    )
    return record.to_bytes(32, "big")


def unpack_tuple(packed):
    if type(packed) is not bytes or len(packed) != 32:
        raise ValueError("one 32-byte tuple record required")
    record = int.from_bytes(packed, "big")
    if record & ((1 << 47) - 1):
        raise ValueError("noncanonical tuple padding")
    a_words = tuple((record >> shift) & 0xFFFFFFFF
                    for shift in (224, 192, 160, 128, 96, 64))
    ranks = (
        (record >> 63) & 0x1,
        (record >> 56) & 0x7F,
        (record >> 54) & 0x3,
        (record >> 47) & 0x7F,
    )
    return a_words, expand_e_ranks(ranks)


LAYOUT_FIXTURE_A = (
    0x12345678,
    0x9ABCDEF0,
    0x00000000,
    0xFFFFFFFF,
    0x80000000,
    0x01020304,
)
LAYOUT_FIXTURE_SHA256 = (
    "1bb33a58e7b07affd6a400dbcbad59a624fcd50c8081a131b6937106fe3b688c"
)


def verify_tuple_layout():
    digest = hashlib.sha256()
    checked = 0
    for r8 in range(1 << 7):
        for r7 in range(1 << 2):
            for r6 in range(1 << 7):
                for r5 in range(1 << 1):
                    e_words = expand_e_ranks((r5, r6, r7, r8))
                    packed = pack_tuple(LAYOUT_FIXTURE_A, e_words)
                    if unpack_tuple(packed) != (LAYOUT_FIXTURE_A, e_words):
                        raise ValueError("tuple layout round trip failed")
                    digest.update(packed.hex().encode("ascii") + b"\n")
                    checked += 1
    if digest.hexdigest() != LAYOUT_FIXTURE_SHA256:
        raise ValueError("tuple layout exhaustive digest mismatch")
    return {
        "layout_records_checked": checked,
        "layout_record_bytes": 32,
        "layout_digest_match": True,
    }


MESSAGE_A_HEX = (
    "8ce3f8055c401aed579e5f7fbc3116cbca189b3ceb75f04c958f0a0e7760b082"
    "dcd5027d32260ad67b12b659eee66518ad7f88ddf8ad20bb7ae40ffd21609249"
    "9abdeb1b1f195f415a7210c155614f13a2269dd1be888a61359257d4adf3737b"
    "9f0484a6eb830a5866add94a9669232d45271fa5b8f69585428bbce30703b904"
)
MESSAGE_B_HEX = (
    "8ce3f8055c401aed579e5f7fbc3116cbca189b3ceb75f04c958f0a0e7760b082"
    "dcd5027d32260ad67b12b659eee66518ad7f88ddf8ad20bb7ae40ffd21609249"
    "9abdeb1b1f195f415a7210c155614f13a2269dd1be887a6735b2dfc5fde32975"
    "c70595a6eb838a5c66add94a9669232d45271fa5b8f69585428bbce30703b904"
)


def validate_request(request):
    if type(request) is not dict:
        raise ValueError("organizer request object required")
    required = {
        "schema_version",
        "experiment_id",
        "target_profile",
        "event",
        "max_message_bytes",
        "trials",
    }
    if set(request) != required:
        raise ValueError("unexpected organizer request fields")
    if request["schema_version"] != 1:
        raise ValueError("unexpected organizer schema")
    if request["experiment_id"] != "published-r31-witness-replay":
        raise ValueError("unexpected experiment id")
    if request["target_profile"] != "sha256-r31-prefix-v1":
        raise ValueError("unexpected organizer target")
    if request["event"] != {"kind": "full-collision"}:
        raise ValueError("unexpected organizer event")
    if type(request["max_message_bytes"]) is not int or request["max_message_bytes"] < 128:
        raise ValueError("organizer message budget is too small")
    if type(request["trials"]) is not list:
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
    layout_observations = verify_tuple_layout()
    rows = [
        {
            "trial": trial["trial"],
            "message_a_hex": MESSAGE_A_HEX,
            "message_b_hex": MESSAGE_B_HEX,
            "observations": layout_observations,
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
