"""Self-contained replay/experiments for the sha256-r37 grouped round-skip birthday package (v1b).

Message family: with two coins drawn once per run, a 36-byte prefix P and a 128-bit offset R0, m(g, t) is
    bytes 0..35 = P,   bytes 36..51 = BE128(g XOR R0),   bytes 52..54 = BE24(t),
so W0..W8 = P, W9..W12 = g XOR R0, W13 = (t << 8) | 0x80, W14 = 0, W15 = 440 after FIPS padding (one block).
Group g = 7k + l is lane l of group batch k; the table index n = (k << 27) | (t << 3) | l decodes to (g, t),
so any index regenerates its message from P and R0.

Run by the organizer's isolated executor (python-message-pairs-v1).  Both experiments run a scaled copy of
the package's algorithm on this exact family and reduced hash: the "digest" is the declared 16-bit mask of the
reduced 37-round digest, the key is a fixed subset of those bits taken from digest words d, c, h, g (the
round-skip key words), the table is never initialised (unwritten slots return seeded garbage), a table word is
a 6-bit TAG and a 9-bit index, a TAG match runs the cold verification (regenerate the stored message from its
index, recompute, compare), and a deterministic cap halts the run.  Each trial processes one scaled group batch
of 7 consecutive groups x 52 consecutive counters (364 messages).
  h1-success   (11-bit key): returns the confirmed pair if the algorithm succeeds.
  h1-overwrite ( 8-bit key): returns an existing masked collision that the algorithm missed, if any.
The organizer re-hashes every returned pair; the two trial counts are the trusted measurements.  Trial 0 of
h1-success also re-runs the counted full-scale v1 batch on 4 group batches of this family and aborts unless all
lanes equal the reference 144-bit keys and every count equals the charged ledger.
"""
from __future__ import annotations

import hashlib
import json
import struct
import sys

R = 37
MASK32 = 0xFFFFFFFF
M_256 = (1 << 256) - 1
LANES7, LANE_BITS7 = 7, 36
PERSIST = frozenset([8] + list(range(27, 43)))
EXPECTED = {'total': 1406, 'sections': {'rounds': 1092, 'schedule': 193, 'key': 62, 'table': 55, 'loop': 4}, 'ops': {'arith': 1326, 'load': 33, 'store': 7, 'addr': 40}, 'persistent': 44, 'peak_tmp': 20}

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


def digest_int(msg55, rounds):
    """Reference reduced digest of a 55-byte message (one padded block, feed-forward) as a 256-bit integer."""
    w = list(struct.unpack(">16I", msg55 + b"\x80" + b"\x00\x00\x00\x00\x00\x00\x01\xb8"))
    M = MASK32
    for t in range(16, rounds):
        x = w[t - 15]; y = w[t - 2]
        s0 = (((x >> 7) | (x << 25)) ^ ((x >> 18) | (x << 14)) ^ (x >> 3)) & M
        s1 = (((y >> 17) | (y << 15)) ^ ((y >> 19) | (y << 13)) ^ (y >> 10)) & M
        w.append((w[t - 16] + s0 + w[t - 7] + s1) & M)
    a, b, c, d, e, f, g, h = IV
    for t in range(rounds):
        S1 = (((e >> 6) | (e << 26)) ^ ((e >> 11) | (e << 21)) ^ ((e >> 25) | (e << 7))) & M
        t1 = (h + S1 + ((e & f) ^ (~e & g)) + K[t] + w[t]) & M
        S0 = (((a >> 2) | (a << 30)) ^ ((a >> 13) | (a << 19)) ^ ((a >> 22) | (a << 10))) & M
        t2 = (S0 + ((a & b) ^ (a & c) ^ (b & c))) & M
        h = g; g = f; f = e; e = (d + t1) & M; d = c; c = b; b = a; a = (t1 + t2) & M
    out = 0
    for iv, x in zip(IV, (a, b, c, d, e, f, g, h)):
        out = (out << 32) | ((iv + x) & M)
    return out


def family_message(g, t, P, R0):
    return P + ((g ^ R0) % (1 << 128)).to_bytes(16, "big") + (t & 0xFFFFFF).to_bytes(3, "big")


def family_words(g, t, P, R0):
    return list(struct.unpack(">13I", family_message(g, t, P, R0)[:52])) + [((t & 0xFFFFFF) << 8) | 0x80, 0, 0x1B8]


