"""LS1: distinguished-point collision search on sha3-256-r6-prefix-v1 with a linear-structure message embedding.

Chain function on 256-bit points u (little-endian lanes u0..u3):
  m(u) = 128 bytes = lanes 0..15 of the absorbed state: lane 1 = u0^K1, lane 11 = u1^K11, lane 6 = u0^u1^K6,
  lane 9 = u2^K9, lane 14 = u3^K14, lane 4 = u2^u3^K4, the other lanes 0..15 the constants K below; padding gives lane 16 =
  0x8000000000000006.  F(u) = SHA3-256-r6(m(u)) XOR PD (PD a fixed 256-bit mask).  m is injective, so F(u) = F(u') with
  u != u' gives two distinct messages with equal complete digests.
This program regenerates the bit-sliced straight line of proof.md Section 3 (the same algorithm as the C generator; its
5-byte encoding must hash to PROG_SHA256), checks it against a plain six-round implementation, and runs
  rho-w22   : the search of proof.md Section 4 at width 22 (planes 22..255 zeroed after each step), one pair per trial;
  proj-w256 : eight chained full-width steps from 256 random points, first pair agreeing on the 22 low digest bits.
One Python integer holds a plane for all trials of the request (trial t in bits 256t..256t+255); trials never interact.
"""
import sys, json, hashlib

NR = 6
M64 = (1 << 64) - 1
M320 = (1 << 320) - 1
RCA = [0x1, 0x8082, 0x800000000000808A, 0x8000000080008000, 0x808B, 0x80000001, 0x8000000080008081, 0x8000000000008009,
       0x8A, 0x88, 0x80008009, 0x8000000A, 0x8000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003,
       0x8000000000008002, 0x8000000000000080, 0x800A, 0x800000008000000A, 0x8000000080008081, 0x8000000000008080,
       0x80000001, 0x8000000080008008]
ROT = [[0, 36, 3, 41, 18], [1, 44, 10, 45, 2], [62, 6, 43, 15, 61], [28, 55, 25, 21, 56], [27, 20, 39, 8, 14]]
TRIAL = 27                        # constants of the C generator's trial 27 (best of 32)
PROG_SHA256 = "8c2b8795a9656a0530eb055f71c455e8dbcae1689a63736ad8e3500f4fafd0cc"
NINSTR = 26367
NREG = 2304
NC = -1
O_IN, O_XOR, O_AND, O_OR, O_NOT = 0, 1, 2, 3, 4


def rotl64(v, r):
    return ((v << r) | (v >> (64 - r))) & M64 if r else v


def consts(trial):
    K = [0] * 25
    K[16] = 0x8000000000000006
    W = M64 if (trial & 1) else 0
    r0 = M64 if (trial & 2) else 0
    r1 = M64 if (trial & 4) else 0
    r2 = M64 if (trial & 8) else 0
    r3 = M64 if (trial & 16) else 0
    K[0] = 0; K[5] = M64; K[10] = M64; K[15] = M64
    K[3] = 0; K[8] = 0; K[13] = W
    K[2] = rotl64(W, 3); K[7] = 0; K[12] = 0
    K[1] = r0; K[11] = r1; K[6] = r0 ^ r1 ^ rotl64(W, 1) ^ K[16]
    K[9] = r2; K[14] = r3; K[4] = r2 ^ r3 ^ M64 ^ rotl64(W, 2)
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

    def has_cons(self, op, a, b):
        if op != O_NOT and a > b: a, b = b, a
        return (op, a, b) in self.cons

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
        if self.op[a[0]] == O_NOT:
            return (self.a[a[0]], a[1] ^ 1)
        before = len(self.op)
        n = self.consn(O_NOT, a[0], 0)
        if len(self.op) > before and self.lin[a[0]] >= 0:
            self.lin[n] = self.lin[a[0]]; self.k[n] = self.k[a[0]] ^ 1
        return (n, a[1] ^ 1)

    def and2(self, a, b, sel=0):
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


def t_pol(b1, b2):
    a0, a1 = b1[0], b1[1] ^ 1
    b0, b1_ = b2[0], b2[1]
    if a0 == NC: return b1_ if a1 else 0
    if b0 == NC: return a1 if b1_ else 0
    if a0 == b0: return a1 if a1 == b1_ else 0
    return 1 if (a1 == 1 and b1_ == 1) else 0


