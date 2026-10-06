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
RM={r:sum(((1<<(32-r))-1)<<(STRIDE*j) for j in range(LANES)) for r in (7,8,12,16)}
LM={r:sum((((1<<r)-1)<<(32-r))<<(STRIDE*j) for j in range(LANES)) for r in (7,8,12,16)}
TWO_B=sum((1<<33)<<(STRIDE*j) for j in range(LANES))
MC=((1<<128)-1)<<32
SB=1<<176
INC=1<<32
IV=(0x6A09E667,0xBB67AE85,0x3C6EF372,0xA54FF53A,0x510E527F,0x9B05688C,0x1F83D9AB,0x5BE0CD19)
PERM=(2,6,3,10,7,0,4,13,1,11,12,5,9,14,15,8)
KEY_WORDS=(0,1,2,3,5)
LAYOUT={"fixed-a3-gap-spread":(32,32,False),"fixed-a3-gap-single":(1,1024,False),"fixed-a3-gap-fullword":(32,32,True)}

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
    return ((z >> r) & RM[r]) | ((z << (32 - r)) & LM[r])

def target_key_masks(base=M):
    """Masks at the five scalar-key destinations (four charged shifts)."""
    return [base] + [base << d for d in (36, 72, 108, 144)]

def extract_keys(o, masks=None):
    """Extract each lane directly into its five scalar-key destinations."""
    masks = target_key_masks() if masks is None else masks
    keys = []
    for lane in range(LANES):
        source = STRIDE * lane
        pieces = []
        for x, dest, mask in zip(o, (0, 36, 72, 108, 144), masks):
            y = x >> (source - dest) if source > dest else \
                (x << (dest - source) if source < dest else x)
            pieces.append(y & mask)
        keys.append(pieces[0] | pieces[1] | pieces[2] | pieces[3] | pieces[4])
    return keys

def pack(o):
    """Counted key: o0 | o1<<36 | o2<<72 | o3<<108 | o5<<144 (8 operations)."""
    return o[0] | (o[1] << 36) | (o[2] << 72) | (o[3] << 108) | (o[4] << 144)

def key_masks(mask_hex):
    """(mask on the packed 5-word key or None, mask on the packed 8-word digest, words)."""
    words = struct.unpack("<8I", bytes.fromhex(mask_hex))
    k8 = sum(w << (32 * i) for i, w in enumerate(words))
    k5 = None if any(words[i] for i in (4, 6, 7)) else sum(words[w] << (36 * j) for j, w in enumerate(KEY_WORDS))
    return k5, k8, words

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
    return False, w, CC, ops

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
    keys=extract_keys(out,target_key_masks(V(M)))
    return [k.x for k in keys],nb,V.n-nb

def validate_batch(m,K,ts):
    keys,nb,ne=counted_packed_body_keys(K,ts)
    allout=packed_body(packed_constants(K),pack_lanes(ts),True)
    for j,t in enumerate(ts):
        ref=compress2(make_message(m,K,t))
        if keys[j]!=pack([ref[i] for i in KEY_WORDS]):
            raise ValueError("packed key differs from independent scalar reference")
        if [((o>>(36*j))&M) for o in allout]!=ref:
            raise ValueError("packed full digest differs from scalar reference")
    if (nb,ne)!=(212,97):
        raise ValueError("unexpected operation count")
    return nb,ne

def trial(seed,groups,per_group,full,k5,k8,wmask):
    mem=Memory(seed); CC=0; msgs=0; verifications=0; tmin=99; tmax=0; obs={}
    sbase=(1<<256) if full else SB # Evidence-only full key uses a larger Python namespace.
    for gi in range(groups):
        U0,U1=group_words(seed,gi); m=unpack(U0,U1); K=setup(m); PK=packed_constants(K)
        mem.store(4*gi+1,U0); mem.store(4*gi+2,U1)
        if gi==0:
            # All-zero/high/carry-edge t values, plus the first complete batch.
            nb,ne=validate_batch(m,K,[0,1,2,M,M-1,1<<31,(1<<31)-1])
            validate_batch(m,K,list(range(7)))
            obs.update(first_packed_body_ops=nb,first_extract_key_ops=ne,reference_checks=14)
        R=gi<<160
        for base in range(0,per_group,LANES):
            active=min(LANES,per_group-base); ts=list(range(base,base+active))
            out=packed_body(PK,pack_lanes(ts),full)
            if full:
                keys=[sum(((o>>(36*j))&M)<<(32*i) for i,o in enumerate(out))&k8 for j in range(active)]
            else:
                keys=[key&k5 for key in extract_keys(out)][:active]
            for key in keys:
                msgs+=1
                matched,w,CC,ops=table_step(mem,key,sbase,R,CC)
                tmin=min(tmin,ops); tmax=max(tmax,ops)
                if matched:
                    verifications+=1; tz=w&M; gz=w>>160
                    mzprefix=unpack(mem.load(4*gz+1),mem.load(4*gz+2))
                    mz=make_message(mzprefix,setup(mzprefix),tz)
                    mx=make_message(m,K,R&M)
                    dz=compress2(mz); dx=compress2(mx)
                    if mz!=mx and all(((dz[i]^dx[i])&wmask[i])==0 for i in range(8)):
                        obs.update(messages=msgs,verifications=verifications,table_ops_min=tmin,table_ops_max=tmax,stale_garbage_pointers=mem.stale)
                        return struct.pack("<16I",*mz).hex(),struct.pack("<16I",*mx).hex(),obs
                R+=1
    obs.update(messages=msgs,verifications=verifications,table_ops_min=tmin,table_ops_max=tmax,stale_garbage_pointers=mem.stale)
    return None,None,obs

def main():
    request=json.load(sys.stdin)
    if request["schema_version"]!=1 or request["target_profile"]!="blake3-r2-prefix-v1":
        raise ValueError("wrong request")
    event=request["event"]
    if event["kind"]!="digest-xor-mask" or int(event["expected_hex"],16)!=0:
        raise ValueError("wrong event")
    groups,per_group,full=LAYOUT[request["experiment_id"]]
    k5,k8,wmask=key_masks(event["mask_hex"])
    if not full and k5 is None: raise ValueError("mask outside key")
    rows=[]
    for item in request["trials"]:
        a,b,obs=trial(bytes.fromhex(item["seed"]),groups,per_group,full,k5,k8,wmask)
        rows.append({"trial":item["trial"],"message_a_hex":a,"message_b_hex":b,"observations":obs})
    json.dump({"schema_version":1,"trials":rows},sys.stdout,separators=(",",":"),sort_keys=True)
    sys.stdout.write("\n")

if __name__=="__main__": main()
