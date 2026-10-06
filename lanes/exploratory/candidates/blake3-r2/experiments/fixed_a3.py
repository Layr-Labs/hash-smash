"""Fixed-a3 grouped BLAKE3-r2 experiment; execute only in organizer sandbox.
Derived from tekkac's seven-way evaluator and winglock/jaazinn sparse table.
Fresh family: fourteen prefix words; choose m14,m15 to force round-one a3=0.
Numeric counts and self-check observations are untrusted participant data.
"""
import hashlib
import json
import struct
import sys
M=(1<<32)-1
W=(1<<256)-1
LANES=7
STRIDE=36
PM=sum(M<<(STRIDE*j) for j in range(LANES))
LOW={k:sum(((1<<k)-1)<<(STRIDE*j) for j in range(LANES)) for k in (7,8,12,16,20,24,25)}
TWO_B=sum((1<<33)<<(STRIDE*j) for j in range(LANES))
TOP=(1<<256)-1
GAP=1<<32
IV=(0x6A09E667,0xBB67AE85,0x3C6EF372,0xA54FF53A,0x510E527F,0x9B05688C,0x1F83D9AB,0x5BE0CD19)
PERM=(2,6,3,10,7,0,4,13,1,11,12,5,9,14,15,8)
KEY_WORDS=(0,1,2,3,5)
LAYOUT={"fixed-a3-pf-spread":(32,32,False),"fixed-a3-pf-single":(1,1024,False),"fixed-a3-pf-fullword":(32,32,True),"fixed-a3-pf-keysub":(32,32,False)}

def ror(z, r):
    return ((z >> r) | (z << (32 - r))) & M

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

def broadcast(x):
    """Seven copies of one 32-bit value in 36-bit fields."""
    return sum(x << (STRIDE * j) for j in range(LANES))

def pack_lanes(xs):
    """Pack at most seven 32-bit lane values; omitted high lanes are zero."""
    return sum((x & M) << (STRIDE * j) for j, x in enumerate(xs))

def pror(z, r):
    """Rotate each of seven 32-bit fields, discarding all guard bits."""
    return ((z >> r) & LOW[32-r]) | ((z & LOW[r]) << (32-r))

EXTRACT_MASKS = (("W0", (0,)), ("W14", (1,4)), ("W25", (2,5)), ("W36", (3,6)), ("M012", (0,1,2)), ("W13", (1,3)), ("W05", (0,5)), ("W246", (2,4,6)), ("M34", (3,4)))
DESIGN = (((0, 1, 2), (((0,), 0), ((1, 4), 1), ((2, 5), 2), ((3, 6), 2))),
          ((3, 4), (((1, 3), 3), ((0, 5), 3), ((2, 4, 6), 4))))


def sh(x, n):
    """shift by n slots (left if n > 0); a zero shift is no instruction"""
    return x if n == 0 else (x << (STRIDE * n) if n > 0 else x >> (-STRIDE * n))


def extract_keys(o, mask=None):
    """Seven gapped keys o0 | o1<<36 | o2<<72 | o3<<108 | o5<<144 from the five
    packed outputs o = (o0, o1, o2, o3, o5); mask(name) gives the mask words.
    64 operations."""
    mask = (lambda name: MASKS[name]) if mask is None else mask
    parts = {j: [] for j in range(LANES)}
    for S, words in DESIGN:
        for G, delta in words:
            Wg = mask("W" + "".join(map(str, G)))
            w = None
            for k in S:
                v = sh(o[k] & Wg, k - delta)
                w = v if w is None else w | v
            for j in G:
                x = sh(w, delta - j)
                if any(0 <= jj - delta + k + delta - j <= 7 for jj in G if jj != j for k in S):
                    x = x & mask("M" + "".join(map(str, S)))
                parts[j].append(x)
    keys = []
    for j in range(LANES):
        k = parts[j][0]
        for x in parts[j][1:]:
            k = k | x
        keys.append(k)
    return keys


MASKS = {n: sum(M << (36*j) for j in js) for n, js in EXTRACT_MASKS}


