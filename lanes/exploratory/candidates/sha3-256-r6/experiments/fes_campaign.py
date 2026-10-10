"""Reduced run of the campaign CAMP of proof.md Section 8 on the exact target sha3-256-r6-prefix-v1 (SHA3-256, prefix
rounds 0 to 5, zero state, rate 136 bytes, suffix 0x06, full 256-bit digest). Python standard library only. Reads one
organizer request (JSON) on stdin and writes one JSON document on stdout.

Once per request: the 6-round hash below must match two known-answer digests of the organizer reference and, at 24
rounds, hashlib.sha3_256; rank(W40) = 40; all 780 basis-pair two-round polarizations of Lemma 3 must vanish.

Trials 256g .. 256g + 255 form one group: group index h = int(seed of the group's first trial, 16) mod G, trial k is
coset lane c = k mod 256, coset j = 256 h + c. Its origin t_j is fresh randomness of Section 6.1: the leader step
draws two random words (RAND, one charged primitive each) from the trial's own coins, here the two halves of
SHAKE-256 of the trial's seed; this seed expansion only makes the run reproducible and is not the attack's randomness
source. The group executes the schedule of Sections 5 to 7 at reduced size: the first 2^N_DIR Gray points of each
coset (directions w_0 .. w_{N_DIR-1}), degree bound 8, all 175 planes, the full 140-bit key and the sparse-set table
of Section 7. Every operation of those sections runs through the counting machine below (one call = one charged
256-bit primitive; no permutation call is made), and the program stops unless each executed count equals the formula
of proof.md: 11 per coset leader and 5 per group for control; the bit-sliced setup of Section 6.3 (all 256 lanes in
each word), 13616 for the transpose of the 256 origins into 320 bitplanes and 960 for the constant lanes of the input
frame per group, and at every point S 640 + popcount(w(S)) for the input, 73842 for rounds 0 to 4 and 4265 for the
round-5 linear step into the coefficient record; 4 * 175 per transform pair and 2 * 175 per phase term; the
plane-major FES of Section 5.3 at every plane and Gray step and its closed sum per plane (61 records in registers,
values into the buffer, the last store of the other records omitted) with 2 per group for the spill, every buffer
word written once, 175 buffer reads per point i >= 1 and 175 loads at point zero, 4664 per point for chi and
transpose, 6, 9 or 8 table operations per candidate (miss with the bound test failing, miss after the dense test,
valid hit), 7660 for the byte tables, 88 + 1452 per message rebuilt in verification and at most 3127 operations per
verification. The bitplanes must equal the origins, and the counted setup values must equal, at every point and
lane, an independent evaluation that is not counted (rounds 0 and 1 by Lemma 3). Sparse words start with arbitrary
content: a never-written sparse word reads as a fixed pseudo-random function of its address, either a word of at
least 2^255 or h 2^48 plus a value below 2 QR, so fresh keys often reach the dense test. Reading a never-written work,
dense or coset word stops the program. Beside the algorithm (not counted): at point i the message of lane i mod 256
is hashed natively and its 140 key bits, with bit 140 set, are compared with the emitted key word (key_mismatch);
after the run, the key of the first candidate is probed again (a valid hit) and the verification routine is run on
it. Also beside the algorithm, own_pairs16 counts the unordered pairs of the trial's own 2^N_DIR candidates whose
emitted keys agree on their low 16 bits (bits 0..3 of digest lanes 0..3); uniform digests give C(512, 2)/2^16 = 1.996
per trial. Nothing about cost is inferred from a run.
"""
import sys, json, hashlib
from math import comb, isqrt

