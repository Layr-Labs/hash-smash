"""v6 sha256-r31 package check (organizer sandbox; stdlib only; deterministic).

Trials 0..91 return the 92 pairs found by the pre-registered runs (E-C, then the 91 E-S successes in key order;
trials 0..15 are the 16 certificates). Every M1' = M1 + DW word-wise, DW in words 5..9 of the second block.
Every trial also runs the counted 7-lane x 36-bit SWAR batch of the online phase on 16 random 256-bit words derived
from the organizer's trial seed (SHAKE-256), and compares each lane's key (CV word 0) and full chaining value with a
scalar 31-step SHA-256 compression of the same lane block. Observations (untrusted, recomputable from this source):
exact counted primitives per batch and by category, lanes whose key / full CV equal the scalar compression.
No probability or cost inference: trials 92..255 return no pair by design."""
import base64, hashlib, json, sys, zlib

C = 2140
L, W = 7, 36
M32 = 0xFFFFFFFF
IV = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
     0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
     0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
     0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967]
DW = (0x00000ffa, 0x001f77ef, 0xb00fb5fa, 0xd800f100, 0x00008004)
PAIRS_Z = "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"   # zlib+base64 of the 92 first messages M0||M1 (128 bytes each)
CATS = ("rand", "load", "add", "and", "or", "xor", "shift", "cmp", "branch")


def rotr(x, r):
    return ((x >> r) | (x << (32 - r))) & M32


def compress31(st, words):
    w = list(words)
    for i in range(16, 31):
        s0 = rotr(w[i - 15], 7) ^ rotr(w[i - 15], 18) ^ (w[i - 15] >> 3)
        s1 = rotr(w[i - 2], 17) ^ rotr(w[i - 2], 19) ^ (w[i - 2] >> 10)
        w.append((w[i - 16] + s0 + w[i - 7] + s1) & M32)
    a, b, c, d, e, f, g, h = st
    for i in range(31):
        t1 = (h + (rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25)) + ((e & f) ^ (~e & g)) + K[i] + w[i]) & M32
        t2 = ((rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22)) + ((a & b) ^ (a & c) ^ (b & c))) & M32
        h, g, f, e, d, c, b, a = g, f, e, (d + t1) & M32, c, b, a, (t1 + t2) & M32
    return [(x + y) & M32 for x, y in zip(st, (a, b, c, d, e, f, g, h))]


