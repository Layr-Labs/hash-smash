"""Scaled grouped birthday search on exact sha256-r32, using the counted program of proof.md.

Reads one python-message-pairs-v1 request on stdin and writes one JSON result.
Per trial (organizer seed): G groups share a 52-byte prefix W0..W12 drawn from
SHAKE-256(seed); each group enumerates y = 0..Y-1 in W13 = (y << 8) | 0x80
(55-byte messages, W14 = 0, W15 = 440). Every message is evaluated ONLY by
body() below, which is the per-message program of proof.md Section 3 written
with Python operators. A_i, E_i are the new a, e of step i (i = 0..31). It
returns the key words A28, A29, E28, E29 (= H3, H2, H7, H6 minus IV) and
D' = T2_30 + ~A26, where D' + 1 = A30 - E30 = (H1 - IV1) - (H5 - IV5) mod 2^32,
plus the packed 256-bit key word.

The same body() runs on plain ints (fast path) and on Word, a 256-bit int
subclass that counts every +, &, |, ^, ~, <<, >> exactly like
scripts/reference_operation_costs.py and truncates every result mod 2^256.
All group constants and W13 are Words in the counted run, so every operation
of the body is counted. For y = 0 of every group and for every key match the
program runs the counted body, checks that it agrees with the fast body and
with a plain full 32-step compression bit for bit (key words, D', packed key
fields), and reports the counts (body_ops_min/max, setup_ops_max) and
evaluator_checks / evaluator_mismatches (expected 0) as observations.

Scaled key = the event-mask bits of H2, H3, H6, H7 plus the low t bits of D'
(t = 1 or 2; the mask has bits 0..t-1 on both H1 and H5, so equal masked
digests give equal low t bits of D'). The table maps each scaled key to the
LATEST message with that key (unconditional overwrite, as in proof.md
Section 4). A key match is verified with two plain full compressions against
the whole 20-bit mask; the first verified pair ends the trial; otherwise the
new message overwrites the slot. Standard library only.
"""
import hashlib
import json
import sys

M = 0xffffffff
W256 = (1 << 256) - 1
K = (0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
     0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
     0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
     0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967)
IV = (0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19)
LAYOUTS = {"sha256r32-v2-spread": (32, 32, 1), "sha256r32-v2-single-group": (1, 1024, 2)}


class Word(int):
    """256-bit register value; every operator costs 1 (reference_operation_costs.py convention)."""
    ops = 0


def _counted(fn):
    def apply(self, other=None):
        Word.ops += 1
        return Word((fn(int(self)) if other is None else fn(int(self), int(other))) & W256)
    return apply


for _name, _fn in {"add": lambda x, y: x + y, "and": lambda x, y: x & y, "or": lambda x, y: x | y,
                   "xor": lambda x, y: x ^ y, "lshift": lambda x, y: x << y,
                   "rshift": lambda x, y: x >> y, "invert": lambda x: ~x}.items():
    setattr(Word, "__%s__" % _name, _counted(_fn))
for _name, _fn in {"radd": lambda x, y: y + x, "rand": lambda x, y: y & x, "ror": lambda x, y: y | x,
                   "rxor": lambda x, y: y ^ x}.items():
    setattr(Word, "__%s__" % _name, _counted(_fn))


# Sigma functions of a REDUCED word x (x < 2^32), 7 operations each, via z = x | x << 32.
# Bits 0..31 of the result are exact; bits 32..63 hold garbage (the result is < 2^64).
def S1(x):  # rotr6 ^ rotr11 ^ rotr25
    z = x | (x << 32)
    return (z ^ (z >> 5) ^ (z >> 19)) >> 6


def S0(x):  # rotr2 ^ rotr13 ^ rotr22
    z = x | (x << 32)
    return (z ^ (z >> 11) ^ (z >> 20)) >> 2


def s1(x):  # rotr17 ^ rotr19 ^ shr10
    z = x | (x << 32)
    return (((z ^ (z >> 2)) >> 7) ^ x) >> 10


def s0(x):  # rotr7 ^ rotr18 ^ shr3
    z = x | (x << 32)
    return (((z ^ (z >> 11)) >> 4) ^ x) >> 3


def words_of(prefix52, y):
    block = prefix52 + y.to_bytes(3, "big") + b"\x80" + (440).to_bytes(8, "big")
    return [int.from_bytes(block[4 * i:4 * i + 4], "big") for i in range(16)]


# ---- plain reference compression (verification and self-check only) ----
def ror(x, n):
    return ((x >> n) | (x << (32 - n))) & M


