#!/usr/bin/env python3
# r38joint.py - sha256-r38 (38 steps) ordinary collision: the two-block P1 claw of newjordan 51613d1c on the P8
# characteristic of dariolina 1a695f0b, found by a van Oorschot-Wiener distinguished-point walk on a counted 256-bit
# word RAM with a bit-sliced 256-lane kernel (the machine program of our 19034ce3 / lamb356 4487063 / Jbenisek
# d90878ff, as run by dkuthoore 0b2616e3). Own code, standard library only; P8 is read as data.
# Sections: [1] SHA-256 r38, P8 data, the claw maps; [2] kernel generator + allocator; [3] counted machine;
# [4] Attack (stage 1, stage 2, claw filters, step 3b); [5] experiments and main.
import sys, json, random, time, hashlib

# ---------------------------------------------------------------- [1] reference, P8 data, maps
M = 0xffffffff; NR = 38
K = [0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,
     0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,
     0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,
     0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb]
IV = [0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19]
def ror(x,n): return ((x>>n)|(x<<(32-n)))&M
def S0(x): return ror(x,2)^ror(x,13)^ror(x,22)
def S1(x): return ror(x,6)^ror(x,11)^ror(x,25)
def s0(x): return ror(x,7)^ror(x,18)^(x>>3)
def s1(x): return ror(x,17)^ror(x,19)^(x>>10)
def CH(x,y,z): return (x&y)^(~x&z&M)
def MAJ(x,y,z): return (x&y)^(x&z)^(y&z)
def trace(cv,w16,n=NR):
    W=list(w16)
    for i in range(16,n): W.append((s1(W[i-2])+W[i-7]+s0(W[i-15])+W[i-16])&M)
    A={-1-i:cv[i] for i in range(4)}; E={-1-i:cv[4+i] for i in range(4)}
    for i in range(n):
        E[i]=(A[i-4]+E[i-4]+S1(E[i-1])+CH(E[i-1],E[i-2],E[i-3])+K[i]+W[i])&M
        A[i]=(E[i]-A[i-4]+S0(A[i-1])+MAJ(A[i-1],A[i-2],A[i-3]))&M
    return A,E,W
def compress(cv,w16,n=NR):
    A,E,W=trace(cv,w16,n); f=[A[n-1],A[n-2],A[n-3],A[n-4],E[n-1],E[n-2],E[n-3],E[n-4]]
    return [(cv[i]+f[i])&M for i in range(8)]
def digest_r38(msg):
    """sha256-r38 of a byte string (FIPS padding), as the organizer verifier computes it"""
    ml=len(msg); m=msg+b'\x80'+b'\x00'*((55-ml)%64)+(8*ml).to_bytes(8,'big'); cv=IV
    for o in range(0,len(m),64): cv=compress(cv,[int.from_bytes(m[o+4*i:o+4*i+4],'big') for i in range(16)])
    return b''.join(x.to_bytes(4,'big') for x in cv)
# P8 (1a695f0b): chaining value and the two message blocks of the published 38-step semi-free-start pair (data)
PCV = [0x95a24959,0xb4053f95,0x1bf0473e,0x1eab3b7c,0x650c63d3,0xe6493d3b,0xed004f1d,0xeb7eaad3]
PMX = [0xbd047e95,0x1dc94891,0x4bbe458b,0xc7dc3c0a,0x8b6235e1,0x9d7630ee,0x569da3a0,0x94ddb1c2,0x464e545d,0xa804c932,0xacecbe75,
       0xc8280172,0x9a4d6768,0x16139532,0xe00d6a99,0x5fb2827b]
PMY = [0xbd047e95,0x1dc94891,0x4bbe458b,0xc7dc3c0a,0x8b6235e1,0x9d7630ee,0x569da3a0,0xb4ddb1c2,0x420e5c5d,0x8804c932,0xa9edacdf,
       0xc8200d72,0x9a4d6768,0x16139532,0xe00d6a99,0x5bf28a7b]
_tx=trace(PCV,PMX); _ty=trace(PCV,PMY)
SAx=[_tx[0][i] for i in range(16)]; SAy=[_ty[0][i] for i in range(16)]
SEx=[_tx[1][i] for i in range(16)]; SEy=[_ty[1][i] for i in range(16)]
R16H=[int(t,16) for t in ('4b02d320 7b1ab320 7b22b320 7b3ab320 c802f320 c80ad320 c80af320 c812d320 c822f320 c82ad320 c82af320 c832d320 '
                          'cb12f320 cb1ad320 cb1af320 cb22d320 cb32f320 cb3ad320 cb3af320 fb02b320').split()]
R16F=0x405; OFFS=(0,1,4,5,1024,1025,1028,1029)
T20=[((h-R16H[0])&M)>>13 for h in R16H]
assert all((R16H[0]+(t<<13))&M==h for h,t in zip(R16H,T20)) and len(set(T20))==20 and all(h&R16F==0 for h in R16H)
def r16ok(e): return (e&~R16F&M) in R16H
Cc2=0x7af32e15; RWIN=9; RTOP=RWIN<<26; M26=(1<<26)-1; M28=(1<<28)-1; M29=(1<<29)-1
SUBSETS=[[4*s+i for i in range(4)] for s in range(5)]       # the five 4-head subsets, rotated per window

def cv_consts(cv):
    a,b,c,d,e,f,g,h=cv
    E0base=(d-S0(a)-MAJ(a,b,c))&M; k0=(-S0(a)-MAJ(a,b,c)-h-S1(e)-CH(e,f,g)-K[0])&M
    return dict(a=a,b=b,e=e,f=f,E0base=E0base,k0=k0,KF=(k0+Cc2-g-K[1])&M,K2=(Cc2+k0)&M)
def Ffun(cv,a0,co):
    E0=(a0+co['E0base'])&M
    return (a0-S0(a0)-MAJ(a0,co['a'],co['b'])-S1(E0)-CH(E0,co['e'],co['f'])+co['KF'])&M
def Pfun(u): return (s0(u)-u)&M
def hfun(cv,a0):
    a,b,c,d,e,f,g,h=cv; E0=(a0+d-S0(a)-MAJ(a,b,c))&M
    return (-S0(a0)-MAJ(a0,a,b)-g-S1(E0)-CH(E0,e,f)-K[1])&M
def variantW(cv,a0,a1,SA,SE):
    """W0..W15 of one member of the P1 pair: A0 = a0, A1 = a1, A2..A15 and E6..E15 from the P8 pair"""
    A={-1:cv[0],-2:cv[1],-3:cv[2],-4:cv[3]}; E={-1:cv[4],-2:cv[5],-3:cv[6],-4:cv[7]}
    A[0]=a0; A[1]=a1
    for i in range(2,16): A[i]=SA[i]
    for i in range(6): E[i]=(A[i]+A[i-4]-S0(A[i-1])-MAJ(A[i-1],A[i-2],A[i-3]))&M
    for i in range(6,16): E[i]=SE[i]
    return [(E[i]-A[i-4]-E[i-4]-S1(E[i-1])-CH(E[i-1],E[i-2],E[i-3])-K[i])&M for i in range(16)]
