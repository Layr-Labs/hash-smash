"""LS1: distinguished-point collision search on sha3-256-r6-prefix-v1 with a linear-structure message embedding.

Chain function on 256-bit points u (little-endian lanes u0..u3):
  m(u) = 128 bytes = lanes 0..15 of the absorbed state: lane 1 = u0^K1, lane 6 = u1^K6, lane 11 = u0^u1^K11,
  lane 4 = u2, lane 9 = u3, lane 14 = u2^u3^K14, the other lanes 0..15 the constants K below; padding gives lane 16 =
  0x8000000000000006.  F(u) = SHA3-256-r6(m(u)) XOR PD (PD a fixed 256-bit mask).  m is injective, so F(u) = F(u') with
  u != u' gives two distinct messages with equal complete digests.
This program regenerates the bit-sliced straight line of proof.md Section 3 (the same algorithm and node order as the C
generator gen3.c, with the generator's decisions PLAN: constants trial, round-1 and theta complements, free term
polarities; its 5-byte encoding must hash to PROG_SHA256), assembles and checks the revised 2,715-instruction control
image and 14-instruction prefilter, checks the straight line against a plain 6-round implementation, and runs
  rho-w22   : the search of proof.md Section 4 at width 22 (planes 22..255 zeroed after each step), one pair per trial;
              the table keeps the trail number of each end; the replay measures the stored trail by walking it;
  proj-w256 : eight chained full-width steps from 256 random points, first pair agreeing on the 22 low digest bits.
One Python integer holds a plane for all trials of the request (trial t in bits 256t..256t+255); trials never interact.
"""
import sys, json, hashlib

M64 = (1 << 64) - 1
RCA = [0x1, 0x8082, 0x800000000000808A, 0x8000000080008000, 0x808B, 0x80000001, 0x8000000080008081, 0x8000000000008009,
       0x8A, 0x88, 0x80008009, 0x8000000A, 0x8000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003,
       0x8000000000008002, 0x8000000000000080, 0x800A, 0x800000008000000A, 0x8000000080008081, 0x8000000000008080,
       0x80000001, 0x8000000080008008]
ROT = [[0, 36, 3, 41, 18], [1, 44, 10, 45, 2], [62, 6, 43, 15, 61], [28, 55, 25, 21, 56], [27, 20, 39, 8, 14]]
NR = 6                         # rounds of the target
PLAN = """
trial 0
nr 6 optmode 3 trick 1 lasttrick 1 notfold 0
F1 ffffffffff8ffeff0100000000000000000000000018010000000000000000000200000000d00000
G1 00000000000000000000000000000000000000000000000000000000000000000000000000000000
FG 2 000000480000809000000005000000128400001020000000000006211280200818c22000438c0211 60800a58188860100000044050800300600c410000001082002888400003108c0000000180020480
FG 3 0a0a8011020000000001092d0440204801020002285082084000004010042001070c0400500c0022 081040000819100200e080204180008510000a0023810000a800020000818008004000a002184069
FG 4 0804800004081d444000300046004000400040000000040001000501407000050290008000000010 000010a088301184810400000801200c80040200040ac61010000016024001809510280808008000
FG 5 00000000000400000000000000000000000000020000100800000000010200000004000000000200 90000080000000040000000000812002000000000000401002000000180200000120204020081020
PHI 0 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
PHI 1 0000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
PHI 2 0000000000000000000100000000000000000000000002000040000000002000000001000020008000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000080000200022100000008000000000000804000000000000000000400004000004000001000000000000000000000000000000000000001000000000002000004000000800000000000000000000000000000000
PHI 3 0010010000000000010000000000000800000000000000000000000000000000000000080000000000000000040000002020000000000001000000000000020002000000000000000000000000000000000000000000000300000000000100000000000000000000000040000018000000010000800000080000000000000000010000000000000000000000000000000008000000000000000008000000000000000000000000000000000100000000000000001000000001000200000000000000000000000000
PHI 4 0000000000000000000004000000000100000000000000000420000000400000000000000000000000000000000800000000000000000000000080000000000000000001000000000000000080000000000048000000000000000000000000000000000000000000000000040000000000040000000000000000000000080040000000000000800000000000000000000000001000010000001000000000000000000000000000000000001000000000000000000000008000000000000000000000000080000000
PHI 5 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
"""
PL = {}
for _ln in PLAN.strip().split("\n"):
    _t = _ln.split()
    if _t[0] in ("trial", "F1", "G1"): PL[_t[0]] = _t[1]
    elif _t[0] == "FG": PL[("FG", int(_t[1]))] = (_t[2], _t[3])
    elif _t[0] == "PHI": PL[("PHI", int(_t[1]))] = _t[2]
TRIAL = int(PL["trial"])            # constants of the generator's selected trial
PROG_SHA256 = "16ea87a20539b4d91eb0f7dcfdc575cded1b8d2c0a0b10a51abcc1b8f2ee1460"
NINSTR = 26570
NREG = 2304
NC = -1
O_IN, O_XOR, O_AND, O_OR, O_NOT = 0, 1, 2, 3, 4


def consts(trial):
    # the fixed annihilating constant set 56 (every trial of the generator uses it); lane 16 = padding
    K = [0x0000000000000000, 0xffffffffffffffff, 0xffffffffffffffff, 0x0000000000000000, 0xffffffffffffffff, 0xffffffffffffffff, 0x8000000000000006, 0x0000000000000000, 0x0000000000000000, 0x0000000000000000, 0xffffffffffffffff, 0x0000000000000000, 0x0000000000000000, 0xffffffffffffffff, 0xffffffffffffffff, 0xffffffffffffffff] + [0] * 9
    K[16] = 0x8000000000000006
    return K


