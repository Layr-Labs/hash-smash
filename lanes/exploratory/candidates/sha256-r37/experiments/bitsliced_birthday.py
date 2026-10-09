"""Scaled replay of the bit-sliced grouped birthday search for reduced SHA-256 (r37 / r38).

Messages are 55 bytes, so each is one padded block: W0..W12 form a group prefix,
W13 = (u << 8) | 0x80 carries the 24-bit inner variable u, W14 = 0, W15 = 440.
The R-round digest is IV + (A_{R-1}, A_{R-2}, A_{R-3}, A_{R-4}, E_{R-1}, ..., E_{R-4}).
The search key is the 144-bit string
    A_{R-3} || A_{R-4} || (E_{R-2} mod 2^16) || E_{R-3} || E_{R-4}
(digest words c, d, low half of f, g, h minus the IV), which is fixed before
round R-1 and needs only the E half of round R-2 (low 16 bits).

This file contains the complete counted program:
  * `build`  - the bit-sliced Boolean circuit (256 messages per batch, one per
    bit position of a 256-bit plane) for rounds 13..R-2, with free rotations,
    polarity-tracked NOT, 5-gate full adders and group-constant hoisting;
  * `add_transpose` - a zero-aware delta-swap transpose turning the 144 key
    planes, one all-ones row and the 8 lane planes into one 256-bit key word per
    message (key in the high half, lane number in bits 96..103); swaps whose
    operands are all global constants are precomputed once;
  * `emit` - furthest-next-use register allocation over all 64 registers (the
    loop-carried batch id word and the two table temporaries are ordinary
    allocated values), emitting loads and stores explicitly;
  * `VM` - executes the emitted program plus the batch setup and the per-message
    table step, charging one operation per instruction.
Trial 0 of every request re-derives the operation count of one batch on the VM
and checks every lane of that batch against the scalar reference compression
in this file; any mismatch aborts the run. Every trial also checks two lanes.

The scaled search itself (experiment ids):
  s256-bs-spread       : 16 groups x 32 consecutive u values (u = 0..31)
  s256-bs-single-group : 1 group x 512 consecutive u values (u = 0..511)
N_t = 512 = 2^(18/2) samples per trial against an 18-bit masked event on digest
bits computed only by the bit-sliced circuit (words H2, H3, H5 bits 0..15, H6,
H7); random-function success 1 - prod_{i<512}(1 - i/2^18) = 0.39307.
"""

import hashlib
import json
import struct
import sys

M32 = 0xFFFFFFFF
ALL = (1 << 256) - 1
IV = (0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
      0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19)
K = (0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
     0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
     0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
     0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
     0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85)
KEY_EBITS = 16
INDEP = (16, 17, 18, 19, 21, 23, 25)       # schedule words independent of W13
NREG = 64                                   # machine registers, all allocatable
R_BID = 63                                  # batch id word at batch start and end (loop-carried)
ADDR_SHIFT = 111                            # table index = key word >> 111, in [2^144, 2^145)
LANE_ROW0 = 96                              # lane number L lands in key-word bits 96..103
CLAIMED_BATCH_OPS = {37: 45518, 38: 47897}  # checked on the VM in trial 0
SAMPLES = 512
LAYOUT = {"s256-bs-spread": (16, 32), "s256-bs-single-group": (1, 512)}
ONE, ZERO = ("C", 1), ("C", 0)


