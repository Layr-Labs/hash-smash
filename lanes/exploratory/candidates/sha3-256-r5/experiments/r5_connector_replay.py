"""Organizer experiment for our sha3-256-r5 package (stdlib only, deterministic).

Once per run it rebuilds the connector space of construction C from the stored witness
(x = L(s) of message 1, beta0, beta1, alpha1) with the committed linearisation seed:
E_pad + E_0, the witness-anchored non-full linearisation and the linearised E_1, and
reports the ranks. It then derives the certificate pair from the stored Gray-code index.
Per trial it draws a fresh point of the rebuilt space from the trial seed and checks
(observations) that both 135-byte messages pad to the fixed block and that the pair has
the exact 2-round difference alpha2. Every trial returns the certificate pair.
"""
import hashlib
import json
import random
import sys

RC = (0x0000000000000001, 0x0000000000008082, 0x800000000000808A,
      0x8000000080008000, 0x000000000000808B)
RHO = (0, 1, 62, 28, 27, 36, 44, 6, 55, 20, 3, 10, 43, 25, 39,
       41, 45, 15, 21, 8, 18, 2, 61, 56, 14)
M64 = (1 << 64) - 1
NB = 1600


def rot(v, n):
    n %= 64
    return ((v << n) | (v >> (64 - n))) & M64 if n else v


def to_lanes(s):
    return [(s >> (64 * i)) & M64 for i in range(25)]


def from_lanes(a):
    s = 0
    for i in range(25):
        s |= a[i] << (64 * i)
    return s


def theta_l(a):
    c = [a[x] ^ a[x + 5] ^ a[x + 10] ^ a[x + 15] ^ a[x + 20] for x in range(5)]
    d = [c[(x - 1) % 5] ^ rot(c[(x + 1) % 5], 1) for x in range(5)]
    return [a[i] ^ d[i % 5] for i in range(25)]


def rhopi_l(a):
    b = [0] * 25
    for y in range(5):
        for x in range(5):
            b[y + 5 * ((2 * x + 3 * y) % 5)] = rot(a[x + 5 * y], RHO[x + 5 * y])
    return b


