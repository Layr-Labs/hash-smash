"""v8 sha256-r31 package check (organizer sandbox; stdlib only; deterministic).

Trial 0 returns the stored pair of the scored replay (the certificate): M1' = M1 + DW word-wise, DW = the published
characteristic's d5..d9 in words 5..9 of the second block. Every trial also runs the counted 7-lane x 36-bit SWAR batch
of the online phase on 16 random 256-bit words derived from the organizer's trial seed (SHAKE-256), and compares each
lane's key (CV word 0) and full chaining value with a scalar 31-step SHA-256 compression of the same lane block.
Observations (untrusted, recomputable from this source): exact counted primitives per batch and by category, lanes
whose key / full CV equal the scalar compression, and lanes whose bitmap probe (run against a per-trial synthetic
bitmap that holds the scalar keys of lanes 0..3 only) answers correctly. Trial 0 also re-derives the stored M0 from the
pre-registered online key: key = first 16 bytes of SHA-256("sha256-r31-v8 online key 1"), AES-128-CTR (pure-Python
FIPS-197 AES, self-tested on the C.1 vector) in v6on's batch layout at batch 15,645,968, lane 1.
No probability or cost inference: trials 1..255 return no pair."""
import base64, hashlib, json, sys, zlib

C = 2140
L, W = 7, 36
M32 = 0xFFFFFFFF
IV = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
     0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
     0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
     0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967]
DW = (0xfffff006, 0x002087f1, 0x4fefb5fa, 0x28011100, 0x00008004)
PAIRS_Z = "eNoBgAB///IouBY2RMp6Mep/WUeMfXKdBk0e+HQxPM3+mxd/11d9LrxxncgrPlDpxZXC0uZwqoi776qUb25QG0trXiQI73eUASkhRHYpT8iA7ahntqOn4eIqo8iit0OaxWE2BrRX+2PxlWyRKmkZawJTmmMZpfNsaoKhKXzg2GWs9IeWK3vrzn4/7A=="   # zlib+base64 of the stored first message M0||M1 (128 bytes)
CATS = ("rand", "load", "add", "and", "or", "xor", "shift", "cmp", "branch")
ONLINE_KEY = hashlib.sha256(b"sha256-r31-v8 online key 1").digest()[:16]
FOUND_BATCH, FOUND_LANE = 15645968, 1

# ---------------- AES-128 encryption (FIPS-197), pure Python; only used to re-derive M0 ----------------
def _xt(a): return ((a << 1) ^ 0x1B) & 0xFF if a & 0x80 else a << 1
def _sbox():
    s, p, q = [0] * 256, 1, 1
    while True:
        p = p ^ ((p << 1) & 0xFF) ^ (0x1B if p & 0x80 else 0)
        q ^= q << 1; q ^= q << 2; q ^= q << 4; q &= 0xFF
        if q & 0x80: q ^= 0x09
        x = q ^ ((q << 1) | (q >> 7)) ^ ((q << 2) | (q >> 6)) ^ ((q << 3) | (q >> 5)) ^ ((q << 4) | (q >> 4))
        s[p] = (x ^ 0x63) & 0xFF
        if p == 1: break
    s[0] = 0x63
    return s
SBOX = _sbox()
def aes_expand(key):
    w = [list(key[4 * i:4 * i + 4]) for i in range(4)]
    rc = 1
    for i in range(4, 44):
        t = list(w[i - 1])
        if i % 4 == 0:
            t = [SBOX[t[1]] ^ rc, SBOX[t[2]], SBOX[t[3]], SBOX[t[0]]]
            rc = _xt(rc)
        w.append([w[i - 4][k] ^ t[k] for k in range(4)])
    return [sum(w[4 * r:4 * r + 4], []) for r in range(11)]
