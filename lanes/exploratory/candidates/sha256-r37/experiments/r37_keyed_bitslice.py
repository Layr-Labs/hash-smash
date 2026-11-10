"""Counted batch program for the sha256-r37 keyed bit-sliced birthday search.

Reads one python-message-pairs-v1 request on stdin and writes one JSON result.
Standard library only; deterministic.  `--ledger` prints the operation ledger.

Pipeline (identical to proof.md):
  1. build(): a bit-sliced Boolean circuit (XOR/AND/OR, complement flags) that
     maps the 272 random message bits of 256 messages (one 256-bit word per
     bit) to 256 key planes Key = (A30, A31, Z32, T1_32, T1_33, T1_34, Y35, X36);
  2. program(): straight-line batch program = circuit + 256x256 transpose +
     per-message key store and high-digit histogram increment;
  3. allocate(): Belady register allocation on NREG general registers with
     every load and store emitted explicitly;
  4. VM: executes the allocated program instruction by instruction and counts
     every executed instruction (one primitive word operation each);
  5. key_to_state(): explicit inverse of the key map; the digest is that state
     plus the IV.  It is a bijection, so key equality == digest equality.
"""
import heapq
import hashlib
import json
import sys

M32 = 0xFFFFFFFF
FULL = (1 << 256) - 1
K = (0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4,
     0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe,
     0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f,
     0x4a7484aa, 0x5cb0a9dc, 0x76f988da, 0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
     0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc,
     0x53380d13, 0x650a7354)
IV = (0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab,
      0x5be0cd19)
PREFIX = 21          # constant zero bytes at message start
RBYTES = 34          # uniformly random bytes; complete message is 55 bytes
MLEN = PREFIX + RBYTES
NIN = 8 * RBYTES     # 272 random planes per batch
NREG = 60            # allocatable registers (4 more hold AP, ARCHP, SP, AEND)
LOOP_OPS = 4         # per batch: AP += 256, ARCHP += 512, compare, branch
MASKS = {s: sum(1 << m for m in range(256) if not m & s) for s in (128, 64, 32, 16, 8, 4, 2, 1)}
LOWMASK = (1 << 128) - 1


# ----------------------------------------------------------------- reference
def ror(x, n):
    return ((x >> n) | (x << (32 - n))) & M32


def S0(a): return ror(a, 2) ^ ror(a, 13) ^ ror(a, 22)
def S1(e): return ror(e, 6) ^ ror(e, 11) ^ ror(e, 25)
def maj(a, b, c): return (a & b) ^ (a & c) ^ (b & c)
def ch(e, f, g): return (e & f) ^ (~e & g & M32)


def pad(msg):
    return msg + b"\x80" + bytes(55 - len(msg)) + (8 * len(msg)).to_bytes(8, "big")


def ref_digest(msg):
    """Independent scalar sha256-r37 of a <=55-byte message (one block)."""
    blk = pad(msg)
    w = [int.from_bytes(blk[4 * i:4 * i + 4], "big") for i in range(16)]
    for t in range(16, 37):
        x, y = w[t - 15], w[t - 2]
        w.append(((ror(y, 17) ^ ror(y, 19) ^ (y >> 10)) + w[t - 7]
                  + (ror(x, 7) ^ ror(x, 18) ^ (x >> 3)) + w[t - 16]) & M32)
    a, b, c, d, e, f, g, h = IV
    for t in range(37):
        t1 = (h + S1(e) + ch(e, f, g) + K[t] + w[t]) & M32
        t2 = (S0(a) + maj(a, b, c)) & M32
        a, b, c, d, e, f, g, h = (t1 + t2) & M32, a, b, c, (d + t1) & M32, e, f, g
    return b"".join(((x + y) & M32).to_bytes(4, "big") for x, y in zip((a, b, c, d, e, f, g, h), IV))


