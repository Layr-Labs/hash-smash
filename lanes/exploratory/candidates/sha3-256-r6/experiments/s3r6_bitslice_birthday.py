"""Projected144-bit derivative of winglock bfc8c418's incremental evaluator.

Four bounded organizer experiments preserve its grouped/Gray layouts but
use18-bit event masks inside digest bits112..255, a16-bit projected toy key,
a14-bit sparse bucket and64 declined-confirmation cap. Full256-bit digest
comparison is the production algorithm; the toy's18-bit event is explicitly
not a full collision. The organizer recomputes returned mask predicates.
The evaluator checks projected output against the full bitsliced path,
zero-aware transpose against its exact schedule, selected keys against an
independent scalar sponge, and incremental O2P against reconstruction.
Python metadata loops are an evaluator, not a measured RAM cost. No test
here proves full-run Hproj or the statistical allowance in the claim.
"""

import hashlib
import itertools
import json
import sys

M64 = (1 << 64) - 1
W = (1 << 256) - 1
RC = (0x0000000000000001, 0x0000000000008082, 0x800000000000808A,
      0x8000000080008000, 0x000000000000808B, 0x0000000080000001)
RHO = (0, 1, 62, 28, 27, 36, 44, 6, 55, 20, 3, 10, 43, 25, 39,
       41, 45, 15, 21, 8, 18, 2, 61, 56, 14)
DIAG = (0, 6, 12, 18, 24)
EXACT_CHECKS = 4
PROJECTION = ((1 << 144) - 1) << 112

LAYOUTS = {   # groups per trial, list of z in processing order
    "k6r6-proj-full-width": (256, [t ^ (t >> 1) for t in range(2)]),
    "k6r6-proj-spread": (16, [t ^ (t >> 1) for t in range(32)]),
    "k6r6-proj-single-group": (1, [t ^ (t >> 1) for t in range(512)]),
    "k6r6-proj-high-z": (4, [(t ^ (t >> 1)) << 25 for t in range(128)]),
}
MASKS = {'k6r6-proj-full-width': '0000000000000000000000000000ffff03000000000000000000000000000000', 'k6r6-proj-spread': '000000000000000000000000000000000000ffff030000000000000000000000', 'k6r6-proj-single-group': '00000000000000000000000000000000000000000000f0ff3f00000000000000', 'k6r6-proj-high-z': '00000000000000000000000000000000000000000000000000000000c0ffff00'}


