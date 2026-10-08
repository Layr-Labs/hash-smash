"""Self-contained replay/experiment for sha256-r38 generic collision baseline (python-message-pairs-v1).

Run by the organizer's isolated executor: reads one organizer request JSON from stdin and writes one
strict JSON document to stdout with exactly the requested trials.  For each trial it draws uniform
55-byte single-block messages from the organizer seed, computes the reduced 38-round SHA-256 digest with
a self-contained reference, and returns a distinct pair whose digests agree on the organizer's low-14-bit
mask.  The organizer re-hashes every returned pair with its own trusted reduced-round digest, so a wrong
reference here cannot produce an accepted pair.  Trial 0 also runs the counted 7-lane 36-bit-guard SWAR
batch lane-by-lane against the same reference and against the exact charged operation counts, reporting the
outcome as untrusted observations (the organizer trusts only the re-hashed pairs, never these numbers).

Scope: a scaled kernel-and-method demonstration.  It verifies the SWAR evaluator equals the reference core
and that masked collisions of the stated single-block family exist under the exact reduced hash.  It does
not execute the full search, establish the full-scale birthday law, the uninitialised-table tail, or any
resource bound.
"""
from __future__ import annotations

import hashlib
import json
import struct
import sys

R = 38
MASK32 = 0xFFFFFFFF
M_256 = (1 << 256) - 1
LANES7, LANE_BITS7 = 7, 36
M_32x7 = sum(MASK32 << (LANE_BITS7 * l) for l in range(LANES7))
EXPECTED_BATCH_OPS = 2879
EXPECTED_SECTIONS = {'rand_and_mask': 32, 'rounds': 1815, 'schedule': 638, 'feedforward': 16, 'extract': 112}
EXPECTED_PEAK_LIVE = 53

IV = (0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19)
K = (
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
)


def require(cond, msg):
    if not cond:
        raise AssertionError(msg)


def ror(v, r):
    return ((v >> r) | (v << (32 - r))) & MASK32


def big_sigma0(x): return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22)
def big_sigma1(x): return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25)
def small_sigma0(x): return ror(x, 7) ^ ror(x, 18) ^ (x >> 3)
def small_sigma1(x): return ror(x, 17) ^ ror(x, 19) ^ (x >> 10)
def choose(x, y, z): return (x & y) ^ (~x & z)
def majority(x, y, z): return (x & y) ^ (x & z) ^ (y & z)


def compress_state_R(words16, rounds):
    """Working state (a..h), no feed-forward, after `rounds` rounds of one block from the standard IV."""
    w = list(words16)
    for t in range(16, rounds):
        w.append((small_sigma1(w[t - 2]) + w[t - 7] + small_sigma0(w[t - 15]) + w[t - 16]) & MASK32)
    a, b, c, d, e, f, g, h = IV
    for t in range(rounds):
        t1 = (h + big_sigma1(e) + choose(e, f, g) + K[t] + w[t]) & MASK32
        t2 = (big_sigma0(a) + majority(a, b, c)) & MASK32
        a, b, c, d, e, f, g, h = (t1 + t2) & MASK32, a, b, c, (d + t1) & MASK32, e, f, g
    return (a, b, c, d, e, f, g, h)


def cv_block1(words16, rounds):
    st = compress_state_R(words16, rounds)
    return tuple((IV[j] + st[j]) & MASK32 for j in range(8))


def digest_single_block(msg55, rounds):
    """Reference reduced 38-round digest of a 55-byte single-block message (FIPS padding, feed-forward)."""
    require(len(msg55) == 55, "message must be 55 bytes")
    padded = msg55 + b"\x80" + bytes((55 - 55) % 64) + (8 * 55).to_bytes(8, "big")
    require(len(padded) == 64, "single padded block")
    words = list(struct.unpack(">16I", padded))
    cv = cv_block1(words, rounds)
    return b"".join(x.to_bytes(4, "big") for x in cv)


