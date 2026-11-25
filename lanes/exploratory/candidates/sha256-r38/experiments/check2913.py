"""Organizer-executed checks for the filing of O. Goldzweig's 38-step SHA-256 collision attack
(Cryptology ePrint Archive 2026/2913, "A Collision for 38-Step SHA-256").

Standard library only, deterministic, one JSON request on stdin, one JSON document on stdout.
Every trial t <= 8 runs one check and returns a pair only if the check passes:

  trial 0  the published collision M0||M1, M0||M1' (a full collision of the target), returned only
           if every value the paper states for this pair is recomputed from the pair: the chaining
           value, the core A3..A13 of both executions, the variant, lower part and upper pair, the
           modular differences of Table 6, the conditions of Table 2 and the key;
  trial 1  exact count |V7| = 2^14 (row 22), V7 a union of 512 complete aligned blocks of 32;
  trial 2  exact count: 4 values of W8 satisfy row 23;
  trial 3  exact count: 3,276,800 values of W23 satisfy row 25 for the pair's tau;
  trial 4  exact count: 637,534,208 values of W24 satisfy row 26;
  trial 5  exact count of row 17 (W15), 2^-2.752;
  trial 6  exact count of row 30 (W15), 2^-3.000;
  trial 7  exact count of the variants of the core: 1,572,864 values of E6 with dW9 = 0 and a
           solvable dW8 = -4, each with exactly one E5 pattern on F7; 16 random variants are then
           built end to end and follow the pair's differences through step 17;
  trial 8  64 random lower candidates of the published variant, random W1..W6, random W7 in V7 and
           W0 chosen so that the key equals the pair's key: the chaining value is solved from
           W0..W7 and both executions follow the pair's differences through step 17.

Trials 1..8 return a fixed non-colliding marker pair when they pass. Trials >= 9 return no pair.
Exact counts use the carry paths of x + d: on each path the XOR difference D = (x + d) ^ x is
fixed and some bits of x are fixed; with Y = sigma(D), sigma(x + d) - sigma(x) = Y - 2(sigma(x) & Y),
so the condition is affine in x over GF(2) and its solutions are counted by elimination.
"""
import hashlib
import json
import sys

M = 0xFFFFFFFF
K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
     0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
     0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
     0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
     0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb]
IV = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
R = 38

# Table 5 of the paper.
M0 = "33ee28ac5f8ef994c787777c079d17e11198d1beb527c8554bfeff014ab531951cf31bd2bbfc637e122da4f948e6e447d5a6b8b6ea9e7af5aac1aeabeeaceb0d"
M1 = "bd07668b833fe88e689ffe8da52259da14b9855eee5138ba88355f4806d5cf5d161c50014c6b7d7e0e7eb888747559fc990a7af69dd8e59f57d7f6a3c0fbd03b"
M1P = "bd07668b833fe88e689ffe8da52259da14b9855eee5138ba88355f4838b3d19d161c4ffd4c6b7d7e0e813888747559fc990a7af69dd8e59f57d7f6a3c0fbd03f"
H_PAPER = [0xd00b8f69, 0x1466ed03, 0x49c1a713, 0x7c64bf45, 0xbd8254a1, 0xc00b0cc6, 0xa1382798, 0x5f21292d]
HASH_PAPER = [0x9f5936ca, 0x5239e115, 0xc1db7dd9, 0x11f2d688, 0x10171e5f, 0xe37fa366, 0x79b07ba4, 0x2ba4433c]
DIGEST_PAPER = "5b61bad37673bb3323d64bc4fad45b44a7e6bf048d787d6127ec259b12d0d63f"
# The core: A3..A13 of the first and of the second execution (recovered from the pair; checked in trial 0).
CORE = ([0x3baa4a73, 0xef43ece6, 0xac72c958, 0xb1b7ffd2, 0x3d429e3b, 0x93dbdd23, 0x88f2acf8, 0x959ea855,
         0x9871db5e, 0x6a30e20f, 0xdad82f20],
        [0x3baa4a73, 0xef43ece6, 0xac72c958, 0xb1b7ffd2, 0x6f20a07b, 0xe33142fb, 0x2aa7318e, 0xd935a3b4,
         0x9991eb9f, 0x63b1f047, 0xd2793d21])
