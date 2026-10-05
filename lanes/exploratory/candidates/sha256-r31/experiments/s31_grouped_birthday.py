"""Scaled grouped partial-evaluation birthday search on sha256-r31 (proof.md Sections 3 and 6).

Stdlib only. Organizer mode (default): read one JSON request on stdin, write one JSON result.

The grouping method (shared prefix, one varying word, per-message partial evaluation, early
abort on a partial key, a never-initialised sparse-set table, two-layout experiments) is due to
solver jaazinn (sha256-r31 ticket 35ce0758, blake3-r2 ticket 0a5b7ae8), credited as co-author.

Messages are 55 bytes: prefix words W0..W12 (fresh per group) followed by the 3 bytes of y,
so the padded block has W13 = (y << 8) | 0x80, W14 = 0 and W15 = 440.

group_setup(p)        : group constants (W13-independent work), reference primitives;
                        count_setup() counts it.
key_program(G, v, tab): THE counted per-message program of proof.md Section 3.3. v = TB + W13
                        with TB a multiple of 2^32 (TB carries arbitrary high bits here, to
                        exercise lazy masking). Doubled-word rotations, lazy masking, the y-only
                        table S0T[v] = sigma0(W13) read by tab() (one load). Returns
                        (a27, a28, e27, e28, e29) = digest words (H3, H2, H7, H6, H5) minus IV,
                        each reduced below 2^32.
_fast_digest(F, w13)  : NOT part of the attack; an uncounted plain-int evaluator of all eight
                        digest words, used only to keep 256 trials inside the 20 s budget.
                        attempt() compares its key with key_program on every 32nd message and
                        raises on any mismatch.

Experiments (organizer seeds; every returned pair is re-hashed by the organizer):
  s31-grouped-spread : 32 groups x 32 consecutive y, 20-bit mask over all eight digest words.
  s31-single-group   : one group, y = 0..1023, 20-bit mask over the five key words only.
Random-function success for both: 1 - prod_{i<1024}(1 - i/2^20) = 0.39327.

Observation ops_counted = key_program + 8-op key pack on the trial's first message, counted
with an int subclass that counts every +, &, |, ^, <<, >>, ~ like
scripts/reference_operation_costs.py (reflected operators too) plus one per table load.
Group constants are plain ints (registers) and are never combined with each other inside
key_program, so every per-message operation is counted (expected: 499).
"""

import hashlib
import json
import sys

M = 0xFFFFFFFF
IV = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)
K = (0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5, 0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5,
     0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3, 0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174,
     0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC, 0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
     0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7, 0xC6E00BF3, 0xD5A79147, 0x06CA6351)
MASKS = {
    "s31-grouped-spread": (0x80002001, 0x08040020, 0x00400204, 0x40010080,
                           0x01000008, 0x20000800, 0x00100002, 0x04004000),
    "s31-single-group": (0, 0, 0x10080410, 0x40801002, 0, 0x80208040, 0x02020101, 0x21002008),
}


# ---- reference-form primitives (group setup and table build only) ----------------------
def ROR(v, c):
    v = v & M
    return ((v << (32 - c)) | (v >> c)) & M


def S0(a):
    return ROR(a, 2) ^ ROR(a, 13) ^ ROR(a, 22)


def S1(e):
    return ROR(e, 6) ^ ROR(e, 11) ^ ROR(e, 25)


def s0(x):
    return ROR(x, 7) ^ ROR(x, 18) ^ (x >> 3)


def s1(x):
    return ROR(x, 17) ^ ROR(x, 19) ^ (x >> 10)


def CH(e, f, g):
    return (e & f) ^ (~e & g)


def MAJ(a, b, c):
    return (a & b) ^ (a & c) ^ (b & c)


# ---- per-message primitives (proof.md Section 3.3): input x reduced (< 2^32) -----------
def DS0(x):     # Sigma0: D = x | x<<32; low 32 bits of D>>r = rotr(x, r). 7 ops, output lazy
    d = x | (x << 32)
    return (d >> 2) ^ (d >> 13) ^ (d >> 22)