# ---------------------------------------------------------------- circuit
class Net:
    """Signed literals (node, neg) or constants ('C', bit). NOT is a polarity flip."""

    def __init__(self):
        self.nodes, self.cse, self.inputs, self.grp, self.hdef = [], {}, {}, set(), {}

    def inp(self, name):
        if name not in self.inputs:
            self.nodes.append(("in", name))
            n = len(self.nodes) - 1
            self.inputs[name] = n
            if not name.startswith(("lane[", "uhi[")):
                self.grp.add(n)
        return (self.inputs[name], 0)

    def gate(self, op, a, b):
        if a > b:
            a, b = b, a
        key = (op, a, b)
        if key in self.cse:
            return self.cse[key]
        if a in self.grp and b in self.grp:          # group-only: hoisted to group setup
            self.nodes.append(("in", "H%d" % len(self.nodes)))
            n = len(self.nodes) - 1
            self.hdef[n] = key
            self.grp.add(n)
        else:
            self.nodes.append(key)
            n = len(self.nodes) - 1
        self.cse[key] = n
        return n

    @staticmethod
    def isc(x):
        return x[0] == "C"

    def NOT(self, x):
        return (x[0], 1 - x[1]) if not self.isc(x) else ("C", 1 - x[1])

    def XOR(self, x, y):
        if self.isc(x):
            x, y = y, x
        if self.isc(y):
            return ("C", x[1] ^ y[1]) if self.isc(x) else (x[0], x[1] ^ y[1])
        if x[0] == y[0]:
            return ("C", x[1] ^ y[1])
        return (self.gate("xor", x[0], y[0]), x[1] ^ y[1])

    def AND(self, x, y):
        if self.isc(x):
            x, y = y, x
        if self.isc(y):
            return x if y[1] else ZERO
        if x[0] == y[0]:
            return x if x[1] == y[1] else ZERO
        if not x[1] and not y[1]:
            return (self.gate("and", x[0], y[0]), 0)
        if x[1] and y[1]:                                   # ~X & ~Y = ~(X | Y)
            return (self.gate("or", x[0], y[0]), 1)
        if x[1]:
            x, y = y, x
        return (self.gate("and", self.gate("xor", x[0], y[0]), x[0]), 0)  # X & ~Y = (X^Y) & X

    def OR(self, x, y):
        return self.NOT(self.AND(self.NOT(x), self.NOT(y)))

    def CH(self, e, f, g):
        if self.isc(e):
            return f if e[1] else g
        d = self.XOR(f, g)
        if self.isc(d):
            return self.XOR(g, self.AND(e, d))
        if d[1] == 0:
            if e[1] == 0:
                return self.XOR(g, (self.gate("and", e[0], d[0]), 0))
            return self.XOR(f, (self.gate("and", e[0], d[0]), 0))
        if e[1] == 0:
            return self.NOT(self.XOR(f, (self.gate("or", e[0], d[0]), 0)))
        return self.NOT(self.XOR(g, (self.gate("or", e[0], d[0]), 0)))

    def MAJ(self, a, b, c):
        d1 = self.XOR(a, b)
        d2 = self.XOR(b, c)
        if self.isc(d1) or self.isc(d2):
            return self.XOR(b, self.AND(d1, d2))
        if d1[1] == 0 and d2[1] == 0:
            return self.XOR(b, (self.gate("and", d1[0], d2[0]), 0))
        if d1[1] == 1 and d2[1] == 1:
            return self.NOT(self.XOR(b, (self.gate("or", d1[0], d2[0]), 0)))
        if d1[1] == 0 and d2[1] == 1:
            return self.NOT(self.XOR(c, (self.gate("or", d1[0], d2[0]), 0)))
        return self.NOT(self.XOR(a, (self.gate("or", d1[0], d2[0]), 0)))