def pack(o):
    """Counted key: o0 | o1<<36 | o2<<72 | o3<<108 | o5<<144 (8 operations)."""
    return o[0] | (o[1] << 36) | (o[2] << 72) | (o[3] << 108) | (o[4] << 144)

def key_masks(mask_hex, project=False):
    """(mask on the packed 5-word key or None, mask on the packed 8-word digest, words)."""
    words = struct.unpack("<8I", bytes.fromhex(mask_hex))
    k8 = sum(w << (32 * i) for i, w in enumerate(words))
    k5 = None if any(words[i] for i in (4, 6, 7)) and not project else sum(words[w] << (36 * j) for j, w in enumerate(KEY_WORDS))
    return k5, k8, words

class Memory:
    """Never-initialised memory. An unwritten word reads as seed-derived garbage;
    once a dense entry exists, about half of the unwritten words hold the address
    of a genuinely written dense entry (a stale pointer, address > CC)."""
    def __init__(self, seed):
        self.seed, self.cells, self.stale = seed, {}, 0

    def load(self, a, CC):
        if a in self.cells:
            return self.cells[a]
        h = hashlib.sha256(b"garbage" + self.seed + a.to_bytes(33, "little")).digest()
        x = int.from_bytes(h, "little")
        if CC < TOP and h[0] & 1:
            self.stale += 1
            return CC + 1 + x % (TOP - CC)
        if h[0] & 2:
            return CC - (x & 0xFFFFF)          # at or just below CC: never written
        return x

    def store(self, a, v):
        self.cells[a] = v


def table_step(mem, sa, key, CC):
    """Literal transcript of proof.md Section 5 with its operations counted.
    Returns (matched, w, CC, ops); on MATCH, CC is unchanged (the handler writes
    the dummy entry)."""
    w = mem.load(sa, CC); ops = 1               # load [K]
    ops += 2                                    # compare CC < w, branch
    if CC < w:
        q = mem.load(w, CC); ops += 1           # load [w]
        ops += 2                                # compare q == K, branch
        if q == key:
            return True, w, CC, ops             # MATCH entry: 6
    mem.store(sa, CC); ops += 1                 # store [K] <- CC
    mem.store(CC, key); ops += 1                # store [CC] <- K
    CC = CC - 1; ops += 1                       # CC = CC - ONE
    return False, w, CC, ops                    # 9 (both tests) or 6


def dummy_entry(mem, key, CC):
    """Declined MATCH (inside the charged handler): store [CC] <- K; CC -= 1."""
    mem.store(CC, key)
    return CC - 1



class V:
    """Counting word: every operation with a V operand is counted once."""
    n = 0

    def __init__(self, x): self.x = x

    def _op(self, f, o):
        V.n += 1
        return V(f(self.x, o.x if isinstance(o, V) else o) & ((1 << 256) - 1))

    def __add__(self, o): return self._op(lambda a, b: a + b, o)
    __radd__ = __add__
    def __sub__(self, o): return self._op(lambda a, b: a - b, o)
    def __rsub__(self, o): return self._op(lambda a, b: b - a, o)
    def __xor__(self, o): return self._op(lambda a, b: a ^ b, o)
    __rxor__ = __xor__
    def __and__(self, o): return self._op(lambda a, b: a & b, o)
    __rand__ = __and__
    def __or__(self, o): return self._op(lambda a, b: a | b, o)
    __ror__ = __or__
    def __rshift__(self, k): return self._op(lambda a, b: a >> b, k)
    def __lshift__(self, k): return self._op(lambda a, b: a << b, k)
    def __neg__(self): return self._op(lambda a, b: -a, 0)

def unpack(U0,U1):
    return [(U0>>(32*i))&M for i in range(8)]+[(U1>>(32*i))&M for i in range(6)]

