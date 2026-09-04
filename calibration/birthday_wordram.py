"""Organizer-owned SMALL-N model of the baseline's word-RAM instruction schedule.

Never load or execute program text from candidate/. PROGRAM_TEXT is a fixed local
test fixture, independent of participant input. Python memory/time are NOT the
claimed abstract machine costs; steps and word addresses model that machine.
"""
from __future__ import annotations

import hashlib
from collections import Counter
from dataclasses import dataclass
from typing import Callable

DOMAIN = b"HashSmash birthday v1:"
WORD_MASK = (1 << 128) - 1
FIXED_WORDS = 4096
MAX_TEST_RECORDS = 4096
# Half-open word intervals, including every reserved/padding word.
FIXED_LAYOUT = (
    (0, 3, "message"),
    (3, 16, "padding"),
    (16, 272, "histogram"),
    (272, 528, "positions"),
    (528, 544, "output"),
    (544, 672, "sha_workspace"),
    (672, 674, "descriptors"),
    (674, 738, "registers_and_control"),
    (738, 770, "constants"),
    (770, 1024, "padding"),
    (1024, 2048, "code"),
    (2048, 4096, "padding"),
)

PROGRAM_TEXT = """start:
SHL size N 1
ALLOC A size
ALLOC B size
ST 672 A
ST 673 B
fill_init:
SET i 0
SET p A
fill_test:
LT c i N
BZ c sort_init
fill_body:
ST 0 K0
SHR t i 16
OR t K1 t
ST 1 t
AND t i 65535
SHL t t 112
ST 2 t
SHA hi lo 0
SHL t lo 96
OR t t i
ST p hi
ADD a p 1
ST a t
ADD p p 2
ADD i i 1
JMP fill_test
sort_init:
SET src A
SET dst B
SET j 20
pass_test:
LT c 0 j
BZ c scan_init
pass_setup:
SUB j j 1
SHR q j 4
AND r j 15
SUB s 15 r
SHL s s 3
zero_init:
SET k 0
zero_test:
LT c k 256
BZ c hist_init
zero_body:
ADD a 16 k
ST a 0
ADD k k 1
JMP zero_test
hist_init:
SET p src
SET i 0
hist_test:
LT c i N
BZ c prefix_init
hist_body:
ADD a p q
LD w a
SHR b w s
AND b b 255
ADD a 16 b
LD t a
ADD t t 1
ST a t
ADD p p 2
ADD i i 1
JMP hist_test
prefix_init:
SET k 0
SET total 0
prefix_test:
LT c k 256
BZ c scatter_init
prefix_body:
ADD a 16 k
LD t a
ADD a 272 k
ST a total
ADD total total t
ADD k k 1
JMP prefix_test
scatter_init:
SET p src
SET i 0
scatter_test:
LT c i N
BZ c pass_end
scatter_body:
ADD a p q
LD w a
SHR b w s
AND b b 255
ADD a 272 b
LD pos a
ADD t pos 1
ST a t
SHL a pos 1
ADD a dst a
LD x p
ADD nextp p 1
LD y nextp
ST a x
ADD a a 1
ST a y
ADD p p 2
ADD i i 1
JMP scatter_test
pass_end:
SET t src
SET src dst
SET dst t
JMP pass_test
scan_init:
SET i 1
ADD p src 2
scan_test:
LT c i N
BZ c fail
scan_body:
SUB a p 2
LD x0 a
ADD a a 1
LD x1 a
LD y0 p
ADD a p 1
LD y1 a
EQ c x0 y0
BZ c scan_next
SHR u x1 96
SHR v y1 96
EQ c u v
BZ c scan_next
scan_hit:
AND nonce0 x1 MASK96
AND nonce1 y1 MASK96
JMP verify
scan_next:
ADD p p 2
ADD i i 1
JMP scan_test
verify:
EQ c nonce0 nonce1
BZ c verify_build
JMP fail
verify_build:
ST 528 K0
SHR t nonce0 16
OR t K1 t
ST 529 t
AND t nonce0 65535
SHL t t 112
ST 530 t
ST 531 K0
SHR t nonce1 16
OR t K1 t
ST 532 t
AND t nonce1 65535
SHL t t 112
ST 533 t
SHA h0 l0 528
SHA h1 l1 531
EQ u h0 h1
EQ v l0 l1
AND c u v
BZ c fail
success:
ST 534 1
ST 535 34
ST 536 34
HALT
fail:
ST 534 0
ST 535 0
ST 536 0
HALT
"""