def DS1(x):     # Sigma1, 7 ops
    d = x | (x << 32)
    return (d >> 6) ^ (d >> 11) ^ (d >> 25)


def Ds1(x):     # sigma1, 7 ops
    d = x | (x << 32)
    return (d >> 17) ^ (d >> 19) ^ (x >> 10)


def group_setup(p, K=K, IV=IV):
    """Group constants from prefix words p[0..12] (proof.md Section 3.2)."""
    w = list(p)
    a, b, c, d, e, f, g, h = IV
    A, E = {}, {}
    for i in range(13):                                         # steps 0..12, reference form
        t1 = (h + S1(e) + CH(e, f, g) + K[i] + w[i]) & M
        t2 = (S0(a) + MAJ(a, b, c)) & M
        a, b, c, d, e, f, g, h = (t1 + t2) & M, a, b, c, (d + t1) & M, e, f, g
        A[i], E[i] = a, e
    t1 = h + S1(e) + CH(e, f, g) + K[13]                        # step 13 without W13
    t2 = S0(a) + MAJ(a, b, c)
    W = dict(enumerate(w))
    W[14], W[15] = 0, 440                                       # padding words
    for i in (16, 17, 18, 19, 21, 23, 25):                      # W13-independent words
        W[i] = (W[i - 16] + s0(W[i - 15]) + W[i - 7] + s1(W[i - 2])) & M
    G = {
        "U13": (t1 + t2) & M, "V13": (d + t1) & M,              # a13 = U13 + W13, e13 = V13 + W13
        "E11": E[11], "E12": E[12], "FG14": E[12] ^ E[11],
        "A12": A[12], "BC14": A[12] ^ A[11],
        "C20": (W[4] + s0(W[5]) + s1(W[18])) & M,               # W20 = C20 + W13
        "C22": (W[6] + s0(W[7]) + W[15]) & M,                   # W22 = C22 + s1(W20)
        "C24": (W[8] + s0(W[9]) + W[17]) & M,                   # W24 = C24 + s1(W22)
        "C26": (W[10] + s0(W[11]) + W[19]) & M,                 # W26 = C26 + s1(W24)
        "C27": (W[11] + s0(W[12]) + s1(W[25])) & M,             # W27 = C27 + W20
        "W23": W[23], "C28": (W[12] + W[21]) & M,               # fast path only
    }
    for i, hh, dd in ((14, E[10], A[10]), (15, E[11], A[11]), (16, E[12], A[12])):
        G["T%d" % i] = (K[i] + W[i] + hh) & M                   # t1 = X + T_i (h folded)
        G["T%dd" % i] = (K[i] + W[i] + hh + dd) & M             # e_i = X + T_id (d folded)
    for i in (17, 18, 19, 21, 23, 25):
        G["T%d" % i] = (K[i] + W[i]) & M
    for i in (20, 22, 24, 26, 27, 29):                          # W29: s0(W14) = s0(0) = 0
        G["T%d" % i] = K[i]
    G["T28"] = (K[28] + W[12] + W[21]) & M                      # W28 = C28 + s0(W13) + s1(W26)
    return G


def _s0t(v):
    """Table S0T[v] = sigma0(W13), built once for all groups (proof.md Section 3.5)."""
    return s0(v & M)