def setup(m):
    v=list(IV)+list(IV[:4])+[0,0,64,11]
    for (a,b,c,d),i in zip(((0,4,8,12),(1,5,9,13),(2,6,10,14),(3,7,11,15),
                            (0,5,10,15),(1,6,11,12),(2,7,8,13)),range(0,14,2)):
        v[a],v[b],v[c],v[d]=g(v[a],v[b],v[c],v[d],m[i],m[i+1])
    A=(v[3]+v[4])&M
    a1h=(v[1]+v[5]+m[3])&M
    a2h=(v[2]+v[6]+m[7])&M
    a3,b7,c11,d15=g(0,v[7],v[11],v[15],m[4],m[13])
    return {"negA":(-A)&M,"D":v[14],"C":v[9],"B":v[4],
            "A0x":(v[0]+m[2])&M,"d12":v[12],"c8":v[8],"s1":m[6],
            "d13h":ror(v[13]^a1h,16),"b5":v[5],"A1y":(a1h+m[10])&M,
            "a2h":a2h,"c10":v[10],"b6":v[6],"A2y":(a2h+m[0])&M,
            "a3":a3,"b7":b7,"c11":c11,"d15":d15,
            "s8":m[1],"s9":m[11],"s10":m[12],"s11":m[5],"s12":m[9],"s15":m[8]}

def make_message(m,K,t):
    h=ror(K["D"]^t,16)
    ch=(K["C"]+h)&M
    bh=ror(K["B"]^ch,12)
    return m+[(t+K["negA"])&M,(-t-bh)&M]

def packed_constants(K):
    return {name:broadcast(value) for name,value in K.items()}

def packed_body(K,T,full=False):
    # t is the first a3 update in the last G of round one; its final update is zero.
    h=pror(K["D"]^T,16)
    c9=K["C"]+h
    bh=pror(K["B"]^c9,12)
    m15=TWO_B-T-bh
    m14=T+K["negA"]
    d14=pror(h,8)
    c9=c9+d14
    b4=pror(bh^c9,7)
    # Column zero.
    a0=K["A0x"]+b4
    d12=pror(K["d12"]^a0,16); c8=K["c8"]+d12; b4=pror(b4^c8,12)
    a0=a0+b4+K["s1"]
    d12=pror(d12^a0,8); c8=c8+d12; b4=pror(b4^c8,7)
    # Column one: invariant first half is supplied by group setup.
    c9=c9+K["d13h"]; b5=pror(K["b5"]^c9,12)
    a1=K["A1y"]+b5
    d13=pror(K["d13h"]^a1,8); c9=c9+d13; b5=pror(b5^c9,7)
    # Column two.
    d14=pror(d14^K["a2h"],16); c10=K["c10"]+d14; b6=pror(K["b6"]^c10,12)
    a2=K["A2y"]+b6
    d14=pror(d14^a2,8); c10=c10+d14; b6=pror(b6^c10,7)
    # Entire column three is invariant. Direct operand substitution avoids copies.
    a0=a0+b5+K["s8"]; d15=pror(K["d15"]^a0,16); c10=c10+d15; b5=pror(b5^c10,12)
    a0=a0+b5+K["s9"]; d15=pror(d15^a0,8); c10=c10+d15; b5=pror(b5^c10,7)
    a1=a1+b6+K["s10"]; d12=pror(d12^a1,16); c11=K["c11"]+d12; b6=pror(b6^c11,12)
    a1=a1+b6+K["s11"]; d12=pror(d12^a1,8); c11=c11+d12
    a2=a2+K["b7"]+K["s12"]; d13=pror(d13^a2,16); c8=c8+d13; b7=pror(K["b7"]^c8,12)
    a2=a2+b7+m14; d13=pror(d13^a2,8); c8=c8+d13
    a3=K["a3"]+b4+m15; d14=pror(d14^a3,16); c9=c9+d14; b4=pror(b4^c9,12)
    a3=a3+b4+K["s15"]; d14=pror(d14^a3,8); c9=c9+d14
    if full:
        b4=pror(b4^c9,7); b6=pror(b6^c11,7); b7=pror(b7^c8,7)
        return a0^c8,a1^c9,a2^c10,a3^c11,b4^d12,b5^d13,b6^d14,b7^d15
    return a0^c8,a1^c9,a2^c10,a3^c11,b5^d13