def _make_row_phi():
    base0 = [[None] * 5 for _ in range(5)]
    for Y0 in range(5):
        for X0 in range(5):
            P = [0] * 25; P[5 * Y0 + X0] = 1
            C = [P[x] ^ P[x + 5] ^ P[x + 10] ^ P[x + 15] ^ P[x + 20] for x in range(5)]
            D = [C[(x + 4) % 5] ^ rotl64(C[(x + 1) % 5], 1) for x in range(5)]
            w = [0] * 25
            for Y in range(5):
                for X in range(5):
                    w[5 * X + Y] = rotl64(P[((3 * Y + X) % 5) + 5 * X] ^ D[(3 * Y + X) % 5], ROT[(3 * Y + X) % 5][X])
            base0[Y0][X0] = w
    d0 = [None] * 5
    for X0 in range(5):
        C = [1 if x == X0 else 0 for x in range(5)]
        D = [C[(x + 4) % 5] ^ rotl64(C[(x + 1) % 5], 1) for x in range(5)]
        w = [0] * 25
        for Y in range(5):
            for X in range(5):
                w[5 * X + Y] = rotl64(D[(3 * Y + X) % 5], ROT[(3 * Y + X) % 5][X])
        d0[X0] = w
    phi = [[[0] * 32 for _ in range(64)] for _ in range(5)]
    phi_d = [[0] * 32 for _ in range(64)]
    phi_p = [[[0] * 32 for _ in range(64)] for _ in range(5)]
    for z in range(64):
        bzd = [0] * 5
        for X in range(5):
            v = 0
            for k, wk in enumerate(d0[X]):
                if wk: v |= rotl64(wk, z) << (64 * k)
            bzd[X] = v
        rowd = phi_d[z]
        for pm in range(1, 32):
            lsb = pm & -pm
            rowd[pm] = rowd[pm ^ lsb] ^ bzd[lsb.bit_length() - 1]
    for Y in range(5):
        for z in range(64):
            bz = [0] * 5
            for X in range(5):
                v = 0
                for k, wk in enumerate(base0[Y][X]):
                    if wk: v |= rotl64(wk, z) << (64 * k)
                bz[X] = v
            row = phi[Y][z]; rowp = phi_p[Y][z]; rowd = phi_d[z]
            for pm in range(1, 32):
                lsb = pm & -pm
                row[pm] = row[pm ^ lsb] ^ bz[lsb.bit_length() - 1]
                rowp[pm] = row[pm] ^ rowd[pm]
    return phi, phi_d, phi_p


ROW_PHI, PHI_D, PHI_P = _make_row_phi()


def eval_phi(phi, last_next):
    if not last_next:
        b0 = phi & M320
        b1 = (phi >> 320) & M320
        b2 = (phi >> 640) & M320
        b3 = (phi >> 960) & M320
        b4 = (phi >> 1280) & M320
        diff = (b0 ^ b1).bit_count() + (b1 ^ b2).bit_count() + (b2 ^ b3).bit_count() + (b3 ^ b4).bit_count() + (b4 ^ b0).bit_count()
        ox = ((b0 | b1) ^ (b1 | b2) ^ (b2 | b3) ^ (b3 | b4) ^ (b4 | b0)).bit_count()
        return 2240 - (diff >> 1) + ox
    b0 = phi & M64
    b1 = (phi >> 320) & M64
    b2 = (phi >> 640) & M64
    b3 = (phi >> 960) & M64
    b4 = (phi >> 1280) & M64
    nb0, nb1, nb2, nb3, nb4 = M64 ^ b0, M64 ^ b1, M64 ^ b2, M64 ^ b3, M64 ^ b4
    is4 = (b0 & nb4 & ((nb2 & b3) | (nb1 & b2 & nb3))) | (nb0 & nb3 & b4 & (b1 ^ b2))
    is6 = (nb4 & nb0 & ((nb1 & nb2 & nb3) | (b2 & (b1 | b3)))) | (b4 & ((b0 & nb3 & (M64 ^ (b1 ^ b2))) | (b2 & b3 & (b0 | b1))))
    return 320 - is4.bit_count() + is6.bit_count()


