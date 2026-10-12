#!/usr/bin/env python3
"""Count data-path operations in trusted reference cores; never run candidates.

These are portable normalization estimates, not cycle counts or attack bounds.
Public loop/index arithmetic, Python overhead, serialization and memory traffic
are excluded. Narrow rotations retain their explicit shifts, ORs and masks in
the 256-bit RAM model; no native 32/64-bit rotate is assumed.

Poseidon is a prime-field target rather than a binary one, so its data path is
counted in field operations: one addition and one multiplication modulo the
target prime each count as one primitive operation. Reductions are part of
those operations and are not charged again. The 256-bit word model does not
price a 255-bit modular multiplication, so this counting rule is a proposal
for the organizers rather than an established part of collision-frontier-v5.
"""

import json
import operator
from pathlib import Path
import sys
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verifier import blake3, hash_functions, keccak, poseidon


class Word(int):
    operations = 0


def counted(operation):
    def apply(self, other=None):
        Word.operations += 1
        return Word(operation(int(self)) if other is None else operation(int(self), int(other)))
    return apply


for name, operation in {
    "add": operator.add, "and": operator.and_, "or": operator.or_,
    "xor": operator.xor, "lshift": operator.lshift, "rshift": operator.rshift,
    "invert": operator.invert,
}.items():
    setattr(Word, f"__{name}__", counted(operation))


def reference_costs():
    result = {}
    for algorithm, rounds_set in (("md5", (63, 64)), ("sha1", (79, 80)), ("sha256", (31, 32, 37, 38))):
        for rounds in rounds_set:
            Word.operations = 0
            state = tuple(Word(x) for x in hash_functions.IV[algorithm])
            with patch.object(hash_functions.struct, "unpack", return_value=tuple(Word(i) for i in range(16))):
                hash_functions._compress(algorithm, state, bytes(64), rounds)
            suffix = "s" if algorithm == "md5" else "r"
            result[f"{algorithm}-{suffix}{rounds}"] = Word.operations
    for rounds in (5, 6):
        for name, bits in (("sha3-256", 64), ("keccak800", 32)):
            Word.operations = 0
            keccak._permute_lanes([Word(i) for i in range(25)], bits, rounds)
            result[f"{name}-r{rounds}"] = Word.operations
    for rounds in (1, 2):
        Word.operations = 0
        blake3._compress(tuple(Word(x) for x in blake3.IV),
                         tuple(Word(i) for i in range(16)), Word(0), Word(64), Word(11), rounds)
        result[f"blake3-r{rounds}"] = Word.operations
    for rounds in (1, 2):
        result[f"poseidon-r{rounds}"] = sum(poseidon_field_operations(rounds).values())
    return result


class Element(int):
    """Counts modular additions and multiplications in the Poseidon data path."""

    operations = {"add": 0, "mul": 0}

    def __add__(self, other):
        Element.operations["add"] += 1
        return Element(int(self) + int(other))

    def __mul__(self, other):
        Element.operations["mul"] += 1
        return Element(int(self) * int(other))

    def __mod__(self, other):
        # Reduction belongs to the addition or multiplication already charged.
        return Element(int(self) % int(other))

    __radd__ = __add__
    __rmul__ = __mul__


def poseidon_field_operations(rounds):
    """Drive the trusted round function for a prefix of the deployed schedule."""
    poseidon._validate_rounds(rounds)
    Element.operations = {"add": 0, "mul": 0}
    state = [Element(index) for index in range(poseidon.WIDTH)]
    for index in range(rounds):
        state = poseidon.apply_round(
            state, poseidon.ROUND_CONSTANTS[index], full=poseidon.is_full_round(index)
        )
    return dict(Element.operations)


if __name__ == "__main__":
    print(json.dumps(reference_costs(), indent=2, sort_keys=True))