def aes_enc(rk, blk):
    s = [b ^ k for b, k in zip(blk, rk[0])]
    for r in range(1, 11):
        s = [SBOX[x] for x in s]
        s = [s[(i + 4 * (i % 4)) % 16] for i in range(16)]          # ShiftRows (column-major state)
        if r < 10:
            o = []
            for c in range(4):
                a = s[4 * c:4 * c + 4]
                o += [_xt(a[0]) ^ _xt(a[1]) ^ a[1] ^ a[2] ^ a[3], a[0] ^ _xt(a[1]) ^ _xt(a[2]) ^ a[2] ^ a[3],
                      a[0] ^ a[1] ^ _xt(a[2]) ^ _xt(a[3]) ^ a[3], _xt(a[0]) ^ a[0] ^ a[1] ^ a[2] ^ _xt(a[3])]
            s = o
        s = [b ^ k for b, k in zip(s, rk[r])]
    return bytes(s)
def stream_lane(key, b, lane):
    """lane `lane` of v6on's SWAR batch b: word i = bits [36 lane, 36 lane + 32) of AES(ctr 32b+2i) || AES(ctr 32b+2i+1),
    counters as 16-byte blocks (low 64 bits little-endian, high 64 bits 0), outputs read as little-endian integers."""
    rk = aes_expand(key)
    words = []
    for i in range(16):
        x = b"".join(aes_enc(rk, (32 * b + 2 * i + j).to_bytes(8, "little") + bytes(8)) for j in (0, 1))
        words.append((int.from_bytes(x, "little") >> (36 * lane)) & M32)
    return words
assert aes_enc(aes_expand(bytes(range(16))), bytes.fromhex("00112233445566778899aabbccddeeff")).hex() == "69c4e0d86a7b0430d8cdb78070b4c55a"


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
        self.M0 = M32                                    # single-lane mask (lane 0) for the key extraction
        self.regs = 2 + 2 * len(self.lo) + len(self.sm) + 16 + 8 + 8

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

    def batch(self, draws, bitmap):
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
        keys, probes = [], []
        for l in range(L):
            k = self.AND(self.SHR(out0, W * l), self.M0)
            keys.append(k)
            # bitmap probe: 2^32 bits in 2^24 256-bit words; word index k >> 8, bit index k & 255
            wi = self.SHR(k, 8); self.t("load"); word = bitmap.get(wi, 0); bi = self.AND(k, 255)
            probes.append(self.AND(self.SHR(word, bi), 1)); self.t("cmp"); self.t("branch")
        for _ in range(6):
            self.t("branch")
        # verification only (not part of the counted batch): the full CV of every lane from the same registers
        full = [[((x + self.bc(IV[j])) >> (W * l)) & M32 for j, x in enumerate((a, b, c, d, e, f, g, h))] for l in range(L)]
        return keys, full, probes


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
        refs = [compress31(IV, [(draws[i] >> (W * l)) & M32 for i in range(16)]) for l in range(L)]
        bitmap = {}
        for l in range(4):                       # synthetic table: the scalar keys of lanes 0..3 only
            bitmap[refs[l][0] >> 8] = bitmap.get(refs[l][0] >> 8, 0) | (1 << (refs[l][0] & 255))
        member = [1 if (bitmap.get(refs[l][0] >> 8, 0) >> (refs[l][0] & 255)) & 1 else 0 for l in range(L)]
        m = Swar()
        keys, full, probes = m.batch(draws, bitmap)
        ok_key = ok_full = ok_probe = 0
        for l in range(L):
            ok_key += keys[l] == refs[l][0]
            ok_full += full[l] == refs[l]
            ok_probe += probes[l] == member[l]
        obs = {"batch_ops": sum(m.c.values()), "lanes_key_eq_scalar": ok_key, "lanes_cv_eq_scalar": ok_full,
               "lanes_probe_correct": ok_probe, "registers": m.regs}
        obs.update({"ops_" + k: m.c[k] for k in CATS})
        row = {"trial": idx, "message_a_hex": None, "message_b_hex": None, "observations": obs}
        if idx < len(firsts):
            a, b = pair(firsts[idx])
            m0 = [int.from_bytes(a[4 * i:4 * i + 4], "big") for i in range(16)]
            obs["m0_from_online_key_stream"] = stream_lane(ONLINE_KEY, FOUND_BATCH, FOUND_LANE) == m0
            row["message_a_hex"], row["message_b_hex"] = a.hex(), b.hex()
        out.append(row)
    sys.stdout.write(json.dumps({"schema_version": 1, "trials": out}, sort_keys=True))


if __name__ == "__main__":
    main()