# --- counted 7-lane SWAR batch (promoted r32 verify_reg64_batch, round loop to R, full CV extract) ---------
def replicate7(word):
    return sum((word & MASK32) << (LANE_BITS7 * l) for l in range(LANES7))


def lane_lo(r): return replicate7((1 << (32 - r)) - 1)
def lane_hi(r): return replicate7(((1 << r) - 1) << (32 - r))


IV7 = [replicate7(w) for w in IV]
K7 = [replicate7(w) for w in K]


class Reg64:
    def __init__(self):
        self.ops = {"arith": 0, "load": 0, "store": 0, "addr": 0}
        self.section = "rand_and_mask"
        self.sections = {}
        self.max_sum = 0
        self.t = 0
        self.val = []
        self.born = []
        self.last = []

    def _def(self, value, *srcs):
        self.t += 1
        for v in srcs:
            self.last[v] = self.t
        self.val.append(value & M_256)
        self.born.append(self.t)
        self.last.append(self.t)
        return len(self.val) - 1

    def _arith(self, value, *srcs):
        self.ops["arith"] += 1
        self.sections[self.section] = self.sections.get(self.section, 0) + 1
        return self._def(value, *srcs)

    def rand(self, raw): return self._arith(raw)

    def load(self, value):
        self.ops["load"] += 1
        self.ops["addr"] += 1
        return self._def(value)

    def store(self, v):
        self.ops["store"] += 1
        self.ops["addr"] += 1
        self.t += 1
        self.last[v] = self.t

    def add(self, a, b):
        x, y = self.val[a], self.val[b]
        out = self._arith(x + y, a, b)
        lane = (1 << LANE_BITS7) - 1
        for l in range(LANES7):
            s = ((x >> (LANE_BITS7 * l)) & lane) + ((y >> (LANE_BITS7 * l)) & lane)
            require(s == (self.val[out] >> (LANE_BITS7 * l)) & lane, "lane carry")
            self.max_sum = max(self.max_sum, s)
        return out

    def xor(self, a, b): return self._arith(self.val[a] ^ self.val[b], a, b)
    def band(self, a, b): return self._arith(self.val[a] & self.val[b], a, b)
    def shr(self, a, k): return self._arith(self.val[a] >> k, a)
    def shl(self, a, k): return self._arith(self.val[a] << k, a)

    def peak_live(self):
        delta = [0] * (self.t + 2)
        for b, l in zip(self.born, self.last):
            delta[b] += 1
            delta[l + 1] -= 1
        live = peak = 0
        for d in delta:
            live += d
            peak = max(peak, live)
        return peak


REG64_PERSISTENT = 8


def merged_mask_ok(terms, lo, hi):
    keep = range(lo, hi + 1)
    for kind, r in terms:
        good, zero = (range(0, 32 - r), range(32 - r, 36 - r)) if kind == "R" else (range(32 - r, 32), range(28 - r, 32 - r))
        require(set(good) <= set(keep), "merged mask drops a correct bit")
        require(all(p in good or p in zero for p in keep), "merged mask keeps a wrong bit")