def e16_real(cv,a0,a1): return trace(cv,variantW(cv,a0,a1,SAx,SEx),17)[1][16]
def quot(y): return (y&2)>>1 | ((y>>3)&0x7f)<<1 | (y>>11)<<8
def u_of(v28):
    mix=((v28>>3)^(v28>>11)^(v28>>19)^(v28>>24))&15
    return v28|(mix<<28)
def step_point(cv,co,heads4,v):
    """the walk step on a 29-bit point: returns the 32-bit image y (next point = quot(y))"""
    if v>>28==0:
        j=(v>>26)&3; a0=RTOP|(v&M26); return (Ffun(cv,a0,co)-(T20[heads4[j]]<<13))&M
    return (R16H[0]-Pfun(u_of(v&M28)))&M
# the P8 differences the post-filters test (both members' words): D7, D8, D9s, T8, F7d
_Wx=variantW(PCV,SAx[0],SAx[1],SAx,SEx); _Wy=variantW(PCV,SAy[0],SAy[1],SAy,SEy)
assert _Wx==PMX and _Wy==PMY
D7=(_Wy[7]-_Wx[7])&M; D8=(_Wy[8]-_Wx[8])&M; D9s=(s0(_Wy[9])-s0(_Wx[9]))&M; T8=(s0(_Wy[8])-s0(_Wx[8]))&M; F7d=(s0(_Wy[7])-s0(_Wx[7]))&M
assert (F7d,T8,D8,D7,D9s)==(0x03bff800,0xfe808000,0xfbc00800,0x20000000,0x043ff800)

# ---------------------------------------------------------------- [2] kernel generator and allocator
XOR,AND,OR,NOT=0,1,2,3
class G:
    """gate builder; signals s = node*2 + polarity, constants node -1 (s = -2 + bit)"""
    def __init__(s,nin): s.ops=[(None,j,0) for j in range(nin)]; s.nin=nin; s.calls=0
    def K(s,b): return -2+(b&1)
    def NN(s,x): return x>>1
    def PL(s,x): return x&1
    def emit(s,op,a,b):
        if len(s.ops)>=GEN_MAX: raise SystemExit('kernel generator: gate list cap GEN_MAX reached')   # hard cap: the list never holds more than GEN_MAX entries
        s.ops.append((op,a,b)); return (len(s.ops)-1)*2
    def X(s,a,b):
        s.calls+=1; na,nb=a>>1,b>>1
        if na<0 and nb<0: return s.K((a^b)&1)
        if na<0: return b^(a&1)
        if nb<0: return a^(b&1)
        if na==nb: return s.K((a^b)&1)
        return s.emit(XOR,na,nb)|((a^b)&1)
    def AO(s,a,b,orr):
        s.calls+=1; na,nb=a>>1,b>>1
        if na<0 or nb<0:
            if na<0: a,b=b,a
            cb=b&1
            if orr: return s.K(1) if cb else a
            return a if cb else s.K(0)
        if na==nb: return a if (a&1)==(b&1) else s.K(1 if orr else 0)
        pa,pb=a&1,b&1
        if pa==pb:
            op=(OR if orr else AND) if pa==0 else (AND if orr else OR)
            return s.emit(op,na,nb)|pa
        if pa: a,b=b,a; na,nb=nb,na
        nb2=s.emit(NOT,nb,0)>>1
        return s.emit(OR if orr else AND,na,nb2)
    def MUX(s,sel,a,b):
        if a==b: return a
        d=s.X(a,b)
        if d>>1<0: return s.X(b,s.AO(sel,d,0))
        if (d&1)==(sel&1): return s.X(b,s.AO(sel,d,0))
        return s.X(a,s.AO(sel^1,d,0))
    def FA(s,a,b,c,carry=True):
        t=s.X(a,b); sm=s.X(t,c)
        if not carry: return sm,None
        cs=[a,b,c]; ks=[x for x in cs if x>>1<0]; vs=[x for x in cs if x>>1>=0]
        if len(vs)==0: return sm,s.K(((a&1)+(b&1)+(c&1))>=2)
        if len(vs)==1: return sm,(vs[0] if (ks[0]&1)!=(ks[1]&1) else s.K(ks[0]&1))
        if len(vs)==2: return sm,s.AO(vs[0],vs[1],ks[0]&1)
        pab=(a^b)&1; pac=(a^c)&1; pbc=(b^c)&1
        if pab==pac: return sm,s.X(a,s.AO(t,s.X(a,c),0))
        if pab==pbc: return sm,s.X(b,s.AO(t,s.X(b,c),0))
        return sm,s.X(c,s.AO(s.X(a,c),s.X(b,c),0))
    def add(s,xs,ys):
        out=[]; c=s.K(0)
        for j in range(32):
            sm,c=s.FA(xs[j],ys[j],c,carry=(j<31)); out.append(sm)
        return out
    def cvec(s,val): return [s.K((val>>j)&1) for j in range(32)]
    def rotr(s,xs,n): return [xs[(j+n)%32] for j in range(32)]
    def shr(s,xs,n): return [xs[j+n] if j+n<32 else s.K(0) for j in range(32)]
    def x3(s,a,b,c): return [s.X(s.X(a[j],b[j]),c[j]) for j in range(32)]
    def S0(s,x): return s.x3(s.rotr(x,2),s.rotr(x,13),s.rotr(x,22))
    def S1(s,x): return s.x3(s.rotr(x,6),s.rotr(x,11),s.rotr(x,25))
    def s0(s,x): return s.x3(s.rotr(x,7),s.rotr(x,18),s.shr(x,3))
    def NOTv(s,xs): return [x^1 for x in xs]

def build_kernel(cv,heads4,dpb):
    """gate list of one walk step on 29 input planes; returns (g, out29 signals (polarity 0), dp signal)"""
    g=G(29); co=cv_consts(cv); v=[j*2 for j in range(29)]; side=v[28]
    a0=[v[j] for j in range(26)]+[g.K((RWIN>>k)&1) for k in range(6)]
    E0=g.add(a0,g.cvec(co['E0base'])); S0a=g.S0(a0); S1e=g.S1(E0); a,b,e,f=co['a'],co['b'],co['e'],co['f']
    MAJp=[a0[j] if ((a>>j)&1)!=((b>>j)&1) else g.K((a>>j)&1) for j in range(32)]
    CHp=[(E0[j] if ((e>>j)&1) else E0[j]^1) if ((e>>j)&1)!=((f>>j)&1) else g.K((e>>j)&1) for j in range(32)]
    tconst=[(-(T20[h]<<13))&M for h in heads4]; s1_,s2_=v[26],v[27]
    def f1(b0,b1):
        if b0==b1: return g.K(b0)
        return s1_ if (b0,b1)==(0,1) else s1_^1
    def two_in(bits):
        if bits==[0,0,0,0]: return g.K(0)
        if bits==[1,1,1,1]: return g.K(1)
        return g.MUX(s2_,f1(bits[2],bits[3]),f1(bits[0],bits[1]))
    Tj=[two_in([(tconst[k]>>j)&1 for k in range(4)]) for j in range(32)]
    acc=g.add(a0,g.NOTv(S0a)); acc=g.add(acc,g.NOTv(MAJp)); acc=g.add(acc,g.NOTv(S1e)); acc=g.add(acc,g.NOTv(CHp)); acc=g.add(acc,Tj)
    yA=g.add(acc,g.cvec((co['KF']+4)&M))
    v28=[v[j] for j in range(28)]; mix=[g.X(g.X(g.X(v28[3+i],v28[11+i]),v28[19+i]),v28[24+i]) for i in range(4)]
    u=v28+mix; acc=g.add(u,g.NOTv(g.s0(u))); yB=g.add(acc,g.cvec((R16H[0]+1)&M))
    y=[g.MUX(side,yB[j],yA[j]) for j in range(32)]
    out=[y[j] for j in range(32) if j not in (0,2,10)]
    dp=out[0]
    for j in range(1,dpb): dp=g.AO(dp,out[j],1)           # dp true = 1 iff the lane is NOT a distinguished point
    out=[(s if s<0 or (s&1)==0 else g.emit(NOT,s>>1,0)) for s in out]   # register convention: planes hold true values
    assert all(s>=0 for s in out)
    return g,out,dp
