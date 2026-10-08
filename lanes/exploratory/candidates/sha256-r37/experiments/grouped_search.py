# -*- coding: utf-8 -*-
"""Bit-sliced grouped birthday search on reduced-round SHA-256 (r37/r38): scaled evidence.

Organizer-executed evidence for proof.md. Standard library only. Reads one JSON request
from stdin and writes one JSON document to stdout. Five declared experiments share this
file and branch on request["experiment_id"]; the round count R comes from
request["target_profile"] ("sha256-r38-prefix-v1" -> 38, "sha256-r37-prefix-v1" -> 37).

Message family (proof.md): 55-byte single-block messages m(g, z) =
BE32(W0) || ... || BE32(W12) || BE24(z), where W0..W12 are the group's 13 uniform
32-bit prefix words and z is a 24-bit index. Padding puts W13 = (z << 8) | 0x80,
W14 = 0, W15 = 440.

Evaluation: 256 lanes = 256 groups per batch; bit j of every 256-bit plane word belongs
to lane j. The group-constant part of the circuit (everything independent of z) runs
once per batch (function G); the per-z-step part (function F) reads the 24 z planes,
each 0 or all-ones, and produces the 160 key planes: digest words c, d, f, g, h
(digest bytes 8..15 and 20..31), which are fixed before the last round, so round R-1
is skipped and round R-2 computes only e. The circuit is compiled symbolically with
constant folding and polarity flags (XOR with a constant and NOT are flag flips;
AND/OR of equal polarity is one gate; mixed polarity materialises one NOT), a
polarity-aware full adder, Ch and Maj, and a lazily expanded message schedule.

  r-bs-fullwidth-equivalence  (12-bit mask)
      One batch of 256 seeded groups and one seeded z-step. Four lanes' key words are
      checked against the embedded scalar reference (the program aborts on a mismatch).
      Returns two lanes whose key words agree on the low 12 bits of digest word h.
      A mechanical cross-check only.

  r-bs-full-width / r-bs-spread / r-bs-single-group / r-bs-high-z  (18-bit mask)
      The grouped search at scale: N_t = 512 messages per trial, arranged as
      256 groups x 2 z / 16 x 32 / 1 x 512 / 4 x 128 (z = v << 17), with an 18-bit
      scaled key: the low 18 bits of digest word h. Messages are processed in the
      algorithm's order (batch-major, z-step, lane within the step). The scaled table is
      a dict keyed by the 18-bit key, so the slot IS the key: the "different key in the
      same slot" discard case of the full-width sparse set cannot arise here. The first
      match of two distinct messages ends the trial; a trial without a match returns null.
      Several trials share one 256-lane batch, each owning its own lanes; bitwise
      operations never mix lanes, so each trial depends only on its own seed.

Every returned pair is re-checked with the embedded scalar reference before output.
Numeric observations are untrusted; the program makes no cost claim.
"""
import json
import random
import re
import sys

M = (1 << 256) - 1
M32 = 0xffffffff
K = (
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
)
IV = (0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19)
KEY_WORDS = (2, 3, 5, 6, 7)      # digest words c, d, f, g, h
KEY_PLANES = 160


# ---------------------------------------------------------------- scalar reference
def _rotr(v, n):
    return ((v >> n) | (v << (32 - n))) & M32


def scalar_digest(msg, rounds):
    """Reduced-round SHA-256 of a byte string: the first `rounds` rounds of every block,
    standard IV, schedule and constants, feed-forward, big-endian digest."""
    padded = msg + b"\x80" + bytes((55 - len(msg)) % 64) + (8 * len(msg)).to_bytes(8, "big")
    h = list(IV)
    for off in range(0, len(padded), 64):
        w = [int.from_bytes(padded[off + 4 * i:off + 4 * i + 4], "big") for i in range(16)]
        for t in range(16, rounds):
            s0 = _rotr(w[t - 15], 7) ^ _rotr(w[t - 15], 18) ^ (w[t - 15] >> 3)
            s1 = _rotr(w[t - 2], 17) ^ _rotr(w[t - 2], 19) ^ (w[t - 2] >> 10)
            w.append((w[t - 16] + s0 + w[t - 7] + s1) & M32)
        a, b, c, d, e, f, g, hh = h
        for t in range(rounds):
            S1 = _rotr(e, 6) ^ _rotr(e, 11) ^ _rotr(e, 25)
            ch = (e & f) ^ (~e & g & M32)
            t1 = (hh + S1 + ch + K[t] + w[t]) & M32
            S0 = _rotr(a, 2) ^ _rotr(a, 13) ^ _rotr(a, 22)
            mj = (a & b) ^ (a & c) ^ (b & c)
            t2 = (S0 + mj) & M32
            hh, g, f, e, d, c, b, a = g, f, e, (d + t1) & M32, c, b, a, (t1 + t2) & M32
        h = [(x + y) & M32 for x, y in zip(h, (a, b, c, d, e, f, g, hh))]
    return b"".join(x.to_bytes(4, "big") for x in h)