class Col:
    """Column-compression adder modulo 2^nbits, advanced one bit column at a time."""

    def __init__(self, net, nbits=32):
        self.n, self.nbits, self.carry, self.j = net, nbits, [], 0

    def step(self, bits):
        n = self.n
        col = self.carry + list(bits)
        self.carry = []
        last = self.j == self.nbits - 1
        k = sum(l[1] for l in col if n.isc(l))
        col = [l for l in col if not n.isc(l)]
        if k >= 2 and not last:
            self.carry += [ONE] * (k // 2)
        if k % 2:
            col.append(ONE)
        while len(col) >= 3:                                # full adder: 5 gates (or 2 with ONE)
            if col[-1] is ONE:
                found = False
                for i in range(len(col) - 1):
                    for j in range(i + 1, len(col) - 1):
                        if col[i][1] == col[j][1]:
                            b = col.pop(j)
                            a = col.pop(i)
                            col.pop()
                            found = True
                            break
                    if found:
                        break
                if found:
                    if not last:
                        self.carry.append(n.OR(a, b))
                    col.append(n.NOT(n.XOR(a, b)))
                    continue
            a, b, c = col.pop(0), col.pop(0), col.pop(0)
            if not last:
                if c is ONE:
                    self.carry.append(n.OR(a, b))
                    col.append(n.NOT(n.XOR(a, b)))
                    continue
                t = n.XOR(a, b)
                col.append(n.XOR(t, c))
                if t[1] == 0:
                    self.carry.append(n.CH(t, c, a))
                else:
                    self.carry.append(n.CH((t[0], 0), a, c))
            else:
                col.append(n.XOR(n.XOR(a, b), c))
        if len(col) == 2:                                   # half adder
            a, b = col
            if not last:
                self.carry.append(n.AND(a, b))
            col = [n.XOR(a, b)]
        self.j += 1
        return col[0] if col else ZERO


def build(R):
    """Circuit for rounds 13..R-2 of one batch. Returns (net, key literals: 144 planes)."""
    net = Net()
    last = R - 2
    W = {13: [ONE if (0x80 >> j) & 1 else ZERO for j in range(8)]
         + [net.inp("lane[%d]" % i) for i in range(8)] + [net.inp("uhi[%d]" % i) for i in range(16)]}

    def dep(i):
        return i == 13 or (i >= 16 and i not in INDEP)

    def terms(t):
        out, inv = [], False
        for idx, kind in ((t - 2, "s1"), (t - 7, "id"), (t - 15, "s0"), (t - 16, "id")):
            if not dep(idx):
                inv = True
                continue
            w = W[idx]
            if kind == "s1":
                out.append(lambda j, w=w: net.XOR(net.XOR(w[(j + 17) % 32], w[(j + 19) % 32]), w[j + 10] if j < 22 else ZERO))
            elif kind == "s0":
                out.append(lambda j, w=w: net.XOR(net.XOR(w[(j + 7) % 32], w[(j + 18) % 32]), w[j + 3] if j < 29 else ZERO))
            else:
                out.append(lambda j, w=w: w[j])
        if inv:
            out.append(lambda j: net.inp("P%d[%d]" % (t, j)))
        return out

    A = {i: [net.inp("A%d[%d]" % (i, j)) for j in range(32)] for i in (10, 11, 12)}
    E = {i: [net.inp("E%d[%d]" % (i, j)) for j in range(32)] for i in (10, 11, 12)}
    ca, ce = Col(net), Col(net)
    A[13] = [ca.step([net.inp("A13pre[%d]" % j), W[13][j]]) for j in range(32)]
    E[13] = [ce.step([net.inp("DT13pre[%d]" % j), W[13][j]]) for j in range(32)]
    for t in range(14, last + 1):
        a, b, c, d = A[t - 1], A[t - 2], A[t - 3], A[t - 4]
        e, f, g, h = E[t - 1], E[t - 2], E[t - 3], E[t - 4]
        indep = t in INDEP or t <= 15
        if not indep and t < last:
            wcol, ts, W[t] = Col(net), terms(t), []
        elif not indep:
            ts = terms(t)
        nb = KEY_EBITS if t == last else 32
        c1, c2, c3 = Col(net, nb), Col(net, nb), Col(net)
        Et, At = [], []
        for j in range(nb):
            if indep:
                kw = [net.inp("HKW%d[%d]" % (t, j))] if t <= 16 else [net.inp("KW%d[%d]" % (t, j)), h[j]]
            elif t < last:
                wj = wcol.step([fn(j) for fn in ts])
                W[t].append(wj)
                kw = [wj, ONE if (K[t] >> j) & 1 else ZERO, h[j]]
            else:
                kw = [fn(j) for fn in ts] + [ONE if (K[t] >> j) & 1 else ZERO, h[j]]
            s1j = net.XOR(net.XOR(e[(j + 6) % 32], e[(j + 11) % 32]), e[(j + 25) % 32])
            chj = net.CH(e[j], f[j], g[j])
            if t == last:
                Et.append(c1.step(kw + [s1j, chj, d[j]]))
            else:
                t1j = c1.step(kw + [s1j, chj])
                Et.append(c2.step([d[j], t1j]))
                s0j = net.XOR(net.XOR(a[(j + 2) % 32], a[(j + 13) % 32]), a[(j + 22) % 32])
                mj = net.MAJ(a[j], b[j], c[j])
                At.append(c3.step([t1j, s0j, mj]))
        E[t], A[t] = Et, At
    return net, A[last - 1] + A[last - 2] + E[last] + E[last - 1] + E[last - 2]


# ---------------------------------------------------------------- transpose
def tmask(k):
    return sum(1 << c for c in range(256) if not (c >> k) & 1)


def key_row(kb):
    """Row (= key-word bit) of key bit kb: bits 4..143 -> rows 111..250, bits 0..3 -> 251..254."""
    return 251 + kb if kb < 4 else 107 + kb


def word_key(word, pol):
    """The 144-bit key (bit 0 = A_{R-3} bit 0) read back from a transposed key word."""
    word ^= pol
    return sum(((word >> key_row(kb)) & 1) << kb for kb in range(144))


def add_transpose(net, key):
    """Rows 111..254: key planes (as stored; the polarity constant `pol` is a fixed XOR).
    Row 255: the constant all-ones plane, so table indices (word >> 111) lie in
    [2^144, 2^145). Rows 96..103: the lane planes, so bits 96..103 of word L hold L.
    Other rows are zero. A swap whose operands are all global constants (lane,
    ones and mask planes, or results of such swaps) is computed once in global
    setup and becomes an input plane (`cdef`). Returns (sink per message, pol, cdef)."""
    rows, pol = {}, 0
    for kb, lit in enumerate(key):
        rows[key_row(kb)] = lit[0]
        pol |= lit[1] << key_row(kb)
    rows[255] = net.inp("ones")[0]
    for i in range(8):
        rows[LANE_ROW0 + i] = net.inp("lane[%d]" % i)[0]
    mk = {k: net.inp("mask%d" % k)[0] for k in range(8)}
    const = {net.inputs[n] for n in net.inputs if n == "ones" or n.startswith(("mask", "lane["))}
    cdef = {}

    def raw(nd):
        if nd[0] != "sink" and all(o in const for o in operands(nd)):
            net.nodes.append(("in", "TC%d" % len(net.nodes)))
            n = len(net.nodes) - 1
            cdef[n] = nd
            const.add(n)
            return n
        net.nodes.append(nd)
        return len(net.nodes) - 1

    sinks = {}
    for pbits in ((0, 1, 2), (3, 4, 5, 6, 7)):
        other = [b for b in range(8) if b not in pbits]
        for gi in range(1 << len(other)):
            base = sum(((gi >> n) & 1) << b for n, b in enumerate(other))
            members = [base + sum(((x >> n) & 1) << b for n, b in enumerate(pbits)) for x in range(1 << len(pbits))]
            for k in pbits:
                d = 1 << k
                for i in members:
                    if i & d:
                        continue
                    a, b = rows.get(i), rows.get(i + d)
                    if a is None and b is None:
                        continue
                    if a is not None and b is not None:          # delta swap, 6 operations
                        t = raw(("and", raw(("xor", raw(("shr", a, d)), b)), mk[k]))
                        rows[i], rows[i + d] = raw(("xor", a, raw(("shl", t, d)))), raw(("xor", b, t))
                    elif b is None:                              # 3 operations
                        rows[i], rows[i + d] = raw(("and", a, mk[k])), raw(("and", raw(("shr", a, d)), mk[k]))
                    else:                                        # 3 operations
                        t = raw(("and", b, mk[k]))
                        rows[i], rows[i + d] = raw(("shl", t, d)), raw(("xor", b, t))
            if pbits[0] == 3:
                for i in members:
                    sinks[i] = raw(("sink", rows[i]))
    return sinks, pol, cdef


def const_value(nd, val):
    """Value of a precomputed constant swap node (operands already in val)."""
    if nd[0] == "shr":
        return val[nd[1]] >> nd[2]
    if nd[0] == "shl":
        return (val[nd[1]] << nd[2]) & ALL
    a, b = val[nd[1]], val[nd[2]]
    return a ^ b if nd[0] == "xor" else a & b if nd[0] == "and" else a | b


def operands(nd):
    if nd[0] == "in":
        return ()
    if nd[0] in ("shr", "shl", "sink"):
        return (nd[1],)
    return (nd[1], nd[2])


# ---------------------------------------------------------------- group constants
def ror(x, r):
    return ((x >> r) | (x << (32 - r))) & M32


def s0(x): return ror(x, 7) ^ ror(x, 18) ^ (x >> 3)
def s1(x): return ror(x, 17) ^ ror(x, 19) ^ (x >> 10)
def S0(x): return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22)
def S1(x): return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25)