def full_digest(prefix52, y):
    W = words_of(prefix52, y)
    for t in range(16, 32):
        W.append((W[t - 16] + (ror(W[t - 15], 7) ^ ror(W[t - 15], 18) ^ (W[t - 15] >> 3)) + W[t - 7]
                  + (ror(W[t - 2], 17) ^ ror(W[t - 2], 19) ^ (W[t - 2] >> 10))) & M)
    a, b, c, d, e, f, g, h = IV
    for i in range(32):
        t1 = (h + (ror(e, 6) ^ ror(e, 11) ^ ror(e, 25)) + ((e & f) ^ (~e & g)) + K[i] + W[i]) & M
        t2 = ((ror(a, 2) ^ ror(a, 13) ^ ror(a, 22)) + ((a & b) ^ (a & c) ^ (b & c))) & M
        a, b, c, d, e, f, g, h = (t1 + t2) & M, a, b, c, (d + t1) & M, e, f, g
    return [(x + y2) & M for x, y2 in zip(IV, (a, b, c, d, e, f, g, h))]


# ---- group setup (once per group; counted in the Word run as setup_ops) ----
def group_setup(W, iv=IV):
    """W = W0..W12 and iv = IV (registers). Returns the group constants used by body()."""
    W = list(W) + [None, 0, 440] + [None] * 16
    for t in (16, 17, 18, 19, 21, 23, 25):
        W[t] = (W[t - 16] + s0(W[t - 15]) + W[t - 7] + s1(W[t - 2])) & M
    A, E = {}, {}
    A[-1], A[-2], A[-3], A[-4] = iv[0], iv[1], iv[2], iv[3]
    E[-1], E[-2], E[-3], E[-4] = iv[4], iv[5], iv[6], iv[7]
    for i in range(13):
        a, b, c, d, e, f, g, h = A[i - 1], A[i - 2], A[i - 3], A[i - 4], E[i - 1], E[i - 2], E[i - 3], E[i - 4]
        t1 = h + S1(e) + (g ^ (e & (f ^ g))) + K[i] + W[i]
        t2 = S0(a) + ((a & (b | c)) | (b & c))
        A[i], E[i] = (t1 + t2) & M, (d + t1) & M
    a, b, c, d, e, f, g, h = A[12], A[11], A[10], A[9], E[12], E[11], E[10], E[9]
    t1 = h + S1(e) + (g ^ (e & (f ^ g))) + K[13]          # step 13 without W13
    X = {"cA13": t1 + S0(a) + ((a & (b | c)) | (b & c)), "cE13": d + t1}
    X["bOc14"], X["bAc14"], X["fg14"], X["g14"] = A[12] | A[11], A[12] & A[11], E[12] ^ E[11], E[11]
    X["hKW14"], X["d14"] = E[10] + K[14], A[10]              # W14 = 0
    X["c15"], X["g15"], X["hKW15"], X["d15"] = A[12], E[12], E[11] + (K[15] + W[15]), A[11]
    X["hKW16"], X["d16"] = E[12] + (K[16] + W[16]), A[12]
    for i in (17, 18, 19, 21, 23, 25):
        X["KW%d" % i] = K[i] + W[i]
    c20 = W[4] + s0(W[5]) + s1(W[18])
    X["c20"], X["c20K"] = c20, c20 + K[20]
    X["c22"], X["K22"] = W[6] + s0(W[7]) + W[15], K[22]
    X["c24"], X["K24"] = W[8] + s0(W[9]) + W[17], K[24]
    X["c26"], X["K26"] = W[10] + s0(W[11]) + W[19], K[26]
    c2027 = c20 + W[11] + s0(W[12]) + s1(W[25])
    X["c2027"], X["c2027K"] = c2027, c2027 + K[27]
    X["c28K"] = W[12] + W[21] + K[28]
    X["c29K"] = K[29]                                         # s0(W14) = 0
    return X


# ---- per-message body: proof.md Section 3.3, 532 counted operations ----
def body(X, w):
    """w = W13 (reduced). Returns (A28, A29, E28, E29, D', packed key)."""
    A, E = {}, {}
    A[13] = (X["cA13"] + w) & M
    E[13] = (X["cE13"] + w) & M
    KW = {}
    w20 = (X["c20"] + w) & M
    KW[20] = X["c20K"] + w
    w22 = (X["c22"] + s1(w20)) & M
    KW[22] = X["K22"] + w22
    w24 = (X["c24"] + s1(w22)) & M
    KW[24] = X["K24"] + w24
    w26 = (X["c26"] + s1(w24)) & M
    KW[26] = X["K26"] + w26
    w27 = (X["c2027"] + w) & M
    KW[27] = X["c2027K"] + w
    KW[28] = s1(w26) + s0(w) + X["c28K"]
    KW[29] = s1(w27) + w22 + (w + X["c29K"])
    for i in (17, 18, 19, 21, 23, 25):
        KW[i] = X["KW%d" % i]
    # step 14: b, c, d, f, g, h are group constants
    a, e = A[13], E[13]
    t1 = S1(e) + (X["g14"] ^ (e & X["fg14"])) + X["hKW14"]
    A[14] = (t1 + (S0(a) + ((a & X["bOc14"]) | X["bAc14"]))) & M
    E[14] = (t1 + X["d14"]) & M
    # step 15: c, d, g, h are group constants
    a, b, e, f = A[14], A[13], E[14], E[13]
    t1 = S1(e) + (X["g15"] ^ (e & (f ^ X["g15"]))) + X["hKW15"]
    x = a ^ b
    A[15] = (t1 + (S0(a) + (b ^ (x & (b ^ X["c15"]))))) & M
    E[15] = (t1 + X["d15"]) & M
    xprev = x
    # steps 16..29
    for i in range(16, 30):
        a, b, d = A[i - 1], A[i - 2], (A[i - 4] if i >= 17 else X["d16"])
        e, f, g = E[i - 1], E[i - 2], E[i - 3]
        if i == 16:
            t1 = S1(e) + (g ^ (e & (f ^ g))) + X["hKW16"]
        else:
            t1 = S1(e) + (g ^ (e & (f ^ g))) + E[i - 4] + KW[i]
        x = a ^ b
        A[i] = (t1 + (S0(a) + (b ^ (x & xprev)))) & M
        E[i] = (t1 + d) if i == 29 else (t1 + d) & M
        xprev = x
    # D' = T2 of step 30 + ~A26 = (A30 - E30) - 1 mod 2^32
    x = A[29] ^ A[28]
    Dp = S0(A[29]) + (A[28] ^ (x & xprev)) + ~A[26]
    key = (A[28] << 96) | (E[28] << 128)
    key = key | (A[29] << 160)
    key = key | ((E[29] & M) << 192)
    key = key | (Dp << 224)
    return A[28], A[29], E[28], E[29], Dp, key