def message(prefix, z):
    """55-byte message of a group prefix (13 words) and a 24-bit index z."""
    return b"".join(w.to_bytes(4, "big") for w in prefix) + z.to_bytes(3, "big")


# ---------------------------------------------------------------- symbolic compiler
RANK = {"c": 0, "g": 1, "v": 2}


class Compiler:
    """Compiles the bit-sliced circuit into two straight-line Python functions.

    A signal is ("c", bit) for a public constant plane, or (kind, name, flag) with kind
    "g" (group constant: independent of z, computed once per batch by G) or "v"
    (per-step, computed by F); the stored plane word is the true plane XOR
    (flag ? all-ones : 0). Gates with a "v" result go to F, the rest to G.
    """

    def __init__(self):
        self.lines = {"g": [], "v": []}
        self.ops = {k: {"xor": 0, "and": 0, "or": 0, "not": 0} for k in ("g", "v")}
        self.n = 0

    def tmp(self):
        self.n += 1
        return "t%d" % self.n

    @staticmethod
    def const(b):
        return ("c", 1 if b else 0)

    @staticmethod
    def kind(a, b):
        return "v" if RANK[a[0]] == 2 or RANK[b[0]] == 2 else "g"

    @staticmethod
    def flag(a):
        return a[2] if a[0] != "c" else None

    def emit(self, k, op, text):
        t = self.tmp()
        self.lines[k].append("%s=%s" % (t, text))
        self.ops[k][op] += 1
        return t

    def xor(self, a, b):
        if a[0] == "c" and b[0] == "c":
            return ("c", a[1] ^ b[1])
        if a[0] == "c":
            a, b = b, a
        if b[0] == "c":
            return (a[0], a[1], a[2] ^ b[1])
        k = self.kind(a, b)
        return (k, self.emit(k, "xor", "%s^%s" % (a[1], b[1])), a[2] ^ b[2])

    def neg(self, a):
        return ("c", 1 - a[1]) if a[0] == "c" else (a[0], a[1], a[2] ^ 1)

    def band(self, a, b):
        if a[0] == "c" and b[0] == "c":
            return ("c", a[1] & b[1])
        if a[0] == "c":
            a, b = b, a
        if b[0] == "c":
            return a if b[1] else ("c", 0)
        k = self.kind(a, b)
        if a[2] == 0 and b[2] == 0:
            return (k, self.emit(k, "and", "%s&%s" % (a[1], b[1])), 0)
        if a[2] == 1 and b[2] == 1:
            return (k, self.emit(k, "or", "%s|%s" % (a[1], b[1])), 1)
        if a[2] == 1:
            a, b = b, a
        self.ops[k]["not"] += 1
        return (k, self.emit(k, "and", "%s&(%s^M)" % (a[1], b[1])), 0)

    def bor(self, a, b):
        return self.neg(self.band(self.neg(a), self.neg(b)))

    def full_adder(self, x, y, c):
        ops = [x, y, c]
        fl = [self.flag(o) for o in ops]
        if any(f is None for f in fl):
            p = self.xor(x, y)
            return self.xor(p, c), self.bor(self.band(x, y), self.band(p, c))
        for i in range(3):
            j, k = (i + 1) % 3, (i + 2) % 3
            if fl[j] == fl[k]:
                x, y, c = ops[i], ops[j], ops[k]
                break
        p = self.xor(y, c)
        s = self.xor(x, p)
        if self.flag(x) == self.flag(y):
            return s, self.bor(self.band(y, c), self.band(p, x))
        return s, self.xor(self.bor(y, c), self.band(p, self.neg(x)))

    def add(self, x, y):
        out = [None] * 32
        c = self.const(0)
        for i in range(32):
            xi, yi = x[i], y[i]
            if xi[0] == "c" and yi[0] != "c":
                xi, yi = yi, xi
            if yi[0] == "c":
                if yi[1]:
                    out[i] = self.xor(self.neg(xi), c)
                    if i < 31:
                        c = self.bor(xi, c)
                else:
                    out[i] = self.xor(xi, c)
                    if i < 31:
                        c = self.band(xi, c)
            elif i < 31:
                out[i], c = self.full_adder(xi, yi, c)
            else:
                out[i] = self.xor(self.xor(xi, yi), c)
        return out

    @staticmethod
    def rotr(x, n):
        return [x[(i + n) % 32] for i in range(32)]

    def shr(self, x, n):
        return [x[i + n] if i + n < 32 else self.const(0) for i in range(32)]

    def xor3(self, a, b, c):
        return [self.xor(self.xor(a[i], b[i]), c[i]) for i in range(32)]

    def S0(self, x):
        return self.xor3(self.rotr(x, 2), self.rotr(x, 13), self.rotr(x, 22))

    def S1(self, x):
        return self.xor3(self.rotr(x, 6), self.rotr(x, 11), self.rotr(x, 25))

    def s0(self, x):
        return self.xor3(self.rotr(x, 7), self.rotr(x, 18), self.shr(x, 3))

    def s1(self, x):
        return self.xor3(self.rotr(x, 17), self.rotr(x, 19), self.shr(x, 10))

    def ch(self, e, f, g):
        out = []
        for i in range(32):
            p = self.xor(f[i], g[i])
            fe, fp = self.flag(e[i]), self.flag(p)
            if fe is None or fp is None or fe == fp:
                out.append(self.xor(g[i], self.band(e[i], p)))
            else:
                out.append(self.xor(f[i], self.band(self.neg(e[i]), p)))
        return out

    def maj(self, a, b, c, bc=None):
        res, ab = [], []
        for i in range(32):
            fa, fb, fc = self.flag(a[i]), self.flag(b[i]), self.flag(c[i])
            abi = self.xor(a[i], b[i])
            ab.append(abi)
            if None in (fa, fb, fc) or fa == fc:
                bci = bc[i] if bc is not None else self.xor(b[i], c[i])
                res.append(self.xor(b[i], self.band(abi, bci)))
            elif fb == fc:
                res.append(self.xor(a[i], self.band(abi, self.xor(a[i], c[i]))))
            else:
                bci = bc[i] if bc is not None else self.xor(b[i], c[i])
                res.append(self.xor(c[i], self.band(self.xor(a[i], c[i]), bci)))
        return res, ab

    def constw(self, val):
        return [self.const((val >> i) & 1) for i in range(32)]


