"""Scaled end-to-end run of the grouped partial-evaluation birthday search.

Stdlib only. Organizer mode (default) reads one JSON request on stdin and writes
one JSON result. Each organizer trial runs the algorithm of proof.md Section 3
once, scaled to N_t = 2^10 messages (proof.md Section 7):

  b3r2-grouped-spread:   32 groups x t = 0..31, key = mask on o0..o3, o5;
  b3r2-single-group:      1 group  x t = 0..1023, key = mask on o0..o3, o5;
  b3r2-grouped-fullword: 32 groups x t = 0..31, key = mask on all of o0..o7.

A group draws U0 (m0..m7) and U1 (m8..m14) from SHA-256 of (domain, seed, group
index); a message is (m0..m14, m15) with m15 = (t - S) mod 2^32, where
S = a3h + b4h is the group constant of proof.md Section 2, so t is the round-1
state word a3'. Digest words come only from the seven-way SWAR evaluator
`packed_body` (proof.md Section 4). It returns packed o0..o3, o5 fields, and
o4, o6, o7 are never computed. In the evidence-only full mode
(b3r2-grouped-fullword) it also performs the three skipped final b rotations and
returns all eight words with the scalar evaluator; the counted hot path never
uses this mode.

The table is the sparse-set step of proof.md Section 5, executed by the
operation-counting function `table_step`, over a memory whose unwritten words
are adversarial garbage: about half of them carry a pointer field equal to a
genuinely written dense entry (proof.md Lemma 4). Group records live at 4g+1,
4g+2, 4g+3 and the sparse array at SB = 2^160 + key, as in proof.md Section 5;
the full mode uses 2^256 + key (its key has 256 bits; evidence only). On a key
match both messages are rebuilt from the stored records and re-hashed with an
independent reference compression (compress2); the pair is returned when the
messages differ and the masked digest bits agree. A failed trial returns two
nulls. Observations (untrusted) include the counted operations of the first
seven-message batch's body and key extraction, and the extreme table-step counts.

Local mode (not used by the organizer):
  python3 FILE --selftest CASES SEED   counted evaluators vs compress2 (expect
                                       scalar 202+8; packed batch 227+101),
                                       counted group setup, and counted table
                                       steps under adversarial garbage (12/9/8)
"""

import hashlib
import json
import struct
import sys

M = 0xFFFFFFFF
W = (1 << 256) - 1
LANES = 7
STRIDE = 36
PM = sum(M << (STRIDE * j) for j in range(LANES))
RM = {r: sum(((1 << (32 - r)) - 1) << (STRIDE * j) for j in range(LANES))
      for r in (7, 8, 12, 16)}
LM = {r: sum((((1 << r) - 1) << (32 - r)) << (STRIDE * j) for j in range(LANES))
      for r in (7, 8, 12, 16)}
MC = ((1 << 128) - 1) << 32          # pointer field, bits 32..159
SB = 1 << 160                        # sparse-array base (proof.md Section 5)
INC = 1 << 32
IV = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
      0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)
PERM = (2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8)
LAYOUT = {"b3r2-grouped-spread": (32, 32, False), "b3r2-single-group": (1, 1024, False),
          "b3r2-grouped-fullword": (32, 32, True)}
KEY_WORDS = (0, 1, 2, 3, 5)          # digest words packed into the counted key


def ror(z, r):
    return ((z >> r) | (z << (32 - r))) & M


def ror_lazy(z, r):
    """Rotate the low 32 bits while allowing harmless garbage above bit 31.

    The double shift truncates the right-shifted arm to the low 32-bit lane.
    The result's low 32 bits are the desired rotation; callers delay the final
    mask until the five digest words used by the key are formed.
    """
    low = z << 224
    if isinstance(low, int):
        low &= W  # Python emulation of the 256-bit machine's shift truncation.
    return (low >> (224 + r)) | (z << (32 - r))


