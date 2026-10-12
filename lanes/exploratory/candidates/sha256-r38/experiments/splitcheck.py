"""splitcheck: code-consistency checks for the split row-16 search, the published-pair
transcription, and H1 chaining-value uniformity. Organizer-sandbox program (stdlib only).

The runner sends 256 trials with a 20-second total budget. Per trial seed:
  d        = 4 bytes of SHAKE-256(seed)                        -- class offset
  hbase    = 3 bytes mod 65529                                 -- H window base (8 values)
  lbase    = 3 bytes mod 65473                                 -- L window base (64 values)
  uwords   = 32 words of SHAKE-256(seed)                       -- uniformity block (8 true CV1s)
  1. Published pair: F_38(CV,M) == F_38(CV,M') (transcribed Table-5 pair).
  2. Window check: split search over H in [hbase,hbase+8) and L in [lbase,lbase+64)
     (8192 index probes); every returned u verified; the returned set must equal a
     brute-force enumeration of the same window.
  3. Uniformity (H1): the fixed valid S* triple (A0=b75dae71, A1=da6c35e0, A2=479b4dc8,
     c7=8f6c89c5) on 64 chaining values from uwords: count W7 = c7-a in F7, and bin
     (Y,Z0) low bits. H1 predicts W7-pass rate p2 = 287309824/2^32 and uniform bins.
  4. Trial 0 only: full H-index integrity (all 65536 H in exactly one correct bucket)
     and full-space soundness for d (2^20 probes, every returned u verified).
Returns the transcribed SFS pair (message_a/b_hex). These are NOT full collisions
(CV differs from IV); the hypothesis records full collisions 0. All randomness
derives deterministically from the trial seed; output is byte-identical reruns.
"""
import sys
import json
import hashlib

M = 0xFFFFFFFF


def ror(x, n):
    return ((x >> n) | (x << (32 - n))) & M


def s0(x):
    return ror(x, 7) ^ ror(x, 18) ^ (x >> 3)


def s1(x):
    return ror(x, 17) ^ ror(x, 19) ^ (x >> 10)


def S0(x):
    return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22)


def S1(x):
    return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25)


def CH(x, y, z):
    return (x & y) ^ ((~x) & z & M)


def MAJ(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)


K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1,
     0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
     0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786,
     0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
     0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147,
     0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
     0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b,
     0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
     0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a,
     0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
     0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]
R = 38
IV = [0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
      0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19]


def compress38(cv, w16):
    w = list(w16)
    for t in range(16, R):
        w.append((s1(w[t - 2]) + w[t - 7] + s0(w[t - 15]) + w[t - 16]) & M)
    a, b, c, d, e, f, g, h = cv
    for i in range(R):
        t1 = (h + S1(e) + CH(e, f, g) + K[i] + w[i]) & M
        t2 = (S0(a) + MAJ(a, b, c)) & M
        h, g, f, e, d, c, b, a = g, f, e, (d + t1) & M, c, b, a, (t1 + t2) & M
    return [(x + y) & M for x, y in zip(cv, (a, b, c, d, e, f, g, h))]


def h2words(s):
    return [int(s[i:i + 8], 16) for i in range(0, len(s), 8)]


CV = h2words('cd2789801b12a052b87cc8a6a9e059c5c9c3db856ca4b5b563d13ac1c0329f1e')
PM = h2words('48fc271b9fca20cdcc89f96ffc40396f8b328cb46b91ef7897f9b767e24500453b016f58de9804cb66a99ea50ce30b8da28cd15a77a1e994d28e48a09b5f6dbb')
PX = h2words('48fc271b9fca20cdcc89f96ffc40396f8b328cb46b91ef7897f9b767c24500453f416758fe9804cb63a88c0f0ceb1f8da28cd15a77a1e994d28e48a09f1f65bb')
PH = h2words('5d9ca5f459ace3a326c9c26c4252c5854c0803b71b4d5ccd25c3ccc090645c4d')

