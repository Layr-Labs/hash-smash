"""Scaled analogue of the bitsliced grouped birthday search of proof.md (sha3-256-r6).

Stdlib only. Organizer mode (default): read one JSON request on stdin and write
one JSON result. Every digest used for matching is computed ONLY by the
bitsliced grouped evaluator of proof.md Sections 4-5, in the same order and
with the same encodings as the counted program:

  * a batch is 256 bit positions; bit position p of every 256-bit word belongs
    to one group (one structured 64-byte prefix: 256 free bits in lanes 1, 2,
    5, 6; lanes 0, 7 zero; lanes 3, 4 fixed by c1 = L1 ^ L6 ^ 2^63, see
    structured_prefix); z is XORed into the low 32 bits of lanes 1 and 6;
    word P(L, b) holds bit b of lane L for all 256 groups at once;
  * per batch: A2 (round-1 output + round-2 theta) for z = 0, stored with the
    program's storage polarity PI, and O2P = the round-2 output with round-3
    theta applied, in lane-complement encoding Q3;
  * round 1 is linear in z (linear structure, Guo-Liu-Song 2016; Th0rgal
    4867f093): z-bit j flips a fixed 22-word set of A2 by all-ones in every
    group (Lemma 3). Each Gray step on z-bit j flips the support words that
    are ever read and XORs into each of 508 O2P words its fixed patch
    expression (XOR of at most 5 A2 words and possibly all-ones: the exact
    round-2 chi difference plus the induced round-3 D change, Lemma 6), as the
    counted program does;
  * rounds 3, 4 and 5 read a theta'd input, use lane-complement chi (gates and
    complemented copies chosen per chi row from the lane polarities, round
    constants folded into polarity), and add the next round's D words before
    storing; each round's start plane (STARTS = 2, 39, 34, as in the program)
    is stored raw and the next round adds its 5 fix words on read (Lemma 7);
  * the last round computes only chi row 0, lanes 0..3, and only on the 35
    kept planes KEEP (140 digest bits): digest bit (x, b) becomes key row
    ROWOF[(x, b)] = 4 * KEEP.index(b) + x, rows 140..255 are zero (so the key
    is < 2^140 and is itself the table address), and
    the key is in the encoding KEYMASK (stored key = key_of_digest(digest),
    a fixed bit permutation of the 140 kept digest bits XOR KEYMASK);
  * the 256 x 256 delta-swap transpose (stages commute, Lemma 5) gives the
    key of every slot, and the keys are offered in processing order
    q = 0..255, slot decode_slot(q) = 16 * (q mod 16) + floor(q / 16).
  * rounds 4 and 5 are computed in full, then every stored word and fix
    column outside the dependency cone of proof Lemma 10 for these start
    planes (1,363 and 175 stored words, fix columns all and none; the counted
    program computes only these) is replaced by an
    unrelated SHA-256-derived constant before the next round reads it, so a
    key can only be right if nothing outside the cone is ever read;
  * the transpose uses Lemma 9's rotating-frame delta swaps with statically
    zero rows (5 ops per pair; 2 or 3 when one row is zero, 0 when both are;
    the odd-parity row moves; one final rotation per row left outside frame
    0; the program's 16-row layout and stage orders; 3,418 ops in all, as
    in the program's ledger) and is compared with the full 6-op transpose.

Several trials share one batch (each trial owns G consecutive bit positions);
bitwise operations never mix bit positions and the transpose only relocates
bits, so trials stay independent: each trial's output depends on its own seed.

Every mask bit must be a kept digest bit (lanes 0..3, plane in KEEP); the
mask is moved to key rows by ROWOF, so equal masked keys <=> equal masked
digests.  Scale: N_t = 2^9 messages per trial and an 18-bit digest mask, so
N_t^2 / 2^18 = 1 = N^2 / 2^256 as in the full attack. Layouts (G groups per
trial x Z values of z, z in Gray order):

  k6r6-bs-full-width   : 256 groups x 2,  z = gray(t), t < 2
  k6r6-bs-spread       : 16 groups x 32,  z = gray(t), t < 32
  k6r6-bs-single-group : 1 group x 512,   z = gray(t), t < 512
  k6r6-bs-high-z       : 4 groups x 128,  z = gray(t) << 25, t < 128

Self-checks (any failure raises, so the organizer run fails visibly):
  * per trial, the first EXACT_CHECKS keys in processing order, and the first
    key of the trial at every step t = 2^i (one step of every Gray block used),
    are compared over the whole 140-bit stored key with an independent direct
    6-round sponge (sponge6: own rho offsets and round constants) mapped
    through key_of_digest;
  * for every z-bit used, A2(e_j) XOR A2(0), computed from scratch, is
    all-ones exactly on the 22 support words and 0 elsewhere;
  * after the last step of every batch, the maintained A2 (on every word a
    patch reads) and O2P are compared word for word with A2 and O2P rebuilt
    from the prefixes at the current z.
  * at every step, key rows outside ROWOF must be 0 and the rotating zero-row
    transpose must equal the full transpose; at import, the cone sizes of
    Lemma 10 and the 3,418-op count of the rotating zero-row transpose are
    asserted;
  * every key of the batch (all 256 slots, in processing order) also runs
    through the program's tagged-id table (TagTable): each key must be a
    140-bit address; never-written words are adversarial (1/16 carry the
    run's TAG, forcing the verify-and-continue path, which must be taken);
    slots hold pair ids (one id for the messages q = 2k, 2k + 1 of a step,
    as in the program); a genuine candidate's pair must contain an earlier
    message with the same key, and every earlier member is verified by full
    digests; after the batch every table word must carry TAG and name a pair
    containing a message whose key is its address.

The first pair of distinct messages whose masked digests agree is returned; a
trial with no such pair returns two nulls. Observations are informational.

Local modes (not used by the organizer):
  python3 FILE --local LAYOUT TRIALS SEED   real target, local seeds; prints
  successes and the sum and sum of squares of per-trial masked pairs
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

LAYOUTS = {   # groups per trial, list of z in processing order
    "k6r6-bs-full-width": (256, [t ^ (t >> 1) for t in range(2)]),
    "k6r6-bs-spread": (16, [t ^ (t >> 1) for t in range(32)]),
    "k6r6-bs-single-group": (1, [t ^ (t >> 1) for t in range(512)]),
    "k6r6-bs-high-z": (4, [(t ^ (t >> 1)) << 25 for t in range(128)]),
}
# Kept last-round planes (counted program, proof.md Lemma 9); 4 x 35 = 140 digest bits.
KEEP = (0, 1, 2, 3, 4, 9, 10, 11, 16, 17, 18, 22, 23, 24, 25, 29, 30, 31, 32, 37, 38, 39, 40,
        44, 45, 46, 47, 51, 52, 53, 54, 58, 59, 60, 61)
NP = len(KEEP)
ROWOF = {(x, b): 4 * k + x for k, b in enumerate(KEEP) for x in range(4)}


def _mask_hex(bits):
    """18 digest bits (lane x, plane b) -> mask_hex (little-endian digest bytes)."""
    m = 0
    for x, b in bits:
        m |= 1 << (64 * x + b)
    return m.to_bytes(32, "little").hex()


MASKS = {
    "k6r6-bs-full-width": _mask_hex([(0, b) for b in (0, 1, 2, 3, 4)] + [(1, b) for b in (9, 10, 11, 16, 17)]
                                    + [(2, b) for b in (22, 23, 24, 25)] + [(3, b) for b in (29, 30, 31, 32)]),
    "k6r6-bs-spread": _mask_hex([(0, b) for b in (16, 17, 18, 22, 23)] + [(1, b) for b in (37, 38, 39, 40, 44)]
                                + [(2, b) for b in (44, 45, 46, 47)] + [(3, b) for b in (37, 38, 39, 40)]),
    "k6r6-bs-single-group": _mask_hex([(0, b) for b in (54, 58, 59, 60, 61)] + [(1, b) for b in (54, 58, 59, 60, 61)]
                                      + [(2, b) for b in (58, 59, 60, 61)] + [(3, b) for b in (58, 59, 60, 61)]),
    "k6r6-bs-high-z": _mask_hex([(0, b) for b in (29, 30, 31, 32, 37)] + [(1, b) for b in (44, 45, 46, 47, 51)]
                                + [(2, b) for b in (51, 52, 53, 54)] + [(3, b) for b in (0, 1, 2, 3)]),
}


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
    """LE32(z) XORed into bytes 8..11 and 48..51 (low halves of lanes 1 and 6)."""
    m = bytearray(prefix)
    for k in range(4):
        m[8 + k] ^= (z >> (8 * k)) & 0xFF
        m[48 + k] ^= (z >> (8 * k)) & 0xFF
    return bytes(m)


def _rotl64(v, r):
    r %= 64
    return ((v << r) | (v >> (64 - r))) & M64 if r else v


def structured_prefix(r256):
    """256 free bits -> 64-byte prefix with round 1 linear in z (proof Lemma 2;
    linear structure of Guo-Liu-Song 2016, used on this track by Th0rgal
    4867f093 with lanes 0, 5; here lanes 1, 6). Free lanes 1, 2, 5, 6; lanes
    0 and 7 are 0; c1 = L1 ^ L6 ^ 2^63 (column-1 parity, lane 16 = 0x80 << 56),
    L3 = 0x06 ^ rotr(c1, 1) (so D1[2] = 0), L4 = ~rotl(c1, 1) (so D1[0] = ~0)."""
    L = [0] * 8
    L[1], L[2], L[5], L[6] = [(r256 >> (64 * k)) & M64 for k in range(4)]
    c1 = L[1] ^ L[6] ^ (1 << 63)
    L[3] = 0x06 ^ _rotl64(c1, 63)
    L[4] = M64 ^ _rotl64(c1, 1)
    return b"".join(x.to_bytes(8, "little") for x in L)


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
BSP = {}      # source plane -> [(p, xs)]: outputs whose source word lies on that plane
for _Y in range(5):
    for _X in range(5):
        _xs, _ys = _pi_src(_X, _Y)
        _L = _xs + 5 * _ys
        for _b in range(64):
            _bs = (_b - RHO[_L]) % 64
            BSP.setdefault(_bs, []).append((len(SRC), _xs))
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
KEYMASK = 0              # stored key = key_of_digest(digest): kept bits moved to ROWOF, XOR KEYMASK
for (_x, _b), _r in ROWOF.items():
    KEYMASK |= ((LASTPLAN[_b][1] >> _x) & 1) << _r


def key_of_digest(d):
    """Stored key of a digest d (little-endian int): bit 64x + b -> row ROWOF[(x, b)], XOR KEYMASK."""
    k = 0
    for (x, b), r in ROWOF.items():
        k |= ((d >> (64 * x + b)) & 1) << r
    return k ^ KEYMASK


def key_mask_of(mask_le):
    """Digest mask -> key mask; every mask bit must be a kept digest bit."""
    km = 0
    for i in range(256):
        if (mask_le >> i) & 1:
            if (i >> 6, i & 63) not in ROWOF:
                raise ValueError("mask bit %d is not a kept digest bit" % i)
            km |= 1 << ROWOF[(i >> 6, i & 63)]
    return km

PLAN2 = chi_plan(0, P34, RC[1])
PLAN3 = chi_plan(Q3, P34, RC[2])
PLAN4 = chi_plan(Q3, P34, RC[3])
PLAN5 = chi_plan(Q3, P5, RC[4])


def chi(B, plan):
    return [B[a] ^ am ^ ((((B[b] ^ bm) | (B[c] ^ cm)) if g else ((B[b] ^ bm) & (B[c] ^ cm))) ^ om)
            for a, am, b, bm, c, cm, g, om in plan]


def round_ts(src, fix, fp_in, plan, start):
    """Round with theta'd input (plane fp_in lacking fix[x] unless fix is None),
    lane-complement chi, and the next round's D added before the store on every
    plane except this round's start plane `start` (stored raw, as the program's
    rotating plane schedule does); returns (stored state, fix words
    D_next[x][start])."""
    B = [src[s] for s in SRC]
    if fix is not None:
        for p, xs in BSP[fp_in]:
            B[p] ^= fix[xs]
    out = chi(B, plan)
    D = d_words(out)
    fix_out = [D[64 * x + start] for x in range(5)]
    for x in range(5):
        D[64 * x + start] = 0
    return [o ^ D[k] for o, k in zip(out, DCOL)], fix_out


def build_o2p(A2):
    out, fix = round_ts(A2, None, None, PLAN2, 0)
    for L in range(25):
        out[64 * L] ^= fix[L % 5]
    return out


def last_rows(S, fix):
    """Last round on the kept planes only; rows not in ROWOF stay 0."""
    rows = [0] * 256
    for b in KEEP:
        B = []
        for X in range(5):
            L = DIAG[X]
            bs = (b - RHO[L]) % 64
            B.append(S[64 * L + bs] ^ (fix[X] if bs == STARTS[2] else 0))
        (_, Sset, plan), _ = LASTPLAN[b]
        for x in range(4):
            ca, cb, cc, gate, on = plan[x]
            a = B[x] ^ (W if ca else 0)
            u = B[(x + 1) % 5] ^ (W if cb else 0)
            v = B[(x + 2) % 5] ^ (W if cc else 0)
            rows[ROWOF[(x, b)]] = a ^ ((u | v) if gate == "or" else (u & v)) ^ (W if on else 0)
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


SETUP_ORDER = (1, 2, 4, 8, 16, 32, 64, 128)
STEP_ORDER = (1, 2, 4, 8, 16, 32, 64, 128)   # reference order of the full transpose; stages commute


def _par(r):
    return bin(r).count("1") & 1


def _rotl(x, n):
    n %= 256
    return ((x << n) | (x >> (256 - n))) & W if n else x


def _rot_cost(za, zb, ib):
    if za and zb:
        return 0
    if not za and not zb:
        return 5
    return 2 if (za if _par(ib) == 0 else zb) else 3


def _best_order(zero, rows, bits):
    """Cheapest stage order given the statically zero rows (as the program)."""
    best = None
    for order in itertools.permutations(bits):
        z = dict(zero); c = 0
        for d in order:
            for r in rows:
                if r & d:
                    continue
                c += _rot_cost(z[r], z[r | d], r | d)
                if z[r] != z[r | d]:
                    z[r] = z[r | d] = False
        if best is None or (c, order) < best:
            best = (c, order)
    return best[1]


KEYROWS = frozenset(ROWOF.values())
W1 = 16                                         # phase-1 block width (16-row layout)
NB = 256 // W1                                  # rows per phase-2 group
BLOCKS = sorted({r // W1 for r in KEYROWS})
P1ORDER = {g: _best_order({W1 * g + q: (W1 * g + q) not in KEYROWS for q in range(W1)},
                          [W1 * g + q for q in range(W1)], (1, 2, 4, 8)) for g in BLOCKS}
P2ORDER = {gi: _best_order({W1 * i + gi: i not in BLOCKS for i in range(NB)},
                           [W1 * i + gi for i in range(NB)], (16, 32, 64, 128)) for gi in range(W1)}


def transpose_z(rows):
    """Lemma 9 (v4): the program's rotating-frame delta swaps with statically
    zero rows.  Row r is held in a frame: physical bit q is logical bit
    (q + OFF[r]) mod 256.  In a stage d the even-parity row of a pair stays in
    frame 0 and the odd-parity row is rotated into its frame (a zero row needs
    no rotation); cost 5 per pair, 2 if the moving row is zero, 3 if the other
    row is zero, 0 if both are.  Phase 1: stages 1,2,4,8 in each 16-row block
    with a key row; phase 2: stages 16,32,64,128 on rows 16i + gi; then one
    rotation per row not in frame 0.  Returns (rows, ops)."""
    R, Z, OFF, ops = list(rows), [r not in KEYROWS for r in range(256)], [0] * 256, 0

    def swap(ia, ib, d):
        nonlocal ops
        za, zb = Z[ia], Z[ib]
        if za and zb:
            return
        ops += _rot_cost(za, zb, ib)
        if _par(ib) == 0:                          # b even: a moves
            u = 0 if za else _rotl(R[ia], OFF[ia] - d)
            t = (u ^ R[ib]) & MASKD[d]
            R[ib] ^= t; R[ia] = u ^ t; OFF[ia] = d % 256
        else:                                      # a even: b moves
            v = 0 if zb else _rotl(R[ib], OFF[ib] + d)
            t = (R[ia] ^ v) & (W ^ MASKD[d])
            R[ia] ^= t; R[ib] = v ^ t; OFF[ib] = (-d) % 256
        Z[ia] = Z[ib] = False
    for g in BLOCKS:
        for d in P1ORDER[g]:
            for q in range(W1):
                r = W1 * g + q
                if not r & d:
                    swap(r, r + d, d)
    for gi in range(W1):
        for d in P2ORDER[gi]:
            for i in range(NB):
                r = W1 * i + gi
                if not r & d:
                    swap(r, r + d, d)
    for r in range(256):
        if OFF[r]:
            R[r] = _rotl(R[r], OFF[r]); ops += 1
    return R, ops


def decode_slot(q):
    """Processing index q (0..255) of a z-step -> group slot (bit position)."""
    return W1 * (q % NB) + q // NB


PROC = [decode_slot(q) for q in range(256)]
assert sorted(PROC) == list(range(256))
assert transpose_z([0] * 256)[1] == 3418   # Lemma 9 / ledger (16-row layout): ALU ops incl. 128 frame fixes


# ---------------- linear-structure support and incremental round 2 ----------
def _dst(L, b):
    """A2 word (lane L, bit b) -> round-2 chi position (X, Y, plane)."""
    x, y = L % 5, L // 5
    return y, (2 * x + 3 * y) % 5, (b + RHO[L]) % 64


def support(j):
    """Lemma 3: the 22 A2 words flipped (by all-ones, in every group) by z-bit j:
    the two round-1 chi outputs carrying z and the 4 x 5 words of the round-2
    D columns they change."""
    S = set()
    for L in (1, 6):
        X, Y, p = _dst(L, j)
        S.add((X + 5 * Y, p))
    for L, b in list(S):
        for xx, bb in (((L % 5 + 1) % 5, b), ((L % 5 - 1) % 5, (b + 1) % 64)):
            for y in range(5):
                S ^= {(xx + 5 * y, bb)}
    return sorted(S)


SUPPORT = [support(j) for j in range(32)]
assert all(len(s) == 22 for s in SUPPORT)
WT = -1      # the all-ones term of a patch expression


def patch_exprs(j):
    """Lemma 6: O2P word -> set of terms (A2 word indices of the NEW A2, WT)
    whose XOR is the change of that O2P word when z-bit j flips."""
    S = SUPPORT[j]
    flips = {64 * L + b for L, b in S}
    rows = {}
    for L, b in S:
        X, Y, p = _dst(L, b)
        rows.setdefault((Y, p), set()).add(X)
    dout = {}
    for (Y, p), Xs in rows.items():
        c = [1 if X in Xs else 0 for X in range(5)]
        for k in range(5):
            k1, k2 = (k + 1) % 5, (k + 2) % 5
            e = set()
            if c[k] ^ c[k2] ^ (c[k1] & c[k2]):
                e ^= {WT}
            if c[k2]:
                L_, b_ = _bsrc(k1, Y, p)
                e ^= {64 * L_ + b_}
            if c[k1]:
                L_, b_ = _bsrc(k2, Y, p)
                e ^= {64 * L_ + b_}
            if e:
                dout[(k, Y, p)] = frozenset(e)
    dC = {}
    for (x, Y, b), v in dout.items():
        dC[(x, b)] = dC.get((x, b), frozenset()) ^ v
    patch = {64 * (x + 5 * Y) + b: v for (x, Y, b), v in dout.items()}
    for (x, b), v in dC.items():
        for xx, bb in (((x + 1) % 5, b), ((x - 1) % 5, (b + 1) % 64)):
            for Y in range(5):
                w = 64 * (xx + 5 * Y) + bb
                patch[w] = patch.get(w, frozenset()) ^ v
    out = {}
    for w, v in patch.items():
        v = set(v)
        for t in list(v):
            if t != WT and t in flips:     # read after the flip: old = new ^ all-ones
                v ^= {WT}
        if v:
            out[w] = frozenset(v)
    return out


PATCH = [patch_exprs(j) for j in range(32)]
READS = frozenset(t for pe in PATCH for e in pe.values() for t in e if t != WT)
# The program flips only support words that some patch expression reads, and
# stores A2 word i complemented iff i is in PI (a compile-time storage polarity
# chosen to minimise NOTs); every patch term is read in that encoding.
FLIPS = [sorted({64 * L + b for L, b in SUPPORT[j]} & READS) for j in range(32)]
PI = frozenset(i for i in range(1600) if (int.from_bytes(bytes.fromhex(
    "0000ffffffff0000ffffff3f0000feffe0ff010000000000ff1f0000000000fcffff3f000000c0ffffffff0180ffffffff07000000f8ffffffffff0f000000f00000000000000000000000f0ffffff0fff070000c0ffffff7f0000000000feff1cf07f0000000000ffff01000000feff0000000000000000ffffffff3f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000fe070000000000000000000000"), "little") >> i) & 1)
PATCHP = []
for _pe in PATCH:
    _q = {}
    for _w, _e in _pe.items():
        _e = set(_e)
        for _t in list(_e):
            if _t != WT and _t in PI:
                _e ^= {WT}
        if _e:
            _q[_w] = (sorted(t for t in _e if t != WT), W if WT in _e else 0)
    PATCHP.append(sorted(_q.items()))
assert (len(READS), len(PI), sorted({len(p) for p in PATCHP}), sorted({len(f) for f in FLIPS})) == \
    (1152, 439, [508], [13, 14, 15, 16, 17, 18])


def incr_round2(A2S, O2P, j):
    """Flip the read support words of A2 (stored with polarity PI), then patch
    O2P with the exact round-2 output change of Lemma 6 (all terms read from
    the new A2; theta of round 3 included)."""
    for w in FLIPS[j]:
        A2S[w] ^= W
    for w, (ts, c) in PATCHP[j]:
        v = c
        for t in ts:
            v ^= A2S[t]
        O2P[w] ^= v


# ---------------- dependency cone (proof Lemma 10), checked by poisoning ----------
STARTS = (2, 39, 34)    # start plane of rounds 3, 4, 5 (stored raw; its D is the fix word)


def round_needs(ns, nf, fp_out, fp_in):
    """Needed stored words ns {(L, b)} and fix columns nf of a theta-at-store round
    with start plane fp_out whose input lacks D on plane fp_in ->
    (chi outputs, parities, needed input words, needed input fix columns)."""
    dd = {(L % 5, b) for L, b in ns if b != fp_out} | {(x, fp_out) for x in nf}
    par = set()
    for x, b in dd:
        par.add(((x - 1) % 5, b)); par.add(((x + 1) % 5, (b - 1) % 64))
    chi = set(ns) | {(x + 5 * y, b) for x, b in par for y in range(5)}
    ins = set()
    for L, b in chi:
        X, Y = L % 5, L // 5
        for k in range(3):
            ins.add(_bsrc((X + k) % 5, Y, b))
    return chi, par, ins, {L % 5 for L, b in ins if b == fp_in}


NEED5 = frozenset((L, (b - RHO[L]) % 64) for L in DIAG for b in KEEP)
FIX5 = frozenset(L % 5 for L, b in NEED5 if b == STARTS[2])
_c5, _p5, NEED4, FIX4 = round_needs(NEED5, FIX5, STARTS[2], STARTS[1])
_c4, _p4, NEED3, FIX3 = round_needs(NEED4, FIX4, STARTS[1], STARTS[0])
assert (len(NEED5), len(FIX5), len(_c5), len(_p5), len(NEED4), len(FIX4), len(_p4), len(NEED3), len(FIX3)) == \
    (175, 0, 1161, 229, 1363, 5, 320, 1600, 5)
POISON = [int.from_bytes(hashlib.sha256(b"poison" + i.to_bytes(2, "little")).digest(), "little") for i in range(1600)]


def poison(S, fix, need, fneed):
    """Replace every word outside the cone by an unrelated constant (Lemma 10 says none is read)."""
    return ([S[i] if (i >> 6, i & 63) in need else POISON[i] for i in range(1600)],
            [fix[x] if x in fneed else POISON[x] for x in range(5)])


# ---------------- batch ------------------------------------------------------
class Batch:
    """256 groups (bit positions); prefixes[p] is a structured 64-byte prefix."""

    def __init__(self, prefixes, zbits):
        self.prefixes = prefixes
        self.z = 0
        A2 = self.a2_true(0)
        for j in zbits:
            A2j = self.a2_true(1 << j)
            supp = {64 * L + b for L, b in SUPPORT[j]}
            for i in range(1600):
                if A2j[i] ^ A2[i] != (W if i in supp else 0):
                    raise RuntimeError("A2(e_j) ^ A2(0) is not all-ones exactly on the 22-word support")
        self.A2S = [v ^ (W if i in PI else 0) for i, v in enumerate(A2)]
        self.O2P = build_o2p(A2)

    def a2_true(self, z):
        """A2 (round 1 + round-2 theta) of the batch at z, computed from scratch."""
        S = [0] * 1600
        msgs = [message(p, z) for p in self.prefixes]
        for w in range(2):
            rows = [int.from_bytes(m[32 * w:32 * w + 32], "little") for m in msgs]
            S[256 * w:256 * w + 256] = transpose(rows, SETUP_ORDER)
        S[64 * 8 + 1] = W
        S[64 * 8 + 2] = W
        S[64 * 16 + 63] = W
        out, D2 = round_pass(S, d_words(S), RC[0])
        return [out[i] ^ D2[DCOL[i]] for i in range(1600)]

    def flip(self, j):
        self.z ^= 1 << j
        incr_round2(self.A2S, self.O2P, j)

    def check_o2p(self):
        A2 = self.a2_true(self.z)
        if any(self.A2S[i] != A2[i] ^ (W if i in PI else 0) for i in READS):
            raise RuntimeError("maintained A2 differs from A2 rebuilt from the prefixes")
        if build_o2p(A2) != self.O2P:
            raise RuntimeError("incrementally maintained O2P differs from O2P rebuilt from A2")

    def keys(self):
        """Stored keys key_of_digest(digest) indexed by slot."""
        S, fix = round_ts(self.O2P, None, None, PLAN3, STARTS[0])
        S, fix = round_ts(S, fix, STARTS[0], PLAN4, STARTS[1])
        S, fix = poison(S, fix, NEED4, FIX4)
        S, fix = round_ts(S, fix, STARTS[1], PLAN5, STARTS[2])
        S, fix = poison(S, fix, NEED5, FIX5)
        rows = last_rows(S, fix)
        if any(rows[r] for r in range(256) if r not in KEYROWS):
            raise RuntimeError("a key row outside ROWOF is nonzero")
        out, _ = transpose_z(rows)
        if out != transpose(rows, STEP_ORDER):
            raise RuntimeError("zero-row transpose differs from the full transpose")
        return out


def trial_prefixes(seed, groups):
    return [structured_prefix(int.from_bytes(hashlib.sha256(b"s3r6-ls-v1" + seed + g.to_bytes(2, "little")).digest(),
                                             "little")) for g in range(groups)]


def _check(prefix, z, key):
    if key_of_digest(int.from_bytes(sponge6(message(prefix, z)), "little")) != key:
        raise RuntimeError("bitsliced evaluator disagrees with direct sponge")


M128 = (1 << 128) - 1
KEYBITS = 4 * NP


class TagTable:
    """The program's tagged-id table (proof Section 5.3), run on the 140-bit keys
    of one batch as a self-check.  Slot S[K] (K < 2^140 is the address) holds
    TAG * 2^128 + floor(n / 2) (pair id: messages 2k and 2k + 1 of a z-step
    share one id, as in the program); a lookup is a candidate iff the high
    half equals TAG.
    Never-written words are adversarial garbage: 1/16 of the addresses return
    TAG in the high half with a junk id (forcing the verify-and-continue
    path), the rest a word whose high half differs from TAG."""

    def __init__(self, tag_seed):
        self.tag = int.from_bytes(hashlib.sha256(b"s3r6-tag" + tag_seed).digest()[:16], "little")
        self.mem = {}
        self.n = 0
        self.key_of = {}                # message number -> stored key
        self.garbage_candidates = 0

    def garbage(self, K):
        h = hashlib.sha256(b"s3r6-garbage" + K.to_bytes(18, "little")).digest()
        junk = int.from_bytes(h[:16], "little")
        hi = self.tag if h[16] < 16 else self.tag ^ (1 + int.from_bytes(h[17:25], "little"))
        return (hi << 128) | junk

    def step(self, K, verify):
        if not 0 <= K < 1 << KEYBITS:
            raise RuntimeError("key is not a 140-bit table address")
        w = self.mem[K] if K in self.mem else self.garbage(K)
        if (w ^ (self.tag << 128)) >> 128 == 0:            # candidate
            i = w & M128                                    # pair id: messages 2i, 2i + 1
            if 2 * i < self.n and self.mem.get(K) == w:
                if all(self.key_of.get(x) != K for x in (2 * i, 2 * i + 1)):
                    raise RuntimeError("stored pair id names no message with this key")
                for x in (2 * i, 2 * i + 1):
                    if x < self.n:                          # x == n is the current message itself
                        verify(x, self.n)                   # full digests compared; continue
            else:
                self.garbage_candidates += 1                # verified and continued in the program
        self.mem[K] = (self.tag << 128) | (self.n >> 1)
        self.key_of[self.n] = K
        self.n += 1

    def check_ids(self):
        for K, w in self.mem.items():
            if w >> 128 != self.tag or all(self.key_of.get(x) != K for x in (2 * (w & M128), 2 * (w & M128) + 1)):
                raise RuntimeError("table word does not name a pair with a message of its key")


def run_trials(seeds, layout, mask_le):
    kmask = key_mask_of(mask_le)
    G, zs = LAYOUTS[layout]
    per = 256 // G
    zbits = sorted({(a ^ b).bit_length() - 1 for a, b in zip(zs, zs[1:])})
    results = []
    for c0 in range(0, len(seeds), per):
        chunk = seeds[c0:c0 + per]
        pres = [trial_prefixes(s, G) for s in chunk]
        slots = [p for ps in pres for p in ps]
        slots += [structured_prefix(0)] * (256 - len(slots))
        batch = Batch(slots, zbits)
        table = TagTable(b"".join(chunk))

        def verify(i, n, pres=pres):
            """Rebuild both messages from their numbers and compare full digests."""
            ms = []
            for v in (i, n):
                t_, q_ = v >> 8, v & 255
                ti_, g_ = divmod(decode_slot(q_), G)
                ms.append(message(pres[ti_][g_], zs[t_]) if ti_ < len(pres) else None)
            if ms[0] is not None and ms[0] != ms[1] and sponge6(ms[0]) == sponge6(ms[1]):
                raise RuntimeError("full collision at experiment scale (not expected)")
        state = [{"seen": {}, "first": None, "pairs": 0, "checks": 0} for _ in chunk]
        for t, z in enumerate(zs):
            if t:
                batch.flip((z ^ zs[t - 1]).bit_length() - 1)
            keys = batch.keys()
            pow2 = t > 0 and not t & (t - 1)
            done = set()
            for p in PROC:                  # processing order of the program
                table.step(keys[p], verify)
                ti, g = divmod(p, G)
                if ti >= len(chunk):
                    continue
                st = state[ti]
                key = keys[p]
                if st["checks"] < EXACT_CHECKS or (pow2 and ti not in done):
                    _check(pres[ti][g], z, key)
                    st["checks"] += 1
                    done.add(ti)
                k = key & kmask             # equal masked keys <=> equal masked digests
                hit = st["seen"].get(k)
                if hit is None:
                    st["seen"][k] = [(g, z)]
                else:
                    st["pairs"] += len(hit)
                    if st["first"] is None:
                        st["first"] = (hit[0], (g, z))
                    hit.append((g, z))
        batch.check_o2p()
        table.check_ids()
        if table.garbage_candidates == 0 and len(zs) * 256 >= 512:
            raise RuntimeError("the adversarial garbage path was never taken")
        for ti, st in enumerate(state):
            obs = {"masked_pairs": st["pairs"], "messages": G * len(zs), "exactness_checks": st["checks"],
                   "support_columns_checked": len(zbits), "o2p_rebuild_checked": 1}
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
        sq = sum(o["masked_pairs"] ** 2 for _, _, o in res)
        print(json.dumps({"layout": layout, "trials": trials, "successes": succ, "masked_pairs": pairs,
                          "masked_pairs_sq": sq}))
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