def key_program(G, v, tab=_s0t):
    """THE counted per-message program (proof.md Section 3.3)."""
    A = {13: (G["U13"] + v) & M}                                # step 13: 4 ops
    E = {13: (G["V13"] + v) & M}
    W20 = (G["C20"] + v) & M                                    # expansion: 2 + 3*9 + 2 = 31
    W22 = (G["C22"] + Ds1(W20)) & M
    W24 = (G["C24"] + Ds1(W22)) & M
    W26 = (G["C26"] + Ds1(W24)) & M
    W27 = (G["C27"] + W20) & M
    XW = {20: (W20,), 22: (W22,), 24: (W24,), 26: (W26,), 27: (W27,),
          28: (tab(v), Ds1(W26)), 29: (v, W22, Ds1(W27))}       # 1 load + 14 ops
    xp = G["BC14"]                                              # b ^ c of step 14
    for i in range(14, 30):
        e, a = E[i - 1], A[i - 1]
        g = E[i - 3] if i >= 16 else G["E%d" % (i - 3)]
        fg = G["FG14"] if i == 14 else E[i - 2] ^ g
        t = DS1(e) + (g ^ (e & fg))                             # Sigma1 + ch
        if i >= 17:
            t = t + E[i - 4]                                    # h
        for x in XW.get(i, ()):
            t = t + x
        if i <= 16:                                             # h, d are group constants
            E[i] = (t + G["T%dd" % i]) & M
            t1 = t + G["T%d" % i]
        else:
            t1 = t + G["T%d" % i]
            E[i] = (t1 + A[i - 4]) & M
        if i == 29:                                             # key ends at e29
            break
        b = A[i - 2] if i >= 15 else G["A12"]
        x = a ^ b
        A[i] = (t1 + DS0(a) + (b ^ (x & xp))) & M               # maj = b ^ ((a^b) & (b^c))
        xp = x
    return (A[27], A[28], E[27], E[28], E[29])                  # H3, H2, H7, H6, H5 minus IV


def pack(key):
    """K = a27 | a28 << 32 | e27 << 64 | e28 << 96 | e29 << 128 (4 shl + 4 or)."""
    a27, a28, e27, e28, e29 = key
    return a27 | (a28 << 32) | (e27 << 64) | (e28 << 96) | (e29 << 128)


class Word(int):
    """Counting int as in scripts/reference_operation_costs.py (+, &, |, ^, <<, >>, ~),
    also counting reflected operators; tables are read through _tab_counted (one load)."""
    n = 0


def _counted(op):
    def f(self, other):
        Word.n += 1
        return Word(op(int(self), int(other)))
    return f


def _rcounted(op):
    def f(self, other):
        Word.n += 1
        return Word(op(int(other), int(self)))
    return f


for _name, _op in (("add", int.__add__), ("and", int.__and__), ("or", int.__or__),
                   ("xor", int.__xor__), ("lshift", int.__lshift__), ("rshift", int.__rshift__)):
    setattr(Word, "__%s__" % _name, _counted(_op))
    setattr(Word, "__r%s__" % _name, _rcounted(_op))


def _invert(self):
    Word.n += 1
    return Word(~int(self))


Word.__invert__ = _invert


def _tab_counted(v):
    Word.n += 1
    return Word(_s0t(int(v)))


def count_ops(G, v):
    """Counted key_program (incl. the table load) + pack for one message; returns (ops, key)."""
    Word.n = 0
    key = key_program(G, Word(v), _tab_counted)
    pack(key)
    return Word.n, tuple(int(x) for x in key)


def count_setup(p):
    """Counted group_setup (prefix words, IV and K wrapped); returns the operation count."""
    Word.n = 0
    group_setup(tuple(Word(x) for x in p), K=tuple(Word(x) for x in K),
                IV=tuple(Word(x) for x in IV))
    return Word.n


# ---------------------------------------------------------------------------------------
# Uncounted fast path for the experiments only (NOT the attack program): all eight digest
# words with plain ints; cross-checked against key_program on every 32nd message.

def _BS(x, r1, r2, r3):
    d = x | (x << 32)
    return ((d >> r1) ^ (d >> r2) ^ (d >> r3)) & M


def _SS(x, r1, r2, s):
    d = x | (x << 32)
    return ((d >> r1) ^ (d >> r2) ^ (x >> s)) & M