N_DIR, DEG, LANES, NPL = 9, 8, 256, 175
G = 1202736947187009950184717                    # groups of the full campaign (Section 9)
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
CSB, WB = 1 << 130, 1 << 131                     # coset record of coset j at CSB + 2j; work region. DENSE[x] is word x
WF, INT, PL, TW = WB, WB + 512, WB + 656, WB + 976   # (x < Q); SPARSE[k] is the key word k itself (bit 140 set). Work:
INF = TW + 3                                     # working frames, 144 tile words, 320 bitplanes, 3 transpose words,
RB, DW = INF + 1600, INF + 4800                  # input frame (bit z of lane l at INF + 64 l + z), round buffers RB and
ACO = DW + 320                                   # RB + 1600, D words; coefficient record A[S] at ACO + 175 IDX[S]
TABB = ACO + NPL * len(SUBS)                     # (current frame = A[{}]); derivative record tab[T] at TABB + 175 IDX[T]
TBY = TABB + NPL * len(SUBS)                     # byte table b, entry v (two words) at TBY + 512 b + 2 v
FCW, HSP, SPL = TBY + 2560, TBY + 2561, TBY + 2562   # count F (Section 7), spill word of h, spill frame (17)
XB = SPL + 17                                    # buffer: plane p at Gray point i >= 1 at XB + NST p + i - 1
WEND = XB + NPL * NST
CACHED = list(range(1, 32)) + [32 | t for t in range(2, 32)]   # the 61 records held in registers (Section 5.3)
CSET = set(CACHED)