def chi_l(b):
    return [b[i] ^ ((~b[(i % 5 + 1) % 5 + 5 * (i // 5)]) & b[(i % 5 + 2) % 5 + 5 * (i // 5)]) & M64
            for i in range(25)]


def L(s):
    return from_lanes(rhopi_l(theta_l(to_lanes(s))))


def chi(s):
    return from_lanes(chi_l(to_lanes(s)))


def rounds_from_chi_input(x, first_round, last_round):
    """x is the chi input of round first_round; returns the state after round last_round."""
    a = chi_l(to_lanes(x))
    a[0] ^= RC[first_round]
    for i in range(first_round + 1, last_round + 1):
        a = chi_l(rhopi_l(theta_l(a)))
        a[0] ^= RC[i]
    return from_lanes(a)


def perm5(s):
    a = to_lanes(s)
    for i in range(5):
        a = chi_l(rhopi_l(theta_l(a)))
        a[0] ^= RC[i]
    return from_lanes(a)


def bit(x, y, z):
    return 64 * (x + 5 * y) + z


def row_val(s, r):
    y, z = divmod(r, 64)
    v = 0
    for x in range(5):
        v |= ((s >> bit(x, y, z)) & 1) << x
    return v


def row_bits(r):
    y, z = divmod(r, 64)
    return [bit(x, y, z) for x in range(5)]


def chi5(v):
    o = 0
    for i in range(5):
        b = ((v >> i) & 1) ^ ((((v >> ((i + 1) % 5)) & 1) ^ 1) & ((v >> ((i + 2) % 5)) & 1))
        o |= b << i
    return o


CHI5 = [chi5(v) for v in range(32)]
DDT = [[0] * 32 for _ in range(32)]
VMASK = [[0] * 32 for _ in range(32)]
for _d in range(32):
    for _v in range(32):
        _o = CHI5[_v] ^ CHI5[_v ^ _d]
        DDT[_d][_o] += 1
        VMASK[_d][_o] |= 1 << _v


def popcount(v):
    return bin(v).count("1")


# ---------- affine subspaces of GF(2)^5 -----------------------------------------------------

def _span(vecs):
    sp = {0}
    for v in vecs:
        sp |= {u ^ v for u in sp}
    return sp


def _all_affine():
    # enumerate linear subspaces by spans of up to 5 vectors (dedupe by point mask)
    frontier = {1}
    dims = {1: 0}
    for _ in range(5):
        nxt = set()
        for m in frontier:
            pts = [v for v in range(32) if (m >> v) & 1]
            for v in range(32):
                if (m >> v) & 1:
                    continue
                nm = m
                for p in pts:
                    nm |= 1 << (p ^ v)
                if nm not in dims:
                    dims[nm] = dims[m] + 1
                    nxt.add(nm)
        frontier = nxt
    out = []
    for m, dm in dims.items():
        pts = [v for v in range(32) if (m >> v) & 1]
        seen = set()
        for a in range(32):
            am = 0
            for p in pts:
                am |= 1 << (p ^ a)
            if am in seen:
                continue
            seen.add(am)
            out.append((am, dm))
    return out


AFF = _all_affine()  # list of (point mask, dim); 2451 entries


def affine_eqs(mask):
    """Equations (u, k) with u.v = k on all points of the affine set `mask` (a basis of them)."""
    pts = [v for v in range(32) if (mask >> v) & 1]
    eqs = []
    span_u = {0}
    for u in range(1, 32):
        ks = {popcount(u & p) & 1 for p in pts}
        if len(ks) == 1 and u not in span_u:
            eqs.append((u, ks.pop()))
            span_u |= {w ^ u for w in span_u}
    return eqs


def affine_form(mask, fbit):
    """(g, c) with chi bit fbit = g.v ^ c on every point of mask, or None."""
    pts = [v for v in range(32) if (mask >> v) & 1]
    for g in range(32):
        c = ((CHI5[pts[0]] >> fbit) & 1) ^ (popcount(g & pts[0]) & 1)
        if all((((CHI5[p] >> fbit) & 1) ^ (popcount(g & p) & 1)) == c for p in pts):
            return g, c
    return None


# ---------- linear layer as row vectors ------------------------------------------------------

def _l_rows():
    """rows[j] = set of input bits (as int) whose XOR is output bit j of L."""
    cols = [L(1 << i) for i in range(NB)]
    rows = [0] * NB
    for i, cv in enumerate(cols):
        while cv:
            lb = cv & -cv
            j = lb.bit_length() - 1
            rows[j] |= 1 << i
            cv ^= lb
    return rows


def _invert(rows):
    """Rows of the inverse of the matrix given by rows (row j: output j = rows[j] . input)."""
    n = len(rows)
    aug = [(rows[j], 1 << j) for j in range(n)]
    piv = {}
    for j in range(n):
        a, b = aug[j]
        while a:
            hb = a.bit_length() - 1
            if hb in piv:
                pa, pb = piv[hb]
                a ^= pa
                b ^= pb
            else:
                piv[hb] = (a, b)
                break
    # back-substitute to identity
    order = sorted(piv)
    for hb in order:
        a, b = piv[hb]
        rest = a ^ (1 << hb)
        while rest:
            h2 = rest.bit_length() - 1
            pa, pb = piv[h2]
            a ^= pa
            b ^= pb
            rest = a ^ (1 << hb)
        piv[hb] = (a, b)
    # piv[i] = (e_i, combo) means input_i = XOR of outputs in combo
    return [piv[i][1] for i in range(n)]


LROWS = _l_rows()
LINV = _invert(LROWS)


def apply_rows(rows, s):
    out = 0
    for j, r in enumerate(rows):
        if popcount(r & s) & 1:
            out |= 1 << j
    return out


def Linv(s):
    return apply_rows(LINV, s)


# ---------- trail core No. 3 (GLL+20 Table 9, public text) ---------------------------------

def active_rows(s):
    out = []
    for r in range(320):
        v = row_val(s, r)
        if v:
            out.append((r, v))
    return out


def in_kernel(s):
    a = to_lanes(s)
    return all((a[x] ^ a[x + 5] ^ a[x + 10] ^ a[x + 15] ^ a[x + 20]) == 0 for x in range(5))


PAD_BITS = {}
for _j in range(1080, NB):
    PAD_BITS[_j] = ((0x86 >> (_j - 1080)) & 1) if _j < 1088 else 0


TRAIL = ['---------------1|----------------|---------------4|----------------|----------------', '---------------4|---------------4|---------------4|-----------2----|----------------', '2---------------|----------------|----------2-----|----------------|----------------', '2---------------|----------------|----------------|-----------2----|----------------', '----------2----1|----------------|----------2-----|----------------|---------------1', '---------------1|----------------|---------------1|------4---------|----------------', '----------------|----------------|---------------1|----------------|-----------4----', '----------------|-------------1--|----------------|----------------|-----------4----', '----------------|----------------|----------------|----------------|----------------', '---------------1|-------------1--|----------------|------4---------|----------------']


def parse_trail_lines(lines):
    def plane_block(block):
        s = 0
        for y, ln in enumerate(block):
            for x, fld in enumerate(ln.split("|")):
                s |= int(fld.replace("-", "0"), 16) << (64 * (x + 5 * y))
        return s
    return plane_block(lines[:5]), plane_block(lines[5:])


NB = 1600
B2, B3 = parse_trail_lines(TRAIL)
A3 = Linv(B3)
A2 = Linv(B2)
A2_ROWS = active_rows(A2)
RC0 = RC[0]  # iota of round 0 touches lane 0


def place(r, v):
    y, z = divmod(r, 64)
    s = 0
    for x in range(5):
        if (v >> x) & 1:
            s |= 1 << bit(x, y, z)
    return s


def n_active(s):
    a = to_lanes(s)
    act = 0
    for y in range(5):
        act += popcount(a[5 * y] | a[5 * y + 1] | a[5 * y + 2] | a[5 * y + 3] | a[5 * y + 4])
    return act


# ---------------- GF(2) system in RREF -----------------------------------------------------

class Sys:
    """Rows are ints: bit 0 = constant, bit i+1 = variable i. Kept in reduced row echelon form."""

    def __init__(self):
        self.piv = {}
        self.pmask = 0
        self.bad = 0

    def reduce(self, row):
        t = row & self.pmask
        while t:
            lb = t & -t
            row ^= self.piv[lb.bit_length() - 1]
            t = row & self.pmask
        return row

    def add(self, row):
        row = self.reduce(row)
        if row == 0:
            return 0
        if row == 1:
            self.bad += 1
            return -1
        hb = row.bit_length() - 1
        m = 1 << hb
        for p, pr in self.piv.items():
            if pr & m:
                self.piv[p] = pr ^ row
        self.piv[hb] = row
        self.pmask |= m
        return 1

    def rank(self):
        return len(self.piv)

    def expr(self, var):
        b = var + 1
        if b in self.piv:
            return self.piv[b] ^ (1 << b)
        return 1 << b

    def copy(self):
        c = Sys()
        c.piv = dict(self.piv)
        c.pmask = self.pmask
        c.bad = self.bad
        return c


def row_eq(r, u, k):
    """Equation u . x|r = k as a system row."""
    bits = row_bits(r)
    row = k
    for x in range(5):
        if (u >> x) & 1:
            row ^= 1 << (bits[x] + 1)
    return row


def projection(sys_, r):
    """Point mask of the projection of the solution set onto row r of x."""
    ex = [sys_.expr(b) for b in row_bits(r)]
    mask = 0
    # value v is reachable iff for every mu with XOR of linear parts 0, mu.v = mu.c
    rel = []
    for mu in range(1, 32):
        acc = 0
        for x in range(5):
            if (mu >> x) & 1:
                acc ^= ex[x]
        if acc >> 1 == 0:
            rel.append((mu, acc & 1))
    for v in range(32):
        if all((popcount(mu & v) & 1) == c for mu, c in rel):
            mask |= 1 << v
    return mask


# precomputed affine subspaces with their equations and per-bit affine forms
AFFX = []
for _m, _d in AFF:
    AFFX.append((_m, _d, affine_eqs(_m), [affine_form(_m, b) for b in range(5)]))
AFFX.sort(key=lambda t: -t[1])


class Connector:
    def __init__(self, beta1, alpha1):
        self.beta1 = beta1
        self.alpha1 = alpha1
        # E_1: for each active row of beta1, equations of V(beta1|r, alpha2|r) on y = L(a0)
        self.e1 = []
        for r in range(320):
            d = row_val(beta1, r)
            if not d:
                continue
            o = row_val(A2, r)
            assert DDT[d][o] > 0
            bits = row_bits(r)
            for u, k in affine_eqs(VMASK[d][o]):
                sset = 0
                for x in range(5):
                    if (u >> x) & 1:
                        sset ^= LROWS[bits[x]]
                # a0 = chi(x) ^ RC0 ; RC0 = bit 0 of lane 0 (only bit 0 set for round 0)
                const = k ^ (sset & 1)
                self.e1.append((sset, const))
        self.need = {}
        for sset, _ in self.e1:
            t = sset
            while t:
                lb = t & -t
                i = lb.bit_length() - 1
                lane, z = divmod(i, 64)
                x, y = lane % 5, lane // 5
                r = 64 * y + z
                self.need[r] = self.need.get(r, 0) | (1 << x)
                t ^= lb

    def base_system(self, beta0):
        S = Sys()
        for j in range(1080, NB):
            if S.add((LINV[j] << 1) | PAD_BITS[j]) < 0:
                return None, 0
        w0 = 0
        for r in range(320):
            d = row_val(beta0, r)
            if not d:
                continue
            o = row_val(self.alpha1, r)
            for u, k in affine_eqs(VMASK[d][o]):
                w0 += 1
                if S.add(row_eq(r, u, k)) < 0:
                    return None, w0
        return S, w0

    def add_e1(self, S, forms):
        bad = 0
        for sset, const in self.e1:
            row = const
            t = sset
            while t:
                lb = t & -t
                i = lb.bit_length() - 1
                lane, z = divmod(i, 64)
                x, y = lane % 5, lane // 5
                r = 64 * y + z
                g, c = forms[r][x]
                row ^= c
                bits = row_bits(r)
                for xx in range(5):
                    if (g >> xx) & 1:
                        row ^= 1 << (bits[xx] + 1)
                t ^= lb
            if S.add(row) < 0:
                bad += 1
        return bad


def space_of(S):
    """x0 and basis of the affine solution set of S."""
    x0 = 0
    for p, row in S.piv.items():
        if row & 1:
            x0 |= 1 << (p - 1)
    free = [v for v in range(NB) if not (S.pmask >> (v + 1)) & 1]
    basis = []
    for f in free:
        b = 1 << f
        fb = 1 << (f + 1)
        for p, row in S.piv.items():
            if row & fb:
                b |= 1 << (p - 1)
        basis.append(b)
    return x0, basis


def anchored_space(con, x, beta0, rng):
    """Linear system around witness x; consistent by construction."""
    S, w0 = con.base_system(beta0)
    if S is None:
        return None
    rank0 = S.rank()
    S = S.copy()
    forms = {}
    nlin = 0
    rows = list(con.need)
    rng.shuffle(rows)
    for r in rows:
        nbits = con.need[r]
        v = row_val(x, r)
        P = projection(S, r)
        assert (P >> v) & 1
        best = None
        cands = []
        for m, dm, eqs, af in AFFX:
            if best is not None and dm < best:
                break
            if not (m >> v) & 1 or m & ~P:
                continue
            if all(af[xx] is not None for xx in range(5) if (nbits >> xx) & 1):
                best = dm
                cands.append((m, eqs, af))
        m, eqs, af = rng.choice(cands)
        for u, k in eqs:
            rr = S.add(row_eq(r, u, k))
            assert rr >= 0
            nlin += rr
        forms[r] = af
    rank1 = S.rank()
    bad = con.add_e1(S, forms)
    return S, w0, rank0, nlin, rank1, bad


X_WIT = 0xd1f0cca38b936a90929949c2d8eb94f4119af4ec6109dcf0e0067db6ee5565083a8d1b280325c73082d99bd759be3bdbc9d9ec0955ed42fec62b05fbd11e0f0421339a95ae4fbf3924662708d436b428bee3434e2ee5faaf268d00099052727ab63069abc5d35b9a38a3f51e53fd4629aa5d149d604e84e750bfb2767b02557b41ee9644be314195011ae70372a30cf4f18514766416b749099f490933248e4ca3400264149c9e89eb37c77b705b337a82c00461ed76a3dc8bf383ecc448b30081fa5dd6c85efa33
BETA0 = 0x5840f34c45b0c06f91f1a6a60501a15a54a0462e85758060351171d10f7c016e9cc0c28c4b98604f7fc006444e190172b9b1110201b9a148124360d28f4941399ee045fd8aff413c2c50d52f55b2e01395b0721c1fd1e06a4d0185170d30e00205a3b0928a55e031fcd131f90f7c007438e1e1fd19c9401f68522e6c4440806e92a15ac3c510a01ea7e3e3bec124604fa4b2edb94a24e0452fa21775d5e9c029406145c34c38009389c3202e4ff800c89c13d362c0e460bc2c43d6ba8c3400f4b53376565279a0f3
BETA1 = 0x00000020000000005000004e0000000000000004000000008000000200000000200000140000000100000020000000005000004e000000000000000400000004800000100000000020000006000000010000402400000000400000480000000010000002008000008000000000000000200000160000000100004022000000005000004c0000000000000006000000008000000000000000200000140000000100000020000000005000000800000000000000060080000480000000000000002000001200000000
ALPHA1 = 0xc950939908e0a0679db175ae05b9217a9d50d28484646031b55035f78e1c20448d70f0444ec4e02fc91093994060a0679db1572e05b9617a9d52739484f86031b73035ff8e1ea044aa70f0445ee5e02fc15093990860a067ddb155a605b9207a9d92c39484e46031b45035ff8f1c20448d70f0449ecde02fc9509b990860a0679db151ae05b9207a9f52d39484646031b55035ff8e1420448d70f04456cde02ec95093bd0860a0a79db155bc05b9203a1d52d3c484646035255035f48e1c2044ad70f0565ecde02f
LIN_SEED = 11765234521121731771
BEST_IDX = 73686378480
MAX_BASIS = 48


def build():
    con = Connector(BETA1, ALPHA1)
    S, w0, r0, nl, r1, bad = anchored_space(con, X_WIT, BETA0, random.Random(LIN_SEED))
    x0, basis = space_of(S)
    free = [v for v in range(NB) if not (S.pmask >> (v + 1)) & 1]
    drop = next(k for k, f in enumerate(free) if (BETA0 >> f) & 1)
    gbasis = (basis[:drop] + basis[drop + 1:])[:MAX_BASIS]
    g = BEST_IDX ^ (BEST_IDX >> 1)
    x = x0
    for k in range(len(gbasis)):
        if (g >> k) & 1:
            x ^= gbasis[k]
    info = {"w0": w0, "rank_pad_e0": r0, "lin_rows": nl, "rank_after_lin": r1,
            "rank_final": S.rank(), "df": NB - S.rank(), "e1_inconsistent": bad}
    return x0, basis, x, info


def messages(x):
    s1 = Linv(x)
    s2 = Linv(x ^ BETA0)
    return s1, s2


def main():
    req = json.loads(sys.stdin.read())
    x0, basis, xc, info = build()
    c1, c2 = messages(xc)
    ma = (c1 & ((1 << 1080) - 1)).to_bytes(135, "little")
    mb = (c2 & ((1 << 1080) - 1)).to_bytes(135, "little")
    trials = []
    for t in req["trials"]:
        rng = random.Random(int(t["seed"], 16))
        x = x0
        for b in basis:
            if rng.getrandbits(1):
                x ^= b
        s1, s2 = messages(x)
        pad_ok = int(s1 >> 1080 == 0x86 and s2 >> 1080 == 0x86)
        d2 = rounds_from_chi_input(x, 0, 1) ^ rounds_from_chi_input(x ^ BETA0, 0, 1)
        obs = {"fresh_point_alpha2": int(d2 == A2), "fresh_point_padding": pad_ok,
               "space_df": info["df"], "rank_pad_e0": info["rank_pad_e0"],
               "rank_after_lin": info["rank_after_lin"], "rank_final": info["rank_final"],
               "cert_from_space_index": int(c1 >> 1080 == 0x86 and c2 >> 1080 == 0x86)}
        trials.append({"trial": t["trial"], "message_a_hex": ma.hex(), "message_b_hex": mb.hex(),
                       "observations": obs})
    sys.stdout.write(json.dumps({"schema_version": 1, "trials": trials}))


if __name__ == "__main__":
    main()
