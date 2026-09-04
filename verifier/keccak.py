"""Organizer-owned byte-message Keccak sponge reference implementations.

SHA3-256 uses FIPS 202 rate 1088/capacity 512, 256 output bits, and
delimited suffix 0x06. The experimental Keccak-800 instance has rate 544,
capacity 256, 256 output bits, and legacy delimited suffix 0x01.

Reduced variants always execute rounds 0 through rounds-1 on every absorbed
block. These are prefix reductions, NOT Keccak-p's last-round convention.
Lane index is x + 5*y; each lane is serialized in little-endian order.

Specification: https://keccak.team/keccak_specs_summary.html
"""


ROUND_CONSTANTS = (
    0x0000000000000001, 0x0000000000008082, 0x800000000000808A,
    0x8000000080008000, 0x000000000000808B, 0x0000000080000001,
    0x8000000080008081, 0x8000000000008009, 0x000000000000008A,
    0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
    0x000000008000808B, 0x800000000000008B, 0x8000000000008089,
    0x8000000000008003, 0x8000000000008002, 0x8000000000000080,
    0x000000000000800A, 0x800000008000000A, 0x8000000080008081,
    0x8000000000008080, 0x0000000080000001, 0x8000000080008008,
)
RHO_OFFSETS = (
    0, 1, 62, 28, 27,
    36, 44, 6, 55, 20,
    3, 10, 43, 25, 39,
    41, 45, 15, 21, 8,
    18, 2, 61, 56, 14,
)


def _validate_rounds(width_bits: int, rounds: int) -> None:
    if type(width_bits) is not int or width_bits not in (800, 1600):
        raise ValueError("Keccak width must be 800 or 1600 bits")
    full_rounds = 22 if width_bits == 800 else 24
    if type(rounds) is not int or not 1 <= rounds <= full_rounds:
        raise ValueError("unsupported Keccak prefix round count")


def _rotate(value: int, amount: int, lane_bits: int, mask: int) -> int:
    amount %= lane_bits
    return ((value << amount) | (value >> ((lane_bits - amount) % lane_bits))) & mask


def _permute_lanes(lanes: list[int], lane_bits: int, rounds: int) -> None:
    mask = (1 << lane_bits) - 1
    for constant in ROUND_CONSTANTS[:rounds]:
        parity = [lanes[x] ^ lanes[x + 5] ^ lanes[x + 10] ^ lanes[x + 15] ^ lanes[x + 20]
                  for x in range(5)]
        theta = [parity[(x - 1) % 5] ^ _rotate(parity[(x + 1) % 5], 1, lane_bits, mask)
                 for x in range(5)]
        moved = [0] * 25
        for y in range(5):
            for x in range(5):
                index = x + 5 * y
                # Rho followed by pi: B[y, 2*x + 3*y] = rot(A[x,y]).
                moved[y + 5 * ((2 * x + 3 * y) % 5)] = _rotate(
                    lanes[index] ^ theta[x], RHO_OFFSETS[index], lane_bits, mask)
        for y in range(5):
            for x in range(5):
                lanes[x + 5 * y] = (moved[x + 5 * y] ^
                    ((~moved[(x + 1) % 5 + 5 * y]) & moved[(x + 2) % 5 + 5 * y])) & mask
        lanes[0] ^= constant & mask


def permutation(state: bytes, *, width_bits: int = 1600, rounds: int = 24) -> bytes:
    """Apply a pinned prefix of Keccak-f to exactly one serialized state."""
    _validate_rounds(width_bits, rounds)
    if not isinstance(state, bytes) or len(state) != width_bits // 8:
        raise ValueError("state must be bytes of exactly the selected Keccak width")
    lane_bytes = width_bits // 200
    lanes = [int.from_bytes(state[i:i + lane_bytes], "little")
             for i in range(0, len(state), lane_bytes)]
    _permute_lanes(lanes, lane_bytes * 8, rounds)
    return b"".join(lane.to_bytes(lane_bytes, "little") for lane in lanes)


def _sponge(data: bytes, *, width_bits: int, rate_bytes: int, suffix: int, rounds: int) -> bytes:
    _validate_rounds(width_bits, rounds)
    if not isinstance(data, bytes):
        raise ValueError("hash input must be bytes")
    # Both fixed profiles have a one-byte delimited suffix with its high bit
    # clear; the final padding bit can share that byte at a rate boundary.
    padded = bytearray(data)
    padded.append(suffix)
    padded.extend(bytes((-len(padded)) % rate_bytes))
    padded[-1] |= 0x80
    lane_bytes = width_bits // 200
    lanes = [0] * 25
    for offset in range(0, len(padded), rate_bytes):
        block = padded[offset:offset + rate_bytes]
        for index in range(rate_bytes // lane_bytes):
            start = index * lane_bytes
            lanes[index] ^= int.from_bytes(block[start:start + lane_bytes], "little")
        _permute_lanes(lanes, lane_bytes * 8, rounds)
    # Both profiles emit 32 bytes, less than their rate, so no additional
    # squeeze permutation is needed.
    return b"".join(lane.to_bytes(lane_bytes, "little") for lane in lanes)[:32]


def sha3_256(data: bytes, rounds: int = 24) -> bytes:
    """SHA3-256 with the first ``rounds`` Keccak-f[1600] rounds per block."""
    return _sponge(data, width_bits=1600, rate_bytes=136, suffix=0x06, rounds=rounds)


def keccak800(data: bytes, rounds: int = 22) -> bytes:
    """Keccak[rate=544, capacity=256, output=256], legacy padding, prefix rounds."""
    return _sponge(data, width_bits=800, rate_bytes=68, suffix=0x01, rounds=rounds)