DPREG=64; NFIXED=64; GEN_MAX=1300+29+96   # gate-list cap: KCAP records + 29 inputs + at most 29 forcing NOTs and slack
def allocate(g,out,dp,src,dst):
    """linear-scan register allocation of the gate list: inputs = bank src planes, outputs forced to bank dst,
    the DP plane to DPREG, temporaries from NFIXED+1; returns (records (op,d,a,b), dp polarity, registers used)"""
    nin=g.nin; recs=g.ops[nin:]; last={}
    for i,(op,a,b) in enumerate(recs):
        last[a]=nin+i
        if op!=NOT: last[b]=nin+i
    forced={out[j]>>1:dst*32+j for j in range(29)}; dpn=dp>>1; assert dpn>=0
    if dpn in forced:                                                       # the dp plane is also an output plane: copy via NOT NOT? never happens (dp is an OR)
        raise AssertionError('dp coincides with an output')
    forced[dpn]=DPREG
    for t in forced: last[t]=1<<60
    reg={j:src*32+j for j in range(nin)}; free=[]; nxt=NFIXED+1; res=[]
    for i,(op,a,b) in enumerate(recs):
        nid=nin+i; dying=[]
        for t in ((a,) if op==NOT else (a,b)):
            if t>=nin and last.get(t)==nid and t not in dying: dying.append(t)
        if nid in forced: d=forced[nid]
        elif dying: d=reg[dying[0]]; dying=dying[1:]
        elif free: free.sort(); d=free.pop(0)
        else: d=nxt; nxt+=1
        for t in dying: free.append(reg[t])
        reg[nid]=d; res.append((op,d,reg[a],reg[b] if op!=NOT else 0))
    return res,dp&1,nxt
def to_source(recs,name):
    L=['def %s(R):'%name]; ins=set(); defined=set()
    for op,d,a,b in recs:
        for t in ((a,) if op==NOT else (a,b)):
            if t not in defined: ins.add(t)
        defined.add(d)
    for t in sorted(ins): L.append(' r%d=R[%d]'%(t,t))
    sym={XOR:'^',AND:'&',OR:'|'}
    for op,d,a,b in recs:
        L.append(' r%d=r%d^M'%(d,a) if op==NOT else ' r%d=r%d%sr%d'%(d,a,sym[op],b))
    for d in sorted({d for _,d,_,_ in recs if d<64 or d==DPREG}): L.append(' R[%d]=r%d'%(d,d))
    return '\n'.join(L)
ONES=(1<<256)-1
def make_kernels(cv,heads4,dpb):
    ks=[]
    for src,dst in ((0,1),(1,0)):
        g,out,dp=build_kernel(cv,heads4,dpb); recs,dppol,nreg=allocate(g,out,dp,src,dst)
        ns={'M':ONES}; exec(to_source(recs,'k'),ns)
        ks.append(dict(recs=recs,dppol=dppol,nreg=nreg,fn=ns['k'],ngates=len(g.ops)-g.nin,gen_calls=g.calls))
    return ks
def gen_charge(cv,heads4,dpb):
    """the charged cost of producing one window's two kernel images: the cap P.GCAP (the generator's own Python
    operation count is reported by --census as evidence that the cap is above it)"""
    return P.GCAP

# ---------------------------------------------------------------- [3] the counted machine (prices: proof.md S4)
HIGHMASK=[sum(1<<p for p in range(256) if (p>>k)&1) for k in range(8)]
C_LOG8=sum(r<<((1<<r)^5) for r in range(8))
M32=M; M20=(1<<20)-1; M11=(1<<11)-1; M9=(1<<9)-1; M23=(1<<23)-1; M40=(1<<40)-1
class Mach:
    """counted word RAM: every method is one charged primitive (load/store 3: index shift, base add, access; branch 2)"""
    def __init__(s): s.o=0; s.cat={}; s.blk={}; s.nest=0
    def bs(s): return (s.o,s.nest)
    def be(s,name,b,sub=False):
        d=(s.o-b[0])-(s.nest-b[1])
        if sub: s.nest+=(s.o-b[0])-2
        if d>s.blk.get(name,0): s.blk[name]=d
    def x(s,a,b): s.o+=1; return a^b
    def a(s,a,b): s.o+=1; return a&b
    def r(s,a,b): s.o+=1; return a|b
    def n(s,a): s.o+=1; return a^ONES
    def ad(s,a,b): s.o+=1; return (a+b)&ONES
    def sb(s,a,b): s.o+=1; return (a-b)&ONES
    def sl(s,a,k): s.o+=1; return (a<<k)&ONES
    def sr(s,a,k): s.o+=1; return a>>k
    def rl(s,a,k): s.o+=1; k%=256; return a if k==0 else ((a<<k)|(a>>(256-k)))&ONES
    def rr(s,a,k): return s.rl(a,256-(k%256))
    def ne(s,a,b): s.o+=1; return 1 if a!=b else 0
    def jz(s,a): s.o+=2; return a==0
    def jnz(s,a): s.o+=2; return a!=0
    def jeq(s,a,b): s.o+=2; return a==b
    def jne(s,a,b): s.o+=2; return a!=b
    def jge(s,a,b): s.o+=2; return a>=b
    def ld(s,arr,i): s.o+=3; return arr[i]
    def st(s,arr,i,v): s.o+=3; arr[i]=v
    def mv(s): s.o+=1
    def tick(s,name,t0): s.cat[name]=s.cat.get(name,0)+(s.o-t0)
def mS0(m,v): d=m.r(v,m.sl(v,32)); return m.a(m.x(m.x(m.sr(d,2),m.sr(d,13)),m.sr(d,22)),M32)
def mS1(m,v): d=m.r(v,m.sl(v,32)); return m.a(m.x(m.x(m.sr(d,6),m.sr(d,11)),m.sr(d,25)),M32)
def ms0(m,v): d=m.r(v,m.sl(v,32)); return m.a(m.x(m.x(m.sr(d,7),m.sr(d,18)),m.sr(v,3)),M32)
def mMAJ(m,a,b,c): return m.r(m.a(a,b),m.a(c,m.r(a,b)))
def mCH(m,e,f,g): return m.x(m.a(e,f),m.a(m.x(e,M32),g))
def a32(m,a,b): return m.a(m.ad(a,b),M32)
def s32(m,a,b): return m.a(m.sb(a,b),M32)

