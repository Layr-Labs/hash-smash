"""Reduced run of the campaign CAMP of proof.md Section 8 on the exact target sha3-256-r6-prefix-v1 (SHA3-256, prefix
rounds 0 to 5, zero state, rate 136 bytes, suffix 0x06, full 256-bit digest). Python standard library only. Reads one
organizer request (JSON) on stdin and writes one JSON document on stdout.

Once per request: the 6-round hash below must match two known-answer digests of the organizer reference and, at 24
rounds, hashlib.sha3_256; rank(W40) = 40; all 780 basis-pair two-round polarizations of Lemma 3 must vanish.

Trials 256g .. 256g + 255 form one group: group index h = int(seed of the group's first trial, 16) mod G, trial k is
coset lane c = k mod 256, coset j = 256 h + c. Its origin t_j is fresh randomness of Section 6.1: the leader step
draws two random words (RAND, one charged primitive each) from the trial's own coins, here the two halves of
SHAKE-256 of the trial's seed; this seed expansion only makes the run reproducible and is not the attack's randomness
source. The group executes the
schedule of Sections 5 to 7 at reduced size: the first 2^N_DIR Gray points of each coset (directions w_0 ..
w_{N_DIR-1}), degree bound 8, all 175 planes, the full 140-bit key and the sparse-set table of Section 7. Every
operation of those sections runs through the counting machine below (one call = one charged 256-bit primitive; PERM =
one six-round permutation call), and the program stops unless each executed count equals the formula of proof.md:
525 L(i) + 97 per Gray step i >= 1, 175 loads at point zero, 4656 per point for chi and transpose, 11, 15 or 10 table
operations per candidate (miss with the bound test failing, miss after the dense test, valid hit), 11 per coset
leader (within the charged 544) and 5 per group for control, 1416 + 2|S| per direct evaluation, 1282 per
plane conversion, 4 * 175 per transform pair, 2 * 175 per phase term, at most 844 operations and two PERM calls per
verification. Setup values of lanes 1..255 at points S != {} come from a bit-sliced evaluation (a stand-in, not
counted) which must equal the counted schedule on lane 0 at every point and on all lanes at S = {}. Sparse words start
with arbitrary content: a never-written sparse word reads as a fixed pseudo-random word of its address whose index
field lies below 2 QR, so fresh keys often reach the dense test. Reading a never-written work, dense or coset word
stops the program. Beside the algorithm (not counted): at point i the message of lane i mod 256 is hashed natively
and its 140 key bits are compared with the emitted key (key_mismatch); after the run, the key of the first candidate
is probed again (a valid hit) and the verification routine is run on it. Also beside the algorithm, own_pairs16 counts
the unordered pairs of the trial's own 2^N_DIR candidates whose emitted keys agree on their low 16 bits (bits 0..3 of
digest lanes 0..3); uniform digests give C(512, 2)/2^16 = 1.996 per trial. Nothing about cost is inferred from a run.
"""
import sys, json, hashlib
from math import comb, isqrt

N_DIR, DEG, LANES, NPL = 9, 8, 256, 175
G = 1202983983186596773302061                    # groups of the full campaign (Section 9)
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