def run_coins(seed):
    """The run's two coins (prefix P, offset R0) from the organizer seed."""
    h = hashlib.sha256(("coins" + seed).encode()).digest() + hashlib.sha256(("coins2" + seed).encode()).digest()
    return h[:36], int.from_bytes(h[36:52], "big")


# ---- counted full-scale v1 batch (verbatim from the package builder) -----------------------------------------


LB = LANE_BITS7
LANE36 = (1 << LB) - 1


def pack(vals):
    return sum((v & ((1 << LB) - 1)) << (LB * l) for l, v in enumerate(vals))


def unpack(w):
    return [(w >> (LB * l)) & LANE36 for l in range(LANES7)]


def rep(v32):
    return pack([v32 & MASK32] * LANES7)


def lo(r): return rep((1 << (32 - r)) - 1)
def hi(r): return rep(((1 << r) - 1) << (32 - r))


G4 = pack([0xF << 32] * LANES7)
MEVEN = LANE36 | (LANE36 << 72) | (LANE36 << 144)    # 36-bit lanes 0, 2, 4
MODD = (LANE36 << 36) | (LANE36 << 108) | (LANE36 << 180)  # 36-bit lanes 1, 3, 5
M72_0 = (1 << 72) - 1                                # low 72 bits
M72_1 = ((1 << 72) - 1) << 72                        # bits 72..143
THRESH = 1 << 136          # (w XOR c) < 2^136: the 120-bit TAG field matches

# Because every input x to big_sigma0, big_sigma1, small0, small1 is guard-clean (x.bnd <= MASK32, so bits 32..35
# of every 36-bit lane are 0), bits [32-r .. 35-r] of (x >> r) are already 0.  Therefore any mask LO_{r0} with
# r - 4 <= r0 <= r clears bits [36-r .. 35] while leaving bits [0 .. 31-r] intact:
#   LO2 covers r in {2, 6}, LO3 covers r in {3, 7}, LO10 covers r in {10, 11, 13},
#   LO17 covers r in {17, 18}, LO22 covers r in {22, 25}.
LO_FOR_R = {2: "LO2", 6: "LO2", 11: "LO10", 13: "LO10", 22: "LO22", 25: "LO22"}

GLOBAL_MASKS = {"M": rep(MASK32)}
for _r in (2, 13, 22, 6, 11, 25):
    GLOBAL_MASKS[f"HI{_r}"] = hi(_r)
for _n, _v in (("LO2", lo(2)), ("LO3", lo(3)), ("LO10", lo(10)), ("LO17", lo(17)), ("LO22", lo(22)),
               ("HI19", hi(19)), ("HI7", hi(7)), ("HI18", hi(18))):
    GLOBAL_MASKS[_n] = _v
GLOBAL_MASKS["G4"] = G4
GLOBAL_MASKS["MEVEN"] = MEVEN
GLOBAL_MASKS["MODD"] = MODD
GLOBAL_MASKS["M72_0"] = M72_0
GLOBAL_MASKS["M72_1"] = M72_1
GLOBAL_MASKS["THRESH"] = THRESH


class V:
    __slots__ = ("idx", "val", "bnd", "const")

    def __init__(self, idx, val, bnd, const):
        self.idx, self.val, self.bnd, self.const = idx, val, bnd, const


