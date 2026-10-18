"""LS1: distinguished-point collision search on sha3-256-r6-prefix-v1 with a linear-structure message embedding.

Chain function on 256-bit points u (little-endian lanes u0..u3):
  m(u) = 128 bytes = lanes 0..15 of the absorbed state: lane 1 = u0, lane 6 = u1, lane 11 = u0^u1^K11,
  lane 4 = u2, lane 9 = u3, lane 14 = u2^u3^K14, the other lanes 0..15 the constants K below; padding gives lane 16 =
  0x8000000000000006.  F(u) = SHA3-256-r6(m(u)) XOR PD (PD a fixed 256-bit mask).  m is injective, so F(u) = F(u') with
  u != u' gives two distinct messages with equal complete digests.
This program regenerates the bit-sliced straight line of proof.md Section 3 (the same algorithm and node order as the C
generator gen3.c, with the generator's decisions PLAN: constants trial, round-1 and theta complements, free term
polarities; its 5-byte encoding must hash to PROG_SHA256), checks it against a plain 6-round implementation, and runs
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
trial 192
nr 6 optmode 3 trick 1 lasttrick 1 notfold 0
F1 420c12006c81a00281008802004001012004888218245a40000000a1011002000010100081118000
G1 00800000000008200000002000000480008000002000200020000000000000000000000400000010
FG 2 0000000a0e5100000804008018200000430a40000448100080103502004008040442048004042008 00c0c40300840000000080020008040000000404900c04800009000201000080004b202041000100
FG 3 001e0100c84a000410500082010002808003008838000800a401292a000100210040002160010080 044d0061441010102040010200021802018042140000408000200510000000120801480064300408
FG 4 0004201102004002208601000421221005000084c000800020086000082200200428000801000080 800085410200400022000011310202055100080080002208481e2000140a08200091081000804208
FG 5 20000000004000000000000000000000000000002008010000000000000002000000010000000200 0000020000080000011008020000040000000034a0002002040010020a0100484100000008002028
PHI 0 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
PHI 1 0000000000000000000808000000000000010000000000040000000000000080100000000000000000000000000004008000000000000000008000000000000000000000000000000000000000000000000000000000000000020000000000080000000004100000000000000000000000000000000200000000000000000100000000010000000000040000000000000000008000800000100000000000000000000000000000000000000000100100800000000000000000200000000000200000000000000000
PHI 2 0000000000000000000005400000000000000000000000000040000000000000000000000000000000600000000000200000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000800000000000000000000000000000000000002000000000000040000000000000080000000000200090000000000000000004000001008000000000004000001000000000000001000000000000000000000018000000008000000000120000000200000000000000
PHI 3 0000000000000000040804000000000000000000000008000000000000000200000020000000000000000000000000000000000000200000000000020000000000000000000000000020000000000000000000000000000000000000000000020000000000000100000000000000000000008000000200000000004000000000000001000000008001000000000000000000400000000000000200000000000000000208000000000000000080004018000000000000000000000000000020000000000000040000
PHI 4 0000000000000000000000000000000000000080000100000000000000000000000000000000000000000000000000000000000000000000000004000040000000000000000000000000008000000000000000000000000000000000000000200000000000000000000000000000001000010000000001000000000000000000080000008040000000004000000000000000000000000000000000000000000000000000000000000000040000000000000200000000000000000200400000000001000000000000
PHI 5 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
"""
PL = {}
for _ln in PLAN.strip().split("\n"):
    _t = _ln.split()
    if _t[0] in ("trial", "F1", "G1"): PL[_t[0]] = _t[1]
    elif _t[0] == "FG": PL[("FG", int(_t[1]))] = (_t[2], _t[3])
    elif _t[0] == "PHI": PL[("PHI", int(_t[1]))] = _t[2]
TRIAL = int(PL["trial"])            # constants of the generator's selected trial
PROG_SHA256 = "cd2b480a6c607c4c58f27f5a2510d72deb534fbbd46cb67b44134643dacb3bb6"
NINSTR = 27305
NREG = 2304
NC = -1
O_IN, O_XOR, O_AND, O_OR, O_NOT = 0, 1, 2, 3, 4


def consts(trial):
    K = [0] * 25
    K[16] = 0x8000000000000006
    if trial > 0:
        s = (0x9E3779B97F4A7C15 * trial + 1) & M64
        def xs():
            nonlocal s
            s ^= (s << 13) & M64; s ^= s >> 7; s ^= (s << 17) & M64
            return s
        for _ in range(10): xs()
        for l in (0, 2, 3, 5, 7, 8, 10, 12, 13, 15, 11, 14): K[l] = xs()
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
    l[1], l[6], l[11], l[4], l[9], l[14] = u0, u1, u0 ^ u1 ^ KL[11], u2, u3, u2 ^ u3 ^ KL[14]
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