def group_consts(w, R):
    """32-bit group constants named by the circuit inputs, from prefix words W0..W12."""
    ws = dict(enumerate(w))
    ws[14], ws[15] = 0, 440
    for t in INDEP:
        ws[t] = (s1(ws[t - 2]) + ws[t - 7] + s0(ws[t - 15]) + ws[t - 16]) & M32
    a, b, c, d, e, f, g, h = IV
    out = {}
    for t in range(13):
        t1 = h + S1(e) + ((e & f) ^ (~e & g)) + K[t] + ws[t]
        t2 = S0(a) + ((a & b) ^ (a & c) ^ (b & c))
        a, b, c, d, e, f, g, h = (t1 + t2) & M32, a, b, c, (d + t1) & M32, e, f, g
        out["A%d" % t], out["E%d" % t] = a, e
    t13 = h + S1(e) + ((e & f) ^ (~e & g)) + K[13]
    out["A13pre"] = (t13 + S0(a) + ((a & b) ^ (a & c) ^ (b & c))) & M32
    out["DT13pre"] = (d + t13) & M32
    for t in (14, 15, 16):
        out["HKW%d" % t] = (out["E%d" % (t - 4)] + K[t] + ws[t]) & M32
    for t in (17, 18, 19, 21, 23, 25):
        out["KW%d" % t] = (K[t] + ws[t]) & M32
    for t in range(20, R - 1):
        if t in INDEP:
            continue
        acc = 0
        for idx, kind in ((t - 2, "s1"), (t - 7, "id"), (t - 15, "s0"), (t - 16, "id")):
            if not (idx == 13 or (idx >= 16 and idx not in INDEP)):
                v = ws[idx]
                acc += s1(v) if kind == "s1" else s0(v) if kind == "s0" else v
        out["P%d" % t] = acc & M32
    return out