class Prog:
    """Values are either group constants (no register until materialised) or SSA registers."""

    def __init__(self, persistent_consts=frozenset()):
        self.t = 0
        self.born, self.last, self.kind = [], [], []
        self.ops = {"arith": 0, "load": 0, "store": 0, "addr": 0}
        self.sec = "setup"
        self.sections = {}
        self.persist_keys = set(persistent_consts)
        self.mat = {}           # const key -> V register
        self.const_uses = {}
        self.persist_regs = {}  # name -> V (global masks and loop registers)
        for name, v in GLOBAL_MASKS.items():
            self.persist_regs[name] = self._reg(v, (1 << 256) - 1, "persist")
        # loop-carried and table registers: the counter word's increment and end value, the table word c,
        # and the constants 1 and 8 that step its low message-index field
        for name in ("INC", "END", "c", "ONE", "EIGHT"):
            self.persist_regs[name] = self._reg(0, (1 << 256) - 1, "persist")

    # registers -------------------------------------------------------------------------------------
    def _reg(self, val, bnd, kind):
        self.t += 1
        self.born.append(self.t)
        self.last.append(self.t)
        self.kind.append(kind)
        return V(len(self.born) - 1, val & M_256, bnd, None)

    def _use(self, *vs):
        for v in vs:
            if v.idx is not None:
                self.last[v.idx] = self.t + 1

    def _count(self, k="arith", n=1):
        self.ops[k] += n
        self.sections[self.sec] = self.sections.get(self.sec, 0) + n

    def mask(self, name):
        return self.persist_regs[name]

    def gconst(self, packed):
        """A group constant (per-lane values < 2^32), symbolic until used; its static bound is the worst case."""
        return V(None, packed, MASK32, packed)

    def input_reg(self, packed, bnd, kind="persist"):
        return self._reg(packed, bnd, kind)

    def materialise(self, v):
        """A group constant enters a register at its first use (structural identity, not value): a persistent
        register if its serial is in persist_keys, else a load (access + address) that stays live to last use."""
        if v.const is None:
            return v
        key = id(v)
        if key in self.mat:
            return self.mat[key][1]
        serial = len(self.mat)
        if serial in self.persist_keys:
            r = self._reg(v.const, v.bnd, "persist")
        else:
            self._count("load")
            self._count("addr")
            r = self._reg(v.const, v.bnd, "tmp")
        self.mat[key] = (v, r, serial)
        return r

    def _arith(self, val, bnd, *srcs):
        srcs = [self.materialise(s) for s in srcs]
        self._use(*srcs)
        self._count()
        require(bnd < (1 << 256), "bound")
        out = self._reg(val, bnd, "tmp")
        return out, srcs

    # lane arithmetic with static bounds ------------------------------------------------------------
    def add(self, a, b):
        if a.const is not None and b.const is not None:
            return self.gconst(pack([(x + y) & MASK32 for x, y in zip(unpack(a.const), unpack(b.const))]))
        bnd = a.bnd + b.bnd
        require(bnd < (1 << LB), f"static lane bound {bnd:#x} reaches 2^36")
        out, (x, y) = self._arith(0, bnd, a, b)
        out.val = (x.val + y.val) & M_256
        for l, (p, q, r) in enumerate(zip(unpack(x.val), unpack(y.val), unpack(out.val))):
            require(p + q == r, "lane carry leaked")
        return out

    def xor(self, a, b):
        if a.const is not None and b.const is not None:
            return self.gconst(a.const ^ b.const)
        out, (x, y) = self._arith(0, (1 << max(a.bnd, b.bnd).bit_length()) - 1, a, b)
        out.val = x.val ^ y.val
        return out

    def band(self, a, b):
        if a.const is not None and b.const is not None:
            return self.gconst(a.const & b.const)
        out, (x, y) = self._arith(0, min(a.bnd, b.bnd), a, b)
        out.val = x.val & y.val
        return out

    def bor(self, a, b):
        out, (x, y) = self._arith(0, (1 << max(a.bnd, b.bnd).bit_length()) - 1, a, b)
        out.val = x.val | y.val
        return out

    def andm(self, a, name):
        m = self.mask(name)
        out, (x, _) = self._arith(0, min(a.bnd, MASK32) if name == "M" else a.bnd, a, m)
        out.val = x.val & m.val
        if name == "M":
            out.bnd = MASK32
        return out

    def shr(self, a, k):
        out, (x,) = self._arith(0, (1 << 256) - 1, a)
        out.val = x.val >> k
        return out

    def shl(self, a, k):
        out, (x,) = self._arith(0, (1 << 256) - 1, a)
        out.val = (x.val << k) & M_256
        return out

    def clean(self, a):
        return a.bnd <= MASK32

    # sigma functions -----------------------------------------------------------------------------
    def big(self, x, rs, f):
        if x.const is not None:
            return self.gconst(pack([f(v) for v in unpack(x.const)]))
        require(self.clean(x), "shared-LO big_sigma needs zero guard bits")
        r0, r1, r2 = rs
        acc = self.xor(self.andm(self.shr(x, r0), LO_FOR_R[r0]), self.andm(self.shl(x, 32 - r0), f"HI{r0}"))
        acc = self.xor(acc, self.andm(self.shr(x, r1), LO_FOR_R[r1]))
        acc = self.xor(acc, self.andm(self.shl(x, 32 - r1), f"HI{r1}"))
        acc = self.xor(acc, self.andm(self.shr(x, r2), LO_FOR_R[r2]))
        out = self.xor(acc, self.andm(self.shl(x, 32 - r2), f"HI{r2}"))
        out.bnd = MASK32
        return out

    def small1(self, x):
        if x.const is not None:
            return self.gconst(pack([small_sigma1(v) for v in unpack(x.const)]))
        require(self.clean(x), "merged sigma1 needs zero guard bits")
        acc = self.andm(self.xor(self.shr(x, 17), self.shr(x, 19)), "LO17")
        acc = self.xor(acc, self.andm(self.xor(self.shl(x, 15), self.shl(x, 13)), "HI19"))
        out = self.xor(acc, self.andm(self.shr(x, 10), "LO10"))
        out.bnd = MASK32
        return out

    def small0(self, x):
        if x.const is not None:
            return self.gconst(pack([small_sigma0(v) for v in unpack(x.const)]))
        require(self.clean(x), "merged sigma0 needs zero guard bits")
        acc = self.andm(self.xor(self.shr(x, 3), self.shr(x, 7)), "LO3")
        acc = self.xor(acc, self.andm(self.shl(x, 25), "HI7"))
        acc = self.xor(acc, self.andm(self.shr(x, 18), "LO17"))
        out = self.xor(acc, self.andm(self.shl(x, 14), "HI18"))
        out.bnd = MASK32
        return out

    def sum(self, terms):
        cs = [t for t in terms if t.const is not None]
        vs = [t for t in terms if t.const is None]
        cst = None
        for t in cs:
            cst = t if cst is None else self.add(cst, t)
        if not vs:
            return cst
        acc = vs[0]
        for t in vs[1:]:
            acc = self.add(acc, t)
        if cst is not None:
            acc = self.add(acc, cst)
        return acc

    def peak(self, kinds=("tmp",)):
        delta = [0] * (self.t + 3)
        for b, l, k in zip(self.born, self.last, self.kind):
            if k in kinds:
                delta[b] += 1
                delta[l + 1] -= 1
        live = pk = 0
        for d in delta:
            live += d
            pk = max(pk, live)
        return pk

    def n_persist(self):
        return sum(1 for k in self.kind if k == "persist")