class P:
    """the single concrete schedule"""
    DPB=6                 # distinguished point: low 6 bits of the 29-bit point zero
    WIN=1<<25             # walk evaluations per window (131072 iterations of 256 lanes)
    MAXS=1280; CUTP=512   # a trail older than MAXS iterations is cut at the next scan (every CUTP iterations)
    KCAP=1300; RCAP=240   # kernel image cap (records) and register cap
    GCAP=1<<21            # charged generator cost per window (cap)
    WORDS=(1<<14)+(1<<13)+(1<<11)+(1<<10)   # 27,648 table words of 32 bytes, 6 entries of 40 bits (chk 9 | len 11 | id 20)
    BUCKET=True           # True: any of the 6 entries of the word may hold the DP (collision-tolerant); False: the entry is fixed by r
    KEEP_LONGER=True
    QCAP,QFULL=4096,3840
    S2CAP=1<<17           # hard cap on stage-2 iterations per phase (a pair needs at most MAXS+CUTP = 1792; 3840 pairs / 128 slots x 1792 = 53,760)
    CF_HIT=16; CF_ITER=4; CF_PHASE=1024   # charged control-flow allowances: per DP hit (entry scan, flag tests, keep-longer chain), per iteration (cut-scan and halt tests), per stage-2 phase (slot/wheel initialisation)
    NSLOT=128; WHEEL=2048; CMP1=12
    C=2728