def compile_circuit(rounds):
    """Returns (G, F, ops, fixups). G(P) maps the 416 prefix planes (P[32*w + i] = bit i
    of W_w) to the group-constant words F needs; F(gl, Z) maps those and the 24 z planes
    (Z[i] = bit 8+i of W13) to the 160 key planes (word c bits 0..31, then d, f, g, h)."""
    cp = Compiler()
    W = [[("g", "P[%d]" % (32 * w + i), 0) for i in range(32)] for w in range(13)]
    W13 = [cp.const((0x80 >> i) & 1) if i < 8 else ("v", "Z[%d]" % (i - 8), 0) for i in range(32)]
    W += [W13, cp.constw(0), cp.constw(440)]

    def sched(t):
        while len(W) <= t:
            u = len(W)
            W.append(cp.add(cp.add(cp.s1(W[u - 2]), W[u - 7]), cp.add(cp.s0(W[u - 15]), W[u - 16])))
        return W[t]

    a, b, c, d, e, f, g, h = [cp.constw(v) for v in IV]
    bc = None
    for t in range(rounds - 1):
        kw = cp.add(sched(t), cp.constw(K[t]))
        t1 = cp.add(cp.add(cp.add(h, cp.S1(e)), cp.ch(e, f, g)), kw)
        if t == rounds - 2:
            h, g, f, e = g, f, e, cp.add(d, t1)
            break
        mj, ab = cp.maj(a, b, c, bc)
        t2 = cp.add(cp.S0(a), mj)
        h, g, f, e = g, f, e, cp.add(d, t1)
        d, c, b, a = c, b, a, cp.add(t1, t2)
        bc = ab
    # digest words after R rounds in terms of the state after round R-2 plus e_{R-1}:
    # c_R = a, d_R = b, f_R = e, g_R = f, h_R = g
    key = []
    for x, v in zip((a, b, e, f, g), (IV[2], IV[3], IV[5], IV[6], IV[7])):
        key.extend(cp.add(x, cp.constw(v)))
    res, fixups = [], 0
    for s in key:
        if s[0] == "c":
            res.append("M" if s[1] else "0")
        elif s[2]:
            res.append("(%s^M)" % s[1])
            fixups += 1
        else:
            res.append(s[1])
    # Straight-line code over one value array v (slots: P[k] -> k, Z[i] -> 416 + i,
    # t-names -> 440 + ...), compiled in chunks of 1,500 statements so that the
    # organizer's 128 MiB container never holds one huge function body.
    slot = {}
    for k in range(416):
        slot["P[%d]" % k] = k
    for i in range(24):
        slot["Z[%d]" % i] = 416 + i
    tok = re.compile(r"t\d+|P\[\d+\]|Z\[\d+\]")

    def sub(txt):
        return tok.sub(lambda m: "v[%d]" % slot[m.group(0)], txt)

    def chunked(lines, tag):
        funcs = []
        for c0 in range(0, len(lines), 1500):
            body = []
            for ln in lines[c0:c0 + 1500]:
                name, expr = ln.split("=", 1)
                if name not in slot:
                    slot[name] = len(slot)
                body.append("v[%d]=%s" % (slot[name], sub(expr)))
            src = "def C(v):\n " + "\n ".join(body) + "\n"
            env = {"M": M}
            exec(compile(src, "<%s-%d>" % (tag, c0), "exec"), env)
            funcs.append(env["C"])
        return funcs

    g_funcs = chunked(cp.lines["g"], "group-setup-r%d" % rounds)
    f_funcs = chunked(cp.lines["v"], "z-step-r%d" % rounds)
    out_src = "def OUT(v):\n return [" + ",".join(sub(r) for r in res) + "]\n"
    env = {"M": M}
    exec(compile(out_src, "<key-out-r%d>" % rounds, "exec"), env)
    OUT = env["OUT"]
    nslots = len(slot)

    def G(P):
        v = [0] * nslots
        v[0:416] = P
        for fn in g_funcs:
            fn(v)
        return v

    def F(v, Z):
        v[416:440] = Z
        for fn in f_funcs:
            fn(v)
        return OUT(v)

    return G, F, cp.ops, fixups