def assemble():
    instructions = []
    labels = {}
    block = ""
    for line in PROGRAM_TEXT.splitlines():
        if not line:
            continue
        if line.endswith(":"):
            block = line[:-1]
            labels[block] = len(instructions)
        else:
            instructions.append((block, line.split()))
    return instructions, labels


@dataclass
class Execution:
    registers: dict[str, int]
    memory: dict[int, int]
    steps: int
    block_steps: dict[str, int]
    hash_calls: int
    messages: tuple[bytes, ...]
    allocated_words: int

    def records(self):
        base = self.registers["src"]
        return [
            self.memory[base + 2 * i].to_bytes(16, "big")
            + self.memory[base + 2 * i + 1].to_bytes(16, "big")
            for i in range(self.registers["i_count"])
        ]


def run_small(n: int, digest: Callable[[bytes], bytes] | None = None) -> Execution:
    """Run only the organizer-owned program with a bounded test sample.

    An injected digest is for synthetic sorting/verification tests only. It is
    never available to the production verifier/judge or a participant.
    """
    if isinstance(n, bool) or not isinstance(n, int) or not 1 <= n <= MAX_TEST_RECORDS:
        raise ValueError("small-n reference requires 1 <= n <= 4096")
    if digest is None:
        digest = lambda message: hashlib.sha1(message, usedforsecurity=False).digest()
    assert len(DOMAIN) == 22
    constants = {
        "N": n,
        "K0": int.from_bytes(DOMAIN[:16], "big"),
        "K1": int.from_bytes(DOMAIN[16:], "big") << 80,
        "MASK96": (1 << 96) - 1,
    }
    instructions, labels = assemble()
    registers: dict[str, int] = {}
    memory: dict[int, int] = {}
    counts: Counter[str] = Counter()
    pc = 0
    heap = FIXED_WORDS
    hash_calls = 0

    def value(token):
        if token.isdecimal():
            return int(token)
        if token in constants:
            return constants[token]
        return registers[token]  # Reading an uninitialized register is a test failure.

    def address(token):
        result = value(token)
        if not 0 <= result < heap:
            raise AssertionError("word address outside reserved storage")
        return result

    def message_at(base):
        return b"".join(memory[base + i].to_bytes(16, "big") for i in range(3))[:34]

    steps = 0
    while True:
        if steps > 1000 * n + 200000:
            raise AssertionError("instruction budget exceeded")
        block, parts = instructions[pc]
        op, args = parts[0], parts[1:]
        pc += 1
        steps += 1
        counts[block] += 1
        if op == "HALT":
            break
        if op == "SET":
            registers[args[0]] = value(args[1])
        elif op == "ALLOC":
            registers[args[0]] = heap
            heap += value(args[1])
        elif op == "LD":
            registers[args[0]] = memory[address(args[1])]
        elif op == "ST":
            memory[address(args[0])] = value(args[1])
        elif op == "BZ":
            if value(args[0]) == 0:
                pc = labels[args[1]]
        elif op == "JMP":
            pc = labels[args[0]]
        elif op == "SHA":
            raw = digest(message_at(address(args[2])))
            if not isinstance(raw, bytes) or len(raw) != 20:
                raise ValueError("test digest must return exactly 20 bytes")
            registers[args[0]] = int.from_bytes(raw[:16], "big")
            # Canonical zero-extension: SHA overwrites the ENTIRE result word.
            registers[args[1]] = int.from_bytes(raw[16:], "big")
            hash_calls += 1
        else:
            left, right = value(args[1]), value(args[2])
            operations = {
                "ADD": lambda: left + right,
                "SUB": lambda: left - right,
                "SHL": lambda: left << right,
                "SHR": lambda: left >> right,
                "AND": lambda: left & right,
                "OR": lambda: left | right,
                "EQ": lambda: int(left == right),
                "LT": lambda: int(left < right),
            }
            registers[args[0]] = operations[op]() & WORD_MASK
    messages = (message_at(528), message_at(531)) if memory[534] else ()
    registers["i_count"] = n  # Diagnostic only, not an algorithm register.
    return Execution(registers, memory, steps, dict(counts), hash_calls, messages, heap)


def time_upper_bound(n: int) -> int:
    # Allocation/descriptors + fill + sort + scan + verify/return.
    # Public program/literal operands are resident machine state, charged in memory.
    return 5 + (18 * n + 4) + (680 * n + 77325) + (18 * (n - 1) + 4) + 32


def memory_upper_bound(n: int) -> int:
    return 64 * n + 16 * FIXED_WORDS