# Fixed algorithm ROM recovered from official run 39090452148; raw bytes
# also appear in proof.md. Compression here is only evidence transport.
ROM_B85 = (
    'c-rmVRd`hA7RK?}(aA(ff&>x>2~tY%Dy5V<Ezm+8s8FM&0#&HeAi>?;-QC^Y-QB%Hfwr7UCetJ3``&dHYdyVbZhD^cviJYD_e>@e'
    'E|{Ax-&bkZt-tcMa=UC_u`RQA$FR2r$7g`OgMANd?Y91j*jUGU{7wIP412uy6pp3f-yN_AfF1RNz#a_t5U__D_V8FI>kgXkKn}NW'
    'Pp^6FJ(u@T$8vvTU9`t1(Xa<aIIY~4bHryoH65cbYxiD%daYaU3GIAWUea`bvd(UN`e)uB-{#owPa?Sf0*2k~cG|dGo1dTl^9O<R'
    '=QUklTX)uXu;u!)cK`Ex%cL7shYkw=OFzMId{Xv*J-}x=J|NEN?CN5E{&@E|rz_aIfxSD}dw{(s*n5G!H`x1ty)W4NfxSQ22Y`Jb'
    '*av}qFxZEHeJI$6fqgjGM}U1K*hhhVG}y<0eJt3=fqgvKCxCq-*e8K~GT5hpeJa?efqgpIXMlYs*k^%#HrVHYeJ<GNfqg#M7l3^s'
    '*cX9)G1!-YeJR+NfqgmHSAcyb*jIslHQ3jHeJ$A6fqgyLH-LR3*f)WFGuXF)eJj|vfqgsJcYu8-*mr?_H`w=peJ|Mefqg&N4}kq3'
    '*bjmIFxZcP{V3Rvf&DnxPk{X-*iV7|G}zC8{Vdqef&Dz#FM$0b*e`+ovSoL?zyHLUfBy?~ykEAzKL~R=*?#|YJl^BO%xB0vz3mL%'
    '^LMnK-?5+Hdwd7$@nQDk13ca<K>iL^e|yco_x5^hk571jlVSV))BpQnv|*2N+aG`G@5fQhzrXN=+56GicjxB+eEo;tdVg|f`%QoU'
    '6BXt=e>(X4i*#`P!9@Qp?mx*N0{oSLzY_3=5d4Pc56K@2{K>$d4E&+cZ+!lf{BGcn0sa`^cO$>+_WWVM?*@K1@P`3^^lkb*z#jzs'
    '==IA3{DHUW4+s7L;12-)aNu`t(;or+4)CL&Pp0!ncziz}9NW)l%N6*~pU1F=2HMW<y?=p@^-qKbW%4Y?2RT8u<0HWykl7D1pWoXL'
    'kmv{S`+*YuKz=_+q94TX2TSyW`TY=yeh9xGD$x(+_uUeGH@_by(GTPIJraEnzaK8q59jwIB>EBjexyV{lHZS#=tuGU(GvY=em_Q{'
    'AH(nGkm%>&_hTjcvHX6VL_dz-kC*7j^ZPj^`Z@XiToV0U{C;kUer|q0k3>HYzn>t{PvH0SO7!#c`}rjL`S|@riGCu#pCr*w;`j4Q'
    '^z-xk1tj_f`2A#welovbP@-Ru-%pX~r||o!68%(uzmP<~5WinoqF<QbFCx(|!tWQA=ojVp?~v%<!S5H7=ojPn@094@$?q4J=ojbr'
    '(<J(7{C)|EehGfRq(r|Yzh6qCUy9!^EzvK{@0XG2m*MxzO7zR}`{gA1<@o)(B>H#p`*%z9@8<XKk?7yU@82uYzn9;?PojSxzkk0('
    '|9*bIyhOh|zyE+l{{eo#f<(UpzyF{_|3QAgqC~$UzyFX#{~><Al0?4}zyGjA|6zXr5sCgI{Qjd7{YUxz$0YiX@%xWU^dIN<pOEN3'
    '!S6pQ(SMTPuPo88%<n%X(SM5He_EpdG{0X(qF;sIuPV{6%I{Z`=vU+SpONT4!|y*U(SMfTuP)KA&hOWd=-1%)pOff6$L~Kc(SM%b'
    'e?g-E0>A&FME^y8|0Rk3OZ@)J68)F?{Z}OVukiadCHgh_{aO<JTKs-(iGFQ<|5b_ptNi|J68+cs{nsV>uk-tFNc7*}_v=XX>+t(;'
    'O7!34_urD}zs2vrEzy6Q-+xD<{|>+Zu0;P`e!s3nzb?Q3o<#pWe*b-m{`>rXJ&Arje*XiB{s;X2hZ6k{`TdV1`XBN8A4~K<=J)GM'
    '^y~Bc4J7&v`29~L`k(OopGx#U<@Z06=zqrVe=gDgoZtUKqW=ZI|D{C#OMbthM86@w-$<h0h~NK8qW=}Y|FuN_YkvP5iT*eI{<jkS'
    'Z~6W2B>La+``=6SzvuTGOY|G_`#(tZf8h7iCHm?7eiMm)6Mny`M87G&-%O(4jNflA(QnT0XGruj`27|V{TBRwONo9<e!rDOzZJjV'
    'TB6^Y-)|$)Z^Q4mmFTzS_uEPI+wuGDCHn38{SFfS4*Y&ciGD|Zzmr726TjbCqTiX{?;_Ff!tZyL=y&D!yGiuB@%!B+`rY~c9uoZ?'
    '{C-b~eoubCmqfo8zu#M;-<#j>Bhl}}@AsAH_vQEdN%Z^i`~4;Q{rUX?68!=E{y>TTKz@IaM1K&!KUktanBN~F(I3L^50&T-<@bk4'
    '^oQ~L!zKE|`TY?R{So~BNQwSPet(oie-ytzTB1Li-yb8<AH(mDmFSP<_s2=}$MO5)CHmv}{RtBN3H<&<iT*@>f09Ih62CuLqCc76'
    'pCZwp!tYO&=uhSMr%Cju@%z&y`qTOS84~>&{QgXd{!D&<mPCIRzdu`|Kbzm5BhjD3@6VO!&*k^$N%ZIO`|~CG^ZES+68#1I{z8fV'
    'LVkadM1K*#zgVKbnBQL_(O<&vFO}#o<@c9K^q2Ab%O(2D`TZ3V{T2NFN{RkTet(rje-*#KTB5(2-(MrqU&HUOmFTbK_t#1E*YW%7'
    'CHm|6{S6ZR4gCH_iT*}@f0IOi6TiP%qQ9Bn-y+f9!tZaD=x^osw@LK3@%!5)`rG;a9TNQ={Qgdf{!V^>mqdRTzrS0eznkCRBhlZ('
    '@9&l9@8$RRN%Z&e`}-yO`}zF?68!`G{y~ZUL4N;`ME?-Ke^{b_nBPAl(LciPAC>4I<@b+C^pElT$0hp5`TY|T{S*BDNs0bRe*ct2'
    '{}jJ}TB3iN-#;VKKf~{zmFS=4_s>c6&++@`CHm+2{R<NP3;g~?iT*`?|B^)i62E_0qJNp+zar7U!tehm(f^U(|4E|%6TknnME_@g'
    '{}+k=FZ}*hiT+i7|5u6rul)WsiT*Wy|GGr~I=_EIqJM+m|4pL*8^8a%ME`ew{||}&AN>AJiT+Jy-+!Fx^Q)qRy~k(%xy-Lye8@m#'
    'uoG<ag@ZjV-pSh14gY{=WV{n^{d}X$^T%86Ur4s!@DC*9a62KkelC~GZR<yb*pK($-(ukYo6a8>>N~&j`of&hKOZ0O*Z=M@ZYRuk'
    'y#M-4pP%ds^By1U*!p3A_HS{IseRMuH%57U*H_8h_eflS?B9I-Dd76km9IbUZ@&IiaQ%yvuRs28zWzes^}+P{is9L>Kc+?uczw&A'
    '-8a2H#adr|{{6Yn==II``Rt+I$JcUyy^l+X?-^k4=L3Dy_jhFWqg%=53)A<-0blyx?28A!MSru;w0pvx0NXP-p`APHzr{g68uX1n'
    'zp{Tmmx8Y!j<uf*`YE8_K)Ig^`V*D=g+TwJazDuQ`kdj;aNA#>Gu;3Ee^p*u|K?v_p9_F~q+$1eE_wtwzPQ=fGRs%jvHtuh0s7&f'
    'U&8$Q;K~%3etu=`;f^ca@DK0@ML4b8E#1cN|L~T+)d4=!=ex#6`HnOl9}?w6IhNn=0wbL$+v}6RZ~A=EtY>ee<^74riLkvt2=QdT'
    'e=;8*kogYCW8S@e$JUPm{b-Nx>};O{eE}3-fR--+`T{AwKrLS&^aW9TL0Y~b=nJO!g0+0X&=*4Sg=qOgpf8l-3)S+4LZ6%Bb8GqB'
    '&=*GWg=zW1pwC0`d9-{U=nJR#!nJ(i&=*1RMQHgVpf8f*i`4Q(LSGcc7p3Kkg1%^qFIvkN4Sg{bUyPP72KsVPd^xmyIiN3=;)~Vt'
    '#X?^k#TTdLi-W#+iZ5Qv7Y}_oDZZRqzMRmPi{i_r<;w+qxhcNfTE5)SmxtoZqvgv3eF+p_f|f4<`tnkId9{3bp)ViBmru)=5Bd@*'
    'zC<lwBJ?Fud`ViqB<Rae@#WX@<%hlk6kh=?UjgV#rudSze96#Pkm4(-<tqq%DHLCdmM;bRQYpSvEnh116{7eGY5594Utx-`u$Hed'
    '^cA7_ifH+YKwnXcuc(%<DD>Sy@!g^2y94@)QGCU;e8r&ePKxhNE#IBcSDfN2uH`EZeQ6Y5nwBpO`btoICA54cpsyswS5nJY68cI}'
    'e5JH}rJ%1g#aCL(R~q`tP<&;yd}W}oEX7w=%U2fq%29mfw0z~D?=Fh(E-l|((04b*cej@BZs@y*;=4!7cMtU4OYz;S<+~U9?xXnb'
    ')AHR1efLv*_iOp?hraR@UwJKGdFXq9;(I{L_W<-&p!h0i`6@u)gB0I`TD}LNuOh`)QOj2m`W~YA9@6qX1bvk#zDioYO3?Q(#rLq5'
    '?_ubBgyMTd%l8QMJxcLCs^xnW`W~bB9@FwY27QlHe2;7S9*4dsD847Od{02%lN8^RTD~WtuQJ6~S<6=$`ktcrp3?F?1$|Fbd{1ln'
    'o`$|E6kioBUlr)9O7T_I@>PYtY7}2JEnhY0dxqkBM$7jM^gT=QJ*(w=7W%4FeATsl)uFEj#aBbiR|EQ<qxhcF@;wKA&r^KQYx$ms'
    'z85II7qomYK;MfL--}wl7oqPZiti;Y-%HT<GR60@mhWZgdxheAMa%aJ^wp&JYHImvLSHS4ua=gt7WCDo_-bqUYD3?v6yK{_zE`2|'
    'HHz;wE#GU<_d3P*x|Z*C=zD|Wdqd0j2K3dT`08l+>OkL{6yKX#zBi%oEsF0gE#F(v_cq1%wwCX0=zE9adq>On4)ncC@x80%dl&lZ'
    'Qhar_e08DkJ&Nx=E#G_4_ddn<zLxKO=&MKZ)zk9TgT4<az7Mo~A3)!S6yJwhz7L`ABZ}`ME#F7b_c6uyv6k;+=&Mih)z|XXhrR|B'
    'Ujr>)1L*sN;`>C)_X+fUO7VTF<@*%+KBM?P)AD@=eV<c&pKJL(hrTZ;zAv<VUqIiN6yKLxzAvG#A;s5F%hwS48c}?Ww0w=A?<<P$'
    'D=ptw(DyaP_qCSqYv}ui;`>I+_YL%YOYwcH<@*-;zN7fQ)AD@>ecw}j-)s54hrY%XUt=v_W9a*V;`>3%_XG5$Q+(-KzI5noLh&`x'
    '@->0JrW9XOEnidUYew-k)ABWgzUCBPb1h$U=*yt^GPHad(AR?EYoX<90evkgzLr|PmeALV;%lYlYXyC+DZbWPzShv!hT?0Z<!b|d'
    'Z7IICTE4c>*N)<Ar{!x0eeEf}_FBI7(AR<D>!9W90DT=PzK&YHj?mYM;_Ia4>jZtBDZb8HzRu9sh2ra?<?8}{T`9h<TE4E(*Nx)q'
    'rseAfecdU(?pnU?(AR_F>!IcA0ew9wzMfjXp3v8e;_Id5>jiziDZbuXzTVK+hvMs_<?91|eJQ@aTE4!}*N@`sr{(Jhef=rE{#w5N'
    '&^LhM8=&PI0DS`~zJXf4fzUUI;v1yp8w7oWDZas4zQNEpgyI{b<r@NhLn*$YTE3ysH;m#NrsW$3eZwif;aa}o&^LnO8=>VJ0evGW'
    'zL8qKk<d4a;v1#q8wGu%DZbHKzR}P(hT<Ee<r@QiV=2C|TE4N+H;&>Pr{x<5ed8&<@mjv|&^LkNo1o>J0DTiFzKL4CiO@HR;+v%9'
    'n*@E6DZa^CzRA!xh2oo{<(mS1Qz^cwTE3~!H;v+(rsbOkebXtv=~}+&&^LqPo1x{K0ev$mzL{FSnb0?j;+v)An+1KdDZbfSzS+<>'
    'hvJ)~<(mV2b1A;LTE4l^H;>|*r{$Xmee)^4`C7jD(6@l%TcG7z0DTK7zJ*%8h0wQ%;#;KUTLgWJDZa&8zQxeDgyLJG<y!)MODVpk'
    'TE3;ww~XRjrsZ1(eak7n<yyYw(6@r(TcPD!0eveezLi?OmC(0};#;NVTLpcqDZbTOzSYpThT>bJ<y!-NYbn09TE4Z=w~pdlr{!A*'
    'ed{T{^;*95(6@o&+o0v!0DT)NzKvSGjnKD=;@hO<+XQ`^DZb5GzRl3Lh2q<y<=X;%TPeP+TE4B&w~gZ4rsdlPecLI%?OML=(6@u)'
    '+o9##0ew3uzMWdWozS<7;@hR=+Xa2QDZbrWzTMEbhvM6#<=X>&dnvxXTE4x|w~yl6r{&uRefufC{aU{L(0731JD}w|0DT83zJpr6'
    'gV1+~;ya|}I|O})DZay6zQfRWgyK7*<vRj>M=8FeTE3&ucZ}jYrsX>Zea9)j<66Gs(0793JE7$}0evSazLQ$MlhAjH;yb0~I|Y5G'
    'DZbNMzSGcmhT=P;<vRm?XDPn3TE4T;caGvar{y~bedj5@^IE?1(0762yP)N}0DTuJzKdGEi_mw8;=82fy99lgDZa~EzRS>eh2p!S'
    '<+}oXKT>=@YWaSIzMm+*pR{~GLEq05-_KgUpP}y;itiUK-!IU2mEyaq<+}=fzfyd^YWaSJzH1cUH7(yY=(|qwUDxtmhrSyW-wiF_'
    '4e0xg;`>d@_Z#&6PVxP&<@+7_{-F5&(DMBOeK#q-n_9k`cAvjn#<1sgx!Sp1E_i${!=5wE*G@Nlz)sE*zP*WQFX`Kxn)Xt@y_sn*'
    '?c1B1_A<Ub!?c(6?JW#@bU`P7*5jA`^_Ryt#kW^7J-#VUiuL$Z-|^|D<5Qhf>+ywr$1gG*A6eKbX!E(!oHVDf`T65LKE>v9m2gVf'
    'j?datt>-Uf^_6r=TF;+(eJR%S7q;CW!ueBuLi_oR_otLo%65ML0~%x46Ehzn%lBu_WZ&A-^Z{1|ypM0P`3&Cg|Mryc|DykV|Nry-'
    '|Ihco`1e2c`!CtB$7R1eNH=^yU|dr6Zuo${;3Ox&NizF#xP9w?{)tmVLjU~Vxm_-I=9XqSJ}8gV${l7te^7#Vx4eJx<ahGeUjJef'
    'ZR@}9Utz<ZkbU<}?{C5rokZLFGw=N=aLcWZ<3DfK{V8HT{x4VX|J+~i{V8C(19`yp`|pp*7nbR>JU{%`XZjPtdF{u0^4V7N`)2=F'
    'jN8d;JKpch&wPHN=Z7bc{r*Sf_4yp|_@L{z+}|W8(RzOqDfc%(@BSv-*8NS8xxWG6`b~bf+xz@Tz|a3QaQ-Co{mn<YziC>}-y-(='
    'd%KUH_x@Q6{_D$a{{AXr^`YlSKHvRC&yOVV_~pLM`)_*x9Pe^<aC_fFx2kQ~z3-u0+jj4J=r*?9`yRS&?b~~Nk-r`Aw+H?Xz~9lZ'
    'CxO>T|Kn%+{_!6l369Tc*#8CHiXC$'
)
LOADER_HEX = (
    '00000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000'
    '0604000000000000c50a000000000000000000000000000000000000000000000700000400000000050000000000000000000000000000000000000000000000'
    '08000000000000001000000000000000000000000000000000000000000000000402000000000000000000000000000000000000000000000000000000000000'
    '0303000200000000ff00000000000000000000000000000000000000000000000604000300000000ff0000000000000000000000000000000000000000000000'
    '07000004000000000d00000000000000000000000000000000000000000000000205000200000000400000000000000000000000000000000000000000000000'
    '0105000500000000000c000000000000000000000000000000000000000000000500000500010000000000000000000000000000000000000000000000000000'
    '08000000000000000e00000000000000000000000000000000000000000000000101000100000000010000000000000000000000000000000000000000000000'
    '01000000000000000100000000000000000000000000000000000000000000000800000000000000020000000000000000000000000000000000000000000000'
    '00000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000'
    '0604000000000000c50a000000000000000000000000000000000000000000000700000400000000150000000000000000000000000000000000000000000000'
    '0c000000000000000000000000000000000000000000000000000000000000000402000000000000000000000000000000000000000000000000000000000000'
    '0303000200000000ff00000000000000000000000000000000000000000000000604000300000000ff0000000000000000000000000000000000000000000000'
    '07000004000000001a000000000000000000000000000000000000000000000008000000000000002e0000000000000000000000000000000000000000000000'
    '060400030000000016000000000000000000000000000000000000000000000007000004000000001d0000000000000000000000000000000000000000000000'
    '08000000000000002500000000000000000000000000000000000000000000000604000300000000170000000000000000000000000000000000000000000000'
    '07000004000000002000000000000000000000000000000000000000000000000800000000000000250000000000000000000000000000000000000000000000'
    '06040003000000001800000000000000000000000000000000000000000000000700000400000000230000000000000000000000000000000000000000000000'
    '08000000000000002500000000000000000000000000000000000000000000000604000300000000190000000000000000000000000000000000000000000000'
    '07000004000000002b00000000000000000000000000000000000000000000000205000200000000400000000000000000000000000000000000000000000000'
    '0105000500000000000c000000000000000000000000000000000000000000000406000500000000000000000000000000000000000000000000000000000000'
    '09060006000000004000000000000000000000000000000000000000000000000307000200000000ffffffffffffffff00000000000000000000000000000000'
    '0a020007000600000000000000000000000000000000000000000000000000000105000100000000001000000000000000000000000000000000000000000000'
    '05000005000200000000000000000000000000000000000000000000000000000101000100000000010000000000000000000000000000000000000000000000'
    '01000000000000000100000000000000000000000000000000000000000000000800000000000000120000000000000000000000000000000000000000000000'
)