def scalar_key(w, u, R):
    """Reference: the 144-bit key of message (w, u) from a plain R-round compression."""
    ws = list(w) + [(u << 8) | 0x80, 0, 440]
    for t in range(16, R):
        ws.append((s1(ws[t - 2]) + ws[t - 7] + s0(ws[t - 15]) + ws[t - 16]) & M32)
    a, b, c, d, e, f, g, h = IV
    for t in range(R):
        t1 = h + S1(e) + ((e & f) ^ (~e & g)) + K[t] + ws[t]
        t2 = S0(a) + ((a & b) ^ (a & c) ^ (b & c))
        a, b, c, d, e, f, g, h = (t1 + t2) & M32, a, b, c, (d + t1) & M32, e, f, g
    # final state (A_{R-1}, A_{R-2}, A_{R-3}, A_{R-4}, E_{R-1}, E_{R-2}, E_{R-3}, E_{R-4})
    return c | d << 32 | (f & 0xFFFF) << 64 | g << 80 | h << 112


# ---------------------------------------------------------------- fast evaluation
class Program:
    def __init__(self, R):
        self.R = R
        self.net, self.key = build(R)
        self.ninputs = len(self.net.nodes)
        self.sinks, self.pol, self.cdef = add_transpose(self.net, self.key)
        self._compile()

    def _compile(self):
        """Straight-line Python for circuit + transpose; returns the 256 key words."""
        net = self.net
        roots = [self.sinks[L] for L in range(256)]
        need, stack = set(), list(roots)
        while stack:
            n = stack.pop()
            if n in need:
                continue
            need.add(n)
            stack.extend(net.hdef[n][1:] if n in net.hdef else
                         operands(self.cdef[n]) if n in self.cdef else operands(net.nodes[n]))
        lines = ["def f(I):"]
        sym = {"xor": "^", "and": "&", "or": "|"}
        for n in sorted(need):
            nd = self.cdef.get(n, net.nodes[n])
            if n in net.hdef:
                op, a, b = net.hdef[n]
                lines.append(" v%d=v%d%sv%d" % (n, a, sym[op], b))
            elif nd[0] == "in":
                lines.append(" v%d=I[%r]" % (n, nd[1]))
            elif nd[0] == "shr":
                lines.append(" v%d=v%d>>%d" % (n, nd[1], nd[2]))
            elif nd[0] == "shl":
                lines.append(" v%d=(v%d<<%d)&%d" % (n, nd[1], nd[2], ALL))
            elif nd[0] == "sink":
                lines.append(" v%d=v%d" % (n, nd[1]))
            else:
                lines.append(" v%d=v%d%sv%d" % (n, nd[1], sym[nd[0]], nd[2]))
        lines.append(" return (%s)" % ",".join("v%d" % n for n in roots))
        env = {}
        exec(compile("\n".join(lines), "<bitsliced>", "exec"), env)
        self.f = env["f"]

    def inputs(self, lanes):
        """lanes: list of up to 256 (prefix words, u). Builds every input plane."""
        groups = {}
        for L, (w, u) in enumerate(lanes):
            groups.setdefault(tuple(w), []).append(L)
        I = {}
        for w, ls in groups.items():
            gm = sum(1 << L for L in ls)
            for name, v in group_consts(list(w), self.R).items():
                for j in range(32):
                    if (v >> j) & 1:
                        key = "%s[%d]" % (name, j)
                        I[key] = I.get(key, 0) | gm
        for name in self.net.inputs:
            I.setdefault(name, 0)
        for i in range(8):
            I["lane[%d]" % i] = sum(1 << L for L, (w, u) in enumerate(lanes) if (u >> i) & 1)
        for i in range(16):
            I["uhi[%d]" % i] = sum(1 << L for L, (w, u) in enumerate(lanes) if (u >> (8 + i)) & 1)
        for k in range(8):
            I["mask%d" % k] = tmask(k)
        I["ones"] = ALL
        return I

    def keys(self, lanes):
        """144-bit keys of up to 256 messages, from the bit-sliced circuit."""
        words = self.f(self.inputs(lanes))
        return [word_key(words[L], self.pol) for L in range(len(lanes))]