def g(a, b, c, d, x, y):
    a = (a + b + x) & M; d = ror(d ^ a, 16); c = (c + d) & M; b = ror(b ^ c, 12)
    a = (a + b + y) & M; d = ror(d ^ a, 8); c = (c + d) & M; b = ror(b ^ c, 7)
    return a, b, c, d


def compress2(m):
    """Independent reference: digest words o0..o7 of the 2-round root compression
    of one 64-byte block (IV chaining value, counter 0, length 64, flags 11)."""
    v = list(IV) + list(IV[:4]) + [0, 0, 64, 11]
    for _ in (0, 1):
        for (a, b, c, d), i in zip(((0, 4, 8, 12), (1, 5, 9, 13), (2, 6, 10, 14), (3, 7, 11, 15),
                                    (0, 5, 10, 15), (1, 6, 11, 12), (2, 7, 8, 13), (3, 4, 9, 14)),
                                   range(0, 16, 2)):
            v[a], v[b], v[c], v[d] = g(v[a], v[b], v[c], v[d], m[i], m[i + 1])
        m = [m[i] for i in PERM]
    return [v[i] ^ v[i + 8] for i in range(8)]


def unpack(U0, U1):
    """m0..m14 from the two group words (m0 = U0 & M, m_i = (U0 >> 32i) & M, ...)."""
    return [(U0 >> (32 * i)) & M if i else U0 & M for i in range(8)] + \
           [(U1 >> (32 * i)) & M if i else U1 & M for i in range(7)]


def setup(m):
    """Group constants (proof.md Section 2) from m0..m14."""
    v = list(IV) + list(IV[:4]) + [0, 0, 64, 11]
    calls = ((0, 4, 8, 12), (1, 5, 9, 13), (2, 6, 10, 14), (3, 7, 11, 15),
             (0, 5, 10, 15), (1, 6, 11, 12), (2, 7, 8, 13))
    for (a, b, c, d), i in zip(calls, range(0, 14, 2)):
        v[a], v[b], v[c], v[d] = g(v[a], v[b], v[c], v[d], m[i], m[i + 1])
    a3h = (v[3] + v[4] + m[14]) & M
    d14 = ror(v[14] ^ a3h, 16)
    c9 = (v[9] + d14) & M
    b4 = ror(v[4] ^ c9, 12)
    S = (a3h + b4) & M
    s = [m[i] if i != 15 else None for i in PERM]
    a1h = (v[1] + v[5] + s[2]) & M
    a2h = (v[2] + v[6] + s[4]) & M
    return {
        "S": S, "negS": (-S) & M, "d14": d14, "c9": c9, "b4": b4,
        "A0x": (v[0] + s[0]) & M, "d12": v[12], "c8": v[8], "s1": s[1],
        "d13h": ror(v[13] ^ a1h, 16), "b5": v[5], "A1y": (a1h + s[3]) & M,
        "a2h": a2h, "c10": v[10], "b6": v[6], "A2y": (a2h + s[5]) & M,
        "B7x": (v[7] + s[6]) & M, "d15": v[15], "c11": v[11], "b7": v[7], "s7": s[7],
        "s8": s[8], "s9": s[9], "s10": s[10], "s11": s[11], "s12": s[12], "s13": s[13], "s15": s[15],
    }


