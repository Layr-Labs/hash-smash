"""Reduced run of the campaign CAMP of proof.md Section 8 on the exact target sha3-256-r6-prefix-v1 (SHA3-256, prefix
rounds 0 to 5, zero state, rate 136 bytes, suffix 0x06, full 256-bit digest), with the organizer-executed reduced-width
tests of premise H_coset (proof.md Section 12.2). Python standard library only. Reads one organizer request (JSON) on
stdin and writes one JSON document on stdout.

Once per request: the 6-round hash below must match two known-answer digests of the organizer reference and, at 24
rounds, hashlib.sha3_256; rank(W40) = 40; all 780 basis-pair two-round polarizations of Lemma 3 must vanish.

Trials 256g .. 256g + 255 form one group: group index h = int(seed of the group's first trial, 16) mod G, trial k is
coset lane c = k mod 256, coset j = 256 h + c. Its origin t_j is fresh randomness of Section 6.1: the leader step
draws two random words (RAND, one charged primitive each) from the trial's own coins, here the two halves of
SHAKE-256 of the trial's seed; this seed expansion only makes the run reproducible and is not the attack's randomness
source. The group executes the schedule of Sections 5 to 7 at reduced size: the first 2^N_DIR Gray points of each
coset (directions w_0 .. w_{N_DIR-1}), degree bound 8, all 175 planes, the full 140-bit key and the tagged table of
Section 7. Every operation of those sections runs through the counting machine below (one call = one charged
256-bit primitive; no permutation call is made), and the program stops unless each executed count equals the formula
of proof.md: 11 per coset leader and 5 per group for control; the bit-sliced setup of Section 6.3 (all 256 lanes in
each word), 13616 per group for the transpose of the 256 origins into 320 bitplanes, and at every point S
640 + popcount(w(S)) for the input and the constant-folded generated code, 1978, 11659, 14735, 14733 and 14735 for
rounds 0 to 4 and 4230 for the round-5 linear step into the coefficient record; 4 * 175 per transform pair and
2 * 175 per phase term; the plane-major FES of Section 5.3 at every plane and Gray step and its closed sum per plane
(61 records in registers, values into the buffer, the last store of the other records omitted) with 2 per group for
the spill, every buffer word written once, 175 buffer reads per point i >= 1 and 175 loads at point zero, 4664 per
point for chi and transpose, 5 table operations per candidate at even e and 6 at odd e (1408 per point), 7660 for the
ten byte tables and 4 for one-time control; on a candidate path 68 for the stored pair (each second source word
masked to 64 bits), 17 for the current candidate (its i and e are immediates of its site), 67, 236, 242, 242, 242 and
242 for the six constant-folded rounds of each of the three messages, 3950 plus the comparisons, at most 3982
operations per candidate path. The bitplanes must equal the origins, and the counted
setup values must equal, at every point and lane, an independent evaluation that is not counted (rounds 0 and 1 by
Lemma 3). Table words start with arbitrary content: a never-written table word reads as a fixed pseudo-random
function of its address; one in 4096 holds the tag over a pair identifier, half of them of the group and half
arbitrary 128-bit values whose coset records were never written, so garbage candidate paths run on arbitrary record
contents (a never-written coset record reads as a fixed pseudo-random function of its address; such reads are
checked to occur on garbage paths only). Reading a never-written work word stops the program. Beside the algorithm (not
counted): at point i the message of lane i mod 256 is hashed natively and its 140 key bits, with bit 140 set, are
compared with the emitted key word (key_mismatch); after the run, the key of the first candidate is probed again (its
slot names pair 0) and the candidate path is run on it against candidate (0, 1), a member of that pair. Also beside the algorithm, by experiment id. fes-campaign-reduced: own_pairs16 counts the unordered pairs of the
trial's own 2^N_DIR candidates whose emitted keys agree on their low 16 bits (bits 0..3 of digest lanes 0..3); uniform
digests give C(512, 2)/2^16 = 1.996 per trial. hcoset-within16 and hcoset-cross16 (premise test): key bit 4z + x is
digest bit z of lane x (RC[5] cancels in an equality), so key bits 0..15 are the 16 bits of the manifest's event mask.
The group's pair counts pairs16_within (two points of one coset agreeing on key bits 0..15), pairs16_cross and
pairs24_cross (points of two different cosets agreeing on key bits 0..15, resp. 0..23) must lie in the pass intervals
PASS of the manifest's hypotheses, or the program stops. hcoset-within16: trial k (lane c) returns the first two Gray
points of its own coset, in Gray order, whose keys agree on bits 0..15. hcoset-cross16: trial k returns the first Gray
point b >= 256 of the partner coset (lane c XOR 1) whose key agrees on bits 0..15 with a Gray point a < 256 of its own
coset, and that a. Different trials use disjoint message sets. Each returned pair is hashed natively and must agree on
the mask. These two report 13 of the group counts (buffer_reads and table_stores are checked, not reported) and the
three pair counts. Nothing about cost is inferred from a run.
"""
import sys, json, hashlib
from math import comb, isqrt

N_DIR, DEG, LANES, NPL = 9, 8, 256, 175
G = 1202250025869134545910402                    # groups of the full campaign (Section 9)
KCH = 19345871228983                             # Chebyshev parameter of the verification cap (Section 9)
M64, M128, M256 = (1 << 64) - 1, (1 << 128) - 1, (1 << 256) - 1
RC = (0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000, 0x000000000000808B,
      0x0000000080000001, 0x8000000080008081, 0x8000000000008009, 0x000000000000008A, 0x0000000000000088,
      0x0000000080008009, 0x000000008000000A, 0x000000008000808B, 0x800000000000008B, 0x8000000000008089,
      0x8000000000008003, 0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
      0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008)
RHO = (0, 1, 62, 28, 27, 36, 44, 6, 55, 20, 3, 10, 43, 25, 39, 41, 45, 15, 21, 8, 18, 2, 61, 56, 14)
W40 = [int(h, 16) for h in """
00000000000000000000000040000004100100000000000000002000200000000000000000000000
000000000000000000000000800200002000000a0000202000000001400000040000200000000800
00000000000000000000000200000020800800000000000000010001000000000000000000000000
00000000000000000000410010000104000100400000140000802000000000800000000040000010
00000000000000000000820000820000000000080082000000040001000040000000200000200820
00000000000000000020000000000000000000000000000000000000000004000000000000020800
00000000000000000100000010000000000000000040040000800000000000800000000000000000
00000000000000000800000000820000002000080000000000000001004004000000200000000800
00000000000000008000020000000000000000002080000000000000000000000000000000200020
00000000000000030000020010800100040000422082042000040000680040840000000040200020
00000000000000410000020000820100000000002082000000040009200040000000200040200020
00000000000008010041020012820500858000406892040010240000290040800000200040201020
00000000000100010000020000000004000100802080000000002010200040000000080000208020
00000000000200010000020010820101040040482082240000040001280040800000200040200820
00000000000400010001020010800100040000406082440000040000280040800000200040200020
00000000010000010041020010000100040000406092040000040000280040800000000040201020
00000000040000010000020010820100808000402882040010840000210040800000200040200020
00000000080000010041020010000100040000406010040000200000280000800000000040001020
00000000800000010000020000820000900000002082000010040000000040000000200000200020
00000001000000010000030010800100200000422082042000840000600040840000000040200030
00000004000000010000020010820100840000406082040000040000280040800000200040200020
00000080000000010041020010820500050000486092041000240021280040800000200040201020
00000100000000010001020010800100040000406082042000040000280040800000000040201020
00000200200000000000090000000000000000000000000000800000000000400000000000000000
00000400000000010000000000000100000000402000000000000000200000000000000040000020
00001000200000000000080010000104000100400000140000002000000002800000000040000000
00008000000000010000020002820004808108002882100010042100210040000000200000200020
00020000000000010001020010000100040000406080040000000000280000800000000040200020
00100000000000010000020000000004000000002080000000000000200040000000000000200020
004000000000000100000200108201000000004820c2040000840001200844800000200040220820
00800000000000010041020010820120040000406082040000040001280040800000200040201020
020000000000000100000200100001000020004020c2040000840000200040800000000040200020
04000000000000010000020000000000000000002080000000000000200000000000000040000020
08000000000040000400000002000104008100400000140000002100000002800000000040000000
40000000000000010000020010820100840000402882040010040000200040800000200040200020
0a8094012901484005004a005200842021a008000010000402000000000000000000000000000001
080090012801480104004a0052008400318008002000000000000000000000000000000000000020
08009001200048020400480012000001208009000000000000000000000080000000000000010000
0a0294052801480185014a0052028400b1a008000000000000001000000000000008000000000000
00001200040008000000010002000000000001000000000000000000000000400000000000000000
""".split()]
KAT = ((0, '75f9117eb56131a655b34d93115a9781b7899716653c9b79f80902a99e3399f6'),
       (W40[0] ^ W40[39], 'f3025c162a37654390d8b807a6970cbae2a22b8e745218666f323f572066b8f2'))