def build_row_sinfo(b, need, rc_bit0):
    distinct = all(b[X][0] != NC for X in range(5)) and len({b[X][0] for X in range(5)}) == 5
    jmax = 5 if distinct else 0
    sinfo = []
    for bj in range(-1, jmax):
        if bj >= 0:
            k = (bj + 1) % 5
            if not ((need >> bj) & 1) or not ((need >> k) & 1):
                continue
        for s in range(32):
            bb = list(b); bad = False
            for X in range(5):
                if (s >> X) & 1:
                    if b[X][0] == NC: bad = True; break
                    bb[X] = (b[X][0], b[X][1] ^ 1)
            if bad:
                continue
            tc_base = 0; bpm_base = 0; mix_base = 0
            for X in range(5):
                if X == bj or not ((need >> X) & 1):
                    continue
                c = cost_term(bb[(X + 1) % 5], bb[(X + 2) % 5])
                tp = t_pol(bb[(X + 1) % 5], bb[(X + 2) % 5])
                tc_base += c
                if c == 2: mix_base |= 1 << X
                bpm_base |= (b[X][1] ^ tp ^ (rc_bit0 if X == 0 else 0)) << X
            if bj < 0:
                if tc_base <= 6:
                    sinfo.append((s, -1, 0, 0, tc_base, bpm_base, mix_base))
            else:
                k = (bj + 1) % 5
                tp_k = t_pol(bb[(k + 1) % 5], bb[(k + 2) % 5])
                for fk_eff in (0, 1):
                    req_f = 0; req_sel = 0
                    if fk_eff:
                        if (mix_base >> k) & 1: req_sel = 1 << k
                        else: req_f = 1 << k
                    pk = b[k][1] ^ tp_k ^ fk_eff
                    c_bj = 1 if (pk ^ 1) == bb[(bj + 2) % 5][1] else 2
                    tp_bj = (pk ^ 1) if c_bj == 1 else 0
                    tc = tc_base + c_bj
                    if tc <= 6:
                        mix = (mix_base & ~(1 << k)) | ((1 << bj) if c_bj == 2 else 0)
                        bpm = bpm_base ^ (fk_eff << k) ^ ((b[bj][1] ^ tp_bj ^ (rc_bit0 if bj == 0 else 0)) << bj)
                        sinfo.append((s, bj, req_f, req_sel, tc, bpm, mix))
    return sinfo


def get_row_cands_raw(sinfo, avail, max_rc, need):
    INF = 1 << 29
    min_rc = [INF] * 32
    best_choice = [None] * 32
    for s, bj, req_f, req_sel, tc, base_pm, mix in sinfo:
        u_base = s | req_f
        base_rc = tc + (u_base & ~avail).bit_count()
        if base_rc > max_rc: continue
        free_flip = ((s | avail | mix) & need) & ~(0 if bj < 0 else (1 << ((bj + 1) % 5)))
        sub = free_flip
        while True:
            pm = base_pm ^ sub
            if base_rc < min_rc[pm]:
                min_rc[pm] = base_rc
                f = req_f | (sub & ~mix)
                selm = req_sel | (sub & mix)
                best_choice[pm] = (s, f, selm, bj)
            if sub == 0: break
            sub = (sub - 1) & free_flip
    return [(pm, best_choice[pm], min_rc[pm]) for pm in range(32) if min_rc[pm] <= max_rc]


CAND_TAB = [[[[None] * 32 for _ in range(32)] for _ in range(2)] for _ in range(2)]
for _last_i, _need in enumerate((0x1F, 0x0F)):
    for _rc_bit0 in (0, 1):
        for _p in range(32):
            _si = build_row_sinfo([(X, (_p >> X) & 1) for X in range(5)], _need, _rc_bit0)
            for _av in range(32):
                CAND_TAB[_last_i][_rc_bit0][_p][_av] = get_row_cands_raw(_si, _av, 20, _need)