def body(K, R, full=False):
    """Per-message program of proof.md Section 4 (R = t + (g << 160)); returns
    o0, o1, o2, o3, o5. With full=True (evidence only, never counted) it also
    performs the three skipped final b rotations and returns o0..o7."""
    z = K["d14"] ^ R; d14 = ror_lazy(z, 8); c9 = K["c9"] + d14; z = K["b4"] ^ c9; b4 = ror_lazy(z, 7)
    a0 = K["A0x"] + b4
    z = K["d12"] ^ a0; d12 = ror_lazy(z, 16); c8 = K["c8"] + d12; z = b4 ^ c8; b4 = ror_lazy(z, 12)
    a0 = a0 + b4 + K["s1"]
    z = d12 ^ a0; d12 = ror_lazy(z, 8); c8 = c8 + d12; z = b4 ^ c8; b4 = ror_lazy(z, 7)
    c9 = c9 + K["d13h"]; z = K["b5"] ^ c9; b5 = ror_lazy(z, 12)
    a1 = K["A1y"] + b5
    z = K["d13h"] ^ a1; d13 = ror_lazy(z, 8); c9 = c9 + d13; z = b5 ^ c9; b5 = ror_lazy(z, 7)
    z = d14 ^ K["a2h"]; d14 = ror_lazy(z, 16); c10 = K["c10"] + d14; z = K["b6"] ^ c10; b6 = ror_lazy(z, 12)
    a2 = K["A2y"] + b6
    z = d14 ^ a2; d14 = ror_lazy(z, 8); c10 = c10 + d14; z = b6 ^ c10; b6 = ror_lazy(z, 7)
    a3 = R + K["B7x"]
    z = K["d15"] ^ a3; d15 = ror_lazy(z, 16); c11 = K["c11"] + d15; z = K["b7"] ^ c11; b7 = ror_lazy(z, 12)
    a3 = a3 + b7 + K["s7"]
    z = d15 ^ a3; d15 = ror_lazy(z, 8); c11 = c11 + d15; z = b7 ^ c11; b7 = ror_lazy(z, 7)
    # diagonal G(0,5,10,15): complete (b5 is kept for o5)
    a0 = a0 + b5 + K["s8"]; z = d15 ^ a0; d15 = ror_lazy(z, 16); c10 = c10 + d15; z = b5 ^ c10; b5 = ror_lazy(z, 12)
    a0 = a0 + b5 + K["s9"]; z = d15 ^ a0; d15 = ror_lazy(z, 8); c10 = c10 + d15; z = b5 ^ c10; b5 = ror_lazy(z, 7)
    # diagonals G(1,6,11,12) and G(2,7,8,13): final b rotation skipped (counted mode)
    a1 = a1 + b6 + K["s10"]; z = d12 ^ a1; d12 = ror_lazy(z, 16); c11 = c11 + d12; z = b6 ^ c11; b6 = ror_lazy(z, 12)
    a1 = a1 + b6 + K["s11"]; z = d12 ^ a1; d12 = ror_lazy(z, 8); c11 = c11 + d12
    a2 = a2 + b7 + K["s12"]; z = d13 ^ a2; d13 = ror_lazy(z, 16); c8 = c8 + d13; z = b7 ^ c8; b7 = ror_lazy(z, 12)
    a2 = a2 + b7 + K["s13"]; z = d13 ^ a2; d13 = ror_lazy(z, 8); c8 = c8 + d13
    # diagonal G(3,4,9,14): x = m15 = t - S, so a3 + b4 + m15 = a3 + b4 + R + negS
    a3 = a3 + b4 + R + K["negS"]; z = d14 ^ a3; d14 = ror_lazy(z, 16); c9 = c9 + d14; z = b4 ^ c9; b4 = ror_lazy(z, 12)
    a3 = a3 + b4 + K["s15"]; z = d14 ^ a3; d14 = ror_lazy(z, 8); c9 = c9 + d14
    if not full:
        return (a0 ^ c8) & M, (a1 ^ c9) & M, (a2 ^ c10) & M, (a3 ^ c11) & M, (b5 ^ d13) & M
    b6 = ror_lazy(b6 ^ c11, 7); b7 = ror_lazy(b7 ^ c8, 7); b4 = ror_lazy(b4 ^ c9, 7)
    return tuple(x & M for x in (a0 ^ c8, a1 ^ c9, a2 ^ c10, a3 ^ c11,
                                 b4 ^ d12, b5 ^ d13, b6 ^ d14, b7 ^ d15))


def broadcast(x):
    """Seven copies of one 32-bit value in 36-bit fields."""
    return sum(x << (STRIDE * j) for j in range(LANES))


