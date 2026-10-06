"""Scaled analogue of the bitsliced grouped birthday search of proof.md (sha3-256-r5, v2).

Stdlib only. Organizer mode (default): read one JSON request on stdin and write
one JSON result. Every digest used for matching is computed ONLY by the
bitsliced grouped evaluator of proof.md Sections 4-5 (v2 program):

  * a batch is 256 bit positions; bit position p of every 256-bit word belongs
    to one group (one 64-byte prefix); word P(L, b) holds bit b of lane L for
    all 256 groups at once;
  * per batch, A2 (the round-2 theta output) is built for z = 0 and the
    coefficient words COEF[j] (A2(e_j) XOR A2(0) on the 62 support words of
    Lemma 3) by the same bitsliced round code; O2 = theta_3(round 2(A2)), the
    theta'd round-2 output, is built once per batch in the lane-complemented
    encoding Q3 (Section 4.3);
  * a Gray step on z-bit j XORs COEF[j] into A2 on its 62 support words and
    patches O2 by the exact chi difference of the affected round-2 chi rows
    plus the induced change of the round-3 D words (incremental round 2,
    Section 4.4); O2 is never recomputed between z-steps (it is compared with
    a fresh recomputation at the last z of every batch);
  * round 3 (full) and round 4 run with theta applied before the store and
    lane-complemented chi (AND/OR gate per output; polarity patterns P34 and
    P5); round 5 (the last) computes only chi row 0, lanes 0..3, at all 64
    planes from the 5 diagonal lanes: 256 key rows, row k = bit k of the
    stored key K = digest (read little-endian) XOR KEYMASK;
  * a 256 x 256 delta-swap bit transpose, stages 1,2,4,64,128 then 8,16,32
    (the stage order of the counted program), turns the rows into one key per
    group; messages are offered in the processing order q = 0..255,
    slot p = decode_slot(q).

Several trials share one batch (each trial owns G consecutive bit positions);
bitwise operations never mix bit positions and the transpose only relocates
bits, so trials stay independent: each trial's output depends on its own seed.

Scale: N_t = 2^9 messages per trial and an 18-bit digest mask, so
N_t^2 / 2^18 = 1 = N^2 / 2^256 as in the full attack. Layouts (G groups per
trial x Z values of z, z in Gray order):

  k5r5-bs-full-width   : 256 groups x 2,  z = gray(t), t < 2 (one trial fills
                         a whole batch; groups far outnumber group size)
  k5r5-bs-spread       : 16 groups x 32,  z = gray(t), t < 32
  k5r5-bs-single-group : 1 group x 512,   z = gray(t), t < 512
  k5r5-bs-high-z       : 4 groups x 128,  z = gray(t) << 25, t < 128 (Gray
                         updates on z bits 25..31)

Full-width exactness self-checks, every trial: the first EXACT_CHECKS keys in
processing order, plus the last key of the trial in processing order at the
last, Gray-updated z, are compared at full 256-bit width (after removing
KEYMASK) with an independent direct 5-round sponge (sponge5: its own rho
offsets and round constants from the standard recurrences); for every
coefficient column built, A2(e_j) XOR A2(0) is checked to vanish outside the
62 support words; and at the last z of every batch the incrementally updated
O2 is checked against a fresh recomputation from A2. A failure raises, so the
organizer run fails visibly.

The first pair of distinct messages whose masked digests agree is returned; a
trial with no such pair returns two nulls. Observations are informational.

Local modes (not used by the organizer):
  python3 FILE --local LAYOUT TRIALS SEED   real target, local seeds
"""

import hashlib
import itertools
import json
import sys

M64 = (1 << 64) - 1
W = (1 << 256) - 1
RC = (0x0000000000000001, 0x0000000000008082, 0x800000000000808A,
      0x8000000080008000, 0x000000000000808B)
RHO = (0, 1, 62, 28, 27, 36, 44, 6, 55, 20, 3, 10, 43, 25, 39,
       41, 45, 15, 21, 8, 18, 2, 61, 56, 14)
EXACT_CHECKS = 4

LAYOUTS = {   # groups per trial, list of z in processing order
    "k5r5-bs-full-width": (256, [t ^ (t >> 1) for t in range(2)]),
    "k5r5-bs-spread": (16, [t ^ (t >> 1) for t in range(32)]),
    "k5r5-bs-single-group": (1, [t ^ (t >> 1) for t in range(512)]),
    "k5r5-bs-high-z": (4, [(t ^ (t >> 1)) << 25 for t in range(128)]),
}
MASKS = {
    "k5r5-bs-full-width": "1f00000000000000001f00000000000000000f00000000000000000f00000000",
    "k5r5-bs-spread": "0000f80000000000000000001f0000000000000000f00000000000000f000000",
    "k5r5-bs-single-group": "00000000000000f800000000000000f800000000000000f000000000000000f0",
    "k5r5-bs-high-z": "000000001f00000000000000001f00000000000000000f00000f000000000000",
}


