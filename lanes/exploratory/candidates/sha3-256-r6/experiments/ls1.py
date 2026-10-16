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

M64 = (1 << 64) - 1
RCA = [0x1, 0x8082, 0x800000000000808A, 0x8000000080008000, 0x808B, 0x80000001, 0x8000000080008081, 0x8000000000008009,
       0x8A, 0x88, 0x80008009, 0x8000000A, 0x8000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003,
       0x8000000000008002, 0x8000000000000080, 0x800A, 0x800000008000000A, 0x8000000080008081, 0x8000000000008080,
       0x80000001, 0x8000000080008008]
ROT = [[0, 36, 3, 41, 18], [1, 44, 10, 45, 2], [62, 6, 43, 15, 61], [28, 55, 25, 21, 56], [27, 20, 39, 8, 14]]
TRIAL = 18                        # constants of the C generator's trial 18 (best of 32)
PROG_SHA256 = "0843edaec30efd8160d4f8686af87226c1ad9da7e636c44d7bb1bcaad733b202"
NINSTR = 27391
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
        before = len(self.op)
        n = self.consn(O_NOT, a[0], 0)
        if len(self.op) > before and self.lin[a[0]] >= 0:
            self.lin[n] = self.lin[a[0]]; self.k[n] = self.k[a[0]] ^ 1
        return (n, a[1] ^ 1)

    def and2(self, a, b):
        if a[0] == NC: return b if a[1] else (NC, 0)
        if b[0] == NC: return a if b[1] else (NC, 0)
        if a[0] == b[0]: return a if a[1] == b[1] else (NC, 0)
        if a[1] == 0 and b[1] == 0: return (self.consn(O_AND, a[0], b[0]), 0)
        if a[1] == 1 and b[1] == 1: return (self.consn(O_OR, a[0], b[0]), 1)
        A, B = (a[0], b[0]) if a[1] == 0 else (b[0], a[0])
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
            w = []
            for Y in range(5):
                b = [rotl64(P[((3 * Y + X) % 5) + 5 * X] ^ D[(3 * Y + X) % 5], ROT[(3 * Y + X) % 5][X]) for X in range(5)]
                for X in range(5): w.append(b[X] ^ b[(X + 1) % 5])
            base0[Y0][X0] = w
    phi = [[[0] * 32 for _ in range(64)] for _ in range(5)]
    for Y in range(5):
        for z in range(64):
            bz = [0] * 5
            for X in range(5):
                v = 0
                for k, wk in enumerate(base0[Y][X]):
                    if wk: v |= rotl64(wk, z) << (64 * k)
                bz[X] = v
            row = phi[Y][z]
            for pm in range(1, 32):
                lsb = pm & -pm
                row[pm] = row[pm ^ lsb] ^ bz[lsb.bit_length() - 1]
    return phi


ROW_PHI = _make_row_phi()


def eval_phi(phi, last_next):
    if not last_next:
        return 2560 - (phi.bit_count() >> 1)
    e0 = M64 ^ ((phi >> 64) & M64)
    e1 = M64 ^ ((phi >> 128) & M64)
    e2 = M64 ^ ((phi >> 192) & M64)
    e3 = M64 ^ ((phi >> 256) & M64)
    m1 = e0 & e1
    m2 = ~m1 & e1 & e2
    m3 = ~m2 & e2 & e3
    return 256 + (e0 ^ m1).bit_count() + (e1 ^ m2).bit_count() + (e2 ^ m3).bit_count() + e3.bit_count()