def pack_lanes(xs):
    """Pack at most seven 32-bit lane values; omitted high lanes are zero."""
    return sum((x & M) << (STRIDE * j) for j, x in enumerate(xs))


def packed_constants(K):
    return {name: broadcast(value) for name, value in K.items() if name != "S"}


def padd2(a, b):
    return a + b


def padd3(a, b, c):
    return a + b + c


def padd4(a, b, c, d):
    return a + b + c + d


def pror(z, r):
    """Rotate each of seven 32-bit fields, preserving the two guard bits."""
    return ((z >> r) & RM[r]) | ((z << (32 - r)) & LM[r])


def packed_body(K, T):
    """Seven-way SWAR form of the counted five-output body."""
    z = K["d14"] ^ T; d14 = pror(z, 8); c9 = padd2(K["c9"], d14); z = K["b4"] ^ c9; b4 = pror(z, 7)
    a0 = padd2(K["A0x"], b4)
    z = K["d12"] ^ a0; d12 = pror(z, 16); c8 = padd2(K["c8"], d12); z = b4 ^ c8; b4 = pror(z, 12)
    a0 = padd3(a0, b4, K["s1"])
    z = d12 ^ a0; d12 = pror(z, 8); c8 = padd2(c8, d12); z = b4 ^ c8; b4 = pror(z, 7)
    c9 = padd2(c9, K["d13h"]); z = K["b5"] ^ c9; b5 = pror(z, 12)
    a1 = padd2(K["A1y"], b5)
    z = K["d13h"] ^ a1; d13 = pror(z, 8); c9 = padd2(c9, d13); z = b5 ^ c9; b5 = pror(z, 7)
    z = d14 ^ K["a2h"]; d14 = pror(z, 16); c10 = padd2(K["c10"], d14); z = K["b6"] ^ c10; b6 = pror(z, 12)
    a2 = padd2(K["A2y"], b6)
    z = d14 ^ a2; d14 = pror(z, 8); c10 = padd2(c10, d14); z = b6 ^ c10; b6 = pror(z, 7)
    a3 = padd2(T, K["B7x"])
    z = K["d15"] ^ a3; d15 = pror(z, 16); c11 = padd2(K["c11"], d15); z = K["b7"] ^ c11; b7 = pror(z, 12)
    a3 = padd3(a3, b7, K["s7"])
    z = d15 ^ a3; d15 = pror(z, 8); c11 = padd2(c11, d15); z = b7 ^ c11; b7 = pror(z, 7)
    a0 = padd3(a0, b5, K["s8"]); z = d15 ^ a0; d15 = pror(z, 16); c10 = padd2(c10, d15); z = b5 ^ c10; b5 = pror(z, 12)
    a0 = padd3(a0, b5, K["s9"]); z = d15 ^ a0; d15 = pror(z, 8); c10 = padd2(c10, d15); z = b5 ^ c10; b5 = pror(z, 7)
    a1 = padd3(a1, b6, K["s10"]); z = d12 ^ a1; d12 = pror(z, 16); c11 = padd2(c11, d12); z = b6 ^ c11; b6 = pror(z, 12)
    a1 = padd3(a1, b6, K["s11"]); z = d12 ^ a1; d12 = pror(z, 8); c11 = padd2(c11, d12)
    a2 = padd3(a2, b7, K["s12"]); z = d13 ^ a2; d13 = pror(z, 16); c8 = padd2(c8, d13); z = b7 ^ c8; b7 = pror(z, 12)
    a2 = padd3(a2, b7, K["s13"]); z = d13 ^ a2; d13 = pror(z, 8); c8 = padd2(c8, d13)
    a3 = padd4(a3, b4, T, K["negS"]); z = d14 ^ a3; d14 = pror(z, 16); c9 = padd2(c9, d14); z = b4 ^ c9; b4 = pror(z, 12)
    a3 = padd3(a3, b4, K["s15"]); z = d14 ^ a3; d14 = pror(z, 8); c9 = padd2(c9, d14)
    return a0 ^ c8, a1 ^ c9, a2 ^ c10, a3 ^ c11, b5 ^ d13