def group_words(seed,gi):
    raw=hashlib.shake_256(b"fixed-a3-v1"+seed+gi.to_bytes(8,"little")).digest(56)
    return int.from_bytes(raw[:32],"little"),int.from_bytes(raw[32:],"little")

def counted_packed_body_keys(K,ts):
    PK={k:V(v) for k,v in packed_constants(K).items()}
    V.n=0
    out=packed_body(PK,V(pack_lanes(ts)))
    nb=V.n
    keys=extract_keys(out,lambda name: V(MASKS[name]))
    return [k.x for k in keys],nb,V.n-nb

# Statically lowered fixed 64-register schedule; no participant code was executed to generate it.
RAM_FIXED=['BC7', 'CC', 'K_A0x', 'K_A1y', 'K_A2y', 'K_B', 'K_C', 'K_D', 'K_a2h', 'K_a3', 'K_b5', 'K_b6', 'K_b7', 'K_c10', 'K_c11', 'K_c8', 'K_d12', 'K_d13h', 'K_d15', 'K_negA', 'K_s1', 'K_s10', 'K_s11', 'K_s12', 'K_s15', 'K_s8', 'K_s9', 'LOW_12', 'LOW_16', 'LOW_20', 'LOW_24', 'LOW_25', 'LOW_7', 'LOW_8', 'M012', 'M34', 'ONE', 'T', 'TWO_B', 'W0', 'W05', 'W13', 'W14', 'W246', 'W25', 'W36']
RAM_PROGRAM=[['BitXor', 46, [7, 37]], ['RShift', 47, [46, {'imm': 16}]], ['BitAnd', 47, [47, 28]], ['BitAnd', 46, [46, 28]], ['LShift', 46, [46, {'imm': 16}]], ['BitOr', 46, [47, 46]], ['Add', 47, [6, 46]], ['BitXor', 48, [5, 47]], ['RShift', 49, [48, {'imm': 12}]], ['BitAnd', 49, [49, 29]], ['BitAnd', 48, [48, 27]], ['LShift', 48, [48, {'imm': 20}]], ['BitOr', 48, [49, 48]], ['Sub', 49, [38, 37]], ['Sub', 49, [49, 48]], ['Add', 50, [37, 19]], ['RShift', 51, [46, {'imm': 8}]], ['BitAnd', 51, [51, 30]], ['BitAnd', 46, [46, 33]], ['LShift', 46, [46, {'imm': 24}]], ['BitOr', 46, [51, 46]], ['Add', 47, [47, 46]], ['BitXor', 48, [48, 47]], ['RShift', 51, [48, {'imm': 7}]], ['BitAnd', 51, [51, 31]], ['BitAnd', 48, [48, 32]], ['LShift', 48, [48, {'imm': 25}]], ['BitOr', 48, [51, 48]], ['Add', 51, [2, 48]], ['BitXor', 52, [16, 51]], ['RShift', 53, [52, {'imm': 16}]], ['BitAnd', 53, [53, 28]], ['BitAnd', 52, [52, 28]], ['LShift', 52, [52, {'imm': 16}]], ['BitOr', 52, [53, 52]], ['Add', 53, [15, 52]], ['BitXor', 48, [48, 53]], ['RShift', 54, [48, {'imm': 12}]], ['BitAnd', 54, [54, 29]], ['BitAnd', 48, [48, 27]], ['LShift', 48, [48, {'imm': 20}]], ['BitOr', 48, [54, 48]], ['Add', 51, [51, 48]], ['Add', 51, [51, 20]], ['BitXor', 52, [52, 51]], ['RShift', 54, [52, {'imm': 8}]], ['BitAnd', 54, [54, 30]], ['BitAnd', 52, [52, 33]], ['LShift', 52, [52, {'imm': 24}]], ['BitOr', 52, [54, 52]], ['Add', 53, [53, 52]], ['BitXor', 48, [48, 53]], ['RShift', 54, [48, {'imm': 7}]], ['BitAnd', 54, [54, 31]], ['BitAnd', 48, [48, 32]], ['LShift', 48, [48, {'imm': 25}]], ['BitOr', 48, [54, 48]], ['Add', 47, [47, 17]], ['BitXor', 54, [10, 47]], ['RShift', 55, [54, {'imm': 12}]], ['BitAnd', 55, [55, 29]], ['BitAnd', 54, [54, 27]], ['LShift', 54, [54, {'imm': 20}]], ['BitOr', 54, [55, 54]], ['Add', 55, [3, 54]], ['BitXor', 56, [17, 55]], ['RShift', 57, [56, {'imm': 8}]], ['BitAnd', 57, [57, 30]], ['BitAnd', 56, [56, 33]], ['LShift', 56, [56, {'imm': 24}]], ['BitOr', 56, [57, 56]], ['Add', 47, [47, 56]], ['BitXor', 54, [54, 47]], ['RShift', 57, [54, {'imm': 7}]], ['BitAnd', 57, [57, 31]], ['BitAnd', 54, [54, 32]], ['LShift', 54, [54, {'imm': 25}]], ['BitOr', 54, [57, 54]], ['BitXor', 46, [46, 8]], ['RShift', 57, [46, {'imm': 16}]], ['BitAnd', 57, [57, 28]], ['BitAnd', 46, [46, 28]], ['LShift', 46, [46, {'imm': 16}]], ['BitOr', 46, [57, 46]], ['Add', 57, [13, 46]], ['BitXor', 58, [11, 57]], ['RShift', 59, [58, {'imm': 12}]], ['BitAnd', 59, [59, 29]], ['BitAnd', 58, [58, 27]], ['LShift', 58, [58, {'imm': 20}]], ['BitOr', 58, [59, 58]], ['Add', 59, [4, 58]], ['BitXor', 46, [46, 59]], ['RShift', 60, [46, {'imm': 8}]], ['BitAnd', 60, [60, 30]], ['BitAnd', 46, [46, 33]], ['LShift', 46, [46, {'imm': 24}]], ['BitOr', 46, [60, 46]], ['Add', 57, [57, 46]], ['BitXor', 58, [58, 57]], ['RShift', 60, [58, {'imm': 7}]], ['BitAnd', 60, [60, 31]], ['BitAnd', 58, [58, 32]], ['LShift', 58, [58, {'imm': 25}]], ['BitOr', 58, [60, 58]], ['Add', 51, [51, 54]], ['Add', 51, [51, 25]], ['BitXor', 60, [18, 51]], ['RShift', 61, [60, {'imm': 16}]], ['BitAnd', 61, [61, 28]], ['BitAnd', 60, [60, 28]], ['LShift', 60, [60, {'imm': 16}]], ['BitOr', 60, [61, 60]], ['Add', 57, [57, 60]], ['BitXor', 54, [54, 57]], ['RShift', 61, [54, {'imm': 12}]], ['BitAnd', 61, [61, 29]], ['BitAnd', 54, [54, 27]], ['LShift', 54, [54, {'imm': 20}]], ['BitOr', 54, [61, 54]], ['Add', 51, [51, 54]], ['Add', 51, [51, 26]], ['BitXor', 60, [60, 51]], ['RShift', 61, [60, {'imm': 8}]], ['BitAnd', 61, [61, 30]], ['BitAnd', 60, [60, 33]], ['LShift', 60, [60, {'imm': 24}]], ['BitOr', 60, [61, 60]], ['Add', 57, [57, 60]], ['BitXor', 54, [54, 57]], ['RShift', 60, [54, {'imm': 7}]], ['BitAnd', 60, [60, 31]], ['BitAnd', 54, [54, 32]], ['LShift', 54, [54, {'imm': 25}]], ['BitOr', 54, [60, 54]], ['Add', 55, [55, 58]], ['Add', 55, [55, 21]], ['BitXor', 52, [52, 55]], ['RShift', 60, [52, {'imm': 16}]], ['BitAnd', 60, [60, 28]], ['BitAnd', 52, [52, 28]], ['LShift', 52, [52, {'imm': 16}]], ['BitOr', 52, [60, 52]], ['Add', 60, [14, 52]], ['BitXor', 58, [58, 60]], ['RShift', 61, [58, {'imm': 12}]], ['BitAnd', 61, [61, 29]], ['BitAnd', 58, [58, 27]], ['LShift', 58, [58, {'imm': 20}]], ['BitOr', 58, [61, 58]], ['Add', 55, [55, 58]], ['Add', 55, [55, 22]], ['BitXor', 52, [52, 55]], ['RShift', 58, [52, {'imm': 8}]], ['BitAnd', 58, [58, 30]], ['BitAnd', 52, [52, 33]], ['LShift', 52, [52, {'imm': 24}]], ['BitOr', 52, [58, 52]], ['Add', 52, [60, 52]], ['Add', 58, [59, 12]], ['Add', 58, [58, 23]], ['BitXor', 56, [56, 58]], ['RShift', 59, [56, {'imm': 16}]], ['BitAnd', 59, [59, 28]], ['BitAnd', 56, [56, 28]], ['LShift', 56, [56, {'imm': 16}]], ['BitOr', 56, [59, 56]], ['Add', 53, [53, 56]], ['BitXor', 59, [12, 53]], ['RShift', 60, [59, {'imm': 12}]], ['BitAnd', 60, [60, 29]], ['BitAnd', 59, [59, 27]], ['LShift', 59, [59, {'imm': 20}]], ['BitOr', 59, [60, 59]], ['Add', 58, [58, 59]], ['Add', 50, [58, 50]], ['BitXor', 56, [56, 50]], ['RShift', 58, [56, {'imm': 8}]], ['BitAnd', 58, [58, 30]], ['BitAnd', 56, [56, 33]], ['LShift', 56, [56, {'imm': 24}]], ['BitOr', 56, [58, 56]], ['Add', 53, [53, 56]], ['Add', 58, [9, 48]], ['Add', 49, [58, 49]], ['BitXor', 46, [46, 49]], ['RShift', 58, [46, {'imm': 16}]], ['BitAnd', 58, [58, 28]], ['BitAnd', 46, [46, 28]], ['LShift', 46, [46, {'imm': 16}]], ['BitOr', 46, [58, 46]], ['Add', 47, [47, 46]], ['BitXor', 48, [48, 47]], ['RShift', 58, [48, {'imm': 12}]], ['BitAnd', 58, [58, 29]], ['BitAnd', 48, [48, 27]], ['LShift', 48, [48, {'imm': 20}]], ['BitOr', 48, [58, 48]], ['Add', 48, [49, 48]], ['Add', 48, [48, 24]], ['BitXor', 46, [46, 48]], ['RShift', 49, [46, {'imm': 8}]], ['BitAnd', 49, [49, 30]], ['BitAnd', 46, [46, 33]], ['LShift', 46, [46, {'imm': 24}]], ['BitOr', 46, [49, 46]], ['Add', 46, [47, 46]], ['BitXor', 47, [51, 53]], ['BitXor', 46, [55, 46]], ['BitXor', 49, [50, 57]], ['BitXor', 48, [48, 52]], ['BitXor', 50, [54, 56]], ['BitAnd', 51, [47, 39]], ['BitAnd', 52, [46, 39]], ['LShift', 52, [52, {'imm': 36}]], ['BitOr', 51, [51, 52]], ['BitAnd', 52, [49, 39]], ['LShift', 52, [52, {'imm': 72}]], ['BitOr', 51, [51, 52]], ['BitAnd', 52, [47, 42]], ['RShift', 52, [52, {'imm': 36}]], ['BitAnd', 53, [46, 42]], ['BitOr', 52, [52, 53]], ['BitAnd', 53, [49, 42]], ['LShift', 53, [53, {'imm': 36}]], ['BitOr', 52, [52, 53]], ['BitAnd', 53, [52, 34]], ['RShift', 52, [52, {'imm': 108}]], ['BitAnd', 54, [47, 44]], ['RShift', 54, [54, {'imm': 72}]], ['BitAnd', 55, [46, 44]], ['RShift', 55, [55, {'imm': 36}]], ['BitOr', 54, [54, 55]], ['BitAnd', 55, [49, 44]], ['BitOr', 54, [54, 55]], ['BitAnd', 55, [54, 34]], ['RShift', 54, [54, {'imm': 108}]], ['BitAnd', 47, [47, 45]], ['RShift', 47, [47, {'imm': 72}]], ['BitAnd', 46, [46, 45]], ['RShift', 46, [46, {'imm': 36}]], ['BitOr', 46, [47, 46]], ['BitAnd', 47, [49, 45]], ['BitOr', 46, [46, 47]], ['RShift', 47, [46, {'imm': 36}]], ['BitAnd', 47, [47, 34]], ['RShift', 46, [46, {'imm': 144}]], ['BitAnd', 49, [48, 41]], ['BitAnd', 56, [50, 41]], ['LShift', 56, [56, {'imm': 36}]], ['BitOr', 49, [49, 56]], ['LShift', 56, [49, {'imm': 72}]], ['BitAnd', 56, [56, 35]], ['BitAnd', 49, [49, 35]], ['BitAnd', 57, [48, 40]], ['BitAnd', 58, [50, 40]], ['LShift', 58, [58, {'imm': 36}]], ['BitOr', 57, [57, 58]], ['LShift', 58, [57, {'imm': 108}]], ['RShift', 57, [57, {'imm': 72}]], ['BitAnd', 48, [48, 43]], ['RShift', 48, [48, {'imm': 36}]], ['BitAnd', 50, [50, 43]], ['BitOr', 48, [48, 50]], ['LShift', 50, [48, {'imm': 72}]], ['BitAnd', 50, [50, 35]], ['BitAnd', 59, [48, 35]], ['RShift', 48, [48, {'imm': 72}]], ['BitAnd', 48, [48, 35]], ['BitOr', 51, [51, 58]], ['BitOr', 53, [53, 56]], ['BitOr', 50, [55, 50]], ['BitOr', 47, [47, 49]], ['BitOr', 49, [52, 59]], ['BitOr', 52, [54, 57]], ['BitOr', 46, [46, 48]], ['TABLE', -1, [51, 1, 36]], ['TABLE', -1, [53, 1, 36]], ['TABLE', -1, [50, 1, 36]], ['TABLE', -1, [47, 1, 36]], ['TABLE', -1, [49, 1, 36]], ['TABLE', -1, [52, 1, 36]], ['TABLE', -1, [46, 1, 36]]]

