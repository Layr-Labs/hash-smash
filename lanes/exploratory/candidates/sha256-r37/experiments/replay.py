"""sha256-r37 capped-search port of ePrint 2026/1120 SS4.2 (Li-Zhang-Li-Liu-Qian-Zhu).

Self-contained (organizer Docker mounts exactly this file). Embeds the
published Table-17 anchor (ePrint 2026/1120), re-derives the 8-round
trajectory and the SS4.2 round-inverse completion at startup, and runs a
SCALED copy of the full 3-block ordinary padded-message protocol:

  m = B1 || B2 || PAD    (128 data bytes; PAD is the fixed FIPS block whose
  W14|W15 field holds the bitlength 1024, so the attack block's W14/W15
  degree of freedom is never touched by padding; both members share B1, the
  recovered W0..W7, W8..W13 and PAD, and differ in B2 words 6,7,8,9,10,14,15
  by the published Table-15 delta pattern.)

Trial protocol (identical shape to the full attack, scaled depths
N_CHAIN = 256, GATE_CAP = 16, N_DOF = 16):
  1. N_CHAIN pseudo-random forward blocks B1 from the organizer seed;
     CV1 = compress37(IV, B1).
  2. Trajectory A0..A7,E0..E7 = forward(CV1, B1_words 0..7, 8); recover
     W0..W7 by SS4.2 round-inverse; gate on the six Table-16 bit conditions
     of W6 (3) and W7 (3).
  3. For each gate pass (up to GATE_CAP), N_DOF pseudo-random (W14,W15)
     completions; build both members, hash both with the embedded 37-round
     core, and return the first pair whose digest XOR vanishes on the
     organizer event mask.

All returned pairs are checked by this program's own core before emission;
the organizer re-checks them independently. Deterministic: same request
bytes always yield identical output.
"""
import hashlib
import json
import struct
import sys

MASK = 0xFFFFFFFF
K64 = struct.unpack(
    ">64I",
    bytes.fromhex(
        "428a2f9871374491b5c0fbcfe9b5dba53956c25b59f111f1923f82a4ab1c5ed5"
        "d807aa9812835b01243185be550c7dc372be5d7480deb1fe9bdc06a7c19bf174"
        "e49b69c1efbe47860fc19dc6240ca1cc2de92c6f4a7484aa5cb0a9dc76f988da"
        "983e5152a831c66db00327c8bf597fc7c6e00bf3d5a7914706ca635114292967"
        "27b70a852e1b21384d2c6dfc53380d13650a7354766a0abb81c2c92e92722c85"
        "a2bfe8a1a81a664bc24b8b70c76c51a3d192e819d6990624f40e3585106aa070"
        "19a4c1161e376c082748774c34b0bcb5391c0cb34ed8aa4a5b9cca4f682e6ff3"
        "748f82ee78a5636f84c878148cc7020890befffaa4506cebbef9a3f7c67178f2"
    ),
)
IV = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
      0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)

# Published Table-17 anchor pair (semi-free-start; ePrint 2026/1120).
ANCHOR_HEX = (
    "4d7f86ff32ece589d8accfc42cc2e433068b5b34eba68a282fe12cad6aa26b0c"
    "9f0d78e1681b8277faa9c7e056aed439cc2dbbc2dd2ba0fcb95d377b5dd43a81")
ANCHOR_CV_HEX = "63b4986c35d83dc0c98894e4784e08fc78a7f7525ed877a8315a2db3d5614eb4"
ANCHOR_PAIR_HEX = (
    "4d7f86ff32ece589d8accfc42cc2e433068b5b34eba68a280fe12cad6ee2630c"
    "bf0d78e16d1a90ddfaa1d3e056aed439cc2dbbc2dd2ba0fcbd1d3f7b7dd43a81")
DELTA = {6: 0x20000000, 7: 0x04400800, 8: 0x20000000,
         9: 0x050112AA, 10: 0x00081400, 14: 0x04400800, 15: 0x20000000}

N_CHAIN = 256
GATE_CAP = 16
N_DOF = 16


def ror(x, n):
    return ((x >> n) | (x << (32 - n))) & MASK