# ---------------------------------------------------------------- lane helpers
def prefix_planes(prefixes):
    """416 plane words from up to 256 prefixes (lane j = prefixes[j]); missing lanes zero."""
    planes = [0] * 416
    for j, pref in enumerate(prefixes):
        bit = 1 << j
        for w in range(13):
            v = pref[w]
            base = 32 * w
            for i in range(32):
                if (v >> i) & 1:
                    planes[base + i] |= bit
    return planes


def z_planes(z):
    return [M if (z >> i) & 1 else 0 for i in range(24)]


def lane_values(planes):
    """256 integers: value j has bit i = bit j of planes[i] (string transpose)."""
    rows = [format(p, "0256b") for p in reversed(planes)]
    cols = zip(*rows)
    vals = [int("".join(col), 2) for col in cols]
    vals.reverse()
    return vals


def key_words(planes160, j):
    """The five key digest words of lane j from the 160 key planes."""
    out = []
    for w in range(5):
        v = 0
        for i in range(32):
            v |= ((planes160[32 * w + i] >> j) & 1) << i
        out.append(v)
    return out


def masked_h(digest, bits):
    return int.from_bytes(digest[28:32], "big") & ((1 << bits) - 1)


# ---------------------------------------------------------------- experiments
def equivalence_trial(G, F, rng, rounds, obs):
    prefixes = [[rng.getrandbits(32) for _ in range(13)] for _ in range(256)]
    z = rng.getrandbits(24)
    key = F(G(prefix_planes(prefixes)), z_planes(z))
    for j in (0, 85, 170, 255):
        ref = scalar_digest(message(prefixes[j], z), rounds)
        want = [int.from_bytes(ref[4 * w:4 * w + 4], "big") for w in KEY_WORDS]
        if key_words(key, j) != want:
            sys.stderr.write("bit-sliced key words differ from the scalar reference\n")
            sys.exit(1)
    obs["checked_lanes"] = 4
    vals = lane_values(key[128:140])          # low 12 bits of digest word h
    seen = {}
    for j in range(256):
        if vals[j] in seen:
            return message(prefixes[seen[vals[j]]], z), message(prefixes[j], z)
        seen[vals[j]] = j
    return None