CW, CD, CA = 0x31de0240, 0x00028000, 0xf8010000          # w, d, a (Section 3.1)
PUB = dict(A2=0x42747b1a, E6=0x99ccff09, A0=0x248e4477, A1=0x166a78d5, E4=0xcd0d33ea, E5=0x8426bd20,
           A14=0x5bde5962, A15=0x9b3a6d8a, TAU=0x6002033f, KEY=0x00b50618)
# Table 6: t -> (dA_t, dE_t, dW_t); all other steps 0..37 have no difference.
TABLE6 = {7: (0x31de0240, 0x31de0240, 0x31de0240), 8: (0x4f5565d8, 0x39f440a0, 0xfffffffc),
          9: (0xa1b48496, 0xa8dcc1ef, 0), 10: (0x4396fb5f, 0x6774e337, 0x00028000),
          11: (0x01201041, 0x39a879c6, 0), 12: (0xf9810e38, 0x06627ff8, 0), 13: (0xf7a10e01, 0xc43d71fb, 0),
          14: (0, 0xfffdf000, 0), 15: (0xf8010000, 0x00000200, 0x00000004), 16: (0x00000004, 0xffdffe24, 0),
          17: (0, 0xf77ffe00, 0), 19: (0, 0xf8010000, 0), 20: (0, 0x00000004, 0), 23: (0, 0, 0x07ff0000),
          24: (0, 0, 0xfffffffc)}


def rotr(x, n):
    return ((x >> n) | (x << (32 - n))) & M


def S0(x):
    return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22)


def S1(x):
    return rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25)


def s0(x):
    return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)


def s1(x):
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)


def ch(x, y, z):
    return (x & y) ^ (~x & z & M)


def maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)


