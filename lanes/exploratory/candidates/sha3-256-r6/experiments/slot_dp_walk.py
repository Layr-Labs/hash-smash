# -*- coding: utf-8 -*-
"""Bit-sliced six-round SHA3-256 step map and 256-slot distinguished-point walk.

Organizer-executed evidence for proof.md Sections 3, 5 and 10. Standard library only.
Reads one JSON request from stdin and writes one JSON document to stdout.

Two experiments share this file and branch on request["experiment_id"]:

  bitslice-fullwidth-equivalence
      One bit-sliced batch of 256 messages LE32(x), x uniform 256-bit words from the
      trial seed. Digests are taken ONLY from the bit-sliced circuit (proof.md
      Section 3), then two slots whose bit-sliced digests agree on the 12 masked bits
      (bits 0-2 of each digest lane 0..3) are returned. The organizer recomputes both
      complete digests with the reference implementation. A wrong circuit output on
      any masked bit makes the host check fail.

  slot-dp-walk-n20
      The proof.md Section 5 algorithm at reduced width n = 20: x is a 20-bit word and
      the step map is f_n(x) = digest planes 0..19 of LE32(x) (planes 20..255 of the
      next input are zero). 256 chains run in the 256 bit slots. DP = digest bits
      17,18,19 all zero (the top t = 3 bits of the n-bit window, mirroring bits
      224..255 at full width), so theta = 1/8. The record table is keyed on exactly
      the other 17 bits 0..16. Chains are abandoned at L = 128 evaluations. Same-batch
      DPs are processed in slot order. No slot is reseeded once g >= K0 = 2048, and
      in-flight chains are drained. The run halts at its first RELOCATE, as in the
      full algorithm. Returned pairs satisfy the 20-bit output event on the real
      target, which the organizer verifies. The numeric observation "outcome" is
      1 = pair found, 2 = RELOCATE failed (one start lies on the other chain),
      3 = all slots drained without a repeated DP.

The program makes no probability or cost claim. Numeric observations are untrusted.
"""
import json
import random
import sys

RHO = (0, 1, 62, 28, 27, 36, 44, 6, 55, 20, 3, 10, 43, 25, 39,
       41, 45, 15, 21, 8, 18, 2, 61, 56, 14)
RC = (0x0000000000000001, 0x0000000000008082, 0x800000000000808A,
      0x8000000080008000, 0x000000000000808B, 0x0000000080000001)
ROUNDS = 6
M = (1 << 256) - 1
M64 = (1 << 64) - 1


# ---------------------------------------------------------------- scalar reference
def rot(v, k):
    k %= 64
    return ((v << k) | (v >> (64 - k))) & M64 if k else v


def scalar_digest_int(x):
    """Six-round prefix SHA3-256 of the 32-byte message LE32(x), as an integer."""
    a = [0] * 25
    for j in range(4):
        a[j] = (x >> (64 * j)) & M64
    a[4] = 0x06
    a[16] = 0x8000000000000000
    for r in range(ROUNDS):
        c = [a[i] ^ a[i + 5] ^ a[i + 10] ^ a[i + 15] ^ a[i + 20] for i in range(5)]
        d = [c[(i - 1) % 5] ^ rot(c[(i + 1) % 5], 1) for i in range(5)]
        b = [0] * 25
        for y in range(5):
            for i in range(5):
                b[y + 5 * ((2 * i + 3 * y) % 5)] = rot(a[i + 5 * y] ^ d[i], RHO[i + 5 * y])
        a = [b[i + 5 * y] ^ ((~b[(i + 1) % 5 + 5 * y] & M64) & b[(i + 2) % 5 + 5 * y])
             for y in range(5) for i in range(5)]
        a[0] ^= RC[r]
    return a[0] | (a[1] << 64) | (a[2] << 128) | (a[3] << 192)


