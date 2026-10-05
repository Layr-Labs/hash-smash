#!/usr/bin/env python3
"""blake3-r1 zero-digest collision pair: constructor, op counter, liveness.

Reads the organizer request JSON on stdin, prints one strict JSON document
on stdout: for every organizer trial, the constructed message pair plus
numeric observations reporting this program's own operation ledger and
register liveness. Stdlib only; fully deterministic; no randomness, no
branches on hash values, no compression evaluations, no external data.

The construction is the one proved in proof.md: Lemma-2 column solves and
Lemma-1 diagonal solves for message M (all-zero targets) and companion M'
(Gd0' target (1,1), Gd2' runtime target taken from Gd0' own A/B outputs,
column compensations K = 0xFE0000FD and L = 0xFE180100, the closed forms of
the design point (C0, D0) = (1, 1)).
"""
import json
import struct
import sys

MASK = 0xFFFFFFFF
IV = [0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
      0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19]


class Prog:
    """Straight-line program recorder with the exact per-step charge."""

    def __init__(self):
        self.vals = {}
        self.cse = {}
        self.ops_exec = 0      # charged unit ops (masked add/sub cost 2)
        self.instrs = []       # executed instructions: (op, a_desc, b_desc, out_desc)
        self.consts = set()

    def C(self, v):
        v &= MASK
        if v:
            self.consts.add(v)
        return ('L', v)

    def op(self, o, a, b):
        cost = 2 if o in ('addm', 'subm') else 1
        va = a[1] if a[0] == 'L' else self.vals[a[1]]
        vb = b[1] if b[0] == 'L' else self.vals[b[1]]
        key = (o, a, b)
        if key in self.cse:
            t = self.cse[key]
            return t if isinstance(t, tuple) else ('V', t)
        if o == 'shl':
            r = (va << vb) & MASK
        elif o == 'shr':
            r = va >> vb
        elif o == 'addm':
            r = (va + vb) & MASK
        elif o == 'subm':
            r = (va - vb) & MASK
        else:
            r = {'xor': va ^ vb, 'or': va | vb, 'and': va & vb}[o]
        self.ops_exec += cost
        if r == 0:
            self.cse[key] = self.C(0)
            self.instrs.append((o, a, b, ('L', 0)))
            return self.C(0)
        name = "r%d" % self.ops_exec
        self.vals[name] = r
        self.cse[key] = name
        self.instrs.append((o, a, b, ('V', name)))
        return ('V', name)

    def add(self, a, b):
        if a[0] == 'L' and a[1] == 0:
            return b
        if b[0] == 'L' and b[1] == 0:
            return a
        return self.op('addm', a, b)

    def sub(self, a, b):
        if b[0] == 'L' and b[1] == 0:
            return a
        return self.op('subm', a, b)

    def xor(self, a, b):
        if a[0] == 'L' and a[1] == 0:
            return b
        if b[0] == 'L' and b[1] == 0:
            return a
        return self.op('xor', a, b)

    def rot(self, x, k):  # rotate-left by k (1..31): 4 ops; rot(0) folds
        if x[0] == 'L' and x[1] == 0:
            return self.C(0)
        lo = self.op('shl', x, self.C(k))
        hi = self.op('shr', x, self.C(32 - k))
        o = self.op('or', lo, hi)
        return self.op('and', o, self.C(MASK))


def column(P, IVs, k, Bt, Ct, d):
    """Lemma 2: solve G(k,k+4,k+8,k+12) for outputs (B, C) = (Bt, Ct)."""
    a, b, c = IVs[k], IVs[(k + 4) % 8], IVs[k]
    b1 = P.xor(P.rot(Bt, 7), Ct)
    c1 = P.xor(b, P.rot(b1, 12))
    d1 = P.sub(c1, c)
    D = P.sub(Ct, c1)
    a1 = P.xor(d, P.rot(d1, 16))
    x = P.sub(P.sub(a1, a), b)
    A = P.xor(P.rot(D, 8), d1)
    y = P.sub(P.sub(A, a1), b1)
    return x, y, A, D


def diag(P, a, b, c, d, Ct, Dt):
    """Lemma 1: solve diagonal G for outputs (C, D) = (Ct, Dt)."""
    c1 = P.sub(Ct, Dt)
    d1 = P.sub(c1, c)
    a1 = P.xor(d, P.rot(d1, 16))
    x = P.sub(P.sub(a1, a), b)
    b1 = P.rot(P.xor(b, c1), 20)   # ror(...,12) == rol(...,20)
    A = P.xor(P.rot(Dt, 8), d1)
    y = P.sub(P.sub(A, a1), b1)
    B = P.rot(P.xor(b1, Ct), 25)   # ror(...,7)  == rol(...,25)
    return x, y, A, B