def build():
    g = Gen()
    for j in range(256):
        n = g.new(O_IN, 0, 0); g.lin[n] = g.fadd(1 << j, n)
    S = [[(NC, (KL[l] >> z) & 1) for z in range(64)] for l in range(25)]
    for z in range(64):
        S[1][z] = (z, (KL[1] >> z) & 1); S[11][z] = (64 + z, (KL[11] >> z) & 1)
        S[9][z] = (128 + z, (KL[9] >> z) & 1); S[14][z] = (192 + z, (KL[14] >> z) & 1)
    for z in range(64):
        S[6][z] = g.xorv(g.xorv((z, 0), (64 + z, 0)), (NC, (KL[6] >> z) & 1))
        S[4][z] = g.xorv(g.xorv((128 + z, 0), (192 + z, 0)), (NC, (KL[4] >> z) & 1))
    for r in range(NR):
        last = r == NR - 1
        C = [[None] * 64 for _ in range(5)]
        D_ = [[None] * 64 for _ in range(5)]
        for x in range(5):
            s = S[x][63]
            for y in range(1, 5): s = g.xorv(s, S[x + 5 * y][63])
            C[x][63] = s
        for z in range(64):
            if z < 63:
                for x in range(5):
                    s = S[x][z]
                    for y in range(1, 5): s = g.xorv(s, S[x + 5 * y][z])
                    C[x][z] = s
            for x in range(5):
                D_[x][z] = g.xorv(C[(x + 4) % 5][z], C[(x + 1) % 5][(z + 63) & 63])
        nY, need = (1, 0x0F) if last else (5, 0x1F)
        nn0, nf0 = len(g.op), len(g.form)
        B_row = [[[None] * 5 for _ in range(64)] for _ in range(nY)]
        has_not = [[0] * 64 for _ in range(nY)]
        row_tab = [[None] * 64 for _ in range(nY)]
        for Y in range(nY):
            for z in range(64):
                b = B_row[Y][z]
                hn = 0; p = 0
                for X in range(5):
                    y, x = X, (3 * Y + X) % 5
                    zz = (z - ROT[x][y]) & 63
                    v = g.xorv(S[x + 5 * y][zz], D_[x][zz])
                    b[X] = v
                    p |= v[1] << X
                    if v[0] != NC and (g.op[v[0]] == O_NOT or g.has_cons(O_NOT, v[0], 0)): hn |= 1 << X
                has_not[Y][z] = hn
                rc_bit0 = ((RCA[r] >> z) & 1) if Y == 0 else 0
                distinct = all(b[X][0] != NC for X in range(5)) and len({b[X][0] for X in range(5)}) == 5
                if distinct:
                    row_tab[Y][z] = CAND_TAB[1 if last else 0][rc_bit0][p]
                else:
                    si = build_row_sinfo(b, need, rc_bit0)
                    row_tab[Y][z] = [get_row_cands_raw(si, av, 20, need) for av in range(32)]

        not_uses = [0] * (len(g.op) + 64)
        chosen = [[None] * 64 for _ in range(nY)]
        cur_pm = [[0] * 64 for _ in range(nY)]
        cur_phi = 0

        def get_avail(Y, z):
            b = B_row[Y][z]; av = has_not[Y][z]
            for X in range(5):
                if b[X][0] != NC and not_uses[b[X][0]] > 0: av |= 1 << X
            return av

        def get_cands(Y, z, max_rc):
            return [x for x in row_tab[Y][z][get_avail(Y, z)] if x[2] <= max_rc]

        def choice_tc(Y, z, ch):
            s, f, selm, bj = ch
            b = B_row[Y][z]
            bb = [(b[X][0], b[X][1] ^ ((s >> X) & 1)) for X in range(5)]
            tc = 0
            for X in range(5):
                if not ((need >> X) & 1): continue
                if X == bj:
                    k = (bj + 1) % 5
                    tp_k = t_pol(bb[(k + 1) % 5], bb[(k + 2) % 5]) ^ ((selm >> k) & 1)
                    pk = b[k][1] ^ ((f >> k) & 1) ^ tp_k
                    tc += 1 if (pk ^ 1) == bb[(bj + 2) % 5][1] else 2
                else:
                    tc += cost_term(bb[(X + 1) % 5], bb[(X + 2) % 5])
            return tc

        for Y in range(nY):
            for z in range(64):
                b = B_row[Y][z]
                cands = row_tab[Y][z][get_avail(Y, z)]
                pm, ch, rc = min(cands, key=lambda x: (x[2], x[0]))
                chosen[Y][z] = ch
                u = ch[0] | ch[1]
                for X in range(5):
                    if (u >> X) & 1: not_uses[b[X][0]] += 1
                cur_pm[Y][z] = pm
                cur_phi ^= ROW_PHI[Y][z][pm]

        if 1 <= r < 5:
            last_next = (r + 1 == 5)
            cur_next_score = eval_phi(cur_phi, last_next)

            def unuse_row(Y, z):
                b = B_row[Y][z]; hn = has_not[Y][z]
                ch = chosen[Y][z]; ou = ch[0] | ch[1]
                orc = choice_tc(Y, z, ch)
                for X in range(5):
                    if (ou >> X) & 1:
                        not_uses[b[X][0]] -= 1
                        if not_uses[b[X][0]] == 0 and not ((hn >> X) & 1): orc += 1
                return orc

            def use_row(Y, z, ch, pm):
                chosen[Y][z] = ch; cur_pm[Y][z] = pm
                b = B_row[Y][z]; nu = ch[0] | ch[1]
                for X in range(5):
                    if (nu >> X) & 1: not_uses[b[X][0]] += 1

            def try_pair(Y1, z1, Y2, z2):
                nonlocal cur_phi, cur_next_score
                if Y1 == Y2 and z1 == z2: return False
                b1, b2 = B_row[Y1][z1], B_row[Y2][z2]
                if r == 1 and z1 != z2:
                    s1n = {b1[i][0] for i in range(5) if b1[i][0] != NC}
                    if any(b2[j][0] in s1n for j in range(5)): return False
                och1, och2 = chosen[Y1][z1], chosen[Y2][z2]
                orc1 = unuse_row(Y1, z1)
                orc2 = unuse_row(Y2, z2)
                c1 = get_cands(Y1, z1, orc1 + 1)
                c2 = get_cands(Y2, z2, orc2 + 1)
                bch1, bch2 = och1, och2
                bpm1, bpm2 = cur_pm[Y1][z1], cur_pm[Y2][z2]
                best_tot = orc1 + orc2 + cur_next_score
                best_ns = cur_next_score
                rp1, rp2 = ROW_PHI[Y1][z1], ROW_PHI[Y2][z2]
                base_phi = cur_phi ^ rp1[bpm1] ^ rp2[bpm2]
                max_rc12 = orc1 + orc2 + 1
                imp = False
                for pm1, ch1, rc1 in c1:
                    p1 = base_phi ^ rp1[pm1]
                    for pm2, ch2, rc2 in c2:
                        rc12 = rc1 + rc2
                        if rc12 > max_rc12: continue
                        ns = eval_phi(p1 ^ rp2[pm2], last_next)
                        if rc12 + ns < best_tot:
                            best_tot = rc12 + ns; best_ns = ns
                            bch1, bpm1 = ch1, pm1
                            bch2, bpm2 = ch2, pm2
                            imp = True
                use_row(Y1, z1, bch1, bpm1)
                use_row(Y2, z2, bch2, bpm2)
                cur_phi = base_phi ^ rp1[bpm1] ^ rp2[bpm2]
                cur_next_score = best_ns
                return imp

            no_imp = 0
            for _ in range(15):
                if no_imp >= 3: break
                imp = False
                for Y in range(nY):
                    for z in range(64):
                        och, bpm = chosen[Y][z], cur_pm[Y][z]
                        orc = unuse_row(Y, z)
                        cands = get_cands(Y, z, orc + 1)
                        bch = och
                        best_tot = orc + cur_next_score; best_ns = cur_next_score
                        rp = ROW_PHI[Y][z]
                        base_phi = cur_phi ^ rp[bpm]
                        for pm, ch, rc in cands:
                            ns = eval_phi(base_phi ^ rp[pm], last_next)
                            if rc + ns < best_tot:
                                best_tot = rc + ns; best_ns = ns
                                bch, bpm = ch, pm; imp = True
                        use_row(Y, z, bch, bpm)
                        cur_phi = base_phi ^ rp[bpm]; cur_next_score = best_ns
                no_imp = 0 if imp else no_imp + 1
                if no_imp >= 3: break
                imp = False
                for z in range(64):
                    old_rc, c = [0] * 5, [None] * 5
                    for Y in range(5):
                        old_rc[Y] = unuse_row(Y, z)
                        c[Y] = get_cands(Y, z, old_rc[Y])
                    best_tot = sum(old_rc) + cur_next_score
                    bch = [chosen[Y][z] for Y in range(5)]
                    bpm = [cur_pm[Y][z] for Y in range(5)]
                    rp0, rp1, rp2, rp3, rp4 = (ROW_PHI[Y][z] for Y in range(5))
                    pp0, pp1, pp2, pp3, pp4 = (PHI_P[Y][z] for Y in range(5))
                    pd = PHI_D[z]
                    base_phi = cur_phi ^ rp0[bpm[0]] ^ rp1[bpm[1]] ^ rp2[bpm[2]] ^ rp3[bpm[3]] ^ rp4[bpm[4]]
                    best_key = (best_tot, -1, -1, -1, -1, -1)
                    for cm in range(32):
                        phi_cm = base_phi ^ pd[cm]
                        bns = eval_phi(phi_cm, last_next)
                        dp = [(rc0 + eval_phi(phi_cm ^ pp0[pm0], last_next), (pm0,), (ch0,), pm0) for pm0, ch0, rc0 in c[0]]
                        for Y, ppY in ((1, pp1), (2, pp2), (3, pp3)):
                            wY = [(pm, rc + eval_phi(phi_cm ^ ppY[pm], last_next) - bns, ch) for pm, ch, rc in c[Y]]
                            ndp = [None] * 32
                            for w0, pms, chs, m0 in dp:
                                for pm, w, ch in wY:
                                    nm = m0 ^ pm
                                    nw = w0 + w
                                    npms = pms + (pm,)
                                    cur = ndp[nm]
                                    if cur is None or nw < cur[0] or (nw == cur[0] and npms < cur[1]):
                                        ndp[nm] = (nw, npms, chs + (ch,), nm)
                            dp = [x for x in ndp if x is not None]
                        dp_map = {x[3]: x for x in dp}
                        for pm4, ch4, rc4 in c[4]:
                            prev = dp_map.get(cm ^ pm4)
                            if prev is None:
                                continue
                            tot = prev[0] + rc4 + eval_phi(phi_cm ^ pp4[pm4], last_next) - bns
                            pms5 = prev[1] + (pm4,)
                            key = (tot, *pms5)
                            if key < best_key:
                                best_key = key
                                bpm = list(pms5)
                                bch = list(prev[2]) + [ch4]
                                imp = True
                    cur_phi = base_phi ^ rp0[bpm[0]] ^ rp1[bpm[1]] ^ rp2[bpm[2]] ^ rp3[bpm[3]] ^ rp4[bpm[4]]
                    cur_next_score = eval_phi(cur_phi, last_next)
                    for Y in range(5):
                        use_row(Y, z, bch[Y], bpm[Y])
                no_imp = 0 if imp else no_imp + 1
                if no_imp >= 3: break
                imp = False
                for z in range(64):
                    for Y1 in range(4):
                        for Y2 in range(Y1 + 1, 5):
                            if try_pair(Y1, z, Y2, z): imp = True
                no_imp = 0 if imp else no_imp + 1
                if no_imp >= 3: break
                imp = False
                for _ in range(2):
                    imp4 = False
                    for z in range(64):
                        zn = (z + 1) & 63
                        for Y1 in range(5):
                            for Y2 in range(5):
                                if r > 1 or Y1 == Y2:
                                    if try_pair(Y1, z, Y2, zn): imp4 = True
                    imp = imp or imp4
                    if not imp4: break
                no_imp = 0 if imp else no_imp + 1
                if no_imp >= 3: break

        del g.op[nn0:], g.a[nn0:], g.b[nn0:], g.k[nn0:], g.lin[nn0:]
        for m_, _ in g.form[nf0:]: del g.fidx[m_]
        del g.form[nf0:]
        g.cons = {k: v for k, v in g.cons.items() if v < nn0}
        NS = [row[:] for row in S]
        for Y in range(nY):
            for z in range(64):
                orig_b = []
                for X in range(5):
                    y, x = X, (3 * Y + X) % 5
                    zz = (z - ROT[x][y]) & 63
                    orig_b.append(g.xorv(S[x + 5 * y][zz], D_[x][zz]))
                s, f, selm, bj = chosen[Y][z]
                nb = [g.notv(orig_b[X]) if (((s | f) >> X) & 1) else None for X in range(5)]
                b = [nb[X] if ((s >> X) & 1) else orig_b[X] for X in range(5)]
                fb = [nb[X] if ((f >> X) & 1) else orig_b[X] for X in range(5)]
                if bj >= 0:
                    k = (bj + 1) % 5
                    t1 = b[(k + 1) % 5]
                    t = g.and2((t1[0], t1[1] ^ 1), b[(k + 2) % 5], (selm >> k) & 1)
                    NS[k + 5 * Y][z] = g.xorv(fb[k], t)
                for X in range(5):
                    if (need >> X) & 1:
                        if bj >= 0 and X == k: continue
                        t1 = NS[k + 5 * Y][z] if X == bj else b[(X + 1) % 5]
                        t = g.and2((t1[0], t1[1] ^ 1), b[(X + 2) % 5], (selm >> X) & 1)
                        NS[X + 5 * Y][z] = g.xorv(fb[X], t)
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
    l[1], l[11], l[6], l[9], l[14], l[4] = u0 ^ KL[1], u1 ^ KL[11], u0 ^ u1 ^ KL[6], u2 ^ KL[9], u3 ^ KL[14], u2 ^ u3 ^ KL[4]
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


def main():
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
    json.dump({"schema_version": 1, "trials": out}, sys.stdout, separators=(",", ":"), sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