# ---------------------------------------------------------------- bit-sliced circuit
class Compiler:
    """Symbolic compile of the proof.md Section 3 circuit into straight-line code.

    A signal is ("c", bit) for a public constant plane or ("v", name, flag) where the
    stored plane word is the true plane XOR (flag ? all-ones : 0). XOR with a constant
    and NOT only flip the flag (no instruction). AND of two plain operands is AND;
    of two flagged operands is OR with the flag set (De Morgan); a mixed pair
    materialises one NOT and then an AND.
    """

    def __init__(self):
        self.lines = []
        self.n = 0
        self.ops = {"xor": 0, "and": 0, "or": 0, "not": 0}

    def tmp(self):
        self.n += 1
        return "t%d" % self.n

    def xor(self, a, b):
        if a[0] == "c" and b[0] == "c":
            return ("c", a[1] ^ b[1])
        if a[0] == "c":
            a, b = b, a
        if b[0] == "c":
            return ("v", a[1], a[2] ^ b[1])
        t = self.tmp()
        self.lines.append("%s=%s^%s" % (t, a[1], b[1]))
        self.ops["xor"] += 1
        return ("v", t, a[2] ^ b[2])

    def neg(self, a):
        return ("c", 1 - a[1]) if a[0] == "c" else ("v", a[1], a[2] ^ 1)

    def band(self, a, b):
        if a[0] == "c" and b[0] == "c":
            return ("c", a[1] & b[1])
        if a[0] == "c":
            a, b = b, a
        if b[0] == "c":
            return a if b[1] else ("c", 0)
        t = self.tmp()
        if a[2] == 0 and b[2] == 0:
            self.lines.append("%s=%s&%s" % (t, a[1], b[1]))
            self.ops["and"] += 1
            return ("v", t, 0)
        if a[2] == 1 and b[2] == 1:
            self.lines.append("%s=%s|%s" % (t, a[1], b[1]))
            self.ops["or"] += 1
            return ("v", t, 1)
        if a[2] == 1:
            a, b = b, a
        self.lines.append("%s=%s&(%s^M)" % (t, a[1], b[1]))
        self.ops["not"] += 1
        self.ops["and"] += 1
        return ("v", t, 0)


def compile_circuit():
    cp = Compiler()
    st = [[("c", 0)] * 64 for _ in range(25)]
    for lane in range(4):
        for z in range(64):
            st[lane][z] = ("v", "P[%d]" % (64 * lane + z), 0)
    st[4] = [("c", (0x06 >> z) & 1) for z in range(64)]
    st[16] = [("c", ((1 << 63) >> z) & 1) for z in range(64)]
    for r in range(ROUNDS):
        last = r == ROUNDS - 1
        col = [[None] * 64 for _ in range(5)]
        for x in range(5):
            for z in range(64):
                acc = st[x][z]
                for y in range(1, 5):
                    acc = cp.xor(acc, st[x + 5 * y][z])
                col[x][z] = acc
        dd = [[cp.xor(col[(x - 1) % 5][z], col[(x + 1) % 5][(z - 1) % 64]) for z in range(64)]
              for x in range(5)]
        bb = [None] * 25
        for idx in (range(25) if not last else (0, 6, 12, 18, 24)):
            x, y = idx % 5, idx // 5
            th = [cp.xor(st[idx][z], dd[x][z]) for z in range(64)]
            off = RHO[idx]
            bb[y + 5 * ((2 * x + 3 * y) % 5)] = [th[(z - off) % 64] for z in range(64)]
        out = [None] * 25
        for idx in (range(25) if not last else range(4)):
            x, y = idx % 5, idx // 5
            b1, b2 = bb[(x + 1) % 5 + 5 * y], bb[(x + 2) % 5 + 5 * y]
            out[idx] = [cp.xor(bb[idx][z], cp.band(cp.neg(b1[z]), b2[z])) for z in range(64)]
        out[0] = [cp.xor(out[0][z], ("c", (RC[r] >> z) & 1)) for z in range(64)]
        st = out
    res = []
    fixups = 0
    for lane in range(4):
        for z in range(64):
            s = st[lane][z]
            if s[0] == "c":
                res.append("M" if s[1] else "0")
            elif s[2]:
                res.append("(%s^M)" % s[1])
                fixups += 1
            else:
                res.append(s[1])
    src = "def F(P):\n " + "\n ".join(cp.lines) + "\n return [" + ",".join(res) + "]\n"
    env = {"M": M}
    exec(compile(src, "<bitsliced-sha3-r6>", "exec"), env)
    return env["F"], cp.ops, fixups


def set_slot(planes, j, x, width):
    bit = 1 << j
    inv = M ^ bit
    for i in range(width):
        if (x >> i) & 1:
            planes[i] |= bit
        else:
            planes[i] &= inv


def get_slot(planes, j, width):
    v = 0
    for i in range(width):
        v |= ((planes[i] >> j) & 1) << i
    return v


# ---------------------------------------------------------------- experiment 1
EQ_MASK_BITS = (0, 1, 2, 64, 65, 66, 128, 129, 130, 192, 193, 194)