KL = consts(TRIAL)


# ---------------- generator (same algorithm and node order as gen.c) ----------------
class Gen:
    def __init__(self):
        self.op, self.a, self.b, self.k, self.lin = [], [], [], [], []
        self.form, self.fidx, self.cons = [], {}, {}

    def new(self, op, a, b):
        self.op.append(op); self.a.append(a); self.b.append(b); self.k.append(0); self.lin.append(-1)
        return len(self.op) - 1

    def consn(self, op, a, b):
        if op != O_NOT and a > b: a, b = b, a
        key = (op, a, b)
        n = self.cons.get(key)
        if n is None:
            n = self.new(op, a, b); self.cons[key] = n
        return n

    def fadd(self, m, node):
        f = len(self.form); self.form.append((m, node)); self.fidx[m] = f
        return f

    def xorv(self, a, b):
        if a[0] == NC: return (b[0], b[1] ^ a[1])
        if b[0] == NC: return (a[0], a[1] ^ b[1])
        if a[0] == b[0]: return (NC, a[1] ^ b[1])
        la, lb = self.lin[a[0]], self.lin[b[0]]
        if la >= 0 and lb >= 0:
            m = self.form[la][0] ^ self.form[lb][0]
            kk = self.k[a[0]] ^ self.k[b[0]]
            if m == 0: return (NC, kk ^ a[1] ^ b[1])
            f = self.fidx.get(m)
            if f is not None:
                n3 = self.form[f][1]
                return (n3, kk ^ a[1] ^ b[1] ^ self.k[n3])
            n = self.new(O_XOR, min(a[0], b[0]), max(a[0], b[0]))
            self.k[n] = kk; self.lin[n] = self.fadd(m, n)
            return (n, a[1] ^ b[1])
        return (self.consn(O_XOR, a[0], b[0]), a[1] ^ b[1])

    def notv(self, a):
        if a[0] == NC: return a
        before = len(self.op)
        n = self.consn(O_NOT, a[0], 0)
        if len(self.op) > before and self.lin[a[0]] >= 0:
            self.lin[n] = self.lin[a[0]]; self.k[n] = self.k[a[0]] ^ 1
        return (n, a[1] ^ 1)

    def and2(self, a, b, sel=0):
        """logical a AND b; a mixed-polarity term is A ^ (A & B) (polarity 0) or, with sel, (NOT A) | B (polarity 1)"""
        if a[0] == NC: return b if a[1] else (NC, 0)
        if b[0] == NC: return a if b[1] else (NC, 0)
        if a[0] == b[0]: return a if a[1] == b[1] else (NC, 0)
        if a[1] == 0 and b[1] == 0: return (self.consn(O_AND, a[0], b[0]), 0)
        if a[1] == 1 and b[1] == 1: return (self.consn(O_OR, a[0], b[0]), 1)
        A, B = (a[0], b[0]) if a[1] == 0 else (b[0], a[0])
        if sel:
            na = self.notv((A, 0))
            return (self.consn(O_OR, na[0], B), 1)
        t = self.consn(O_AND, A, B)
        return self.xorv((A, 0), (t, 0))


def cost_term(b1, b2):
    if b1[0] == NC or b2[0] == NC or b1[0] == b2[0]: return 0
    return 1 if (b1[1] ^ 1) == b2[1] else 2


def row_choose(b, need):
    """the row decision of gen3.c: complement subset s and 10-gate position j (-1: none), first cheapest"""
    distinct = all(v[0] != NC for v in b) and len(set(v[0] for v in b)) == 5
    best, bc, bj = -1, 1 << 30, -1
    for j in range(-1, 5 if distinct else 0):
        if j >= 0 and not ((need >> j) & 1 and (need >> ((j + 1) % 5)) & 1): continue
        for s in range(32):
            c = 0; bb = list(b)
            for X in range(5):
                if s >> X & 1:
                    if b[X][0] == NC: c = 1 << 29
                    else: bb[X] = (b[X][0], b[X][1] ^ 1); c += 1
            for X in range(5):
                if need >> X & 1:
                    if X == j:
                        k = (j + 1) % 5; p1, p2 = bb[(k + 1) % 5], bb[(k + 2) % 5]
                        if (p1[1] ^ 1) == p2[1]: c += cost_term((bb[k][0], bb[k][1] ^ (p1[1] ^ 1)), bb[(X + 2) % 5])
                        else: c += 1                                   # mixed term k: its output polarity is free
                    else: c += cost_term(bb[(X + 1) % 5], bb[(X + 2) % 5])
            if c < bc: bc, best, bj = c, s, j
    return best, bj


TAB = {}
for _L in (0, 1):
    for _p in range(32):
        TAB[(_L, _p)] = row_choose([(X, (_p >> X) & 1) for X in range(5)], 0x0F if _L else 0x1F)


def bits(h, n):
    v = int.from_bytes(bytes.fromhex(h), "little")
    return [(v >> i) & 1 for i in range(n)]