def verify_reg64_batch(raw_words, scalar_cvs7):
    g = Reg64()
    mask = {"M": g.load(M_32x7)}
    for r in (2, 13, 22, 6, 11, 25):
        mask[f"LO{r}"], mask[f"HI{r}"] = g.load(lane_lo(r)), g.load(lane_hi(r))
    for name, value in (("LO17", lane_lo(17)), ("HI19", lane_hi(19)), ("LO10", lane_lo(10)), ("LO3", lane_lo(3)),
                        ("HI7", lane_hi(7)), ("LO18", lane_lo(18)), ("HI18", lane_hi(18))):
        mask[name] = g.load(value)
    M = mask["M"]

    def rot(x, r):
        return g.xor(g.band(g.shr(x, r), mask[f"LO{r}"]), g.band(g.shl(x, 32 - r), mask[f"HI{r}"]))

    def big0(x): return g.xor(g.xor(rot(x, 2), rot(x, 13)), rot(x, 22))
    def big1(x): return g.xor(g.xor(rot(x, 6), rot(x, 11)), rot(x, 25))

    def small1(x):
        right = g.band(g.xor(g.shr(x, 17), g.shr(x, 19)), mask["LO17"])
        left = g.band(g.xor(g.shl(x, 15), g.shl(x, 13)), mask["HI19"])
        return g.xor(g.xor(right, left), g.band(g.shr(x, 10), mask["LO10"]))

    def small0(x):
        a = g.band(g.xor(g.shr(x, 3), g.shr(x, 7)), mask["LO3"])
        b = g.band(g.shl(x, 25), mask["HI7"])
        c = g.band(g.shr(x, 18), mask["LO18"])
        d = g.band(g.shl(x, 14), mask["HI18"])
        return g.xor(g.xor(g.xor(a, b), c), d)

    a0, b0, c0, d0, e0, f0, g0, h0 = IV
    w = {}
    g.section = "rand_and_mask"
    for i in range(16):
        w[i] = g.band(g.rand(raw_words[i]), M)

    def word(i):
        if i >= 16 and i not in w:
            g.section = "schedule"
            t = g.add(g.add(g.add(small1(w[i - 2]), w[i - 7]), small0(w[i - 15])), w[i - 16])
            w[i] = g.band(t, M)
            g.section = "rounds"
        return w[i]

    g.section = "rounds"
    t1 = g.add(g.load(replicate7(h0 + big_sigma1(e0) + choose(e0, f0, g0) + K[0])), word(0))
    e_n = g.band(g.add(g.load(replicate7(d0)), t1), M)
    a_n = g.band(g.add(t1, g.load(replicate7(big_sigma0(a0) + majority(a0, b0, c0)))), M)
    sa, se = a_n, e_n
    S1 = big1(se)
    ch = g.xor(g.load(replicate7(f0)), g.band(se, g.load(replicate7(e0 ^ f0))))
    S0 = big0(sa)
    mj = g.xor(g.band(sa, g.load(replicate7(a0 ^ b0))), g.load(replicate7(a0 & b0)))
    t1 = g.add(g.add(g.add(g.load(replicate7(g0 + K[1])), S1), ch), word(1))
    e_n = g.band(g.add(g.load(replicate7(c0)), t1), M)
    a_n = g.band(g.add(g.add(t1, S0), mj), M)
    A0, B0, E0 = g.load(replicate7(a0)), g.load(replicate7(b0)), g.load(replicate7(e0))
    sa, sb, sc, sd, se, sf, sg = a_n, sa, A0, B0, e_n, se, E0
    S1 = big1(se)
    ch = g.xor(sg, g.band(se, g.xor(sf, sg)))
    S0 = big0(sa)
    xab = g.xor(sa, sb)
    mj = g.xor(sb, g.band(xab, g.xor(sb, sc)))
    t1 = g.add(g.add(g.add(g.load(replicate7(f0 + K[2])), S1), ch), word(2))
    e_n = g.band(g.add(sd, t1), M)
    a_n = g.band(g.add(g.add(t1, S0), mj), M)
    prev_ab = xab
    sa, sb, sc, sd, se, sf, sg, sh = a_n, sa, sb, sc, e_n, se, sf, sg
    for i in range(3, R):
        S1 = big1(se)
        ch = g.xor(sg, g.band(se, g.xor(sf, sg)))
        S0 = big0(sa)
        xab = g.xor(sa, sb)
        mj = g.xor(sb, g.band(xab, prev_ab))
        t1 = g.add(g.add(g.add(g.add(sh, S1), ch), g.load(K7[i])), word(i))
        e_n = g.band(g.add(sd, t1), M)
        a_n = g.band(g.add(g.add(t1, S0), mj), M)
        prev_ab = xab
        sa, sb, sc, sd, se, sf, sg, sh = a_n, sa, sb, sc, e_n, se, sf, sg
    g.section = "feedforward"
    state = (sa, sb, sc, sd, se, sf, sg, sh)
    out = [g.band(g.add(g.load(IV7[j]), state[j]), M) for j in range(8)]
    g.section = "extract"
    m32 = g.load(MASK32)
    cv_lanes = [[None] * 8 for _ in range(LANES7)]
    for j in range(8):
        for l in range(LANES7):
            x = g.band(g.shr(out[j], LANE_BITS7 * l), m32)
            g.store(x)
            cv_lanes[l][j] = g.val[x]
    for l in range(LANES7):
        require(tuple(cv_lanes[l]) == scalar_cvs7[l], "SWAR CV lane mismatch vs reference")
    require(g.peak_live() + REG64_PERSISTENT <= 64, "liveness exceeds 64 registers")
    require(g.max_sum < (1 << LANE_BITS7), "lane sum reached 2^36")
    return {"ops": dict(g.ops), "sections": dict(g.sections), "peak_live": g.peak_live(),
            "total": sum(g.ops.values())}