def equivalence_trial(F, rng, obs):
    xs = [rng.getrandbits(256) for _ in range(256)]
    planes = [0] * 256
    for j, x in enumerate(xs):
        set_slot(planes, j, x, 256)
    out = F(planes)
    seen = {}
    pair = None
    for j in range(256):
        key = 0
        for k, i in enumerate(EQ_MASK_BITS):
            key |= ((out[i] >> j) & 1) << k
        if key in seen and xs[seen[key]] != xs[j] and pair is None:
            pair = (xs[seen[key]], xs[j])
        seen.setdefault(key, j)
    mism = 0
    for j in range(0, 256, 64):  # untrusted self-check of four full digests
        if get_slot(out, j, 256) != scalar_digest_int(xs[j]):
            mism += 1
    obs["scalar_mismatches_of_4"] = mism
    return pair


# ---------------------------------------------------------------- experiment 2
N_BITS, T_BITS, L_MAX, K0 = 20, 3, 128, 2048
KEY_MASK = (1 << (N_BITS - T_BITS)) - 1
N_MASK = (1 << N_BITS) - 1


def f_n(x):
    return scalar_digest_int(x) & N_MASK


def relocate(s1, l1, s2, l2):
    if l1 < l2:
        s1, l1, s2, l2 = s2, l2, s1, l1
    a = s1
    for _ in range(l1 - l2):
        a = f_n(a)
    b = s2
    for _ in range(l2):
        if a == b:
            return None  # one start lies on the other chain
        fa, fb = f_n(a), f_n(b)
        if fa == fb:
            return (a, b)
        a, b = fa, fb
    return None


def walk_trial(F, rng, obs):
    planes = [0] * 256
    start = [0] * 256
    length = [0] * 256
    active = M
    for j in range(256):
        start[j] = rng.getrandbits(N_BITS)
        set_slot(planes, j, start[j], N_BITS)
    table = {}
    inserted_batch = {}
    g = 0
    batch = 0
    dps = 0
    while active:
        out = F(planes)
        batch += 1
        nact = bin(active).count("1")
        g += nact
        for j in range(256):
            if (active >> j) & 1:
                length[j] += 1
        planes = out[:N_BITS] + [0] * (256 - N_BITS)
        anyb = 0
        for i in range(N_BITS - T_BITS, N_BITS):
            anyb |= out[i]
        dpw = (M ^ anyb) & active
        events = dpw
        for j in range(256):
            if (active >> j) & 1 and not (dpw >> j) & 1 and length[j] >= L_MAX:
                events |= 1 << j
        j = 0
        while events >> j:
            if (events >> j) & 1:
                if (dpw >> j) & 1:
                    dps += 1
                    z = get_slot(out, j, N_BITS)
                    key = z & KEY_MASK
                    if key in table:
                        s2, l2 = table[key]
                        obs["batches"] = batch
                        obs["evaluations"] = g
                        obs["dps"] = dps
                        obs["same_batch_dp"] = 1 if inserted_batch[key] == batch else 0
                        pair = relocate(start[j], length[j], s2, l2)
                        obs["outcome"] = 1 if pair else 2
                        return pair
                    table[key] = (start[j], length[j])
                    inserted_batch[key] = batch
                if g < K0:
                    start[j] = rng.getrandbits(N_BITS)
                    length[j] = 0
                    set_slot(planes, j, start[j], N_BITS)
                else:
                    active &= M ^ (1 << j)
            j += 1
    obs["batches"] = batch
    obs["evaluations"] = g
    obs["dps"] = dps
    obs["same_batch_dp"] = 0
    obs["outcome"] = 3
    return None


# ---------------------------------------------------------------- driver
def main():
    req = json.loads(sys.stdin.read())
    F, ops, fixups = compile_circuit()
    exp = req["experiment_id"]
    rows = []
    for t in req["trials"]:
        rng = random.Random(int(t["seed"], 16))
        obs = {"xor": ops["xor"], "and": ops["and"], "or": ops["or"], "not": ops["not"],
               "fixup_planes": fixups}
        if exp == "bitslice-fullwidth-equivalence":
            pair = equivalence_trial(F, rng, obs)
        else:
            pair = walk_trial(F, rng, obs)
        if pair is None:
            ma = mb = None
        else:
            ma = pair[0].to_bytes(32, "little").hex()
            mb = pair[1].to_bytes(32, "little").hex()
        rows.append({"trial": t["trial"], "message_a_hex": ma, "message_b_hex": mb,
                     "observations": obs})
    sys.stdout.write(json.dumps({"schema_version": 1, "trials": rows}, sort_keys=True,
                                separators=(",", ":")))


if __name__ == "__main__":
    main()