def build():
    g = Gen()
    for j in range(256):
        n = g.new(O_IN, 0, 0); g.lin[n] = g.fadd(1 << j, n)
    S = [[(NC, (KL[l] >> z) & 1) for z in range(64)] for l in range(25)]
    for z in range(64):
        S[1][z] = (z, (KL[1] >> z) & 1); S[6][z] = (64 + z, (KL[6] >> z) & 1)
        S[4][z] = (128 + z, (KL[4] >> z) & 1); S[9][z] = (192 + z, (KL[9] >> z) & 1)
    for z in range(64):
        S[11][z] = g.xorv(g.xorv((z, 0), (64 + z, 0)), (NC, (KL[11] >> z) & 1))
        S[14][z] = g.xorv(g.xorv((128 + z, 0), (192 + z, 0)), (NC, (KL[14] >> z) & 1))
    for r in range(NR):
        last = r == NR - 1
        if r == 1: ff, gg = bits(PL["F1"], 320), bits(PL["G1"], 320)
        elif r >= 2: ff, gg = bits(PL[("FG", r)][0], 320), bits(PL[("FG", r)][1], 320)
        else: ff = gg = [0] * 320
        phi = bits(PL[("PHI", r)], 1600)
        C = [[None] * 64 for _ in range(5)]
        D_ = [[None] * 64 for _ in range(5)]
        for x in range(5):
            s = S[x][63]
            for y in range(1, 5): s = g.xorv(s, S[x + 5 * y][63])
            C[x][63] = g.notv(s) if gg[x * 64 + 63] else s
        for z in range(64):
            if z < 63:
                for x in range(5):
                    s = S[x][z]
                    for y in range(1, 5): s = g.xorv(s, S[x + 5 * y][z])
                    C[x][z] = g.notv(s) if gg[x * 64 + z] else s
            for x in range(5):
                D_[x][z] = g.xorv(C[(x + 4) % 5][z], C[(x + 1) % 5][(z + 63) & 63])
                if ff[x * 64 + z]: D_[x][z] = g.notv(D_[x][z])
        NS = [row[:] for row in S]
        nY, need = (1, 0x0F) if last else (5, 0x1F)
        for Y in range(nY):
            for z in range(64):
                b = []
                for X in range(5):
                    y, x = X, (3 * Y + X) % 5
                    zz = (z - ROT[x][y]) & 63
                    b.append(g.xorv(S[x + 5 * y][zz], D_[x][zz]))
                if all(v[0] != NC for v in b) and len(set(v[0] for v in b)) == 5:
                    best, bj = TAB[(int(last), sum(v[1] << X for X, v in enumerate(b)))]
                else:
                    best, bj = row_choose(b, need)
                for X in range(5):
                    if best >> X & 1: b[X] = g.notv(b[X])
                k = (bj + 1) % 5
                if bj >= 0:                                          # 10-gate row: output bj reads output k
                    p1, p2 = b[(k + 1) % 5], b[(k + 2) % 5]
                    sel = ((b[(bj + 2) % 5][1] ^ 1) ^ b[k][1]) if (p1[1] ^ 1) != p2[1] else 0
                    NS[k + 5 * Y][z] = g.xorv(b[k], g.and2((p1[0], p1[1] ^ 1), p2, sel))
                for X in range(5):
                    if need >> X & 1:
                        if bj >= 0 and X == k: continue
                        t1 = NS[k + 5 * Y][z] if X == bj else b[(X + 1) % 5]     # not y and z == not chi_y and z
                        t = g.and2((t1[0], t1[1] ^ 1), b[(X + 2) % 5], phi[(X + 5 * Y) * 64 + z])
                        NS[X + 5 * Y][z] = g.xorv(b[X], t)
        for z in range(64):
            NS[0][z] = (NS[0][z][0], NS[0][z][1] ^ ((RCA[r] >> z) & 1))
        S = NS
    out = [S[j >> 6][j & 63] for j in range(256)]
    PD = 0
    for j, v in enumerate(out):
        assert v[0] != NC and v[0] >= 256
        PD |= v[1] << j
    return g, [v[0] for v in out], PD


def allocate(g, outn):
    nn = len(g.op)
    live = [False] * nn
    for n in outn: live[n] = True
    for i in range(nn - 1, 255, -1):
        if live[i]:
            live[g.a[i]] = True
            if g.op[i] != O_NOT: live[g.b[i]] = True
    last = [0] * nn
    for i in range(256, nn):
        if live[i]:
            last[g.a[i]] = i
            if g.op[i] != O_NOT: last[g.b[i]] = i
    outj = {}
    for j, n in enumerate(outn): last[n] = 0xFFFF; outj[n] = j
    outdef = list(outn)
    reg = [0] * nn
    busy = [False] * NREG
    free = list(range(NREG - 1, 255, -1))
    for j in range(256):
        reg[j] = j
        if last[j]: busy[j] = True
    code, prog, peak = {O_XOR: 0, O_AND: 1, O_OR: 2, O_NOT: 3}, [], 0
    for i in range(256, nn):
        if not live[i]: continue
        op, a = g.op[i], g.a[i]
        b = a if op == O_NOT else g.b[i]
        for k, o in enumerate((a, b)):
            if k == 1 and o == a: break
            if last[o] == i:
                r = reg[o]; busy[r] = False
                if r >= 256: free.append(r)
        if i in outj:
            d = outj[i]; assert not busy[d]
        elif free:
            d = free.pop()
        else:
            d = next(r for r in range(256) if not busy[r] and outdef[r] >= last[i])
        busy[d] = True; reg[i] = d; peak = max(peak, d + 1)
        prog.append((code[op], d, reg[a], 0 if op == O_NOT else reg[g.b[i]]))
    return prog, peak


def encode(prog):
    out = bytearray()
    for c, d, a, b in prog:
        out += (c | d << 3 | a << 15 | b << 27).to_bytes(5, "little")
    return bytes(out)