def get_row_cands(s_info, avail, max_rc):
    INF = 1 << 29
    min_rc = [INF] * 32
    best_s = [0] * 32
    best_f = [0] * 32
    for s, term_c, base_pm in s_info:
        base_rc = term_c + (s & ~avail).bit_count()
        if base_rc > max_rc: continue
        free_f = s | avail
        f = free_f
        while True:
            pm = base_pm ^ f
            if base_rc < min_rc[pm]:
                min_rc[pm] = base_rc; best_s[pm] = s; best_f[pm] = f
            if f == 0: break
            f = (f - 1) & free_f
    return [(pm, best_s[pm], best_f[pm], min_rc[pm]) for pm in range(32) if min_rc[pm] <= max_rc]


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
    for r in range(6):
        last = r == 5
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
        row_tc = [[[0] * 32 for _ in range(64)] for _ in range(nY)]
        row_sinfo = [[None] * 64 for _ in range(nY)]
        for Y in range(nY):
            for z in range(64):
                b = B_row[Y][z]
                hn = 0
                for X in range(5):
                    y, x = X, (3 * Y + X) % 5
                    zz = (z - ROT[x][y]) & 63
                    v = g.xorv(S[x + 5 * y][zz], D_[x][zz])
                    b[X] = v
                    if v[0] != NC and g.has_cons(O_NOT, v[0], 0): hn |= 1 << X
                has_not[Y][z] = hn
                rc_bit0 = ((RCA[r] >> z) & 1) if Y == 0 else 0
                sinfo = []
                tc_arr = row_tc[Y][z]
                for s in range(32):
                    bb = list(b); bad = False
                    for X in range(5):
                        if (s >> X) & 1:
                            if b[X][0] == NC: bad = True; break
                            bb[X] = (b[X][0], b[X][1] ^ 1)
                    if bad:
                        tc_arr[s] = 1 << 29
                        continue
                    tc = 0
                    for X in range(5):
                        if (need >> X) & 1: tc += cost_term(bb[(X + 1) % 5], bb[(X + 2) % 5])
                    tc_arr[s] = tc
                    if tc <= 6:
                        bpm = 0
                        for X in range(5):
                            if (need >> X) & 1:
                                tp = t_pol(bb[(X + 1) % 5], bb[(X + 2) % 5])
                                bpm |= (b[X][1] ^ tp ^ (rc_bit0 if X == 0 else 0)) << X
                        sinfo.append((s, tc, bpm))
                row_sinfo[Y][z] = sinfo

        not_uses = [0] * (len(g.op) + 64)
        chosen_s = [[0] * 64 for _ in range(nY)]
        chosen_f = [[0] * 64 for _ in range(nY)]
        cur_pm = [[0] * 64 for _ in range(nY)]
        cur_phi = 0

        def get_avail(Y, z):
            b = B_row[Y][z]; av = has_not[Y][z]
            for X in range(5):
                if b[X][0] != NC and not_uses[b[X][0]] > 0: av |= 1 << X
            return av

        for Y in range(nY):
            for z in range(64):
                b = B_row[Y][z]; av = get_avail(Y, z); tc_arr = row_tc[Y][z]
                best, bc = -1, 1 << 30
                for s in range(32):
                    c = tc_arr[s] + (s & ~av).bit_count()
                    if c < bc: bc, best = c, s
                chosen_s[Y][z] = best; chosen_f[Y][z] = best
                for X in range(5):
                    if (best >> X) & 1: not_uses[b[X][0]] += 1
                bpm = next(pm for s, _, pm in row_sinfo[Y][z] if s == best) ^ best
                cur_pm[Y][z] = bpm
                cur_phi ^= ROW_PHI[Y][z][bpm]

        if 1 <= r < 5:
            last_next = (r + 1 == 5)
            cur_next_score = eval_phi(cur_phi, last_next)

            def try_pair(Y1, z1, Y2, z2):
                nonlocal cur_phi, cur_next_score
                if Y1 == Y2 and z1 == z2: return False
                b1, b2 = B_row[Y1][z1], B_row[Y2][z2]
                if r == 1 and z1 != z2:
                    s1n = {b1[i][0] for i in range(5) if b1[i][0] != NC}
                    if any(b2[j][0] in s1n for j in range(5)): return False
                os1, of1 = chosen_s[Y1][z1], chosen_f[Y1][z1]; ou1 = os1 | of1
                os2, of2 = chosen_s[Y2][z2], chosen_f[Y2][z2]; ou2 = os2 | of2
                orc1, orc2 = row_tc[Y1][z1][os1], row_tc[Y2][z2][os2]
                hn1, hn2 = has_not[Y1][z1], has_not[Y2][z2]
                for X in range(5):
                    if (ou1 >> X) & 1:
                        not_uses[b1[X][0]] -= 1
                        if not_uses[b1[X][0]] == 0 and not ((hn1 >> X) & 1): orc1 += 1
                for X in range(5):
                    if (ou2 >> X) & 1:
                        not_uses[b2[X][0]] -= 1
                        if not_uses[b2[X][0]] == 0 and not ((hn2 >> X) & 1): orc2 += 1
                c1 = get_row_cands(row_sinfo[Y1][z1], get_avail(Y1, z1), orc1 + 1)
                c2 = get_row_cands(row_sinfo[Y2][z2], get_avail(Y2, z2), orc2 + 1)
                bs1, bf1, bs2, bf2 = os1, of1, os2, of2
                bpm1, bpm2 = cur_pm[Y1][z1], cur_pm[Y2][z2]
                best_tot = orc1 + orc2 + cur_next_score
                best_ns = cur_next_score
                rp1, rp2 = ROW_PHI[Y1][z1], ROW_PHI[Y2][z2]
                base_phi = cur_phi ^ rp1[bpm1] ^ rp2[bpm2]
                max_rc12 = orc1 + orc2 + 1
                imp = False
                for pm1, s1, f1, rc1 in c1:
                    p1 = base_phi ^ rp1[pm1]
                    for pm2, s2, f2, rc2 in c2:
                        rc12 = rc1 + rc2
                        if rc12 > max_rc12: continue
                        ns = eval_phi(p1 ^ rp2[pm2], last_next)
                        if rc12 + ns < best_tot:
                            best_tot = rc12 + ns; best_ns = ns
                            bs1, bf1, bpm1 = s1, f1, pm1
                            bs2, bf2, bpm2 = s2, f2, pm2
                            imp = True
                chosen_s[Y1][z1], chosen_f[Y1][z1], cur_pm[Y1][z1] = bs1, bf1, bpm1
                chosen_s[Y2][z2], chosen_f[Y2][z2], cur_pm[Y2][z2] = bs2, bf2, bpm2
                cur_phi = base_phi ^ rp1[bpm1] ^ rp2[bpm2]
                cur_next_score = best_ns
                nu1, nu2 = bs1 | bf1, bs2 | bf2
                for X in range(5):
                    if (nu1 >> X) & 1: not_uses[b1[X][0]] += 1
                    if (nu2 >> X) & 1: not_uses[b2[X][0]] += 1
                return imp

            no_imp = 0
            for _ in range(15):
                if no_imp >= 3: break
                imp = False
                for Y in range(nY):
                    for z in range(64):
                        b = B_row[Y][z]; hn = has_not[Y][z]
                        os, of = chosen_s[Y][z], chosen_f[Y][z]; ou = os | of
                        orc = row_tc[Y][z][os]
                        for X in range(5):
                            if (ou >> X) & 1:
                                not_uses[b[X][0]] -= 1
                                if not_uses[b[X][0]] == 0 and not ((hn >> X) & 1): orc += 1
                        cands = get_row_cands(row_sinfo[Y][z], get_avail(Y, z), orc + 1)
                        bs, bf, bpm = os, of, cur_pm[Y][z]
                        best_tot = orc + cur_next_score; best_ns = cur_next_score
                        rp = ROW_PHI[Y][z]
                        base_phi = cur_phi ^ rp[bpm]
                        for pm, s, f, rc in cands:
                            ns = eval_phi(base_phi ^ rp[pm], last_next)
                            if rc + ns < best_tot:
                                best_tot = rc + ns; best_ns = ns
                                bs, bf, bpm = s, f, pm; imp = True
                        chosen_s[Y][z], chosen_f[Y][z], cur_pm[Y][z] = bs, bf, bpm
                        cur_phi = base_phi ^ rp[bpm]; cur_next_score = best_ns
                        nu = bs | bf
                        for X in range(5):
                            if (nu >> X) & 1: not_uses[b[X][0]] += 1
                no_imp = 0 if imp else no_imp + 1
                if no_imp >= 3: break
                imp = False
                for z in range(64):
                    old_rc, c = [0] * 5, [None] * 5
                    for Y in range(5):
                        b = B_row[Y][z]; hn = has_not[Y][z]
                        os, of = chosen_s[Y][z], chosen_f[Y][z]; ou = os | of
                        orc = row_tc[Y][z][os]
                        for X in range(5):
                            if (ou >> X) & 1:
                                not_uses[b[X][0]] -= 1
                                if not_uses[b[X][0]] == 0 and not ((hn >> X) & 1): orc += 1
                        old_rc[Y] = orc
                        c[Y] = get_row_cands(row_sinfo[Y][z], get_avail(Y, z), orc)
                    best_tot = sum(old_rc) + cur_next_score; best_ns = cur_next_score
                    bs = [chosen_s[Y][z] for Y in range(5)]
                    bf = [chosen_f[Y][z] for Y in range(5)]
                    bpm = [cur_pm[Y][z] for Y in range(5)]
                    rp0, rp1, rp2, rp3, rp4 = (ROW_PHI[Y][z] for Y in range(5))
                    base_phi = cur_phi ^ rp0[bpm[0]] ^ rp1[bpm[1]] ^ rp2[bpm[2]] ^ rp3[bpm[3]] ^ rp4[bpm[4]]
                    for pm0, s0, f0, rc0 in c[0]:
                        p0 = base_phi ^ rp0[pm0]
                        for pm1, s1, f1, rc1 in c[1]:
                            p1 = p0 ^ rp1[pm1]; rc01 = rc0 + rc1
                            for pm2, s2, f2, rc2 in c[2]:
                                p2 = p1 ^ rp2[pm2]; rc012 = rc01 + rc2
                                for pm3, s3, f3, rc3 in c[3]:
                                    p3 = p2 ^ rp3[pm3]; rc0123 = rc012 + rc3
                                    for pm4, s4, f4, rc4 in c[4]:
                                        sum_rc = rc0123 + rc4
                                        ns = eval_phi(p3 ^ rp4[pm4], last_next)
                                        if sum_rc + ns < best_tot:
                                            best_tot = sum_rc + ns; best_ns = ns
                                            bs = [s0, s1, s2, s3, s4]; bf = [f0, f1, f2, f3, f4]; bpm = [pm0, pm1, pm2, pm3, pm4]
                                            imp = True
                    cur_next_score = best_ns
                    cur_phi = base_phi ^ rp0[bpm[0]] ^ rp1[bpm[1]] ^ rp2[bpm[2]] ^ rp3[bpm[3]] ^ rp4[bpm[4]]
                    for Y in range(5):
                        chosen_s[Y][z], chosen_f[Y][z], cur_pm[Y][z] = bs[Y], bf[Y], bpm[Y]
                        nu = bs[Y] | bf[Y]
                        for X in range(5):
                            if (nu >> X) & 1: not_uses[B_row[Y][z][X][0]] += 1
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
        for m, _ in g.form[nf0:]: del g.fidx[m]
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
                b = list(orig_b)
                s, f = chosen_s[Y][z], chosen_f[Y][z]
                for X in range(5):
                    if (s >> X) & 1: b[X] = g.notv(orig_b[X])
                for X in range(5):
                    if (need >> X) & 1:
                        t1 = b[(X + 1) % 5]
                        t = g.and2((t1[0], t1[1] ^ 1), b[(X + 2) % 5])
                        bx = g.notv(orig_b[X]) if ((f >> X) & 1) else orig_b[X]
                        NS[X + 5 * Y][z] = g.xorv(bx, t)
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
def perm(a, rounds):
    for rc in RCA[:rounds]:
        c = [a[x] ^ a[x + 5] ^ a[x + 10] ^ a[x + 15] ^ a[x + 20] for x in range(5)]
        d = [c[(x + 4) % 5] ^ (((c[(x + 1) % 5] << 1) | (c[(x + 1) % 5] >> 63)) & M64) for x in range(5)]
        b = [0] * 25
        for x in range(5):
            for y in range(5):
                v = a[x + 5 * y] ^ d[x]; r = ROT[x][y]
                b[y + 5 * ((2 * x + 3 * y) % 5)] = ((v << r) | (v >> (64 - r))) & M64 if r else v
        for y in range(5):
            for x in range(5):
                a[x + 5 * y] = b[x + 5 * y] ^ (~b[(x + 1) % 5 + 5 * y] & b[(x + 2) % 5 + 5 * y])
        a[0] ^= rc
    return a


