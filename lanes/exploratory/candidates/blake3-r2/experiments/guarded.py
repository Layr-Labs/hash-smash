"""Seven independent BLAKE3 messages in guarded 36-bit slots.
Evidence only: the production RAM construction and counts are in proof.md.
"""
import hashlib
import json
import struct
import sys

IV = (0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,
      0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19)
P = (2,6,3,10,7,0,4,13,1,11,12,5,9,14,15,8)
S = 36
B = sum(1 << (S*j) for j in range(7))
M = ((1<<32)-1)*B
WORD = (1<<256)-1
RM={r:((1<<(32-r))-1)*B for r in (7,8,12,16)}
LM={r:(((1<<r)-1)<<(32-r))*B for r in (7,8,12,16)}
CALLS=((0,4,8,12),(1,5,9,13),(2,6,10,14),(3,7,11,15),
       (0,5,10,15),(1,6,11,12),(2,7,8,13),(3,4,9,14))

def ror(x,r):
    low=RM[r]
    high=LM[r]
    return ((x>>r)&low)|(((x<<(32-r))&WORD)&high)

def g(v,a,b,c,d,x,y):
    v[a]=(v[a]+v[b]+x)&M
    v[d]=ror(v[d]^v[a],16)
    v[c]=(v[c]+v[d])&M
    v[b]=ror(v[b]^v[c],12)
    v[a]=(v[a]+v[b]+y)&M
    v[d]=ror(v[d]^v[a],8)
    v[c]=(v[c]+v[d])&M
    v[b]=ror(v[b]^v[c],7)

def packed(messages):
    rows=[struct.unpack('<16I',m) for m in messages]
    words=[sum(rows[j][i]<<(S*j) for j in range(len(rows))) for i in range(16)]
    v=[x*B for x in IV+IV[:4]+(0,0,64,11)]
    m=words
    for _ in range(2):
        for i,(a,b,c,d) in enumerate(CALLS):
            g(v,a,b,c,d,m[2*i],m[2*i+1])
        m=[m[i] for i in P]
    out=[v[i]^v[i+8] for i in range(8)]
    return [b''.join(((x>>(S*j))&0xffffffff).to_bytes(4,'little') for x in out)
            for j in range(len(messages))]

def scalar(message):
    v=list(IV+IV[:4]+(0,0,64,11)); m=list(struct.unpack('<16I',message))
    def rr(x,r):
        return ((x>>r)|(x<<(32-r)))&0xffffffff
    for _ in range(2):
        for i,(a,b,c,d) in enumerate(CALLS):
            v[a]=(v[a]+v[b]+m[2*i])&0xffffffff
            v[d]=rr(v[d]^v[a],16); v[c]=(v[c]+v[d])&0xffffffff
            v[b]=rr(v[b]^v[c],12)
            v[a]=(v[a]+v[b]+m[2*i+1])&0xffffffff
            v[d]=rr(v[d]^v[a],8); v[c]=(v[c]+v[d])&0xffffffff
            v[b]=rr(v[b]^v[c],7)
        m=[m[i] for i in P]
    return struct.pack('<8I',*(v[i]^v[i+8] for i in range(8)))

def trial(seed,mask):
    raw=hashlib.shake_256(b'guarded-seven-v1'+bytes.fromhex(seed)).digest(1024*64)
    messages=[raw[i*64:(i+1)*64] for i in range(1024)]
    seen={}; pair=(None,None); mismatches=0
    for start in range(0,1024,7):
        batch=messages[start:start+7]
        digests=packed(batch)
        for message,digest in zip(batch,digests):
            if start == 0:
                mismatches+=int(digest!=scalar(message))
            key=int.from_bytes(digest,'little')&mask
            if key in seen and seen[key]!=message and pair[0] is None:
                pair=(seen[key],message)
            else:
                seen.setdefault(key,message)
    return pair,mismatches

def main():
    req=json.load(sys.stdin)
    mask=int.from_bytes(bytes.fromhex(req['event']['mask_hex']),'little')
    result=[]
    for item in req['trials']:
        (a,b),mismatch=trial(item['seed'],mask)
        result.append({'trial':item['trial'],
            'message_a_hex':None if a is None else a.hex(),
            'message_b_hex':None if b is None else b.hex(),
            'observations':{'packed_scalar_mismatches':mismatch,'messages':1024,
                            'packed_lanes':7,'slot_stride':36}})
    json.dump({'schema_version':1,'trials':result},sys.stdout,separators=(',',':'))

if __name__=='__main__':
    main()