def construct():
    """Emit the two-message straight-line program; return word values."""
    P = Prog()
    IVs = [P.C(x) for x in IV]
    Z = P.C(0)
    l64 = P.C(64)
    l11 = P.C(11)
    C0, D0 = P.C(1), P.C(1)
    # Design-time closed forms of (C0, D0) = (1, 1), as immediates:
    #   c1 = C0 - D0 = 0;  A0 = rol8(D0) ^ c1 = 0x00000100
    #   b1 = ror12(c1) = 0;  B0 = ror7(b1 ^ C0) = 0x02000000
    #   K = (A0 - B0) - (C0 ^ rol8(B0)) = 0xFE0000FD   (column-0 C target)
    #   L = rol12(rol7(D0) ^ A0) ^ (A0 - B0) = 0xFE180100  (column-3 B target)
    K = P.C(0xFE0000FD)
    L = P.C(0xFE180100)
    # message M: zero-target columns, then zero-target diagonals
    w1 = [None] * 16
    cols = [column(P, IVs, k, Z, Z, d) for k, d in enumerate([Z, Z, l64, l11])]
    for k in range(4):
        w1[2 * k], w1[2 * k + 1] = cols[k][0], cols[k][1]
    Aout = [c[2] for c in cols]
    Dout = [c[3] for c in cols]
    dg = [diag(P, Aout[j], Z, Z, Dout[(j + 3) % 4], Z, Z) for j in range(4)]
    for j in range(4):
        w1[8 + 2 * j], w1[9 + 2 * j] = dg[j][0], dg[j][1]
    # companion M': compensated columns 0 and 3; columns 1, 2 shared via CSE
    w2 = [None] * 16
    c2 = [column(P, IVs, k, (L if k == 3 else Z), (K if k == 0 else Z), d)
          for k, d in enumerate([Z, Z, l64, l11])]
    for k in range(4):
        w2[2 * k], w2[2 * k + 1] = c2[k][0], c2[k][1]
    g0 = diag(P, c2[0][2], Z, Z, c2[3][3], C0, D0)
    g1 = diag(P, c2[1][2], Z, Z, c2[0][3], Z, Z)
    g2 = diag(P, c2[2][2], L, K, c2[1][3], g0[2], g0[3])
    g3 = diag(P, c2[3][2], Z, Z, c2[2][3], Z, Z)
    for j, g in enumerate((g0, g1, g2, g3)):
        w2[8 + 2 * j], w2[9 + 2 * j] = g[0], g[1]
    return P, w1, w2


def liveness(P, W1, W2):
    """Peak simultaneously-live values over the emitted instruction order."""
    lastu = {}
    for i, (o, a, b, r) in enumerate(P.instrs):
        for d in (a, b):
            if d[0] == 'V':
                lastu[d[1]] = i
    # every produced word is consumed by one output store at the end
    final = len(P.instrs) + 1
    created = {}
    for i, (o, a, b, r) in enumerate(P.instrs):
        if r[0] == 'V' and r[1] not in created:
            created[r[1]] = i
    for t in list(W1) + list(W2):
        if t[0] == 'V':
            lastu[t[1]] = final
    events = [(ci, 1) for ci in created.values()]
    events += [(lastu.get(name, ci), -1) for name, ci in created.items()]
    events.sort(key=lambda e: (e[0], -e[1]))
    cur = peak = 0
    for _t, d in events:
        cur += d
        if d == 1 and cur > peak:
            peak = cur
    return len(created), peak


def main():
    P, w1, w2 = construct()
    request = json.loads(sys.stdin.read())
    regs, peak_live = liveness(P, w1, w2)
    resolve = lambda t: t[1] if t[0] == 'L' else P.vals[t[1]]
    W1 = [resolve(t) for t in w1]
    W2 = [resolve(t) for t in w2]
    a = struct.pack("<16I", *W1)
    b = struct.pack("<16I", *W2)
    observations = {
        "data-path-ops": P.ops_exec,               # charged ALU ledger (203)
        "data-path-instrs": len(P.instrs),         # emitted instruction count
        "packing-ops-256bit": 112,                 # 2 msgs x 4 words x 7 merges x (shl, or)
        "stores-256bit": 8,                        # 2 x 64-byte messages, 8 words
        "charged-total-packed": P.ops_exec + 120,  # primary ledger (323)
        "stores-32bit": 32,
        "charged-total-word-stores": P.ops_exec + 32,
        "allocated-registers": regs,
        "peak-live-values": peak_live,
        "differing-words": sum(1 for x, y in zip(W1, W2) if x != y),
        "immediate-constants": len(P.consts),
    }
    out = {"schema_version": 1, "trials": [
        {"trial": row["trial"],
         "message_a_hex": a.hex(),
         "message_b_hex": b.hex(),
         "observations": dict(observations)}
        for row in request["trials"]]}
    sys.stdout.write(json.dumps(out, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
