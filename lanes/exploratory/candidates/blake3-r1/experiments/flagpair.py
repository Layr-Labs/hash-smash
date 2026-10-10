"""1-round BLAKE3: a 1,088-byte message B and a 64-byte message A with equal digests.

Implements steps 1 to 3 of the algorithm of proof.md Section 3 for a given
1,088-byte B: the 17 chunk compressions of B, then A from the parent words by
Lemma 1. Trial 0 applies them to the B of the first published pair of this
construction (A comes out as the bytes 00..3f); trial 1 is the algorithm's
output (B = 1,088 zero bytes); every other trial uses a B expanded from its
organizer seed with SHAKE-256. Standard library only; no OS randomness, wall
time or ambient state. The program evaluates chunk compressions only, not the
target hash: the organizer recomputes both digests.
"""

import hashlib
import json
import struct
import sys

M = 0xFFFFFFFF
IV = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
      0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)
K = 0x0130C253          # IV[3] + IV[7]: a + b before the column call G(3,7,11,15; m6, m7)
DELTA = 7               # 12 XOR 11: parent root flags against one-block root flags
CHUNK_START, CHUNK_END = 1, 2
CALLS = ((0, 4, 8, 12), (1, 5, 9, 13), (2, 6, 10, 14), (3, 7, 11, 15),
         (0, 5, 10, 15), (1, 6, 11, 12), (2, 7, 8, 13), (3, 4, 9, 14))

B_PUBLISHED = bytes.fromhex(
    "b4914dea6099f4256b92d24fea762d237f303b8d4de8561ad9ba0c14c12ec8f185986a7ab59ccaf88da74c3f6fdd15e4"
    "f7bb03b1341df772b7f94d12e50c0f04803b2879070165a13fa655650a359861676eeeee9026c2d292af421126bc634f"
    "3aee933d0e6e14b0570b5c548ebe02bf4fabf105149ad1851a8ad0641ed670c49eb319dfe9cd9ba371efad549fc627d7"
    "ec841e40a8755d5b822bb28dbbe1a0f95e72f47058d07090b07586a3135d242ecdd301f8c3877b57c9d08433047f00be"
    "36f257528fa1932cf0c31e823d0c8e427647b139cd51fdc9811e98f5d0126a36f38766b47377dd30fab03b8b49bb5a70"
    "e70d870c5ade8d43c2da62e89035491b8ff25b2fb44116824453ea4d0bdd1af189de7e433bb4d4c65b65910083f9ea0f"
    "7b548aa24425fa27f2a0136e48d10617e01720410384618125f7923a1fd2417e7c14bd4a4638ca00455c373f9ec03dbb"
    "31c1195ac7056e3682d92b1b3b58d2eda4250e41c7ed1c5c93ea9b1e757cca971618db05cfaf0c025840a0c22462f8cd"
    "1c881a20e2180b66d98193cca7ce8404cb63d3d327be2637390e6afed14676fc85d26be0d5d70b8b46e1466f39aa33c0"
    "36e74594f929da0d4c21af6d4131fc7ce34f13017d22500a0d0863fe89dd75432fcdb41d0207db6a4e7d481fdbc13998"
    "26bfa7e341ed85b12e28c5c0e1529ee5e771698415afb1b15ca1b462291d33bc6dfa061a419b457db3d37f2f8690adfe"
    "a437a7ea9f56bd60e5423d64b0b0094da8393a3c3c3818bbf6527fa50feef434c563cdd352c45825de0e90a62ce12c2d"
    "84b3301063a6e453ee24bf7e7d42be9822d0b2339170fda66f9fd5412f0c5415be8595f7b306d7779be56bb1acb65569"
    "c171a6c1eae59fde17decd064d74ccc89f2d6041235724a10fe7c12885eaf680ebca704c0529da2de73f068f7d261187"
    "11ccd096228960bef54016d6f3172db3e2a33efa9aa72fd4afc2e7463fa024d4962f946158e135c8696a8d4274fa4434"
    "10c18bf330862943c7451ac0baaa53d782e57b5dc3b3abfd1aa7f60b1485526d1518335661864fceed9096ddb4044b3e"
    "14bd9041136c0f082e6f3f7be8ed6a03940ba4fa569a86366a927791c9f214c016c47fdb298eb4d093151c074842d29c"
    "aafc3222cfc6c48c08fdaa24a3d597511839402367add9e962160ba67cada4bc1d148795807335b99c69df2b842431b6"
    "50912ebbc2c55d2ba352513515909fa536d638d033547896b459298c7d79a8523ed28ad7952397d447dc22f0ab866452"
    "4670112949b9ff29145562137b1599811d757775c883d875f8e84491fb989ce8c21d4d2941bfa603f0cb0315ad8d8dad"
    "ac95ef50feeda7e69ab031454bf21884452f24f4a28bd8490f15b53581b54e5b2f9e41391998fe2d2f709ed138aa8068"
    "7d17af50bc720247e113424f5c2b81a4918f18847ec5d66634a90c09edd237e5ee6b47ff7cdd544b3d7f5e6e9e494b1e"
    "66eee9f3c5107231ced0b0fdf302125ca8b028a4395692e532f57a178ea48bd4")