def schedule_full(words16, rounds):
    w = list(words16)
    for t in range(16, rounds):
        w.append((small_sigma1(w[t - 2]) + w[t - 7] + small_sigma0(w[t - 15]) + w[t - 16]) & MASK32)
    return w


def ref_states(words16, rounds_upto):
    """List of states after each round 0..rounds_upto-1 (reference, scalar)."""
    w = schedule_full(words16, max(rounds_upto, 16))
    a, b, c, d, e, f, g, h = IV
    out = []
    for t in range(rounds_upto):
        t1 = (h + big_sigma1(e) + ((e & f) ^ (~e & g)) + K[t] + w[t]) & MASK32
        t2 = (big_sigma0(a) + ((a & b) ^ (a & c) ^ (b & c))) & MASK32
        a, b, c, d, e, f, g, h = (t1 + t2) & MASK32, a, b, c, (d + t1) & MASK32, e, f, g
        out.append((a, b, c, d, e, f, g, h))
    return out


def ref_key_words(words16, R):
    """(A_{R-4}, A_{R-3}, E_{R-4}, E_{R-3}, E_{R-2}) from the reference (full rounds to R-1 for cross-check)."""
    st = ref_states(words16, R)
    sR2 = st[R - 2]          # state after round R-2
    a, b, c, d, e, f, g, h = sR2
    sR1 = st[R - 1]          # state after round R-1: (d,c,h,g,f) must equal (c,b,g,f,e) of sR2
    require((sR1[3], sR1[2], sR1[7], sR1[6], sR1[5]) == (c, b, g, f, e), "key words are final-state words")
    return (c, b, g, f, e)