def compile_prog(prog):
    """The straight line, executed instruction by instruction (opcode 0 XOR, 1 AND, 2 OR, 3 NOT)."""
    P = tuple(prog)

    def step(R, A):
        for c, d, a, b in P:
            if c == 0: R[d] = R[a] ^ R[b]
            elif c == 1: R[d] = R[a] & R[b]
            elif c == 2: R[d] = R[a] | R[b]
            else: R[d] = R[a] ^ A
    return step


# ---------------- reference ----------------
def _perm_src():
    """Keccak-f rounds as straight Python source (theta, rho, pi, chi, iota per round; lanes a0..a24)."""
    L = ["def perm(a, rounds):", " " + ",".join("a%d" % i for i in range(25)) + " = a", " for rc in RCA[:rounds]:"]
    for x in range(5): L.append("  c%d = a%d ^ a%d ^ a%d ^ a%d ^ a%d" % (x, x, x + 5, x + 10, x + 15, x + 20))
    for x in range(5): L.append("  d%d = c%d ^ (((c%d << 1) | (c%d >> 63)) & M64)" % (x, (x + 4) % 5, (x + 1) % 5, (x + 1) % 5))
    for x in range(5):
        for y in range(5):
            r = ROT[x][y]; i = x + 5 * y; o = y + 5 * ((2 * x + 3 * y) % 5)
            L.append("  v = a%d ^ d%d; b%d = %s" % (i, x, o, "(((v << %d) | (v >> %d)) & M64)" % (r, 64 - r) if r else "v"))
    for y in range(5):
        for x in range(5):
            L.append("  a%d = b%d ^ (~b%d & b%d)" % (x + 5 * y, x + 5 * y, (x + 1) % 5 + 5 * y, (x + 2) % 5 + 5 * y))
    L.append("  a0 ^= rc")
    L.append(" a[:] = [" + ",".join("a%d" % i for i in range(25)) + "]")
    L.append(" return a")
    return "\n".join(L)


exec(compile(_perm_src(), "perm", "exec"))