def check_literal_loader(instructions, labels, fixups):
    """Official-only execution of literal loader and ROM; compare to source assembler."""
    import struct
    mask = (1 << 256) - 1
    label_names = sorted(labels)
    label_ids = {name: i for i, name in enumerate(label_names)}
    at = {}
    for name in label_names:
        at.setdefault(labels[name], []).append(name)
    refs = dict(fixups)
    rom = []
    for pc in range(len(instructions) + 1):
        for name in at.get(pc, []):
            rom.append(255 | (label_ids[name] << 64))
        if pc == len(instructions): break
        op, d, a, b, imm = instructions[pc]
        if pc in refs: imm = label_ids[refs[pc]]
        rom.append(op | (d << 8) | (a << 24) | (b << 40) | (imm << 64))
    assert len(rom) <= 3072 and len(labels) <= 256
    # Primitive loader ISA: SET, ADDI, SHR, ANDI, LOAD, STORE, EQI,
    # JZ, JMP, SHL, OR, ADD, HALT. Every instruction counts once.
    # ROM [0,3072), labels [3072,3328), output [4096,6896).
    # Fields are opcode,d,a,b,192-bit immediate, encoded in 32 bytes.
    SET, ADDI, SHR, ANDI, LOAD, STORE, EQI, JZ, JMP, SHL, OR, ADD, HALT = range(13)
    # r0=i, r1=output count, r2=word, r3=tag, r4=predicate,
    # r5=label/address scratch, r6=relocated immediate, r7=old low bits.
    import base64, zlib, hashlib
    literal_rom = zlib.decompress(base64.b85decode(ROM_B85))
    assert len(literal_rom) == 88224
    assert hashlib.sha256(literal_rom).hexdigest() == '4593c1d2a34d62e68fe740883f084823f0e63fd8322b6e7874f55209d440a9a2'
    assert literal_rom == b''.join(x.to_bytes(32,'little') for x in rom)
    encoded = bytes.fromhex(LOADER_HEX)
    assert len(encoded) == 1536
    mem = [0]*8192
    mem[:len(rom)] = [int.from_bytes(literal_rom[i:i+32], "little") for i in range(0,len(literal_rom),32)]
    r = [0]*16
    pc = steps = 0
    while True:
        assert steps < 1 << 20 and 0 <= pc < len(encoded)//32
        raw=encoded[pc*32:(pc+1)*32]
        op,d,a,b,z=struct.unpack('<BHHHB',raw[:8]); imm=int.from_bytes(raw[8:],'little')
        assert not z and max(d,a,b)<16
        pc+=1;steps+=1
        if op==SET:r[d]=imm
        elif op==ADDI:r[d]=(r[a]+imm)&mask
        elif op==SHR:r[d]=r[a]>>imm
        elif op==ANDI:r[d]=r[a]&imm
        elif op==LOAD:
            assert 0<=r[a]<8192
            r[d]=mem[r[a]]
        elif op==STORE:
            assert 0<=r[a]<8192
            mem[r[a]]=r[b]
        elif op==EQI:r[d]=int(r[a]==imm)
        elif op==JZ:
            if not r[a]:pc=imm
        elif op==JMP:pc=imm
        elif op==SHL:r[d]=(r[a]<<imm)&mask
        elif op==OR:r[d]=r[a]|r[b]
        elif op==ADD:r[d]=(r[a]+r[b])&mask
        elif op==HALT:break
        else:raise AssertionError('unknown loader instruction')
    assert r[1]==len(instructions)
    expected=[op|(d<<8)|(a<<24)|(b<<40)|(imm<<64) for op,d,a,b,imm in instructions]
    assert mem[4096:4096+len(expected)]==expected
    for name,i in label_ids.items():assert mem[3072+i]==labels[name]
    assert steps == 77033
    return rom, {'loader_steps':steps,'loader_code_bytes':len(encoded),'rom_records':len(rom)}