LAYOUTS = {
    "r-bs-full-width": (256, [0, 1]),
    "r-bs-spread": (16, list(range(32))),
    "r-bs-single-group": (1, list(range(512))),
    "r-bs-high-z": (4, [v << 17 for v in range(128)]),
}


def search_batch(G, F, rounds, trials, groups, zs, obs_list):
    """Run one batch: trials[k] owns lanes k*groups .. (k+1)*groups-1. Returns pairs."""
    per = 256 // groups
    assert len(trials) <= per
    prefixes, owner = [], []
    for k, (tid, rng) in enumerate(trials):
        for _ in range(groups):
            prefixes.append([rng.getrandbits(32) for _ in range(13)])
            owner.append(k)
    gl = G(prefix_planes(prefixes))
    tables = [dict() for _ in trials]
    result = [None] * len(trials)
    done = 0
    steps = 0
    for z in zs:
        if done == len(trials):
            break
        steps += 1
        key = F(gl, z_planes(z))
        vals = lane_values(key[128:146])       # low 18 bits of digest word h
        for j in range(len(prefixes)):
            k = owner[j]
            if result[k] is not None:
                continue
            kv = vals[j]
            tab = tables[k]
            if kv in tab:
                j0, z0 = tab[kv]
                ma, mb = message(prefixes[j0], z0), message(prefixes[j], z)
                if ma == mb:
                    continue
                result[k] = (ma, mb)
                done += 1
            else:
                tab[kv] = (j, z)
    for k in range(len(trials)):
        obs_list[k]["steps"] = steps
        obs_list[k]["inserted"] = len(tables[k])
    return result


def main():
    req = json.loads(sys.stdin.read())
    rounds = {"sha256-r38-prefix-v1": 38, "sha256-r37-prefix-v1": 37}[req["target_profile"]]
    G, F, ops, fixups = compile_circuit(rounds)
    exp = req["experiment_id"]
    base_obs = {"rounds": rounds,
                "step_xor": ops["v"]["xor"], "step_and": ops["v"]["and"],
                "step_or": ops["v"]["or"], "step_not": ops["v"]["not"],
                "step_gates": sum(ops["v"].values()),
                "group_gates": sum(ops["g"].values()), "fixup_planes": fixups}
    rows = [None] * len(req["trials"])
    obs_all = [dict(base_obs) for _ in req["trials"]]
    pairs = [None] * len(req["trials"])
    mask_bits = 18
    if exp == "r-bs-fullwidth-equivalence":
        mask_bits = 12
        for n, t in enumerate(req["trials"]):
            rng = random.Random(int(t["seed"], 16))
            pairs[n] = equivalence_trial(G, F, rng, rounds, obs_all[n])
    else:
        groups, zs = LAYOUTS[exp]
        per = 256 // groups
        idx = list(range(len(req["trials"])))
        for start in range(0, len(idx), per):
            chunk = idx[start:start + per]
            trials = [(n, random.Random(int(req["trials"][n]["seed"], 16))) for n in chunk]
            res = search_batch(G, F, rounds, trials, groups, zs, [obs_all[n] for n in chunk])
            for k, n in enumerate(chunk):
                pairs[n] = res[k]
    mask = (1 << mask_bits) - 1
    for n, t in enumerate(req["trials"]):
        pair = pairs[n]
        if pair is None:
            ma = mb = None
        else:
            da, db = scalar_digest(pair[0], rounds), scalar_digest(pair[1], rounds)
            if pair[0] == pair[1] or (masked_h(da, 32) ^ masked_h(db, 32)) & mask:
                sys.stderr.write("returned pair fails the scalar re-check\n")
                sys.exit(1)
            ma, mb = pair[0].hex(), pair[1].hex()
        rows[n] = {"trial": t["trial"], "message_a_hex": ma, "message_b_hex": mb,
                   "observations": obs_all[n]}
    sys.stdout.write(json.dumps({"schema_version": 1, "trials": rows}, sort_keys=True,
                                separators=(",", ":")))


if __name__ == "__main__":
    main()