def setup_fast(prefix52):
    return {k: v & W256 for k, v in group_setup(words_of(prefix52, 0)[:13]).items()}


def key_of_digest(H):
    """(A28, A29, E28, E29, D'+1) from a full digest."""
    a28, a29, e28, e29 = ((H[j] - IV[j]) & M for j in (3, 2, 7, 6))
    return a28, a29, e28, e29, (((H[1] - IV[1]) - (H[5] - IV[5])) & M)


def counted_check(prefix52, y, fast):
    """Counted run of setup and body; returns (mismatch, body_ops, setup_ops)."""
    Word.ops = 0
    Xw = group_setup([Word(v) for v in words_of(prefix52, 0)[:13]], [Word(v) for v in IV])
    setup_ops = Word.ops
    Xw = {k: Word(int(v) & W256) for k, v in Xw.items()}
    Word.ops = 0
    out = body(Xw, Word((y << 8) | 0x80))
    body_ops = Word.ops
    a28, a29, e28, e29, dp, key = (int(v) for v in out)
    exp = key_of_digest(full_digest(prefix52, y))
    fields = tuple((key >> p) & M for p in (96, 160, 128, 192, 224))
    bad = ((a28, a29, e28, e29 & M, (dp + 1) & M) != exp or fields[:4] != exp[:4]
           or (fields[4] + 1) & M != exp[4] or key != fast[5] & W256
           or (fast[4] - dp) & M != 0)
    return int(bad), body_ops, setup_ops


def run_trial(seed_hex, groups, ys, dbits, mask_words):
    coins = hashlib.shake_256(b"hashsmash-sha256r32-grouped-v2" + bytes.fromhex(seed_hex)).digest(64 * groups)
    m2, m3, m6, m7 = mask_words[2], mask_words[3], mask_words[6], mask_words[7]
    dmask = (1 << dbits) - 1
    S, D = {}, []                  # S: scaled key -> latest record index; D: record -> (prefix, y)
    obs = {"messages_evaluated": 0, "key_matches": 0, "evaluator_checks": 0, "evaluator_mismatches": 0,
           "body_ops_min": 10 ** 9, "body_ops_max": 0, "setup_ops_max": 0}

    def check(prefix, y, fast):
        bad, bops, sops = counted_check(prefix, y, fast)
        obs["evaluator_checks"] += 1
        obs["evaluator_mismatches"] += bad
        obs["body_ops_min"] = min(obs["body_ops_min"], bops)
        obs["body_ops_max"] = max(obs["body_ops_max"], bops)
        obs["setup_ops_max"] = max(obs["setup_ops_max"], sops)

    for gi in range(groups):
        prefix = coins[64 * gi:64 * gi + 52]
        X = setup_fast(prefix)
        for y in range(ys):
            fast = body(X, (y << 8) | 0x80)
            obs["messages_evaluated"] += 1
            if y == 0:
                check(prefix, y, fast)
            a28, a29, e28, e29 = fast[0], fast[1], fast[2], fast[3] & M
            skey = (((a29 + IV[2]) & m2), ((a28 + IV[3]) & m3), ((e29 + IV[6]) & m6),
                    ((e28 + IV[7]) & m7), fast[4] & dmask)
            s = S.get(skey)
            if s is not None:
                obs["key_matches"] += 1
                check(prefix, y, fast)
                op, oy = D[s]
                da, db = full_digest(op, oy), full_digest(prefix, y)
                if (op, oy) != (prefix, y) and all(((p ^ q) & mw) == 0 for p, q, mw in zip(da, db, mask_words)):
                    return (op + oy.to_bytes(3, "big")).hex(), (prefix + y.to_bytes(3, "big")).hex(), obs
            S[skey] = len(D)
            D.append((prefix, y))
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