def need(cond, what):
    if not cond:
        raise SystemExit('check failed: ' + what)


# ---- reference SHA3-256 with prefix rounds (lane x + 5y, little-endian lanes); not counted ----
def keccak_f(L, rounds):
    L = list(L)
    for r in range(rounds):
        C = [L[x] ^ L[x + 5] ^ L[x + 10] ^ L[x + 15] ^ L[x + 20] for x in range(5)]
        D = [C[x - 1] ^ ((C[(x + 1) % 5] << 1 | C[(x + 1) % 5] >> 63) & M64) for x in range(5)]
        B = [0] * 25
        for i in range(25):
            x, y, s = i % 5, i // 5, RHO[i]
            v = L[i] ^ D[x]
            B[y + 5 * ((2 * x + 3 * y) % 5)] = (v << s | v >> (64 - s)) & M64
        L = [B[i] ^ (~B[i - i % 5 + (i + 1) % 5] & B[i - i % 5 + (i + 2) % 5]) for i in range(25)]
        L[0] ^= RC[r]
    return L


def sha3_256(msg, rounds=6):
    p = bytearray(msg) + b'\x06'
    p += bytes(-len(p) % 136)
    p[-1] |= 0x80
    L = [0] * 25
    for o in range(0, len(p), 136):
        for k in range(17):
            L[k] ^= int.from_bytes(p[o + 8 * k:o + 8 * k + 8], 'little')
        L = keccak_f(L, rounds)
    return b''.join(v.to_bytes(8, 'little') for v in L[:4])


def message(t):          # Lemma 1: the 135-byte message of parameter t (u_0..u_4 in lanes 0-4 and 10-14)
    u = t.to_bytes(40, 'little')
    return u + bytes(40) + u + bytes(15)


def lanes(t):            # the absorbed block of message(t), padding byte 135 = 0x86 included
    u = [(t >> 64 * k) & M64 for k in range(5)]
    return u + [0] * 5 + u + [0, 0x86 << 56] + [0] * 8


def rank(vs):
    piv = {}
    for v in vs:
        while v:
            b = v.bit_length() - 1
            if b not in piv:
                piv[b] = v
                break
            v ^= piv[b]
    return len(piv)


def setup_checks():
    for t, hx in KAT:
        m = message(t)
        need(sha3_256(m, 6).hex() == hx, 'known-answer digest')
        need(sha3_256(m, 24) == hashlib.sha3_256(m).digest(), '24-round SHA3-256 against hashlib')
    need(rank(W40) == 40, 'rank of W40')
    F0 = keccak_f(lanes(0), 2)
    F = [keccak_f(lanes(w), 2) for w in W40]
    n = 0
    for i in range(40):
        for j in range(i + 1, 40):
            G2 = keccak_f(lanes(W40[i] ^ W40[j]), 2)
            need(not any(a ^ b ^ c ^ d for a, b, c, d in zip(G2, F[i], F[j], F0)), 'polarization %d %d' % (i, j))
            n += 1
    need(n == 780, 'number of polarizations')


