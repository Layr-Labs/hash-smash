"""Scaled grouped birthday search for sha256-r32 using the 4-lane program in proof.md.

Reads one python-message-pairs-v1 request on stdin and writes one JSON result.
Every message is evaluated only by body4(), the packed program of proof.md
Section 4. A_i and E_i are the new a and e of step i. body4 returns packed
A28, A29, E28, E29 and D30 = A30 - E30, whose low 32 bits in lane i are
H3, H2, H7, H6 minus IV and (H1 - IV1) - (H5 - IV5).

Word counts every +, -, &, |, ^, ~, <<, >> the way
scripts/reference_operation_costs.py does, and truncates mod 2^256. On the
first batch of every group and on every key match, the counted body is checked
against a plain 32-step compression. Observations are numeric only.
Standard library only.
"""
import hashlib
import json
import sys

M32 = 0xFFFFFFFF
W256 = (1 << 256) - 1
M4 = 0
SENT = 0
for _i in range(4):
    M4 |= M32 << (64 * _i)
    SENT |= 1 << (64 * _i + 63)
STEP = 0x400 | (0x400 << 64) | (0x400 << 128) | (0x400 << 192)
INIT_W = 0x80 | (0x180 << 64) | (0x280 << 128) | (0x380 << 192)
K = (0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
     0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
     0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
     0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967)
IV = (0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19)
LAYOUTS = {"sha256r32-swar4-spread": (32, 32, 1), "sha256r32-swar4-single-group": (1, 1024, 2)}


class Word(int):
    ops = 0

    def __new__(cls, v):
        return int.__new__(cls, int(v) & W256)


def _counted(fn):
    def apply(self, other=None):
        Word.ops += 1
        return Word(fn(int(self)) if other is None else fn(int(self), int(other)))
    return apply


for _name, _fn in {"add": lambda x, y: x + y, "sub": lambda x, y: x - y, "and": lambda x, y: x & y,
                   "or": lambda x, y: x | y, "xor": lambda x, y: x ^ y, "lshift": lambda x, y: x << y,
                   "rshift": lambda x, y: x >> y, "invert": lambda x: ~x}.items():
    setattr(Word, "__%s__" % _name, _counted(_fn))
for _name, _fn in {"radd": lambda x, y: y + x, "rsub": lambda x, y: y - x, "rand": lambda x, y: y & x,
                   "ror": lambda x, y: y | x, "rxor": lambda x, y: y ^ x}.items():
    setattr(Word, "__%s__" % _name, _counted(_fn))


def S1(x):
    z = x | (x << 32)
    return ((z ^ (z >> 5) ^ (z >> 19)) >> 6) & M4


def S0(x):
    z = x | (x << 32)
    return ((z ^ (z >> 11) ^ (z >> 20)) >> 2) & M4


def s1(x):
    z = x | (x << 32)
    return ((((z ^ (z >> 2)) >> 7) ^ x) >> 10) & M4


def s0(x):
    z = x | (x << 32)
    return ((((z ^ (z >> 11)) >> 4) ^ x) >> 3) & M4


def lane(x, i):
    return (int(x) >> (64 * i)) & M32


def splat(x):
    x &= M32
    r = 0
    for i in range(4):
        r |= x << (64 * i)
    return r & W256


def words_of(prefix52, y):
    block = prefix52 + y.to_bytes(3, "big") + b"\x80" + (440).to_bytes(8, "big")
    return [int.from_bytes(block[4 * i:4 * i + 4], "big") for i in range(16)]


def ror(x, n):
    return ((x >> n) | (x << (32 - n))) & M32


def full_digest(prefix52, y):
    W = words_of(prefix52, y)
    for t in range(16, 32):
        W.append((W[t - 16] + (ror(W[t - 15], 7) ^ ror(W[t - 15], 18) ^ (W[t - 15] >> 3)) + W[t - 7]
                  + (ror(W[t - 2], 17) ^ ror(W[t - 2], 19) ^ (W[t - 2] >> 10))) & M32)
    a, b, c, d, e, f, g, h = IV
    for i in range(32):
        t1 = (h + (ror(e, 6) ^ ror(e, 11) ^ ror(e, 25)) + ((e & f) ^ (~e & g)) + K[i] + W[i]) & M32
        t2 = ((ror(a, 2) ^ ror(a, 13) ^ ror(a, 22)) + ((a & b) ^ (a & c) ^ (b & c))) & M32
        a, b, c, d, e, f, g, h = (t1 + t2) & M32, a, b, c, (d + t1) & M32, e, f, g
    return [(x + y2) & M32 for x, y2 in zip(IV, (a, b, c, d, e, f, g, h))]