def digest(msg, rounds=NR):
    blk = bytearray(136 * (len(msg) // 136 + 1)); blk[:len(msg)] = msg
    blk[len(msg)] ^= 6; blk[-1] ^= 0x80
    st = [0] * 25
    for o in range(0, len(blk), 136):
        for i in range(17): st[i] ^= int.from_bytes(blk[o + 8 * i:o + 8 * i + 8], "little")
        perm(st, rounds)
    return b"".join(st[i].to_bytes(8, "little") for i in range(4))


def msg_of(u):
    l = [KL[i] for i in range(16)]
    u0, u1, u2, u3 = [(u >> (64 * i)) & M64 for i in range(4)]
    l[1], l[6], l[11], l[4], l[9], l[14] = u0 ^ KL[1], u1 ^ KL[6], u0 ^ u1 ^ KL[11], u2 ^ KL[4], u3 ^ KL[9], u2 ^ u3 ^ KL[14]
    return b"".join(v.to_bytes(8, "little") for v in l)


def F_ref(u, PD):
    return int.from_bytes(digest(msg_of(u)), "little") ^ PD


# ---------------- setup and checks ----------------
def setup():
    for m in (b"", b"abc", bytes(135), bytes(200)):
        assert digest(m, 24) == hashlib.sha3_256(m).digest()
    g, outn, PD = build()
    prog, peak = allocate(g, outn)
    assert hashlib.sha256(encode(prog)).hexdigest() == PROG_SHA256 and len(prog) == NINSTR and peak <= NREG
    return compile_prog(prog), PD, len(prog)


def to_planes(points, T):
    """points[t][l] (256-bit) -> 256 planes with bit 256 t + l."""
    planes = [0] * 256
    for t in range(T):
        for l, u in enumerate(points[t]):
            g = 256 * t + l
            j = 0
            while u:
                if u & 1: planes[j] |= 1 << g
                u >>= 1; j += 1
    return planes


def lane_value(R, g, width=256):
    v = 0
    for j in range(width):
        v |= ((R[j] >> g) & 1) << j
    return v


def check_step(step, PD):
    import random
    rnd = random.Random(1)
    pts = [[rnd.getrandbits(256) for _ in range(256)]]
    R = [0] * NREG
    R[:256] = to_planes(pts, 1)
    A = (1 << 256) - 1
    cur = pts[0]
    for _ in range(2):
        step(R, A)
        cur = [F_ref(u, PD) for u in cur]
        for l in range(0, 256, 15):
            assert lane_value(R, l) == cur[l]


def shake(data, n):
    return hashlib.shake_256(data).digest(n)


# ---------------- rho-w22: the search of proof.md Section 4 at width W ----------------
W, H, DK, DTT, LC, U, TB = 22, 4, 3, 5, 256, 3000, 400      # a DP: bits 0..3 zero and bits 4..6, as a number, < 5; replay cap LC; no trail is cut


def rho_w(trials, step, PD):
    T = len(trials)
    A = (1 << (256 * T)) - 1
    mask = (1 << W) - 1
    R = [0] * NREG
    seeds = [bytes.fromhex(t["seed"]) for t in trials]
    rho, nid, att, astart = [0] * T, [0] * T, [-1] * T, [0] * T
    table = [dict() for _ in range(T)]
    done = [None] * T
    obs = [dict(steps=0, trails=0, attempts=0, stored=0, replay_evals=0) for _ in range(T)]
    lid, lst = [0] * (256 * T), [0] * (256 * T)
    pend = []

    def f_small(u):
        return F_ref(u, PD) & mask

    def is_dp(x):
        return x & ((1 << H) - 1) == 0 and (x >> H) & ((1 << DK) - 1) < DTT

    def new_attempt(t, c):
        att[t] += 1; obs[t]['attempts'] += 1
        rho[t] = int.from_bytes(shake(seeds[t] + att[t].to_bytes(4, 'little'), 8), 'little') & mask
        table[t].clear(); nid[t] = 256; astart[t] = c
        for l in range(256):
            g = 256 * t + l
            lid[g] = l; lst[g] = c
            pend.append((g, (rho[t] + l) & mask))
        obs[t]['trails'] += 256

    def apply_pending():
        if not pend: return
        clr = 0
        for g, _ in pend: clr |= 1 << g
        for j in range(W):
            st = 0
            for g, x in pend:
                if (x >> j) & 1: st |= 1 << g
            R[j] = (R[j] & ~clr & A) | st
        del pend[:]

    def replay(sa, sb, lb, t):
        if lb > LC: return None                        # the new trail is longer than the cap
        a, la = sa, 0                                  # la: evaluations of the stored trail from its start to its DP
        while True:
            a = f_small(a); la += 1
            if is_dp(a) or la >= LC: break
        obs[t]['replay_evals'] += la
        if not is_dp(a): return None
        a, b = sa, sb
        for _ in range(abs(la - lb)):
            if la > lb: a = f_small(a)
            else: b = f_small(b)
        obs[t]['replay_evals'] += abs(la - lb)
        if a == b: return None
        for _ in range(min(la, lb) + 1):
            na, nb = f_small(a), f_small(b)
            obs[t]['replay_evals'] += 2
            if na == nb: return a, b
            a, b = na, nb
        return None

    for t in range(T): new_attempt(t, 0)
    apply_pending()
    c = 0
    while any(d is None for d in done):
        c += 1
        if c > 4000: raise RuntimeError("no pair")
        step(R, A)
        for j in range(W, 256): R[j] = 0               # width reduction (this experiment only)
        anyv = 0
        for j in range(H): anyv |= R[j]
        dpm = A ^ anyv                                  # walks with the low H bits zero
        eq, lt = dpm, 0                                 # then the DK bits above them, as a number, < DTT (bit-parallel, most significant first)
        for i in range(DK):
            p = R[H + DK - 1 - i]
            if (DTT >> (DK - 1 - i)) & 1: lt |= eq & (A ^ p); eq &= p
            else: eq &= A ^ p
        dpm = lt
        img = [R[j].to_bytes(32 * T, "little") for j in range(W)]          # byte image of the planes 0..W-1 of this step
        events = []
        while dpm:
            low = dpm & -dpm
            events.append(low.bit_length() - 1)
            dpm ^= low
        seen, fresh = set(), set()
        for g in events:
            t = g >> 8
            if g in seen or done[t] is not None or t in fresh: continue
            seen.add(g)
            x = sum(((img[j][g >> 3] >> (g & 7)) & 1) << j for j in range(W))
            ln = c - lst[g]
            tb = table[t]
            if x in tb:
                ida = tb[x]
                if ida != lid[g]:
                    r = replay((rho[t] + ida) & mask, (rho[t] + lid[g]) & mask, ln, t)
                    if r is not None:
                        done[t] = r; obs[t]['steps'] = c - astart[t]; obs[t]['stored'] = len(tb)
                        continue
            else:
                tb[x] = lid[g]
            if nid[t] >= U:
                new_attempt(t, c); fresh.add(t); continue
            i = nid[t]; nid[t] += 1; obs[t]['trails'] += 1
            lid[g] = i; lst[g] = c
            pend.append((g, (rho[t] + i) & mask))
        for t in range(T):
            if done[t] is None and c - astart[t] >= TB: new_attempt(t, c)
        apply_pending()
    return done, obs


# ---------------- proj-w256: chained full-width steps, 22-bit agreement ----------------
def proj_w(trials, step, PD, steps=8, bits=22):
    T = len(trials)
    A = (1 << (256 * T)) - 1
    pts = []
    for tr in trials:
        raw = shake(bytes.fromhex(tr["seed"]) + b"proj", 32 * 256)
        pts.append([int.from_bytes(raw[32 * l:32 * l + 32], "little") for l in range(256)])
    R = [0] * NREG
    R[:256] = to_planes(pts, T)
    from array import array
    allkeys = []                            # allkeys[s][g]: the 22 low image bits of lane g at step s

    def point(t, l, s):                     # input of step s on lane l (reference chain from the start point)
        u = pts[t][l]
        for _ in range(s): u = F_ref(u, PD)
        return u

    for s in range(steps):
        step(R, A)
        cols = [bin(R[j] | (1 << (256 * T)))[:2:-1] for j in range(bits)]   # bit g of plane j = cols[j][g]
        allkeys.append(array("I", (int("".join(c[g] for c in reversed(cols)), 2) for g in range(256 * T))))
        del cols
    done = [None] * T
    for t in range(T):
        st = {}
        for s in range(steps):
            ks = allkeys[s]
            for l in range(256):
                key = ks[256 * t + l]
                o = st.get(key)
                if o is None:
                    st[key] = (l, s)
                else:
                    a, b = point(t, o[0], o[1]), point(t, l, s)
                    if a != b:
                        done[t] = (a, b, s); break
            if done[t] is not None: break
    return done


def control_preflight():
    """Assemble and check the revised packed control image before either experiment."""
    (XO, AN, OR, NO, AD, SU, SL, SR, EQ, LT, MO, AI, SI, SLI, SRI, ANI,
     EQI, LTI, MOI, LD, ST, LDA, BNZ, BZ, JMP, JAL, JR, RND, PERM, HALT) = range(30)
    C, IDN, RHO, ONES, PF, H, LR, LR2, ZERO = 2181, 2183, 2184, 2185, 2186, 2187, 2188, 2189, 2190
    L, DPM, C1, ACC, TT, REC, SLOT, TR, FL, X, Y, LV, NP, NM, ONEB = range(256, 271)
    P, Q, N, MM, LA, LB, UU, FF, PDR, XX0, XX1, XX2, XX3, TQ, FP = range(280, 295)
    W0 = 300
    S, U, SB, IDB, KB = 23048, 92192, 15, 17, 46
    TB = 1326257481908368167240609567959154688
    LRC = 39426468968298390845350463093604352
    HMAX = 49787865427095778383460604988882945
    DPLO, DK, DT, PFLO, PFN = 145, 10, 708, 241, 15
    lid, lst, misc = S, S + 256, S + 512
    out = misc + 8
    ins, lab, fix = [], {}, []

    def e(op, d=0, a=0, b=0, imm=0, target=None):
        ins.append([op, d, a, b, imm])
        if target is not None:
            fix.append((len(ins) - 1, target))

    def mark(name):
        assert name not in lab
        lab[name] = len(ins)

    def br(cmpop, bop, a, b, target, imm=None):
        e(cmpop, FL, a, b if imm is None else 0, 0 if imm is None else imm)
        e(bop, a=FL, target=target)

    def jeq(a, b, t): br(EQ, BNZ, a, b, t)
    def jeqi(a, i, t): br(EQI, BNZ, a, 0, t, i)
    def jnei(a, i, t): br(EQI, BZ, a, 0, t, i)
    def jlti(a, i, t): br(LTI, BNZ, a, 0, t, i)
    def jgei(a, i, t): br(LTI, BZ, a, 0, t, i)
    def jlt(a, b, t): br(LT, BNZ, a, b, t)
    def jmp(t): e(JMP, target=t)
    def jal(d, t): e(JAL, d, target=t)

    def state():
        for i in range(7): e(LDA, W0 + i, imm=misc + i)
        e(ANI, XX0, UU, imm=M64)
        e(SRI, XX1, UU, imm=64); e(ANI, XX1, XX1, imm=M64)
        e(SRI, XX2, UU, imm=128); e(ANI, XX2, XX2, imm=M64)
        e(SRI, XX3, UU, imm=192)
        e(SLI, TQ, XX0, imm=64); e(XO, W0, W0, TQ)
        e(SLI, TQ, XX1, imm=128); e(XO, W0 + 1, W0 + 1, TQ)
        e(XO, W0 + 1, W0 + 1, XX2)
        e(SLI, TQ, XX3, imm=64); e(XO, W0 + 2, W0 + 2, TQ)
        e(XO, TQ, XX0, XX1); e(SLI, TQ, TQ, imm=192); e(XO, W0 + 2, W0 + 2, TQ)
        e(XO, TQ, XX2, XX3); e(SLI, TQ, TQ, imm=128); e(XO, W0 + 3, W0 + 3, TQ)

    mark("start")
    e(RND, RHO); e(MOI, IDN, imm=256); e(MOI, H); e(MOI, C); e(MOI, ZERO); e(NO, ONES, ZERO); e(MOI, PTR := 274)
    mark("clr")
    for k in range(8): e(ST, a=PTR, b=ZERO, imm=k)
    e(AI, PTR, PTR, imm=8); jlti(PTR, S, "clr"); e(MOI, L)
    mark("iw")
    e(AD, NP, RHO, L); e(ST, a=L, b=L, imm=lid); e(ST, a=L, b=ZERO, imm=lst); jal(LR, "setwalk")
    e(AI, L, L, imm=1); jlti(L, 256, "iw")
    mark("loop"); jeq(PF, ONES, "cont")
    mark("hit")
    e(AI, H, H, imm=1); jlti(H, HMAX + 1, "h1"); e(HALT, imm=10); mark("h1")
    e(OR, SS := 275, DPLO, DPLO + 1)
    for j in range(DPLO + 2, PFLO): e(OR, SS, SS, j)
    e(OR, DPM, PF, SS); e(NO, DPM, DPM)
    bits = [(DT >> (DK - 1 - i)) & 1 for i in range(DK)]
    last = max(i for i, v in enumerate(bits) if v); first = True
    for i in range(last + 1):
        p = DPLO - 1 - i; e(NO, X, p)
        if bits[i]:
            if first: e(AN, Y, DPM, X); first = False
            else: e(AN, X, DPM, X); e(OR, Y, Y, X)
            if i < last: e(AN, DPM, DPM, p)
        else: e(AN, DPM, DPM, X)
    e(MO, DPM, Y); e(AI, C1, C, imm=1)
    mark("dpl"); jeqi(DPM, 0, "cont")
    mark("dp1"); e(MOI, L); e(MO, X, DPM)
    for i, sh in enumerate((128, 64, 32, 16, 8, 4, 2, 1)):
        e(ANI, Y, X, imm=(1 << sh) - 1); jnei(Y, 0, f"ct{i}")
        e(SRI, X, X, imm=sh); e(AI, L, L, imm=sh); mark(f"ct{i}")
    e(SI, Y, DPM, imm=1); e(AN, DPM, DPM, Y)
    mark("gather"); e(SR, ACC, 0, L); e(ANI, ACC, ACC, imm=1)
    for j in range(1, 256):
        e(SR, TT, j, L); e(ANI, TT, TT, imm=1); e(SLI, TT, TT, imm=j); e(OR, ACC, ACC, TT)
    mark("record")
    e(ANI, REC, ACC, imm=(1 << KB) - 1); e(SLI, REC, REC, imm=1); e(AI, REC, REC, imm=1)
    e(LD, ID := 276, L, imm=lid); e(SLI, ID, ID, imm=KB + 1); e(OR, REC, REC, ID)
    e(ANI, SLOT, ACC, imm=(1 << SB) - 1); jlti(SLOT, S, "slok"); e(SI, SLOT, SLOT, imm=S); mark("slok")
    mark("probe"); e(LD, TR, SLOT)
    for k in range(4):
        if k: e(SRI, Y, TR, imm=64 * k); e(ANI, X, Y, imm=M64)
        else: e(ANI, X, TR, imm=M64)
        jeqi(X, 0, f"empty{k}"); e(XO, X, X, REC); e(ANI, X, X, imm=(1 << (KB + 1)) - 1); jeqi(X, 0, f"match{k}")
    mark("pnext"); e(AI, SLOT, SLOT, imm=1); jnei(SLOT, S, "probe"); e(MOI, SLOT); jmp("probe")
    for k in range(4):
        mark(f"empty{k}")
        if k: e(SLI, X, REC, imm=64 * k); e(OR, TR, TR, X)
        else: e(OR, TR, TR, REC)
        e(ST, a=SLOT, b=TR); jmp("ins")
    mark("ins"); e(MO, LV, C1); jal(LR, "restart"); jmp("dpl")
    for k in range(4):
        mark(f"match{k}"); e(SRI, X, TR, imm=64 * k + KB + 1); e(ANI, X, X, imm=(1 << IDB) - 1); jmp("match")
    mark("cont"); e(AI, C, C, imm=1); jnei(C, TB, "loop")
    mark("dl"); e(HALT, imm=12)
    mark("restart"); jnei(IDN, U, "rs1"); e(HALT, imm=11); mark("rs1")
    e(ST, a=L, b=IDN, imm=lid); e(ST, a=L, b=LV, imm=lst); e(AD, NP, RHO, IDN); e(AI, IDN, IDN, imm=1)
    mark("setwalk"); e(MOI, ONEB, imm=1); e(SL, ONEB, ONEB, L); e(NO, NM, ONEB)
    mark("swplanes")
    for j in range(256):
        e(AN, X, j, NM)
        if j: e(SRI, Y, NP, imm=j); e(ANI, Y, Y, imm=1)
        else: e(ANI, Y, NP, imm=1)
        e(SL, Y, Y, L); e(OR, j, X, Y)
    mark("swend"); e(JR, a=LR)
    mark("evalF"); state(); mark("efperm"); e(PERM, a=W0); e(LDA, PDR, imm=misc + 7); e(XO, FF, W0, PDR); e(JR, a=LR2)
    mark("outm"); state(); e(JR, a=LR2)
    mark("match")
    e(LD, Y, L, imm=lid); e(LD, LB, L, imm=lst); e(SU, LB, C1, LB); jgei(LB, LRC + 1, "rfail")
    e(AD, P, RHO, X); e(AD, Q, RHO, Y); e(MO, UU, P); e(MOI, LA)
    mark("meas"); jal(LR2, "evalF"); e(AI, LA, LA, imm=1); jlti(FF, DT << (DPLO - DK), "measd")
    jgei(LA, LRC, "rfail"); e(MO, UU, FF); jmp("meas")
    mark("measd"); jlt(LA, LB, "advq"); e(SU, N, LA, LB); e(MO, MM, LB)
    mark("advp"); jeqi(N, 0, "lock"); e(MO, UU, P); jal(LR2, "evalF"); e(MO, P, FF); e(SI, N, N, imm=1); jmp("advp")
    mark("advq"); e(SU, N, LB, LA); e(MO, MM, LA)
    mark("advq2"); jeqi(N, 0, "lock"); e(MO, UU, Q); jal(LR2, "evalF"); e(MO, Q, FF); e(SI, N, N, imm=1); jmp("advq2")
    mark("lock"); jeq(P, Q, "rfail")
    mark("lloop"); jeqi(MM, 0, "rfail"); e(MO, UU, P); jal(LR2, "evalF"); e(MO, FP, FF); e(MO, UU, Q); jal(LR2, "evalF")
    jeq(FP, FF, "found"); e(MO, P, FP); e(MO, Q, FF); e(SI, MM, MM, imm=1); jmp("lloop")
    mark("found"); e(MO, UU, P); jal(LR2, "outm")
    for i in range(4): e(ST, a=ZERO, b=W0 + i, imm=out + i)
    e(MO, UU, Q); jal(LR2, "outm")
    for i in range(4): e(ST, a=ZERO, b=W0 + i, imm=out + 4 + i)
    e(HALT, imm=1); mark("rfail"); e(HALT, imm=13); mark("end")
    for i, name in fix: ins[i][4] = lab[name]

    assert len(ins) == 2715 and max(max(x[1:4]) for x in ins) == 2190
    assert {k: lab[k] for k in ("loop", "hit", "dpl", "gather", "record", "probe", "cont", "restart", "setwalk", "evalF", "outm", "match", "meas", "end")} == {
        "loop": 26, "hit": 28, "dpl": 153, "gather": 199, "record": 1221, "probe": 1231, "cont": 1298,
        "restart": 1302, "setwalk": 1309, "evalF": 2592, "outm": 2622, "match": 2649, "meas": 2658, "end": 2715}
    expected = {XO: 21, AN: 268, OR: 615, NO: 11, AD: 4, SU: 3, SL: 257, SR: 256, EQ: 3, LT: 1, MO: 18,
                AI: 17, SI: 5, SLI: 270, SRI: 276, ANI: 540, EQI: 23, LTI: 7, MOI: 10, LD: 4, ST: 24,
                LDA: 15, BNZ: 21, BZ: 13, JMP: 14, JAL: 9, JR: 3, RND: 1, PERM: 1, HALT: 5}
    got = {}
    for pc, x in enumerate(ins):
        got[x[0]] = got.get(x[0], 0) + 1
        assert 0 <= x[4] < 1 << 192 and max(x[1:4]) < 2192
        if x[0] in (BNZ, BZ): assert pc and ins[pc - 1][0] in (EQ, LT, EQI, LTI) and ins[pc - 1][1] == x[2] == FL and x[4] < len(ins)
        if x[0] in (JMP, JAL): assert x[4] < len(ins)
    assert got == expected and (lab["h1"] - lab["hit"] - 1) + (lab["dpl"] - lab["h1"]) + 2 == 126

    def pack32(x):
        op, d, a, b, imm = x
        return bytes((op, d & 255, d >> 8, a & 255, a >> 8, b & 255, b >> 8, 0)) + imm.to_bytes(24, "little")

    raw = b"".join(pack32(x) for x in ins)
    assert len(raw) == 86880 and hashlib.sha256(raw).hexdigest() == "f559c8ef25971d844a63973312bcf50ceb3009f7343d8055aeeeeacbb8de11e9"
    pfi = [[OR, PF, PFLO if not i else PF, PFLO + 1 + i, 0] for i in range(PFN - 1)]
    pfraw = b"".join((op | d << 3 | a << 15 | b << 27).to_bytes(5, "little") for op, d, a, b, _ in pfi)
    assert len(pfraw) == 70 and hashlib.sha256(pfraw).hexdigest() == "56de9ca14dcf427d03151d957e3d59fb3bd23296949cf67e0e69f6fb6401db80"

    all_lanes = (1 << 256) - 1
    stream = hashlib.shake_256(b"sha3-r6-control-handler-v1").digest(127 * 121 * 32)
    off = 0
    for trial in range(128):
        r = [0] * 2192
        if trial:
            for p in range(DPLO - DK, 256):
                r[p] = int.from_bytes(stream[off:off + 32], "little"); off += 32
        r[H], r[C] = 0, 17
        for op, d, a, b, _ in pfi: r[d] = r[a] | r[b]
        want = all_lanes
        for p in range(DPLO, 256): want &= all_lanes ^ r[p]
        eqm, ltm = want, 0
        for i in range(DK):
            p = DPLO - 1 - i
            if (DT >> (DK - 1 - i)) & 1: ltm |= eqm & (all_lanes ^ r[p]); eqm &= r[p]
            else: eqm &= all_lanes ^ r[p]
        pc = lab["hit"]
        while pc != lab["dpl"]:
            op, d, a, b, imm = ins[pc]; pc += 1
            if op == OR: r[d] = r[a] | r[b]
            elif op == AN: r[d] = r[a] & r[b]
            elif op == NO: r[d] = all_lanes ^ r[a]
            elif op == MO: r[d] = r[a]
            elif op == AI: r[d] = (r[a] + imm) & all_lanes
            elif op == LTI: r[d] = int(r[a] < imm)
            elif op == BNZ:
                if r[a]: pc = imm
            elif op == HALT: raise AssertionError("hit handler aborted")
            else: raise AssertionError("unexpected hit-handler opcode")
        assert r[DPM] == ltm
    return {"control_instructions": 2715, "prefilter_instructions": 14, "handler_tests": 128}


def main():
    preflight = control_preflight()
    step, PD, nins = setup()
    check_step(step, PD)
    req = json.load(sys.stdin)
    if req["schema_version"] != 1 or req["target_profile"] != "sha3-256-r%d-prefix-v1" % NR:
        raise ValueError("unexpected organizer target")
    mask = ((1 << 22) - 1).to_bytes(32, "little")
    if req["event"] != {"kind": "digest-xor-mask", "mask_hex": mask.hex(), "expected_hex": "00" * 32}:
        raise ValueError("unexpected organizer event")
    trials = req["trials"]
    out = []
    if req["experiment_id"] == "rho-w22":
        done, obs = rho_w(trials, step, PD)
        for t, tr in enumerate(trials):
            a, b = done[t]
            ma, mb = msg_of(a), msg_of(b)
            assert ma != mb and (int.from_bytes(digest(ma), "little") ^ int.from_bytes(digest(mb), "little")) & ((1 << W) - 1) == 0
            obs[t].update(preflight)
            out.append({"trial": tr["trial"], "message_a_hex": ma.hex(), "message_b_hex": mb.hex(), "observations": obs[t]})
    elif req["experiment_id"] == "proj-w256":
        done = proj_w(trials, step, PD)
        for t, tr in enumerate(trials):
            if done[t] is None:
                out.append({"trial": tr["trial"], "message_a_hex": None, "message_b_hex": None})
            else:
                a, b, s = done[t]
                out.append({"trial": tr["trial"], "message_a_hex": msg_of(a).hex(), "message_b_hex": msg_of(b).hex(),
                            "observations": {"step": s, **preflight}})
    else:
        raise ValueError("unknown experiment")
    json.dump({"schema_version": 1, "trials": out}, sys.stdout, separators=(",", ":"), sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