def target_key_masks(base=M):
    """Masks at the five scalar-key destinations (four charged shifts)."""
    return [base] + [base << d for d in (32, 64, 96, 128)]


def extract_keys(o, masks=None):
    """Extract each lane directly into its five scalar-key destinations."""
    masks = target_key_masks() if masks is None else masks
    keys = []
    for lane in range(LANES):
        source = STRIDE * lane
        pieces = []
        for x, dest, mask in zip(o, (0, 32, 64, 96, 128), masks):
            y = x >> (source - dest) if source > dest else \
                (x << (dest - source) if source < dest else x)
            pieces.append(y & mask)
        keys.append(pieces[0] | pieces[1] | pieces[2] | pieces[3] | pieces[4])
    return keys


def pack(o):
    """Counted key: o0 | o1<<32 | o2<<64 | o3<<96 | o5<<128 (8 operations)."""
    return o[0] | (o[1] << 32) | (o[2] << 64) | (o[3] << 96) | (o[4] << 128)


def key_masks(mask_hex):
    """(mask on the packed 5-word key or None, mask on the packed 8-word digest, words)."""
    words = struct.unpack("<8I", bytes.fromhex(mask_hex))
    k8 = sum(w << (32 * i) for i, w in enumerate(words))
    k5 = None if any(words[i] for i in (4, 6, 7)) else sum(words[w] << (32 * j) for j, w in enumerate(KEY_WORDS))
    return k5, k8, words


def group_words(seed, gi):
    h = hashlib.sha256(b"b3r2-grouped-v1" + seed + gi.to_bytes(4, "little")).digest()
    h += hashlib.sha256(b"b3r2-grouped-v1" + seed + gi.to_bytes(4, "little") + b"\x01").digest()
    w = struct.unpack("<16I", h)
    U0 = sum(w[i] << (32 * i) for i in range(8))
    U1 = sum(w[8 + i] << (32 * i) for i in range(7))
    return U0, U1


class Memory:
    """Never-initialised memory. An unwritten word reads as seed-derived garbage;
    for about half of the unwritten addresses (once a record exists) the garbage
    carries, in bits 32..159, the address of a genuinely written dense entry."""
    def __init__(self, seed):
        self.seed, self.cells, self.stale = seed, {}, 0

    def load(self, a, CC=0):
        if a in self.cells:
            return self.cells[a]
        h = hashlib.sha256(b"garbage" + self.seed + a.to_bytes(33, "little")).digest()
        x = int.from_bytes(h, "little")
        if CC >= INC and h[0] & 1:
            j = int.from_bytes(hashlib.sha256(b"stale" + h).digest(), "little") % (CC >> 32)
            x = (x & ~MC) | (j << 32)
            self.stale += 1
        return x

    def store(self, a, v):
        self.cells[a] = v


def table_step(mem, key, sbase, R, CC):
    """Sparse-set step of proof.md Section 5, with its operations counted exactly
    as listed there. Returns (matched, w, CC, ops)."""
    ops = 0
    sa = key | sbase; ops += 1                     # OR
    w = mem.load(sa, CC); ops += 1                 # load
    p = w & MC; ops += 1                           # AND
    ops += 2                                       # compare p < CC, branch
    if p < CC:
        q = mem.load(p, CC); ops += 1              # load
        ops += 2                                   # compare q == key, branch
        if q == key:
            return True, w, CC, ops                # MATCH: 8
    mem.store(sa, R | CC); ops += 2                # OR, store
    mem.store(CC, key); ops += 1                   # store
    CC = CC + INC; ops += 1                        # add
    return False, w, CC, ops                       # 12 or 9