def ram_keys(K,ts):
    reg=[0]*64
    pk=packed_constants(K)
    for i,name in enumerate(RAM_FIXED):
        if name.startswith("K_"): v=pk[name[2:]]
        elif name.startswith("LOW_"): v=LOW[int(name[4:])]
        elif name in MASKS: v=MASKS[name]
        else: v={"T":pack_lanes(ts),"CC":TOP,"BC7":broadcast(7),"ONE":1,"TWO_B":TWO_B}[name]
        reg[i]=v
    keys=[];n=0
    for op,d,args in RAM_PROGRAM:
        x,y=[a["imm"] if isinstance(a,dict) else reg[a] for a in args[:2]]
        if op=="TABLE": keys.append(x); continue
        if op=="Add": z=x+y
        elif op=="Sub": z=x-y
        elif op=="BitXor": z=x^y
        elif op=="BitAnd": z=x&y
        elif op=="BitOr": z=x|y
        elif op=="RShift": z=x>>y
        elif op=="LShift": z=x<<y
        else: raise ValueError("unknown RAM opcode")
        reg[d]=z&W; n+=1
    if n!=276: raise ValueError("unexpected lowered schedule length")
    return keys

def validate_batch(m,K,ts):
    keys,nb,ne=counted_packed_body_keys(K,ts)
    if ram_keys(K,ts)!=keys: raise ValueError("lowered RAM keys differ from counted expression")
    allout=packed_body(packed_constants(K),pack_lanes(ts),True)
    for j,t in enumerate(ts):
        ref=compress2(make_message(m,K,t))
        if keys[j]!=pack([ref[i] for i in KEY_WORDS]):
            raise ValueError("packed key differs from independent scalar reference")
        if [((o>>(36*j))&M) for o in allout]!=ref:
            raise ValueError("packed full digest differs from scalar reference")
    if (nb,ne)!=(212,64):
        raise ValueError("unexpected operation count")
    return nb,ne