def key_to_digest(k):
    """Inverse key map: (A30,A31,Z32,T1_32,T1_33,T1_34,Y35,X36) -> digest."""
    A30, A31, Z32, t32, t33, t34, Y35, X36 = k
    A = {30: A30, 31: A31, 32: (Z32 + S0(A31)) & M32}
    T2 = lambda j: (S0(A[j]) + maj(A[j], A[j - 1], A[j - 2])) & M32
    A[33] = (t32 + T2(32)) & M32
    A[34] = (t33 + T2(33)) & M32
    A[35] = (t34 + T2(34)) & M32
    E34 = (A30 + t33) & M32
    E35 = (A31 + t34) & M32
    t35 = (Y35 + S1(E35) + K[35]) & M32
    A[36] = (t35 + T2(35)) & M32
    E36 = (A[32] + t35) & M32
    t36 = (X36 + S1(E36) + ch(E36, E35, E34) + K[36]) & M32
    A37 = (t36 + T2(36)) & M32
    E37 = (A[33] + t36) & M32
    st = (A37, A[36], A[35], A[34], E37, E36, E35, E34)
    return b"".join(((x + y) & M32).to_bytes(4, "big") for x, y in zip(st, IV))


def state_to_key(st):
    """Forward map Phi: raw state (A37,A36,A35,A34,E37,E36,E35,E34) -> key."""
    A37, A36, A35, A34, E37, E36, E35, E34 = st
    T2 = lambda x, y, z: (S0(x) + maj(x, y, z)) & M32
    t36 = (A37 - T2(A36, A35, A34)) & M32
    A33 = (E37 - t36) & M32
    t35 = (A36 - T2(A35, A34, A33)) & M32
    A32 = (E36 - t35) & M32
    t34 = (A35 - T2(A34, A33, A32)) & M32
    A31 = (E35 - t34) & M32
    t33 = (A34 - T2(A33, A32, A31)) & M32
    A30 = (E34 - t33) & M32
    t32 = (A33 - T2(A32, A31, A30)) & M32
    Z32 = (A32 - S0(A31)) & M32
    Y35 = (t35 - S1(E35) - K[35]) & M32
    X36 = (t36 - S1(E36) - ch(E36, E35, E34) - K[36]) & M32
    return (A30, A31, Z32, t32, t33, t34, Y35, X36)


def digest_to_state(dg):
    return tuple((int.from_bytes(dg[4 * j:4 * j + 4], "big") - IV[j]) & M32 for j in range(8))


# ------------------------------------------------------------------- circuit
class Circuit:
    """Literals: 2*node + complement flag; literal 0 is FALSE and 1 is TRUE."""

    def __init__(self):
        self.nodes = [("CONST",)]
        self.cse = {}
        self.nin = 0

    def new_input(self):
        self.nodes.append(("IN", self.nin))
        self.nin += 1
        return 2 * (len(self.nodes) - 1)

    def gate(self, op, x, y):
        key = (op, min(x, y), max(x, y))
        n = self.cse.get(key)
        if n is None:
            self.nodes.append(key)
            n = self.cse[key] = len(self.nodes) - 1
        return n

    def xor(self, a, b):
        if a < 2: return b ^ a
        if b < 2: return a ^ b
        if a >> 1 == b >> 1: return (a ^ b) & 1
        return 2 * self.gate("XOR", a >> 1, b >> 1) | ((a ^ b) & 1)

    def and_(self, a, b):
        if a < 2: return b if a else 0
        if b < 2: return a if b else 0
        if a >> 1 == b >> 1: return a if a == b else 0
        if not a & 1 and not b & 1: return 2 * self.gate("AND", a >> 1, b >> 1)
        if a & 1 and b & 1: return 2 * self.gate("OR", a >> 1, b >> 1) | 1
        if a & 1: a, b = b, a                      # a & ~B = a ^ (a & B)
        return self.xor(a, 2 * self.gate("AND", a >> 1, b >> 1))

    def or_(self, a, b):
        return self.and_(a ^ 1, b ^ 1) ^ 1

    def full(self, a, b, c):
        """Sum and carry; 5 gates for three non-constant inputs."""
        lits = [a, b, c]
        for k in lits:
            if k < 2:                                  # constant input: half adder
                rest = list(lits)
                rest.remove(k)
                x, y = rest
                if k == 0:
                    return self.xor(x, y), self.and_(x, y)
                return self.xor(x, y) ^ 1, self.or_(x, y)
        for i, j, p in ((0, 1, 2), (0, 2, 1), (1, 2, 0)):
            if (lits[i] & 1) == (lits[j] & 1):
                x, y, piv = lits[i], lits[j], lits[p]
                break
        t, u = self.xor(x, piv), self.xor(y, piv)     # equal complement flags
        return self.xor(t, y), self.xor(piv, self.and_(t, u))


