"""Deterministic equivalence probe, not a collision search or cost benchmark.

Public Keccak round equations and constants are from FIPS 202. Run only through
the organizer's immutable-source, networkless Python executor.
"""
import hashlib
import json
import struct
import sys

Z = (1 << 256) - 1
MASK64 = (1 << 64) - 1
RHO = (0, 1, 62, 28, 27, 36, 44, 6, 55, 20, 3, 10, 43, 25, 39,
       41, 45, 15, 21, 8, 18, 2, 61, 56, 14)
RC = (0x1, 0x8082, 0x800000000000808A, 0x8000000080008000,
      0x808B, 0x80000001)
OPS = 0


def transpose(rows):
    rows = list(rows)
    for s in (128, 64, 32, 16, 8, 4, 2, 1):
        mask = sum(1 << c for c in range(256) if not c & s)
        for i in range(256):
            if not i & s:
                a, b = rows[i], rows[i+s]
                t0 = a >> s
                t1 = t0 ^ b
                t2 = t1 & mask
                t3 = t2 << s
                rows[i] = a ^ t3
                rows[i+s] = b ^ t2
    return rows


def xor(a, b):
    global OPS
    if a[1] and b[1]:
        return a[0] ^ b[0], True
    if a[1] and a[0] == 0:
        return b
    if b[1] and b[0] == 0:
        return a
    OPS += 1
    return a[0] ^ b[0], False


def negate(a):
    global OPS
    if not a[1]:
        OPS += 1
    return a[0] ^ Z, a[1]


def conjunction(a, b):
    global OPS
    if a[1] and b[1]:
        return a[0] & b[0], True
    if a[1]:
        return (0, True) if a[0] == 0 else b
    if b[1]:
        return (0, True) if b[0] == 0 else a
    OPS += 1
    return a[0] & b[0], False


def round_planes(state, ri):
    global OPS
    OPS = 0
    c = [[state[x][z] for z in range(64)] for x in range(5)]
    for x in range(5):
        for z in range(64):
            for y in range(1, 5):
                c[x][z] = xor(c[x][z], state[x+5*y][z])
    parity_ops = OPS
    d = [[xor(c[(x-1)%5][z], c[(x+1)%5][(z-1)%64])
          for z in range(64)] for x in range(5)]
    d_ops = OPS - parity_ops
    b = [None] * 25
    lanes = (0, 6, 12, 18, 24) if ri == 5 else range(25)
    for i in lanes:
        x, y = i % 5, i // 5
        a = [xor(state[i][z], d[x][z]) for z in range(64)]
        b[y+5*((2*x+3*y)%5)] = [a[(z-RHO[i])%64] for z in range(64)]
    theta_ops = OPS - parity_ops - d_ops
    out = [None] * 25
    for i in (range(4) if ri == 5 else range(25)):
        x, y = i % 5, i // 5
        out[i] = [xor(b[i][z], conjunction(negate(b[(x+1)%5+5*y][z]),
                                        b[(x+2)%5+5*y][z])) for z in range(64)]
    chi_ops = OPS - parity_ops - d_ops - theta_ops
    for z in range(64):
        if RC[ri] >> z & 1:
            out[0][z] = xor(out[0][z], (Z, True))
    return out, (parity_ops, d_ops, theta_ops, chi_ops,
                 OPS-parity_ops-d_ops-theta_ops-chi_ops)


def bitsliced(messages):
    assert len(messages) == 256 and all(len(m) == 64 for m in messages)
    left = [int.from_bytes(m[:32], "little") for m in messages]
    right = [int.from_bytes(m[32:], "little") for m in messages]
    assert transpose(transpose(left)) == left
    assert transpose(transpose(right)) == right
    inputs = transpose(left) + transpose(right)
    state = [[(inputs[64*i+z], False) if i < 8 else
              (Z if (i == 8 and z in (1, 2)) or (i == 16 and z == 63) else 0, True)
              for z in range(64)] for i in range(25)]
    counts = []
    for ri in range(6):
        state, count = round_planes(state, ri)
        counts.append(count)
    output = transpose([state[i][z][0] for i in range(4) for z in range(64)])
    assert counts[0] == (195, 320, 515, 4800, 1), counts[0]
    assert sum(counts[-1]) <= 2752, counts[-1]
    return [v.to_bytes(32, "little") for v in output], counts


def scalar(message):
    block = message + b"\x06" + bytes(70) + b"\x80"
    a = list(struct.unpack("<17Q", block)) + [0] * 8
    for rc in RC:
        c = [a[x] ^ a[x+5] ^ a[x+10] ^ a[x+15] ^ a[x+20] for x in range(5)]
        d = [c[(x-1)%5] ^ ((c[(x+1)%5] << 1 | c[(x+1)%5] >> 63) & MASK64)
             for x in range(5)]
        b = [0] * 25
        for x in range(5):
            for y in range(5):
                i = x + 5*y
                v = a[i] ^ d[x]
                r = RHO[i]
                b[y+5*((2*x+3*y)%5)] = ((v << r) | (v >> (64-r))) & MASK64
        a = [b[x+5*y] ^ ((~b[(x+1)%5+5*y] & MASK64) & b[(x+2)%5+5*y])
             for y in range(5) for x in range(5)]
        a[0] ^= rc
    return struct.pack("<4Q", *a[:4])


def main():
    request = json.load(sys.stdin)
    assert request["schema_version"] == 1
    assert request["target_profile"] == "sha3-256-r6-prefix-v1"
    assert request["experiment_id"] == "bitslice-padding-equivalence"
    items = request["trials"]
    assert 1 <= len(items) <= 256
    messages = [hashlib.shake_256(b"sha3-padding-check-v1" + bytes.fromhex(item["seed"])).digest(64)
                for item in items]
    # Additional fixed edge cases fill unused slots; a full request adds them below.
    padded = messages + [bytes(64)] * (256-len(messages))
    outputs, counts = bitsliced(padded)
    assert all(outputs[i] == scalar(m) for i, m in enumerate(padded))
    edge_messages = [bytes(64), b"\xff"*64, bytes(range(64))] + [bytes(64)]*253
    edge_outputs, _ = bitsliced(edge_messages)
    assert all(edge_outputs[i] == scalar(edge_messages[i]) for i in range(3))
    rows = []
    for item, digest in zip(items, outputs):
        # Null witnesses are intentional: equivalence is the experiment's purpose.
        rows.append({"trial": item["trial"], "message_a_hex": None, "message_b_hex": None,
                     "observations": {"complete_digest_matches": 1,
                                      "first_round_logical_ops": sum(counts[0]),
                                      "last_round_logical_ops": sum(counts[-1]),
                                      "transpose_involution_passed": 1,
                                      "edge_cases_passed": 3,
                                      "computed_digest": int.from_bytes(digest, "little")}})
    json.dump({"schema_version": 1, "trials": rows}, sys.stdout, sort_keys=True, separators=(",", ":"))
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