class V:
    """Counting word: every operation with a V operand is counted once."""
    n = 0

    def __init__(self, x): self.x = x

    def _op(self, f, o):
        V.n += 1
        return V(f(self.x, o.x if isinstance(o, V) else o) & ((1 << 256) - 1))

    def __add__(self, o): return self._op(lambda a, b: a + b, o)
    __radd__ = __add__
    def __xor__(self, o): return self._op(lambda a, b: a ^ b, o)
    __rxor__ = __xor__
    def __and__(self, o): return self._op(lambda a, b: a & b, o)
    __rand__ = __and__
    def __or__(self, o): return self._op(lambda a, b: a | b, o)
    __ror__ = __or__
    def __rshift__(self, k): return self._op(lambda a, b: a >> b, k)
    def __lshift__(self, k): return self._op(lambda a, b: a << b, k)
    def __neg__(self): return self._op(lambda a, b: -a, 0)


def counted_body_key(K, R):
    V.n = 0
    o = body(K, V(R))
    nb = V.n
    k = pack(o)
    return k.x, nb, V.n - nb


def counted_packed_body_keys(K, ts):
    """Count one seven-way body and extraction of all seven scalar keys."""
    V.n = 0
    o = packed_body(packed_constants(K), V(pack_lanes(ts)))
    nb = V.n
    masks = target_key_masks(V(M))
    keys = extract_keys(o, masks)
    return [k.x for k in keys], nb, V.n - nb


def trial(seed, groups, per_group, full, k5, k8, wmask):
    mem = Memory(seed)
    CC = 0
    msgs = verifications = 0
    tmin, tmax = 99, 0
    obs = {}
    sbase = (1 << 256) if full else SB
    for gi in range(groups):
        U0, U1 = group_words(seed, gi)
        m = unpack(U0, U1)
        K = setup(m)
        PK = packed_constants(K)
        mem.store(4 * gi + 1, U0)                  # group record: 4g+1, 4g+2, 4g+3
        mem.store(4 * gi + 2, U1)
        mem.store(4 * gi + 3, K["S"])
        G, R = gi << 160, gi << 160
        for base in range(0, per_group, LANES):
            active = min(LANES, per_group - base)
            ts = list(range(base, base + active))
            if full:
                keys = [sum(w << (32 * i) for i, w in enumerate(body(K, G + t, True))) & k8 for t in ts]
            else:
                if msgs == 0:                      # counted run of the first packed batch
                    _, obs["first_packed_body_ops"], obs["first_extract_key_ops"] = \
                        counted_packed_body_keys(K, ts + [0] * (LANES - active))
                keys = [key & k5 for key in extract_keys(packed_body(PK, pack_lanes(ts)))]
            for key in keys[:active]:
                msgs += 1
                matched, w, CC, ops = table_step(mem, key, sbase, R, CC)
                tmin, tmax = min(tmin, ops), max(tmax, ops)
                if matched:
                    verifications += 1
                    tz, gz = w & M, w >> 160
                    mz = unpack(mem.load(4 * gz + 1), mem.load(4 * gz + 2)) + [(tz - mem.load(4 * gz + 3)) & M]
                    mx = m + [((R & M) + K["negS"]) & M]
                    dz, dx = compress2(mz), compress2(mx)
                    if mz != mx and all((dz[i] ^ dx[i]) & wmask[i] == 0 for i in range(8)):
                        obs.update(messages=msgs, verifications=verifications, table_ops_min=tmin,
                                   table_ops_max=tmax, stale_garbage_pointers=mem.stale)
                        return struct.pack("<16I", *mz).hex(), struct.pack("<16I", *mx).hex(), obs
                R += 1
    obs.update(messages=msgs, verifications=verifications, table_ops_min=tmin,
               table_ops_max=tmax, stale_garbage_pointers=mem.stale)
    return None, None, obs