def group_setup(W0):
    W = list(W0) + [None, 0, 440] + [0] * 16

    def s0s(x):
        z = x | (x << 32)
        return ((((z ^ (z >> 11)) >> 4) ^ x) >> 3) & M32

    def s1s(x):
        z = x | (x << 32)
        return ((((z ^ (z >> 2)) >> 7) ^ x) >> 10) & M32

    def S0s(x):
        z = x | (x << 32)
        return ((z ^ (z >> 11) ^ (z >> 20)) >> 2) & M32

    def S1s(x):
        z = x | (x << 32)
        return ((z ^ (z >> 5) ^ (z >> 19)) >> 6) & M32

    for t in (16, 17, 18, 19, 21, 23, 25):
        W[t] = (W[t - 16] + s0s(W[t - 15]) + W[t - 7] + s1s(W[t - 2])) & M32
    A, E = {}, {}
    A[-1], A[-2], A[-3], A[-4] = IV[:4]
    E[-1], E[-2], E[-3], E[-4] = IV[4:]
    for i in range(13):
        a, b, c, d = A[i - 1], A[i - 2], A[i - 3], A[i - 4]
        e, f, g, h = E[i - 1], E[i - 2], E[i - 3], E[i - 4]
        t1 = h + S1s(e) + (g ^ (e & (f ^ g))) + K[i] + W[i]
        t2 = S0s(a) + ((a & (b | c)) | (b & c))
        A[i] = (t1 + t2) & M32
        E[i] = (d + t1) & M32
    a, b, c, d = A[12], A[11], A[10], A[9]
    e, f, g, h = E[12], E[11], E[10], E[9]
    t1p = h + S1s(e) + (g ^ (e & (f ^ g))) + K[13]
    X = {
        "cA13": (t1p + S0s(a) + ((a & (b | c)) | (b & c))) & M32,
        "cE13": (d + t1p) & M32,
        "bOc14": A[12] | A[11],
        "bAc14": A[12] & A[11],
        "fg14": E[12] ^ E[11],
        "g14": E[11],
        "hKW14": (E[10] + K[14]) & M32,
        "d14": A[10],
        "c15": A[12],
        "g15": E[12],
        "hKW15": (E[11] + K[15] + 440) & M32,
        "d15": A[11],
        "hKW16": (E[12] + K[16] + W[16]) & M32,
        "d16": A[12],
    }
    for i in (17, 18, 19, 21, 23, 25):
        X["KW%d" % i] = (K[i] + W[i]) & M32
    c20 = (W[4] + s0s(W[5]) + s1s(W[18])) & M32
    X["c20"] = c20
    X["c20K"] = (c20 + K[20]) & M32
    X["c22"] = (W[6] + s0s(W[7]) + 440) & M32
    X["K22"] = K[22]
    X["c24"] = (W[8] + s0s(W[9]) + W[17]) & M32
    X["K24"] = K[24]
    X["c26"] = (W[10] + s0s(W[11]) + W[19]) & M32
    X["K26"] = K[26]
    c2027 = (c20 + W[11] + s0s(W[12]) + s1s(W[25])) & M32
    X["c2027"] = c2027
    X["c2027K"] = (c2027 + K[27]) & M32
    X["c28K"] = (W[12] + W[21] + K[28]) & M32
    X["c29K"] = K[29]
    return {k: splat(v) for k, v in X.items()}


def body4(X, w):
    """Packed body of proof.md Section 4. w holds four W13 lanes."""
    A, E = {}, {}
    A[13] = (X["cA13"] + w) & M4
    E[13] = (X["cE13"] + w) & M4
    w20 = (X["c20"] + w) & M4
    KW20 = X["c20K"] + w
    w22 = (X["c22"] + s1(w20)) & M4
    KW22 = X["K22"] + w22
    w24 = (X["c24"] + s1(w22)) & M4
    KW24 = X["K24"] + w24
    w26 = (X["c26"] + s1(w24)) & M4
    KW26 = X["K26"] + w26
    w27 = (X["c2027"] + w) & M4
    KW27 = X["c2027K"] + w
    KW28 = s1(w26) + s0(w) + X["c28K"]
    KW29 = s1(w27) + w22 + (w + X["c29K"])
    KW = {20: KW20, 22: KW22, 24: KW24, 26: KW26, 27: KW27, 28: KW28, 29: KW29,
          17: X["KW17"], 18: X["KW18"], 19: X["KW19"], 21: X["KW21"], 23: X["KW23"], 25: X["KW25"]}
    a, e = A[13], E[13]
    t1 = S1(e) + (X["g14"] ^ (e & X["fg14"])) + X["hKW14"]
    A[14] = (t1 + (S0(a) + ((a & X["bOc14"]) | X["bAc14"]))) & M4
    E[14] = (t1 + X["d14"]) & M4
    a, b, e, f = A[14], A[13], E[14], E[13]
    t1 = S1(e) + (X["g15"] ^ (e & (f ^ X["g15"]))) + X["hKW15"]
    x = a ^ b
    A[15] = (t1 + (S0(a) + (b ^ (x & (b ^ X["c15"]))))) & M4
    E[15] = (t1 + X["d15"]) & M4
    xprev = x
    for i in range(16, 30):
        a, b = A[i - 1], A[i - 2]
        d = X["d16"] if i == 16 else A[i - 4]
        e, f, g = E[i - 1], E[i - 2], E[i - 3]
        if i == 16:
            t1 = S1(e) + (g ^ (e & (f ^ g))) + X["hKW16"]
        else:
            t1 = S1(e) + (g ^ (e & (f ^ g))) + E[i - 4] + KW[i]
        x = a ^ b
        A[i] = (t1 + (S0(a) + (b ^ (x & xprev)))) & M4
        E[i] = (t1 + d) if i == 29 else (t1 + d) & M4
        xprev = x
    x = A[29] ^ A[28]
    T2 = S0(A[29]) + (A[28] ^ (x & xprev))
    D30 = ((T2 & M4) | SENT) - (A[26] & M4)
    return A[28], A[29], E[28], E[29], D30