class Swar:
    """7 lanes x 36 bits in one 256-bit word; every executed primitive is counted; masks are resident registers."""

    def __init__(self):
        self.c = dict.fromkeys(CATS, 0)
        self.M = self.bc(M32)
        self.lo = {r: self.bc(M32 >> r) for r in (2, 6, 7, 11, 13, 17, 18, 19, 22, 25)}
        self.hi = {r: self.bc((M32 << (32 - r)) & M32) for r in self.lo}
        self.sm = {k: self.bc(M32 >> k) for k in (3, 10)}
        self.regs = 1 + 2 * len(self.lo) + len(self.sm) + 16 + 8 + 8

    @staticmethod
    def bc(v):
        return sum((v & M32) << (W * l) for l in range(L))

    def t(self, k):
        self.c[k] += 1

    def AND(self, a, b): self.t("and"); return a & b
    def OR(self, a, b): self.t("or"); return a | b
    def XOR(self, a, b): self.t("xor"); return a ^ b
    def ADD(self, a, b): self.t("add"); return (a + b) & ((1 << 256) - 1)
    def SHR(self, a, k): self.t("shift"); return a >> k
    def SHL(self, a, k): self.t("shift"); return (a << k) & ((1 << 256) - 1)
    def mk(self, x): return self.AND(x, self.M)
    def ROTR(self, x, r): return self.OR(self.AND(self.SHR(x, r), self.lo[r]), self.AND(self.SHL(x, 32 - r), self.hi[r]))
    def S32(self, x, k): return self.AND(self.SHR(x, k), self.sm[k])
    def sig0(self, x): return self.XOR(self.XOR(self.ROTR(x, 7), self.ROTR(x, 18)), self.S32(x, 3))
    def sig1(self, x): return self.XOR(self.XOR(self.ROTR(x, 17), self.ROTR(x, 19)), self.S32(x, 10))
    def BS1(self, x): return self.XOR(self.XOR(self.ROTR(x, 6), self.ROTR(x, 11)), self.ROTR(x, 25))
    def BS0(self, x): return self.XOR(self.XOR(self.ROTR(x, 2), self.ROTR(x, 13)), self.ROTR(x, 22))
    def CH(self, e, f, g): return self.XOR(self.AND(e, f), self.AND(self.XOR(e, self.M), g))
    def MAJ(self, a, b, c): return self.XOR(self.XOR(self.AND(a, b), self.AND(a, c)), self.AND(b, c))

    def batch(self, draws):
        """the counted early-abort batch of the online phase (the same primitives in the same order as our charged swar31.py)."""
        w = []
        for i in range(16):
            self.t("rand")
            w.append(self.mk(draws[i]))
        st = []
        for j in range(8):
            self.t("load"); st.append(self.bc(IV[j]))
        a, b, c, d, e, f, g, h = st
        for i in range(31):
            if i < 16:
                wi = w[i]
            else:
                s1 = self.sig1(w[(i - 2) % 16]); s0 = self.sig0(w[(i - 15) % 16])
                wi = self.mk(self.ADD(self.ADD(s1, w[(i - 7) % 16]), self.ADD(s0, w[(i - 16) % 16])))
                w[i % 16] = wi
            s1 = self.BS1(e); ch = self.CH(e, f, g)
            self.t("load"); k = self.bc(K[i])
            t1 = self.ADD(self.ADD(self.ADD(h, s1), self.ADD(ch, wi)), k)
            t2 = self.ADD(self.BS0(a), self.MAJ(a, b, c))
            h, g, f, e, d, c, b, a = g, f, e, self.mk(self.ADD(d, t1)), c, b, a, self.mk(self.ADD(t1, t2))
        self.t("load"); out0 = self.mk(self.ADD(self.bc(IV[0]), a))
        keys = []
        for l in range(L):
            k = self.AND(self.SHR(out0, W * l), self.M)
            keys.append(k & M32)
            self.SHR(k, 8); self.t("load"); self.AND(k, 255); self.SHR(0, 0); self.AND(0, 1); self.t("cmp"); self.t("branch")
        for _ in range(6):
            self.t("branch")
        # verification only (not part of the counted batch): the full CV of every lane from the same registers
        full = [[((x + self.bc(IV[j])) >> (W * l)) & M32 for j, x in enumerate((a, b, c, d, e, f, g, h))] for l in range(L)]
        return keys, full


def pair(m0):
    words = [int.from_bytes(m0[4 * i:4 * i + 4], "big") for i in range(32)]
    for j, d in enumerate(DW):
        words[21 + j] = (words[21 + j] + d) & M32
    return m0, b"".join(x.to_bytes(4, "big") for x in words)


def main():
    req = json.loads(sys.stdin.read())
    blob = zlib.decompress(base64.b64decode(PAIRS_Z))
    firsts = [blob[128 * i:128 * i + 128] for i in range(len(blob) // 128)]
    out = []
    for tr in req["trials"]:
        idx = tr["trial"]
        draws_raw = hashlib.shake_256(bytes.fromhex(tr["seed"])).digest(16 * 32)
        draws = [int.from_bytes(draws_raw[32 * i:32 * i + 32], "little") for i in range(16)]
        m = Swar()
        keys, full = m.batch(draws)
        ok_key = ok_full = 0
        for l in range(L):
            blk = [(draws[i] >> (W * l)) & M32 for i in range(16)]
            ref = compress31(IV, blk)
            ok_key += keys[l] == ref[0]
            ok_full += full[l] == ref
        obs = {"batch_ops": sum(m.c.values()), "lanes_key_eq_scalar": ok_key, "lanes_cv_eq_scalar": ok_full,
               "registers": m.regs}
        obs.update({"ops_" + k: m.c[k] for k in CATS})
        row = {"trial": idx, "message_a_hex": None, "message_b_hex": None, "observations": obs}
        if idx < len(firsts):
            a, b = pair(firsts[idx])
            row["message_a_hex"], row["message_b_hex"] = a.hex(), b.hex()
        out.append(row)
    sys.stdout.write(json.dumps({"schema_version": 1, "trials": out}, sort_keys=True))


if __name__ == "__main__":
    main()