def key_value(kw):
    """144-bit address from (A_{R-4}, A_{R-3}, E_{R-4}, E_{R-3}, E_{R-2}): 4 x (32 + 4 bits of E_{R-2})."""
    x1, x2, x3, x4, x5 = kw
    q1 = x1 | ((x5 & 0xF) << 32)
    q2 = x2 | (((x5 >> 4) & 0xF) << 32)
    q3 = x3 | (((x5 >> 8) & 0xF) << 32)
    q4 = x4 | (((x5 >> 12) & 0xF) << 32)
    return q1 | (q2 << 36) | (q3 << 72) | (q4 << 108)


def batch(g: Prog, prefixes, v, R, Wv_packed, words_fixed=None):
    """Counted per-message batch.  prefixes: 7 lists of 16 words (word v ignored).  Wv_packed: the varying word
    register value (all lanes).  Returns the 7 addresses (from the SWAR values) and the key-word V's."""
    # group-constant words
    w = {}
    for i in range(16):
        if i == v:
            continue
        w[i] = g.gconst(pack([prefixes[l][i] for l in range(LANES7)]))
    Wv = g.input_reg(Wv_packed, MASK32, "persist")   # the counter register (loop-carried)
    w[v] = Wv
    sig_use = {}
    last_sched = R - 2
    for t in range(16, last_sched + 1):
        for s in (t - 2, t - 15):
            sig_use[s] = sig_use.get(s, 0) + 1

    def word_terms(t):
        if t < 16 or sig_use.get(t, 0) > 0:
            if t not in w:
                g.sec = "schedule"
                s = g.sum([g.small0(word(t - 15)), word(t - 16), word(t - 7), g.small1(word(t - 2))])
                if s.const is None and sig_use.get(t, 0) and not g.clean(s):
                    s = g.andm(s, "M")
                w[t] = s
                g.sec = "rounds"
            return [w[t]]
        else:
            # Terminal schedule words (t in {R-3, R-2}, sig_use == 0) need no mask M; returning their four
            # additive schedule terms directly folds any constant schedule terms with K[t] in t1_terms.
            g.sec = "schedule"
            s0_w = g.small0(word(t - 15))
            w16 = word(t - 16)
            w7 = word(t - 7)
            s1_w = g.small1(word(t - 2))
            g.sec = "rounds"
            return [s0_w, w16, w7, s1_w]

    def word(t):
        return word_terms(t)[0]

    # state entering round v: group constant
    g.sec = "rounds"
    sts = [ref_states(prefixes[l][:v] + [0] * (16 - v), v) if v > 0 else None for l in range(LANES7)]
    if v > 0:
        st = [pack([sts[l][v - 1][j] for l in range(LANES7)]) for j in range(8)]
    else:
        st = [rep(x) for x in IV]
    a, b, c, d, e, f, gg, h = (g.gconst(x) for x in st)
    prev_ab = None
    states = {}
    for t in range(v, R - 1):
        e_only = (t == R - 2)
        w_terms = word_terms(t)
        s1 = g.big(e, (6, 11, 25), big_sigma1)
        if e.const is not None and f.const is not None and gg.const is not None:
            ch = g.gconst(pack([(x & y) ^ (~x & z) & MASK32 for x, y, z in zip(unpack(e.const), unpack(f.const), unpack(gg.const))]))
        else:
            fg = g.xor(f, gg)
            ch = g.xor(gg, g.band(e, fg))
        kt = g.gconst(rep(K[t]))
        t1_terms = [h, s1, ch, kt] + w_terms
        if e_only:
            # E_{R-2} is only read via (x5 << 20..32) & G4, which reads only bits 0..15 of each 36-bit lane;
            # since e_n.bnd < 2^36 (verified by g.add), bits 32..35 do not affect bits 0..15 and need no M mask.
            e_n = g.sum(t1_terms + [d])
            states[t] = ("E", e_n)
            a, b, c, d, e, f, gg, h = None, a, b, c, e_n, e, f, gg
            break
        if a.const is not None and b.const is not None and c.const is not None:
            mj = g.gconst(pack([(x & y) ^ (x & z) ^ (y & z) for x, y, z in zip(unpack(a.const), unpack(b.const), unpack(c.const))]))
            ab = g.xor(a, b)
        else:
            ab = g.xor(a, b)
            bc = prev_ab if prev_ab is not None else g.xor(b, c)
            mj = g.xor(b, g.band(ab, bc))
        prev_ab = ab
        # share the variable part of T1 between E and A; compute e_n before s0 = big_sigma0(a) to reduce peak live registers
        consts = [x for x in t1_terms if x.const is not None]
        vars_ = [x for x in t1_terms if x.const is None]
        ct1 = None
        for x in consts:
            ct1 = x if ct1 is None else g.add(ct1, x)
        if not vars_:
            t1 = ct1
            e_n = g.sum([d, t1])
            if e_n.const is None:
                e_n = g.andm(e_n, "M")
            s0 = g.big(a, (2, 13, 22), big_sigma0)
            a_n = g.sum([t1, s0, mj])
        elif d.const is not None:
            base = g.sum(vars_)
            e_n = g.sum([base, g.add(ct1, d) if ct1 is not None else d])
            if e_n.const is None:
                e_n = g.andm(e_n, "M")
            s0 = g.big(a, (2, 13, 22), big_sigma0)
            a_n = g.sum([base, s0, mj] + ([ct1] if ct1 is not None else []))
        else:
            t1 = g.sum(t1_terms)
            e_n = g.add(d, t1)
            if e_n.const is None:
                e_n = g.andm(e_n, "M")
            s0 = g.big(a, (2, 13, 22), big_sigma0)
            a_n = g.sum([t1, s0, mj])
        if a_n.const is None:
            a_n = g.andm(a_n, "M")
        a, b, c, d, e, f, gg, h = a_n, a, b, c, e_n, e, f, gg
    # after the loop: state after round R-2 has a=None (skipped), b=A_{R-3}, c=A_{R-4}, e=E_{R-2}, f=E_{R-3}, g=E_{R-4}
    kw = (c, b, gg, f, e)
    return kw, Wv