def compress(state, block, rounds):
    w = list(struct.unpack(">16I", block))
    for i in range(16, rounds):
        x, y = w[i - 15], w[i - 2]
        w.append((w[i - 16] + (ror(x, 7) ^ ror(x, 18) ^ (x >> 3))
                  + w[i - 7] + (ror(y, 17) ^ ror(y, 19) ^ (y >> 10))) & MASK)
    a, b, c, d, e, f, g, h = state
    for i in range(rounds):
        t1 = (h + (ror(e, 6) ^ ror(e, 11) ^ ror(e, 25))
              + ((e & f) ^ ((~e) & g)) + K64[i] + w[i]) & MASK
        t2 = ((ror(a, 2) ^ ror(a, 13) ^ ror(a, 22))
              + ((a & b) ^ (a & c) ^ (b & c))) & MASK
        a, b, c, d, e, f, g, h = (t1 + t2) & MASK, a, b, c, (d + t1) & MASK, e, f, g
    return tuple((s + v) & MASK for s, v in zip(state, (a, b, c, d, e, f, g, h)))


def digest37(data):
    padded = data + b"\x80" + bytes((55 - len(data)) % 64) + (8 * len(data)).to_bytes(8, "big")
    state = IV
    for off in range(0, len(padded), 64):
        state = compress(state, padded[off:off + 64], 37)
    return b"".join(v.to_bytes(4, "big") for v in state)


def i2b(ws):
    return b"".join((v & MASK).to_bytes(4, "big") for v in ws)


