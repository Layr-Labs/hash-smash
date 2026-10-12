"""Reduced run of the campaign of proof.md on the exact target sha3-256-r6-prefix-v1 (SHA3-256, prefix rounds 0 to 5, zero
state, rate 136 bytes, suffix 0x06, full 256-bit digest) with the organizer-executed tests of premise H_coset (Section 12.2).
Standard library only. Reads one organizer request (JSON) on stdin, writes one JSON document on stdout.
Once per request: the 6-round hash equals two known-answer digests of the organizer reference and, at 24 rounds,
hashlib.sha3_256; rank(W40) = 40; the 780 two-round polarizations of Lemma 3 vanish.
Trials 256g .. 256g + 255 form a group (h = int(seed of its first trial, 16) mod G); trial k is coset lane c = k mod 256, coset
j = 256 h + c. The leader step draws t_j from two RAND primitives, here the halves of SHAKE-256 of the trial's seed (a
reproducible stand-in, not the attack's randomness). Every operation below runs through the counting machine (one call = one
256-bit primitive, no permutation call) and the program stops unless each executed count equals the formula of proof.md.
(1) Reference schedule (Sections 5.3, 5.4, 6, 7): the first 2^9 Gray points of each coset, degree 8, 175 planes, the 140-bit key,
the value-masked table, native verification: leader 11 per coset and 5 per group; transpose 13616; per point the folded setup
code (1978 + 2 popcount, 11651, 14725, 14723, 14725, 4220); transform 4 * 175 per pair; phase 2 * 175 per term; 7800 per record
transpose; frame copies; the candidate-major FES (3301 per coset); the key 6 per candidate; table 6, 14 or 10; byte tables
7660; verification 5 + 61 + 61 + 58 + 19 and the folded rounds of both messages (67, 236, 242, 242, 242, 79: round 5 keeps
only what digest lanes 0..3 use, by liveness), at most 2428. Register peaks of the generated code: 11, 28, 28, 28, 28, 16
(setup), 34 (verification, 39 with the first digest and v), 64 in the main loop.
(2) CAMP-F (Sections 5.5, 6.3, 6.4): the setup code without dead operations (1347 + 2 popcount, 11651, 14725, 13666, 3865 and
244 per point; round 5 stores the 8 XOR-forms of the planes (x, z), x < 5, z < 2) on the 32 points within the first 5
directions, its transform (4 * 8 per pair) and phase (2 * 8 per term), the records equal to the XORs of the reference plane
records; then the plane-major FES of the 8 forms on all 511 Gray steps in two passes of 4 forms (15, 15, 14, 14 and 13 cached
records; NOT of the forms with target 0; 3 AND and STORE, resp. 3 AND, LOAD and AND, per point; block control 9), whose filter
word at every point must equal the survivors (event bits 0..7 of the emitted keys equal 1) of all 2^17 candidates.
Not counted: the bitplanes, setup values and current values equal independent evaluations; at point i the message of lane
i mod 256 is hashed natively and its key compared with the emitted key (key_mismatch); the first candidate is probed and
verified again. Sparse words never written read as a fixed function of their address (top half 0 or >= 2^127, never the tag);
a read of a never-written work or coset word, or of a frame word after its last change, stops the program.
By experiment id (event bit 4 z + x = key bit 36 x + z = digest bit z of lane x): fes-campaign-reduced counts own_pairs16, the
pairs of the trial's 512 keys agreeing on event bits 0..15; hcoset-within16 / hcoset-cross16 stop unless pairs16_within,
pairs16_cross, pairs24_cross lie in the PASS intervals and return the first pair of its coset (cross: of the partner coset)
agreeing on bits 0..15; hcoset-filter8 stops unless the survivor count lies in [422, 602] and the survivor pairs agreeing on
bits 8..15 are within 4 sd of C(n, 2)/256, and returns the t-th such pair; every pair is hashed natively. Nothing about cost is
inferred from a run.
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
CSB, WB = 1 << 130, 1 << 131                     # coset record of coset j at CSB + 2j; work region. SPARSE[k] is the
WF, PL, TW = WB, WB + 512, WB + 832              # key word k itself (bit 143 set). Work: working frames, 320
INF = TW + 3                                     # bitplanes, 3 transpose words, input words (inverted plane k at
RB, DW = INF + 320, INF + 8320                   # INF + k), the output of round r at RB + 1600 r + 64 l + z, D words;
ACO = DW + 320                                   # coefficient record A[S] at ACO + 175 IDX[S] (current frame = A[{}]);
TABB = ACO + NPL * len(SUBS)                     # derivative record tab[T] at TABB + 175 IDX[T]; byte table (b, k) at
TBY = TABB + NPL * len(SUBS)                     # TBY + 256 (2b + k); the words of F and h across setup and FES;
FCW, HSP = TBY + 2560, TBY + 2561                # candidate-major record S of coset lane c at CMR + 256 IDX[S] + c;
CMR = HSP + 1                                    # the fixed frame of the current coset (record S at FR + IDX[S]);
FR = CMR + 256 * len(SUBS)                       # 61 spill words of the hit path
SPL = FR + len(SUBS)
AFO = SPL + 61                                   # CAMP-F (Sections 5.5, 6.3): coefficient record S of the 8 forms at AFO + 8 IDX[S], derivative
TFO = AFO + 8 * len(SUBS)                        # record T at TFO + 8 IDX[T]; the FES frame of the forms (record T of form f at FFR + 8 IDX[T] + f),
FFR = TFO + 8 * len(SUBS)                        # the accumulators ACC (2^N_DIR words) and the block counter after them
ACB = FFR + 8 * len(SUBS)
WEND = ACB + (1 << N_DIR) + 1
CACHED = list(range(1, 32)) + [32 | t for t in range(3, 32)]   # the 60 records held in registers
CSET = set(CACHED)
STRIDE = 36                                      # candidate-major word: pre-chi bit (x, z) at bit 36 x + z, lane x = 5
MARK = 1 << 3 * STRIDE + 35                      # a copy of lane 0 (bits 180 + z), constant marker bit 143
KEYMASK = sum(((1 << 35) - 1) << STRIDE * x for x in range(4)) | MARK
ROWS = [None] * 256                              # row r of a record's 256 x 256 transpose: its plane p, or None (zero)
for _p, (_x, _z) in enumerate(PLANES):
    ROWS[STRIDE * _x + _z] = _p
    if _x == 0:
        ROWS[5 * STRIDE + _z] = _p
SPREAD = [sum((v >> b & 1) << 4 * b for b in range(6)) for v in range(64)]


def ev24(k):             # beside the algorithm: key bits 0..23 in event order (bit 4 z + x = pre-chi row-0 bit (x, z))
    return sum(SPREAD[k >> STRIDE * x & 63] << x for x in range(4))


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


def fcoset(n):           # candidate-major FES of one coset over 2^n - 1 Gray steps: 61 initial loads (60 cached records
    n1 = (1 << n) - 1    # and the current value), a top LOAD per step whose top is not cached, x XOR per step, per link
    links = sum(comb(n, k) * min(DEG, k) for k in range(1, n + 1)) - n1          # 1 if cached, else LOAD, XOR, STORE,
    lc = sum((1 << n - T.bit_length()) - 1 for T in CACHED)                       # minus the STORE at the last change
    ulast = sum(comb(n - 1, k) for k in range(1, DEG)) - len(CACHED)              # of each uncached |T| <= 7 record
    return len(CACHED) + 1 + (n1 - len(CACHED)) + n1 + 3 * links - 2 * lc - ulast


# code generation: per Gray step the top T_L and the links T_{L-1} .. T_1, each flagged at its last update
# (i + 2^(max T + 1) >= 2^N_DIR: that STORE is not emitted), and the step's count
SITES = [(sh[-1], [(T, i + (1 << T.bit_length()) > NST) for T in sh[-2::-1]])
         for i, sh in ((i, shapes(i)) for i in range(1, NST + 1))]
COST = [(top not in CSET) + sum(1 if T in CSET else 3 - last for T, last in ch) + 1 for top, ch in SITES]
FCOSET = fcoset(N_DIR)
need(len(CACHED) == 60 and FCOSET == 61 + sum(COST), 'FES per coset: 61 initial loads and the step counts')
need(fcoset(40) == 18794671433175, 'FES per coset at n = 40 (17.0937 per candidate)')
RTR = 4 * (66 + 198 + 5 * 196 + 66) + 2 * 128 * 10   # one record's 256 x 256 transpose: four 64 x 64 blocks, two stages


def popsum(n):           # Section 6.3: sum of popcount(w(S)) over |S| <= 8; bit k of w(S) is set iff |S & B_k| is odd,
    s = 0                # B_k = {b < n : bit k of w_b is set}, m = |B_k|
    for k in range(320):
        m = sum(W40[b] >> k & 1 for b in range(n))
        s += sum(comb(m, j) * sum(comb(n - m, l) for l in range(DEG + 1 - j)) for j in range(1, DEG + 1, 2))
    return s


POP = popsum(N_DIR)
need(popsum(40) == 4592341856, 'Section 6.3 popcount sum at n = 40')


CAPF = cap(QR * (QR - 1), 1 << 141)              # verification cap (full size R140)
GM = 0x9E3779B97F4A7C15F39CC0605CEDC8341082276BF3A27251F86C6A11D0C18E95   # odd multiplier of the garbage stand-in
J_D = sum(S.bit_count() for S in SUBS)
def vd(n):               # Section 4.3: V_D = number of terms of all derivative records tab[T], |T| <= 8, of n directions
    return sum(comb(j, r) * comb(n - j, r) * sum(comb(r, k) for k in range(min(r, DEG - j) + 1))
               for j in range(1, min(DEG, n) + 1) for r in range(min(j, n - j) + 1))


V_D = vd(N_DIR)

# ---- counting machine: every call is one charged 256-bit primitive of the current section ----
SECS = {s: [0] for s in ('once', 'leader', 'sgroup', 'spoint', 'transform', 'phase', 'rtr', 'buf', 'fes', 'cht',
                          'table', 'verify', 'vcheck', 'cs', 'ct', 'cp', 'cfa', 'cfb')}
K = SECS['once']
SPARSE, WRK, CREC, CALLS, GBASE = {}, [], {}, [0], [0]


def sec(name):
    global K
    K = SECS[name]


def LDS(a):              # sparse word; a never-written one holds arbitrary content (a fixed function of its address)
    K[0] += 1
    v = SPARSE.get(a)
    if v is None:
        x = (a * GM) & M256
        x ^= x >> 127
        v = x if x >> 255 else GBASE[0] + x % (2 * QR)
    return v


def STS(a, v): K[0] += 1; SPARSE[a] = v


def LDW(a):
    K[0] += 1
    v = WRK[a - WB]
    if v is None:
        raise SystemExit('check failed: read of a never-written work word')
    return v


def STW(a, v): K[0] += 1; WRK[a - WB] = v


def LDC(a):
    K[0] += 1
    need(a in CREC, 'read of a never-written coset record')
    return CREC[a]


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


def lanes5(w0, w1):      # 6: lanes 0..3 from w0, lane 4 is w1 itself; lanes 10..14 are the same registers, and the
    need(w1 >> 64 == 0, 'second source word below 2^64')    # zero lanes and the padding lane are immediates
    return [AND(w0, M64), AND(SHR(w0, 64), M64), AND(SHR(w0, 128), M64), SHR(w0, 192), w1]


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
    need(all(type(v) is int for v in L[:4]), 'digest lanes in registers')
    return codes, L[:4], g.n


def dce_s(codes, out):   # drop the operations that no digest lane (lanes 0..3 of round 5) depends on, by liveness from the end
    live, keep = set(out), []
    for code in reversed(codes):
        k = []
        for op in reversed(code):
            if op[1] in live:
                live.discard(op[1])
                live.update((op[2], op[3]) if op[0] in ('x', 'a') else (op[2],))
                k.append(op)
        keep.append(k[::-1])
    return keep[::-1]


SCODE, SOUT, SREG = scode()
SCODE = dce_s(SCODE, SOUT)
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
def ldr(a):              # a row: LOAD of its word, or a constant row (a tuple) set by one MOV
    return MOV(a[0]) if type(a) is tuple else LDW(a)


def tr64(src, dst, sh):  # 64 x 64 transpose, stages s = 1..32: rows 2..63 in registers, rows 0 and 1 in two fixed words
    R = [0, 0] + [ldr(a) for a in src[2:]]       # (load 66); then 66 to store, or 258 to shift by sh and OR into dst
    for k in (0, 1):
        STW(TW + k, ldr(src[k]))
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


def rtrans(base, dst, mark):   # one record (plane p at base + p, bit c for coset lane c) into candidate-major words:
    rows = [(0,) if p is None else base + p for p in ROWS]   # word dst + c holds row r at bit r (pre-chi bit (x, z) at
    if mark:                                     # bit 36 x + z, lane 5 a copy of lane 0); the current value A[{}] has
        rows[143] = (M256,)                      # the marker row 143 all ones. Rows: 210 LOADs and 46 MOVs of a
    for g in range(4):                           # constant; four 64 x 64 blocks (1310 each), then stages 64 and 128 on
        tr64(rows[64 * g:64 * g + 64], range(dst + 64 * g, dst + 64 * g + 64), 0)   # word pairs (10 each): 7800
    for s in (64, 128):
        for k in range(256):
            if not k & s:
                u, v = LDW(dst + k), LDW(dst + k + s)
                t = AND(XOR(SHR(u, s), v), MASK[s])
                STW(dst + k, XOR(u, SHL(t, s)))
                STW(dst + k + s, XOR(v, t))


# Constant-folded rounds 0..4 and round-5 step, generated once (Section 11.2): a state word is a known constant (0 or 1) or a data word
# n >= 2; an operation is emitted only if its result is not fixed (XOR 0, AND 1, v XOR v fold; XOR 1 is a NOT; AND 0 is 0). Code: (0, n, a, 0)
# LOAD; (1, a, n, 0) STORE; (2|3, n, u, v) XOR|AND; (4, n, u, 0) NOT; (5, p, n, 0) STORE into word p of A[S]; (6, n, k, 0) LOAD of input plane k.
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


def bgen(g, st, mem, r, fm=0):
    C, D, pc, dc = [[0] * 64 for _ in range(5)], [[0] * 64 for _ in range(5)], [], []    # address of each data word
    for z in range(64):
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
    if not cc:
        code += pc[63]
        for z in range(64):
            code += pc[z] if z < 63 else []
            if not dd:
                code += dc[z]
                for x in range(5):
                    if D[x][z] > 1 and D[x][z] not in dad:
                        dad[D[x][z]] = DW + 64 * x + z
                        code.append((1, DW + 64 * x + z, D[x][z], 0))
    if r == 5 and fm:
        pv = {}
        for z in (0, 1):
            for x in range(5):
                g.code, vz = [], (z - RHO[6 * x]) % 64
                s, d = st[6 * x][vz], D[x][vz]
                for t in (s, d):
                    if t > 1:
                        g.code.append((0, t, dad.get(t, mem.get(t)), 0))
                pv[x, z] = g.x(s, d)
                code += g.code
        for f, (z, xs) in enumerate(FORMS):
            g.code, v = [], pv[xs[0], z]
            for x in xs[1:]:
                v = g.x(v, pv[x, z])
            code += g.code + [(5, f, v, 0)]
        return code, None
    if r == 5:
        for p, (x, z) in enumerate(PLANES):
            g.code, vz = [], (z - RHO[6 * x]) % 64
            s, d = st[6 * x][vz], D[x][vz]
            for t in (s, d):
                if t > 1:
                    g.code.append((0, t, dad.get(t, mem.get(t)), 0))
            v = g.x(s, d)
            code += g.code + [(5, p, v, 0)]
        return code, None
    nxt, new = [[0] * 64 for _ in range(25)], {}
    for z in range(64):
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


def bcode(fm=0):           # input: lane k < 5, bit z is data word 2 + 64 k + z, read from plane 64 k + z (code 6)
    st, mem = [[0] * 64 for _ in range(25)], {}
    for k in range(5):
        for z in range(64):
            st[k][z] = st[10 + k][z] = 2 + 64 * k + z
            mem[2 + 64 * k + z] = PL + 64 * k + z
    for z in (57, 58, 63):
        st[16][z] = 1
    g, codes = Gen(321), []
    for r in range(6):
        c, st = bgen(g, st, mem, r, fm)
        need(None not in [o[2] for o in c if o[0] == 0], 'every LOAD has an address')
        codes.append([(6, a, b - PL, 0) if t == 0 and PL <= b < PL + 320 else (0, a, b - WB, 0) if t == 0 else (1, a - WB, b, d) if t == 1
                      else (t, a, b, d) for t, a, b, d in c])
    return codes, g.n


FORMS = ((0, (0, 1)), (0, (1, 2)), (0, (2, 3)), (0, (3, 4)), (1, (1,)), (1, (3,)), (1, (0, 2)), (1, (2, 4)))   # (z, planes x XORed)
BCODE, BREG = bcode()
BRND = (1978, 11651, 14725, 14723, 14725, 4220)
need(sorted(o[2] for o in BCODE[0] if o[0] == 6) == sorted(2 * list(range(320))), 'round 0 LOADs each plane twice')


def peak(ops, out=()):   # registers of straight-line code (result, operands): the most values live at once
    live, top = set(out), len(out)
    for d, src in reversed(ops):
        live.discard(d)
        live.update(src)
        top = max(top, len(live))
    return top


def sops(codes):         # scalar code; a rotation is its two shifts, OR and AND (two temporaries)
    ops, n = [], 0
    for code in codes:
        for t, d, a, b in code:
            if t == 'r':
                n -= 3
                ops += [(n, {a}), (n + 1, {a}), (n + 2, {n, n + 1}), (d, {n + 2})]
            else:
                ops.append((d, {a, b} if t in ('x', 'a') else {a}))
    return ops


def bpeak(codes):
    return [peak([(a, ()) if t in (0, 6) else (None, (b,)) if t in (1, 5) else (a, (b, d) if t < 4 else (b,))
                  for t, a, b, d in c]) for c in codes]


BPEAK = bpeak(BCODE)
SPEAK = peak(sops(SCODE), SOUT)                  # verification: SPEAK + 4 (first digest) + 1 (v); main loop: 60 cached
need(BPEAK == [11, 28, 28, 28, 28, 16] and SPEAK + 4 + 1 == 39 and len(CACHED) + 2 + 2 == 64,   # records, x, v and
     'register peaks: setup rounds, verification 39 of the 61 freed and v, main loop 64')        # two temporaries


PLR, INR = PL - WB, INF - WB


def run(code, R, base, w, done):   # executes generated setup code; every instruction is one counted primitive (n, added to the section at the end);
    n, W, o = len(code), WRK, base - WB    # w = w(S): the first LOAD of a plane that w inverts is followed by NOT and the STORE of its input word
    for t, a, b, c in code:        # (3 primitives), which every later LOAD of that plane reads; word addresses of the code are relative to WB
        if t == 2:
            R[a] = R[b] ^ R[c]
        elif t == 0:
            R[a] = v = W[b]
            if v is None:
                raise SystemExit('check failed: read of a never-written work word')
        elif t == 1:
            W[a] = R[b]
        elif t == 4:
            R[a] = R[b] ^ M256
        elif t == 3:
            R[a] = R[b] & R[c]
        elif t == 6:
            if not w >> b & 1:
                R[a] = W[PLR + b]
            elif b in done:
                R[a] = W[INR + b]
            else:
                done.add(b)
                R[a] = W[INR + b] = W[PLR + b] ^ M256
                n += 2
        else:
            W[o + a] = R[b]
    K[0] += n


# ---- CAMP-F (proof.md Sections 5.5, 6.3, 6.4): eight XOR-forms, setup code without dead operations, plane-major FES ----
NS = 5                                           # directions of the counted forms setup (the FES below runs on all N_DIR)
KAF, KBF = (15, 15, 14, 14), (13, 13, 13, 13)    # cached records per form: pass A (4 + 58 + 2 temporaries), pass B (4 + 52 + 7 + 1)
SETUP_PT = (1347, 11651, 14725, 13666, 3865, 244)     # per point: rounds 0..4 (round 0 plus 2 popcount) and the round-5 step
need(sum(KAF) + 4 + 2 == 64 and sum(KBF) + 4 + 7 + 1 == 64, 'registers of the two passes')


def dce_b(codes):        # drop the operations and stores that no stored form depends on (liveness from the stores, rounds 5 to 0)
    nr, na, keep = set(), set(), []
    for code in reversed(codes):
        k = []
        for t, a, b, c in reversed(code):
            if t == 5 or (t == 1 and a in na) or (t in (0, 6, 2, 3, 4) and a in nr):
                if t in (0, 6, 2, 3, 4):
                    nr.discard(a)
                if t == 1:
                    na.discard(a)
                if t == 0:
                    na.add(b)
                if t in (1, 4, 5):
                    nr.add(b)
                if t in (2, 3):
                    nr.update((b, c))
                k.append((t, a, b, c))
        keep.append(k[::-1])
    return keep[::-1]


FCODE, FREG = bcode(1)
FCODE = dce_b(FCODE)
need([len(c) for c in FCODE] == list(SETUP_PT) and all(map(int.__le__, bpeak(FCODE), BPEAK)), 'setup code of the forms: counts, register peaks')


def sav(T, n):           # operations saved by holding record T in a register over the 2^n - 1 steps (Appendix B)
    m = T.bit_length() - 1
    if T.bit_count() < DEG:
        return 2 * ((1 << (n - 1 - m)) - 1 if m <= n - 2 else 0) - 1
    return (1 << (n - 1 - m)) - 1


def cache_set(k, n):     # the k records of largest saving, ties by the smaller mask
    return set(sorted((T for T in range(1, 1 << n) if T.bit_count() <= DEG), key=lambda T: (-sav(T, n), T))[:k])


def fes_f(n, CR):        # operations of one word sequence over the 2^n - 1 steps with the records CR in registers (Appendix B)
    n1 = (1 << n) - 1
    links = sum(comb(n, k) * min(DEG, k) for k in range(1, n + 1)) - n1
    lcr = tcr = 0
    for T in CR:
        m = T.bit_length() - 1
        if T.bit_count() < DEG:
            lcr += (1 << (n - 1 - m)) - 1 if m <= n - 2 else 0
            tcr += 1
        else:
            tcr += (1 << (n - 1 - m)) if m <= n - 1 else 0
    uall = sum(comb(n - 1, k) for k in range(1, DEG))
    unc = uall - sum(1 for T in CR if T.bit_count() < DEG and T.bit_length() - 1 <= n - 2)
    return len(CR) + 1 + n1 + (n1 - tcr) + 3 * links - 2 * lcr - unc


def forms_setup():       # Sections 6.3 and 6.4 for the 8 forms at NS directions, from the bitplanes of the group: counted
    SB = [S for S in SUBS if S < 1 << NS]
    sec('cs')
    R0, pop = [0, M256] + [None] * (FREG - 1), 0
    for S in SB:
        w = 0
        for b in range(NS):
            if S >> b & 1:
                w ^= W40[b]
        R, cnt, done = R0[:], [], set()
        for r in range(6):
            k0 = K[0]
            run(FCODE[r], R, AFO + 8 * IDX[S], w, done)
            cnt.append(K[0] - k0)
        need(cnt == [SETUP_PT[0] + 2 * w.bit_count(), *SETUP_PT[1:]], 'forms setup: 1347 + 2 popcount, 11651, 14725, 13666, 3865, 244')
        pop += w.bit_count()
    need(pop == popsum(NS) and SECS['cs'][0] == sum(SETUP_PT) * len(SB) + 2 * pop, 'forms setup: 45498 per point')
    sec('ct')
    for j in range(NS):
        for S in SB:
            if S >> j & 1:
                bs, bt = AFO + 8 * IDX[S], AFO + 8 * IDX[S ^ 1 << j]
                for f in range(8):
                    STW(bs + f, XOR(LDW(bs + f), LDW(bt + f)))
    need(SECS['ct'][0] == 32 * sum(S.bit_count() for S in SB), 'forms transform 4 * 8 * J')
    sec('cp')
    nt = 0
    for T in SB[1:]:
        R, k = (T >> 1) & ~T, DEG - T.bit_count()
        Vs, V = [], R
        while True:
            if V.bit_count() <= k:
                Vs.append(AFO + 8 * IDX[T | V])
            if not V:
                break
            V = (V - 1) & R
        nt += len(Vs)
        for f in range(8):
            acc = LDW(Vs[0] + f)
            for b in Vs[1:]:
                acc = XOR(acc, LDW(b + f))
            STW(TFO + 8 * IDX[T] + f, acc)
    need(SECS['cp'][0] == 16 * nt and nt == vd(NS), 'forms phase 2 * 8 * V')


def forms_fes(K24):      # Section 5.5: the plane-major FES of the 8 forms in two passes, the filter word s, N_DIR directions
    SB = [S for S in SUBS if S < 1 << NS]
    for T in SUBS:       # beside the algorithm, not counted: record T of form f = XOR of the plane records of the reference (Lemma 6 is linear)
        for f, (z, xs) in enumerate(FORMS):
            e = 0
            for x in xs:
                e ^= WRK[(ACO if T == 0 else TABB) - WB + NPL * IDX[T] + x + 5 * z]
            WRK[FFR - WB + 8 * IDX[T] + f] = e
    need(all(WRK[(AFO if T == 0 else TFO) - WB + 8 * IDX[T] + f] == WRK[FFR - WB + 8 * IDX[T] + f] for T in SB for f in range(8)),
         'counted form records equal the XOR of the reference plane records, T within the first NS directions')
    exp = [0] * (1 << N_DIR)
    for n_, k in enumerate(K24):                 # survivors from the emitted keys (event bits 0..7 equal 1); key index 256 i + c
        if k & 255 == 1:
            exp[n_ >> 8] |= 1 << (n_ & 255)
    sw = [0] * (1 << N_DIR)
    for pas, (fl, ks) in enumerate(((range(4), KAF), (range(4, 8), KBF))):
        sec('cfa' if pas == 0 else 'cfb')
        STW(ACB + (1 << N_DIR), 0)               # block counter
        CR = [cache_set(k, N_DIR) for k in ks]
        reg = [{T: LDW(FFR + 8 * IDX[T] + f) for T in CR[q]} for q, f in enumerate(fl)]
        x = [LDW(FFR + f) if f in (1, 2, 3) else NOT(LDW(FFR + f)) for f in fl]   # current values; forms 1, 2, 3 must equal 1, the others 0: NOT
        for i in range(1 << N_DIR):
            for q, f in enumerate(fl):
                if i:
                    top, chain = SITES[i - 1]
                    w = reg[q][top] if top in CR[q] else LDW(FFR + 8 * IDX[top] + f)
                    for T, last in chain:
                        if T in CR[q]:
                            w = reg[q][T] = XOR(reg[q][T], w)
                        else:
                            a = FFR + 8 * IDX[T] + f
                            w = XOR(LDW(a), w)
                            if last:
                                WRK[a - WB] = None
                            else:
                                STW(a, w)
                    x[q] = XOR(x[q], w)
            t = AND(AND(AND(x[0], x[1]), x[2]), x[3])
            if pas == 0:
                STW(ACB + i, t)
            else:
                sw[i] = AND(t, LDW(ACB + i))
        for q, f in enumerate(fl):               # end of the block: STORE the K + 1 registers
            for T, v in reg[q].items():
                STW(FFR + 8 * IDX[T] + f, v)
            STW(FFR + f, x[q])
        c = LDW(ACB + (1 << N_DIR))              # block control, 8: counter LOAD, ADD, STORE, compare, branch, three base-address ADDs
        c = ADD(c, 1)
        STW(ACB + (1 << N_DIR), c)
        BR(EQ(c, 1))
        for b in (ACB, FFR, TFO):
            ADD(c, b)
        need(K[0] == sum(fes_f(N_DIR, CR[q]) + k + 1 for q, k in enumerate(ks)) + (1, 4)[pas] + (4 + pas) * (1 << N_DIR) + 9, 'pass %s count' % 'AB'[pas])
    need(sw == exp, 'the filter word equals the survivors of the emitted keys at every Gray point')


# ---- Section 5: candidate-major FES per coset, chi in registers; Section 7: table, verification ----
def build_tables():      # ONCE: entry v of byte table (b, k) is word k of the XOR of w_{8b+j} over the bits j of v;
    for b in range(5):   # one zero STORE per table, then each entry v from entry v - 2^j (j its lowest set bit) by
        for k in range(2):   # LOAD, XOR with the immediate word, STORE: 10 x (1 + 255 x 3) = 7660
            base = TBY + 512 * b + 256 * k
            STW(base, 0)
            for v in range(1, 256):
                j = (v & -v).bit_length() - 1
                STW(base + v, XOR(LDW(base + (v ^ 1 << j)), WW[8 * b + j][k]))


def jaddr(cid):          # coset record address CSB + 2 j of identifier cid = h 2^48 + c 2^N_DIR + i, j = 256 h + c: 7
    return ADD(SHL(OR(SHL(SHR(cid, 48), 8), AND(SHR(cid, N_DIR), 255)), 1), CSB)


def cold_msg(cid):       # earlier candidate, a run-time identifier: decode (i 1, address 7, records 3, g(i) 2: 13),
    k0 = K[0]            # byte tables (8 per byte, 7 for byte 0: 39), lanes (6) = 58
    i = AND(cid, (1 << N_DIR) - 1)
    a = jaddr(cid)
    w0, w1 = LDC(a), LDC(ADD(a, 1))
    g = XOR(i, SHR(i, 1))
    for b in range(5):                           # byte b of the 40-bit g(i) indexes tables (b, 0) and (b, 1)
        v = AND(SHR(g, 8 * b), 255) if b else AND(g, 255)
        w0 = XOR(w0, LDW(ADD(v, TBY + 512 * b)))
        w1 = XOR(w1, LDW(ADD(v, TBY + 512 * b + 256)))
    L = lanes5(w0, w1)
    need(K[0] - k0 == 58, 'earlier candidate 58 operations')
    return w0 | w1 << 256, L


def cur_msg(v, i):       # current candidate: Gray step i is an immediate of its site, so sum g(i)_b w_b is two
    k0 = K[0]            # immediate words; its identifier is the low half of v (AND), address 7, records and
    g, m0, m1 = i ^ i >> 1, 0, 0                 # immediates 5, lanes 6 = 19
    for b in range(N_DIR):                       # generation time
        if g >> b & 1:
            m0, m1 = m0 ^ WW[b][0], m1 ^ WW[b][1]
    a = jaddr(AND(v, M128))
    w0 = XOR(LDC(a), m0)
    w1 = XOR(LDC(ADD(a, 1)), m1)
    L = lanes5(w0, w1)
    need(K[0] - k0 == 19, 'current candidate 19 operations')
    return w0 | w1 << 256, L


def verify(cold, live, i):   # earlier candidate cold against the current one (v register, Gray step i); live: the 61
    prev = K                 # FES registers (60 cached records, x); result 'cap', 'equal' or 'differ' and live back
    sec('verify' if prev is not SECS['vcheck'] else 'vcheck')
    f = ADD(LDW(FCW), 1)                         # the verification count F in its word: LOAD, ADD, STORE, compare,
    STW(FCW, f)                                  # branch (5)
    out = ('cap', None, None, None, None, live)
    if not BR(EQ(f, CAPF)):
        for k, w in enumerate(live):             # spill the 61 FES registers (61); v stays, SPEAK + 4 + 1 = 39 in use
            STW(SPL + k, w)
        ta, la = cold_msg(cold)
        da = rounds6(la)
        tb, lb = cur_msg(REGS['v'], i)
        db = rounds6(lb)
        st = 'equal'
        for k in range(4):
            if not BR(EQ(da[k], db[k])):
                st = 'differ'
                break
        out = (st, ta, tb, da, db, [LDW(SPL + k) for k in range(len(live))])   # reload (61): at most 2428
    globals()['K'] = prev
    return out


# value-masked table (Section 7): the key word k is its own address, SPARSE[k] holds v = (r << 128) | cid; a miss costs 6, a false pass 14, a valid hit 10
def probe(k):
    cid = REGS['cid']
    v = REGS['v']
    s = LDS(k)
    if BR(SHR(XOR(s, v), 128)):
        STS(k, v)
        REGS['I'] += 1
        REGS['v'] = ADD(v, 1)
        REGS['cid'] = REGS['v'] & M128
        return None                              # miss: LDS, XOR, SHR, BR, STS, ADD = 6
    s = LDS(k)
    if BR(LT(s, v)):
        c2 = AND(LDS(k), M128)
        need(c2 < cid, 'hit: an earlier identifier')
        return c2
    STS(k, v)
    REGS['X'] += 1
    REGS['I'] += 1
    f = ADD(LDW(FCW), 1)
    STW(FCW, f)
    if BR(EQ(f, CAPF)):
        return 'cap'
    REGS['v'] = ADD(v, 1)
    REGS['cid'] = REGS['v'] & M128
    return None


REGS = {'h': 0, 'F': 0, 'cid': 0, 'M': 0, 'X': 0, 'I': 0, 'r': 0, 'R_HI': 0, 'v': 0}


def run_group(h, seeds, mode):
    global SPARSE, WRK, CREC
    for s in SECS.values():
        s[0] = 0
    CALLS[0] = 0
    SPARSE, WRK, CREC = {}, [None] * (WEND - WB), {}
    GBASE[0] = h << 48
    REGS.update(M=0, X=0, I=0)
    sec('once')
    REGS['h'], REGS['F'] = MOV(h), MOV(0)
    rval = (((h + 1) * GM) & ((1 << 127) - 1)) | 1
    REGS['r'] = MOV(rval)
    REGS['R_HI'] = SHL(REGS['r'], 128)
    REGS['v'] = OR(REGS['R_HI'], SHL(REGS['h'], 48))
    build_tables()
    need(SECS['once'][0] == 6 + 7660, 'one-time control 6 (group index, count F, tag r and v) and byte tables 7660')
    per, origins = leaders(seeds)
    for c in range(LANES):
        j = 256 * h + c
        need(CREC[CSB + 2 * j] | CREC[CSB + 2 * j + 1] << 256 == origins[c] < 1 << 320, 'coset record')
        need(per[c] == 11, 'leader count 11 per coset')
    own = [{} for _ in range(LANES)]
    sec('fes')
    STW(HSP, REGS['h'])
    STW(FCW, REGS['F'])
    REGS['h'] = REGS['F'] = None
    sec('sgroup')                                # Section 6.3, once per group: the bitplanes
    transpose()
    P = [sum((t >> k & 1) << c for c, t in enumerate(origins)) for k in range(320)]
    need(SECS['sgroup'][0] == 13616 and WRK[PL - WB:PL - WB + 320] == P, 'transpose 13616, bitplanes equal the origins')
    sec('spoint')
    pop, R0 = 0, [0, M256] + [None] * (BREG - 1)
    for S in SUBS:
        w = 0
        for b in range(N_DIR):
            if S >> b & 1:
                w ^= W40[b]
        R, cnt, done = R0[:], [], set()
        for r in range(6):
            k0 = K[0]
            run(BCODE[r], R, ACO + NPL * IDX[S], w, done)
            cnt.append(K[0] - k0)
        need(cnt == [BRND[0] + 2 * w.bit_count(), *BRND[1:]], 'rounds 0..4 (1978 + 2 popcount, 11651, 14725, 14723, '
             '14725), linear step 4220')
        pop += w.bit_count()
    need(pop == POP and SECS['spoint'][0] == 62022 * len(SUBS) + 2 * POP, 'setup points: 62022 P + 2 popcount sum')
    val = ref_values(P)
    need(all(WRK[ACO - WB + NPL * IDX[S]:ACO - WB + NPL * IDX[S] + NPL] == val[S] for S in SUBS),
         'counted setup equals the reference at every point and lane')
    del val, P
    sec('transform')
    for j in range(N_DIR):
        for S in SUBS:
            if S >> j & 1:
                bs, bt = ACO + NPL * IDX[S], ACO + NPL * IDX[S ^ 1 << j]
                for p in range(NPL):
                    STW(bs + p, XOR(LDW(bs + p), LDW(bt + p)))
    need(SECS['transform'][0] == 4 * NPL * J_D, 'transform 4 * 175 * J_D')
    sec('phase')
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

    sec('rtr')
    for S in SUBS:
        rtrans(ACO if S == 0 else TABB + NPL * IDX[S], CMR + 256 * IDX[S], S == 0)
    need(SECS['rtr'][0] == RTR * len(SUBS) and RTR == 7800, 'record transposes 7800 per record')
    A0 = WRK[ACO - WB:ACO - WB + NPL]
    need(all(WRK[CMR - WB + c] == sum((A0[p] >> c & 1) << r for r, p in enumerate(ROWS) if p is not None) | MARK
             for c in range(LANES)), 'candidate-major current values equal the planes')
    sec('fes')
    REGS['h'] = LDW(HSP)
    sec('leader')
    REGS['cid'] = SHL(REGS['h'], 48)             # group control: the group's first identifier
    REGS['h'] = None
    st = {'checks': 0, 'mismatch': 0}
    K24 = [0] * QR
    found = key0 = None
    for c in range(LANES):
        sec('buf')
        for k in range(len(SUBS)):
            STW(FR + k, LDW(CMR + 256 * k + c))
        sec('fes')
        f0, t0, m0, x0 = SECS['fes'][0], SECS['table'][0], REGS['M'], REGS['X']
        reg = {T: LDW(FR + IDX[T]) for T in CACHED}
        x = LDW(FR)
        o = own[c]
        for i in range(1 << N_DIR):
            if i:
                sec('fes')
                k1 = K[0]
                top, chain = SITES[i - 1]
                w = reg[top] if top in CSET else LDW(FR + IDX[top])
                for T, last in chain:
                    if T in CSET:
                        w = reg[T] = XOR(reg[T], w)
                    else:
                        a = FR + IDX[T]
                        w = XOR(LDW(a), w)
                        if last:
                            WRK[a - WB] = None
                        else:
                            STW(a, w)
                x = XOR(x, w)
                need(K[0] - k1 == COST[i - 1], 'FES count per Gray step')
            sec('cht')
            t1 = SHR(x, 2 * STRIDE)
            t2 = AND(SHR(x, STRIDE), t1)
            key = AND(XOR(XOR(t1, t2), x), KEYMASK)
            sec('table')
            need(REGS['cid'] == (h << 48) + (c << N_DIR) + i, 'identifier of candidate (h, c, i)')
            e = ev24(key)
            K24[LANES * i + c] = e
            o[e & 0xFFFF] = o.get(e & 0xFFFF, 0) + 1
            if c == i % LANES:
                d = sha3_256(message(point(origins[c], i)))
                kn = sum(((int.from_bytes(d[8 * y:8 * y + 8], 'little') ^ (RC[5] if y == 0 else 0)) & (1 << 35) - 1)
                         << STRIDE * y for y in range(4))
                st['checks'] += 1
                st['mismatch'] += kn | MARK != key
            if c == i == 0:
                key0 = key
            t1, x1 = K[0], REGS['X']
            r = probe(key)
            if r == 'cap':
                need(K[0] - t1 == 13 and WRK[FCW - WB] == CAPF, 'false pass halted at the cap after 13 operations')
                found = ('cap', None, None, None, None, None)
                break
            if r is not None:
                REGS['M'] += 1
                v = verify(r, [reg[T] for T in CACHED] + [x], i)
                if v[0] != 'differ':
                    found = v
                    break
                reg, x = dict(zip(CACHED, v[5])), v[5][-1]
                REGS['v'] = ADD(REGS['v'], 1)
                REGS['cid'] = REGS['v'] & M128
            need(K[0] - t1 == (10 if r is not None else 14 if REGS['X'] > x1 else 6), 'table path 6, 14 or 10')
        if found:
            break
        dm, dx = REGS['M'] - m0, REGS['X'] - x0
        need(SECS['fes'][0] - f0 == FCOSET, 'FES count per coset')
        need(SECS['table'][0] - t0 == 6 * ((1 << N_DIR) - dm - dx) + 14 * dx + 10 * dm, 'table 6 / 14 / 10')
    if not found:
        sec('leader')
        BR(EQ(SHR(REGS['cid'], 48), G))
        need(SECS['leader'][0] == 11 * LANES + 5, 'leader 11 per coset, group control 5')
        need(SECS['fes'][0] == LANES * FCOSET + 3 and SECS['cht'][0] == 6 * QR and
             SECS['buf'][0] == 2 * len(SUBS) * LANES, 'FES (256 cosets, h and F 3), chi 6 per candidate, frame copies')
        need(REGS['I'] == QR - REGS['M'] and REGS['cid'] == (h << 48) + QR, 'sparse inserts, identifiers')
        need(WRK[FCW - WB] == REGS['M'] + REGS['X'] < CAPF, 'F counts verifications and false passes, below the cap')
        sec('vcheck')
        k1 = K[0]
        r = probe(key0)
        REGS['v'] = ADD(REGS['v'], 1)
        REGS['cid'] = REGS['v'] & M128
        need(r == h << 48 and K[0] - k1 == 10, 'valid hit 10 operations')
        k1, saved, WRK[FCW - WB] = K[0], WRK[FCW - WB], 0
        REGS['cid'] = (h << 48) + (80 << N_DIR) + 1
        REGS['v'] = REGS['R_HI'] | REGS['cid']
        v = verify(r, [reg[T] for T in CACHED] + [x], 1)
        WRK[FCW - WB] = saved
        for t0, dd, tt in ((origins[0], v[3], v[1]), (origins[80] ^ W40[0], v[4], v[2])):
            need(tt == t0, 'reconstructed source')
            need(b''.join(w.to_bytes(8, 'little') for w in dd) == sha3_256(message(tt)), 'reconstructed digest')
        need(v[0] == 'differ' and CALLS[0] == 0 and K[0] - k1 <= 2428, 'verification <= 2428, no permutation call')
        forms_setup()
        forms_fes(K24)
    need(SECS['verify'][0] <= 2428 * REGS['M'], 'verification bound')
    need(found or (c, i) == (LANES - 1, NST), 'all cosets and Gray points')
    need(SECS['once'][0] == 7666, 'once ops 7666')   # checked, not reported (<= 16 observations)
    obs = {'fes_ops': SECS['fes'][0], 'buffer_reads': SECS['buf'][0],
           'chi_transpose_ops': SECS['cht'][0] + SECS['rtr'][0],
           'table_ops': SECS['table'][0], 'sparse_inserts': REGS['I'],
           'in_range_mismatches': REGS['X'], 'key_matches': REGS['M'], 'leader_ops': SECS['leader'][0],
           'setup_group_ops': SECS['sgroup'][0], 'setup_point_ops': SECS['spoint'][0],
           'transform_phase_ops': SECS['transform'][0] + SECS['phase'][0],
           'verify_check_ops': SECS['vcheck'][0], 'perm_calls': CALLS[0], 'native_checks': st['checks'],
           'key_mismatch': st['mismatch']}
    out = [None] * LANES
    if found and found[0] == 'equal':
        ma, mb = message(found[1]), message(found[2])
        if ma != mb and sha3_256(ma) == sha3_256(mb):
            out[0] = (ma.hex(), mb.hex())
    if mode is None:
        return [dict(own_pairs16=sum(n * (n - 1) // 2 for n in o.values()), **obs) for o in own], out
    del obs['buffer_reads'], obs['sparse_inserts']
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
         'hcoset-cross16': ('cross16', MASK16), 'hcoset-filter8': ('filter8', MASK16)}


def filter8(K24, origins):    # proof.md Section 12.4: the survivors of the eight-bit filter; beside the algorithm, not counted
    sv = [n for n, k in enumerate(K24) if k & 255 == 1]          # key index n = 256 i + c: lane c, Gray point i
    need(422 <= len(sv) <= 602, 'survivor count')
    byv = {}
    for n in sv:
        byv.setdefault(K24[n] >> 8 & 255, []).append(n)
    npair, e = sum(len(v) * (len(v) - 1) // 2 for v in byv.values()), len(sv) * (len(sv) - 1) / 512
    need(abs(npair - e) <= 4 * e ** .5, 'pairs of survivors on event bits 8..15')
    out = [None] * LANES
    for t, (a, b) in enumerate([(v[j], v[j + 1]) for u, v in sorted(byv.items()) for j in range(len(v) - 1)][:LANES]):
        ma, mb = (message(point(origins[n % LANES], n // LANES)) for n in (a, b))
        da, db = sha3_256(ma), sha3_256(mb)
        need(ma != mb and all(da[8 * x] & 3 == 0 == db[8 * x] & 3 and (da[8 * x] ^ db[8 * x]) & 15 == 0 for x in range(4)),
             'returned survivor pair')
        out[t] = (ma.hex(), mb.hex())
    return {'survivors8': len(sv), 'pairs8_survivors': npair}, out


def premise_test(K24, origins, mode):   # proof.md Section 12.2; beside the algorithm, not counted
    col = [K24[c::LANES] for c in range(LANES)]   # keys of coset lane c in Gray order
    w16 = sum(pairs([k & 0xFFFF for k in v]) for v in col)
    w24 = sum(pairs(list(v)) for v in col)
    counts = {'pairs16_within': w16, 'pairs16_cross': pairs([k & 0xFFFF for k in K24]) - w16,
              'pairs24_cross': pairs(list(K24)) - w24}
    for name, (lo, hi) in PASS.items():
        need(lo <= counts[name] <= hi, name + ' inside its pass interval')
    if mode == 'filter8':
        return filter8(K24, origins)
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