def digest(msg, rounds=6):
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
    l[1], l[11], l[6] = u0 ^ KL[1], u1 ^ KL[11], u0 ^ u1 ^ KL[6]
    l[9], l[14], l[4] = u2 ^ KL[9], u3 ^ KL[14], u2 ^ u3 ^ KL[4]
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
W, H, LC, U, TB = 22, 4, 128, 3000, 400


def rho_w(trials, step, PD):
    T = len(trials)
    A = (1 << (256 * T)) - 1
    mask = (1 << W) - 1
    R = [0] * NREG
    seeds = [bytes.fromhex(t["seed"]) for t in trials]
    rho, nid, att, astart = [0] * T, [0] * T, [-1] * T, [0] * T
    table = [dict() for _ in range(T)]
    done = [None] * T
    obs = [dict(steps=0, trails=0, dead=0, attempts=0, stored=0, replay_evals=0) for _ in range(T)]
    lid, lst = [0] * (256 * T), [0] * (256 * T)
    due, pend = {}, []

    def f_small(u):
        return F_ref(u, PD) & mask

    def new_attempt(t, c):
        att[t] += 1; obs[t]['attempts'] += 1
        rho[t] = int.from_bytes(shake(seeds[t] + att[t].to_bytes(4, 'little'), 8), 'little') & mask
        table[t].clear(); nid[t] = 256; astart[t] = c
        for l in range(256):
            g = 256 * t + l
            lid[g] = l; lst[g] = c
            due.setdefault(c + LC, []).append((g, l, att[t]))
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

    def replay(sa, la, sb, lb, t):
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
        dpm = A ^ anyv
        events = []
        while dpm:
            low = dpm & -dpm
            events.append((low.bit_length() - 1, 1))
            dpm ^= low
        for g, ident, at in due.pop(c, []):
            if lid[g] == ident and att[g >> 8] == at: events.append((g, 2))
        events.sort()
        seen, fresh = set(), set()
        for g, kind in events:
            t = g >> 8
            if g in seen or done[t] is not None or t in fresh: continue
            seen.add(g)
            if kind == 1:
                x = lane_value(R, g, W)
                ln = c - lst[g]
                tb = table[t]
                if x in tb:
                    ida, la = tb[x]
                    if ida != lid[g]:
                        r = replay((rho[t] + ida) & mask, la, (rho[t] + lid[g]) & mask, ln, t)
                        if r is not None:
                            done[t] = r; obs[t]['steps'] = c - astart[t]; obs[t]['stored'] = len(tb)
                            continue
                else:
                    tb[x] = (lid[g], ln)
            else:
                obs[t]['dead'] += 1
            if nid[t] >= U:
                new_attempt(t, c); fresh.add(t); continue
            i = nid[t]; nid[t] += 1; obs[t]['trails'] += 1
            lid[g] = i; lst[g] = c
            due.setdefault(c + LC, []).append((g, i, att[t]))
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
    if req["schema_version"] != 1 or req["target_profile"] != "sha3-256-r6-prefix-v1":
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