def rec_addr(g,k):
    return (g<<36)|GAP|k

def trial(seed,groups,per_group,full,k5,k8,wmask):
    mem=Memory(seed); CC=TOP; msgs=0; verifications=0; dummy=0; tmin=99; tmax=0; obs={}
    for gi in range(groups):
        U0,U1=group_words(seed,gi); m=unpack(U0,U1); K=setup(m); PK=packed_constants(K)
        mem.store(rec_addr(gi,1),U0); mem.store(rec_addr(gi,2),U1)
        if gi==0:
            nb,ne=validate_batch(m,K,[0,1,2,M,M-1,1<<31,(1<<31)-1])
            validate_batch(m,K,list(range(7)))
            obs.update(first_packed_body_ops=nb,first_extract_key_ops=ne,reference_checks=14,ram_registers=64)
        for base in range(0,per_group,LANES):
            active=min(LANES,per_group-base); ts=list(range(base,base+active))
            if full:
                out=packed_body(PK,pack_lanes(ts),True)
                keys=[sum(((o>>(36*j))&M)<<(32*i) for i,o in enumerate(out))&k8 for j in range(active)]
            else:
                keys=[key&k5 for key in ram_keys(K,ts)][:active]
            for lane,key in enumerate(keys):
                current_i=TOP-CC
                if current_i!=gi*per_group+base+lane:
                    raise ValueError("dense address no longer decodes the current message")
                sa=key+(1<<257) if full else key
                matched,w,newCC,ops=table_step(mem,sa,key,CC)
                msgs+=1; tmin=min(tmin,ops); tmax=max(tmax,ops)
                if matched:
                    verifications+=1; gz,tz=divmod(TOP-w,per_group)
                    mzprefix=unpack(mem.load(rec_addr(gz,1),CC),mem.load(rec_addr(gz,2),CC))
                    mz=make_message(mzprefix,setup(mzprefix),tz)
                    mx=make_message(m,K,base+lane)
                    dz=compress2(mz); dx=compress2(mx)
                    if mz!=mx and all(((dz[i]^dx[i])&wmask[i])==0 for i in range(8)):
                        obs.update(messages=msgs,verifications=verifications,dummy_entries=dummy,table_ops_min=tmin,table_ops_max=tmax,stale_garbage_pointers=mem.stale)
                        return struct.pack("<16I",*mz).hex(),struct.pack("<16I",*mx).hex(),obs
                    newCC=dummy_entry(mem,key,CC); dummy+=1
                CC=newCC
    obs.update(messages=msgs,verifications=verifications,dummy_entries=dummy,table_ops_min=tmin,table_ops_max=tmax,stale_garbage_pointers=mem.stale)
    return None,None,obs

def main():
    request=json.load(sys.stdin)
    if request["schema_version"]!=1 or request["target_profile"]!="blake3-r2-prefix-v1":
        raise ValueError("wrong request")
    event=request["event"]
    if event["kind"]!="digest-xor-mask" or int(event["expected_hex"],16)!=0:
        raise ValueError("wrong event")
    groups,per_group,full=LAYOUT[request["experiment_id"]]
    k5,k8,wmask=key_masks(event["mask_hex"],request["experiment_id"]=="fixed-a3-pf-keysub")
    if not full and k5 is None: raise ValueError("mask outside key")
    rows=[]
    for item in request["trials"]:
        a,b,obs=trial(bytes.fromhex(item["seed"]),groups,per_group,full,k5,k8,wmask)
        rows.append({"trial":item["trial"],"message_a_hex":a,"message_b_hex":b,"observations":obs})
    json.dump({"schema_version":1,"trials":rows},sys.stdout,separators=(",",":"),sort_keys=True)
    sys.stdout.write("\n")

if __name__=="__main__": main()