def key_and_table(g: Prog, kw):
    """Fold 16 bits of E_{R-2} into guard bits, extract the 7 per-lane 144-bit addresses via a 2-level butterfly,
    and probe the table."""
    x1, x2, x3, x4, x5 = [g.materialise(x) for x in kw]
    g.sec = "key"
    G = g.mask("G4")
    q1 = g.bor(x1, g.band(g.shl(x5, 32), G))
    q2 = g.bor(x2, g.band(g.shl(x5, 28), G))
    q3 = g.bor(x3, g.band(g.shl(x5, 24), G))
    q4 = g.bor(x4, g.band(g.shl(x5, 20), G))

    # 2-level butterfly transpose for lanes 0..5 + direct unmasked shifts for lane 6 (50 ops vs 72 ops):
    # Level 1 (16 ops): pair (q1, q2) into 72-bit blocks e01 (lanes 0, 2, 4) and o01 (lanes 1, 3, 5),
    # and pair (q3, q4) into e23 (lanes 0, 2, 4) and o23 (lanes 1, 3, 5).
    e01 = g.bor(g.andm(q1, "MEVEN"), g.andm(g.shl(q2, 36), "MODD"))
    o01 = g.bor(g.andm(g.shr(q1, 36), "MEVEN"), g.andm(q2, "MODD"))
    e23 = g.bor(g.andm(q3, "MEVEN"), g.andm(g.shl(q4, 36), "MODD"))
    o23 = g.bor(g.andm(g.shr(q3, 36), "MEVEN"), g.andm(q4, "MODD"))

    # Level 2 (24 ops): extract 144-bit keys for lanes 0..5.  Since e01, o01 < 2^216, (e01 >> 144) and (o01 >> 144)
    # are already < 2^72 and need no M72_0 mask.
    a0 = g.bor(g.andm(e01, "M72_0"), g.andm(g.shl(e23, 72), "M72_1"))
    a1 = g.bor(g.andm(o01, "M72_0"), g.andm(g.shl(o23, 72), "M72_1"))
    a2 = g.bor(g.andm(g.shr(e01, 72), "M72_0"), g.andm(e23, "M72_1"))
    a3 = g.bor(g.andm(g.shr(o01, 72), "M72_0"), g.andm(o23, "M72_1"))
    a4 = g.bor(g.shr(e01, 144), g.andm(g.shr(e23, 72), "M72_1"))
    a5 = g.bor(g.shr(o01, 144), g.andm(g.shr(o23, 72), "M72_1"))

    # Lane 6 (10 ops, zero masks): since q1..q4 < 2^252, (q_i >> 216) < 2^36 has zero bits above bit 35.
    a6 = g.bor(
        g.bor(g.shr(q1, 216), g.shl(g.shr(q2, 216), 36)),
        g.bor(g.shl(g.shr(q3, 216), 72), g.shl(g.shr(q4, 216), 108)),
    )
    addrs = [a0, a1, a2, a3, a4, a5, a6]

    g.sec = "table"
    c_reg = g.persist_regs["c"]
    TW = g.mask("THRESH")
    cur = c_reg
    for l in range(LANES7):
        if l > 0:
            nxt, _ = g._arith(0, (1 << 256) - 1, cur, g.persist_regs["ONE"])    # c_l = c_{l-1} + 1 (index field)
            cur = nxt
        # LOAD S[addr] (access + address), XOR with c_l, compare with 2^136, branch, STORE S[addr] = c_l
        g._count("load"); g._count("addr")
        wreg = g._reg(0, (1 << 256) - 1, "tmp")
        g._use(addrs[l])
        x, _ = g._arith(0, (1 << 256) - 1, wreg, cur)
        g._arith(0, 1, x, TW)            # compare
        g._count()                       # conditional branch
        g._use(addrs[l], cur)
        g._count("store"); g._count("addr")
        g.t += 1
    g.sec = "loop"
    g._arith(0, (1 << 256) - 1, c_reg, g.persist_regs["EIGHT"])   # c += 8: next batch, lane field cleared
    return [a.val for a in addrs]