# ---------------------------------------------------------------- counted program
BID, C128 = "BID", "C128"          # batch id word (allocated value) and the constant 2^128


def bid_word(b, g, rtag):
    """Batch id word: b in bits 0..15, group number g (104 bits) in bits 16..95 and
    104..127, bits 96..103 zero (the transpose puts L there), run tag in 128..255."""
    return (rtag << 128) | ((g >> 80) << 104) | ((g & ((1 << 80) - 1)) << 16) | b


def emit(net, roots, nreg=NREG):
    """Furthest-next-use register allocation over all nreg registers.

    The batch id word BID starts in r[nreg-1] and is an ordinary value: it may be
    spilled (one store) and reloaded. A sink is the table step of one message: it
    reads the key word, BID and the constant 2^128 and takes two temporaries from
    the free registers. The final 'loop' instruction reads BID."""
    c128 = net.inp(C128)[0]
    need, stack = {c128}, list(roots)
    while stack:
        n = stack.pop()
        if n in need:
            continue
        need.add(n)
        stack.extend(operands(net.nodes[n]))
    order = [i for i in range(len(net.nodes)) if i in need and net.nodes[i][0] != "in"] + ["loop"]

    def opnds(n):
        if n == "loop":
            return (BID,)
        nd = net.nodes[n]
        return (nd[1], BID, c128) if nd[0] == "sink" else operands(nd)

    uses = {}
    for pos, n in enumerate(order):
        for o in opnds(n):
            uses.setdefault(o, []).append(pos)
    INF = 1 << 60
    ptr = {}

    def nxt(v, pos):
        u = uses.get(v, ())
        i = ptr.get(v, 0)
        while i < len(u) and u[i] < pos:
            i += 1
        ptr[v] = i
        return u[i] if i < len(u) else INF

    uhi_nodes = {net.inputs["uhi[%d]" % i] for i in range(16)}
    reg = {net.inputs["uhi[%d]" % i]: i for i in range(16)}
    reg[BID] = nreg - 1
    free = [r for r in range(nreg) if r not in reg.values()][::-1]
    inmem = {i for i in need if net.nodes[i][0] == "in" and i not in uhi_nodes}
    prog = []

    def evict(pos, protect):
        v = max((v for v in reg if v not in protect), key=lambda v: nxt(v, pos))
        r = reg.pop(v)
        if nxt(v, pos) < INF and v not in inmem:
            prog.append(("st", v, r))
            inmem.add(v)
        free.append(r)

    def take(pos, protect):
        if not free:
            evict(pos, protect)
        return free.pop()

    for pos, n in enumerate(order):
        ops = opnds(n)
        for o in ops:
            if o not in reg:
                reg[o] = take(pos, set(ops))
                prog.append(("ld", reg[o], o))
        src = [reg[o] for o in ops]
        if n == "loop":
            prog.append(("loop", src[0]))
            break
        nd = net.nodes[n]
        if nd[0] == "sink":
            tmp = [take(pos, set(ops)), take(pos, set(ops))]
            prog.append(("table", src[0], tmp[0], tmp[1], src[1], src[2], n))
            free.extend(tmp)
        for o in set(ops):
            if nxt(o, pos + 1) >= INF:
                free.append(reg.pop(o))
        if nd[0] == "sink":
            continue
        rd = take(pos + 1, set())
        reg[n] = rd
        prog.append((nd[0], rd, src[0], nd[2] if nd[0] in ("shr", "shl") else src[1]))
    return prog