# ---------------- independent direct sponge (exactness reference) ----------
def _keccak_tables():
    rho = [[0] * 5 for _ in range(5)]
    x, y = 1, 0
    for t in range(24):
        rho[x][y] = ((t + 1) * (t + 2) // 2) % 64
        x, y = y, (2 * x + 3 * y) % 5
    rc, r = [], 1
    for _ in range(6):
        c = 0
        for j in range(7):
            if r & 1:
                c |= 1 << ((1 << j) - 1)
            r = ((r << 1) ^ 0x71) & 0xFF if r & 0x80 else r << 1
        rc.append(c)
    return rho, rc


_TABLES = _keccak_tables()


def sponge6(msg):
    """Direct SHA3-256 sponge with Keccak rounds 0..5 on one 136-byte block."""
    rho, rc = _TABLES
    block = bytearray(msg) + bytearray(136 - len(msg))
    block[len(msg)] ^= 0x06
    block[135] ^= 0x80
    a = [[int.from_bytes(block[8 * (x + 5 * y):8 * (x + 5 * y) + 8], "little") if x + 5 * y < 17 else 0
          for y in range(5)] for x in range(5)]
    for rnd in range(6):
        c = [a[x][0] ^ a[x][1] ^ a[x][2] ^ a[x][3] ^ a[x][4] for x in range(5)]
        d = [c[(x - 1) % 5] ^ (((c[(x + 1) % 5] << 1) | (c[(x + 1) % 5] >> 63)) & M64) for x in range(5)]
        b = [[0] * 5 for _ in range(5)]
        for x in range(5):
            for y in range(5):
                v, r = a[x][y] ^ d[x], rho[x][y]
                b[y][(2 * x + 3 * y) % 5] = ((v << r) | (v >> (64 - r))) & M64 if r else v
        a = [[b[x][y] ^ ((~b[(x + 1) % 5][y]) & b[(x + 2) % 5][y]) for y in range(5)] for x in range(5)]
        a[0][0] ^= rc[rnd]
    return b"".join(a[x][0].to_bytes(8, "little") for x in range(4))


def message(prefix, z):
    m = bytearray(prefix)
    for k in range(4):
        m[k] ^= (z >> (8 * k)) & 0xFF
        m[40 + k] ^= (z >> (8 * k)) & 0xFF
    return bytes(m)


# ---------------- bitsliced geometry -----------------------------------------
# word index of P(L, b) is 64*L + b
def _pi_src(X, Y):
    return ((Y - 3 * X) * 3) % 5, X


def _bsrc(X, Y, b):
    """A2 word (L, b') read by rho/pi output position (X, Y) at plane b."""
    xs, ys = _pi_src(X, Y)
    L = xs + 5 * ys
    return L, (b - RHO[L]) % 64


SRC = []      # source word index, output order p = 64*(X + 5Y) + b
DIDX = []     # D word index of the source
BS0 = []      # (p, xs) with source plane 0: receives the plane-0 fix-up
for _Y in range(5):
    for _X in range(5):
        _xs, _ys = _pi_src(_X, _Y)
        _L = _xs + 5 * _ys
        for _b in range(64):
            _bs = (_b - RHO[_L]) % 64
            if _bs == 0:
                BS0.append((len(SRC), _xs))
            SRC.append(64 * _L + _bs)
            DIDX.append(64 * _xs + _bs)
CHI1 = [64 * ((X + 1) % 5 + 5 * Y) + b for Y in range(5) for X in range(5) for b in range(64)]
CHI2 = [64 * ((X + 2) % 5 + 5 * Y) + b for Y in range(5) for X in range(5) for b in range(64)]
DPREV = [64 * ((x - 1) % 5) + b for x in range(5) for b in range(64)]
DNEXT = [64 * ((x + 1) % 5) + (b - 1) % 64 for x in range(5) for b in range(64)]
DCOL = [64 * ((i // 64) % 5) + i % 64 for i in range(1600)]


def d_words(S):
    """Theta D words (index 64x + b) of a bitsliced state."""
    C = [S[i] ^ S[i + 320] ^ S[i + 640] ^ S[i + 960] ^ S[i + 1280] for i in range(320)]
    return [C[p] ^ C[n] for p, n in zip(DPREV, DNEXT)]


def round_pass(S, D, rc):
    """Setup round 1 (plain encoding): theta + rho + pi + chi + iota; returns (state, D of output)."""
    B = [S[s] ^ D[d] for s, d in zip(SRC, DIDX)]
    out = [v ^ ((B[i] ^ W) & B[j]) for v, i, j in zip(B, CHI1, CHI2)]
    for b in range(64):
        if (rc >> b) & 1:
            out[b] ^= W
    return out, d_words(out)


# ---------------- lane-complement polarity (Keccak team; tekkac b001199a) ----
def lanepol(p, L):
    return (p >> L) & 1


def fpol(pout):
    """Polarity of the theta'd next-round input given chi-output polarity pout."""
    pc = [0] * 5
    for L in range(25):
        pc[L % 5] ^= lanepol(pout, L)
    q = 0
    for L in range(25):
        x = L % 5
        q |= (lanepol(pout, L) ^ pc[(x - 1) % 5] ^ pc[(x + 1) % 5]) << L
    return q


_ROWCACHE = {}


def solve_row(q, p, iota, outs):
    """Cheapest gate plan of one chi row: inputs with polarity bits q, wanted
    output polarities p, iota flip of output 0. plan[X] = (ca, cb, cc, gate,
    outnot): c* = 1 uses a complemented copy of that input."""
    key = (q, p, iota, tuple(outs))
    if key in _ROWCACHE:
        return _ROWCACHE[key]
    qb = [(q >> k) & 1 for k in range(5)]
    pb_ = [(p >> k) & 1 for k in range(5)]
    best = None
    for Sm in range(32):
        S = [k for k in range(5) if (Sm >> k) & 1]
        cost = len(S)
        plan = {}
        for X in outs:
            ib = iota if X == 0 else 0
            bo = None
            for ca, cb, cc in itertools.product((0, 1), repeat=3):
                if (ca and X not in S) or (cb and (X + 1) % 5 not in S) or (cc and (X + 2) % 5 not in S):
                    continue
                pa = qb[X] ^ ca
                pbb = qb[(X + 1) % 5] ^ cb
                pcc = qb[(X + 2) % 5] ^ cc
                if (pbb, pcc) == (1, 0):
                    gate, pT = "and", 0
                elif (pbb, pcc) == (0, 1):
                    gate, pT = "or", 1
                else:
                    continue
                on = int(pa ^ pT ^ ib != pb_[X])
                if bo is None or on < bo[0]:
                    bo = (on, (ca, cb, cc, gate, on))
            if bo is None:
                cost = 99
                break
            cost += bo[0]
            plan[X] = bo[1]
        if best is None or cost < best[0]:
            best = (cost, S, plan)
    _ROWCACHE[key] = best
    return best


P34 = 1336081           # chi-output polarity of rounds 3 and 4 (and of round 2 into O2P)
P5 = 1188625            # chi-output polarity of round 5
Q3 = fpol(P34)          # polarity of O2P and of the round-4 and round-5 inputs
QLAST = fpol(P5)        # polarity of the round-6 input


def _rowq(qin, Y):
    return sum(lanepol(qin, _pi_src(X, Y)[0] + 5 * _pi_src(X, Y)[1]) << X for X in range(5))


def chi_plan(qin, pout, rc):
    """Per output word p = 64(X+5Y)+b: (a, amask, b, bmask, c, cmask, is_or, outmask)."""
    plan = []
    for Y in range(5):
        qrow, prow = _rowq(qin, Y), (pout >> (5 * Y)) & 31
        for X in range(5):
            for b in range(64):
                io = (rc >> b) & 1 if Y == 0 else 0
                ca, cb, cc, gate, on = solve_row(qrow, prow, io, range(5))[2][X]
                plan.append((64 * (X + 5 * Y) + b, W if ca else 0,
                             64 * ((X + 1) % 5 + 5 * Y) + b, W if cb else 0,
                             64 * ((X + 2) % 5 + 5 * Y) + b, W if cc else 0,
                             gate == "or", W if on else 0))
    return plan


def last_plan(b):
    q = sum(lanepol(QLAST, DIAG[X]) << X for X in range(5))
    io = (RC[5] >> b) & 1
    best = None
    for p in range(16):
        r = solve_row(q, p, io, range(4))
        if best is None or r[0] < best[0][0]:
            best = (r, p)
    return best


LASTPLAN = [last_plan(b) for b in range(64)]
KEYMASK = 0              # stored key = digest (little-endian int) XOR KEYMASK
for _b in range(64):
    for _x in range(4):
        KEYMASK |= ((LASTPLAN[_b][1] >> _x) & 1) << (64 * _x + _b)

PLAN2 = chi_plan(0, P34, RC[1])
PLAN3 = chi_plan(Q3, P34, RC[2])
PLAN4 = chi_plan(Q3, P34, RC[3])
PLAN5 = chi_plan(Q3, P5, RC[4])


def chi(B, plan):
    return [B[a] ^ am ^ ((((B[b] ^ bm) | (B[c] ^ cm)) if g else ((B[b] ^ bm) & (B[c] ^ cm))) ^ om)
            for a, am, b, bm, c, cm, g, om in plan]


def round_ts(src, fix, plan):
    """Round with theta'd input (plane 0 lacking fix[x] unless fix is None),
    lane-complement chi, and the next round's D added before the store for
    planes b >= 1; returns (stored state, fix-up words D_next[x][0])."""
    B = [src[s] for s in SRC]
    if fix is not None:
        for p, xs in BS0:
            B[p] ^= fix[xs]
    out = chi(B, plan)
    D = d_words(out)
    fix_out = [D[64 * x] for x in range(5)]
    for x in range(5):
        D[64 * x] = 0
    return [o ^ D[k] for o, k in zip(out, DCOL)], fix_out


def build_o2p(A2):
    out, fix = round_ts(A2, None, PLAN2)
    for L in range(25):
        out[64 * L] ^= fix[L % 5]
    return out


def last_rows(S, fix, projected=False):
    rows = [0] * 256
    for b in range(64):
        outputs = [x for x in range(4) if not projected or 64*x+b >= 112]
        needed = {v for x in outputs for v in (x, (x+1)%5, (x+2)%5)}
        B = [0] * 5
        for X in sorted(needed):
            L = DIAG[X]
            bs = (b - RHO[L]) % 64
            B[X] = S[64*L+bs] ^ (fix[X] if bs == 0 else 0)
        (_, Sset, plan), _ = LASTPLAN[b]
        for x in outputs:
            ca, cb, cc, gate, on = plan[x]
            a = B[x] ^ (W if ca else 0)
            u = B[(x+1)%5] ^ (W if cb else 0)
            v = B[(x+2)%5] ^ (W if cc else 0)
            rows[64*x+b] = a ^ ((u | v) if gate == "or" else (u & v)) ^ (W if on else 0)
    return rows



# ---------------- transpose ----------------------------------------------------
def _mask(d):
    m = 0
    for c in range(256):
        if not c & d:
            m |= 1 << c
    return m


MASKD = {d: _mask(d) for d in (1, 2, 4, 8, 16, 32, 64, 128)}


def transpose(rows, order):
    """256 x 256 bit transpose by delta swaps; the stages commute, `order` mirrors the program."""
    R = list(rows)
    for d in order:
        m = MASKD[d]
        for i0 in range(256):
            if not i0 & d:
                a, b = R[i0], R[i0 + d]
                t = ((a >> d) ^ b) & m
                R[i0] = a ^ (t << d)
                R[i0 + d] = b ^ t
    return R


def transpose_projected(rows):
    """Compile-time known-zero specialization of the first five stages.

    Python tracks the static zero mask as evaluator metadata, not as claimed
    RAM work. A real unrolled program emits the chosen case for each swap.
    Operations are 0/3/4/6 for both-zero/left-zero/right-zero/neither.
    """
    R = list(rows)
    zero = [i < 112 for i in range(256)]
    phase1_ops = 0
    for d in STEP_ORDER:
        mask = MASKD[d]
        for i in range(256):
            if i & d:
                continue
            j = i+d
            if d in (1,2,4,64,128):
                if zero[i] and zero[j]:
                    continue
                if zero[i]:
                    t = R[j] & mask
                    R[i], R[j] = t << d, R[j] ^ t
                    phase1_ops += 3
                elif zero[j]:
                    t = (R[i] >> d) & mask
                    R[i], R[j] = R[i] ^ (t << d), t
                    phase1_ops += 4
                else:
                    t = ((R[i] >> d) ^ R[j]) & mask
                    R[i], R[j] = R[i] ^ (t << d), R[j] ^ t
                    phase1_ops += 6
                zero[i] = zero[j] = False
            else:
                t = ((R[i] >> d) ^ R[j]) & mask
                R[i], R[j] = R[i] ^ (t << d), R[j] ^ t
    if phase1_ops != 2208:
        raise RuntimeError("unexpected static projected transpose count")
    return R


SETUP_ORDER = (1, 2, 4, 8, 16, 32, 64, 128)
STEP_ORDER = (1, 2, 4, 64, 128, 8, 16, 32)


def decode_slot(q):
    """Processing index q (0..255) of a z-step -> group slot (bit position)."""
    gi, i = q >> 3, q & 7
    return 64 * (gi >> 3) + 8 * i + (gi & 7)


PROC = [decode_slot(q) for q in range(256)]
assert sorted(PROC) == list(range(256))


# ---------------- Gray support and incremental round 2 -------------------------
def support(j):
    jp = (j + 36) % 64
    pos = set()
    for x, b in ((1, j), (4, j + 1), (1, jp), (4, jp + 1), (4, j), (2, j + 1),
                 (0, j), (3, j + 1), (0, jp), (3, jp + 1), (2, jp), (0, jp + 1)):
        for y in range(5):
            pos.add((x + 5 * y, b % 64))
    pos.add((3, j))
    pos.add((19, jp))
    return sorted(pos)


SUPPORT = [support(j) for j in range(32)]
assert all(len(s) == 62 for s in SUPPORT)


def incr_rows(j):
    """Affected round-2 chi rows of z-bit j: {(Y, plane): {X: (k, L, b)}}."""
    rows = {}
    for k, (L, b) in enumerate(SUPPORT[j]):
        x, y = L % 5, L // 5
        X, Y = y, (2 * x + 3 * y) % 5
        rows.setdefault((Y, (b + RHO[L]) % 64), {})[X] = (k, L, b)
    return sorted(rows.items())


ROWS2 = [incr_rows(j) for j in range(32)]


def incr_round2(A2, O2P, coef, j):
    """A2 ^= COEF[j] on the support; O2P ^= exact chi difference + induced dD3."""
    dout = {}
    for (Y, bp), d in ROWS2[j]:
        if len(d) == 1:
            (X, (k, L, bs)), = d.items()
            c = coef[k]
            A2[64 * L + bs] ^= c
            Lp, bp1 = _bsrc((X + 1) % 5, Y, bp)
            Lm, bm1 = _bsrc((X - 1) % 5, Y, bp)
            dout[(X, Y, bp)] = c
            dout[((X - 1) % 5, Y, bp)] = c & A2[64 * Lp + bp1]
            dout[((X - 2) % 5, Y, bp)] = (A2[64 * Lm + bm1] ^ W) & c
        else:
            old, new = [], []
            for X in range(5):
                L, bs = _bsrc(X, Y, bp)
                o = A2[64 * L + bs]
                if X in d:
                    A2[64 * L + bs] = o ^ coef[d[X][0]]
                old.append(o)
                new.append(A2[64 * L + bs])
            for X in sorted({(X - s) % 5 for X in d for s in (0, 1, 2)}):
                linear = coef[d[X][0]] if X in d else 0
                if (X+1)%5 in d or (X+2)%5 in d:
                    n1, n2 = new[(X + 1) % 5], new[(X + 2) % 5]
                    o1, o2 = old[(X + 1) % 5], old[(X + 2) % 5]
                    gate_delta = ((n1 ^ W) & n2) ^ ((o1 ^ W) & o2)
                    v = linear ^ gate_delta if X in d else gate_delta
                else:
                    v = linear
                dout[(X, Y, bp)] = v
    # Three-pass schedule: store 183 deltas, reduce145 column parities,
    # then form215 theta differences and patch1090 state words once.
    # Dictionary keys/group membership below are compile-time geometry in
    # the costed program; this Python is a diagnostic evaluator.
    groups = {}
    for x,Y,b in dout:
        groups.setdefault((x,b), []).append((x,Y,b))
    dC = {}
    for key, terms in groups.items():
        v = dout[terms[0]]
        for term in terms[1:]:
            v ^= dout[term]
        dC[key] = v
    induced = {}
    for x,b in dC:
        for key in (((x+1)%5,b),((x-1)%5,(b+1)%64)):
            induced.setdefault(key, []).append((x,b))
    dD = {}
    for key, terms in induced.items():
        v = dC[terms[0]]
        for term in terms[1:]:
            v ^= dC[term]
        dD[key] = v
    destinations = set(dout) | {(x,Y,b) for x,b in dD for Y in range(5)}
    if (len(dout),len(dC),len(dD),len(destinations)) != (183,145,215,1090):
        raise RuntimeError("unexpected incremental support geometry")
    for x,Y,b in sorted(destinations):
        v = O2P[64*(x+5*Y)+b]
        if (x,b) in dD:
            v ^= dD[(x,b)]
        if (x,Y,b) in dout:
            v ^= dout[(x,Y,b)]
        O2P[64*(x+5*Y)+b] = v


# ---------------- batch ------------------------------------------------------
class Batch:
    """256 groups (bit positions); prefixes[p] is a 64-byte prefix (or zeros)."""

    def __init__(self, prefixes, zbits):
        S = [0] * 1600
        for w in range(2):
            rows = [int.from_bytes(p[32 * w:32 * w + 32], "little") for p in prefixes]
            S[256 * w:256 * w + 256] = transpose(rows, SETUP_ORDER)
        S[64 * 8 + 1] = W
        S[64 * 8 + 2] = W
        S[64 * 16 + 63] = W
        D1 = d_words(S)                     # round-1 D, independent of z (Lemma 1)
        out, D2 = round_pass(S, D1, RC[0])
        self.A2 = [out[i] ^ D2[DCOL[i]] for i in range(1600)]
        self.coef = {}
        for j in zbits:
            S2 = list(S)
            S2[j] ^= W
            S2[64 * 5 + j] ^= W
            if d_words(S2) != D1:
                raise RuntimeError("round-1 theta not invariant under the z flip")
            o2, D22 = round_pass(S2, D1, RC[0])
            A2j = [o2[i] ^ D22[DCOL[i]] for i in range(1600)]
            supp = {64 * L + b for L, b in SUPPORT[j]}
            for i in range(1600):
                if i not in supp and A2j[i] != self.A2[i]:
                    raise RuntimeError("z-dependence outside the 62-word support")
            self.coef[j] = [A2j[64 * L + b] ^ self.A2[64 * L + b] for L, b in SUPPORT[j]]
        self.O2P = build_o2p(self.A2)

    def flip(self, j):
        incr_round2(self.A2, self.O2P, self.coef[j], j)

    def check_o2p(self):
        if build_o2p(self.A2) != self.O2P:
            raise RuntimeError("incrementally maintained O2P differs from O2P rebuilt from A2")

    def keys(self):
        """Projected keys; return only true digest bits112..255, others zero.

        This evaluator computes all round5 parities. Only its stores are
        pruned in the claimed RAM schedule; zeroing below simulates omission.
        """
        S, fix = round_ts(self.O2P, None, PLAN3)
        S, fix = round_ts(S, fix, PLAN4)
        S, fix = round_ts(S, fix, PLAN5)
        reference = transpose(last_rows(S, fix), STEP_ORDER)
        # B[1] is unused at output planes0..47, mapping to lane6 source
        # planes20..63 and0..3. No retained output may read these stores.
        for b in list(range(20,64)) + list(range(4)):
            S[64*6+b] = 0
        rows = last_rows(S, fix, projected=True)
        result = transpose_projected(rows)
        if result != [k & PROJECTION for k in reference]:
            raise RuntimeError("projected path differs from full evaluator")
        return result


def trial_prefixes(seed, groups):
    return [b"".join(hashlib.sha256(b"s3r6-bitslice-v1" + seed + g.to_bytes(2, "little") + bytes((k,))).digest()
                     for k in (0, 1)) for g in range(groups)]


def _check(prefix, z, key):
    if ((int.from_bytes(sponge6(message(prefix, z)), "little") ^ KEYMASK) & PROJECTION) != key:
        raise RuntimeError("bitsliced evaluator disagrees with direct sponge")


def run_trials(seeds, layout, mask_le):
    G, zs = LAYOUTS[layout]
    per = 256 // G
    zbits = sorted({(a ^ b).bit_length() - 1 for a, b in zip(zs, zs[1:])})
    results = []
    for c0 in range(0, len(seeds), per):
        chunk = seeds[c0:c0 + per]
        pres = [trial_prefixes(s, G) for s in chunk]
        slots = [p for ps in pres for p in ps]
        slots += [bytes(64)] * (256 - len(slots))
        batch = Batch(slots, zbits)
        state = [{"sparse": {}, "dk": [], "ids": [], "first": None, "pairs": 0, "checks": 0, "declined": 0, "capped": False} for _ in chunk]
        event_bits = [b for b in range(256) if mask_le >> b & 1]
        if len(event_bits) != 18 or mask_le & ~PROJECTION:
            raise RuntimeError("invalid projected toy mask")
        for t, z in enumerate(zs):
            if t:
                batch.flip((z ^ zs[t - 1]).bit_length() - 1)
            keys = batch.keys()
            pow2 = t > 0 and not t & (t - 1)
            done = set()
            for p in PROC:                  # processing order of the program
                ti, g = divmod(p, G)
                if ti >= len(chunk):
                    continue
                st = state[ti]
                key = keys[p]
                if st["checks"] < EXACT_CHECKS or (pow2 and ti not in done):
                    _check(pres[ti][g], z, key)
                    st["checks"] += 1
                    done.add(ti)
                if st["capped"]:
                    continue
                event_key = sum(((key >> b) & 1) << j for j,b in enumerate(event_bits))
                k = event_key >> 2          # toy16-bit key, 18-bit event
                h = k >> 2                  # toy14-bit bucket
                n = len(st["dk"])
                # Untouched slots deliberately contain arbitrary candidate IDs.
                i = st["sparse"].get(h, ((h*17)^73) & 511)
                matched = i < n and st["dk"][i] == k
                if matched:
                    st["pairs"] += 1
                    ga,za = st["ids"][i]
                    ma,mb = message(pres[ti][ga],za),message(pres[ti][g],z)
                    da,db = sponge6(ma),sponge6(mb)
                    verified = ma != mb and ((int.from_bytes(da,"little") ^ int.from_bytes(db,"little")) & mask_le) == 0
                    if verified and st["first"] is None:
                        st["first"] = ((ga,za),(g,z))
                    if not verified:
                        st["declined"] += 1
                        if st["declined"] >= 64:
                            st["capped"] = True
                    # Keep the first representative on a projected match.
                else:
                    st["sparse"][h] = n
                # EVERY processed message keeps its real key and identity,
                # including declined matches. Never insert a dummy zero key.
                st["dk"].append(k)
                st["ids"].append((g,z))
                if len(st["dk"]) != len(st["ids"]):
                    raise RuntimeError("message-number invariant failed")
        batch.check_o2p()
        for ti, st in enumerate(state):
            obs = {"masked_pairs": st["pairs"], "messages": G * len(zs), "exactness_checks": st["checks"],
                   "support_columns_checked": len(zbits), "o2p_rebuild_checked": 1,
                   "declined_projected_matches": st["declined"], "confirmation_cap_reached": int(st["capped"]),
                   "projection_bits": 144, "phase1_transpose_ops": 2208}
            if st["first"] is None:
                results.append((None, None, obs))
            else:
                (ga, za), (gb, zb) = st["first"]
                results.append((message(pres[ti][ga], za).hex(), message(pres[ti][gb], zb).hex(), obs))
    return results


def main():
    if len(sys.argv) == 5 and sys.argv[1] == "--local":
        layout, trials, seed = sys.argv[2], int(sys.argv[3]), sys.argv[4]
        mask = int.from_bytes(bytes.fromhex(MASKS[layout]), "little")
        seeds = [hashlib.sha256(("local-" + seed + "-" + str(t)).encode()).digest() for t in range(trials)]
        res = run_trials(seeds, layout, mask)
        succ = sum(1 for a, _, _ in res if a is not None)
        pairs = sum(o["masked_pairs"] for _, _, o in res)
        print(json.dumps({"layout": layout, "trials": trials, "successes": succ, "masked_pairs": pairs}))
        return
    request = json.load(sys.stdin)
    if request["schema_version"] != 1 or request["target_profile"] != "sha3-256-r6-prefix-v1":
        raise ValueError("unexpected organizer target")
    event = request["event"]
    if event.get("kind") != "digest-xor-mask" or int(event["expected_hex"], 16) != 0:
        raise ValueError("unexpected organizer event")
    layout = request["experiment_id"]
    if layout not in LAYOUTS:
        raise ValueError("unexpected experiment id")
    mask_le = int.from_bytes(bytes.fromhex(event["mask_hex"]), "little")
    items = request["trials"]
    res = run_trials([bytes.fromhex(it["seed"]) for it in items], layout, mask_le)
    rows = []
    for it, (a, b, obs) in zip(items, res):
        rows.append({"trial": it["trial"], "message_a_hex": a, "message_b_hex": b, "observations": obs})
    json.dump({"schema_version": 1, "trials": rows}, sys.stdout, separators=(",", ":"), sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