def loop_control(g: Prog, wv):
    """Counter word += INC, compare with END, conditional branch."""
    g.sec = "loop"
    g._arith(0, (1 << 256) - 1, wv, g.persist_regs["INC"])
    g._arith(0, 1, wv, g.persist_regs["END"])
    g._count()

# ---- scaled table model (verbatim from the package builder) ----

# digest bit positions (word index 0..7 = a..h, bit within the 32-bit word); key bits come first
KEY_BITS_POS = [(3, 0), (2, 1), (7, 2), (6, 3), (3, 9), (2, 10), (7, 11), (6, 12), (3, 18), (2, 19), (7, 20)]
OTHER_POS = [(5, 4), (0, 5), (1, 6), (4, 7), (5, 13)]
MASK_POS = KEY_BITS_POS + OTHER_POS          # 16 bits
GROUPS, COUNTERS = 7, 52                     # N = 364 messages per trial, one scaled group batch
IDX_BITS, TAG_BITS = 9, 6                    # index n = (t << 3) | l fits 9 bits; 6-bit TAG
CONFIGS = {"h1-success": 11, "h1-overwrite": 8}   # key bits per experiment


def mask_int():
    m = 0
    for w, b in MASK_POS:
        m |= 1 << ((7 - w) * 32 + b)
    return m


def bits_of(dig_int, positions):
    v = 0
    for i, (w, b) in enumerate(positions):
        v |= ((dig_int >> ((7 - w) * 32 + b)) & 1) << i
    return v


def cap_for(n, k):
    """V = floor(N^2/2^k) + floor(N^2/2^(k+6)) + garbage allowance (8 x the expected garbage calls, min 8)."""
    return (n * n >> k) + (n * n >> (k + 6)) + max(8, (8 * n) >> TAG_BITS)


def run(k, digest_of, msg_of, g0, t0, tag, garbage_word):
    """One scaled run.  digest_of(msg) -> int; msg_of(g, t) -> message; garbage_word(slot) -> int.
    Returns (pair or None, stats)."""
    n_msgs = GROUPS * COUNTERS
    V = cap_for(n_msgs, k)
    table = {}
    keymask = (1 << k) - 1
    st = {"cold": 0, "garbage": 0, "keymatch": 0, "overwrite_loss": 0, "capped": 0}
    seen = {}            # full masked digest -> (msg, n) of every processed message, for the missed-collision check
    found = None
    missed = None
    for t in range(COUNTERS):
        for l in range(GROUPS):
            msg = msg_of(g0 + l, t0 + t)
            d = digest_of(msg)
            dm = bits_of(d, MASK_POS)
            key = bits_of(d, KEY_BITS_POS[:k]) & keymask
            n = (t << 3) | l
            c = (tag << IDX_BITS) | n
            w = table.get(key)
            if w is None:
                w = garbage_word(key)
            if found is None and (w >> IDX_BITS) == tag:
                st["cold"] += 1
                if st["cold"] > V + 1:
                    st["capped"] = 1
                    return None, missed, st
                n_old = w & ((1 << IDX_BITS) - 1)
                t_old, l_old = n_old >> 3, n_old & 7
                m_old = msg_of(g0 + l_old, t0 + t_old)
                if key in table:
                    st["keymatch"] += 1
                else:
                    st["garbage"] += 1
                if m_old != msg and bits_of(digest_of(m_old), MASK_POS) == dm:
                    found = (m_old, msg)
            if found is None and dm in seen and seen[dm][0] != msg and missed is None:
                missed = (seen[dm][0], msg)
            seen.setdefault(dm, (msg, n))
            table[key] = c
        if found is not None:
            break
    if found is None and missed is not None:
        st["overwrite_loss"] = 1
    return found, missed, st