class VM:
    """nreg registers x 256 bits; one operation per executed instruction."""

    def __init__(self, nreg=NREG):
        self.nreg = nreg
        self.r = [0] * nreg
        self.mem = {}
        self.table = {}
        self.ops = 0
        self.candidates = []

    def batch(self, prog, lane_of, garbage):
        r, mem, rb = self.r, self.mem, self.nreg - 1
        for i in range(16):                                  # batch planes in r[0..15]: 3 ops each
            r[i] = (0 - ((r[rb] >> i) & 1)) & ALL            # bit i of b = bit i of BID
            self.ops += 3
        self.keys = {}
        for ins in prog:
            op = ins[0]
            if op == "ld":
                r[ins[1]] = mem[ins[2]]
            elif op == "st":
                mem[ins[1]] = r[ins[2]]
            elif op == "xor":
                r[ins[1]] = r[ins[2]] ^ r[ins[3]]
            elif op == "and":
                r[ins[1]] = r[ins[2]] & r[ins[3]]
            elif op == "or":
                r[ins[1]] = r[ins[2]] | r[ins[3]]
            elif op == "shr":
                r[ins[1]] = r[ins[2]] >> ins[3]
            elif op == "shl":
                r[ins[1]] = (r[ins[2]] << ins[3]) & ALL
            elif op == "table":
                _, rk, ri, re, rbid, rc, node = ins
                L = lane_of[node]
                self.keys[L] = r[rk]
                r[ri] = r[rk] >> ADDR_SHIFT                      # 1  index in [2^144, 2^145)
                r[re] = self.table.get(r[ri], garbage)          # 1  load T[idx]
                r[rk] = r[rk] ^ r[rbid]                          # 1  entry x = key word ^ BID
                r[re] = r[re] ^ r[rk]                            # 1
                if r[re] < r[rc]:                                # 2  compare with 2^128, branch
                    self.candidates.append((L, self.table.get(r[ri], garbage)))
                self.table[r[ri]] = r[rk]                        # 1  store T[idx]
                self.ops += 7
                continue
            elif op == "loop":
                r[rb] = r[ins[1]] + 1                            # 4  BID + 1, load limit, compare, branch
                self.ops += 4
                continue
            self.ops += 1
        return self.ops


def count_batch(P, w, b, g=0, rtag=0, nreg=NREG):
    """Run one batch (prefix w, u = b*256 + L) on the VM. Returns (ops, key words, max register, prog, vm)."""
    net = P.net
    prog = emit(net, [P.sinks[L] for L in range(256)], nreg)
    lane_of = {n: L for L, n in P.sinks.items()}
    gc = group_consts(w, P.R)
    mem = {}
    val = {}
    for n, nd in enumerate(net.nodes[:]):
        if nd[0] != "in":
            continue
        name = nd[1]
        if n in net.hdef:
            op, a, c = net.hdef[n]
            v = val[a] ^ val[c] if op == "xor" else val[a] & val[c] if op == "and" else val[a] | val[c]
        elif n in P.cdef:
            v = const_value(P.cdef[n], val)
        elif name.startswith("lane["):
            v = sum(1 << L for L in range(256) if (L >> int(name[5:-1])) & 1)
        elif name.startswith("mask"):
            v = tmask(int(name[4:]))
        elif name == "ones":
            v = ALL
        elif name == C128:
            v = 1 << 128
        elif name.startswith("uhi["):
            v = 0
        else:
            base, j = name[:-1].split("[")
            v = ALL if (gc[base] >> int(j)) & 1 else 0
        val[n] = v
        mem[n] = v
    vm = VM(nreg)
    vm.mem = mem
    vm.r[nreg - 1] = bid_word(b, g, rtag)
    ops = vm.batch(prog, lane_of, garbage=0)
    regs = max(x for ins in prog if ins[0] not in ("ld", "st", "table", "loop")
               for x in (ins[1:3] if ins[0] in ("shr", "shl") else ins[1:]))
    return ops, vm.keys, regs, prog, vm