def cap(num, den):       # Section 7: r = ceil(mu), R = r + ceil(sqrt(4096 r))
    r = -(-num // den)
    s = isqrt(4096 * r)
    return r + s + (s * s < 4096 * r)


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
CAPF = cap(QR * (QR - 1), 1 << 141)              # verification cap (full size R140)
GM = 0x9E3779B97F4A7C15F39CC0605CEDC8341082276BF3A27251F86C6A11D0C18E95   # odd multiplier of the garbage stand-in
J_D = sum(S.bit_count() for S in SUBS)
V_D = sum(comb(j, r) * comb(N_DIR - j, r) * sum(comb(r, k) for k in range(min(r, DEG - j) + 1))
          for j in range(1, DEG + 1) for r in range(min(j, N_DIR - j) + 1))

# ---- counting machine: every call is one charged 256-bit primitive of the current section ----
SECS = {s: [0] for s in ('once', 'leader', 'sgroup', 'spoint', 'transform', 'phase', 'zero', 'fes', 'buf', 'cht',
                          'table', 'verify', 'vcheck')}
K = SECS['once']
SPARSE, DENSE, WRK, CREC, CALLS, GBASE = {}, {}, [], {}, [0], [0]


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


def LDD(a):
    K[0] += 1
    v = DENSE.get(a)
    if v is None:
        raise SystemExit('check failed: read of a never-written dense word')
    return v


def STD(a, v): K[0] += 1; DENSE[a] = v


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


# ---- Section 7: the scalar six-round evaluation of verification (242 per round) and its lane initialization (26) ----
def rot(v, s):
    return AND(OR(SHL(v, s), SHR(v, 64 - s)), M64)


def linear(L):           # theta, rho, pi: 20 + 25 + 25 + 96 = 166; pi is register renaming
    C = [XOR(XOR(XOR(XOR(L[x], L[x + 5]), L[x + 10]), L[x + 15]), L[x + 20]) for x in range(5)]
    D = [XOR(C[(x - 1) % 5], rot(C[(x + 1) % 5], 1)) for x in range(5)]
    B = [0] * 25
    for i in range(25):
        x, y = i % 5, i // 5
        v = XOR(L[i], D[x])
        B[y + 5 * ((2 * x + 3 * y) % 5)] = rot(v, RHO[i]) if RHO[i] else v
    return B


def rnd(L, r):           # 166 + chi 75 + iota 1 = 242
    B = linear(L)
    A = [XOR(B[i], AND(NOT(B[i - i % 5 + (i + 1) % 5]), B[i - i % 5 + (i + 2) % 5])) for i in range(25)]
    A[0] = XOR(A[0], RC[r])
    return A


ZL = (5, 6, 7, 8, 9, 15, 17, 18, 19, 20, 21, 22, 23, 24)


def lane_init(w0, w1):   # 26: lanes 0-3 from w0 (6), lane 4 is w1 itself, five copies, the padding lane, 14 zero lanes
    need(w1 >> 64 == 0, 'second source word below 2^64')
    L = [0] * 25
    L[0], L[1], L[2] = AND(w0, M64), AND(SHR(w0, 64), M64), AND(SHR(w0, 128), M64)
    L[3], L[4] = SHR(w0, 192), w1                # w0 >> 192 is below 2^64; w1 is already the 64-bit lane 4
    for k in range(5):
        L[10 + k] = MOV(L[k])
    L[16] = MOV(0x86 << 56)
    for k in ZL:
        L[k] = MOV(0)
    return L


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
def al(a):               # round 0 reads lanes 10..14 from the stored words of lanes 0..4 (equal in every block A(t))
    return a - 640 if 640 <= a < 960 else a


COLS = [[CIDX[64 * x + z] for x in range(5)] for z in range(64)]   # slice z: the 5 words of each column x
COLS0 = [[tuple(map(al, c)) for c in cz] for cz in COLS]
SLICE = [[SRC[64 * l + z] for l in range(25)] for z in range(64)]   # slice z: (source word, D word) of output lane l
SLICE0 = [[(al(s), d) for s, d in sz] for sz in SLICE]
FRAME = [(64 * l + z, M256 if l == 16 and z in (57, 58, 63) else 0) for l in (5, 6, 7, 8, 9, 15, 16, 17, 18, 19, 20, 21,
                                                                         22, 23, 24) for z in range(64)]


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


def frame():             # constant lanes of the input frame, once per group: 15 x 64 STOREs (960); lane 16 holds the
    for a, v in FRAME:   # padding 0x86 in bits 57, 58, 63; lanes 10..14 are never stored
        STW(INF + a, v)


def load_input(w):       # point S: plane k, NOT where bit k of w(S) is set, into bit k mod 64 of lane k div 64: 640 + pop
    for k in range(320):
        v = LDW(PL + k)
        STW(INF + k, NOT(v) if w >> k & 1 else v)


def dstep(src, cols):    # theta's D words: the column parities of slice 63 (45), then per slice z its parities (45) and
    def col(t):          # D[x][z] = C[x - 1][z] XOR C[x + 1][z - 1], 5 XORs and 5 STOREs: 45 + 64 x 55 = 3565
        c = LDW(src + t[0])
        for a in t[1:]:
            c = XOR(c, LDW(src + a))
        return c
    prev = [col(t) for t in cols[63]]
    for z in range(64):
        cur = [col(t) for t in cols[z]]
        for x in range(5):
            STW(DW + 64 * x + z, XOR(cur[x - 1], prev[(x + 1) % 5]))
        prev = cur


def bround(src, dst, r):  # round r: 3565, then per slice z 25 x (LOAD, LOAD, XOR) for theta, rho and pi, 25 x (NOT,
    dstep(src, COLS0 if r == 0 else COLS)       # AND, XOR) for chi into 25 more registers, iota as one NOT of lane 0
    for z in range(64):                          # at each set bit of RC[r], 25 STOREs: 3565 + 64 x 175 + |RC[r]|
        B = [XOR(LDW(src + s), LDW(DW + d)) for s, d in (SLICE0 if r == 0 else SLICE)[z]]
        A = [XOR(B[i], AND(NOT(B[i - i % 5 + (i + 1) % 5]), B[i - i % 5 + (i + 2) % 5])) for i in range(25)]
        if RC[r] >> z & 1:
            A[0] = NOT(A[0])
        for i in range(25):
            STW(dst + 64 * i + z, A[i])


def linear5(src, base):  # round-5 theta, rho, pi into the 175 plane words of A[S]: 3565 + 175 x (LOAD, LOAD, XOR, STORE)
    dstep(src, COLS)
    for p, (s, d) in enumerate(SRC_SEL):
        STW(base + p, XOR(LDW(src + s), LDW(DW + d)))


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


def build_tables():      # ONCE: entry v of byte table b is the XOR of w_{8b+k} over the bits k of v (two words);
    for b in range(5):   # 2 zero STOREs per table, then per entry LOAD, XOR, STORE per word: 5 x (2 + 255 x 6) = 7660
        base = TBY + 512 * b
        STW(base, 0)
        STW(base + 1, 0)
        for v in range(1, 256):
            k = (v & -v).bit_length() - 1
            u = base + 2 * (v ^ (1 << k))
            STW(base + 2 * v, XOR(LDW(u), WW[8 * b + k][0]))
            STW(base + 2 * v + 1, XOR(LDW(u + 1), WW[8 * b + k][1]))


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


def recon(cid):          # source and digest of candidate cid = (h << 48) | (i << 8) | e: decode (17), five byte-table
    k0 = K[0]            # lookups of g(i) (9 each), lane initialization (26), six rounds in word operations (1452)
    e = AND(cid, 255)
    i = AND(SHR(cid, 8), (1 << 40) - 1)
    c = OR(SHL(AND(e, 15), 4), SHR(e, 4))       # emission index e = 16 l + tau -> lane c = 16 tau + l
    a = ADD(SHL(OR(SHL(SHR(cid, 48), 8), c), 1), CSB)
    w0, w1 = LDC(a), LDC(ADD(a, 1))
    g = XOR(i, SHR(i, 1))
    for b in range(5):                           # bytes 0..4 of the 40-bit g(i)
        u = ADD(SHL(AND(SHR(g, 8 * b), 255), 1), TBY + 512 * b)
        w0, w1 = XOR(w0, LDW(u)), XOR(w1, LDW(ADD(u, 1)))
    L = lane_init(w0, w1)
    need(K[0] - k0 == 88, 'rebuild 88 operations')
    k0 = K[0]
    for r in range(6):
        L = rnd(L, r)
    need(K[0] - k0 == 1452, 'six-round evaluation 1452 operations')
    return w0 | w1 << 256, L[:4]


def verify(cold, U):     # earlier candidate cold against the current one (the cid register); live: the 16 column keys
    prev = K             # U and cid; result 'cap', 'equal' or 'differ'
    sec('verify' if prev is not SECS['vcheck'] else 'vcheck')
    f = ADD(LDW(FCW), 1)                         # the verification count F is a memory word: LOAD, ADD, STORE
    STW(FCW, f)
    out = ('cap', None, None, None, None)
    if not BR(EQ(f, CAPF)):
        live = U + [REGS['cid']]
        for k, v in enumerate(live):             # spill: the scalar schedule then has the register file
            STW(SPL + k, v)
        ta, da = recon(cold)
        tb, db = recon(REGS['cid'])
        st = 'equal'
        for k in range(4):
            if not BR(EQ(da[k], db[k])):
                st = 'differ'
                break
        need([LDW(SPL + k) for k in range(17)] == live, 'registers restored')
        out = (st, ta, tb, da, db)
    globals()['K'] = prev
    return out


def probe(k):            # the key word k (bit 140 set) is its own SPARSE address; DENSE[cid] is word cid. 6 (bound test
    cid = REGS['cid']    # fails), 9 (dense test fails), each with the insertion and the increment; a valid hit returns
    s = LDS(k)           # after 7 and its increment follows the verification (8)
    STD(cid, k)
    if BR(LT(s, cid)):
        if BR(EQ(LDD(s), k)):
            return s                             # valid hit: the first candidate with this key
        REGS['X'] += 1
    STS(k, cid)
    REGS['I'] += 1
    REGS['cid'] = ADD(cid, 1)
    return None


REGS = {'h': 0, 'cid': 0, 'M': 0, 'X': 0, 'I': 0}


def run_group(h, seeds):
    global SPARSE, DENSE, WRK, CREC
    for s in SECS.values():
        s[0] = 0
    CALLS[0] = 0
    SPARSE, DENSE, WRK, CREC = {}, {}, [None] * (WEND - WB), {}
    GBASE[0] = h << 48
    REGS.update(M=0, X=0, I=0)
    sec('once')                                  # one-time control (group index, count F) and the byte tables
    REGS['h'] = MOV(h)
    STW(FCW, 0)
    build_tables()
    need(SECS['once'][0] == 2 + 7660, 'one-time control 2 and byte tables 7660')
    per, origins = leaders(seeds)
    for c in range(LANES):
        j = 256 * h + c
        need(CREC[CSB + 2 * j] | CREC[CSB + 2 * j + 1] << 256 == origins[c] < 1 << 320, 'coset record')
        need(per[c] == 11, 'leader count 11 per coset')
    own = [{} for _ in range(LANES)]             # beside the algorithm: low 16 key bits of each lane's candidates
    sec('fes')                                   # the group index h, the one value live across the setup and the FES
    STW(HSP, REGS['h'])                          # phase, goes to a fixed word here and comes back after the FES phase
    REGS['h'] = None                             # (2 per group, Section 5.3): the setup has all 64 registers
    sec('sgroup')                                # Section 6.3, once per group: bitplanes and the constant lanes
    transpose()
    P = [sum((t >> k & 1) << c for c, t in enumerate(origins)) for k in range(320)]
    need(SECS['sgroup'][0] == 13616 and WRK[PL - WB:PL - WB + 320] == P, 'transpose 13616, bitplanes equal the origins')
    frame()
    need(SECS['sgroup'][0] == 13616 + 960, 'constant lanes 960')
    sec('spoint')                                # every point S, |S| <= 8, in order of increasing |S|
    pop = 0
    for S in SUBS:
        w = 0
        for b in range(N_DIR):
            if S >> b & 1:
                w ^= W40[b]                      # w(S) is fixed at generation time: the NOTs of the input code
        k0 = K[0]
        load_input(w)
        k1 = K[0]
        src = INF
        for r in range(5):                       # rounds 0..4: input frame -> RB -> RB + 1600 -> RB -> RB + 1600 -> RB
            bround(src, RB + 1600 * (r & 1), r)
            src = RB + 1600 * (r & 1)
        k2 = K[0]
        linear5(RB, ACO + NPL * IDX[S])
        need((k1 - k0, k2 - k1, K[0] - k2) == (640 + w.bit_count(), 73842, 4265), 'input, rounds 0..4, linear step')
        pop += w.bit_count()
    need(pop == POP and SECS['spoint'][0] == 78747 * len(SUBS) + POP, 'setup points: 78747 P + popcount sum')
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
    sec('leader')
    REGS['cid'] = SHL(REGS['h'], 48)             # group control: the group's first identifier
    keys = [0] * LANES
    st = {'checks': 0, 'mismatch': 0}
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
                need(REGS['cid'] == (h << 48) | (i << 8) | (16 * l + tau), 'identifier of candidate (h, i, e)')
                keys[16 * tau + l] = U[tau]
                o = own[16 * tau + l]
                o[U[tau] & 0xFFFF] = o.get(U[tau] & 0xFFFF, 0) + 1
                t1, x1 = K[0], REGS['X']
                r = probe(U[tau])
                if r is not None:                # valid hit: full verification against the stored candidate
                    REGS['M'] += 1
                    v = verify(r, U)
                    if v[0] != 'differ':
                        found = v
                        break
                    REGS['cid'] = ADD(REGS['cid'], 1)
                need(K[0] - t1 == (8 if r is not None else 9 if REGS['X'] > x1 else 6), 'table path 6, 9 or 8')
            sec('cht')
            if found:
                break
        if found:
            break
        if i == 0:
            key0 = keys[0]
        dm, dx = REGS['M'] - m0, REGS['X'] - x0
        need(SECS['cht'][0] - c0 == 4664, 'chi/transpose 4664 per point')
        need(SECS['table'][0] - t0 == 6 * (LANES - dm - dx) + 9 * dx + 8 * dm, 'table 6 / 9 / 8 per candidate')
        need((SECS['buf'][0] - b0, SECS['zero'][0] - z0) == ((NPL, 0) if i else (0, NPL)),
             '175 buffer reads per point i >= 1, 175 point-zero loads')
        c = i % LANES                            # check beside the algorithm, not counted
        g, t = i ^ i >> 1, origins[c]
        for b in range(N_DIR):
            if g >> b & 1:
                t ^= W40[b]
        d = sha3_256(message(t))
        kn = sum(((int.from_bytes(d[8 * x:8 * x + 8], 'little') ^ (RC[5] if x == 0 else 0)) >> z & 1) << 4 * z + x
                 for z in range(35) for x in range(4))
        st['checks'] += 1
        st['mismatch'] += kn | 1 << 140 != keys[c]
    if not found:
        sec('leader')                            # group control: next group index (cid >> 48), compare with G, branch
        BR(EQ(SHR(REGS['cid'], 48), G))
        need(SECS['leader'][0] == 11 * LANES + 5, 'leader 11 per coset, group control 5')
        need(SECS['cht'][0] == 4664 << N_DIR and SECS['buf'][0] == NPL * NST, 'chi/transpose and buffer totals')
        need(REGS['I'] == QR - REGS['M'] and REGS['cid'] == (h << 48) + QR, 'sparse inserts, identifiers')
        sec('vcheck')                            # beside the run: probe the first candidate's key again (valid hit,
        k1, saved = K[0], WRK[FCW - WB]          # 8 operations), then verify it against candidate (i, e) = (1, 5)
        r = probe(key0)
        REGS['cid'] = ADD(REGS['cid'], 1)
        need(r == h << 48 and K[0] - k1 == 8, 'valid hit 8 operations')
        k1, WRK[FCW - WB] = K[0], 0
        REGS['cid'] = (h << 48) | (1 << 8) | 5
        v = verify(r, U)
        WRK[FCW - WB] = saved
        for t0, dd, tt in ((origins[0], v[3], v[1]), (origins[5 << 4] ^ W40[0], v[4], v[2])):
            need(tt == t0, 'reconstructed source')
            need(b''.join(w.to_bytes(8, 'little') for w in dd) == sha3_256(message(tt)), 'reconstructed digest')
        need(v[0] == 'differ' and CALLS[0] == 0 and K[0] - k1 <= 3127, 'verification <= 3127, no permutation call')
    need(SECS['verify'][0] <= 3127 * REGS['M'], 'verification bound')
    need(i + 1 == 1 << N_DIR or found, 'all Gray points')
    need(SECS['zero'][0] == 175 and SECS['once'][0] == 7662, 'point-zero loads 175, once ops 7662')  # checked, not reported (<= 16 observations)
    obs = {'fes_ops': SECS['fes'][0], 'buffer_reads': SECS['buf'][0], 'chi_transpose_ops': SECS['cht'][0],
           'table_ops': SECS['table'][0], 'sparse_inserts': REGS['I'],
           'in_range_mismatches': REGS['X'], 'key_matches': REGS['M'], 'leader_ops': SECS['leader'][0],
           'setup_group_ops': SECS['sgroup'][0], 'setup_point_ops': SECS['spoint'][0],
           'transform_phase_ops': SECS['transform'][0] + SECS['phase'][0],
           'verify_check_ops': SECS['vcheck'][0], 'perm_calls': CALLS[0], 'native_checks': st['checks'],
           'key_mismatch': st['mismatch']}
    pair = None
    if found and found[0] == 'equal':
        ma, mb = message(found[1]), message(found[2])
        if ma != mb and sha3_256(ma) == sha3_256(mb):
            pair = (ma.hex(), mb.hex())
    return obs, [sum(n * (n - 1) // 2 for n in o.values()) for o in own], pair


def main():
    req = json.loads(sys.stdin.read())
    setup_checks()
    trials = req['trials']
    out = []
    for g in range(0, len(trials), LANES):
        grp = trials[g:g + LANES]
        seeds = [t['seed'] for t in grp] + [grp[0]['seed'] + '/%d' % c for c in range(len(grp), LANES)]
        obs, ownp, pair = run_group(int(grp[0]['seed'], 16) % G, seeds)
        for c, t in enumerate(grp):
            a, b = pair if pair else (None, None)
            out.append({'trial': t['trial'], 'message_a_hex': a, 'message_b_hex': b,
                        'observations': dict(own_pairs16=ownp[c], **obs)})
            pair = None
    sys.stdout.write(json.dumps({'schema_version': 1, 'trials': out}, separators=(',', ':')))


if __name__ == '__main__':
    main()