# ---- self-check of the counted batch on the deterministic family ----------------------------------------------
def v1_self_check(seed, batches):
    last = None
    for bi in range(batches):
        h = hashlib.sha256((seed + "selfcheck%d" % bi).encode()).digest()
        g0 = int.from_bytes(h[:13], "big")
        t = int.from_bytes(h[13:16], "big")
        P, R0 = run_coins(seed + "selfcheck%d" % bi)
        prefixes = [family_words(g0 + l, t, P, R0) for l in range(LANES7)]
        g = Prog(PERSIST)
        kw, wv = batch(g, prefixes, 13, R, pack([prefixes[l][13] for l in range(LANES7)]))
        addrs = key_and_table(g, kw)
        loop_control(g, wv)
        for l in range(LANES7):
            require(addrs[l] == key_value(ref_key_words(prefixes[l], R)), "lane %d key mismatch" % l)
        got = {"total": sum(g.ops.values()), "sections": g.sections, "ops": g.ops,
               "persistent": g.n_persist(), "peak_tmp": g.peak()}
        require(got == EXPECTED, "counted batch differs from the charged ledger: %r" % (got,))
        require(g.n_persist() + g.peak() <= 64, "register file exceeded")
        last = got
    return last


# ---- organizer experiments --------------------------------------------------------------------------------------
def trial(seed, k):
    h = hashlib.sha256(("trial" + seed).encode()).digest()
    g0 = int.from_bytes(h[:12], "big")                         # first group of the scaled group batch
    t0 = int.from_bytes(h[12:15], "big") % ((1 << 24) - COUNTERS)
    tag = h[15] & ((1 << TAG_BITS) - 1)

    def garbage_word(slot):                                     # fixed contents of never-written slots
        return int.from_bytes(hashlib.sha256(("garbage" + seed + ":%d" % slot).encode()).digest()[:4], "big") \
            & ((1 << (IDX_BITS + TAG_BITS)) - 1)

    cache = {}

    def digest_of(msg):
        v = cache.get(msg)
        if v is None:
            v = cache[msg] = digest_int(msg, R)
        return v

    P, R0 = run_coins(seed)
    return run(k, digest_of, lambda g, t: family_message(g, t, P, R0), g0, t0, tag, garbage_word)


def main():
    request = json.load(sys.stdin)
    eid = request["experiment_id"]
    k = CONFIGS[eid]
    require(int(request["event"]["mask_hex"], 16) == mask_int(), "declared mask differs from the scaled model")
    rows = []
    for entry in request["trials"]:
        found, missed, st = trial(entry["seed"], k)
        pair = found if eid == "h1-success" else (missed if found is None else None)
        row = {"trial": entry["trial"],
               "message_a_hex": pair[0].hex() if pair else None,
               "message_b_hex": pair[1].hex() if pair else None,
               "observations": {"cold": st["cold"], "garbage": st["garbage"], "keymatch": st["keymatch"],
                                "capped": st["capped"], "overwrite_loss": st["overwrite_loss"]}}
        if entry["trial"] == 0 and eid == "h1-success":
            res = v1_self_check(entry["seed"], 4)
            row["observations"].update({"v1_batch_ops": res["total"], "v1_persistent": res["persistent"],
                                        "v1_peak_tmp": res["peak_tmp"]})
        rows.append(row)
    sys.stdout.write(json.dumps({"schema_version": 1, "trials": rows}, separators=(",", ":"), sort_keys=True))


if __name__ == "__main__":
    main()
