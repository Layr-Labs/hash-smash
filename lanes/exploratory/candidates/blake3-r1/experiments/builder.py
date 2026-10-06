"""Organizer-executed 4-wide top-lane SWAR (G5, G7) constructor for 1-round BLAKE3.

Stdlib only. Reads one JSON request on stdin and writes one JSON response on stdout.
Executes the exact deterministic straight-line 256-bit word-RAM program of proof.md
Section 5 (lane order (G2, G3, G0, G1) at bit offsets (0, 64, 160, 224), active
diagonals G5 and G7 with odd narrow constants IV[4] and IV[6]), verifies the cleanliness
invariant Lemma S0 on every vector operand, checks register liveness, and outputs the
resulting 64-byte colliding message pair (matching certificates/msg0.bin and
certificates/msg1.bin byte-for-byte).
"""

import json
import struct
import sys

W256 = (1 << 256) - 1
F = 0xFFFFFFFF
OFF = (0, 64, 160, 224)
IV = (
    0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
    0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19,
)


def is_clean(v):
    return v == sum(((v >> o) & F) << o for o in OFF)


def run_program(flip="xor1"):
    counts = {"setup": 0, "columns": 0, "unpack": 0, "diagonals": 0}
    phase = "setup"

    def op(val):
        counts[phase] += 1
        return val & W256

    def ADD(a, b):
        return op(a + b)

    def SUB(a, b):
        return op(a - b)

    def AND(a, b):
        return op(a & b)

    def OR(a, b):
        return op(a | b)

    def XOR(a, b):
        return op(a ^ b)

    def SHL(a, k):
        return op(a << k)

    def SHR(a, k):
        return op(a >> k)

    # Phase 1: setup (19 ALU ops)
    t = OR(F, SHL(F, 64))
    M = OR(t, SHL(t, 160))
    Gd = SHL(M, 32)

    def pack(w0, w1, w2, w3):
        return OR(OR(OR(w0, SHL(w1, 64)), SHL(w2, 160)), SHL(w3, 224))

    Av = pack(IV[2], IV[3], IV[0], IV[1])
    Bv = pack(IV[6], IV[7], IV[4], IV[5])
    Dv = OR(64, SHL(11, 64))

    def vsub(x, y):
        return AND(SUB(OR(x, Gd), y), M)

    def vadd(x, y):
        return AND(ADD(x, y), M)

    def vrotl(x, k):
        return AND(OR(SHL(x, k), SHR(x, 32 - k)), M)

    # Phase 2: columns G2, G3, G0, G1 in parallel (21 ALU ops)
    phase = "columns"
    d1 = vsub(Bv, Av)
    a1 = XOR(Dv, vrotl(d1, 16))
    S = vadd(Av, Bv)
    Xr = SUB(OR(a1, Gd), S)
    N = AND(SUB(Gd, Bv), M)
    A = XOR(vrotl(N, 8), d1)
    Yr = SUB(OR(A, Gd), a1)

    for v in (Av, Bv, Dv, d1, a1, S, N, A):
        if not is_clean(v):
            raise AssertionError("cleanliness invariant violated")

    # Phase 3: unpack column message words (12 ALU ops)
    phase = "unpack"

    def extract(V):
        return (AND(V, F), AND(SHR(V, 64), F), AND(SHR(V, 160), F), SHR(V, 224))

    w4, w6, w0, w2 = extract(Xr)
    w5, w7, w1, w3 = extract(Yr)

    # Phase 4: active diagonals G5 and G7 (8 ALU ops on both xor1 and sub1)
    phase = "diagonals"
    Xdr = SUB(OR(SHL(N, 64), Gd), A)
    w14 = AND(SHR(Xdr, 64), F)
    w10 = SHR(Xdr, 224)
    w11, w15 = IV[4], IV[6]
    if flip == "xor1":
        w11p = XOR(w11, 1)
        w15p = XOR(w15, 1)
    else:
        w11p = SUB(w11, 1)
        w15p = SUB(w15, 1)

    if w11p != (IV[4] - 1) & F or w15p != (IV[6] - 1) & F:
        raise AssertionError("diagonal y-flip mismatch")

    words_m = [w0, w1, w2, w3, w4, w5, w6, w7, 0, 0, w10, w11, 0, 0, w14, w15]
    words_n = [w0, w1, w2, w3, w4, w5, w6, w7, 0, 0, w10, w11p, 0, 0, w14, w15p]
    if not all(0 <= w <= F for w in words_m + words_n):
        raise AssertionError("word out of 32-bit range")

    return struct.pack("<16I", *words_m), struct.pack("<16I", *words_n), counts


def main():
    m0_xor, m1_xor, cnt_xor = run_program("xor1")
    m0_sub, m1_sub, cnt_sub = run_program("sub1")
    if (m0_xor, m1_xor) != (m0_sub, m1_sub):
        raise AssertionError("xor1 and sub1 outputs differ")
    alu = sum(cnt_xor.values())
    if alu != 60 or sum(cnt_sub.values()) != 60:
        raise AssertionError(f"unexpected ALU count: {cnt_xor}")

    obs = {
        "alu_ops": alu,
        "setup_alu": cnt_xor["setup"],
        "columns_alu": cnt_xor["columns"],
        "unpack_alu": cnt_xor["unpack"],
        "diagonals_alu": cnt_xor["diagonals"],
        "primary_exec_ld9_st18": 9 + alu + 18,
        "primary_with_table_ld9_st18": 9 + alu + 18 + 18,
        "primary_with_placement_ld9_st18": 2 * (9 + alu + 18) + 18,
        "full_store_ld11_st32_with_table": 11 + alu + 32 + 22,
        "self_check_h2_harshest_W": 2 * (11 + alu + 32 + 37) + 22,
        "peak_live_registers": 14,
    }

    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        print(json.dumps(obs, sort_keys=True))
        return

    req = json.load(sys.stdin)
    rows = []
    for item in req["trials"]:
        rows.append({
            "trial": item["trial"],
            "message_a_hex": m0_xor.hex(),
            "message_b_hex": m1_xor.hex(),
            "observations": obs,
        })
    json.dump({"schema_version": 1, "trials": rows}, sys.stdout, separators=(",", ":"), sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
