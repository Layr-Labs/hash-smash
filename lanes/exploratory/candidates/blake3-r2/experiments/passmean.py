"""Exact mean of the pass units X of one outer step under the model of proof.md 9.4 (rational arithmetic, no sampling)."""
import json
import sys
from fractions import Fraction as Q
from functools import cache
M = 0xFFFFFFFF
def ror(v, n):
    return (v >> n | v << 32 - n) & M
def g(a, b, c, d, x, y):
    a = a + b + x & M; d = ror(d ^ a, 16); c = c + d & M; b = ror(b ^ c, 12)
    return a + b + y & M
IV2, IV6, X3, X7, X11, X15, W4, W13 = 0x3C6EF372, 0x1F83D9AB, 0x29D4FA98, 0xBEE3AF28, 0x44036000, 0x40C58500, 0x97475638, 0x7C006
K = IV2 + IV6 & M
Y3, Y3B = g(X3, X7, X11, X15, W4, W13), g(X3, X7, X11, X15, ((W4 + K & M) ^ 55 ^ 63) - K & M, W13)
DY3, ETA, EPS = Y3B - Y3 & M, 0x830303CF, 0x6E21BE55
CLS = ror(ETA, 16) & 0x7FFFFFFF
CLV = ~((Y3B - Y3 + ror(ETA, 16) & M) >> 1) & CLS
TAUS = (0x175020A0, 0x175060A0, 0x185020A0, 0x185060A0, 0x275020A0, 0x275060A0, 0x285020A0, 0x285060A0,
        0x385020A0, 0x385060A0, 0x675020A0, 0x675060A0, 0x685020A0, 0x685060A0)
N3 = (384, 24, 256, 32, 64, 4, 384, 48, 512, 64, 16, 1, 96, 12)  # N3_j / 2^48 (Section 17 run on the class)
UNITS = dict(calls=1342, roots=5, pops=13, internal=36, pushes=11, leaves=49, goods=128)  # a call: 546 + 4 * 199
def tb(k, s, x):
    s1, s2 = (k & 1) + x + (s & 1), (k >> 1 & 1) + (x ^ k >> 2 & 1) + (s >> 1)
    return 4 if (s1 ^ s2) & 1 != k >> 3 & 1 else s1 >> 1 | (s2 >> 1) << 1
def ta(k, s, x):
    gb = x ^ k & 1
    d = gb - (k >> 1 & 1) - (s & 1)
    sm = (k >> 1 & 1) + ((d & 1) ^ k >> 2 & 1) + (s >> 1)
    return 4 if sm & 1 != gb ^ k >> 3 & 1 else int(d < 0) | (sm >> 1) << 1
def step(kb, ka, sb, sa, x, k):
    nb, na = tb(kb, sb, x), ta(ka, sa, x)
    na = 0 if k == 19 and na < 4 else na
    return None if nb == 4 or na == 4 else (nb, na)
@cache
def jt(kb, ka, j16, k):
    return sum(1 << b * 4 + a for b in range(4) for a in range(4)
               if any((n := step(kb, ka, b, a, x, k)) and j16 >> n[0] * 4 + n[1] & 1 for x in (0, 1)))
@cache
def level(j, k, c, be):
    i, t = (k + 12) % 32, TAUS[j]
    ps, th = t ^ ror(t, 1), ror(t ^ ror(t, 1), 20)
    fixed = CLS >> i & 1
    out = []
    for om in (0, 1):
        for y9 in (0, 1):
            for e1 in ((CLV >> i & 1,) if fixed else (0, 1)):
                dy, y3 = DY3 >> k & 1, Y3 >> i & 1
                kb = om | (om ^ dy ^ c) << 1 | (ps >> k & 1) << 2 | (EPS >> k & 1) << 3
                ka = e1 ^ y3 ^ be | y9 << 1 | (ETA >> i & 1) << 2 | (th >> i & 1) << 3
                out.append((Q(1, 4 if fixed else 8), kb, ka, om + dy + c >> 1, int(e1 - y3 - be < 0)))
    return tuple(out)
