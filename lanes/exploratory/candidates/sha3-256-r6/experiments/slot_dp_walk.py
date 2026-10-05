# -*- coding: utf-8 -*-
"""Bit-sliced six-round SHA3-256 step map: circuit cross-check, 256-slot DP walk, contact test.

Organizer-executed evidence for proof.md Sections 3, 9 and 10. Standard library only.
Reads one JSON request from stdin and writes one JSON document to stdout. Three declared
experiments share this file and branch on request["experiment_id"]:

  bitslice-fullwidth-equivalence  (12-bit mask)
      256 seeded full 256-bit inputs, one bit-sliced batch; returns two slots whose
      bit-sliced digests agree on digest bits 0-2 of each digest lane. A mechanical
      cross-check only: an XOR mask cannot detect an error identical on both messages.

  slot-dp-walk-n14  (14-bit mask)
      The proof.md Section 5 algorithm at reduced width n = 14: step x <- digest planes
      0..13 of LE32(x); 256 slots; DP = digest bit 13 zero (theta = 1/2), keyed on
      bits 0..12; abandonment at 16; reseeding stops after 256 evaluations, then drain;
      same-batch DPs in slot order; halt at the first RELOCATE (scalar f). Returned pairs
      are absolute 14-bit collisions of the real target.

  contact-n18-k00  (18-bit mask; window k = 0)
      Contact test: N = 2^18, exactly K = 512 evaluations, 256 distinct starts, 256 slots
      in batch-major slot-minor order. A trial returns the first-contact collision pair
      (absolute 18-bit collision), or null if the first contact is a start or no contact
      occurs within K.

Numeric observations are untrusted. The program makes no cost claim; contact frequencies
are for descriptive comparison with the random-function prediction in proof.md.
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


def planes_from_values(xs):
    """256 bit planes from 256 values: bit j of plane i = bit i of xs[j] (string transpose)."""
    rows = [format(x, "0256b") for x in reversed(xs)]   # row 0 is slot 255
    cols = zip(*rows)                                   # column c holds bit 255-c of every slot
    planes = [int("".join(col), 2) for col in cols]     # bit j of each int = slot j
    planes.reverse()                                    # index by bit position i
    return planes


def get_slot(planes, j, width):
    v = 0
    for i in range(width):
        v |= ((planes[i] >> j) & 1) << i
    return v


# ---------------------------------------------------------------- experiment 1
EQ_MASK_BITS = (0, 1, 2, 64, 65, 66, 128, 129, 130, 192, 193, 194)


def equivalence_trial(F, rng, obs):
    xs = [rng.getrandbits(256) for _ in range(256)]
    planes = planes_from_values(xs)
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
    j = rng.getrandbits(8)       # untrusted self-check of one full digest
    obs["scalar_mismatch"] = int(get_slot(out, j, 256) != scalar_digest_int(xs[j]))
    return pair


# ---------------------------------------------------------------- experiment 2
N_BITS, T_BITS, L_MAX, K0 = 14, 1, 16, 256
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


# ---------------------------------------------------------------- experiment 3
# Contact-rate test of H-RF at the operating point of proof.md Section 7
# (K^2/2N close to K0^2/2N = 0.5288, 256 concurrent slots, batch-major order).
C_BITS, C_K = 18, 512           # N = 2^18; K = 512 = 2 batches; K^2/2N = 0.5


def contact_sets(k):
    """Output digest bits S_k and input message bits T_k for contact experiment k.
    The declared experiment uses k = 0; other k were used only in undeclared runs."""
    out_bits = [(k + 12 * i) % 256 for i in range(C_BITS)]
    in_bits = [(7 * k + 11 * i) % 256 for i in range(C_BITS)]
    return out_bits, in_bits


def slot_values(planes, bits):
    """Values of all 256 slots on the given planes (bit i of value = planes[bits[i]])."""
    rows = [format(planes[b], "0256b") for b in reversed(bits)]   # top bit first
    cols = zip(*rows)                                             # column c = slot 255-c
    vals = [int("".join(col), 2) for col in cols]
    vals.reverse()                                                # index by slot j
    return vals


def contact_trial(F, rng, obs, k):
    out_bits, in_bits = contact_sets(k)
    starts = set()
    cur = []
    while len(cur) < 256:                       # 256 distinct uniform C_BITS-bit starts
        x = rng.getrandbits(C_BITS)
        if x not in starts:
            starts.add(x)
            cur.append(x)
    pred = {}                                   # output point -> its evaluated input
    known = set(starts)
    pv = planes_from_values(cur)                # pv[i]: bit i of every start
    planes = [0] * 256
    for i in range(C_BITS):
        planes[in_bits[i]] = pv[i]
    evals = 0
    while evals < C_K:
        out = F(planes)
        ys = slot_values(out, out_bits)
        for j in range(256):                    # slot-minor reveal order
            if evals >= C_K:                    # stop at exactly K evaluations
                break
            evals += 1
            y = ys[j]
            if y in known:
                obs["contact_eval"] = evals
                if y in pred:                   # landed on an earlier output: collision
                    obs["outcome"] = 1
                    return (embed(cur[j], in_bits), embed(pred[y], in_bits))
                obs["outcome"] = 2              # landed on a start: no pair exists
                return None
            known.add(y)
            pred[y] = cur[j]
            cur[j] = y
        planes = [0] * 256
        for i in range(C_BITS):                 # digest planes S feed input planes T
            planes[in_bits[i]] = out[out_bits[i]]
    obs["contact_eval"] = 0
    obs["outcome"] = 3                          # no contact within K evaluations
    return None


def embed(x, in_bits):
    v = 0
    for i, b in enumerate(in_bits):
        if (x >> i) & 1:
            v |= 1 << b
    return v


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
        elif exp.startswith("contact-n18-k"):
            pair = contact_trial(F, rng, obs, int(exp[len("contact-n18-k"):]))
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