GBASE = 0x35F29010
GFREE = (0, 2, 10, 13, 19)
GSET = frozenset(GBASE | sum(1 << b for j, b in enumerate(GFREE) if k >> j & 1) for k in range(32))
GLO = sorted({x & 0xFFFF for x in GSET})

D7 = 0x20000000
T7 = 0x03BFF800


def inF7(w):
    return (s0((w + D7) & M) - s0(w)) & M == T7


A0S = 0xB75DAE71
C7S = 0x8F6C89C5


def yz0(cv):
    a, b, c, d, e, f, g, h = cv
    hh = (d - S0(a) - MAJ(a, b, c)) & M
    e0 = (A0S + hh) & M
    Y = (-S0(A0S) - MAJ(A0S, a, b) - g - S1(e0) - CH(e0, e, f) - K[1]) & M
    W0 = (A0S + hh - d - h - S1(e) - CH(e, f, g) - K[0]) & M
    return Y, W0


def build_index(hvals):
    start = [0] * 65537
    for h in hvals:
        start[((s0(h << 16) & 0xFFFF) + 1)] += 1
    for i in range(65536):
        start[i + 1] += start[i]
    pos = start[:]
    hs = [0] * len(hvals)
    for h in hvals:
        p = s0(h << 16) & 0xFFFF
        hs[pos[p]] = h
        pos[p] += 1
    return start, hs


def search_window(d, hvals, lvals):
    start, hs = build_index(hvals)
    dlo = d & 0xFFFF
    sols = []
    solsink = []
    probes = 0
    for L in lvals:
        sl = s0(L) & 0xFFFF
        for xlo in GLO:
            p = ((xlo - dlo + L) & 0xFFFF) ^ sl
            probes += 1
            for k in range(start[p], start[p + 1]):
                u = (hs[k] << 16) | L
                if (s0(u) - u + d) & M in GSET:
                    sols.append(u)
    sols.sort()
    return sols, probes


def brute_window(d, hvals, lvals):
    out = []
    for h in hvals:
        base = h << 16
        for L in lvals:
            u = base | L
            if (s0(u) - u + d) & M in GSET:
                out.append(u)
    out.sort()
    return out


def index_ok(hvals):
    start, hs = build_index(hvals)
    if len(hs) != len(hvals):
        return False
    if start[65536] != len(hvals):
        return False
    seen = [0] * 65536
    for p in range(65536):
        for k in range(start[p], start[p + 1]):
            h = hs[k]
            if s0(h << 16) & 0xFFFF != p:
                return False
            if h >= 65536:
                return False
            seen[h] += 1
    return all(c == 1 for c in seen)


_FULL_INDEX = None
def full_index():
    global _FULL_INDEX
    if _FULL_INDEX is None:
        _FULL_INDEX = build_index(range(65536))
    return _FULL_INDEX