def nodes(j, s):
    "E[nodes] at levels 0..32 for outcome j, guess s (summed over the borrow b into bit 12)."
    tot = [Q(0)] * 33
    for b in (0, 1):
        D = {}
        for k in range(31, -1, -1):
            for c in (0, 1):
                for be in (0, 1):
                    acc = {}
                    for p, kb, ka, c2, b2 in level(j, k, c, be):
                        nxt = ({sum(1 << q * 4 + s for q in range(4)) if b2 == b else 0: 1} if k == 31
                               else D[k + 1, c2, 0 if k == 19 else b2])
                        for J, q in nxt.items():
                            J0 = jt(kb, ka, J, k)
                            acc[J0] = acc.get(J0, 0) + p * q
                    D[k, c, be] = acc
        F = {(0, s, 0, b): Q(1)}
        for k in range(33):
            if k == 32:
                tot[32] += sum(n for (sb, sa, c, be), n in F.items() if sa == s and be == b)
                break
            G = {}
            for (sb, sa, c, be), n in F.items():
                tot[k] += n * sum(q for J, q in D[k, c, be].items() if J >> sb * 4 + sa & 1)
                for p, kb, ka, c2, b2 in level(j, k, c, be):
                    for x in (0, 1):
                        r = step(kb, ka, sb, sa, x, k)
                        if r:
                            key = r + (c2, 0 if k == 19 else b2)
                            G[key] = G.get(key, 0) + n * p
            F = G
    return tot
def masks(targets, dy):
    "Words x per mask {j: some v has (x + v) ^ ((x + dy) + (v ^ dz_j)) = out_j}."
    S = {(0, (1,) * len(targets)): 1}
    for i in range(32):
        e, T = dy >> i & 1, {}
        for (k, sets), n in S.items():
            for a in (0, 1):
                b, new = a ^ e ^ k, []
                for m, (dz, out) in zip(sets, targets):
                    r = 0
                    for c in range(4):
                        for v in (0, 1):
                            s1, s2 = a + v + (c >> 1), b + (v ^ dz >> i & 1) + (c & 1)
                            r |= (m >> c & (s1 ^ s2 ^ out >> i ^ 1) & 1) << (s1 >> 1) * 2 + (s2 >> 1)
                    new.append(r)
                key = (a + e + k >> 1, tuple(new))
                T[key] = T.get(key, 0) + n
        S = T
    R = {}
    for (k, sets), n in S.items():
        m = sum(1 << j for j, x in enumerate(sets) if x)
        R[m] = R.get(m, 0) + n
    return R
def mean():
    G = [ror(t ^ ror(t, 1), 20) for t in TAUS]
    m1, m2 = masks([(ETA, x) for x in G], 0), masks([(ror(x, 12), EPS) for x in G], DY3)
    share = sum(a * b for x, a in m1.items() for y, b in m2.items() if x & y)
    ev = dict.fromkeys(UNITS, Q(0))
    for j in range(14):
        p = Q(sum(n for x, n in m1.items() if x >> j & 1) * sum(n for y, n in m2.items() if y >> j & 1), 1 << 64)
        ev["calls"] += p; ev["goods"] += Q(N3[j], 1 << 35)
        for s in range(4):
            n = nodes(j, s)
            ev["roots"] += n[0]; ev["pops"] += sum(n); ev["internal"] += sum(n[:32])
            ev["pushes"] += sum(n[1:]); ev["leaves"] += n[32]
    ex = Q(140 * share, 1 << 64) + sum(UNITS[e] * v for e, v in ev.items())  # dispatch 56 and ctr_rest 84
    obs = {e: float(v) for e, v in ev.items()}
    obs.update(ex=float(ex), ex_num=ex.numerator, ex_den_log2=ex.denominator.bit_length() - 1,
               share=share, share_ok=share == 99669577442459648, below_premise=ex <= Q(1369, 16))
    return obs
def main():
    request = json.load(sys.stdin)
    obs = mean()
    rows = [{"trial": t["trial"], "message_a_hex": None, "message_b_hex": None, "observations": obs}
            for t in request["trials"]]
    json.dump({"schema_version": 1, "trials": rows}, sys.stdout, separators=(",", ":"), sort_keys=True)
    sys.stdout.write("\n")
if __name__ == "__main__":
    main()