# ---------------- independent direct sponge (exactness reference) ----------
def _keccak_tables():
    rho = [[0] * 5 for _ in range(5)]
    x, y = 1, 0
    for t in range(24):
        rho[x][y] = ((t + 1) * (t + 2) // 2) % 64
        x, y = y, (2 * x + 3 * y) % 5
    rc, r = [], 1
    for _ in range(5):
        c = 0
        for j in range(7):
            if r & 1:
                c |= 1 << ((1 << j) - 1)
            r = ((r << 1) ^ 0x71) & 0xFF if r & 0x80 else r << 1
        rc.append(c)
    return rho, rc


_TABLES = _keccak_tables()


def sponge5(msg):
    """Direct SHA3-256 sponge with Keccak rounds 0..4 on one 136-byte block."""
    rho, rc = _TABLES
    block = bytearray(msg) + bytearray(136 - len(msg))
    block[len(msg)] ^= 0x06
    block[135] ^= 0x80
    a = [[int.from_bytes(block[8 * (x + 5 * y):8 * (x + 5 * y) + 8], "little") if x + 5 * y < 17 else 0
          for y in range(5)] for x in range(5)]
    for rnd in range(5):
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


# ---------------- bitsliced evaluator ----------------------------------------
# word index of P(L, b) is 64*L + b
def _pi_src(X, Y):
    return ((Y - 3 * X) * 3) % 5, X


SRC = []      # rho/pi gather: B word (X, Y, b) at 64*(X+5Y)+b reads SRC[...]
SRCL = []     # source lane of output lane X + 5Y
for _Y in range(5):
    for _X in range(5):
        _xs, _ys = _pi_src(_X, _Y)
        _L = _xs + 5 * _ys
        SRCL.append(_L)
        for _b in range(64):
            SRC.append(64 * _L + (_b - RHO[_L]) % 64)
DPREV = [64 * ((x - 1) % 5) + b for x in range(5) for b in range(64)]
DNEXT = [64 * ((x + 1) % 5) + (b - 1) % 64 for x in range(5) for b in range(64)]
DIAG = (0, 6, 12, 18, 24)


def d_words(S):
    """Theta D words (index 64x + b) of a bitsliced state."""
    C = [S[i] ^ S[i + 320] ^ S[i + 640] ^ S[i + 960] ^ S[i + 1280] for i in range(320)]
    return [C[p] ^ C[n] for p, n in zip(DPREV, DNEXT)]


def theta_apply(S):
    D = d_words(S)
    return [S[i] ^ D[64 * ((i // 64) % 5) + i % 64] for i in range(1600)]


def round1(S, D1):
    """Setup only: theta (given D) + rho + pi + chi + iota, true values."""
    B = [S[s] ^ D1[64 * ((s // 64) % 5) + s % 64] for s in SRC]
    out = [0] * 1600
    for Y in range(5):
        for X in range(5):
            o1, o2 = 64 * ((X + 1) % 5 + 5 * Y), 64 * ((X + 2) % 5 + 5 * Y)
            base = 64 * (X + 5 * Y)
            for b in range(64):
                out[base + b] = B[base + b] ^ (~B[o1 + b] & B[o2 + b])
    for b in range(64):
        if (RC[0] >> b) & 1:
            out[b] ^= W
    return out


# ---- lane-complement polarity (Keccak team's lane complementing; tekkac b001199a)
P34 = 1336081       # chi-output polarity pattern of round 2 and round 3 (bit L)
P5 = 1188625        # chi-output polarity pattern of round 4


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


Q3 = fpol(P34)
QLAST = fpol(P5)
_ROWCACHE = {}


def solve_row(q, p, iota, outs):
    """Cheapest gate plan of one chi row: q input polarities, p wanted output
    polarities (bit X), iota flip of output 0 (as in the counted program)."""
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


def chi_row(Bv, S, plan):
    comp = {k: ~Bv[k] & W for k in S}
    out = {}
    for X, (ca, cb, cc, gate, on) in plan.items():
        a = comp[X] if ca else Bv[X]
        b_ = comp[(X + 1) % 5] if cb else Bv[(X + 1) % 5]
        c_ = comp[(X + 2) % 5] if cc else Bv[(X + 2) % 5]
        o = a ^ ((b_ & c_) if gate == "and" else (b_ | c_))
        out[X] = o ^ W if on else o
    return out


def round_ts(S, qin, pout, rc):
    """One round from a theta'd input S stored with lane polarities qin; chi
    outputs in polarities pout, then the next round's theta applied before the
    store: returns the theta'd output, stored with polarities fpol(pout)."""
    out = [0] * 1600
    for Y in range(5):
        qrow = sum(lanepol(qin, SRCL[X + 5 * Y]) << X for X in range(5))
        prow = (pout >> (5 * Y)) & 31
        plans = [solve_row(qrow, prow, io, range(5)) for io in (0, 1)]
        for b in range(64):
            io = (rc >> b) & 1 if Y == 0 else 0
            _, Sx, plan = plans[io]
            o = chi_row([S[SRC[64 * (X + 5 * Y) + b]] for X in range(5)], Sx, plan)
            for X in range(5):
                out[64 * (X + 5 * Y) + b] = o[X]
    return theta_apply(out)


def last_plan(b):
    q = sum(lanepol(QLAST, DIAG[X]) << X for X in range(5))
    io = (RC[4] >> b) & 1
    best = None
    for p in range(16):
        r = solve_row(q, p, io, range(4))
        if best is None or r[0] < best[0][0]:
            best = (r, p)
    return best


LASTPLAN = [last_plan(b) for b in range(64)]
KEYMASK = 0
for _b in range(64):
    for _x in range(4):
        KEYMASK |= ((LASTPLAN[_b][1] >> _x) & 1) << (64 * _x + _b)


def last_rows(S):
    """Round 5 (the last), chi row 0, lanes 0..3, from the 5 diagonal lanes:
    row k = 64x + b is bit k of the stored key (digest XOR KEYMASK)."""
    rows = [0] * 256
    for b in range(64):
        (_, Sx, plan), _ = LASTPLAN[b]
        o = chi_row([S[64 * DIAG[X] + (b - RHO[DIAG[X]]) % 64] for X in range(5)], Sx, plan)
        for x in range(4):
            rows[64 * x + b] = o[x]
    return rows


def _mask(d):
    m = 0
    for c in range(256):
        if not c & d:
            m |= 1 << c
    return m


MASKD = {d: _mask(d) for d in (1, 2, 4, 8, 16, 32, 64, 128)}
STAGES = (1, 2, 4, 64, 128, 8, 16, 32)       # stage order of the counted program


def transpose(rows, stages=STAGES):
    """256 x 256 bit transpose by delta swaps (the 8 stages commute)."""
    R = list(rows)
    for d in stages:
        m = MASKD[d]
        for i0 in range(256):
            if not i0 & d:
                a, b = R[i0], R[i0 + d]
                t = ((a >> d) ^ b) & m
                R[i0] = a ^ (t << d)
                R[i0 + d] = b ^ t
    return R


def decode_slot(q):
    """Processing index q (0..255) of a z-step -> slot (bit position) p."""
    gi, i = q >> 3, q & 7
    return 64 * (gi >> 3) + 8 * i + (gi & 7)


ORDER = [decode_slot(q) for q in range(256)]
assert sorted(ORDER) == list(range(256))


def support(j):
    jp = (j + 36) % 64
    pos = set()
    for x, b in ((1, j), (4, j + 1), (1, jp), (4, jp + 1), (4, j), (2, j + 1),
                 (0, j), (3, j + 1), (0, jp), (3, jp + 1), (2, jp), (0, jp + 1)):
        for y in range(5):
            pos.add(64 * (x + 5 * y) + b % 64)
    pos.add(64 * 3 + j)
    pos.add(64 * 19 + jp)
    return sorted(pos)


SUPPORT = [support(j) for j in range(32)]
assert all(len(s) == 62 for s in SUPPORT)
# inverse rho/pi map: A2 word -> B word index 64*(X+5Y)+b
INV = [0] * 1600
for _i, _s in enumerate(SRC):
    INV[_s] = _i
# round-2 chi rows touched by a z_j update: (Y, b) of each changed B word
ROWS2 = [sorted({((INV[i] // 64) // 5, INV[i] % 64) for i in SUPPORT[j]}) for j in range(32)]


def chi_true(Bv):
    return [Bv[X] ^ (~Bv[(X + 1) % 5] & Bv[(X + 2) % 5]) for X in range(5)]


class Batch:
    """256 groups (bit positions); prefixes[p] is a 64-byte prefix (or zeros)."""

    def __init__(self, prefixes, zbits):
        S = [0] * 1600
        for w in range(2):
            rows = [int.from_bytes(p[32 * w:32 * w + 32], "little") for p in prefixes]
            S[256 * w:256 * w + 256] = transpose(rows)
        S[64 * 8 + 1] = W
        S[64 * 8 + 2] = W
        S[64 * 16 + 63] = W
        D1 = d_words(S)                     # round-1 D, independent of z (Lemma 1)
        self.A2 = theta_apply(round1(S, D1))
        self.coef = {}
        for j in zbits:
            S2 = list(S)
            S2[j] ^= W
            S2[64 * 5 + j] ^= W
            if d_words(S2) != D1:
                raise RuntimeError("round-1 theta not invariant under the z flip")
            A2j = theta_apply(round1(S2, D1))
            supp = set(SUPPORT[j])
            for i in range(1600):
                if i not in supp and A2j[i] != self.A2[i]:
                    raise RuntimeError("z-dependence outside the 62-word support")
            self.coef[j] = [A2j[i] ^ self.A2[i] for i in SUPPORT[j]]
        self.O2 = self.fresh_o2()

    def fresh_o2(self):
        """O2 = theta_3(round 2(A2)) in polarity Q3 (A2 itself is uncomplemented)."""
        return round_ts(self.A2, 0, P34, RC[1])

    def flip(self, j):
        """Gray step on z-bit j: A2 ^= COEF[j]; O2 ^= exact chi difference of the
        touched round-2 rows XOR the induced round-3 D-word change."""
        A2 = self.A2
        old = {(Y, b): chi_true([A2[SRC[64 * (X + 5 * Y) + b]] for X in range(5)]) for Y, b in ROWS2[j]}
        for i, c in zip(SUPPORT[j], self.coef[j]):
            A2[i] ^= c
        dout = {}
        for Y, b in ROWS2[j]:
            new = chi_true([A2[SRC[64 * (X + 5 * Y) + b]] for X in range(5)])
            for X in range(5):
                d = new[X] ^ old[(Y, b)][X]
                if d:
                    dout[64 * (X + 5 * Y) + b] = d
        dC = [0] * 320
        for i, d in dout.items():
            dC[64 * ((i // 64) % 5) + i % 64] ^= d
        dD = [dC[p] ^ dC[n] for p, n in zip(DPREV, DNEXT)]
        O2 = self.O2
        for i in range(1600):
            v = dout.get(i, 0) ^ dD[64 * ((i // 64) % 5) + i % 64]
            if v:
                O2[i] ^= v

    def keys(self):
        """Stored keys (digest XOR KEYMASK) of the 256 slots at the current z."""
        S4 = round_ts(self.O2, Q3, P34, RC[2])          # round 3
        S5 = round_ts(S4, fpol(P34), P5, RC[3])         # round 4
        return transpose(last_rows(S5))                  # round 5 (last) + transpose


def trial_prefixes(seed, groups):
    return [b"".join(hashlib.sha256(b"s3r5-bitslice-v1" + seed + g.to_bytes(2, "little") + bytes((k,))).digest()
                     for k in (0, 1)) for g in range(groups)]


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
        state = [{"seen": {}, "first": None, "pairs": 0, "checks": 0} for _ in chunk]
        order = [(p // G, p % G) for p in ORDER if p // G < len(chunk)]
        lastg = {}
        for ti, g in order:
            lastg[ti] = g
        for t, z in enumerate(zs):
            if t:
                batch.flip((z ^ zs[t - 1]).bit_length() - 1)
            keys = batch.keys()
            for ti, g in order:
                st = state[ti]
                dig = keys[ti * G + g] ^ KEYMASK
                if st["checks"] < EXACT_CHECKS or (t == len(zs) - 1 and g == lastg[ti]):
                    if int.from_bytes(sponge5(message(pres[ti][g], z)), "little") != dig:
                        raise RuntimeError("bitsliced evaluator disagrees with direct sponge")
                    st["checks"] += 1
                k = dig & mask_le
                hit = st["seen"].get(k)
                if hit is None:
                    st["seen"][k] = [(g, z)]
                else:
                    st["pairs"] += len(hit)
                    if st["first"] is None:
                        st["first"] = (hit[0], (g, z))
                    hit.append((g, z))
        if batch.O2 != batch.fresh_o2():
            raise RuntimeError("incremental round-2 output disagrees with recomputation")
        for ti, st in enumerate(state):
            obs = {"masked_pairs": st["pairs"], "messages": G * len(zs), "exactness_checks": st["checks"],
                   "support_columns_checked": len(zbits)}
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
    if request["schema_version"] != 1 or request["target_profile"] != "sha3-256-r5-prefix-v1":
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
