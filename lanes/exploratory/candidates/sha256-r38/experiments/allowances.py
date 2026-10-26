"""r38-allowances-check (H4a/H4b/H4c; proof.md Appendix C): the arithmetic behind A_C = 2^78, A_S = 2^74, DEV = 2^70
on the figures quoted verbatim from 51613d1c's proof.md (Section 11, R.2-R.4) and on our own development envelope; and
the 38-step pair 51613d1c quotes in R.2 Part B (output of a 2,852.83 CPU-s pair search) recomputed against its quoted
digest. Arithmetic and consistency only; run times are quoted, not measured. Trial 0 asserts; no message pair."""
import sys, json, math
M = 0xffffffff
def icbrt(n):
    x = 1 << ((n.bit_length() + 2) // 3)
    while True:
        y = (2 * x + n // (x * x)) // 3
        if y >= x: return x
        x = y
P = [p for p in range(2, 200) if all(p % d for d in range(2, p))][:38]
K = [icbrt(p << 96) & M for p in P]
def ror(x, n): return ((x >> n) | (x << (32 - n))) & M
def c38(cv, w):
    w = list(w)
    for i in range(16, 38): w.append((ror(w[i-2], 17) ^ ror(w[i-2], 19) ^ (w[i-2] >> 10)) + w[i-7] + (ror(w[i-15], 7) ^ ror(w[i-15], 18) ^ (w[i-15] >> 3)) + w[i-16] & M)
    a, b, c, d, e, f, g, h = cv
    for i in range(38):
        t1 = h + (ror(e, 6) ^ ror(e, 11) ^ ror(e, 25)) + ((e & f) ^ (~e & g)) + K[i] + w[i] & M
        t2 = (ror(a, 2) ^ ror(a, 13) ^ ror(a, 22)) + ((a & b) ^ (a & c) ^ (b & c)) & M
        a, b, c, d, e, f, g, h = t1 + t2 & M, a, b, c, d + t1 & M, e, f, g
    return [x + y & M for x, y in zip(cv, (a, b, c, d, e, f, g, h))]
H = lambda s: [int(x, 16) for x in s.split()]
CV = H('43058709 adfdbff7 b7e63568 b4e09527 3ef1b89a 18f03df1 7fd9bbaa 7f392ba4')
MX = H('33f3fd01 ab09628d 9971c77a 2f0148d3 442fd7d8 9acaf5c3 2fd3a6f8 a8740b40 c91bb8b5 9e019239 04039fa1 0ce30b8d a18c515a 76a1e994 d28e48a0 9b5f6dbb')
MY = H('33f3fd01 ab09628d 9971c77a 2f0148d3 442fd7d8 9acaf5c3 2fd3a6f8 88740b40 cd5bb0b5 be019239 01028d0b 0ceb1f8d a18c515a 76a1e994 d28e48a0 9f1f65bb')
DG = H('614d0b44 0d272005 713bab9e 4fc8e2a1 126b7229 bbb45050 0d592f10 cf2f96a9')
L2 = math.log2; U = L2(64 / 38); RATE = 3797484   # 64-step SHA-256 = 64/38 units; slowest measured rate (R.2 Part A)
def check():
    assert K[0] == 0x428a2f98 and K[37] == 0x766a0abb
    hx, hy = c38(CV, MX), c38(CV, MY); diff = [i for i in range(16) if MX[i] != MY[i]]
    assert hx == hy == DG and diff == [7, 8, 9, 10, 11, 15]
    ac = 21 + L2(RATE) + U                           # 1a695f0b: under 2^21 core-seconds (R.4 L307; R.2) -> units
    lo, hi = 12 * 8 + 11 * 2514 + 15 * 10800, 12 * 22 + 11 * 9890 + 15 * 10800   # 38 runs: 12 UNSAT 8-22 s, 11 SAT 2,514-9,890 s, 15 TIMEOUT
    assert abs(ac - 43.61) < 0.005 and lo <= 230183 <= hi and 230183 < 2 ** 21 and abs(L2(230183) - 17.81) < 0.005
    rows = [(37.00 + U, 37.75), (38.40 + U, 39.15), (L2(3120 * RATE) + U, 34.22), (L2(11071.7 * RATE) + U, 36.04), (L2(2852.83 * RATE) + U, 34.09)]
    assert all(abs(a - b) < 0.006 for a, b in rows)
    mx = max(b for _, b in rows); dl = L2(68 * 1.4688e6 * 2 ** 40 + 1.4688e6 * 2 ** 47); dlc = dl - L2(2728)
    assert dl < 68.11 and dlc < 56.7                 # 51613d1c H4c: "< 2^68.11 operations = 2^56.7 compressions"
    do = L2(16 * 4838400 * 2 ** 40 + 4838400 * 2 ** 47) - L2(2728)   # own envelope: 16 threads + 1 GPU, 2026-09-01T00Z..10-27T00Z
    dev = L2(2 ** dlc + 2 ** do); pre = L2(2 ** 78 + 2 ** 74 + 2 ** 70)
    assert ac < 74 < 78 and mx < 78 - 38.8 and dev < 70 - 11 and abs(pre - 78.092757) < 1e-6 and pre <= 78.09276
    return dict(pair_collides=1, digest_matches=1, ac_units_log2=round(ac, 4), ac_margin_bits=round(78 - ac, 4), as_margin_bits=round(74 - ac, 4),
                runs_lo=lo, runs_hi=hi, runs_listed=230183, max_published_units_log2=mx, dev_leader_log2=round(dlc, 4),
                dev_own_log2=round(do, 4), dev_margin_bits=round(70 - dev, 4), preprocessing_log2=round(pre, 6), asserted=1)
def serve():
    req = json.load(sys.stdin); rows = []
    for t in req['trials']:
        row = {'trial': t['trial'], 'message_a_hex': None, 'message_b_hex': None}
        if t['trial'] == 0: row['observations'] = check()
        rows.append(row)
    sys.stdout.write(json.dumps({'schema_version': 1, 'trials': rows}, sort_keys=True, separators=(',', ':')) + '\n')
if __name__ == '__main__':
    serve()