def swar_self_check(seed_hex, batches):
    """Run the counted SWAR batch against the reference on seeded random inputs; assert lanes and counts."""
    merged_mask_ok([("R", 17), ("R", 19)], 0, 14)
    merged_mask_ok([("L", 17), ("L", 19)], 13, 31)
    merged_mask_ok([("R", 3), ("R", 7)], 0, 28)
    total = None
    for b in range(batches):
        stream = hashlib.shake_256((seed_hex + f"swar{b}").encode()).digest(16 * LANES7 * 4)
        scal = []
        for l in range(LANES7):
            words = [int.from_bytes(stream[(l * 16 + i) * 4:(l * 16 + i) * 4 + 4], "big") for i in range(16)]
            scal.append(cv_block1(words, R))
        raw = []
        for i in range(16):
            packed = 0
            for l in range(LANES7):
                wi = int.from_bytes(stream[(l * 16 + i) * 4:(l * 16 + i) * 4 + 4], "big")
                packed |= wi << (LANE_BITS7 * l)
            raw.append(packed)
        res = verify_reg64_batch(raw, scal)
        require(res["total"] == EXPECTED_BATCH_OPS, f"batch op count {res['total']} != {EXPECTED_BATCH_OPS}")
        require(res["sections"] == EXPECTED_SECTIONS, f"section counts {res['sections']} != expected")
        require(res["peak_live"] == EXPECTED_PEAK_LIVE, f"peak live {res['peak_live']} != {EXPECTED_PEAK_LIVE}")
        total = res
    return total


def main():
    request = json.load(sys.stdin)
    event = request["event"]
    mask = int(event["mask_hex"], 16)
    expected = int(event["expected_hex"], 16)
    trials = request["trials"]
    messages_per_trial = 512
    out_trials = []
    swar_obs = None
    for entry in trials:
        idx = entry["trial"]
        seed = entry["seed"]
        if idx == 0:
            try:
                res = swar_self_check(seed, 16)
                swar_obs = {"swar_lane_match": 1, "swar_total_ops": res["total"],
                            "swar_peak_live": res["peak_live"], "swar_rounds": R}
            except AssertionError:
                swar_obs = {"swar_lane_match": 0, "swar_total_ops": 0, "swar_peak_live": 0, "swar_rounds": R}
        stream = hashlib.shake_256(("msg" + seed).encode()).digest(55 * messages_per_trial)
        seen = {}
        a_hex = b_hex = None
        for m in range(messages_per_trial):
            msg = stream[m * 55:(m + 1) * 55]
            d = digest_single_block(msg, R)
            key = (int.from_bytes(d, "big") ^ expected) & mask
            if key in seen and seen[key] != msg:
                a_hex, b_hex = seen[key].hex(), msg.hex()
                break
            seen.setdefault(key, msg)
        row = {"trial": idx, "message_a_hex": a_hex, "message_b_hex": b_hex}
        if idx == 0 and swar_obs is not None:
            row["observations"] = swar_obs
        out_trials.append(row)
    sys.stdout.write(json.dumps({"schema_version": 1, "trials": out_trials},
                                separators=(",", ":"), sort_keys=True))


if __name__ == "__main__":
    main()