def selftest(cases, seed):
    counts, packed_counts, packed_ok, full_ok, setup_ops = {}, {}, 0, 0, set()
    for c in range(cases):
        h = hashlib.sha256(b"selftest" + seed.to_bytes(8, "little") + c.to_bytes(8, "little")).digest() * 2
        words = struct.unpack("<16I", h)
        m, t, gi = list(words[:15]), words[15], int.from_bytes(h[:12], "little")
        K = setup(m)
        R = t + (gi << 160)
        k, nb, npk = counted_body_key(K, R)
        d = compress2(m + [(t - K["S"]) & M])
        assert k == pack([d[i] for i in KEY_WORDS]), c
        assert list(body(K, R, True)) == d, c
        full_ok += 1
        counts[(nb, npk)] = counts.get((nb, npk), 0) + 1
        if c < 200:
            V.n = 0
            KV = setup([V(x) for x in m])
            setup_ops.add(V.n)
            assert {n: (v.x if isinstance(v, V) else v) for n, v in KV.items() if n != "S"} == \
                   {n: v for n, v in K.items() if n != "S"}
        if c % LANES == 0:
            ts = []
            for j in range(LANES):
                hj = hashlib.sha256(h + j.to_bytes(1, "little")).digest()
                ts.append(int.from_bytes(hj[:4], "little"))
            keys, npb, npe = counted_packed_body_keys(K, ts)
            packed_counts[(npb, npe)] = packed_counts.get((npb, npe), 0) + 1
            for j, tj in enumerate(ts):
                dj = compress2(m + [(tj - K["S"]) & M])
                assert keys[j] == pack([dj[i] for i in KEY_WORDS]), (c, j)
                packed_ok += 1
    # table steps under adversarial garbage: scaled runs with a 12-bit key
    tcounts, agree = {}, 0
    for r in range(100):
        mem, CC, seen, R = Memory(b"tbl" + r.to_bytes(4, "little")), 0, {}, 0
        for i in range(256):
            key = int.from_bytes(hashlib.sha256(b"k" + r.to_bytes(4, "little") + i.to_bytes(4, "little")).digest()[:2], "little") & 0xFFF
            matched, w, CC, ops = table_step(mem, key, SB, R, CC)
            tcounts[ops] = tcounts.get(ops, 0) + 1
            if matched != (key in seen) or (matched and w != seen[key]):
                raise AssertionError("table semantics")
            if not matched:
                seen[key] = R | (CC - INC)
            R += 1
        agree += 1
    print(json.dumps({"cases": cases, "body_key_op_counts": {"%d,%d" % kk: n for kk, n in counts.items()},
                      "packed_body_extract_op_counts": {"%d,%d" % kk: n for kk, n in packed_counts.items()},
                      "packed_lanes_equal_reference": packed_ok,
                      "full_mode_equals_reference": full_ok, "setup_ops_counted": sorted(setup_ops),
                      "table_runs_ok": agree, "table_op_counts": {str(kk): n for kk, n in sorted(tcounts.items())}}))


def main():
    if len(sys.argv) == 4 and sys.argv[1] == "--selftest":
        selftest(int(sys.argv[2]), int(sys.argv[3]))
        return
    request = json.load(sys.stdin)
    if request["schema_version"] != 1 or request["target_profile"] != "blake3-r2-prefix-v1":
        raise ValueError("unexpected organizer target")
    event = request["event"]
    if event.get("kind") != "digest-xor-mask" or int(event["expected_hex"], 16) != 0:
        raise ValueError("unexpected organizer event")
    groups, per_group, full = LAYOUT[request["experiment_id"]]
    k5, k8, wmask = key_masks(event["mask_hex"])
    if not full and k5 is None:
        raise ValueError("counted-key experiments need a mask inside o0..o3, o5")
    rows = []
    for item in request["trials"]:
        first, second, obs = trial(bytes.fromhex(item["seed"]), groups, per_group, full, k5, k8, wmask)
        rows.append({"trial": item["trial"], "message_a_hex": first, "message_b_hex": second,
                     "observations": obs})
    json.dump({"schema_version": 1, "trials": rows}, sys.stdout, separators=(",", ":"), sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