def b2i(bs):
    return list(struct.unpack(">%dI" % (len(bs) // 4), bs))


def forward(cv, w16, rounds=8):
    """returns trajectories A[i], E[i] (working a/e after round i)."""
    w = list(w16)
    for i in range(16, rounds):
        x, y = w[i - 15], w[i - 2]
        w.append((w[i - 16] + (ror(x, 7) ^ ror(x, 18) ^ (x >> 3))
                  + w[i - 7] + (ror(y, 17) ^ ror(y, 19) ^ (y >> 10))) & MASK)
    a, b, c, d, e, f, g, h = cv
    A, E = {}, {}
    for i in range(rounds):
        t1 = (h + (ror(e, 6) ^ ror(e, 11) ^ ror(e, 25))
              + ((e & f) ^ ((~e) & g)) + K64[i] + w[i]) & MASK
        t2 = ((ror(a, 2) ^ ror(a, 13) ^ ror(a, 22))
              + ((a & b) ^ (a & c) ^ (b & c))) & MASK
        a, b, c, d, e, f, g, h = (t1 + t2) & MASK, a, b, c, (d + t1) & MASK, e, f, g
        A[i] = a
        E[i] = e
    return A, E


def complete_w07(cv, A, E):
    """SS4.2 round-inverse recovery of W0..W7 from the 8-round trajectory and
    the block chaining input cv = (a,b,c,d,e,f,g,h)
    = (A-1,A-2,A-3,A-4,E-1,E-2,E-3,E-4)."""
    S0 = lambda x: ror(x, 2) ^ ror(x, 13) ^ ror(x, 22)
    S1 = lambda x: ror(x, 6) ^ ror(x, 11) ^ ror(x, 25)
    ch = lambda x, y, z: ((x & y) ^ ((~x) & z)) & MASK
    mj = lambda x, y, z: (x & y) ^ (x & z) ^ (y & z)
    # hidden message-extension vars from the t2 equations (i = 0..3):
    # a_i = t1_i + t2_i, e_i = a_{i-4} + t1_i  =>  E_i = A_i + A_{i-4}
    #      - S0(A_{i-1}) - Maj(A_{i-1},A_{i-2},A_{i-3})
    E0 = (A[0] + cv[3] - S0(cv[0]) - mj(cv[0], cv[1], cv[2])) & MASK
    E1 = (A[1] + cv[2] - S0(A[0]) - mj(A[0], cv[0], cv[1])) & MASK
    E2 = (A[2] + cv[1] - S0(A[1]) - mj(A[1], A[0], cv[0])) & MASK
    E3 = (A[3] + cv[0] - S0(A[2]) - mj(A[2], A[1], A[0])) & MASK
    # words from the t1 equations: W_i = E_i - A_{i-4} - E_{i-4}
    #                                   - S1(E_{i-1}) - Ch(E_{i-1},E_{i-2},E_{i-3}) - K_i
    W0 = (E0 - cv[3] - cv[7] - S1(cv[4]) - ch(cv[4], cv[5], cv[6]) - K64[0]) & MASK
    W1 = (E1 - cv[2] - cv[6] - S1(E0) - ch(E0, cv[4], cv[5]) - K64[1]) & MASK
    W2 = (E2 - cv[1] - cv[5] - S1(E1) - ch(E1, E0, cv[4]) - K64[2]) & MASK
    W3 = (E3 - cv[0] - cv[4] - S1(E2) - ch(E2, E1, E0) - K64[3]) & MASK
    W4 = (E[4] - A[0] - E0 - S1(E3) - ch(E3, E2, E1) - K64[4]) & MASK
    W5 = (E[5] - A[1] - E1 - S1(E[4]) - ch(E[4], E3, E2) - K64[5]) & MASK
    W6 = (E[6] - A[2] - E2 - S1(E[5]) - ch(E[5], E[4], E3) - K64[6]) & MASK
    W7 = (E[7] - A[3] - E3 - S1(E[6]) - ch(E[6], E[5], E[4]) - K64[7]) & MASK
    return [W0, W1, W2, W3, W4, W5, W6, W7]


def gate6(w6, w7):
    b = lambda x, i: (x >> i) & 1
    return ((b(w6, 1) == b(w6, 12)) and (b(w6, 8) != b(w6, 25))
            and (b(w6, 14) == b(w6, 18)) and (b(w7, 0) == b(w7, 28))
            and (b(w7, 9) == b(w7, 30)) and (b(w7, 1) == b(w7, 18)))


def digest64(data):
    padded = data + b"\x80" + bytes((55 - len(data)) % 64) + (8 * len(data)).to_bytes(8, "big")
    state = IV
    for off in range(0, len(padded), 64):
        state = compress(state, padded[off:off + 64], 64)
    return state


def selftest():
    try:
        for t in range(6):
            blk = hashlib.sha256(str(t).encode()).digest() * 2
            if digest64(blk) != tuple(b2i(hashlib.sha256(blk).digest())):
                return 0
        anchor = b2i(bytes.fromhex(ANCHOR_HEX))
        pair = b2i(bytes.fromhex(ANCHOR_PAIR_HEX))
        cv = b2i(bytes.fromhex(ANCHOR_CV_HEX))
        if compress(cv, i2b(anchor), 37) != compress(cv, i2b(pair), 37):
            return 0
        if compress(cv, i2b(anchor), 38) == compress(cv, i2b(pair), 38):
            return 0
        A, E = forward(cv, anchor[:16], 8)
        w07 = complete_w07(cv, A, E)
        if w07 != anchor[:8]:
            return 0
        if not gate6(w07[6], w07[7]):
            return 0
        return 1
    except Exception:
        return 0


def run_trial(seed_hex, event):
    mask = int(event["mask_hex"], 16)
    want = int(event["expected_hex"], 16)
    base = bytes.fromhex(seed_hex)
    passes = 0
    hits = 0
    for c in range(N_CHAIN):
        b1 = (hashlib.sha256(base + b"|B1|%d" % c).digest()
              + hashlib.sha256(base + b"|b1|%d" % c).digest())
        cv1 = compress(IV, b1, 37)
        w16 = list(struct.unpack(">16I", b1))
        A, E = forward(cv1, w16[:16], 8)
        w07 = complete_w07(cv1, A, E)
        if not gate6(w07[6], w07[7]):
            continue
        passes += 1
        if passes > GATE_CAP:
            break
        for d in range(N_DOF):
            w14 = int.from_bytes(hashlib.sha256(base + b"|14|%d|%d" % (c, d)).digest()[:4], "big")
            w15 = int.from_bytes(hashlib.sha256(base + b"|15|%d|%d" % (c, d)).digest()[:4], "big")
            wA = w07 + [w16[8], w16[9], w16[10], w16[11], w16[12], w16[13], w14, w15]
            wB = [w ^ DELTA.get(i, 0) for i, w in enumerate(wA)]
            ma = b1 + i2b(wA)
            mb = b1 + i2b(wB)
            da, db = digest37(ma), digest37(mb)
            hits += 1
            if da != db and ((int.from_bytes(da, "big") ^ int.from_bytes(db, "big")) & mask) == want:
                return ma.hex(), mb.hex(), passes, hits
    return None, None, passes, hits


def main():
    request = json.loads(sys.stdin.readline())
    event = request["event"]
    rows = []
    for t in request["trials"]:
        if t["trial"] == 0:
            if selftest() == 0:
                raise SystemExit(1)
        ma, mb, passes, hits = run_trial(t["seed"], event)
        obs = {"gate_passes": passes, "pairs_checked": hits}
        if t["trial"] == 0:
            obs["selftest"] = 1
        rows.append({"trial": t["trial"], "message_a_hex": ma,
                     "message_b_hex": mb, "observations": obs})
    json.dump({"schema_version": 1, "trials": rows}, sys.stdout)


if __name__ == "__main__":
    main()