# ---- one-time preprocessing (ONCE): plane order, record index, masks, layout, generated-code decisions ----
WW = [(v & M256, v >> 256) for v in W40]         # two-word constants of w_0 .. w_39
PLANES = [(p % 5, p // 5) for p in range(NPL)]   # plane p = B[x, z]: x = p mod 5, z = p div 5 (z < 35)
MASK = {s: sum(((1 << s) - 1) << (2 * s * k) for k in range(128 // s)) for s in (1, 2, 4, 8, 16, 32, 64, 128)}
SUBS = sorted((S for S in range(1 << N_DIR) if S.bit_count() <= DEG), key=lambda S: (S.bit_count(), S))
IDX = {S: k for k, S in enumerate(SUBS)}
QR, NST = LANES << N_DIR, (1 << N_DIR) - 1       # candidates and Gray steps i = 1 .. NST of the reduced run
CSB, WB = 1 << 130, 1 << 131                     # coset record of coset j at CSB + 2j; work region. The tagged table
WF, INT, PL, TW = WB, WB + 512, WB + 656, WB + 976   # word of key word k (bit 140 set) is SPARSE[k]. Work:
INF = TW + 3                                     # working frames, 144 tile words, 320 bitplanes, 3 transpose words,
RB, DW, CW = INF + 320, INF + 8320, INF + 8640   # input words (bit z of lane l < 5 at INF + 64 l + z), the output of
ACO = CW + 5                                     # round r at RB + 1600 r + 64 l + z, D words, 5 wrap words; coefficient
TABB = ACO + NPL * len(SUBS)                     # record A[S] at ACO + 175 IDX[S] (current frame = A[{}]); derivative
TBY = TABB + NPL * len(SUBS)                     # record tab[T] at TABB + 175 IDX[T]; byte table (b, k) at
FCW, HSP, SPL = TBY + 2560, TBY + 2561, TBY + 2562   # TBY + 256 (2b + k); count F (Section 7), spill word of h, spill
XB = SPL + 22                                    # frame (16 + 6); buffer: plane p at Gray point i >= 1 at XB + NST p + i - 1
WEND = XB + NPL * NST
CACHED = list(range(1, 32)) + [32 | t for t in range(2, 32)]   # the 61 records held in registers (Section 5.3)
CSET = set(CACHED)


def cap(num, den):       # Section 9: r = ceil(mu), R = r + ceil(sqrt(K r)), K = KCH
    r = -(-num // den)
    s = isqrt(KCH * r)
    return r + s + (s * s < KCH * r)


def shapes(i):           # T_1 .. T_L of Gray step i
    T, sh = 0, []
    while i and len(sh) < DEG:
        b = i & -i
        T |= b
        i ^= b
        sh.append(T)
    return sh


def sc(n):               # Section 5.3: Sc = sum L + (2^n - 1 - 61) + 2 (sum L - (2^n - 1) - links of cached records)
    sl = sum(comb(n, k) * min(DEG, k) for k in range(1, n + 1))
    return sl + (1 << n) - 62 + 2 * (sl - (1 << n) + 1 - sum((1 << n - T.bit_length()) - 1 for T in CACHED))


def ulast(n):            # records with a FES store (|T| <= 7, max T <= n - 2) that are not cached
    return sum(comb(n - 1, k) for k in range(1, DEG)) - 61


# code generation: per Gray step the top T_L and the links T_{L-1} .. T_1, each flagged at its last update
# (i + 2^(max T + 1) >= 2^N_DIR: that STORE is not emitted), and the step's count of Section 5.3
SITES = [(sh[-1], [(T, i + (1 << T.bit_length()) > NST) for T in sh[-2::-1]])
         for i, sh in ((i, shapes(i)) for i in range(1, NST + 1))]
COST = [(top not in CSET) + sum(1 if T in CSET else 3 - last for T, last in ch) + 2 for top, ch in SITES]
FPLANE = 62 + sc(N_DIR) + NST - ulast(N_DIR)
need(sc(40) == 18760331006174 and ulast(40) == 19311426, 'Section 5.3 constants at n = 40')


def popsum(n):           # Section 6.3: sum of popcount(w(S)) over |S| <= 8; bit k of w(S) is set iff |S & B_k| is odd,
    s = 0                # B_k = {b < n : bit k of w_b is set}, m = |B_k|
    for k in range(320):
        m = sum(W40[b] >> k & 1 for b in range(n))
        s += sum(comb(m, j) * sum(comb(n - m, l) for l in range(DEG + 1 - j)) for j in range(1, DEG + 1, 2))
    return s


POP = popsum(N_DIR)
need(popsum(40) == 4592341856, 'Section 6.3 popcount sum at n = 40')


def image():             # code generation: tile stages 0..2 on key row 140 (local row 12) all ones and all else zero
    R = [0] * 16
    R[12] = M256
    for b in range(3):
        s = 1 << b
        for k in range(16):
            if not k & s:
                t = ((R[k] >> s) ^ R[k + s]) & MASK[s]
                R[k], R[k + s] = R[k] ^ t << s, R[k + s] ^ t
    need(not any(R[:8]) and all(R[8:]), 'image of the constant row in rows 8..15')
    return R


IMG = image()
MZ = 1 << 100                                    # allowance for garbage candidate paths (Section 9)
CAPF = cap(QR * (QR - 1), 1 << 141) + MZ         # candidate-path cap R = R140 + 2^100 (full-size formula)
GM = 0x9E3779B97F4A7C15F39CC0605CEDC8341082276BF3A27251F86C6A11D0C18E95   # odd multiplier of the garbage stand-in
J_D = sum(S.bit_count() for S in SUBS)
V_D = sum(comb(j, r) * comb(N_DIR - j, r) * sum(comb(r, k) for k in range(min(r, DEG - j) + 1))
          for j in range(1, DEG + 1) for r in range(min(j, N_DIR - j) + 1))

# ---- counting machine: every call is one charged 256-bit primitive of the current section ----
SECS = {s: [0] for s in ('once', 'leader', 'sgroup', 'spoint', 'transform', 'phase', 'zero', 'fes', 'buf', 'cht',
                          'table', 'verify', 'vcheck')}
K = SECS['once']
SPARSE, WRK, CREC, CALLS, GBASE, TAGW, UNW = {}, [], {}, [0], [0], [0], [0]


def sec(name):
    global K
    K = SECS[name]


def LDS(a):              # table word; a never-written one holds arbitrary content (a fixed function of its address):
    K[0] += 1            # one in 4096 holds the tag (a garbage candidate path) over a pair identifier of the group (half
    v = SPARSE.get(a)    # of them) or an arbitrary 128-bit identifier, whose coset records were never written (the other
    if v is None:        # half); the others a word whose high half differs from the tag
        x = (a * GM) & M256
        x ^= x >> 127
        if x >> 245 == 0:
            v = TAGW[0] | GBASE[0] + x % (QR // 2)
        elif x >> 244 == 0:
            v = TAGW[0] | x & M128
        else:
            v = x if x >> 128 != TAGW[0] >> 128 else x ^ 1 << 255
    return v


def STS(a, v): K[0] += 1; SPARSE[a] = v


def LDW(a):
    K[0] += 1
    v = WRK[a - WB]
    if v is None:
        raise SystemExit('check failed: read of a never-written work word')
    return v


def STW(a, v): K[0] += 1; WRK[a - WB] = v


def LDC(a):              # coset record; a never-written one (garbage identifiers only) holds arbitrary content, a fixed
    K[0] += 1            # pseudo-random 256-bit function of its address
    if a in CREC:
        return CREC[a]
    UNW[0] += 1
    x = (a * GM + GM) & M256
    return x ^ x >> 101


def STC(a, v): K[0] += 1; CREC[a] = v
def XOR(a, b): K[0] += 1; return a ^ b
def AND(a, b): K[0] += 1; return a & b
def OR(a, b): K[0] += 1; return a | b
def NOT(a): K[0] += 1; return a ^ M256
def ADD(a, b): K[0] += 1; return (a + b) & M256
def SUB(a, b): K[0] += 1; return (a - b) & M256
def SHL(a, s): K[0] += 1; return (a << s) & M256
def SHR(a, s): K[0] += 1; return a >> s
def EQ(a, b): K[0] += 1; return int(a == b)
def LT(a, b): K[0] += 1; return int(a < b)
def BR(f): K[0] += 1; return f != 0             # conditional branch on a nonzero register
def MOV(v): K[0] += 1; return v
def RAND(src): K[0] += 1; return next(src)       # one independent uniform random 256-bit word (the trial's coins)
# CALLS counts permutation calls: verification evaluates the six rounds in word operations, so it stays 0


def coins(seed):         # reproducible stand-in for fresh coins: SHAKE-256 of the trial's seed, two 256-bit words
    s = hashlib.shake_256(seed.encode()).digest(64)
    return iter((int.from_bytes(s[:32], 'little'), int.from_bytes(s[32:], 'little')))


# ---- Section 7: verification's six rounds as constant-folded scalar code (67, 236, 242, 242, 242, 79) ----
def rot(v, s):           # 64-bit rotation of a lane: 4
    return AND(OR(SHL(v, s), SHR(v, 64 - s)), M64)


def lanes5(w0, w1):      # 6: lanes 0..3 from w0, lane 4 is w1 itself (below 2^64: a record of the leader step, or masked
    return [AND(w0, M64), AND(SHR(w0, 64), M64), AND(SHR(w0, 128), M64), SHR(w0, 192), w1]   # on a candidate path)


class SGen:              # code generation: a lane is a constant (v,) known at generation time or a data register n;
    def __init__(s):     # an operation is emitted only when its result is not fixed by the constants
        s.n, s.code = 6, []

    def op(s, *o):
        s.n += 1
        s.code.append((o[0], s.n) + o[1:] + (0,) * (3 - len(o)))
        return s.n

    def x(s, a, b):      # XOR: two constants, a zero constant or v XOR v fold; else XOR (with an immediate)
        ca, cb = type(a) is tuple, type(b) is tuple
        if ca and cb:
            return (a[0] ^ b[0],)
        if a == (0,) or b == (0,):
            return b if a == (0,) else a
        if a == b:
            return (0,)
        return s.op('xi', b, a[0]) if ca else s.op('xi', a, b[0]) if cb else s.op('x', a, b)

    def rot(s, a, k):
        if type(a) is tuple:
            return ((a[0] << k | a[0] >> (64 - k)) & M64,) if k else a
        return s.op('r', a, k) if k else a

    def chi(s, a, b, c):  # a XOR (NOT b AND c); NOT of a lane is XOR with the immediate 2^64 - 1
        if type(b) is tuple and type(c) is tuple:
            return s.x(a, (~b[0] & c[0] & M64,))
        if c == (0,) or b == (M64,):
            return a
        if b == (0,):
            return s.x(a, c)
        if type(b) is tuple:
            return s.x(a, s.op('ai', c, ~b[0] & M64))
        nb = s.op('n', b)
        if c == (M64,):
            return s.x(a, nb)
        return s.x(a, s.op('ai', nb, c[0]) if type(c) is tuple else s.op('a', nb, c))

    def round(s, L, r):  # theta, rho, pi (rotation of a data lane 4), chi, iota
        C = []
        for x in range(5):
            v = L[x]
            for y in range(1, 5):
                v = s.x(v, L[x + 5 * y])
            C.append(v)
        D = [s.x(C[x - 1], s.rot(C[(x + 1) % 5], 1)) for x in range(5)]
        B = [None] * 25
        for i in range(25):
            x, y = i % 5, i // 5
            B[y + 5 * ((2 * x + 3 * y) % 5)] = s.rot(s.x(L[i], D[x]), RHO[i])
        A = [s.chi(B[i], B[i - i % 5 + (i + 1) % 5], B[i - i % 5 + (i + 2) % 5]) for i in range(25)]
        A[0] = s.x(A[0], (RC[r],))
        return A


def scode():             # lanes 0..4 in registers 2..6 (lanes 10..14 the same), 14 zero lanes, padding lane 16
    g, codes = SGen(), []
    L = [2, 3, 4, 5, 6] + [(0,)] * 5 + [2, 3, 4, 5, 6, (0,), (0x86 << 56,)] + [(0,)] * 8
    for r in range(6):
        g.code = []
        L = g.round(L, r)
        codes.append(g.code)
    live, kept = set(L[:4]), []
    for ins in reversed(codes[5]):
        t, d, a, b = ins
        if d in live:
            kept.append(ins)
            live.discard(d)
            live.add(a)
            if t in ('x', 'a'):
                live.add(b)
    codes[5] = kept[::-1]
    need(all(type(v) is int for v in L[:4]), 'digest lanes in registers')
    return codes, L[:4], g.n


SCODE, SOUT, SREG = scode()
SRND = (67, 236, 242, 242, 242, 79)


def srun(code, R):       # executes generated scalar code, one counted primitive per operation (a rotation is 4)
    for t, d, a, b in code:
        if t == 'x':
            R[d] = XOR(R[a], R[b])
        elif t == 'xi':
            R[d] = XOR(R[a], b)
        elif t == 'r':
            R[d] = rot(R[a], b)
        elif t == 'a':
            R[d] = AND(R[a], R[b])
        elif t == 'ai':
            R[d] = AND(R[a], b)
        else:
            R[d] = XOR(R[a], M64)


def rounds6(L):          # the six rounds on lanes 0..4; returns digest lanes 0..3
    R = [None] * (SREG + 1)
    R[2:7] = L
    for r in range(6):
        k0 = K[0]
        srun(SCODE[r], R)
        need(K[0] - k0 == SRND[r], 'folded round %d: %d operations' % (r, SRND[r]))
    return [R[v] for v in SOUT]


def leaders(seeds):      # Section 6.2: fresh origin t_j from two random words into the global record and the frame
    sec('leader')
    per, origins = [], []
    H8 = SHL(REGS['h'], 8)                       # group control (1 of 5): H8 = h << 8
    for c in range(LANES):
        k0 = K[0]
        src = coins(seeds[c])
        j = OR(H8, c)
        w0 = RAND(src)
        w1 = AND(RAND(src), M64)                 # t_j = w0 + w1 2^256, uniform on F_2^320
        a = ADD(SHL(j, 1), CSB)
        STC(a, w0)
        STC(ADD(a, 1), w1)
        STW(WF + 2 * c, w0)
        STW(WF + 2 * c + 1, w1)
        per.append(K[0] - k0)
        origins.append(w0 | w1 << 256)
    return per, origins


# ---- bit-sliced state: word 64 l + z holds bit z of lane l, bit c of the word for coset lane c ----
CIDX = [tuple(64 * (x + 5 * y) + z for y in range(5)) for x in range(5) for z in range(64)]
DIDX = [(64 * ((x - 1) % 5) + z, 64 * ((x + 1) % 5) + (z - 1) % 64) for x in range(5) for z in range(64)]
SRC = [None] * 1600                              # theta's D index fused with rho and pi
for _l in range(25):
    for _z in range(64):
        _x, _y = _l % 5, _l // 5
        SRC[64 * (_y + 5 * ((2 * _x + 3 * _y) % 5)) + (_z + RHO[_l]) % 64] = (64 * _l + _z, 64 * _x + _z)
CHI = [(o, o - o % 320 + (o + 64) % 320, o - o % 320 + (o + 128) % 320) for o in range(1600)]
IOTA = [[z for z in range(64) if RC[r] >> z & 1] for r in range(6)]
SRC_SEL = [SRC[64 * x + z] for x, z in PLANES]


def ref_round(A, r):     # reference round (not counted)
    C = [A[a] ^ A[b] ^ A[c] ^ A[d] ^ A[e] for a, b, c, d, e in CIDX]
    D = [C[a] ^ C[b] for a, b in DIDX]
    B = [A[s] ^ D[d] for s, d in SRC]
    A = [B[a] ^ (~B[b] & B[c]) for a, b, c in CHI]
    for z in IOTA[r]:
        A[z] ^= M256
    return A


def ref_values(P):       # reference (not counted): f(e_S) for all |S| <= 8 and all 256 lanes from the bitplanes P,
    def two(Pv):         # rounds 0 and 1 by Lemma 3 (F2 at S = {} and the Delta_b); S -> 175 plane words
        A = [0] * 1600
        A[0:320], A[640:960] = Pv, Pv
        for z in (57, 58, 63):
            A[1024 + z] = M256
        return ref_round(ref_round(A, 0), 1)
    S0 = two(P)
    DEL = [[a ^ b for a, b in zip(two([p ^ M256 if w >> k & 1 else p for k, p in enumerate(P)]), S0)]
           for w in W40[:N_DIR]]
    val = {}

    def dfs(S, A, last):
        B = A
        for r in (2, 3, 4):
            B = ref_round(B, r)
        C = [B[a] ^ B[b] ^ B[c] ^ B[d] ^ B[e] for a, b, c, d, e in CIDX]
        D = [C[a] ^ C[b] for a, b in DIDX]
        val[S] = [B[s] ^ D[d] for s, d in SRC_SEL]
        if S.bit_count() < DEG:
            for j in range(last + 1, N_DIR):
                dfs(S | 1 << j, [a ^ b for a, b in zip(A, DEL[j])], j)
    dfs(0, S0, -1)
    return val


# ---- Section 6.3: the counted bit-sliced setup, all 256 lanes of the group in every word ----
def tr64(src, dst, sh):  # 64 x 64 transpose, stages s = 1..32: rows 2..63 in registers, rows 0 and 1 in two fixed words
    R = [0, 0] + [LDW(a) for a in src[2:]]       # (load 66); then 66 to store, or 258 to shift by sh and OR into dst
    for k in (0, 1):
        STW(TW + k, LDW(src[k]))
    for b in range(6):
        s, m = 1 << b, MASK[1 << b]
        for k in range(64):
            if k & s:
                continue
            kk = k + s
            if k >= 2:                           # both rows in registers: 6
                t = AND(XOR(SHR(R[k], s), R[kk]), m)
                R[k], R[kk] = XOR(R[k], SHL(t, s)), XOR(R[kk], t)
            elif kk >= 2:                        # row k in its word: 8
                u = LDW(TW + k)
                t = AND(XOR(SHR(u, s), R[kk]), m)
                R[kk] = XOR(R[kk], t)
                STW(TW + k, XOR(u, SHL(t, s)))
            else:                                # rows 0 and 1, two scratch registers and one spill word: 12
                u, v = LDW(TW), LDW(TW + 1)
                STW(TW + 2, u)
                t = AND(XOR(SHR(u, s), v), m)
                STW(TW + 1, XOR(v, t))
                t = SHL(t, s)
                STW(TW, XOR(LDW(TW + 2), t))
    for k in range(64):
        v = R[k] if k >= 2 else LDW(TW + k)
        STW(dst[k], OR(LDW(dst[k]), SHL(v, sh)) if sh else v)


def transpose():         # the 256 origins into the 320 bitplanes (bit c of plane k = bit k of t_j, j = 256 h + c): 13616
    for g in range(4):   # first words: four 64-row blocks (stages 0..5), then stages 6 and 7 on word pairs (10 each)
        tr64([WF + 2 * c for c in range(64 * g, 64 * g + 64)], range(PL + 64 * g, PL + 64 * g + 64), 0)
    for s in (64, 128):
        for k in range(256):
            if not k & s:
                u, v = LDW(PL + k), LDW(PL + k + s)
                t = AND(XOR(SHR(u, s), v), MASK[s])
                STW(PL + k, XOR(u, SHL(t, s)))
                STW(PL + k + s, XOR(v, t))
    for g in range(4):   # second words (below 2^64): four 64 x 64 blocks, block g shifted by 64 g into planes 256..319
        tr64([WF + 2 * c + 1 for c in range(64 * g, 64 * g + 64)], range(PL + 256, PL + 320), 64 * g)


def load_input(w):       # point S: plane k, NOT where bit k of w(S) is set, into bit k mod 64 of lane k div 64: 640 + pop
    for k in range(320):
        v = LDW(PL + k)
        STW(INF + k, NOT(v) if w >> k & 1 else v)


# Constant-folded rounds 0..4 and round-5 linear step, generated once (Section 11.2). Generation tracks each of the
# 1600 state words as a known constant, 0 (the zero word) or 1 (the all-ones word), or a data word n >= 2, and emits an
# operation only when its result is not fixed: XOR with 0, AND with 1 and v XOR v fold, XOR with 1 is one NOT, AND
# with 0 is 0. The pattern is the same at every point (w(S) only inverts data words), so one code serves all points.
# Round 0 reads lanes 10..14 from the words of lanes 0..4 (equal in every block A(t)); lane 16 (padding) and the
# zero lanes are constants. Code: (0, n, a, 0) LOAD; (1, a, n, 0) STORE; (2, n, u, v) XOR; (3, n, u, v) AND;
# (4, n, u, 0) NOT; (5, p, n, 0) STORE into word p of the record A[S]. Registers 0 and 1 hold the constants.
class Gen:
    def __init__(s, n):
        s.n, s.code = n, []

    def x(s, a, b):
        if a < 2 and b < 2:
            return a ^ b
        if a == 0 or b == 0:
            return b if a == 0 else a
        if a == b:
            return 0
        s.n += 1
        s.code.append((4, s.n, b, 0) if a == 1 else (4, s.n, a, 0) if b == 1 else (2, s.n, a, b))
        return s.n

    def a(s, a, b):
        if a < 2 and b < 2:
            return a & b
        if a == 0 or b == 0:
            return 0
        if a == 1 or b == 1:
            return b if a == 1 else a
        s.n += 1
        s.code.append((3, s.n, a, b))
        return s.n

    def nt(s, a):
        if a < 2:
            return 1 - a
        s.n += 1
        s.code.append((4, s.n, a, 0))
        return s.n


def bgen(g, st, mem, r):  # code of round r (r = 5: theta, rho, pi into the record); st[l][z] is the state, mem the
    C, D, pc, dc = [[0] * 64 for _ in range(5)], [[0] * 64 for _ in range(5)], [], []    # address of each data word
    for z in range(64):  # theta parities of slice z: each data word LOADed once in the slice
        g.code, have = [], set()
        for x in range(5):
            v = None
            for y in range(5):
                t = st[x + 5 * y][z]
                if t > 1 and t not in have:
                    have.add(t)
                    g.code.append((0, t, mem[t], 0))
                v = t if v is None else g.x(v, t)
            C[x][z] = v
        pc.append(g.code)
    for z in range(64):  # D[x][z] = C[x - 1][z] XOR C[x + 1][z - 1]
        g.code = []
        for x in range(5):
            D[x][z] = g.x(C[x - 1][z], C[(x + 1) % 5][z - 1])
        dc.append(g.code)
    cc, dd = all(v < 2 for c in C for v in c), all(v < 2 for d in D for v in d)
    need(dd or not cc, 'constant parities give constant D words')
    code, dad = [], {}
    if not cc:           # slice 63 first, its data parities stored and reloaded for D[.][63] (the wrap); data D stored
        wrap = [x for x in range(5) if C[x][63] > 1]
        code += pc[63] + [(1, CW + x, C[x][63], 0) for x in wrap]
        for z in range(64):
            code += pc[z] if z < 63 else [(0, C[x][63], CW + x, 0) for x in wrap]
            if not dd:
                code += dc[z]
                for x in range(5):
                    if D[x][z] > 1 and D[x][z] not in dad:
                        dad[D[x][z]] = DW + 64 * x + z
                        code.append((1, DW + 64 * x + z, D[x][z], 0))
    if r == 5:           # slice-fused linear step: only the 301 needed C[x][z] are formed, and plane p = (x, z)
        plane_at = {(x, (z - RHO[6 * x]) % 64): p for p, (x, z) in enumerate(PLANES)}
        needed_c = {((x - 1) % 5, vz) for x, vz in plane_at} | {((x + 1) % 5, (vz - 1) % 64) for x, vz in plane_at}
        C, pc = [[0] * 64 for _ in range(5)], []
        for z in range(64):
            g.code = []
            for x in range(5):
                if (x, z) in needed_c:
                    v = None
                    for y in range(5):
                        t = st[x + 5 * y][z]
                        g.code.append((0, t, mem[t], 0))
                        v = t if v is None else g.x(v, t)
                    C[x][z] = v
            pc.append(g.code)
        code = list(pc[63])
        for z in range(64):
            if z < 63:
                code += pc[z]
            g.code = []
            for x in range(5):
                p = plane_at.get((x, z))
                if p is not None:
                    s = st[6 * x][z]
                    if (x, z) not in needed_c:
                        g.code.append((0, s, mem[s], 0))
                    d = g.x(C[x - 1][z], C[(x + 1) % 5][z - 1])
                    v = g.x(s, d)
                    g.code.append((5, p, v, 0))
            code += g.code
        return code, None
    nxt, new = [[0] * 64 for _ in range(25)], {}
    for z in range(64):  # output slice z: sources and D words LOADed once each, theta-rho-pi, chi, iota, new data STOREd
        g.code, have, B = [], set(), [0] * 25
        for i in range(25):
            x, y, vz = i % 5, i // 5, (z - RHO[i]) % 64
            s, d = st[i][vz], D[x][vz]
            for t in (s, d):
                if t > 1 and t not in have:
                    have.add(t)
                    g.code.append((0, t, dad.get(t, mem.get(t)), 0))
            B[y + 5 * ((2 * x + 3 * y) % 5)] = g.x(s, d)
        A = [g.x(B[k], g.a(g.nt(B[k - k % 5 + (k + 1) % 5]), B[k - k % 5 + (k + 2) % 5])) for k in range(25)]
        if RC[r] >> z & 1:
            A[0] = g.x(A[0], 1)
        for k in range(25):
            v = nxt[k][z] = A[k]
            if v > 1 and v not in mem and v not in new:
                new[v] = RB + 1600 * r + 64 * k + z
                g.code.append((1, new[v], v, 0))
        code += g.code
    mem.update(new)
    return code, nxt


def bcode():             # input words: lane k < 5, bit z is data word 2 + 64 k + z at INF + 64 k + z
    st, mem = [[0] * 64 for _ in range(25)], {}
    for k in range(5):
        for z in range(64):
            st[k][z] = st[10 + k][z] = 2 + 64 * k + z
            mem[2 + 64 * k + z] = INF + 64 * k + z
    for z in (57, 58, 63):
        st[16][z] = 1
    g, codes = Gen(321), []
    for r in range(6):
        c, st = bgen(g, st, mem, r)
        need(None not in [o[2] for o in c if o[0] == 0], 'every LOAD has an address')
        codes.append(c)
    live_mem = {o[2] for o in codes[5] if o[0] == 0}
    live_reg, kept = set(), []
    for ins in reversed(codes[4]):
        t, a, b, d = ins
        if t == 1 and a in live_mem:
            kept.append(ins); live_mem.discard(a); live_reg.add(b)
        elif t in (2, 3) and a in live_reg:
            kept.append(ins); live_reg.discard(a); live_reg.add(b); live_reg.add(d)
        elif t == 4 and a in live_reg:
            kept.append(ins); live_reg.discard(a); live_reg.add(b)
        elif t == 0 and a in live_reg:
            kept.append(ins); live_reg.discard(a); live_mem.add(b)
    codes[4] = kept[::-1]
    return codes, g.n


BCODE, BREG = bcode()
BRND = (1978, 11659, 14735, 14733, 14355, 3234)


def run(code, R, base):  # executes generated setup code, one counted primitive per instruction
    for t, a, b, c in code:
        if t == 2:
            R[a] = XOR(R[b], R[c])
        elif t == 0:
            R[a] = LDW(b)
        elif t == 1:
            STW(a, R[b])
        elif t == 3:
            R[a] = AND(R[b], R[c])
        elif t == 4:
            R[a] = NOT(R[b])
        else:
            STW(base + a, R[b])


# ---- Section 5: plane-major FES into the buffer, chi fused into the transpose tiles; Section 7: table, verification ----
def fes_phase():         # each plane alone over the Gray steps, the 61 cached records in registers, values into the
    sec('fes')           # buffer; the group index, stored after the leader step, is loaded back at the end
    need(REGS['h'] is None, 'no register live across the setup and the FES phase')
    for p in range(NPL):
        k0 = K[0]
        reg = {T: LDW(TABB + NPL * IDX[T] + p) for T in CACHED}
        x = LDW(ACO + p)
        for i, (top, chain) in enumerate(SITES, 1):
            k1 = K[0]
            v = reg[top] if top in CSET else LDW(TABB + NPL * IDX[top] + p)
            for T, last in chain:
                if T in CSET:
                    v = reg[T] = XOR(reg[T], v)
                else:
                    a = TABB + NPL * IDX[T] + p
                    v = XOR(LDW(a), v)
                    if not last:
                        STW(a, v)
            x = XOR(x, v)
            need(WRK[XB - WB + NST * p + i - 1] is None, 'buffer word written once')
            STW(XB + NST * p + i - 1, x)
            need(K[0] - k1 == COST[i - 1], 'FES count per plane and Gray step')
        need(K[0] - k0 == FPLANE, 'FES count per plane')
    REGS['h'] = LDW(HSP)
    need(None not in WRK[XB - WB:], 'buffer: all 175 (2^N_DIR - 1) words written')


def build_tables():      # ONCE: entry v of byte table (b, k) is word k of the XOR of w_{8b+j} over the bits j of v;
    for b in range(5):   # one zero STORE per table, then each entry v from entry v - 2^j (j its lowest set bit) by
        for k in range(2):   # LOAD, XOR with the immediate word, STORE: 10 x (1 + 255 x 3) = 7660
            base = TBY + 512 * b + 256 * k
            STW(base, 0)
            for v in range(1, 256):
                j = (v & -v).bit_length() - 1
                STW(base + v, XOR(LDW(base + (v ^ 1 << j)), WW[8 * b + j][k]))


def stage(R, nz, d, s):  # butterfly: rows k, k + d (bit d of k clear), column shift s; one zero input: 3 ALU
    m = MASK[s]
    for k in range(16):
        if k & d:
            continue
        kk = k + d
        if nz[k] and nz[kk]:
            t = AND(XOR(SHR(R[k], s), R[kk]), m)
            R[k], R[kk] = XOR(R[k], SHL(t, s)), XOR(R[kk], t)
        elif nz[k]:
            R[kk] = AND(SHR(R[k], s), m)
            R[k] = AND(R[k], m)
            nz[kk] = True
        else:
            need(not nz[kk], 'known-zero lower row')


def pair_msgs(p):        # pair p = (h << 47) | (i << 7) | k, a run-time identifier: its members are the emissions
    k0 = K[0]            # e = 2k, 2k + 1 of point i, coset lanes c0 = 32 (k AND 7) + (k >> 3) and c0 + 16; decode and
    k = AND(p, 127)      # four record loads (21), the shared byte-table sum (37), the four source words with each second
    i = AND(SHR(p, 7), (1 << 40) - 1)            # word masked to 64 bits (6), their spill (4): 68
    c = OR(SHL(AND(k, 7), 5), SHR(k, 3))
    a = ADD(SHL(OR(SHL(SHR(p, 47), 8), c), 1), CSB)
    w = [LDC(a), LDC(ADD(a, 1)), LDC(ADD(a, 32)), LDC(ADD(a, 33))]
    g = XOR(i, SHR(i, 1))
    for b in range(5):                           # byte b of the 40-bit g(i) indexes tables (b, 0) and (b, 1)
        v = AND(SHR(g, 8 * b), 255) if b else AND(g, 255)
        t0, t1 = LDW(ADD(v, TBY + 512 * b)), LDW(ADD(v, TBY + 512 * b + 256))
        s0, s1 = (XOR(s0, t0), XOR(s1, t1)) if b else (t0, t1)
    w = [XOR(w[0], s0), AND(XOR(w[1], s1), M64), XOR(w[2], s0), AND(XOR(w[3], s1), M64)]   # total for any p
    for k in range(4):
        STW(SPL + 18 + k, w[k])
    need(K[0] - k0 == 68, 'pair members 68 operations')
    return w


def cur_msg(c, i, e):    # current candidate (h, i, e): i and e are immediates of its site (Section 7), so the record
    k0 = K[0]            # address is (h << 9) + CSB + 2c, h = (c AND (2^128 - 1)) >> 47, and sum g(i)_b w_b is two
    g, m0, m1 = i ^ i >> 1, 0, 0                 # immediate words: 4 + 5 + 2 (spill) + 6 = 17
    for b in range(N_DIR):                       # generation time
        if g >> b & 1:
            m0, m1 = m0 ^ WW[b][0], m1 ^ WW[b][1]
    a = ADD(SHL(SHR(AND(c, M128), 47), 9), CSB + 2 * (16 * (e & 15) + (e >> 4)))
    w0 = XOR(LDC(a), m0)
    w1 = XOR(LDC(ADD(a, 1)), m1)
    STW(SPL + 16, w0)
    STW(SPL + 17, w1)
    L = lanes5(w0, w1)
    need(K[0] - k0 == 17, 'current candidate 17 operations')
    return w0 | w1 << 256, L


def verify(wd, U, tau, i, e):   # candidate path: both members of the pair named by the table word wd against the
    prev = K             # current candidate (c register, (h, i, e)), whose key U[tau] was just probed; result 'cap',
    sec('verify' if prev is not SECS['vcheck'] else 'vcheck')   # 'equal' (distinct messages) or 'differ'
    k0 = K[0]
    f = ADD(LDW(FCW), 1)                         # the candidate-path count F is a memory word: LOAD, ADD, STORE
    STW(FCW, f)
    out = ('cap',) + (None,) * 6
    if not BR(EQ(f, CAPF)):
        live = U[:tau] + U[tau + 1:] + [REGS['c']]   # the probed key is not read again: 15 keys and c
        for k, v in enumerate(live):             # spill: the scalar schedule then has the register file
            STW(SPL + k, v)
        p = AND(wd, M128)                        # the stored pair identifier
        tb, lb = cur_msg(REGS['c'], i, e)
        db = rounds6(lb)
        w = pair_msgs(p)
        st, tm, dm, cmp = 'differ', [], [], 0
        for m in range(2):                       # member m against the current candidate
            ta = w[2 * m] | w[2 * m + 1] << 256
            da = rounds6(lanes5(w[2 * m], w[2 * m + 1]))
            tm.append(ta)
            dm.append(da)
            eq = True
            for k in range(4):
                cmp += 2
                if not BR(EQ(da[k], db[k])):
                    eq = False
                    break
            if eq:                               # equal digests: compare the source words (8)
                cmp += 8
                x = OR(XOR(LDW(SPL + 16), LDW(SPL + 18 + 2 * m)), XOR(LDW(SPL + 17), LDW(SPL + 19 + 2 * m)))
                if BR(x):
                    st = 'equal'
                    out = (st, ta, tb, da, db, tm, dm)
                    break
        if st == 'differ':
            need([LDW(SPL + k) for k in range(16)] == live, 'registers restored')
            BR(MOV(1))                           # return to the site's STORE: 2
            need(K[0] - k0 == 3461 + cmp <= 3493, 'candidate path 3461 + comparisons, at most 3493')
            out = (st, None, tb, None, db, tm, dm)
    globals()['K'] = prev
    return out


def probe(k, e):         # the key word k (bit 140 set) is its own table address; c = TAG 2^128 + n, n the identifier
    c = REGS['c']        # of the current pair. 5 operations (6 at odd e, with the increment); a word whose high half
    w = LDS(k)           # is the tag starts a candidate path, after which the STORE follows
    if BR(LT(XOR(w, c), 1 << 128)):
        return w
    return None


def store(k, e):
    STS(k, REGS['c'])
    REGS['I'] += 1
    if e & 1:
        REGS['c'] = ADD(REGS['c'], 1)


REGS = {'h': 0, 'c': 0, 'M': 0, 'X': 0, 'I': 0}


def run_group(h, seeds, mode):
    global SPARSE, WRK, CREC
    for s in SECS.values():
        s[0] = 0
    CALLS[0] = 0
    SPARSE, WRK, CREC = {}, [None] * (WEND - WB), {}
    GBASE[0] = h << 47
    REGS.update(M=0, X=0, I=0)
    sec('once')                                  # one-time control (group index, count F, tag) and the byte tables
    REGS['h'] = MOV(h)
    STW(FCW, 0)
    TAGW[0] = AND(RAND(coins(seeds[0] + '/tag')), M256 ^ M128)   # c = TAG 2^128, TAG one uniform 128-bit value
    REGS['c'] = TAGW[0] + (h << 47)              # the identifier carried over from groups 0 .. h - 1 (not an operation)
    build_tables()
    need(SECS['once'][0] == 4 + 7660, 'one-time control 4 and byte tables 7660')
    per, origins = leaders(seeds)
    for c in range(LANES):
        j = 256 * h + c
        need(CREC[CSB + 2 * j] | CREC[CSB + 2 * j + 1] << 256 == origins[c] < 1 << 320, 'coset record')
        need(per[c] == 11, 'leader count 11 per coset')
    own = [{} for _ in range(LANES)]             # beside the algorithm: low 16 key bits of each lane's candidates
    sec('fes')                                   # the group index h, the one value live across the setup and the FES
    STW(HSP, REGS['h'])                          # phase, goes to a fixed word here and comes back after the FES phase
    REGS['h'] = None                             # (2 per group, Section 5.3): the setup has all 64 registers
    sec('sgroup')                                # Section 6.3, once per group: the bitplanes
    transpose()
    P = [sum((t >> k & 1) << c for c, t in enumerate(origins)) for k in range(320)]
    need(SECS['sgroup'][0] == 13616 and WRK[PL - WB:PL - WB + 320] == P, 'transpose 13616, bitplanes equal the origins')
    sec('spoint')                                # every point S, |S| <= 8, in order of increasing |S|
    pop, R0 = 0, [0, M256] + [None] * (BREG - 1)
    for S in SUBS:
        w = 0
        for b in range(N_DIR):
            if S >> b & 1:
                w ^= W40[b]                      # w(S) is fixed at generation time: the NOTs of the input code
        k0 = K[0]
        load_input(w)
        cnt = [K[0] - k0]
        R = R0[:]
        for r in range(6):                       # rounds 0..4 into RB + 1600 r, round-5 linear step into A[S]
            k0 = K[0]
            run(BCODE[r], R, ACO + NPL * IDX[S])
            cnt.append(K[0] - k0)
        need(cnt == [640 + w.bit_count(), *BRND], 'input, rounds 0..4 (1978, 11659, 14735, 14733, 14355), linear step 3234')
        pop += w.bit_count()
    need(pop == POP and SECS['spoint'][0] == 61334 * len(SUBS) + POP, 'setup points: 61334 P + popcount sum')
    val = ref_values(P)
    need(all(WRK[ACO - WB + NPL * IDX[S]:ACO - WB + NPL * IDX[S] + NPL] == val[S] for S in SUBS),
         'counted setup equals the reference at every point and lane')
    del val, P
    sec('transform')                             # Lemma 6: truncated Moebius transform, 4 operations per plane word
    for j in range(N_DIR):
        for S in SUBS:
            if S >> j & 1:
                bs, bt = ACO + NPL * IDX[S], ACO + NPL * IDX[S ^ 1 << j]
                for p in range(NPL):
                    STW(bs + p, XOR(LDW(bs + p), LDW(bt + p)))
    need(SECS['transform'][0] == 4 * NPL * J_D, 'transform 4 * 175 * J_D')
    sec('phase')                                 # Lemma 6: tab[T] = XOR of a_(T+V), V in R(T), |T + V| <= 8
    for T in SUBS[1:]:
        R, k = (T >> 1) & ~T, DEG - T.bit_count()
        Vs, V = [], R
        while True:
            if V.bit_count() <= k:
                Vs.append(ACO + NPL * IDX[T | V])
            if not V:
                break
            V = (V - 1) & R
        bt = TABB + NPL * IDX[T]
        for p in range(NPL):
            acc = LDW(Vs[0] + p)
            for b in Vs[1:]:
                acc = XOR(acc, LDW(b + p))
            STW(bt + p, acc)
    need(SECS['phase'][0] == 2 * NPL * V_D, 'phase 2 * 175 * V_D')

    fes_phase()
    need(SECS['fes'][0] == NPL * FPLANE + 2, 'FES total: 175 planes and the spill')
    keys = [0] * LANES
    st = {'checks': 0, 'mismatch': 0}
    K24 = []                                     # key bits 0..23 of every candidate, point-major (not counted)
    found = key0 = U = None
    for i in range(1 << N_DIR):
        c0, t0, z0, b0 = SECS['cht'][0], SECS['table'][0], SECS['zero'][0], SECS['buf'][0]
        m0, x0 = REGS['M'], REGS['X']
        for tau in range(9):
            R, nz = [0] * 16, [False] * 16
            for dz, z in enumerate(range(4 * tau, min(4 * tau + 4, 35))):
                if i:                            # the five values of z from the buffer
                    sec('buf')
                    vals = [LDW(XB + NST * (5 * z + x) + i - 1) for x in range(5)]
                else:                            # point zero: the current-value frame A[{}]
                    sec('zero')
                    vals = [LDW(ACO + 5 * z + x) for x in range(5)]
                sec('cht')                       # chi of row 0, iota omitted: 12 ALU per z, into the tile
                for x in range(4):
                    R[4 * dz + x] = XOR(AND(NOT(vals[(x + 1) % 5]), vals[(x + 2) % 5]), vals[x])
                    nz[4 * dz + x] = True
            for b in range(4):
                stage(R, nz, 1 << b, 1 << b)
                if tau == 8 and b == 2:          # key row 140 all ones: XOR its stage-2 image (8 immediates)
                    for r in range(8, 16):
                        R[r] = XOR(R[r], IMG[r])
            for l in range(16):
                STW(INT + 16 * tau + l, R[l])
        for l in range(16):
            U = [LDW(INT + 16 * tau + l) for tau in range(9)] + [0] * 7
            nz = [True] * 9 + [False] * 7
            for b in range(4):
                stage(U, nz, 1 << b, 16 << b)
            sec('table')
            for tau in range(16):
                e = 16 * l + tau
                need(REGS['c'] == TAGW[0] | (h << 47) | (i << 7) | e >> 1, 'identifier of the pair of (h, i, e)')
                keys[16 * tau + l] = U[tau]
                o = own[16 * tau + l]
                o[U[tau] & 0xFFFF] = o.get(U[tau] & 0xFFFF, 0) + 1
                t1, old = K[0], U[tau] in SPARSE
                r = probe(U[tau], e)
                if r is not None:                # candidate path: written slot (key match) or garbage word
                    REGS['M' if old else 'X'] += 1
                    u0 = UNW[0]
                    v = verify(r, U, tau, i, e)
                    need(UNW[0] == u0 or not old, 'never-written coset records read on garbage paths only')
                    if v[0] != 'differ':
                        found = v
                        break
                store(U[tau], e)
                need(K[0] - t1 == 5 + (e & 1), 'table path 5, or 6 at odd e')
            sec('cht')
            if found:
                break
        if found:
            break
        if i == 0:
            key0 = keys[0]
        dm, dx = REGS['M'] - m0, REGS['X'] - x0
        need(SECS['cht'][0] - c0 == 4664, 'chi/transpose 4664 per point')
        need(SECS['table'][0] - t0 == 1408, 'table 1408 per point (5.5 per candidate)')
        need((SECS['buf'][0] - b0, SECS['zero'][0] - z0) == ((NPL, 0) if i else (0, NPL)),
             '175 buffer reads per point i >= 1, 175 point-zero loads')
        K24.extend(k & 0xFFFFFF for k in keys)   # beside the algorithm, not counted
        c = i % LANES                            # check beside the algorithm, not counted
        d = sha3_256(message(point(origins[c], i)))
        kn = sum(((int.from_bytes(d[8 * x:8 * x + 8], 'little') ^ (RC[5] if x == 0 else 0)) >> z & 1) << 4 * z + x
                 for z in range(35) for x in range(4))
        st['checks'] += 1
        st['mismatch'] += kn | 1 << 140 != keys[c]
    if not found:
        sec('leader')                            # group control: next group index ((c AND (2^128 - 1)) >> 47), compare
        BR(EQ(SHR(AND(REGS['c'], M128), 47), G))    # with G, branch
        need(SECS['leader'][0] == 11 * LANES + 5, 'leader 11 per coset, group control 5')
        need(SECS['cht'][0] == 4664 << N_DIR and SECS['buf'][0] == NPL * NST, 'chi/transpose and buffer totals')
        need(REGS['I'] == QR and REGS['c'] == TAGW[0] | (h << 47) + QR // 2, 'table stores, identifiers')
        sec('vcheck')                            # beside the run: probe the first candidate's key again (4 operations;
        k1, saved = K[0], WRK[FCW - WB]          # the slot names pair 0), the candidate path against (i, e) = (0, 1),
        r = probe(key0, 0)                       # the second member of that pair (equal message, continue), the STORE
        need(r == TAGW[0] | h << 47 and K[0] - k1 == 4, 'stored pair 0, 4 operations')
        WRK[FCW - WB] = 0
        v = verify(r, U, 1, 0, 1)
        STS(key0, REGS['c'])                     # the STORE of that probe (e = 0: no increment)
        WRK[FCW - WB] = saved
        for t0, dd, tt in ((origins[0], v[6][0], v[5][0]), (origins[16], v[6][1], v[5][1]), (origins[16], v[4], v[2])):
            need(tt == t0, 'reconstructed source')
            need(b''.join(w.to_bytes(8, 'little') for w in dd) == sha3_256(message(tt)), 'reconstructed digest')
        need(v[0] == 'differ' and CALLS[0] == 0 and K[0] - k1 <= 5 + 3493, 'candidate path <= 3493, no permutation call')
    need(SECS['verify'][0] <= 3493 * (REGS['M'] + REGS['X']), 'candidate-path bound')
    need(i + 1 == 1 << N_DIR or found, 'all Gray points')
    need(SECS['zero'][0] == 175 and SECS['once'][0] == 7664, 'point-zero loads 175, once ops 7664')  # checked, not reported (<= 16 observations)
    obs = {'fes_ops': SECS['fes'][0], 'buffer_reads': SECS['buf'][0], 'chi_transpose_ops': SECS['cht'][0],
           'table_ops': SECS['table'][0], 'table_stores': REGS['I'],
           'garbage_paths': REGS['X'], 'key_matches': REGS['M'], 'leader_ops': SECS['leader'][0],
           'setup_group_ops': SECS['sgroup'][0], 'setup_point_ops': SECS['spoint'][0],
           'transform_phase_ops': SECS['transform'][0] + SECS['phase'][0],
           'verify_check_ops': SECS['vcheck'][0], 'perm_calls': CALLS[0], 'native_checks': st['checks'],
           'key_mismatch': st['mismatch']}
    out = [None] * LANES
    if found and found[0] == 'equal':            # a full collision (probability below 2^-222) goes to trial 0
        ma, mb = message(found[1]), message(found[2])
        if ma != mb and sha3_256(ma) == sha3_256(mb):
            out[0] = (ma.hex(), mb.hex())
    if mode is None:
        return [dict(own_pairs16=sum(n * (n - 1) // 2 for n in o.values()), **obs) for o in own], out
    del obs['buffer_reads'], obs['table_stores']   # checked above, not reported (<= 16 observations)
    if found:                                    # no premise test after a stop
        obs.update(pairs16_within=-1, pairs16_cross=-1, pairs24_cross=-1)
    else:
        counts, out = premise_test(K24, origins, mode)
        obs.update(counts)
    return [obs] * LANES, out


def point(t, i):         # parameter of Gray point i of the coset with origin t
    g = i ^ i >> 1
    for b in range(N_DIR):
        if g >> b & 1:
            t ^= W40[b]
    return t


def pairs(vals):         # unordered pairs of equal values (sum over runs of C(len, 2))
    vals.sort()
    tot, run = 0, 1
    for a, b in zip(vals, vals[1:]):
        if a == b:
            tot += run
            run += 1
        else:
            run = 1
    return tot


PASS = {'pairs16_within': (421, 601), 'pairs16_cross': (129115, 132005), 'pairs24_cross': (420, 600)}
MASK16 = {'kind': 'digest-xor-mask', 'mask_hex': '0f00000000000000' * 4, 'expected_hex': '00' * 32}
MODES = {'fes-campaign-reduced': (None, {'kind': 'full-collision'}), 'hcoset-within16': ('within16', MASK16),
         'hcoset-cross16': ('cross16', MASK16)}


def premise_test(K24, origins, mode):   # proof.md Section 12.2; beside the algorithm, not counted
    col = [K24[c::LANES] for c in range(LANES)]   # keys of coset lane c in Gray order
    w16 = sum(pairs([k & 0xFFFF for k in v]) for v in col)
    w24 = sum(pairs(list(v)) for v in col)
    counts = {'pairs16_within': w16, 'pairs16_cross': pairs([k & 0xFFFF for k in K24]) - w16,
              'pairs24_cross': pairs(list(K24)) - w24}
    for name, (lo, hi) in PASS.items():
        need(lo <= counts[name] <= hi, name + ' inside its pass interval')
    out, half = [], 1 << N_DIR - 1
    for c in range(LANES):
        first, hit = {}, None
        if mode == 'within16':                   # the first repeat of key bits 0..15 inside coset c
            for i, k in enumerate(col[c]):
                if k & 0xFFFF in first:
                    hit = ((c, first[k & 0xFFFF]), (c, i))
                    break
                first[k & 0xFFFF] = i
        else:                                    # points a < 256 of coset c against points b >= 256 of coset c XOR 1
            for i in range(half):
                first.setdefault(col[c][i] & 0xFFFF, i)
            for i in range(half, 2 * half):
                if col[c ^ 1][i] & 0xFFFF in first:
                    hit = ((c, first[col[c ^ 1][i] & 0xFFFF]), (c ^ 1, i))
                    break
        if hit:
            ma, mb = (message(point(origins[cc], ii)) for cc, ii in hit)
            da, db = sha3_256(ma), sha3_256(mb)
            need(ma != mb and all((da[8 * x] ^ db[8 * x]) & 15 == 0 for x in range(4)), 'returned pair on the mask')
            hit = (ma.hex(), mb.hex())
        out.append(hit)
    return counts, out


def main():
    req = json.loads(sys.stdin.read())
    eid = req.get('experiment_id')
    need(eid in MODES and req.get('event') == MODES[eid][1], 'experiment id and its event')
    setup_checks()
    trials = req['trials']
    out = []
    for g in range(0, len(trials), LANES):
        grp = trials[g:g + LANES]
        seeds = [t['seed'] for t in grp] + [grp[0]['seed'] + '/%d' % c for c in range(len(grp), LANES)]
        obs, pairs_out = run_group(int(grp[0]['seed'], 16) % G, seeds, MODES[eid][0])
        for c, t in enumerate(grp):
            a, b = pairs_out[c] or (None, None)
            out.append({'trial': t['trial'], 'message_a_hex': a, 'message_b_hex': b, 'observations': dict(obs[c])})
    sys.stdout.write(json.dumps({'schema_version': 1, 'trials': out}, separators=(',', ':')))


if __name__ == '__main__':
    main()