def check_current_assembly():
    # Adapted from Jbenisek 18d9298d Appendix D.1; official executor only.
    import struct
    M256 = (1 << 256) - 1
    M64 = (1 << 64) - 1
    PARAMS = {'NR': 6, 'HF': 111, 'DPLO': 145, 'DK': 10, 'DT': 704, 'S': 22912, 'U': 91648, 'SB': 15, 'IDB': 17, 'W': 633825300114114700748351602688, 'J': 62557, 'LRC': 39650209299238673334714631209353216, 'Tb': 1326282235757393717704586450847137792, 'HMAX': 60373388996093333731432449989148673, 'PFLO': 242, 'PFN': 14}
    NR = PARAMS['NR']                                  # rounds of the target
    UNIT = 271 * NR                                    # the cost model's price of one NR-round permutation (word operations)
    RB, RPW = 64, 4                                    # record width; records per word
    RM = (1 << RB) - 1


    def keyb(Pm): return RB - 1 - Pm['IDB']            # key bits of a record: 1 + KEYB + IDB = 64


    def thr(Pm): return Pm['DT'] << (Pm['DPLO'] - Pm['DK'])    # the DP is x < THR (DK = 0: DT = 1)

    # ---- ISA ----
    XOR, AND, OR, NOT, ADD, SUB, SHL, SHR, EQ, LT, MOV = range(11)
    ADDI, SUBI, SHLI, SHRI, ANDI, EQI, LTI, MOVI = range(11, 19)
    LD, ST, LDA, BNZ, BZ, JMP, JAL, JR, RND, PERM, HALT = range(19, 30)
    NAMES = 'XOR AND OR NOT ADD SUB SHL SHR EQ LT MOV ADDI SUBI SHLI SHRI ANDI EQI LTI MOVI LD ST LDA BNZ BZ JMP JAL JR RND PERM HALT'.split()
    CMPOPS = (EQ, LT, EQI, LTI)

    # ---- registers ----
    C, NXT, IDN, RHO, ONES, PF, H, LR, LR2, ZERO = range(2181, 2191)   # state (2,181..2,190; 2,191 spare)
    (L, DPM, C1, ACC, TT, REC, SLOT, TR, F, X, Y, LV, NP, NM, ONEB, V, MN, E, PTR, SS, ID, STV) = range(256, 278)
    (P, Q, N, MM, LA, LB, UU, FF, PDR, X0, X1, X2, X3, TQ, FP) = range(280, 295)
    Z = 295
    W0 = 300                                                              # W0..W6, the 1600-bit state of evalF
    NREGS = 2192


    class Asm:
        def __init__(s):
            s.ins = []; s.lab = {}; s.fix = []

        def pc(s): return len(s.ins)

        def label(s, n):
            assert n not in s.lab, n
            s.lab[n] = len(s.ins)

        def e(s, op, d=0, a=0, b=0, imm=0, tgt=None):
            s.ins.append([op, d, a, b, imm])
            if tgt is not None: s.fix.append((len(s.ins) - 1, tgt))

        def resolve(s):
            for i, t in s.fix: s.ins[i][4] = s.lab[t]
            for x in s.ins: assert 0 <= x[4] < 1 << 192 and max(x[1:4]) < 2192

        # plain instructions
        def xor(s, d, a, b): s.e(XOR, d, a, b)
        def and_(s, d, a, b): s.e(AND, d, a, b)
        def or_(s, d, a, b): s.e(OR, d, a, b)
        def not_(s, d, a): s.e(NOT, d, a)
        def add(s, d, a, b): s.e(ADD, d, a, b)
        def sub(s, d, a, b): s.e(SUB, d, a, b)
        def shl(s, d, a, b): s.e(SHL, d, a, b)
        def shr(s, d, a, b): s.e(SHR, d, a, b)
        def mov(s, d, a): s.e(MOV, d, a)
        def addi(s, d, a, i): s.e(ADDI, d, a, 0, i)
        def subi(s, d, a, i): s.e(SUBI, d, a, 0, i)
        def shli(s, d, a, i): s.e(SHLI, d, a, 0, i)
        def shri(s, d, a, i): s.e(SHRI, d, a, 0, i)
        def andi(s, d, a, i): s.e(ANDI, d, a, 0, i)
        def movi(s, d, i): s.e(MOVI, d, 0, 0, i)
        def ld(s, d, a, i): s.e(LD, d, a, 0, i)
        def st(s, a, i, b): s.e(ST, 0, a, b, i)
        def lda(s, d, i): s.e(LDA, d, 0, 0, i)
        def rnd(s, d): s.e(RND, d)
        def permute(s, a): s.e(PERM, 0, a)
        def halt(s, code): s.e(HALT, 0, 0, 0, code)
        def jmp(s, t): s.e(JMP, tgt=t)
        def jal(s, d, t): s.e(JAL, d, tgt=t)
        def jr(s, a): s.e(JR, 0, a)

        # compare + branch pairs (a branch is always right after its compare)
        def _br(s, brop, t): s.e(brop, 0, F, 0, 0, t)
        def jeq(s, a, b, t): s.e(EQ, F, a, b); s._br(BNZ, t)
        def jne(s, a, b, t): s.e(EQ, F, a, b); s._br(BZ, t)
        def jeqi(s, a, i, t): s.e(EQI, F, a, 0, i); s._br(BNZ, t)
        def jnei(s, a, i, t): s.e(EQI, F, a, 0, i); s._br(BZ, t)
        def jlt(s, a, b, t): s.e(LT, F, a, b); s._br(BNZ, t)
        def jge(s, a, b, t): s.e(LT, F, a, b); s._br(BZ, t)
        def jlti(s, a, i, t): s.e(LTI, F, a, 0, i); s._br(BNZ, t)
        def jgei(s, a, i, t): s.e(LTI, F, a, 0, i); s._br(BZ, t)


    def build_state(A, MISC):
        """W0..W6 := the 1600-bit state of the one-block message m(u), u in UU (26 instructions)."""
        for i in range(7): A.lda(W0 + i, MISC + i)
        A.andi(X0, UU, M64); A.shri(X1, UU, 64); A.andi(X1, X1, M64); A.shri(X2, UU, 128); A.andi(X2, X2, M64); A.shri(X3, UU, 192)
        A.shli(TQ, X0, 64); A.xor(W0, W0, TQ)                    # lane 1  = u0
        A.shli(TQ, X1, 128); A.xor(W0 + 1, W0 + 1, TQ)           # lane 6  = u1
        A.xor(W0 + 1, W0 + 1, X2)                                # lane 4  = u2
        A.shli(TQ, X3, 64); A.xor(W0 + 2, W0 + 2, TQ)            # lane 9  = u3
        A.xor(TQ, X0, X1); A.shli(TQ, TQ, 192); A.xor(W0 + 2, W0 + 2, TQ)   # lane 11 = u0 ^ u1 ^ K11
        A.xor(TQ, X2, X3); A.shli(TQ, TQ, 128); A.xor(W0 + 3, W0 + 3, TQ)   # lane 14 = u2 ^ u3 ^ K14


    def program(Pm):
        """Pm: S (table words), U (trail limit), SB (slot bits), IDB (trail number bits), LRC (replay cap), Tb, HMAX, DPLO, DK, DT,
        PFLO, PFN, WTEST (None or width)."""
        S, U, SB, LRC, Tb, HMAX = Pm['S'], Pm['U'], Pm['SB'], Pm['LRC'], Pm['Tb'], Pm['HMAX']
        DPLO, DK, DT, PFLO, PFN, WT = Pm['DPLO'], Pm['DK'], Pm['DT'], Pm['PFLO'], Pm['PFN'], Pm.get('WTEST')
        IDB = Pm['IDB']; KEYB = keyb(Pm); THR = thr(Pm)
        assert (1 << SB) <= 2 * S and S % 8 == 0 and PFLO > DPLO + 1 and U <= RPW * S and U <= 1 << IDB and (WT or DPLO - DK > KEYB)
        assert (DK == 0 and DT == 1) or (DK >= 1 and 0 < DT < 1 << DK and DPLO >= DK)
        LID, LST, MISC = S, S + 256, S + 512
        OUT = MISC + 8
        A = Asm()
        # ---------------- setup ----------------
        A.label('start')
        A.rnd(RHO); A.movi(IDN, 256); A.movi(H, 0); A.movi(C, 0); A.movi(ZERO, 0); A.not_(ONES, ZERO)
        A.movi(PTR, 0)
        A.label('clr')                                           # TAB := 0, eight words per pass
        for k in range(8): A.st(PTR, k, ZERO)
        A.addi(PTR, PTR, 8); A.jlti(PTR, S, 'clr')
        A.movi(L, 0)
        A.label('iw')                                            # for l < 256: LID[l] := l; LST[l] := 0; lane l := rho + l
        A.add(NP, RHO, L); A.st(L, LID, L); A.st(L, LST, ZERO); A.jal(LR, 'setwalk')
        A.addi(L, L, 1); A.jlti(L, 256, 'iw')
        # ---------------- the loop: the straight line (SLPOS) then the tests ----------------
        A.label('loop')
        A.jeq(PF, ONES, 'cont')                                  # prefilter test (2)
        # ---------------- hit: some walk has planes PFLO..PFLO+PFN-1 zero ----------------
        A.label('hit')
        A.addi(H, H, 1); A.jlti(H, HMAX + 1, 'h1'); A.halt(10); A.label('h1')      # hit counter and abort (F5)
        A.or_(SS, DPLO, DPLO + 1)
        for j in range(DPLO + 2, PFLO): A.or_(SS, SS, j)         # OR of the planes DPLO..PFLO-1
        A.or_(DPM, PF, SS); A.not_(DPM, DPM)                     # DPM: walks with planes DPLO..255 zero
        if DK:                                                   # keep the walks whose planes DPLO-1 .. DPLO-DK, as a number, are < DT
            bits = [(DT >> (DK - 1 - i)) & 1 for i in range(DK)]  # most significant first: plane DPLO - 1 - i
            last1 = max(i for i in range(DK) if bits[i]); first = True
            for i in range(last1 + 1):
                p = DPLO - 1 - i
                A.not_(X, p)
                if bits[i]:
                    if first: A.and_(Y, DPM, X); first = False   # lt := eq and not p
                    else: A.and_(X, DPM, X); A.or_(Y, Y, X)      # lt := lt or (eq and not p)
                    if i < last1: A.and_(DPM, DPM, p)            # eq := eq and p
                else: A.and_(DPM, DPM, X)                        # eq := eq and not p
            A.mov(DPM, Y)                                        # DPM := lt
        A.addi(C1, C, 1)                                         # steps completed including this one
        A.label('dpl')
        A.jeqi(DPM, 0, 'cont')
        A.label('dp1')                                           # ---- one DP walk: l := lowest set bit of DPM ----
        A.movi(L, 0); A.mov(X, DPM)
        for i, sh in enumerate((128, 64, 32, 16, 8, 4, 2, 1)):
            A.andi(Y, X, (1 << sh) - 1); A.jnei(Y, 0, 'ct%d' % i); A.shri(X, X, sh); A.addi(L, L, sh); A.label('ct%d' % i)
        A.subi(Y, DPM, 1); A.and_(DPM, DPM, Y)                   # clear that bit
        A.label('gather')                                        # ACC := the 256-bit point of walk l (bit j = plane j, bit l)
        A.shr(ACC, 0, L); A.andi(ACC, ACC, 1)
        for j in range(1, 256):
            A.shr(TT, j, L); A.andi(TT, TT, 1); A.shli(TT, TT, j); A.or_(ACC, ACC, TT)
        A.label('record')                                        # REC := 1 | (end bits 0..67) << 1 | trail number << 69
        A.andi(REC, ACC, (1 << KEYB) - 1); A.shli(REC, REC, 1); A.addi(REC, REC, 1)
        A.ld(ID, L, LID); A.shli(ID, ID, KEYB + 1); A.or_(REC, REC, ID)
        A.andi(SLOT, ACC, (1 << SB) - 1); A.jlti(SLOT, S, 'sl_ok'); A.subi(SLOT, SLOT, S); A.label('sl_ok')
        A.label('probe')                                         # one table word: its four records in order
        A.ld(TR, SLOT, 0)
        for k in range(RPW):
            if k: A.shri(Y, TR, RB * k); A.andi(X, Y, RM)
            else: A.andi(X, TR, RM)
            A.jeqi(X, 0, 'empty%d' % k)
            A.xor(X, X, REC); A.andi(X, X, (1 << (KEYB + 1)) - 1); A.jeqi(X, 0, 'match%d' % k)
        A.label('pnext')
        A.addi(SLOT, SLOT, 1); A.jnei(SLOT, S, 'probe')
        A.movi(SLOT, 0); A.jmp('probe')
        for k in range(RPW):                                     # insertion into the first empty record of the word
            A.label('empty%d' % k)
            if k: A.shli(X, REC, RB * k); A.or_(TR, TR, X)
            else: A.or_(TR, TR, REC)
            A.st(SLOT, 0, TR); A.jmp('ins')
        A.label('ins')
        A.mov(LV, C1); A.jal(LR, 'restart'); A.jmp('dpl')
        for k in range(RPW):                                     # a record with the same KEYB end bits: X := its trail number
            A.label('match%d' % k)
            A.shri(X, TR, RB * k + KEYB + 1); A.andi(X, X, (1 << IDB) - 1); A.jmp('match')
        # ---------------- end of iteration ----------------
        A.label('cont')
        A.addi(C, C, 1); A.jnei(C, Tb, 'loop')                   # counter (3 with the compare and branch)
        A.label('dl')
        A.halt(12)                                               # c = Tb: the attempt failed
        # ---------------- restart(l) and the insertion of a point into lane l ----------------
        A.label('restart')                                       # in: L, LV; link LR
        A.jnei(IDN, U, 'rs1'); A.halt(11); A.label('rs1')
        A.st(L, LID, IDN); A.st(L, LST, LV); A.add(NP, RHO, IDN); A.addi(IDN, IDN, 1)
        A.label('setwalk')                                       # in: L, NP; link LR
        A.movi(ONEB, 1); A.shl(ONEB, ONEB, L); A.not_(NM, ONEB)
        A.label('sw_planes')
        for j in range(256):
            A.and_(X, j, NM)
            if j: A.shri(Y, NP, j); A.andi(Y, Y, 1)
            else: A.andi(Y, NP, 1)
            A.shl(Y, Y, L); A.or_(j, X, Y)
        A.label('sw_end')
        A.jr(LR)
        # ---------------- the evaluation of F on one point with the permutation ----------------
        A.label('evalF')                                         # in: UU; out: FF; link LR2
        build_state(A, MISC)
        A.label('ef_perm')
        A.permute(W0); A.lda(PDR, MISC + 7); A.xor(FF, W0, PDR)
        if WT: A.andi(FF, FF, (1 << WT) - 1)                     # test builds only: F truncated to the low WT bits
        A.jr(LR2)
        A.label('outm')                                          # in: UU; out: W0..W3 = the 128-byte message m(UU); link LR2
        build_state(A, MISC)
        A.jr(LR2)
        # ---------------- replay ----------------
        A.label('match')                                         # in: X (stored trail a), L (walk of trail b), C1
        A.ld(Y, L, LID); A.ld(LB, L, LST); A.sub(LB, C1, LB)     # trail b: its number and its length lb = c1 - LST[l]
        A.jgei(LB, LRC + 1, 'rfail')                             # lb > LRC: the replay refuses it
        A.add(P, RHO, X); A.add(Q, RHO, Y)
        A.mov(UU, P); A.movi(LA, 0)
        A.label('meas')                                          # la := evaluations of trail a from its start to its first DP
        A.jal(LR2, 'evalF'); A.addi(LA, LA, 1); A.jlti(FF, THR, 'measd')       # the image is a DP when FF < THR
        A.jgei(LA, LRC, 'rfail'); A.mov(UU, FF); A.jmp('meas')
        A.label('measd')
        A.jlt(LA, LB, 'advq')
        A.sub(N, LA, LB); A.mov(MM, LB)
        A.label('advp')
        A.jeqi(N, 0, 'lock'); A.mov(UU, P); A.jal(LR2, 'evalF'); A.mov(P, FF); A.subi(N, N, 1); A.jmp('advp')
        A.label('advq')
        A.sub(N, LB, LA); A.mov(MM, LA)
        A.label('advq2')
        A.jeqi(N, 0, 'lock'); A.mov(UU, Q); A.jal(LR2, 'evalF'); A.mov(Q, FF); A.subi(N, N, 1); A.jmp('advq2')
        A.label('lock')
        A.jeq(P, Q, 'rfail')
        A.label('lloop')
        A.jeqi(MM, 0, 'rfail')
        A.mov(UU, P); A.jal(LR2, 'evalF'); A.mov(FP, FF); A.mov(UU, Q); A.jal(LR2, 'evalF')
        A.jeq(FP, FF, 'found')
        A.mov(P, FP); A.mov(Q, FF); A.subi(MM, MM, 1); A.jmp('lloop')
        A.label('found')                                         # output m(p), m(q): words W0..W3 of the built states
        A.mov(UU, P); A.jal(LR2, 'outm')
        for i in range(4): A.st(ZERO, OUT + i, W0 + i)
        A.mov(UU, Q); A.jal(LR2, 'outm')
        for i in range(4): A.st(ZERO, OUT + 4 + i, W0 + i)
        A.halt(1)
        A.label('rfail')
        A.halt(13)
        A.label('end')
        A.resolve()
        return A


    def audit(A):
        """every conditional branch follows the compare that sets its register; every label inside range"""
        for i, x in enumerate(A.ins):
            if x[0] in (BNZ, BZ):
                p = A.ins[i - 1]
                assert p[0] in CMPOPS and p[1] == x[2], ('branch without compare', i)
                assert x[4] < len(A.ins)
            if x[0] in (JMP, JAL): assert x[4] < len(A.ins)


    # ---------------- encoding ----------------
    def enc(x):
        op, d, a, b, imm = x
        return struct.pack('<BHHHB', op, d, a, b, 0) + imm.to_bytes(24, 'little')


    def dec(bs):
        out = []
        for i in range(0, len(bs), 32):
            op, d, a, b, z = struct.unpack('<BHHHB', bs[i:i + 8])
            out.append((op, d, a, b, int.from_bytes(bs[i + 8:i + 32], 'little')))
        return out


    def sl_bytes(prog, PFLO, PFN):
        """prog.bin + the prefilter: PF := OR of planes PFLO..PFLO+PFN-1 (PFN-1 ORs), 5-byte instructions"""
        out = bytearray(prog)
        def w(code, d, a, b): return (code | d << 3 | a << 15 | b << 27).to_bytes(5, 'little')
        out += w(2, PF, PFLO, PFLO + 1)
        for j in range(PFLO + 2, PFLO + PFN): out += w(2, PF, PF, j)
        return bytes(out)



    def counts(A, Pm):
        """Worst-case operation counts of every routine, from the lengths of the emitted code (an instruction is one
        operation, PERM is UNIT).  seg(a, b) = number of instructions between two labels."""
        I = A.lab
        def seg(a, b): return I[b] - I[a]
        S, U, LRC = Pm['S'], Pm['U'], Pm['LRC']
        c = {}
        c['n_instr'] = len(A.ins)
        c['setwalk'] = seg('setwalk', 'sw_end') + 1                                  # with the return
        c['restart'] = (seg('restart', 'rs1') - 1) + seg('rs1', 'setwalk') + c['setwalk']   # the cap check passes (no HALT)
        c['restart_halt'] = seg('restart', 'rs1') - 1 + 1                           # the last call: compare, branch not taken, HALT
        c['hit'] = (seg('hit', 'h1') - 1) + seg('h1', 'dpl') + 2                     # per processed hit, no DP walk
        c['ctz_clear'] = seg('dp1', 'gather')
        c['gather'] = seg('gather', 'record')
        c['record_slot'] = seg('record', 'sl_ok')
        c['probe_word'] = 1 + 7 + 8 * (RPW - 1) + 3                                  # load, four occupied non-matching records, next word
        c['probe_wrap'] = 2
        c['probe_end'] = 1 + 7 + 8 * (RPW - 2) + 4                                   # load, three records passed, the fourth: shift, mask, empty test
        c['empty_tail'] = 2 + 1 + 1 + 3                                              # shift, or, store, jump; move, call, jump back
        c['dp_fixed'] = 2 + c['ctz_clear'] + c['gather'] + c['record_slot'] + c['probe_end'] + c['probe_wrap'] + c['empty_tail']
        c['dp_max'] = c['dp_fixed'] + c['probe_word'] * S                            # at most S occupied words passed
        c['dl_final'] = seg('dl', 'restart')                                         # c = Tb: the HALT (the compare and branch are in the iteration's 3)
        c['e_eval'] = seg('evalF', 'outm') - 1 + UNIT                                # one evaluation of F with the permutation, with the return
        c['e_outm'] = seg('outm', 'match')                                           # the message builder, with the return
        e = c['e_eval']
        c['match_entry'] = 3 + seg('match', 'meas')                                  # trail number from the record (3), entry (9: with the lb test 2)
        c['meas_iter'] = e + 8                                                       # one measuring evaluation without the DP
        c['meas_last'] = e + 4                                                       # the evaluation that lands on the DP
        c['replay_iter'] = 13 + 2 * e                                                # one lock-step iteration (not found)
        # success after k lock-step iterations, la measured: 12 + (la - 1)(e + 8) + (e + 4) + 2 + 2 + n (7 + e) + 2 + 2
        #   + (k - 1)(13 + 2e) + (9 + 2e) + 67; exhaustion: ... + m (13 + 2e) + 3.  Largest at la = lb = k = LRC:
        #   (e + 8 + 13 + 2e) LRC + 12 - 4 + 2 + 2 + 2 + 2 - 13 + 9 + 67
        c['replay_const'] = c['match_entry'] - 4 + 2 + 2 + 2 + 2 - 13 + 9 + 67
        c['replay_max'] = (c['meas_iter'] + c['replay_iter']) * LRC + c['replay_const']
        c['setup'] = seg('start', 'clr') + (S // 8) * 11 + 1 + 256 * (7 + c['setwalk'])
        return c


    def pf_bytes(PFLO, PFN):
        return sl_bytes(b'', PFLO, PFN)



    # Packed construction uses the emitted 32-byte image as its work buffer.
    # Forward references retain only (instruction index, label ID) pairs.
    BaseAsm = Asm
    class PackedAsm(BaseAsm):
        def __init__(self):
            self.buf = bytearray()
            self.lab = {}
            self.fix = []
        def pc(self):
            return len(self.buf) // 32
        def label(self, name):
            assert name not in self.lab and len(self.lab) < 256
            self.lab[name] = self.pc()
        def e(self, op, d=0, a=0, b=0, imm=0, tgt=None):
            assert self.pc() < 2800
            assert 0 <= imm < 1 << 192 and max(d, a, b) < 2192
            if tgt is not None:
                assert len(self.fix) < 256
                self.fix.append((self.pc(), tgt))
            self.buf.extend(enc((op, d, a, b, imm)))
        def resolve(self):
            for index, name in self.fix:
                address = self.lab[name]
                self.buf[32*index+8:32*index+32] = address.to_bytes(24, 'little')

    A = program(PARAMS)
    audit(A)
    Asm = PackedAsm
    packed = program(PARAMS)
    Asm = BaseAsm
    assert bytes(packed.buf) == b''.join(enc(x) for x in A.ins)
    assert packed.lab == A.lab

    binary = b''.join(enc(x) for x in A.ins)
    assert dec(binary) == [tuple(x) for x in A.ins]
    c = counts(A, PARAMS)
    expected = dict(n_instr=2706, hit=117, setwalk=1283, restart=1289,
                    restart_halt=3, dp_fixed=1115, probe_word=35,
                    replay_const=79, setup=361752)
    for key, value in expected.items():
        assert c[key] == value, (key, c[key], value)
    assert len(binary) == 86592
    pf = pf_bytes(242, 14)
    assert len(pf) == 65
    # Execute the encoded OR filter on zero and every one-hot input plane.
    # These basis tests cover each input's inclusion in this OR-only circuit.
    for bit in range(-1, 256):
        regs = [0] * NREGS
        if bit >= 0: regs[bit] = M256
        for pos in range(0, len(pf), 5):
            inst = int.from_bytes(pf[pos:pos+5], 'little')
            op = inst & 7
            d, a, b = (inst >> 3) & 4095, (inst >> 15) & 4095, (inst >> 27) & 4095
            assert op == 2
            regs[d] = regs[a] | regs[b]
        assert regs[PF] == (M256 if bit >= 242 else 0)
        rest = 0
        for j in range(145, 242): rest |= regs[j]
        assert (rest | regs[PF]) == (M256 if bit >= 145 else 0)
    rom, loader_obs = check_literal_loader(A.ins, A.lab, A.fix)
    return rom, loader_obs, {'assembly_instructions': len(A.ins), 'assembly_bytes': len(binary),
            'prefilter_bytes': len(pf), 'prefilter_basis_cases': 257,
            'assembly_labels': len(A.lab), 'assembly_fixups': len(packed.fix),
            'packed_assembly_equal': 1}


def main():
    rom, loader_observations, assembly_observations = check_current_assembly()
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
            out.append({"trial": tr["trial"], "message_a_hex": ma.hex(), "message_b_hex": mb.hex(), "observations": obs[t]})
    elif req["experiment_id"] == "proj-w256":
        done = proj_w(trials, step, PD)
        for t, tr in enumerate(trials):
            if done[t] is None:
                out.append({"trial": tr["trial"], "message_a_hex": None, "message_b_hex": None})
            else:
                a, b, s = done[t]
                out.append({"trial": tr["trial"], "message_a_hex": msg_of(a).hex(), "message_b_hex": msg_of(b).hex(), "observations": {"step": s}})
    else:
        raise ValueError("unknown experiment")
    if req["experiment_id"] == "proj-w256":
        assert len(rom) <= 11 * len(out), "insufficient trial slots for full ROM evidence"
    for index, result in enumerate(out):
        if req['experiment_id'] == 'proj-w256':
            # Numeric ROM evidence is distributed across trials within the
            # organizer's 16-observation limit. No hash event is changed.
            obs = dict(loader_observations)
            for k in range(11):
                pos = index*11+k
                if pos < len(rom):obs['rom_%d' % k]=rom[pos]
            result['observations']=obs
        else:
            result.setdefault('observations',{}).update(assembly_observations)
            result['observations'].update(loader_observations)
    json.dump({"schema_version": 1, "trials": out}, sys.stdout, separators=(",", ":"), sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