def _fast_digest(G, w13):
    """Plain-int evaluator: (key words, all 8 digest words)."""
    A, E = [(G["U13"] + w13) & M], [(G["V13"] + w13) & M]
    Ac = {12: G["A12"]}
    Ec = {11: G["E11"], 12: G["E12"]}
    Wv = {20: (G["C20"] + w13) & M}
    for i in (22, 24, 26):
        Wv[i] = (G["C%d" % i] + _SS(Wv[i - 2], 17, 19, 10)) & M
    Wv[27] = (G["C27"] + Wv[20]) & M
    Wv[28] = (G["C28"] + _SS(w13, 7, 18, 3) + _SS(Wv[26], 17, 19, 10)) & M
    Wv[29] = (w13 + Wv[22] + _SS(Wv[27], 17, 19, 10)) & M
    Wv[30] = (_SS(440, 7, 18, 3) + G["W23"] + _SS(Wv[28], 17, 19, 10)) & M
    xp = G["BC14"]
    for i in range(14, 31):
        e, a = E[i - 14], A[i - 14]
        f = E[i - 15] if i >= 15 else Ec[12]
        g = E[i - 16] if i >= 16 else Ec[i - 3]
        b = A[i - 15] if i >= 15 else Ac[12]
        t = _BS(e, 6, 11, 25) + (g ^ (e & (f ^ g)))
        if i <= 16:
            e_new, t1 = t + G["T%dd" % i], t + G["T%d" % i]
        else:
            if i in Wv:
                t = t + Wv[i] + (K[i] if i >= 28 else G["T%d" % i])
            else:
                t = t + G["T%d" % i]
            t1 = t + E[i - 17]
            e_new = t1 + A[i - 17]
        x = a ^ b
        A.append((t1 + _BS(a, 2, 13, 22) + (b ^ (x & xp))) & M)
        E.append(e_new & M)
        xp = x
    st8 = (A[17], A[16], A[15], A[14], E[17], E[16], E[15], E[14])
    key = (A[14], A[15], E[14], E[15], E[16])
    return key, tuple((IV[j] + st8[j]) & M for j in range(8))


def _coins(seed, *label):
    return hashlib.sha256(b"s31-grouped-v1|" + seed + b"|" + "|".join(map(str, label)).encode()).digest()


def prefix(seed, g):
    r = _coins(seed, "R", g, 0) + _coins(seed, "R", g, 1)      # two uniform 256-bit words
    return tuple(int.from_bytes(r[4 * j:4 * j + 4], "big") for j in range(13))


def message(p, y):
    return b"".join(x.to_bytes(4, "big") for x in p) + y.to_bytes(3, "big")


def layout(exp, seed):
    if exp == "s31-grouped-spread":
        out = []
        for g in range(32):
            y0 = int.from_bytes(_coins(seed, "Y", g)[:8], "big") % ((1 << 24) - 31)
            out.append((prefix(seed, g), range(y0, y0 + 32)))
        return out
    return [(prefix(seed, 0), range(1024))]


def attempt(exp, seed):
    mask = MASKS[exp]
    tb = (int.from_bytes(_coins(seed, "TB"), "big") >> 32) << 32   # high garbage, low 32 = 0
    table = {}
    found = None
    hits = 0
    ops = None
    checked = 0
    for p, ys in layout(exp, seed):
        G = group_setup(p)
        for j, y in enumerate(ys):
            w13 = (y << 8) | 0x80
            key, dg = _fast_digest(G, w13)
            if j % 32 == 0:                          # cross-check against the counted program
                if ops is None:
                    ops, ref_key = count_ops(G, tb + w13)
                else:
                    ref_key = key_program(G, tb + w13)
                if ref_key != key:
                    raise RuntimeError("fast path disagrees with key_program")
                checked += 1
            mk = tuple(dg[j2] & mask[j2] for j2 in range(8))
            other = table.get(mk)
            if other is None:
                table[mk] = (p, y)
            else:
                hits += 1
                if found is None and other != (p, y):
                    found = (message(*other), message(p, y))
    return found, hits, ops, checked


def main():
    req = json.loads(sys.stdin.read())
    exp = req["experiment_id"]
    rows = []
    for t in req["trials"]:
        found, hits, ops, checked = attempt(exp, bytes.fromhex(t["seed"]))
        a, b = (found[0].hex(), found[1].hex()) if found else (None, None)
        rows.append({"trial": t["trial"], "message_a_hex": a, "message_b_hex": b,
                     "observations": {"masked_matches": hits, "ops_counted": ops,
                                      "crosschecked": checked}})
    sys.stdout.write(json.dumps({"schema_version": 1, "trials": rows}, sort_keys=True))


if __name__ == "__main__":
    main()