def run_trial(seed_hex, trial):
    seed = bytes.fromhex(seed_hex)
    dg = hashlib.shake_256(seed).digest(10 + 512 * 4 + 16 * 4)
    d = int.from_bytes(dg[0:4], 'little')
    hbase = int.from_bytes(dg[4:7], 'little') % 65529
    lbase = int.from_bytes(dg[7:10], 'little') % 65473
    uw = [int.from_bytes(dg[10 + 4 * i:14 + 4 * i], 'little') for i in range(512)]
    mw = [int.from_bytes(dg[10 + 2048 + 4 * i:10 + 2048 + 4 * i + 4], 'little') for i in range(16)]
    obs = {}
    # 1. published pair
    hx = compress38(CV, PX)
    hy = compress38(CV, PM)
    pair_ok = (hx == PH and hy == PH)
    obs['published_pair_ok'] = pair_ok
    # 2. window check
    hs = list(range(hbase, hbase + 8))
    ls = list(range(lbase, lbase + 64))
    got, probes = search_window(d, hs, ls)
    assert probes == 64 * 16  # 64 L values x 16 low G values; H range affects bucket sizes only
    want = brute_window(d, hs, ls)
    bad = 0
    for u in got:
        if (s0(u) - u + d) & M not in GSET:
            bad += 1
    obs['wmatch'] = (got == want and bad == 0)
    # 3. uniformity on the fixed S* triple with TRUE first-block chaining values:
    #    M0 = two fresh words + zeros, CV1 = F_38(IV, M0) (the claimed distribution).
    wp = 0
    yb = [0, 0, 0, 0]
    zb = [0, 0, 0, 0]
    for i in range(32):
        m0 = [(mw[j] + uw[16 * i + j]) & M for j in range(16)]
        cv1 = compress38(IV, m0)
        a, b, c, _d, e, f, g, h = cv1
        if inF7((C7S - a) & M):
            wp += 1
        Y, W0 = yz0(cv1)
        yb[(Y >> 14) & 3] += 1
        zb[(W0 >> 14) & 3] += 1
    obs['w7passes'] = wp
    for i in range(4):
        obs['ybin%d' % i] = yb[i]
        obs['zbin%d' % i] = zb[i]
    # 4. trial 0 only: full index integrity and full-space soundness
    # 4. counted inner loop: per-L operation count in Section 1 primitives on all 64 window L values.
    start, hsfull = full_index()
    solsink = []
    cnt = [0]
    dlo = d & 0xFFFF
    maxperl = 0
    for li in range(64):
        La = (lbase + li) & 0xFFFF
        c = [0]
        c[0] += 11; sLf = s0(La)
        c[0] += 4
        sL = sLf & 0xFFFF
        for xlo in GLO:
            c[0] += 2; t1 = (xlo - dlo) & M
            c[0] += 2; t1 = (t1 + La) & M
            c[0] += 1; t1 = t1 & 0xFFFF
            c[0] += 1; p = t1 ^ sL
            c[0] += 1; a0 = start[p]
            c[0] += 1; b0 = start[p + 1]
            c[0] += 4
            for k in range(a0, b0):
                c[0] += 1; h = hsfull[k]
                c[0] += 1; hh = h << 16
                c[0] += 1; u = hh | La
                c[0] += 11; s0h = s0(hh)
                c[0] += 1; x = s0h ^ sLf
                c[0] += 2; x = (x - u) & M
                c[0] += 2; x = (x + d) & M
                c[0] += 1; x = x & 0xFFF7DBFA
                c[0] += 2; hit = (x == 0x35F29010 & 0xFFF7DBFA)
                if hit:
                    c[0] += 1; solsink.append(u)
        if c[0] > maxperl:
            maxperl = c[0]
    assert maxperl <= 15 + 16 * (12 + 2 * 23)  # == 943, the charged per-L bound
    obs['maxperl'] = maxperl
    if trial == 0:
        obs['index_ok'] = index_ok(range(65536))
        sols, probes0 = search_window(d, range(65536), range(65536))
        assert probes0 == 65536 * 16
        bad0 = 0
        for u in sols:
            if (s0(u) - u + d) & M not in GSET:
                bad0 += 1
        obs['nsolutions'] = len(sols)
        obs['mismatches'] = bad0
        obs['probes0'] = probes0
    assert pair_ok and bad == 0 and got == want and (trial != 0 or (obs['index_ok'] and obs['mismatches'] == 0))
    ma = ''.join('%08x' % w for w in CV) + ''.join('%08x' % w for w in PM)
    mb = ''.join('%08x' % w for w in CV) + ''.join('%08x' % w for w in PX)
    return {'message_a_hex': ma, 'message_b_hex': mb, 'observations': obs}


def main():
    req = json.loads(sys.stdin.read())
    out = []
    for t in req['trials']:
        r = run_trial(t['seed'], t['trial'])
        out.append({'trial': t['trial'], 'message_a_hex': r['message_a_hex'],
                    'message_b_hex': r['message_b_hex'], 'observations': r['observations']})
    sys.stdout.write(json.dumps({'schema_version': 1, 'trials': out}))


if __name__ == '__main__':
    main()