class ColAdd:
    """Ripple adder evaluated one bit column at a time (LSB first)."""

    def __init__(self, C):
        self.C, self.c, self.i = C, 0, 0

    def step(self, x, y):
        if self.i == 31:
            s = self.C.xor(self.C.xor(x, y), self.c)
        else:
            s, self.c = self.C.full(x, y, self.c)
        self.i += 1
        return s


def build():
    C = Circuit()
    byte_lits = []
    for pos in range(64):
        if pos < PREFIX:
            v = 0
        elif pos < MLEN:
            byte_lits.append([C.new_input() for _ in range(8)])
            continue
        elif pos == MLEN:
            v = 0x80
        else:
            v = (8 * MLEN).to_bytes(8, "big")[pos - 56]
        byte_lits.append([(v >> k) & 1 for k in range(8)])
    W = [[byte_lits[4 * i + 3 - j // 8][j % 8] for j in range(32)] for i in range(16)]
    A = {-j: [(IV[j] >> i) & 1 for i in range(32)] for j in range(4)}
    E = {-j: [(IV[4 + j] >> i) & 1 for i in range(32)] for j in range(4)}
    T1 = {}
    for t in range(37):
        e, f, g, h = E.get(t), E.get(t - 1), E.get(t - 2), E.get(t - 3)
        a, b, c, d = A.get(t), A.get(t - 1), A.get(t - 2), A.get(t - 3)
        ad = [ColAdd(C) for _ in range(8)]
        wad = [ColAdd(C) for _ in range(3)]
        ow, ot1, oa, oe, oy = [], [], [], [], []
        for i in range(32):
            if t >= 16:
                p, q = W[t - 2], W[t - 15]
                s1 = C.xor(C.xor(p[(i + 17) % 32], p[(i + 19) % 32]), p[i + 10] if i < 22 else 0)
                s0 = C.xor(C.xor(q[(i + 7) % 32], q[(i + 18) % 32]), q[i + 3] if i < 29 else 0)
                wi = wad[2].step(wad[1].step(wad[0].step(W[t - 16][i], W[t - 7][i]), s0), s1)
                ow.append(wi)
            else:
                wi = W[t][i]
            if t <= 34:
                sig = C.xor(C.xor(e[(i + 6) % 32], e[(i + 11) % 32]), e[(i + 25) % 32])
                chi = C.xor(g[i], C.and_(e[i], C.xor(f[i], g[i])))
                t1 = ad[3].step(ad[2].step(ad[1].step(ad[0].step(wi, (K[t] >> i) & 1), h[i]), sig), chi)
                ot1.append(t1)
                oe.append(ad[4].step(d[i], t1))
                if t <= 31:
                    mj = C.xor(b[i], C.and_(C.xor(a[i], b[i]), C.xor(b[i], c[i])))
                    if t <= 30:
                        sg0 = C.xor(C.xor(a[(i + 2) % 32], a[(i + 13) % 32]), a[(i + 22) % 32])
                        mj = ad[5].step(sg0, mj)
                    oa.append(ad[6].step(t1, mj))
            elif t == 35:   # Y35 = E32 + W35 + Ch(E35, E34, E33)
                chi = C.xor(g[i], C.and_(e[i], C.xor(f[i], g[i])))
                oy.append(ad[1].step(ad[0].step(h[i], wi), chi))
            else:           # X36 = E33 + W36
                oy.append(ad[0].step(h[i], wi))
        if t >= 16:
            W.append(ow)
        if t <= 34:
            T1[t], E[t + 1] = ot1, oe
            if t <= 31:
                A[t + 1] = oa
        elif t == 35:
            Y35 = oy
        else:
            X36 = oy
    return C, [A[30], A[31], A[32], T1[32], T1[33], T1[34], Y35, X36]


# ------------------------------------------------------------- batch program
def program(C, key):
    """Virtual straight-line program. op = (opc, dst, src1, src2, imm)."""
    ops, kinds, nv = [], {}, [0]

    def new(kind):
        nv[0] += 1
        kinds[nv[0]] = kind
        return nv[0]

    live, st = set(), [l >> 1 for w in key for l in w]
    while st:
        n = st.pop()
        if n not in live:
            live.add(n)
            if C.nodes[n][0] in ("XOR", "AND", "OR"):
                st += [C.nodes[n][1], C.nodes[n][2]]
    vn, pending = {}, {}
    for n in sorted(live):
        nd = C.nodes[n]
        if nd[0] == "IN":       # drawn lazily just before first use
            vn[n] = new(("in", nd[1]))
            pending[vn[n]] = [("RAND", vn[n], None, None, None), ("STARCH", None, vn[n], None, nd[1])]
        else:
            for s in (vn[nd[1]], vn[nd[2]]):
                ops.extend(pending.pop(s, ()))
            vn[n] = new("g")
            ops.append((nd[0], vn[n], vn[nd[1]], vn[nd[2]], None))
    assert not pending
    rows, pol = [], 0
    for wi, w in enumerate(key):
        for b, l in enumerate(w):
            rows.append(vn[l >> 1])
            pol |= (l & 1) << (32 * wi + b)
    mreg = {s: new(("const", "M%d" % s)) for s in MASKS}

    def dswap(r, s):
        x, y = rows[r], rows[r + s]
        t0, t1, t2, y2, t3, x2 = (new("t") for _ in range(6))
        ops.extend([("SHR", t0, x, None, s), ("XOR", t1, t0, y, None), ("AND", t2, t1, mreg[s], None),
                    ("XOR", y2, y, t2, None), ("SHL", t3, t2, None, s), ("XOR", x2, x, t3, None)])
        rows[r], rows[r + s] = x2, y2

    for r0 in range(32):
        for s in (128, 64, 32):
            for r in range(r0, 256, 32):
                if not r & s:
                    dswap(r, s)
    for blk in range(8):
        for s in (16, 8, 4, 2, 1):
            for r in range(32 * blk, 32 * blk + 32):
                if not r & s:
                    dswap(r, s)
        for r in range(32 * blk, 32 * blk + 32):
            y, d, c0, c1 = rows[r], new("t"), new("t"), new("t")
            ops.extend([("STA", None, y, None, r), ("SHR", d, y, None, 128), ("LDI", c0, d, None, None),
                        ("ADDI", c1, c0, None, 1), ("STI", None, c1, d, None)])
    return ops, kinds, pol


def srcs(op):
    o = op[0]
    if o == "RAND": return ()
    if o == "STI": return (op[2], op[3])
    if o in ("STARCH", "STA", "SHR", "SHL", "ADDI", "LDI"): return (op[2],)
    return (op[2], op[3])


def allocate(ops, kinds, nreg=NREG):
    """Belady (furthest next use) allocation; returns physical program."""
    INF = 1 << 60
    uses = {}
    for i, op in enumerate(ops):
        for s in srcs(op):
            uses.setdefault(s, []).append(i)
    ptr = dict.fromkeys(uses, 0)

    def nxt(v, i):
        u = uses.get(v, ())
        p = ptr.get(v, 0)
        while p < len(u) and u[p] <= i:
            p += 1
        if v in ptr:
            ptr[v] = p
        return u[p] if p < len(u) else INF

    reg, free, heap, phys, home = {}, list(range(nreg)), [], [], {}
    inmem = {v for v, k in kinds.items() if k[0] == "const"}

    def slot(v):
        k = kinds[v]
        if k[0] == "in": return ("ARCH", k[1])
        if k[0] == "const": return ("CONST", k[1])
        return home.setdefault(v, ("SPILL", len(home)))

    def getreg(i, locked):
        if free:
            return free.pop()
        stash = []
        while True:
            neg, v = heapq.heappop(heap)
            if v not in reg:
                continue
            nu = nxt(v, i - 1)
            if -neg != nu:
                heapq.heappush(heap, (-nu, v))
                continue
            if v in locked:
                stash.append((neg, v))
                continue
            break
        for e in stash:
            heapq.heappush(heap, e)
        r = reg.pop(v)
        if nu < INF and v not in inmem:
            phys.append(("ST", r, slot(v)))
            inmem.add(v)
        return r

    for i, op in enumerate(ops):
        ss = srcs(op)
        for s in ss:
            if s not in reg:
                r = getreg(i, set(ss))
                phys.append(("LD", r, slot(s)))
                reg[s] = r
            heapq.heappush(heap, (-nxt(s, i), s))
        sregs = [reg[s] for s in ss]
        for s in set(ss):
            if nxt(s, i) == INF:
                free.append(reg.pop(s))
        rd = None
        if op[1] is not None:
            rd = getreg(i + 1, set())
            reg[op[1]] = rd
            heapq.heappush(heap, (-nxt(op[1], i), op[1]))
        phys.append((op[0], rd, sregs, op[4]))
        if op[0] == "STARCH":
            inmem.add(op[2])
        if op[1] is not None and nxt(op[1], i) == INF:
            free.append(reg.pop(op[1]))
    return phys, len(home)


# ------------------------------------------------------------------------ VM
AP, ARCHP, SP, AEND = NREG, NREG + 1, NREG + 2, NREG + 3
CONSTS = ["M%d" % s for s in MASKS]
CONSTV = [MASKS[s] for s in MASKS]
A_BASE, ARCH_BASE, SP_BASE = 1 << 130, 1 << 132, 1 << 133   # proof.md memory map


def vm_batch(phys, mem, regs, rand):
    """Execute one batch; every executed instruction counts as one operation."""
    def addr(sl):
        if sl[0] == "ARCH": return regs[ARCHP] + sl[1]
        if sl[0] == "CONST": return regs[SP] + CONSTS.index(sl[1])
        return regs[SP] + 16 + sl[1]
    n = 0
    for ins in phys:
        o = ins[0]
        n += 1
        if o == "LD": regs[ins[1]] = mem.get(addr(ins[2]), 0)
        elif o == "ST": mem[addr(ins[2])] = regs[ins[1]]
        else:
            rd, s, imm = ins[1], ins[2], ins[3]
            if o == "XOR": regs[rd] = regs[s[0]] ^ regs[s[1]]
            elif o == "AND": regs[rd] = regs[s[0]] & regs[s[1]]
            elif o == "OR": regs[rd] = regs[s[0]] | regs[s[1]]
            elif o == "SHR": regs[rd] = regs[s[0]] >> imm
            elif o == "SHL": regs[rd] = (regs[s[0]] << imm) & FULL
            elif o == "RAND": regs[rd] = rand()
            elif o == "STARCH": mem[regs[ARCHP] + imm] = regs[s[0]]
            elif o == "STA": mem[regs[AP] + imm] = regs[s[0]]
            elif o == "LDI": regs[rd] = mem.get(regs[s[0]], 0)
            elif o == "ADDI": regs[rd] = (regs[s[0]] + imm) & FULL
            elif o == "STI": mem[regs[s[1]]] = regs[s[0]]
            else: raise ValueError(o)
    regs[AP] += 256          # loop control: two pointer additions,
    regs[ARCHP] += 512       # one comparison of AP with AEND and one branch
    return n + LOOP_OPS


# ------------------------------------------------------- fast evaluator
def eval_planes(C, key, planes):
    val = [0] * len(C.nodes)
    for n, nd in enumerate(C.nodes):
        o = nd[0]
        if o == "IN": val[n] = planes[nd[1]]
        elif o == "XOR": val[n] = val[nd[1]] ^ val[nd[2]]
        elif o == "AND": val[n] = val[nd[1]] & val[nd[2]]
        elif o == "OR": val[n] = val[nd[1]] | val[nd[2]]
    return [val[l >> 1] ^ (FULL if l & 1 else 0) for w in key for l in w]


def keys_from_planes(rows):
    """Lane m of the result has bit i = bit m of rows[i]: the same delta-swap
    transpose as the counted program, evaluated directly."""
    rows = list(rows)
    for s in (128, 64, 32, 16, 8, 4, 2, 1):
        mk = MASKS[s]
        for r in range(256):
            if not r & s:
                t = ((rows[r] >> s) ^ rows[r + s]) & mk
                rows[r + s] ^= t
                rows[r] ^= (t << s) & FULL
    return rows


def split_key(kw):
    return tuple((kw >> (32 * j)) & M32 for j in range(8))


def message_of_lane(planes, m):
    """Complete 55-byte message of lane m: random byte r has bit k in plane 8r+k."""
    return bytes(PREFIX) + bytes(sum(((planes[8 * r + k] >> m) & 1) << k for k in range(8))
                                 for r in range(RBYTES))


class Stream:
    def __init__(self, seed_hex):
        self.seed, self.ctr, self.buf = bytes.fromhex(seed_hex), 0, b""

    def __call__(self):
        while len(self.buf) < 32:
            self.buf += hashlib.shake_256(self.seed + self.ctr.to_bytes(8, "big")).digest(4096)
            self.ctr += 1
        w, self.buf = int.from_bytes(self.buf[:32], "big"), self.buf[32:]
        return w


def setup():
    C, key = build()
    ops, kinds, pol = program(C, key)
    phys, nspill = allocate(ops, kinds)
    return C, key, phys, pol, nspill


def ledger(phys):
    cnt = {}
    for ins in phys:
        cnt[ins[0]] = cnt.get(ins[0], 0) + 1
    cnt["LOOP"] = LOOP_OPS
    cnt["TOTAL"] = len(phys) + LOOP_OPS
    return cnt


def witness_batch(C, key, phys, pol, seed_hex):
    """Run the counted program on one batch and check every lane."""
    mem, regs = {}, [0] * (NREG + 4)
    regs[AP], regs[ARCHP], regs[SP], regs[AEND] = A_BASE, ARCH_BASE, SP_BASE, A_BASE + 256
    for i, v in enumerate(CONSTV):
        mem[SP_BASE + i] = v
    ops = vm_batch(phys, mem, regs, Stream(seed_hex))
    planes = [mem[ARCH_BASE + j] for j in range(NIN)]
    msgs = [message_of_lane(planes, m) for m in range(256)]
    bad = 0
    hist = {}
    for m in range(256):
        kw = mem[A_BASE + m] ^ pol                     # complement flags removed
        rd = ref_digest(msgs[m])
        bad += key_to_digest(split_key(kw)) != rd
        bad += state_to_key(digest_to_state(rd)) != split_key(kw)
        hist[mem[A_BASE + m] >> 128] = hist.get(mem[A_BASE + m] >> 128, 0) + 1
    bad += any(mem.get(d, 0) != c for d, c in hist.items())
    fast = keys_from_planes(eval_planes(C, key, planes))
    bad += sum(fast[m] != mem[A_BASE + m] ^ pol for m in range(256))
    return ops, bad


def run(request):
    C, key, phys, pol, _ = setup()
    batch_ops = len(phys) + LOOP_OPS
    mask = int(request["event"]["mask_hex"], 16)
    out = []
    for tr in request["trials"]:
        obs = {"batch_ops": batch_ops}
        if tr["trial"] == 0:
            ops, bad = witness_batch(C, key, phys, pol, tr["seed"])
            obs["vm_executed_ops"] = ops
            obs["vm_lane_mismatches"] = bad
        rnd = Stream(tr["seed"])
        planes = [rnd() for _ in range(NIN)]
        keys = keys_from_planes(eval_planes(C, key, planes))
        seen, pair = {}, (None, None)
        for m in range(256):
            dg = int.from_bytes(key_to_digest(split_key(keys[m])), "big") & mask
            if dg in seen:
                ma, mb = message_of_lane(planes, seen[dg]), message_of_lane(planes, m)
                if ma != mb:
                    pair = (ma.hex(), mb.hex())
                    break
            seen.setdefault(dg, m)
        out.append({"trial": tr["trial"], "message_a_hex": pair[0], "message_b_hex": pair[1],
                    "observations": obs})
    return {"schema_version": 1, "trials": out}


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--ledger":
        C, key, phys, pol, nspill = setup()
        g = sum(1 for nd in C.nodes if nd[0] in ("XOR", "AND", "OR"))
        print(json.dumps({"circuit_gates_built": g, "spill_slots": nspill, **ledger(phys)}, sort_keys=True))
        print(json.dumps(witness_batch(C, key, phys, pol, "00" * 32)))
    else:
        json.dump(run(json.load(sys.stdin)), sys.stdout, sort_keys=True, separators=(",", ":"))