def ror(x, n):
    return ((x >> n) | (x << (32 - n))) & M


def compress(cv, m, counter, flags):
    """Chaining value of one 1-round compression with block length 64."""
    v = list(cv) + list(IV[:4]) + [counter, 0, 64, flags]
    for i, (a, b, c, d) in enumerate(CALLS):
        x, y = m[2 * i], m[2 * i + 1]
        v[a] = (v[a] + v[b] + x) & M
        v[d] = ror(v[d] ^ v[a], 16)
        v[c] = (v[c] + v[d]) & M
        v[b] = ror(v[b] ^ v[c], 12)
        v[a] = (v[a] + v[b] + y) & M
        v[d] = ror(v[d] ^ v[a], 8)
        v[c] = (v[c] + v[d]) & M
        v[b] = ror(v[b] ^ v[c], 7)
    return [v[i] ^ v[i + 8] for i in range(8)]


def parent_words(words):
    """Step 1: the chaining values of B's two chunks, h_16 || g (272 words in)."""
    h = IV
    for k in range(16):
        flags = (CHUNK_START if k == 0 else 0) | (CHUNK_END if k == 15 else 0)
        h = compress(h, words[16 * k:16 * k + 16], 0, flags)
    return list(h) + compress(IV, words[256:272], 1, CHUNK_START | CHUNK_END)


def a_words(p):
    """Step 2 (Lemma 1, flags 12 -> 11): P with m6, m7 moved."""
    a1 = (K + p[6]) & M
    a1p = a1 ^ DELTA
    a = list(p)
    a[6] = (a1p - K) & M
    a[7] = (p[7] + a1 - a1p) & M
    return a


def pack(words):
    """Step 3: little-endian bytes, eight 32-bit words per 256-bit RAM word."""
    out = []
    for k in range(0, len(words), 8):
        acc = words[k]
        for j in range(1, 8):
            acc = acc | (words[k + j] << (32 * j))
        out.append(int(acc).to_bytes(32, "little"))
    return b"".join(out)


def build(b):
    return pack(a_words(parent_words(struct.unpack("<272I", b)))), b


def main():
    request = json.load(sys.stdin)
    if request["schema_version"] != 1 or request["target_profile"] != "blake3-r1-prefix-v1":
        raise ValueError("unexpected organizer target")
    if request["event"] != {"kind": "full-collision"}:
        raise ValueError("unexpected organizer event")
    trials = []
    for trial in request["trials"]:
        t = trial["trial"]
        b = B_PUBLISHED if t == 0 else bytes(1088) if t == 1 else hashlib.shake_256(bytes.fromhex(trial["seed"])).digest(1088)
        a, b = build(b)
        trials.append({"trial": t, "message_a_hex": a.hex(), "message_b_hex": b.hex()})
    json.dump({"schema_version": 1, "trials": trials}, sys.stdout, separators=(",", ":"), sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