# ---- one-time preprocessing (ONCE): plane order, record index, masks, layout ----
WW = [(v & M256, v >> 256) for v in W40]         # two-word constants of w_0 .. w_39
PLANES = [(p % 5, p // 5) for p in range(NPL)]   # plane p = B[x, z]: x = p mod 5, z = p div 5 (z < 35)
RET = [x == 0 or (x == 1 and z < 4) for x, z in PLANES]   # the 39 retained current values
MASK = {s: sum(((1 << s) - 1) << (2 * s * k) for k in range(128 // s)) for s in (1, 2, 4, 8, 16, 32, 64, 128)}
SUBS = sorted((S for S in range(1 << N_DIR) if S.bit_count() <= DEG), key=lambda S: (S.bit_count(), S))
IDX = {S: k for k, S in enumerate(SUBS)}
QR = LANES << N_DIR                              # candidates of the reduced run
SPB, DNB = 1 << 200, 1 << 201                    # SPARSE[k] at SPB | k (k < 2^140); DENSE[i] at DNB | i
CSB, WB = 1 << 90, 1 << 91                       # coset-start record of coset j at CSB + 2j (j < 256 G); work region:
WF, SF, INT = WB, WB + 512, WB + 1024            # working frames, scalar frame, 144 intermediate tile words
ACO = WB + 1168                                  # coefficient record A[S] at ACO + 175 IDX[S]; current frame = A[{}]
TABB = ACO + NPL * len(SUBS)                     # derivative record tab[T] at TABB + 175 IDX[T]
WEND = TABB + NPL * len(SUBS)


def cap(num, den):       # Section 7: r = ceil(mu), R = r + ceil(sqrt(4096 r))
    r = -(-num // den)
    s = isqrt(4096 * r)
    return r + s + (s * s < 4096 * r)


CAPF = cap(QR * (QR - 1), 1 << 141)              # verification cap (full size R140)
GM = 0x9E3779B97F4A7C15F39CC0605CEDC8341082276BF3A27251F86C6A11D0C18E95   # odd multiplier of the garbage stand-in
SUML = sum(comb(N_DIR, k) * min(DEG, k) for k in range(1, N_DIR + 1))
J_D = sum(S.bit_count() for S in SUBS)
V_D = sum(comb(j, r) * comb(N_DIR - j, r) * sum(comb(r, k) for k in range(min(r, DEG - j) + 1))
          for j in range(1, DEG + 1) for r in range(min(j, N_DIR - j) + 1))

# ---- counting machine: every call is one charged 256-bit primitive of the current section ----
SECS = {s: [0] for s in ('once', 'leader', 'eval', 'conv', 'transform', 'phase', 'zero', 'fes', 'cht', 'table',
                          'verify', 'vcheck')}
K = SECS['once']
SPARSE, DENSE, WRK, CREC, CALLS = {}, [], [], {}, [0]


def sec(name):
    global K
    K = SECS[name]


def LDS(a):              # sparse word; a never-written one holds arbitrary content (a fixed function of its address)
    K[0] += 1
    v = SPARSE.get(a)
    if v is None:
        x = (a * GM) & M256
        x ^= x >> 127
        v = x >> 128 << 128 | (x & M128) % (2 * QR)
    return v


def STS(a, v): K[0] += 1; SPARSE[a] = v


def LDD(a):
    K[0] += 1
    v = DENSE[a - DNB]
    if v is None:
        raise SystemExit('check failed: read of a never-written dense word')
    return v


def STD(a, v): K[0] += 1; DENSE[a - DNB] = v


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
def PERM(L): CALLS[0] += 1; return keccak_f(L, 6)   # one six-round permutation call (one unit, 1626 operations)


def coins(seed):         # reproducible stand-in for fresh coins: SHAKE-256 of the trial's seed, two 256-bit words
    s = hashlib.shake_256(seed.encode()).digest(64)
    return iter((int.from_bytes(s[:32], 'little'), int.from_bytes(s[32:], 'little')))


# ---- Section 6: scalar direct evaluation (1416 + 2|S|) and vertical conversion (1282 per plane) ----
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


def lane_init(w0, w1):   # 28: five extractions (8), five copies, the padding lane, 14 zero lanes
    L = [0] * 25
    L[0], L[1], L[2] = AND(w0, M64), AND(SHR(w0, 64), M64), AND(SHR(w0, 128), M64)
    L[3], L[4] = AND(SHR(w0, 192), M64), AND(w1, M64)
    for k in range(5):
        L[10 + k] = MOV(L[k])
    L[16] = MOV(0x86 << 56)
    for k in ZL:
        L[k] = MOV(0)
    return L


def evaluate(c, S):      # lane c at point S: rounds 0-4 and the round-5 linear step; W0, V into the scalar frame
    w0, w1 = LDW(WF + 2 * c), LDW(WF + 2 * c + 1)
    for b in range(N_DIR):
        if S >> b & 1:   # the basis constants of S are immediates of the generated code
            w0, w1 = XOR(w0, WW[b][0]), XOR(w1, WW[b][1])
    L = lane_init(w0, w1)
    for r in range(5):
        L = rnd(L, r)
    B = linear(L)
    W0 = OR(OR(OR(B[0], SHL(B[1], 64)), SHL(B[2], 128)), SHL(B[3], 192))
    V = OR(B[4], SHL(B[0], 64))
    STW(SF + 2 * c, W0)
    STW(SF + 2 * c + 1, V)
    return W0, V


def convert(S):          # 175 planes of point S from the scalar frame: MOV, 256 x (LD SHR AND SHL OR), ST
    base = ACO + NPL * IDX[S]
    for p, (x, z) in enumerate(PLANES):
        off, pos = (0, 64 * x + z) if x < 4 else (1, z)
        acc = MOV(0)
        for c in range(LANES):
            acc = OR(acc, SHL(AND(SHR(LDW(SF + 2 * c + off), pos), 1), c))
        STW(base + p, acc)


def leaders(h, seeds):   # Section 6.2: fresh origin t_j from two random words into the global record and the frame
    sec('leader')
    per, origins = [], []
    H8 = SHL(h, 8)                               # group control: H8 = h << 8 and the ID register HB = h << 176
    REGS['HB'] = SHL(h, 176)
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
    BR(EQ(ADD(h, 1), G))                         # group control: next group or halt
    return per, origins


# ---- bit-sliced stand-in for the setup values (not counted): plane 64 lane + z, one bit per coset lane ----
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


def bs_round(A, r):
    C = [A[a] ^ A[b] ^ A[c] ^ A[d] ^ A[e] for a, b, c, d, e in CIDX]
    D = [C[a] ^ C[b] for a, b in DIDX]
    B = [A[s] ^ D[d] for s, d in SRC]
    A = [B[a] ^ (~B[b] & B[c]) for a, b, c in CHI]
    for z in IOTA[r]:
        A[z] ^= M256
    return A


def bs_values(origins):  # f(e_S) for all |S| <= 8 and all 256 lanes: S -> 175 plane words
    P = [sum((t >> k & 1) << c for c, t in enumerate(origins)) for k in range(320)]

    def two(Pv):
        A = [0] * 1600
        A[0:320], A[640:960] = Pv, Pv
        for z in (57, 58, 63):
            A[1024 + z] = M256
        return bs_round(bs_round(A, 0), 1)
    S0 = two(P)
    DEL = [[a ^ b for a, b in zip(two([p ^ M256 if w >> k & 1 else p for k, p in enumerate(P)]), S0)]
           for w in W40[:N_DIR]]
    val = {}

    def dfs(S, A, last):
        B = A
        for r in (2, 3, 4):
            B = bs_round(B, r)
        C = [B[a] ^ B[b] ^ B[c] ^ B[d] ^ B[e] for a, b, c, d, e in CIDX]
        D = [C[a] ^ C[b] for a, b in DIDX]
        val[S] = [B[s] ^ D[d] for s, d in SRC_SEL]
        if S.bit_count() < DEG:
            for j in range(last + 1, N_DIR):
                dfs(S | 1 << j, [a ^ b for a, b in zip(A, DEL[j])], j)
    dfs(0, S0, -1)
    return val


# ---- Section 5: one Gray point (FES on 175 planes, chi fused into the transpose tiles); Section 7: the table ----
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


def recon(cid):          # source and digest of candidate cid = (h << 48) | (i << 8) | e: coset record, Gray point, PERM
    e = AND(cid, 255)
    i = AND(SHR(cid, 8), (1 << 40) - 1)
    c = OR(SHL(AND(e, 15), 4), SHR(e, 4))       # emission index e = 16 l + tau -> lane c = 16 tau + l
    a = ADD(SHL(OR(SHL(SHR(cid, 48), 8), c), 1), CSB)
    w0, w1 = LDC(a), LDC(ADD(a, 1))
    g = XOR(i, SHR(i, 1))
    for b in range(N_DIR):                       # full size: the 40 bits of g(i)
        if BR(EQ(AND(SHR(g, b), 1), 1)):
            w0, w1 = XOR(w0, WW[b][0]), XOR(w1, WW[b][1])
    return w0 | w1 << 256, PERM(lane_init(w0, w1))[:4]


def verify(cold, imm):   # earlier candidate cold against the current one (ID HB >> 128 | imm); 'cap', 'equal', 'differ'
    prev = K
    sec('verify' if prev is not SECS['vcheck'] else 'vcheck')
    REGS['F'] = ADD(REGS['F'], 1)
    out = ('cap', None, None, None, None)
    if not BR(EQ(REGS['F'], CAPF)):
        ta, da = recon(cold)
        tb, db = recon(OR(SHR(REGS['HB'], 128), imm))
        st = 'equal'
        for k in range(4):
            if not BR(EQ(da[k], db[k])):
                st = 'differ'
                break
        out = (st, ta, tb, da, db)
    globals()['K'] = prev
    return out


def probe(kw, imm):      # sparse set: 11 (bound test fails), 15 (dense test fails), each with insertion; 10 (valid hit)
    a = OR(kw, SPB)      # imm = ((i << 8) | e) << 128, an immediate of the generated code at Gray site i, emission e
    s = LDS(a)
    i = AND(s, M128)
    if BR(LT(i, REGS['N'])):
        if BR(EQ(LDD(OR(i, DNB)), kw)):
            return SHR(s, 128)                   # valid hit: the ID of the first candidate with this key
        REGS['X'] += 1
    n = REGS['N']
    STD(OR(n, DNB), kw)
    STS(a, OR(OR(REGS['HB'], imm), n))
    REGS['N'] = ADD(n, 1)
    return None


REGS = {'N': 0, 'F': 0, 'HB': 0, 'M': 0, 'X': 0}


def site(i):             # code generation (ONCE): immediate record addresses tab[T_1] .. tab[T_L] of Gray site i
    T, out = 0, []
    while i and len(out) < DEG:
        b = i & -i
        T |= b
        i ^= b
        out.append(TABB + NPL * IDX[T])
    return out


def run_group(h, seeds):
    global SPARSE, DENSE, WRK, CREC
    for s in SECS.values():
        s[0] = 0
    CALLS[0] = 0
    SPARSE, DENSE, WRK, CREC = {}, [None] * QR, [None] * (WEND - WB), {}
    sec('once')                                  # one-time control: count and verification registers; no reset
    REGS['N'], REGS['F'] = MOV(0), MOV(0)
    REGS['M'] = REGS['X'] = 0
    per, origins = leaders(h, seeds)
    for c in range(LANES):
        j = 256 * h + c
        need(CREC[CSB + 2 * j] | CREC[CSB + 2 * j + 1] << 256 == origins[c] < 1 << 320, 'coset record')
        need(per[c] == 11, 'leader count 11 per coset')
    need(SECS['leader'][0] == 11 * LANES + 5 <= 544 * LANES, 'leader total within the charge')
    own = [{} for _ in range(LANES)]             # beside the algorithm: low 16 key bits of each lane's candidates
    val = bs_values(origins)
    need(len(val) == len(SUBS), 'number of evaluation points')
    sec('eval')
    for c in range(LANES):
        evaluate(c, 0)
    sec('conv')
    convert(0)
    need(SECS['conv'][0] == 1282 * NPL, 'conversion 1282 per plane')
    need(WRK[ACO - WB:ACO - WB + NPL] == val[0], 'counted setup at S = {} equals the stand-in')
    sec('eval')
    for S in SUBS[1:]:
        W0, V = evaluate(0, S)
        bits = [(W0 >> (64 * x + z) if x < 4 else V >> z) & 1 for x, z in PLANES]
        need(bits == [v & 1 for v in val[S]], 'counted evaluation on lane 0 equals the stand-in')
        WRK[ACO - WB + NPL * IDX[S]:ACO - WB + NPL * IDX[S] + NPL] = val[S]
    need(SECS['eval'][0] == 1416 * (LANES + len(SUBS) - 1) + 2 * J_D, 'evaluations 1416 + 2|S|')
    del val
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

    REG = [None] * NPL
    keys = [0] * LANES
    st = {'checks': 0, 'mismatch': 0}
    found = key0 = None
    for i in range(1 << N_DIR):
        adr = site(i)
        L = len(adr)
        f0, c0, t0, z0 = SECS['fes'][0], SECS['cht'][0], SECS['table'][0], SECS['zero'][0]
        m0, x0 = REGS['M'], REGS['X']
        top, chain = (adr[-1], adr[-2::-1]) if L else (0, [])
        for tau in range(9):
            R, nz = [0] * 16, [False] * 16
            for dz, z in enumerate(range(4 * tau, min(4 * tau + 4, 35))):
                vals = [0] * 5
                sec('fes' if L else 'zero')
                for x in range(5):
                    p = 5 * z + x
                    if L:                        # Lemma 5 on plane p: top LD, (LD XOR ST) per link, x update
                        v = LDW(top + p)
                        for b in chain:
                            v = XOR(LDW(b + p), v)
                            STW(b + p, v)
                        if RET[p]:
                            v = REG[p] = XOR(REG[p], v)
                        else:
                            v = XOR(LDW(ACO + p), v)
                            STW(ACO + p, v)
                    else:                        # point zero: 39 cache loads, 136 uncached inputs
                        v = LDW(ACO + p)
                        if RET[p]:
                            REG[p] = v
                    vals[x] = v
                sec('cht')                       # chi of row 0, iota omitted: 12 ALU per z, into the tile
                for x in range(4):
                    R[4 * dz + x] = XOR(AND(NOT(vals[(x + 1) % 5]), vals[(x + 2) % 5]), vals[x])
                    nz[4 * dz + x] = True
            for b in range(4):
                stage(R, nz, 1 << b, 1 << b)
            for l in range(16):
                STW(INT + 16 * tau + l, R[l])
        for l in range(16):
            U = [LDW(INT + 16 * tau + l) for tau in range(9)] + [0] * 7
            nz = [True] * 9 + [False] * 7
            for b in range(4):
                stage(U, nz, 1 << b, 16 << b)
            sec('table')
            for tau in range(16):
                keys[16 * tau + l] = U[tau]
                o = own[16 * tau + l]
                o[U[tau] & 0xFFFF] = o.get(U[tau] & 0xFFFF, 0) + 1
                imm = (i << 8) | (16 * l + tau)  # candidate (h, i, e): ID (h << 48) | imm
                r = probe(U[tau], imm << 128)
                if r is not None:                # valid hit: full verification against the stored candidate
                    REGS['M'] += 1
                    v = verify(r, imm)
                    if v[0] != 'differ':
                        found = v
                        break
            sec('cht')
            if found:
                break
        if found:
            break
        if i == 0:
            key0 = keys[0]
        dm, dx = REGS['M'] - m0, REGS['X'] - x0
        need(SECS['cht'][0] - c0 == 4656, 'chi/transpose 4656 per point')
        need(SECS['table'][0] - t0 == 11 * (LANES - dm - dx) + 15 * dx + 10 * dm, 'table 11 / 15 / 10 per candidate')
        if L:
            need(SECS['fes'][0] - f0 == 525 * L + 97, 'FES 525 L + 97 per Gray step')
        else:
            need(SECS['zero'][0] - z0 == NPL, 'point zero 175 loads')
        c = i % LANES                            # check beside the algorithm, not counted
        g, t = i ^ i >> 1, origins[c]
        for b in range(N_DIR):
            if g >> b & 1:
                t ^= W40[b]
        d = sha3_256(message(t))
        kn = sum(((int.from_bytes(d[8 * x:8 * x + 8], 'little') ^ (RC[5] if x == 0 else 0)) >> z & 1) << 4 * z + x
                 for z in range(35) for x in range(4))
        st['checks'] += 1
        st['mismatch'] += kn != keys[c]
    if not found:
        need(SECS['fes'][0] == 525 * SUML + 97 * ((1 << N_DIR) - 1), 'FES total')
        need(SECS['cht'][0] == 4656 << N_DIR and REGS['N'] == QR - REGS['M'], 'chi/transpose total, dense count')
        sec('vcheck')                            # beside the run: probe the first candidate's key again (valid hit,
        k1, c1, saved = K[0], CALLS[0], REGS['F']   # 10 operations), then verify it against candidate (i, e) = (1, 5)
        r = probe(key0, 0)
        need(r == h << 48 and K[0] - k1 == 10, 'valid hit 10 operations')
        k1, REGS['F'] = K[0], 0
        v = verify(r, (1 << 8) | 5)
        REGS['F'] = saved
        for t0, dd, tt in ((origins[0], v[3], v[1]), (origins[5 << 4] ^ W40[0], v[4], v[2])):
            need(tt == t0, 'reconstructed source')
            need(b''.join(w.to_bytes(8, 'little') for w in dd) == sha3_256(message(tt)), 'reconstructed digest')
        need(v[0] == 'differ' and CALLS[0] - c1 == 2 and K[0] - k1 <= 844, 'verification <= 844 + 2 calls')
    need(SECS['verify'][0] <= 844 * REGS['M'] and SECS['once'][0] <= 16, 'verification and one-time bounds')
    need(i + 1 == 1 << N_DIR or found, 'all Gray points')
    obs = {'fes_ops': SECS['fes'][0], 'chi_transpose_ops': SECS['cht'][0],
           'point_zero_loads': SECS['zero'][0], 'table_ops': SECS['table'][0], 'dense_count': REGS['N'],
           'in_range_mismatches': REGS['X'], 'key_matches': REGS['M'], 'leader_ops': SECS['leader'][0],
           'evaluation_ops': SECS['eval'][0], 'conversion_ops': SECS['conv'][0],
           'transform_phase_ops': SECS['transform'][0] + SECS['phase'][0], 'verify_check_ops': SECS['vcheck'][0],
           'perm_calls': CALLS[0], 'native_checks': st['checks'], 'key_mismatch': st['mismatch']}
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
