"""Scaled analogue of the bitsliced grouped birthday search of proof.md (sha3-256-r5).

Stdlib only. Organizer mode (default): read one JSON request on stdin and write
one JSON result. Every digest used for matching is computed ONLY by the
bitsliced grouped evaluator of proof.md Sections 3-5:

  * a batch is 256 bit positions; bit position p of every 256-bit word belongs
    to one group (one 64-byte prefix); word P(L, b) holds bit b of lane L for
    all 256 groups at once;
  * per batch, A2 (the round-2 theta output) is built for z = 0 and the
    coefficient words COEF[j] (A2(e_j) XOR A2(0) on the 62 support positions of
    Lemma 2) are built by the same bitsliced round code; as z walks in Gray
    order, A2 is updated by XORing COEF[j] into the 62 support words;
  * rounds 2-4 run on the bitsliced words; the theta D words for the next
    round are formed by a separate d_words() pass over each round's output
    (mathematically identical to the fused round of proof Section 5);
  * round 5 (the last) computes only chi row 0, lanes 0..3, at all 64 bit planes: 256
    key rows (row k = bit k of the digest read little-endian);
  * a 256 x 256 delta-swap bit transpose (stages 1..16 in blocks of 32 rows,
    then stages 32..128) turns the 256 rows into one 256-bit key per group.

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
processing order, plus the last key of the trial (last group at the last,
Gray-updated z), are compared at full 256-bit width with an independent
direct 5-round sponge (sponge5: its own rho offsets and round constants from
the standard recurrences); and, for every coefficient column built, A2(e_j)
XOR A2(0) is checked to vanish outside the 62 support positions. A failure
raises, so the organizer run fails visibly.

The first pair of distinct messages whose masked digests agree is returned; a
trial with no such pair returns two nulls. Observations are informational.

Local modes (not used by the organizer):
  python3 FILE --local LAYOUT TRIALS SEED   real target, local seeds
"""

import hashlib
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


# rho/pi gather tables in output order p = 64*(X + 5Y) + b
SRC = []      # source word index 64*Lsrc + (b - rho) mod 64
DIDX = []     # D word index 64*xsrc + (b - rho) mod 64
for _Y in range(5):
    for _X in range(5):
        _xs, _ys = _pi_src(_X, _Y)
        _L = _xs + 5 * _ys
        for _b in range(64):
            _bs = (_b - RHO[_L]) % 64
            SRC.append(64 * _L + _bs)
            DIDX.append(64 * _xs + _bs)
CHI = []
for _Y in range(5):
    for _X in range(5):
        for _b in range(64):
            CHI.append((64 * ((_X + 1) % 5 + 5 * _Y) + _b, 64 * ((_X + 2) % 5 + 5 * _Y) + _b))
CHI1 = [a for a, _ in CHI]
CHI2 = [b for _, b in CHI]
DPREV = [64 * ((x - 1) % 5) + b for x in range(5) for b in range(64)]
DNEXT = [64 * ((x + 1) % 5) + (b - 1) % 64 for x in range(5) for b in range(64)]


def d_words(S):
    """Theta D words (index 64x + b) of a bitsliced state."""
    C = [S[i] ^ S[i + 320] ^ S[i + 640] ^ S[i + 960] ^ S[i + 1280] for i in range(320)]
    return [C[p] ^ C[n] for p, n in zip(DPREV, DNEXT)]


def round_pass(S, D, rc):
    """theta (if D given) + rho + pi + chi + iota; returns (state, D of output)."""
    if D is None:
        B = [S[s] for s in SRC]
    else:
        B = [S[s] ^ D[d] for s, d in zip(SRC, DIDX)]
    out = [v ^ (~B[i] & B[j]) for v, i, j in zip(B, CHI1, CHI2)]
    for b in range(64):
        if (rc >> b) & 1:
            out[b] ^= W
    return out, d_words(out)


def round5_rows(S, D):
    """Digest rows k = 64x + b (x = 0..3) of round 5 (the last): chi row 0 only."""
    B = [S[SRC[p]] ^ D[DIDX[p]] for p in range(320)]          # output row Y = 0
    rows = [B[p] ^ (~B[CHI1[p]] & B[CHI2[p]]) for p in range(256)]
    for b in range(64):
        if (RC[4] >> b) & 1:
            rows[b] ^= W
    return rows


def _mask(d):
    m = 0
    for c in range(256):
        if not c & d:
            m |= 1 << c
    return m


MASKD = {d: _mask(d) for d in (1, 2, 4, 8, 16, 32, 64, 128)}
PAIRS1 = [(d, [(blk + r, blk + r + d) for blk in range(0, 256, 32) for r in range(32) if not r & d])
          for d in (1, 2, 4, 8, 16)]
PAIRS2 = [(d, [(r + 32 * i, r + 32 * i + d) for r in range(32) for i in range(8) if not (i & (d // 32))])
          for d in (32, 64, 128)]


def transpose(rows):
    """256 x 256 bit transpose by delta swaps (phase 1 then phase 2)."""
    R = list(rows)
    for d, pairs in PAIRS1 + PAIRS2:
        m = MASKD[d]
        for i0, i1 in pairs:
            a, b = R[i0], R[i1]
            t = ((a >> d) ^ b) & m
            R[i0] = a ^ (t << d)
            R[i1] = b ^ t
    return R


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
        out, D2 = round_pass(S, D1, RC[0])
        self.A2 = [out[i] ^ D2[64 * ((i // 64) % 5) + i % 64] for i in range(1600)]
        self.coef = {}
        for j in zbits:
            S2 = list(S)
            S2[j] ^= W
            S2[64 * 5 + j] ^= W
            if d_words(S2) != D1:
                raise RuntimeError("round-1 theta not invariant under the z flip")
            o2, D22 = round_pass(S2, D1, RC[0])
            A2j = [o2[i] ^ D22[64 * ((i // 64) % 5) + i % 64] for i in range(1600)]
            supp = set(SUPPORT[j])
            for i in range(1600):
                if i not in supp and A2j[i] != self.A2[i]:
                    raise RuntimeError("z-dependence outside the 62-word support")
            self.coef[j] = [A2j[i] ^ self.A2[i] for i in SUPPORT[j]]

    def flip(self, j):
        A2 = self.A2
        for i, c in zip(SUPPORT[j], self.coef[j]):
            A2[i] ^= c

    def keys(self):
        S, D = round_pass(self.A2, None, RC[1])
        for r in (2, 3):
            S, D = round_pass(S, D, RC[r])
        return transpose(round5_rows(S, D))


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
        for t, z in enumerate(zs):
            if t:
                batch.flip((z ^ zs[t - 1]).bit_length() - 1)
            keys = batch.keys()
            for ti, st in enumerate(state):
                for g in range(G):
                    key = keys[ti * G + g]
                    if st["checks"] < EXACT_CHECKS or (t == len(zs) - 1 and g == G - 1):
                        if int.from_bytes(sponge5(message(pres[ti][g], z)), "little") != key:
                            raise RuntimeError("bitsliced evaluator disagrees with direct sponge")
                        st["checks"] += 1
                    k = key & mask_le
                    hit = st["seen"].get(k)
                    if hit is None:
                        st["seen"][k] = [(g, z)]
                    else:
                        st["pairs"] += len(hit)
                        if st["first"] is None:
                            st["first"] = (hit[0], (g, z))
                        hit.append((g, z))
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