def words(hexstr):
    return [int(hexstr[8 * i:8 * i + 8], 16) for i in range(len(hexstr) // 8)]


def expand(w):
    w = list(w)
    for t in range(16, R):
        w.append((s1(w[t - 2]) + w[t - 7] + s0(w[t - 15]) + w[t - 16]) & M)
    return w


def trace(cv, w16):
    """Equations (2), (3) of the paper: returns A, E (dicts over t = -4..R-1), the expanded words, F_R(cv, M)."""
    w = expand(w16)
    A = {-1: cv[0], -2: cv[1], -3: cv[2], -4: cv[3]}
    E = {-1: cv[4], -2: cv[5], -3: cv[6], -4: cv[7]}
    for t in range(R):
        E[t] = (A[t - 4] + E[t - 4] + S1(E[t - 1]) + ch(E[t - 1], E[t - 2], E[t - 3]) + K[t] + w[t]) & M
        A[t] = (E[t] - A[t - 4] + S0(A[t - 1]) + maj(A[t - 1], A[t - 2], A[t - 3])) & M
    out = [(A[R - 1 - i] + cv[i]) & M for i in range(4)] + [(E[R - 1 - i] + cv[4 + i]) & M for i in range(4)]
    return A, E, w, out


def digest(msg):
    data = msg + b"\x80" + b"\x00" * ((55 - len(msg)) % 64) + (8 * len(msg)).to_bytes(8, "big")
    cv = IV
    for off in range(0, len(data), 64):
        cv = trace(cv, words(data[off:off + 64].hex()))[3]
    return "".join("%08x" % x for x in cv)


def E_of(A, t):        # equation (4)
    return (A[t] + A[t - 4] - S0(A[t - 1]) - maj(A[t - 1], A[t - 2], A[t - 3])) & M


def W_of(A, E, t):     # equation (5)
    return (E[t] - A[t - 4] - E[t - 4] - S1(E[t - 1]) - ch(E[t - 1], E[t - 2], E[t - 3]) - K[t]) & M


def block_from_states(H, A_lo, side, A14, A15):
    """W0..W15 from the chaining value H and A0..A15 (A0..A2 given, A3..A13 from the core side)."""
    A = {-1: H[0], -2: H[1], -3: H[2], -4: H[3], 0: A_lo[0], 1: A_lo[1], 2: A_lo[2], 14: A14, 15: A15}
    E = {-1: H[4], -2: H[5], -3: H[6], -4: H[7]}
    for i, v in enumerate(CORE[side]):
        A[3 + i] = v
    for t in range(16):
        E[t] = E_of(A, t)
    return [W_of(A, E, t) for t in range(16)]


def solve_cv(A_lo, target):
    """The chaining value H with W0..W7 = target (Section 2.1: W_{7-i} = kappa_i(H0..H_{i-1}) - H_i)."""
    H = [0] * 8
    for i in range(8):
        H[i] = 0
        H[i] = (block_from_states(H, A_lo, 0, 0, 0)[7 - i] - target[7 - i]) & M
    return H


def core_E(side, t):
    A = {3 + i: v for i, v in enumerate(CORE[side])}
    return E_of(A, t)


# ---------------------------------------------------------------- exact counting over GF(2)
def sigma_rows(sig):
    rows = [0] * 32
    for j in range(32):
        y = sig(1 << j)
        for i in range(32):
            if y >> i & 1:
                rows[i] |= 1 << j
    return rows


def reduce_system(eqs):
    """Reduced echelon form of parity equations (mask, value) over the 32 bits of x; None if inconsistent."""
    rows = {}
    for m, v in eqs:
        for p, (bm, bv) in rows.items():
            if m >> p & 1:
                m ^= bm
                v ^= bv
        if m == 0:
            if v:
                return None
            continue
        p = m.bit_length() - 1
        for q in list(rows):
            bm, bv = rows[q]
            if bm >> p & 1:
                rows[q] = (bm ^ m, bv ^ v)
        rows[p] = (m, v)
    return rows


def solutions(rows):
    free = [b for b in range(32) if b not in rows]
    out = []
    for a in range(1 << len(free)):
        x = 0
        for k, b in enumerate(free):
            if a >> k & 1:
                x |= 1 << b
        for p, (m, v) in rows.items():
            if (bin(x & m).count("1") & 1) ^ v:
                x |= 1 << p
        out.append(x)
    return out


def count_diff(sig, d, T, collect=False):
    """Number of x mod 2^32 with sig(x + d) - sig(x) = T (mod 2^32), and optionally the solutions."""
    rows_sig = sigma_rows(sig)
    total, found = 0, []
    stack = [(0, 0, 0, 0, 0)]                 # bit, carry into it, D so far, fixed-bit mask, fixed values
    while stack:
        i, c, D, fm, fv = stack.pop()
        while i < 32 and (d >> i & 1) == c:   # D_i = 0 and the carry is forced
            i += 1
        if i < 32:                            # D_i = 1 and the carry out equals x_i
            for xi in (0, 1):
                stack.append((i + 1, xi, D | (1 << i), fm | (1 << i), fv | (xi << i)))
            continue
        Y = sig(D)
        Z = (Y - T) & M
        if Z & 1:
            continue
        Z >>= 1                               # need (sig(x) & Y) = Z on bits 0..30
        if Z & ~Y & 0x7FFFFFFF:
            continue
        eqs = [(rows_sig[k], Z >> k & 1) for k in range(31) if Y >> k & 1]
        eqs += [(1 << k, fv >> k & 1) for k in range(32) if fm >> k & 1]
        rows = reduce_system(eqs)
        if rows is None:
            continue
        total += 1 << (32 - len(rows))
        if collect:
            found += solutions(rows)
    return total, sorted(found)


def delta(f, x, dx):
    return (f((x + dx) & M) - f(x)) & M


# ---------------------------------------------------------------- the published pair
def pair_states():
    m0, m1, m1p = words(M0), words(M1), words(M1P)
    H = trace(IV, m0)[3]
    a1, e1, w1, o1 = trace(H, m1)
    a2, e2, w2, o2 = trace(H, m1p)
    return H, (a1, e1, w1, o1), (a2, e2, w2, o2)


def check_pair():
    H, (a1, e1, w1, o1), (a2, e2, w2, o2) = pair_states()
    ok = H == H_PAPER and o1 == o2 == HASH_PAPER and M1 != M1P
    ok &= digest(bytes.fromhex(M0 + M1)) == digest(bytes.fromhex(M0 + M1P)) == DIGEST_PAPER
    ok &= [a1[t] for t in range(3, 14)] == CORE[0] and [a2[t] for t in range(3, 14)] == CORE[1]
    ok &= (a1[2], e1[6], a1[0], a1[1], e1[4], e1[5], a1[14], a1[15]) == tuple(
        PUB[k] for k in ("A2", "E6", "A0", "A1", "E4", "E5", "A14", "A15"))
    for t in range(R):
        got = ((a2[t] - a1[t]) & M, (e2[t] - e1[t]) & M, (w2[t] - w1[t]) & M)
        ok &= got == TABLE6.get(t, (0, 0, 0))
    ok &= bin(e1[7] ^ e2[7]).count("1") == 13                                  # |F7| = 13
    ok &= (w2[7] - w1[7]) & M == CW and (w2[10] - w1[10]) & M == CD and (a2[15] - a1[15]) & M == CA
    tau = (-delta(s0, w1[10], CD)) & M
    ok &= tau == PUB["TAU"]
    ok &= delta(s1, w1[15], 4) == (-CD) & M                                    # row 17
    ok &= delta(s0, w1[7], CW) == (-4) & M                                     # row 22
    ok &= delta(s0, w1[8], -4 & M) == (-CA - CW) & M                           # row 23
    ok &= (delta(s1, w1[23], -CA & M) + delta(s0, w1[10], CD)) & M == 0         # row 25
    ok &= (delta(s1, w1[24], -4 & M) + CD) & M == 0                            # row 26
    ok &= delta(s0, w1[15], 4) == CA                                           # row 30
    key = (w1[9] + s0(w1[1]) + w1[0]) & M                                      # C16, Section 4.3
    ok &= key == PUB["KEY"] and key == (w1[16] - s1(w1[14])) & M
    return ok


# ---------------------------------------------------------------- randomness from the organizer seed
class Stream:
    def __init__(self, seed_hex, label):
        self.buf = hashlib.shake_256((label + ":" + seed_hex).encode()).digest(1 << 16)
        self.pos = 0

    def word(self):
        v = int.from_bytes(self.buf[self.pos:self.pos + 4], "big")
        self.pos += 4
        return v


def pair_diffs_through(cv, lo, A14, A15, upto=17):
    """Both executions from cv with A0..A2 = lo, the core and the upper pair; returns (dW pattern ok,
    the list of (dA_t, dE_t) for t <= upto, consistency of the traced states with the chosen ones)."""
    wa = block_from_states(cv, lo, 0, A14, A15)
    wb = block_from_states(cv, lo, 1, A14, (A15 + CA) & M)
    dw = [(y - x) & M for x, y in zip(wa, wb)]
    want = [0] * 7 + [CW, (-4) & M, 0, CD, 0, 0, 0, 0, 4]
    ta, tb = trace(cv, wa), trace(cv, wb)
    consistent = all(ta[0][t] == v for t, v in enumerate(list(lo) + CORE[0] + [A14, A15]))
    diffs = [((tb[0][t] - ta[0][t]) & M, (tb[1][t] - ta[1][t]) & M) for t in range(upto + 1)]
    return dw == want, diffs, consistent, wa


def published_diffs(upto=17):
    _, (a1, e1, _, _), (a2, e2, _, _) = pair_states()
    return [((a2[t] - a1[t]) & M, (e2[t] - e1[t]) & M) for t in range(upto + 1)]


def lower_part(A2, E6, E5, W8):
    """A1 and A0 from E5 and W8 for the variant A2 (Section 4.2)."""
    A = {3 + i: v for i, v in enumerate(CORE[0])}
    A[2] = A2
    A1 = (E5 - A[5] + S0(A[4]) + maj(A[4], A[3], A2)) & M
    E7, E8 = core_E(0, 7), core_E(0, 8)
    E4 = (E8 - A[4] - S1(E7) - ch(E7, E6, E5) - K[8] - W8) & M
    A0 = (E4 - A[4] + S0(A[3]) + maj(A[3], A2, A1)) & M
    return A0, A1


def variant_A2(E6):
    A = {3 + i: v for i, v in enumerate(CORE[0])}
    return (E6 - A[6] + S0(A[5]) + maj(A[5], A[4], A[3])) & M


def lower_candidate_pair(st, A2, E6, E5F, F7, W8vals, V7list):
    """A random lower candidate of the variant, random W1..W6, random W7 in V7, W0 set by the key."""
    E5 = (E5F & F7) | (st.word() & ~F7 & M)
    W8 = W8vals[st.word() % 4]
    A0, A1 = lower_part(A2, E6, E5, W8)
    lo = (A0, A1, A2)
    w = [0] + [st.word() for _ in range(6)] + [V7list[st.word() % len(V7list)]]
    W9 = block_from_states([0] * 8, lo, 0, 0, 0)[9]                          # W9 does not depend on H
    w[0] = (PUB["KEY"] - W9 - s0(w[1])) & M
    H = solve_cv(lo, w)
    theta = block_from_states([0] + H[1:], lo, 0, 0, 0)[7]                    # W7 + H0, Section 2.1
    ok_dw, diffs, consistent, wa = pair_diffs_through(H, lo, PUB["A14"], PUB["A15"])
    ok = ok_dw and consistent and wa[:8] == w and wa[8] == W8 and theta == (w[7] + H[0]) & M
    return ok, diffs


def variants_check(st, W8vals, V7list):
    E7a, E7b, E8a, E8b, E9a, E9b = (core_E(s, t) for t in (7, 8, 9) for s in (0, 1))
    F7, F8 = E7a ^ E7b, E8a ^ E8b                       # dW8 depends on E6 only on F7, dW9 only on F8
    O = F7 & F8
    dE9, dE8 = (E9b - E9a) & M, (E8b - E8a) & M
    dS1E8, dS1E7 = (S1(E8b) - S1(E8a)) & M, (S1(E7b) - S1(E7a)) & M

    def patterns(mask):
        b = [i for i in range(32) if mask >> i & 1]
        for a in range(1 << len(b)):
            yield sum(1 << b[k] for k in range(len(b)) if a >> k & 1)

    ok9 = [e for e in patterns(F8) if (dE9 - dS1E8 - (ch(E8b, E7b, e) - ch(E8a, E7a, e))) & M == 0]
    T8 = (dE8 - dS1E7 + 4) & M                          # dW8 = -4  <=>  ch(E7',E6,E5) - ch(E7,E6,E5) = T8
    Fp, Fn = F7 & E7a, F7 & ~E7a & M
    small, large, sign = (Fn, Fp, 1) if bin(Fn).count("1") <= bin(Fp).count("1") else (Fp, Fn, -1)
    sol8, hist = {}, {}
    for e in patterns(F7):
        R_ = (T8 + (e & Fp) - (e & Fn)) & M             # need (E5 & Fp) - (E5 & Fn) = R_
        sols = []
        for q in patterns(small):
            p = (R_ + q) & M if sign == 1 else (q - R_) & M
            if p & ~large & M == 0:
                sols.append(p | q)
        if sols:
            sol8[e] = sols
            hist[len(sols)] = hist.get(len(sols), 0) + 1
    by9 = {}
    for e in ok9:
        by9.setdefault(e & O, []).append(e)
    pairs = sum(len(by9.get(e & O, [])) for e in sol8)  # E6 patterns on F7 | F8 meeting both conditions
    count = pairs << (32 - bin(F7 | F8).count("1"))
    ok = count == 1572864 and set(hist) == {1}
    pubE6, pubE5 = PUB["E6"], PUB["E5"]
    ok &= (pubE6 & F8) in ok9 and sol8.get(pubE6 & F7) == [pubE5 & F7]
    ok &= variant_A2(pubE6) == PUB["A2"]
    pub = published_diffs()
    eight = sorted(e for e in sol8 if (e & O) in by9)
    for _ in range(16):
        e7 = eight[st.word() % len(eight)]
        cands = by9[e7 & O]
        e8 = cands[st.word() % len(cands)]
        E6 = (st.word() & ~(F7 | F8) & M) | e7 | e8
        good, diffs = lower_candidate_pair(st, variant_A2(E6), E6, sol8[e7][0], F7, W8vals, V7list)
        ok &= good and diffs == pub
    return ok


def run_check(t, seed):
    if t == 0:
        return check_pair()
    if t in (1, 2, 7, 8):
        if "V7" not in CACHE:
            CACHE["V7"] = count_diff(s0, CW, (-4) & M, collect=True)
            CACHE["W8"] = count_diff(s0, (-4) & M, (-CA - CW) & M, collect=True)
        n7, V7 = CACHE["V7"]
        n23, W8vals = CACHE["W8"]
        blocks = set(x >> 5 for x in V7)
        v7ok = n7 == 16384 and len(set(V7)) == 16384 and len(blocks) == 512    # 512 blocks of 32 values
        if t == 1:
            return v7ok and words(M1)[7] in set(V7)
        if t == 2:
            return n23 == 4 and len(W8vals) == 4 and words(M1)[8] in W8vals
        st = Stream(seed, "check2913-%d" % t)
        if t == 7:
            return v7ok and n23 == 4 and variants_check(st, W8vals, V7)
        F7 = core_E(0, 7) ^ core_E(1, 7)
        pub = published_diffs()
        ok = v7ok and n23 == 4
        for _ in range(64):
            good, diffs = lower_candidate_pair(st, PUB["A2"], PUB["E6"], PUB["E5"], F7, W8vals, V7)
            ok &= good and diffs == pub
        return ok
    if t == 3:
        return count_diff(s1, (-CA) & M, PUB["TAU"])[0] == 3276800
    if t == 4:
        return count_diff(s1, (-4) & M, (-CD) & M)[0] == 637534208
    if t == 5:
        return count_diff(s1, 4, (-CD) & M)[0] == ROW17
    if t == 6:
        return count_diff(s0, 4, CA)[0] == ROW30
    return False


CACHE = {}
ROW17 = 637534208   # 2^-2.752
ROW30 = 536870912   # 2^-3


def main():
    req = json.loads(sys.stdin.read())
    out = []
    for row in req["trials"]:
        t = row["trial"]
        pair = (None, None)
        if t <= 8 and run_check(t, row["seed"]):
            if t == 0:
                pair = (M0 + M1, M0 + M1P)
            else:
                marker = ("ePrint 2026/2913 check %d passed" % t).encode().hex()
                pair = (marker, marker + "00")
        out.append({"trial": t, "message_a_hex": pair[0], "message_b_hex": pair[1]})
    sys.stdout.write(json.dumps({"schema_version": 1, "trials": out}, sort_keys=True))


if __name__ == "__main__":
    main()