class Attack:
    def __init__(s,win=P.WIN,seed=1,check=False,subset=None,measure=True):
        s.m=Mach(); s.win=win; s.check=check; s.subset=subset; s.measure=measure
        s.rnd=random.SystemRandom() if seed is None else random.Random(seed)
        s.R=[0]*512; s.LA=[0]*256; s.sav=[0]*32
        s.st=dict(windows=0,iters=0,hits=0,matches=0,s2phases=0,s2iters=0,pairs=0,merges=0,degenerate=0,same=0,cross=0,
                  claws=0,notclaw=0,c1=0,c2=0,g=0,f7=0,step3b=0,accepted=0,trails=0,cuts=0,qmax=0,slotfull=0)
        s.distinct=set() if measure else None; s.dstage={} if measure else None   # measurement bookkeeping, created only when measure=True (never in --attack)
        s.cv_id=0; s.success=False; s.message=None                                   # exactly one retained collision pair (a single slot, not a list)
        t0=s.m.o; s.m.o+=2*P.C+120; s.m.tick('run_setup',t0)     # advice expansion: the P8 pair's two traces (2 compressions) + constants
    # ----- window
    def window_setup(s,cv=None,m0=None):
        m=s.m; t0=m.o
        if cv is None:
            m0=[s.rnd.getrandbits(32) for _ in range(16)]; m.o+=2+16
            cv=compress(IV,m0); m.o+=P.C
        s.m0=m0; s.cv=cv; s.cv_id+=1
        s.heads4=SUBSETS[(s.cv_id-1)%5] if s.subset is None else SUBSETS[s.subset]
        s.co=cv_consts(cv); m.o+=140
        s.pfc=s.pf_consts(); m.o+=260
        tg=m.o; s.ks=make_kernels(cv,s.heads4,P.DPB)
        assert len(s.ks[0]['recs'])<=P.KCAP and max(s.ks[0]['nreg'],s.ks[1]['nreg'])<=P.RCAP, (len(s.ks[0]['recs']),s.ks[0]['nreg'])
        m.o+=gen_charge(cv,s.heads4,P.DPB); m.tick('generator',tg)
        s.tab=[0]*P.WORDS; m.o+=4*P.WORDS
        s.qn=0; s.qw=[0]*(P.QCAP//4+1); s.cur=0; s.it=0; s.rot=0
        for j in range(32): s.R[j]=(sum(1<<l for l in range(256) if (l>>j)&1) if j<8 else 0)   # trail i starts at point i
        m.o+=32
        for l in range(256): s.LA[l]=l; m.o+=3
        s.idc=256; s.st['windows']+=1; m.tick('window_setup',t0)
    def pf_consts(s):
        """per-window constants of the post-filter chain for both members (counted 260 in window_setup)"""
        cv=s.cv; out=[]
        for SA,SE in ((SAx,SEx),(SAy,SEy)):
            A2,A3,A4,A5=SA[2],SA[3],SA[4],SA[5]; E6,E7,E8,E9=SE[6],SE[7],SE[8],SE[9]
            out.append(dict(cE5=(A5-S0(A4)-MAJ(A4,A3,A2))&M, cE4=(A4-S0(A3))&M, mA=A3&A2, mB=A3|A2,
                            cE3=(A3+cv[0]-S0(A2))&M, A2=A2,
                            c9=(E9-A5-S1(E8)-CH(E8,E7,E6)-K[9])&M, c8=(E8-A4-S1(E7)-K[8])&M, E7=E7, E6=E6,
                            c7=(E7-A3-S1(E6)-K[7])&M))
        return out
    # ----- lane helpers (as 19034ce3)
    def insert_lane(s,base,low,l,val,nbits=20):
        m=s.m; R=s.R; b=m.bs(); m.o+=2
        Z=m.rl(val,l); nl=m.n(low)
        for j in range(nbits):
            t=Z if j==0 else m.rr(Z,j); p=R[base+j]
            R[base+j]=m.x(p,m.a(m.x(p,t),low))
        for j in range(nbits,29): R[base+j]=m.a(R[base+j],nl)
        m.be('insert_lane',b,True)
    def find_lane(s,mask):
        m=s.m; bb=m.bs(); m.o+=2
        low=m.a(mask,m.sb(0,mask)); l=0
        for k in range(7,2,-1):
            b=m.ne(m.a(low,HIGHMASK[k]),0)
            l=m.sl(b,k) if k==7 else m.r(l,m.sl(b,k))
        l=m.r(l,m.a(m.sr(C_LOG8,m.x(m.sr(low,l),5)),7))
        m.be('find_lane',bb,True)
        return low,l
    def extract(s,base,jlo,jhi,low,l,name):
        m=s.m; R=s.R; b=m.bs(); m.o+=2
        Z=m.a(R[base+jhi],low)
        for j in range(jhi-1,jlo-1,-1): Z=m.r(m.rl(Z,1),m.a(R[base+j],low))
        v=m.rr(Z,l); m.be(name,b,True)
        return v
    def qpush(s,pk):
        if s.qn>=P.QCAP: raise SystemExit('queue cap QCAP reached')      # unreachable by the QFULL rule (at most 3839 + 256 pushes before a stage-2 phase); a hard halt, so the queue never grows past its allocation
        m=s.m; b=m.bs(); m.o+=2
        wi=m.sr(s.qn,2); sh=m.sl(m.a(s.qn,3),6); w=m.ld(s.qw,wi)
        w=m.x(w,m.a(m.x(w,m.sl(pk,sh)),m.sl((1<<64)-1,sh))); m.st(s.qw,wi,w); s.qn=m.ad(s.qn,1)
        m.be('qpush',b,True)
    def qpop(s,qi):
        m=s.m; b=m.bs(); m.o+=2
        w=m.ld(s.qw,m.sr(qi,2)); v=m.a(m.sr(w,m.sl(m.a(qi,3),6)),(1<<64)-1); m.be('qpop',b,True)
        return v
    # ----- stage 1
    def iter1(s):
        m=s.m; R=s.R; k=s.ks[s.cur]
        k['fn'](R); m.o+=len(k['recs']); s.cur^=1; s.it+=1; s.st['iters']+=1
        n0=R[DPREG]; m.o+=5+P.CF_ITER
        hit=m.n(n0) if k['dppol']==0 else n0       # dp plane true 1 = not a DP; polarity 1 stores the complement
        if m.jnz(hit):
            t0=m.o
            while True:
                low,l=s.find_lane(hit); hit=m.x(hit,low)
                s.hit(low,l)
                if m.jz(hit): break
            full=m.jge(s.qn,P.QFULL); m.tick('hits',t0)
            if full: s.stage2()
            if s.success: return
        if s.it%P.CUTP==0: s.cutscan()
    def hit(s,low,l):
        m=s.m; R=s.R; base=s.cur*32; s.st['hits']+=1; m.o+=P.CF_HIT; ta=m.bs()
        r=s.extract(base,P.DPB,28,low,l,'extract23')                       # the 23 high bits of the DP
        t=m.ad(m.ad(m.ad(m.sl(r,14),m.sl(r,13)),m.sl(r,11)),m.sl(r,10)); word=m.sr(t,23); chk=m.a(r,M9)   # word = r x WORDS >> 23
        w=m.ld(s.tab,word)
        lw=m.ld(s.LA,l); idv=m.a(lw,M20); ln=m.sb(s.it,m.sr(lw,20))
        en=m.r(m.r(idv,m.sl(m.a(ln,M11),20)),m.sl(chk,31))                 # entry: id | len << 20 | chk << 31 (40 bits); len masked to 11 bits
        m.be('hit_a',ta); tb=m.bs()
        match=False; sub=None
        if P.BUCKET:
            # six entries; find one with this chk and a nonzero length (a MATCH), else an empty one, else the replacement entry
            empty=None
            for i in range(6):
                e=m.a(m.sr(w,40*i),M40)
                if m.jeq(m.sr(e,31),chk) and m.jnz(m.a(m.sr(e,20),M11)): match=True; sub=i; break
                if empty is None and m.jz(m.a(m.sr(e,20),M11)): empty=i
            if not match:
                if empty is not None: sub=empty
                else: sub=s.rot; s.rot=(s.rot+1)%6; m.o+=2; s.st['slotfull']+=1
        else:
            f=m.a(t,M23); sub=m.sr(m.ad(m.sl(f,2),m.sl(f,1)),23)
            e=m.a(m.sr(w,40*sub),M40)
            match=m.jeq(m.sr(e,31),chk) and m.jnz(m.a(m.sr(e,20),M11))
        sh=m.ad(m.sl(sub,5),m.sl(sub,3)); e=m.a(m.sr(w,sh),M40)
        if (not match) or (not P.KEEP_LONGER) or m.jge(ln,m.a(m.sr(e,20),M11)):
            w2=m.x(w,m.sl(m.x(e,en),sh)); m.st(s.tab,word,w2)
        m.be('hit_b',tb)
        if match:
            tc=m.bs(); s.st['matches']+=1
            pk=m.r(m.sl(m.a(e,(1<<31)-1),32),m.a(en,(1<<31)-1)); s.qpush(pk)   # (id|len<<20) of both trails
            if s.qn>s.st['qmax']: s.st['qmax']=s.qn
            m.be('hit_match',tc)
        td=m.bs(); nid=s.idc
        if m.jge(nid,1<<20): m.be('hit_c',td); return
        s.idc=m.ad(nid,1); m.st(s.LA,l,m.r(nid,m.sl(s.it,20))); s.st['trails']+=1
        s.insert_lane(base,low,l,nid); m.be('hit_c',td)
    def cutscan(s):
        m=s.m; t0=m.o; base=s.cur*32
        for l in range(256):
            tl=m.bs(); lw=m.ld(s.LA,l); age=m.sb(s.it,m.sr(lw,20)); m.o+=3
            if m.jge(age,P.MAXS):
                if not m.jge(s.idc,1<<20):
                    low=m.sl(1,l); nid=s.idc; s.idc=m.ad(nid,1); s.st['cuts']+=1
                    m.st(s.LA,l,m.r(nid,m.sl(s.it,20))); s.insert_lane(base,low,l,nid)
            m.be('cut_lane',tl)
        m.tick('cutscan',t0)
    # ----- stage 2
    def stage2(s):
        m=s.m; R=s.R; t0=m.o; s.st['s2phases']+=1; sv=s.cur; m.o+=P.CF_PHASE
        for j in range(32): s.sav[j]=R[sv*32+j]
        m.o+=64
        cur=0; it2=0; qi=0; bact=0; live=0
        free=list(range(P.NSLOT-1,-1,-1)); bid={}; nxt={}; wh=[0]*(P.WHEEL//16); qn=s.qn
        while True:
            while True:
                m.o+=4
                if not (free and qi<qn): break
                tl=m.bs(); m.o+=4; p=free.pop(); pk=s.qpop(qi); qi+=1; m.o+=1
                x1=m.sr(pk,32); x2=m.a(pk,(1<<31)-1); l1=m.sr(x1,20); l2=m.sr(x2,20)
                if m.jge(l1,l2): xA,lA,xB,lB=x1,l1,x2,l2
                else: xA,lA,xB,lB=x2,l2,x1,l1
                m.o+=2; d=m.sb(lA,lB); low=m.sl(1,p)
                s.insert_lane(cur*32,low,p,xA&M20)
                if m.jz(d):
                    s.insert_lane(cur*32,m.sl(low,128),p+128,xB&M20); bact=m.r(bact,low)
                else:
                    idx=m.a(m.ad(it2,d),P.WHEEL-1); wi=m.sr(idx,4); sh=m.sl(m.a(idx,15),4)
                    w=m.ld(wh,wi); head=m.a(m.sr(w,sh),0xFFFF)
                    m.st(bid,p,xB&M20); m.st(nxt,p,head); m.st(wh,wi,m.x(w,m.sl(m.x(head,m.ad(p,1)),sh)))
                live+=1; m.o+=1; s.st['pairs']+=1; m.be('launch',tl)
            if s.success or m.jz(live): break
            if it2>=P.S2CAP: s.st['s2capped']=s.st.get('s2capped',0)+1; break      # hard cap: the remaining pairs of this phase are abandoned
            tw=m.bs(); idx=m.a(it2,P.WHEEL-1); wi=m.sr(idx,4); sh=m.sl(m.a(idx,15),4)
            w=m.ld(wh,wi); head=m.a(m.sr(w,sh),0xFFFF)
            if m.jnz(head): m.st(wh,wi,m.x(w,m.sl(head,sh)))
            m.be('wheel_check',tw)
            while m.jnz(head):
                tl=m.bs(); p=m.sb(head,1); iB=m.ld(bid,p); head=m.ld(nxt,p); lowp=m.sl(1,p)
                s.insert_lane(cur*32,m.sl(lowp,128),p+128,iB); bact=m.r(bact,lowp); m.be('launchB',tl)
            k=s.ks[cur]; k['fn'](R); m.o+=len(k['recs']); cur^=1; it2+=1; m.o+=3; s.st['s2iters']+=1
            tc=m.bs(); base=cur*32; acc=0
            for j in range(P.CMP1):
                pl=R[base+j]; dj=m.x(pl,m.rl(pl,128)); acc=dj if j==0 else m.r(acc,dj)
            cand=m.a(m.n(acc),bact); m.be('cmp1',tc)
            if m.jnz(cand):
                tc=m.bs(); acc2=0
                for j in range(P.CMP1,29):
                    pl=R[base+j]; dj=m.x(pl,m.rl(pl,128)); acc2=dj if j==P.CMP1 else m.r(acc2,dj)
                full=m.a(cand,m.n(acc2)); m.be('cmp2',tc)
                while m.jnz(full):
                    tm=m.bs(); low,l=s.find_lane(full); full=m.x(full,low); s.st['merges']+=1
                    pp=R[(cur^1)*32]; low2=m.r(low,m.sl(low,128))
                    Z=s.extract((cur^1)*32,0,28,low2,l,'extract29x2')
                    x=m.a(Z,M29); y=m.a(m.sr(Z,128),M29)
                    if m.jne(x,y):
                        tcl=m.o; r_cl=s.claw(x,y); m.nest+=m.o-tcl
                        if r_cl: s.success=True
                    else: s.st['degenerate']+=1
                    bact=m.x(bact,low); m.o+=4; free.append(l); live-=1; m.o+=1; m.be('merge',tm)
                    if s.success: break                           # first accepted pair: leave the merge loop
            if s.success: break                                   # ... and the phase: no further pair is examined or retained
        for j in range(32): R[sv*32+j]=s.sav[j]
        m.o+=64; s.qn=0; m.tick('stage2',t0)
    # ----- the claw: decode, exact test, post-filters, step 3b
    def claw(s,x,y):
        m=s.m; t0=m.o; tb=m.bs()
        sx=m.sr(x,28); sy=m.sr(y,28)
        if m.jeq(sx,sy): s.st['same']+=1; m.be('claw_side',tb); m.tick('claw',t0); return 0
        s.st['cross']+=1
        if m.jnz(sx): x,y=y,x
        m.mv(); j=m.a(m.sr(x,26),3); a0=m.r(m.a(x,M26),RTOP)
        v28=m.a(y,M28); mix=m.a(m.x(m.x(m.x(m.sr(v28,3),m.sr(v28,11)),m.sr(v28,19)),m.sr(v28,24)),15); u=m.r(v28,m.sl(mix,28))
        hj=s.heads4[j]; m.o+=3
        m.be('claw_decode',tb)
        r=s.claw_core(a0,hj,u)
        m.tick('claw',t0); return r
    def claw_core(s,a0,hj,u):
        """(a0, head, u) -> exact claw test, post-filters C1 C2 G F7, step 3b; returns 1 on a verified collision"""
        m=s.m; co=s.co; cv=s.cv; tb=m.bs()
        E0=a32(m,a0,co['E0base'])
        F=a32(m,s32(m,s32(m,s32(m,s32(m,a0,mS0(m,a0)),m.x(m.a(a0,co['a']^co['b']),co['a']&co['b'])),mS1(m,E0)),
                        m.x(m.a(E0,co['e']^co['f']),co['f'])),co['KF']); m.o+=0
        Pu=s32(m,ms0(m,u),u)
        d=s32(m,s32(m,F,T20[hj]<<13),s32(m,R16H[0],Pu)); m.o+=1
        if m.jnz(m.a(d,~R16F&M)): s.st['notclaw']+=1; m.be('claw_test',tb); return 0      # the quotient's false positive
        s.st['claws']+=1
        if s.check:
            assert F==Ffun(cv,a0,co) and d in OFFS
            e=e16_real(cv,a0,(u-hfun(cv,a0))&M); assert r16ok(e) and (e&~R16F&M)==R16H[hj]
        if s.measure: s.distinct.add((s.cv_id,a0,u)); dkey=(s.cv_id,a0,u); s.dstage[dkey]=max(s.dstage.get(dkey,0),0)   # measurement only (measure=False in --attack)
        a1=a32(m,a32(m,s32(m,u,F),a0),co['K2'])          # a1 = u - h(a0) = u - F + a0 + K2
        m.be('claw_test',tb); tb=m.bs()
        px,py=s.pfc
        E5x=a32(m,a1,px['cE5']); E5y=a32(m,a1,py['cE5'])
        E4x=s32(m,a32(m,a0,px['cE4']),m.r(px['mA'],m.a(a1,px['mB']))); E4y=s32(m,a32(m,a0,py['cE4']),m.r(py['mA'],m.a(a1,py['mB'])))
        W8x=s32(m,s32(m,px['c8'],E4x),mCH(m,px['E7'],px['E6'],E5x)); W8y=s32(m,s32(m,py['c8'],E4y),mCH(m,py['E7'],py['E6'],E5y))
        c1=m.jeq(s32(m,W8y,W8x),D8); m.be('claw_c1',tb)
        if s.check:
            wx=variantW(cv,a0,a1,SAx,SEx); wy=variantW(cv,a0,a1,SAy,SEy)
            assert (W8x,W8y)==(wx[8],wy[8]) and c1==(((wy[8]-wx[8])&M)==D8)
        if not c1: return 0
        s.st['c1']+=1; tb=m.bs()
        if s.measure: s.dstage[dkey]=max(s.dstage[dkey],1)
        W9x=s32(m,px['c9'],E5x); W9y=s32(m,py['c9'],E5y)
        c2=m.jeq(s32(m,ms0(m,W9y),ms0(m,W9x)),D9s); m.be('claw_c2',tb)
        if s.check: assert (W9x,W9y)==(wx[9],wy[9])
        if not c2: return 0
        s.st['c2']+=1; tb=m.bs()
        if s.measure: s.dstage[dkey]=max(s.dstage[dkey],2)
        g=m.jeq(s32(m,ms0(m,W8y),ms0(m,W8x)),T8); m.be('claw_g',tb)
        if not g: return 0
        s.st['g']+=1; tb=m.bs()
        if s.measure: s.dstage[dkey]=max(s.dstage[dkey],3)
        E3x=s32(m,px['cE3'],mMAJ(m,px['A2'],a1,a0)); E3y=s32(m,py['cE3'],mMAJ(m,py['A2'],a1,a0))
        W7x=s32(m,s32(m,px['c7'],E3x),mCH(m,px['E6'],E5x,E4x)); W7y=s32(m,s32(m,py['c7'],E3y),mCH(m,py['E6'],E5y,E4y))
        f7=m.jeq(s32(m,W7y,W7x),D7) and m.jeq(s32(m,ms0(m,W7y),ms0(m,W7x)),F7d); m.be('claw_f7',tb)
        if s.check: assert (W7x,W7y)==(wx[7],wy[7])
        if not f7: return 0
        s.st['f7']+=1
        if s.measure: s.dstage[dkey]=max(s.dstage[dkey],4)
        return s.step3b(a0,a1)
    def step3b(s,a0,a1):
        """both members' blocks from (cv, a0, a1), two charged compressions, exact comparison of the eight words"""
        m=s.m; tb=m.bs(); s.st['step3b']+=1; cv=s.cv
        Ws=[]
        for SA,SE in ((SAx,SEx),(SAy,SEy)):
            A={-1:cv[0],-2:cv[1],-3:cv[2],-4:cv[3]}; E={-1:cv[4],-2:cv[5],-3:cv[6],-4:cv[7]}; A[0]=a0; A[1]=a1
            for i in range(2,16): A[i]=SA[i]
            for i in range(6): E[i]=s32(m,s32(m,a32(m,A[i],A[i-4]),mS0(m,A[i-1])),mMAJ(m,A[i-1],A[i-2],A[i-3]))
            for i in range(6,16): E[i]=SE[i]
            Ws.append([s32(m,s32(m,s32(m,s32(m,s32(m,E[i],A[i-4]),E[i-4]),mS1(m,E[i-1])),mCH(m,E[i-1],E[i-2],E[i-3])),K[i]) for i in range(16)])
        m.be('step3b_words',tb); tb=m.bs()
        hx=compress(cv,Ws[0]); hy=compress(cv,Ws[1]); m.o+=2*P.C
        ok=all(m.jeq(hx[i],hy[i]) for i in range(8)) and Ws[0]!=Ws[1]
        m.be('step3b_cmp',tb)
        if s.check:
            assert Ws[0]==variantW(cv,a0,a1,SAx,SEx) and Ws[1]==variantW(cv,a0,a1,SAy,SEy)
        if not ok: return 0
        s.st['accepted']+=1
        if s.m0 is not None:                                        # the final verification of the two 3-block digests (FIN)
            m.o+=6*P.C+1600
            ma=b''.join(w.to_bytes(4,'big') for w in s.m0+Ws[0]); mb=b''.join(w.to_bytes(4,'big') for w in s.m0+Ws[1])
            if ma!=mb and digest_r38(ma)==digest_r38(mb): s.message=(ma,mb); s.success=True; return 1   # the one output; every loop exits on s.success
            return 0
        s.success=True; return 1
    def run_window(s,cv=None,m0=None,iters=None):
        s.success=False; s.window_setup(cv,m0)
        for _ in range(iters if iters else s.win//256):
            s.iter1()
            if s.success or s.idc>=1<<20: break                               # trail ids exhausted: the window ends after the final stage 2
        if s.qn and not s.success: s.stage2()
        return s.st

def count_groups(dset):
    par={}
    def find(k):
        while par.get(k,k)!=k: k=par[k]
        return k
    for cvid,a0,u in dset:
        ka,ku=(cvid,0,a0),(cvid,1,u); par.setdefault(ka,ka); par.setdefault(ku,ku); ra,ru=find(ka),find(ku)
        if ra!=ru: par[ra]=ru
    return len(set(find(k) for k in par))

# ---------------------------------------------------------------- [5] selftest, experiments, main
def selftest():
    rr=random.Random(7); print('selftest r38joint')
    # 1. F + P = E16x of the P1 pair (derived identity) on random (cv, a0, u); the P8 pair is a claw and step 3b accepts it
    for _ in range(500):
        cv=[rr.getrandbits(32) for _ in range(8)]; co=cv_consts(cv); a0=rr.getrandbits(32); u=rr.getrandbits(32)
        assert (Ffun(cv,a0,co)+Pfun(u))&M==e16_real(cv,a0,(u-hfun(cv,a0))&M)
    A=Attack(win=1<<12,seed=3,check=True,subset=3); A.window_setup(cv=PCV)
    a0,a1=SAx[0],SAx[1]; u=(a1+hfun(PCV,a0))&M; e=e16_real(PCV,a0,a1); hj=R16H.index(e&~R16F&M)
    assert hj in A.heads4; o0=A.m.o; r=A.claw_core(a0,hj,u); print(' P8 pair through claw_core: accepted=%d ops=%d'%(r,A.m.o-o0)); assert r==1
    # 2. post-filter closed forms equal the real words (check mode asserts inside claw_core) on forced claws from a small window
    # 3. kernel: 256 random lanes against the scalar step, both images
    cv=[rr.getrandbits(32) for _ in range(8)]; co=cv_consts(cv); heads4=SUBSETS[1]; ks=make_kernels(cv,heads4,P.DPB)
    for src in (0,1):
        lanes=[rr.getrandbits(29) for _ in range(256)]; R=[0]*512
        for j in range(29): R[src*32+j]=sum(((lanes[l]>>j)&1)<<l for l in range(256))
        ks[src]['fn'](R); dst=1-src; bad=0
        for l in range(256):
            want=quot(step_point(cv,co,heads4,lanes[l])); got=sum(((R[dst*32+j]>>l)&1)<<j for j in range(29))
            isdp=(want&((1<<P.DPB)-1))==0; flag=(R[DPREG]>>l)&1; notdp=flag if ks[src]['dppol']==0 else 1-flag
            bad+=(got!=want)+(notdp!=(0 if isdp else 1))
        print(' kernel image %d: %d records, %d registers, dppol %d, bad %d'%(src,len(ks[src]['recs']),ks[src]['nreg'],ks[src]['dppol'],bad)); assert bad==0
    # 4. a reduced window in check mode: every claw asserted against the real E16 and the real words
    A=Attack(win=1<<21,seed=11,check=True); t=time.time(); A.run_window()
    print(' window 2^21 check mode: %s  ops=%d  %.1fs'%({k:v for k,v in A.st.items() if v},A.m.o,time.time()-t))
    assert A.st['claws']>0 and A.st['notclaw']>0
    print('SELFTEST PASS')

EXPERIMENTS=('r38-p8-claw','r38-window-small')
def _e1(i,sd):
    """r38-p8-claw. Trial 0: the P8 pair through the shipped claw_core (exact claw test, post-filters, step 3b with two
    compressions) with the kernel built for PCV, and both kernel images executed on 256 random lanes against the scalar step. Trials 1..255: random (cv, a0, u): the row-16 identity F(a0) + P(u) = E16x,
    and the claw predicate against the real E16 for a point pair of the walk's encoding."""
    if i==0:
        A=Attack(win=1<<12,seed=1,check=True,subset=3); A.window_setup(cv=PCV)
        a0,a1=SAx[0],SAx[1]; u=(a1+hfun(PCV,a0))&M; e=e16_real(PCV,a0,a1); hj=R16H.index(e&~R16F&M); o0=A.m.o
        r=A.claw_core(a0,hj,u)
        rr=random.Random(0xA38); kbad=0
        for src in (0,1):                                   # both kernel images on 256 random lanes against the scalar step
            lanes=[rr.getrandbits(29) for _ in range(256)]; R=[0]*512
            for j in range(29): R[src*32+j]=sum(((lanes[l]>>j)&1)<<l for l in range(256))
            A.ks[src]['fn'](R); dst=1-src
            for l in range(256):
                want=quot(step_point(PCV,A.co,A.heads4,lanes[l])); got=sum(((R[dst*32+j]>>l)&1)<<j for j in range(29))
                isdp=(want&((1<<P.DPB)-1))==0; flag=(R[DPREG]>>l)&1; notdp=flag if A.ks[src]['dppol']==0 else 1-flag
                kbad+=(got!=want)+(notdp!=(0 if isdp else 1))
        out={'accepted':r,'kernel_lanes':512,'kernel_bad':kbad,'claws':A.st['claws'],'c1':A.st['c1'],'c2':A.st['c2'],'g':A.st['g'],'f7':A.st['f7'],'step3b':A.st['step3b'],
             'claw_ops':A.m.o-o0,'kernel_records':len(A.ks[0]['recs']),'kernel_regs':max(A.ks[0]['nreg'],A.ks[1]['nreg']),
             'sfs_collision':int(compress(PCV,PMX)==compress(PCV,PMY) and PMX!=PMY),'blk_census':sum(A.m.blk.values())}
        assert out['accepted']==1 and out['sfs_collision']==1 and out['claws']==out['c1']==out['c2']==out['g']==out['f7']==out['step3b']==1 and out['kernel_bad']==0
        return out
    rnd=random.Random(sd); cv=[rnd.getrandbits(32) for _ in range(8)]; co=cv_consts(cv)
    x=rnd.getrandbits(28); y=rnd.getrandbits(28)|(1<<28); j=(x>>26)&3; a0=RTOP|(x&M26); u=u_of(y&M28); heads4=SUBSETS[sd%5]
    a1=(u-hfun(cv,a0))&M; e=e16_real(cv,a0,a1)
    d=((Ffun(cv,a0,co)-(T20[heads4[j]]<<13))-(R16H[0]-Pfun(u)))&M
    out={'identity':int((Ffun(cv,a0,co)+Pfun(u))&M==e),'w1_is_u':int(variantW(cv,a0,a1,SAx,SEx)[1]==u),
         'claw_iff_r16':int((d in OFFS)==(r16ok(e) and (e&~R16F&M)==R16H[heads4[j]])),
         'quot_match':int(quot(step_point(cv,co,heads4,x))==quot(step_point(cv,co,heads4,y)))}
    assert out['identity']==1 and out['w1_is_u']==1 and out['claw_iff_r16']==1
    return out
WIN_EXP={   # frozen counts of r38-window-small on the organizer trial seeds (int(seed[:16],16)): hits, matches, s2iters, merges, cross, raw claws, distinct, groups, c1, c2, ops, records, blk census
    13353826747539155261:(16437,888,853,888,431,185,184,184,23,3,13544329,1229,772),
    8529908969004918242:(16343,862,812,862,413,178,175,175,25,0,13535361,1246,752),
    18362963209688203087:(16203,904,840,904,416,185,183,183,21,2,13466257,1229,783),
    6505625951789745816:(16335,933,819,933,440,198,193,193,24,4,13618813,1255,772)}
def _e2(i,sd):
    """r38-window-small. Trials 0..3: four windows of 2^20 walk evaluations (4096 iterations), check mode, first block from the
    trial seed; every claw asserted against the real E16 and the real words; frozen counts for the organizer seeds."""
    if i>=4: return None
    A=Attack(win=1<<20,seed=sd,check=True); A.run_window(); st=A.st; dg=count_groups(A.distinct)
    tup=(st['hits'],st['matches'],st['s2iters'],st['merges'],st['cross'],st['claws'],len(A.distinct),dg,st['c1'],st['c2'],A.m.o,len(A.ks[0]['recs']),sum(A.m.blk.values()))
    if sd in WIN_EXP: assert tup==WIN_EXP[sd]
    return {'iterations':st['iters'],'dp_hits':st['hits'],'matches':st['matches'],'stage2_iterations':st['s2iters'],'merges':st['merges'],
            'cross':st['cross'],'raw_claws':st['claws'],'distinct_claws':len(A.distinct),'distinct_groups':dg,'c1':st['c1'],'c2':st['c2'],
            'ops':A.m.o,'kernel_records':len(A.ks[0]['recs']),'blk_census':sum(A.m.blk.values())}
def serve():
    req=json.load(sys.stdin); eid=req['experiment_id']
    if eid not in EXPERIMENTS: raise SystemExit('unknown experiment id')
    fn=_e1 if eid==EXPERIMENTS[0] else _e2; rows=[]
    for t in req['trials']:
        obs=fn(t['trial'],int(t['seed'][:16],16)); row={'trial':t['trial'],'message_a_hex':None,'message_b_hex':None}
        if obs: row['observations']=obs
        rows.append(row)
    sys.stdout.write(json.dumps({'schema_version':1,'trials':rows},sort_keys=True,separators=(',',':'))+'\n')

B_WINDOWS=3227292921399400871242; W_BUDGET=2082564932999596136475692503019   # proof.md Section 7, set from the 24 pre-declared windows
def main():
    a=sys.argv[1:]
    if '--selftest' in a: selftest(); return
    if '--windows' in a:
        nwin=int(a[a.index('--windows')+1]); seed=int(a[a.index('--seed')+1]) if '--seed' in a else 1; res=[]
        win=int(a[a.index('--win')+1]) if '--win' in a else P.WIN
        A=None
        for w in range(nwin):
            A=None                                   # the previous window's allocations are released before the next window is built
            A=Attack(win=win,seed=seed*1000+w,check='--check' in a,subset=(seed+w)%5); t=time.time(); A.run_window()   # head subset rotates from the seed, as the attack rotates from its start
            st=dict(A.st); st.update(ops=A.m.o,cat=dict(A.m.cat),blk=dict(A.m.blk),sec=time.time()-t,kernel_len=len(A.ks[0]['recs']),
                     kernel_nreg=max(A.ks[0]['nreg'],A.ks[1]['nreg']),distinct_claws=len(A.distinct),distinct_groups=count_groups(A.distinct),
                     seed=seed*1000+w,heads4=A.heads4,subset=(seed+w)%5,bucket=P.BUCKET,keep=P.KEEP_LONGER,win=win,gen_calls=A.ks[0]['gen_calls']+A.ks[1]['gen_calls'],ngates=A.ks[0]['ngates'],
                     dist_c1=sum(1 for v in A.dstage.values() if v>=1),dist_c2=sum(1 for v in A.dstage.values() if v>=2),dist_g=sum(1 for v in A.dstage.values() if v>=3),dist_f7=sum(1 for v in A.dstage.values() if v>=4))
            res.append(st)
            print('window %d: %d distinct claws, %d ops, %.1f per claw, %.0fs'%(w,st['distinct_claws'],st['ops'],st['ops']/max(1,st['distinct_claws']),st['sec']),flush=True)
        if '--out' in a: json.dump(res,open(a[a.index('--out')+1],'w'))
        return
    if '--attack' in a:
        seed=int(a[a.index('--seed')+1]) if '--seed' in a else None; w=0; work=0; A=None
        start=random.SystemRandom().randrange(5) if seed is None else seed%5   # the five head subsets are cycled from a uniform random start
        while (B_WINDOWS is None or w<B_WINDOWS) and (W_BUDGET is None or work<W_BUDGET):
            A=None                                   # the previous window's table, queue and images are released before the next window is built (one window's allocations at a time)
            A=Attack(win=P.WIN,seed=None if seed is None else seed*1000+w,check=False,subset=(start+w)%5,measure=False); A.run_window(); w+=1; work+=A.m.o+6
            if A.message is not None: ma,mb=A.message; print('collision',ma.hex(),mb.hex(),flush=True); return
        print('no collision after %d windows (%d charged operations)'%(w,work)); sys.exit(1)
    serve()
if __name__=='__main__': main()