# ---------------------------------------------------------------- scaled search
def prefix(seed, group):
    data = hashlib.shake_256(b"s256-bs-prefix|" + seed + struct.pack("<I", group)).digest(52)
    return list(struct.unpack(">13I", data))


def message(words, u):
    return struct.pack(">13I", *words) + struct.pack(">I", (u << 8) | 0x80)[:3]


def digest_words(key):
    """Digest words H2, H3, H5 (bits 0..15 only), H6, H7 from the key."""
    c, d, f, g, h = key & M32, (key >> 32) & M32, (key >> 64) & 0xFFFF, (key >> 80) & M32, (key >> 112) & M32
    return ((IV[2] + c) & M32, (IV[3] + d) & M32, (IV[5] + f) & 0xFFFF, (IV[6] + g) & M32, (IV[7] + h) & M32)


def trial(P, seed, groups, per_group, mask):
    msgs = [(prefix(seed, g), u) for g in range(groups) for u in range(per_group)]
    keys = []
    for s in range(0, len(msgs), 256):
        batch = msgs[s:s + 256]
        ks = P.keys(batch)
        for L in (0, len(batch) - 1):                            # lane self-check
            if ks[L] != scalar_key(batch[L][0], batch[L][1], P.R):
                raise SystemExit("bit-sliced evaluator mismatch")
        keys += ks
    m = (mask[2], mask[3], mask[5] & 0xFFFF, mask[6], mask[7])
    seen, first, pairs = {}, (None, None, 0), 0
    for i, ((w, u), k) in enumerate(zip(msgs, keys)):
        dw = digest_words(k)
        kk = tuple(x & y for x, y in zip(dw, m))
        bucket = seen.setdefault(kk, [])
        if bucket and first[0] is None:
            first = (bucket[0].hex(), message(w, u).hex(), i + 1)
        pairs += len(bucket)
        bucket.append(message(w, u))
    return first[0], first[1], first[2], pairs


def self_check(P, seed):
    w = prefix(seed, 0xFFFFFFFF)
    b = 0x5A5A
    tags = hashlib.shake_256(b"s256-bs-bid|" + seed).digest(29)
    g, rtag = int.from_bytes(tags[:13], "big"), int.from_bytes(tags[13:], "big")
    ops, words, regs, prog, vm = count_batch(P, w, b, g, rtag)
    for L in range(256):
        wd = words[L]
        if (word_key(wd, P.pol) != scalar_key(w, (b << 8) | L, P.R)
                or (wd >> LANE_ROW0) & 0xFF != L or wd >> 255 != 1):
            raise SystemExit("counted program mismatch at lane %d" % L)
    if ops != CLAIMED_BATCH_OPS[P.R] or regs >= NREG or vm.r[R_BID] != bid_word(b + 1, g, rtag):
        raise SystemExit("operation count %d / registers %d differ from the claim" % (ops, regs))
    return ops


def rounds_of(profile):
    return int(profile.split("-r")[1].split("-")[0])


def main():
    request = json.loads(sys.stdin.read())
    R = rounds_of(request["target_profile"])
    P = Program(R)
    groups, per_group = LAYOUT[request["experiment_id"]]
    assert groups * per_group == SAMPLES
    mask = struct.unpack(">8I", bytes.fromhex(request["event"]["mask_hex"]))
    assert mask[0] == 0 and mask[1] == 0 and mask[4] == 0 and mask[5] >> 16 == 0
    out = []
    for item in request["trials"]:
        seed = bytes.fromhex(item["seed"])
        obs = {}
        if item is request["trials"][0]:
            obs["batch_ops"] = self_check(P, seed)
        a, b, first_index, pairs = trial(P, seed, groups, per_group, mask)
        obs.update({"first_match_sample": first_index, "masked_pairs": pairs})
        out.append({"trial": item["trial"], "message_a_hex": a, "message_b_hex": b, "observations": obs})
    sys.stdout.write(json.dumps({"schema_version": 1, "trials": out}, separators=(",", ":")))


if __name__ == "__main__":
    main()