def key_of_digest(H):
    a28, a29, e28, e29 = ((H[j] - IV[j]) & M32 for j in (3, 2, 7, 6))
    return a28, a29, e28, e29, ((H[1] - IV[1]) - (H[5] - IV[5])) & M32


def check_batch(prefix, base_y, X, w):
    Word.ops = 0
    out = body4({k: Word(v) for k, v in X.items()}, Word(int(w)))
    ops = Word.ops
    bad = 0
    for i in range(4):
        got = tuple(lane(out[j], i) for j in range(5))
        exp = key_of_digest(full_digest(prefix, base_y + i))
        if got != exp:
            bad += 1
    return bad, ops


def run_trial(seed_hex, groups, ys, dbits, mask_words):
    coins = hashlib.shake_256(b"hashsmash-sha256r32-swar4" + bytes.fromhex(seed_hex)).digest(64 * groups)
    m2, m3, m6, m7 = mask_words[2], mask_words[3], mask_words[6], mask_words[7]
    dmask = (1 << dbits) - 1
    S, D = {}, []
    obs = {"messages_evaluated": 0, "key_matches": 0, "evaluator_checks": 0, "evaluator_mismatches": 0,
           "body_ops_min": 10 ** 9, "body_ops_max": 0, "lanes_checked": 0}

    def check(prefix, base_y, X, w):
        bad, ops = check_batch(prefix, base_y, X, w)
        obs["evaluator_checks"] += 1
        obs["evaluator_mismatches"] += bad
        obs["lanes_checked"] += 4
        obs["body_ops_min"] = min(obs["body_ops_min"], ops)
        obs["body_ops_max"] = max(obs["body_ops_max"], ops)

    for gi in range(groups):
        prefix = coins[64 * gi:64 * gi + 52]
        X = group_setup(words_of(prefix, 0)[:13])
        w = INIT_W
        for batch in range(ys // 4):
            base_y = batch * 4
            fast = body4(X, w)
            if batch == 0:
                check(prefix, base_y, X, w)
            for i in range(4):
                y = base_y + i
                obs["messages_evaluated"] += 1
                a28, a29, e28, e29 = lane(fast[0], i), lane(fast[1], i), lane(fast[2], i), lane(fast[3], i)
                d30 = lane(fast[4], i)
                skey = (((a29 + IV[2]) & m2), ((a28 + IV[3]) & m3), ((e29 + IV[6]) & m6),
                        ((e28 + IV[7]) & m7), d30 & dmask)
                s = S.get(skey)
                if s is not None:
                    obs["key_matches"] += 1
                    check(prefix, base_y, X, w)
                    op, oy = D[s]
                    da, db = full_digest(op, oy), full_digest(prefix, y)
                    if (op, oy) != (prefix, y) and all(((p ^ q) & mw) == 0 for p, q, mw in zip(da, db, mask_words)):
                        return (op + oy.to_bytes(3, "big")).hex(), (prefix + y.to_bytes(3, "big")).hex(), obs
                S[skey] = len(D)
                D.append((prefix, y))
            w = (w + STEP) & W256
    return None, None, obs


def main():
    request = json.loads(sys.stdin.read())
    groups, ys, dbits = LAYOUTS[request["experiment_id"]]
    mask = bytes.fromhex(request["event"]["mask_hex"])
    mask_words = [int.from_bytes(mask[4 * i:4 * i + 4], "big") for i in range(8)]
    trials = []
    for trial in request["trials"]:
        ma, mb, obs = run_trial(trial["seed"], groups, ys, dbits, mask_words)
        trials.append({"trial": trial["trial"], "message_a_hex": ma, "message_b_hex": mb, "observations": obs})
    sys.stdout.write(json.dumps({"schema_version": 1, "trials": trials}))


if __name__ == "__main__":
    main()
