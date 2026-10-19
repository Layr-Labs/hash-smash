#!/usr/bin/env python3
# p1claw38.py - sha256-r38, the A0-variant two-block procedure of ePrint 2026/1120 with the characteristic P8 of dariolina's 1a695f0b
# (data, credited) and the "P1" sum-claw that finds the row-16 passes by a meet-in-the-middle between a 2^26-slot table over the
# low variant word a0 and a scan over the free word u = W1, instead of the bit-sliced plane programs of fb176310.  Own code (no
# program of another participant is executed; P8's cells, pair and conditions are data read from the public proof of 1a695f0b,
# credited in proof.md Section 2).  Standard library only.
# Sections: (1) SHA-256 r38 reference; (2) P8 characteristic and the S pair; (3) the counted claw machine and ledger; (4) organizer
# experiments p1-online-r38 and p1-q3-r38 (stdin JSON -> stdout JSON); (5) selftest, calibrate, ledger, main.
import sys, json, hashlib, struct, math, random
from fractions import Fraction

# ----------------------------------------------------------------- (1) reference
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

# ----------------------------------------------------------------- (2) P8 characteristic and the S pair (1a695f0b, transcription)
PCV = [0x95a24959,0xb4053f95,0x1bf0473e,0x1eab3b7c,0x650c63d3,0xe6493d3b,0xed004f1d,0xeb7eaad3]
PMX = [0xbd047e95,0x1dc94891,0x4bbe458b,0xc7dc3c0a,0x8b6235e1,0x9d7630ee,0x569da3a0,0x94ddb1c2,0x464e545d,0xa804c932,0xacecbe75,
       0xc8280172,0x9a4d6768,0x16139532,0xe00d6a99,0x5fb2827b]
PMY = [0xbd047e95,0x1dc94891,0x4bbe458b,0xc7dc3c0a,0x8b6235e1,0x9d7630ee,0x569da3a0,0xb4ddb1c2,0x420e5c5d,0x8804c932,0xa9edacdf,
       0xc8200d72,0x9a4d6768,0x16139532,0xe00d6a99,0x5bf28a7b]
_ROWS = ("=nu============================= uuu============================= ==n=============================|"
 "=========n=====n====n======n==== ==n=u====n==nu=====nu===u==n==== =====u===u==========n===========|"
 "================================ ======nn===n================n=nn ==u=============================|"
 "===============n===========u==== =u=============n===========u==== =====u=n=======n===u==u=n=u=n=n=|"
 "====n===============n========u== ==n==n==u=====un================ ============u=======nn==========|"
 "==u====u==u==========uu=======u= =nu=u==n==n=====u=n=nn=========u ================================|"
 "==n============================= =========n============n=nuu==uu= ================================|"
 "====n=========n=========n==n==== ====u=========n================= ================================|"
 "======n=u======un=============== ====================n===u======= =====u===n==========n===========|"
 "================================ =u==1====n===+u====u0=u=0==+==== ==u=============================|"
 "==u============================= =0=====++0===+0=+==01=0=0==+==== ================================|"
 "================================ =0=====++1===n1=+==1==1====n==== ================================|"
 "================================ ==+====nn=======u=============== ================================|"
 "================================ ==+====00====1==0==========1==== ================================|"
 "================================ ==u====10=======1=============== ================================|"
 "================================ ==0============================= ================================").split('|')
CELLS=[[(0,0,0)]*NR for _ in range(3)]; PQ=[0]*NR; _PL={}
for _r,_l in enumerate(_ROWS):
    for _k,_s in enumerate(_l.split()):
        m=v=x=p=0
        for _j,_c in enumerate(_s):
            b=1<<(31-_j); m|=b*(_c in 'un01'); v|=b*(_c in 'u1'); x|=b*(_c in 'un'); p|=b*(_c=='+')
        CELLS[_k][_r+7]=(m,v,x); _PL[_r+7]=_PL.get(_r+7,0)|p
for _i in _PL: PQ[_i]=_PL[_i]&_PL.get(_i-1,0)
PQE=list(PQ); PQE[18]=0                       # accepted event does not impose E18 = E17 on bits 24,23,15 (Section 6.1)
X2=[]
for _t in ('E16 7 = E16 26,E16 14 ! E16 28,A15 4 = A16 4,E16 11 = E16 16,A15 7 = A16 7,A14 15 = A16 15,A14 16 = A16 16,A15 17 = A16 17,'
           'A14 23 = A16 23,A14 25 = A16 25,A15 27 = A16 27,E16 3 ! E16 8,E16 4 = E16 23,W16 20 ! W16 27,W16 22 = W16 31,W16 4 ! W16 6,'
           'A15 29 = A16 29,W16 14 = W16 18,W16 8 = W16 25,W16 1 ! W16 12,A17 9 ! A17 20,A16 15 = A17 15,A17 6 = A17 18,A16 16 ! A17 16,'
           'A16 23 = A17 23,A16 25 = A17 25,A17 8 ! A17 17,E18 0 = E18 13,E18 17 = E18 22,E18 5 ! E18 23,A16 29 = A18 29,E18 9 = E18 23,'
           'E21 10 = E21 15,E21 11 = E21 24,E21 2 = E21 16').split(','):
    _a,_b,_e,_c,_d=_t.split()
    X2.append(('AEW'.index(_a[0]),int(_a[1:]),int(_b),int(_e=='='),'AEW'.index(_c[0]),int(_c[1:]),int(_d),max(int(_a[1:]),int(_c[1:]))))
def cellok(k,i,x,y):
    m,v,df=CELLS[k][i]; return (x&m)==v and (x^y)==df
def exact(tx,ty): return all(tx[k][i]==ty[k][i] for k in (0,1) for i in range(34,38))
def rowok(tx,ty,i):
    if i<0: return True
    (Ax,Ex,Wx),(Ay,Ey,Wy)=tx,ty
    if not (cellok(0,i,Ax[i],Ay[i]) and cellok(1,i,Ex[i],Ey[i])): return False
    if i not in (7,8) and not cellok(2,i,Wx[i],Wy[i]): return False
    if (Ex[i]^Ex[i-1])&PQE[i]: return False
    for (k1,i1,b1,eq,k2,i2,b2,row) in X2:
        if row==i and (((tx[k1][i1]>>b1)^(tx[k2][i2]>>b2))&1)!=(0 if eq else 1): return False
    return True
_tx=trace(PCV,PMX); _ty=trace(PCV,PMY)
SAx=[_tx[0][i] for i in range(16)]; SAy=[_ty[0][i] for i in range(16)]
SE={i:_tx[1][i] for i in range(4,16)}
D7,T7=0x20000000,0x03bff800
def inF7(w): return ((s0((w+D7)&M)-s0(w))&M)==T7
C4=(SAx[4]-S0(SAx[3])-MAJ(SAx[3],SAx[2],SAx[1]))&M
W8C=(SE[8]-SAx[4]-S1(SE[7])-CH(SE[7],SE[6],SE[5])-K[8])&M
D8=(PMY[8]-PMX[8])&M; T8=(s0(PMY[8])-s0(PMX[8]))&M
def in_G(a0):
    w=(W8C-((a0+C4)&M))&M; return ((s0((w+D8)&M)-s0(w))&M)==T8
def c7of(a0):
    e4=(a0+C4)&M; return (SE[7]-2*SAx[3]+S0(SAx[2])+MAJ(SAx[2],SAx[1],a0)-S1(SE[6])-CH(SE[6],SE[5],e4)-K[7])&M
def words_from_cv(cv,a0):
    out=[]
    for SA in (SAx,SAy):
        A={-1:cv[0],-2:cv[1],-3:cv[2],-4:cv[3]}; E={-1:cv[4],-2:cv[5],-3:cv[6],-4:cv[7]}
        for i in range(14): A[i]=SA[i]
        A[0]=a0
        for i in range(14): E[i]=(A[i]+A[i-4]-S0(A[i-1])-MAJ(A[i-1],A[i-2],A[i-3]))&M
        out.append([(E[i]-A[i-4]-E[i-4]-S1(E[i-1])-CH(E[i-1],E[i-2],E[i-3])-K[i])&M for i in range(14)])
    return out
MASK=0x7fe96c7c
CLASSES=[(0x2a7beb1b,0x9b649791),(0x2a7bfb1b,0x9b648791),(0x2a7feb1b,0x9b609793),(0x2a7ffb1b,0x9b608793),
         (0xaa7beb1b,0x1b649791),(0xaa7bfb1b,0x1b648791),(0xaa7feb1b,0x1b609793),(0xaa7ffb1b,0x1b608793)]
LB=(11,2,3,6,13,14,16,19); G1=(0x10,0x20,0x30)
G3=[int(t,16)<<20 for t in '1b6 1b8 236 238 240 246 248 24e 250 256 258 260 266 268 26e 270 3b6 3b8 436 438 440 446 448 44e 450 456 458 460 466 468 46e 470'.split()]
NB=96
def bconst(ci,b): return (CLASSES[ci][1]&~MASK&M)|G1[b%3]|G3[b//3]
def lane_a0(c,L):
    a=c|(0x800 if L&1 else 0x400)
    for k in range(1,8): a|=((L>>k)&1)<<LB[k]
    return a
_A,_E=_tx[0],_tx[1]
C16=(_A[12]+_E[12]+S1(_E[15])+CH(_E[15],_E[14],_E[13])+K[16]+s1(PMX[14])+PMX[9])&M
R16H=[int(t,16) for t in ('4b02d320 7b1ab320 7b22b320 7b3ab320 c802f320 c80ad320 c80af320 c812d320 c822f320 c82ad320 c82af320 c832d320 '
                          'cb12f320 cb1ad320 cb1af320 cb22d320 cb32f320 cb3ad320 cb3af320 fb02b320').split()]
R16F=0x405
def r16ok(e): return (e&~R16F&M) in R16H
OFFS=(0,1,4,5,1024,1025,1028,1029)
T160=sorted(h+o for h in R16H for o in OFFS)      # the 160-word row-16 set S160 (= R16W)

# ----------------------------------------------------------------- (3) the counted claw machine and ledger
# Pricing (collision-frontier-v5, proof.md Section 4; the same machine as fb176310 Section 9.1): load, store, add, sub, and, or, xor,
# not, shift, immediate, random word = 1; compare-and-branch = 2; S0/S1/s0/s1 = 8; CH = 3; MAJ = 4; a table access = address add (1)
# + load or store (1).  Cc2 is the step-0/1 constant of F.  R = 9 is the best a0 window (top 6 bits of a0), from the exhaustive qpf scan.
Cc2=0x7af32e15; RWIN=9; LS=26; TB=32-LS; RTOP=RWIN<<LS; PK_LD=5; PK_ST=9
def cv_consts(cv):
    a,b,c,d,e,f,gg,h=cv
    k0=(-S0(a)-MAJ(a,b,c)-h-S1(e)-CH(e,f,gg)-K[0])&M
    E0base=(d-S0(a)-MAJ(a,b,c))&M
    PP=a&b; QQ=a|b; EF=e^f; FF=f; KF=(k0+Cc2-gg-K[1])&M; K2=(Cc2+k0)&M
    return dict(k0=k0,E0base=E0base,PP=PP,QQ=QQ,EF=EF,FF=FF,KF=KF,K2=K2)
def hfun(cv,a0):
    a,b,c,d,e,f,gg,h=cv; E0=(a0+d-S0(a)-MAJ(a,b,c))&M
    return (-S0(a0)-MAJ(a0,a,b)-gg-S1(E0)-CH(E0,e,f)-K[1])&M
def Ffun(cv,a0,co): return (a0+co['k0']+hfun(cv,a0)+Cc2)&M      # F(a0) = Cc2 + a0 + k0 + h(a0)
def spair_claw_consts():
    cvS=[SAx[3],SAx[2],SAx[1],SAx[0],SE[7-4+4] if False else _tx[1][3],_tx[1][2],_tx[1][1],_tx[1][0]]
    # the S pair's own chaining value (rows -4..-1) and its post-filter differences
    cvS=[_tx[0][3],_tx[0][2],_tx[0][1],_tx[0][0],_tx[1][3],_tx[1][2],_tx[1][1],_tx[1][0]]
    def Wof(A,E):
        return [(E[i+4]-A[i]-E[i]-S1(E[i+3])-CH(E[i+3],E[i+2],E[i+1])-K[i])&M for i in range(16)]
    Ax={i:_tx[0][i] for i in range(-4,16)}; Ex={i:_tx[1][i] for i in range(-4,16)}
    Ay={i:_ty[0][i] for i in range(-4,16)}; Ey={i:_ty[1][i] for i in range(-4,16)}
    Wx=[(Ex[i]-Ax[i-4]-Ex[i-4]-S1(Ex[i-1])-CH(Ex[i-1],Ex[i-2],Ex[i-3])-K[i])&M for i in range(16)]
    Wy=[(Ey[i]-Ay[i-4]-Ey[i-4]-S1(Ey[i-1])-CH(Ey[i-1],Ey[i-2],Ey[i-3])-K[i])&M for i in range(16)]
    return dict(D7=(Wy[7]-Wx[7])&M, D8=(Wy[8]-Wx[8])&M, D9=(Wy[9]-Wx[9])&M,
                T8=(s0(Wy[8])-s0(Wx[8]))&M, F7d=(s0(Wy[7])-s0(Wx[7]))&M, D9s=(s0(Wy[9])-s0(Wx[9]))&M)
SPC=spair_claw_consts()
assert (SPC['F7d'],SPC['T8'],SPC['D8'],SPC['D7'],SPC['D9s'])==(0x03bff800,0xfe808000,0xfbc00800,0x20000000,0x043ff800), SPC

class Mach:
    __slots__=('ops','nld')
    def __init__(self): self.ops=0; self.nld=0
    def op(self,n=1): self.ops+=n
    def br(self): self.ops+=2
    def ld(self): self.ops+=2; self.nld+=1
    def st(self): self.ops+=2
def pf_consts(cv):
    # scalars of the post-filter chain C1 (top 3 bits of E5 = 101b), C2 (W9 in F9), G (W8 in G'), F7 (W7 in F7)
    A2,A3,A4,A5=SAx[6],SAx[7],SAx[8],SAx[9]; E6,E7,E8,E9=SE[10],SE[11],SE[12],SE[13]
    cE5=(A5-S0(A4)-MAJ(A4,A3,A2))&M
    KW9=(E9-A5-S1(E8)-CH(E8,E7,E6)-K[9])&M; cW9=(KW9-cE5)&M
    cE4=(A4-S0(A3))&M; mA=A3&A2; mB=A3|A2
    KW8=(E8-A4-S1(E7)-K[8])&M; cA=E7&E6; cB=~E7&M
    KK7c=(E7-2*A3-cv[0]+S0(A2)-S1(E6)-CH(E6,E5 if False else E5,0) if False else 0)
    KK7c=(E7-2*A3-cv[0]+S0(A2)-S1(E6)-K[7])&M     # the CH(E6,E5,E4) term is folded with a1,a0 at filter time
    D7c=(_ty[1][11]-_tx[1][11])&M
    return dict(cE5=cE5,cW9=cW9,cE4=cE4,mA=mA,mB=mB,KW8=KW8,cA=cA,cB=cB,A2=A2,E6=E6,KK7c=KK7c,D7c=D7c)
def postfilters(m,cv,a0,u,F,pf):
    # counted chain on (a0, u, F); returns stage flags (c1,c2,g,f7).  Each S0/S1/s0=8, CH=3, MAJ=4, others 1, branch 2.
    a1=((u-F)+cv_consts(cv)['K2']+a0)&M; m.op(3)
    E5=(a1+pf['cE5'])&M; m.op(1)
    s1f=s2=s3=s4=0
    m.br()
    if (E5&0xE0000000)==0xA0000000:
        s1f=1
        w9=(pf['cW9']-a1)&M; m.op(1); w9y=(w9+SPC['D9'])&M; m.op(1)
        d9=(s0(w9y)-s0(w9))&M; m.op(16+1)
        m.br()
        if d9==SPC['D9s']:
            s2=1
            maj1=(pf['mA']|(a1&pf['mB']))&M; m.op(2)
            E4=((a0+pf['cE4'])-maj1)&M; m.op(2)
            chx=(pf['cA']^(pf['cB']&E5))&M; m.op(2)
            w8=((pf['KW8']-E4)-chx)&M; m.op(2); w8y=(w8+SPC['D8'])&M; m.op(1)
            d8=(s0(w8y)-s0(w8))&M; m.op(16+1)
            m.br()
            if d8==SPC['T8']:
                s3=1
                maj2=MAJ(pf['A2'],a1,a0); m.op(4)
                ch2=CH(pf['E6'],E5,E4); m.op(3)
                w7=((pf['KK7c']+maj2)-ch2)&M; m.op(2); w7y=(w7+pf['D7c'])&M; m.op(1)
                d7=(s0(w7y)-s0(w7))&M; m.op(16+1)
                m.br()
                if d7==SPC['F7d']: s4=1
    return s1f,s2,s3,s4

def run_claw(cv,LU,ls=18,count=True,ref=False,collect_all=False,cap=None):
    """Build the 2^ls table over a0 in window RWIN, scan 2^LU values of u, return claws, good pairs and the op count.
    The full-scale procedure uses ls = 26; the organizer experiment runs a reduced ls so the request finishes in the sandbox.
    count: charge operations per the ledger pricing.  ref: also count claws with an independent sorted-array search."""
    TB=32-ls; RTOP=(RWIN<<ls)&M
    co=cv_consts(cv); pf=pf_consts(cv)
    tm=(1<<TB)-1; pmask=tm&~5; smask=(1<<ls)-1; SENT=M
    tab=[SENT]*(1<<ls)
    m=Mach() if count else None
    for i in range(1<<ls):
        a0=(RTOP|i)&M; Fv=Ffun(cv,a0,co); slot=Fv>>TB; tab[slot]=(i<<TB)|(Fv&tm)
    occ=sum(1 for e in tab if e!=SENT)
    # scan (deterministic xorshift seeded from the chaining value)
    st=(0x9E3779B97F4A7C15 ^ ((cv[0]<<32)|cv[1]))&0xFFFFFFFFFFFFFFFF
    def rnd():
        nonlocal st
        st^=(st<<13)&0xFFFFFFFFFFFFFFFF; st^=st>>7; st^=(st<<17)&0xFFFFFFFFFFFFFFFF; return (st>>16)&M
    claws=0; passes=[0,0,0,0]; goodpairs=[]; refclaws=0; allclaws=[]
    if ref:
        Fs=sorted(((s<<TB)|(tab[s]&tm)) for s in range(1<<ls) if tab[s]!=SENT)
        import bisect
    for n in range(1<<LU):
        u=rnd(); P=(s0(u)-u)&M
        for h in R16H:
            W=(h-P)&M
            lo=W&tm; strad=lo>=tm-4
            for Wsub in (W,(W+1024)&M):
                idx=Wsub>>TB; e=tab[idx]
                if ((e-Wsub)&pmask)==0 and e!=SENT:
                    F=((idx<<TB)|(e&tm))&M; dd=(F-Wsub)&M
                    if (dd&~5)==0:
                        claws+=1; a0=(RTOP|(e>>TB))&M
                        s1f,s2,s3,s4=postfilters(m or Mach(),cv,a0,u,F,pf)
                        for j,s in enumerate((s1f,s2,s3,s4)): passes[j]+=s
                        if collect_all: allclaws.append((a0,(u-hfun(cv,a0))&M,u))
                        if s4: goodpairs.append((a0,(u-hfun(cv,a0))&M,u))
                if strad:
                    idx2=(idx+1)&smask; e2=tab[idx2]
                    if e2!=SENT:
                        F2=((idx2<<TB)|(e2&tm))&M; dd=(F2-Wsub)&M
                        if (dd&~5)==0:
                            claws+=1; a0=(RTOP|(e2>>TB))&M
                            s1f,s2,s3,s4=postfilters(m or Mach(),cv,a0,u,F2,pf)
                            for j,s in enumerate((s1f,s2,s3,s4)): passes[j]+=s
                            if collect_all: allclaws.append((a0,(u-hfun(cv,a0))&M,u))
                            if s4: goodpairs.append((a0,(u-hfun(cv,a0))&M,u))
        if ref:
            for h in R16H:
                for o in OFFS:
                    want=((h+o)-P)&M; k=bisect.bisect_left(Fs,want)
                    if k<len(Fs) and Fs[k]==want: refclaws+=1
    return dict(occ=occ,occ_frac=occ/(1<<ls),claws=claws,refclaws=refclaws,passes=passes,
                goodpairs=goodpairs,allclaws=allclaws,ops=(m.ops if count else 0))

SExF=[_tx[1][i] for i in range(16)]; SEyF=[_ty[1][i] for i in range(16)]
def variantW_P1(cv,a0,a1,SA,SEF):
    """W0..W15 of one member of the P1 variant (BOTH a0 = A0 and a1 = A1 free; A2..A15 = S, E6..E15 = S).  Port of p1claw.c variantW."""
    A={-1:cv[0],-2:cv[1],-3:cv[2],-4:cv[3]}; E={-1:cv[4],-2:cv[5],-3:cv[6],-4:cv[7]}
    A[0]=a0; A[1]=a1
    for i in range(2,16): A[i]=SA[i]
    for i in range(6): E[i]=(A[i]+A[i-4]-S0(A[i-1])-MAJ(A[i-1],A[i-2],A[i-3]))&M
    for i in range(6,16): E[i]=SEF[i]
    return [(E[i]-A[i-4]-E[i-4]-S1(E[i-1])-CH(E[i-1],E[i-2],E[i-3])-K[i])&M for i in range(16)]
def e16_real_p1(cv,a0,a1):
    """The real E16 of member x of the P1 claw pair (a0,a1); equals F(a0) + Phi(u), checked 0 bad by p1claw.c."""
    W=variantW_P1(cv,a0,a1,SAx,SExF); return trace(cv,W)[1][16]

# ----------------------------------------------------------------- (4) organizer experiments
# organizer budget: one request of 256 trials within 20 s (runner.py); trials 0..NWORK-1 do the work, the rest return no pair.
NWORK=8; ONLINE_LS=17; ONLINE_LU=13; Q3_LS=17; Q3_LU=14
class Shake:
    def __init__(self,label): self.buf=b''; self.n=0; self.lab=label.encode()
    def word(self):
        if not self.buf: self.buf=hashlib.shake_256(self.lab+struct.pack('<I',self.n)).digest(256); self.n+=1
        w=struct.unpack('<I',self.buf[:4])[0]; self.buf=self.buf[4:]; return w
def cv_from_seed(seed):
    sh=Shake(seed); M0=[sh.word() for _ in range(16)]; return compress(IV,M0),M0
def online_experiment(req):
    out=[]; LU=req.get('lu',ONLINE_LU)
    for tr in req['trials']:
        t=tr['trial']; rec=dict(trial=t,message_a_hex=None,message_b_hex=None)
        if t<NWORK:
            ls=req.get('ls',ONLINE_LS)
            cv,M0=cv_from_seed(req['experiment_id']+'|'+tr['seed'])
            r=run_claw(cv,LU,ls=ls,count=True,ref=True,collect_all=True)
            # every claw is a row-16 pass by construction: verify its real E16 (both free words a0,a1) lands in the 160-word set
            bad=0; verified=0
            exp_claws=160.0*r['occ']*(1<<LU)/2**32
            for (a0,a1,u) in r['allclaws']:
                if r16ok(e16_real_p1(cv,a0,a1)): verified+=1
                else: bad+=1
            rec['observations']=dict(occ_frac=round(r['occ_frac'],6),claws=r['claws'],ref_claws=r['refclaws'],
                claws_equal_ref=int(r['claws']==r['refclaws']),expected_claws=round(exp_claws,1),
                c1=r['passes'][0],c1c2=r['passes'][1],c1c2g=r['passes'][2],all4=r['passes'][3],
                good_pairs=len(r['goodpairs']),claw_e16_bad=bad,claw_e16_in_S160=verified,counted_ops=r['ops'])
            if r['goodpairs'] and bad==0:
                a0,a1,u=r['goodpairs'][0]
                wx=variantW_P1(cv,a0,a1,SAx,SExF); wy=variantW_P1(cv,a0,a1,SAy,SEyF)
                rec['message_a_hex']=struct.pack('>32I',*(M0+wx)).hex()
                rec['message_b_hex']=struct.pack('>32I',*(M0+wy)).hex()
        out.append(rec)
    return dict(schema_version=1,trials=out)
def q3_experiment(req):
    """Evidence for H2-P1.  Every claw is a row-16 pass of a P1 good pair; the structural lemma (proof.md Section 7) says rows 17..21 of
    both members then follow the P8 cells by construction (they read only S's words and W16..W21).  Collect claws from the counted procedure
    at a reduced ls and report how many pass rows 17..21 cumulatively and the post-filter stage rates.  No full collision is returned (q3
    is 2^-96; the pooled rate at this scale is the stage product, which matches the exact enumeration)."""
    out=[]; ls=req.get('ls',Q3_LS); LU=req.get('lu',Q3_LU)
    for tr in req['trials']:
        t=tr['trial']; rec=dict(trial=t,message_a_hex=None,message_b_hex=None)
        if t<NWORK:
            cv,_=cv_from_seed(req['experiment_id']+'|'+tr['seed'])
            r=run_claw(cv,LU,ls=ls,count=False,ref=False,collect_all=True)
            cum=[0]*22; npass=0
            for (a0,a1,u) in r['allclaws']:
                wx=variantW_P1(cv,a0,a1,SAx,SExF); wy=variantW_P1(cv,a0,a1,SAy,SEyF)
                if not r16ok(trace(cv,wx)[1][16]): continue
                npass+=1; tx=trace(cv,wx); ty=trace(cv,wy)
                for i in range(16,22):
                    if rowok(tx,ty,i): cum[i]+=1
                    else: break
            rec['observations']=dict(claws=r['claws'],row16_passes=npass,rows_le17=cum[17],rows_le18=cum[18],
                rows_le19=cum[19],rows_le20=cum[20],rows_le21=cum[21],
                c1=r['passes'][0],c1c2=r['passes'][1],c1c2g=r['passes'][2],all4=r['passes'][3],q3_model_log2=-95.8491)
        out.append(rec)
    return dict(schema_version=1,trials=out)
def run_request(req):
    return online_experiment(req) if 'online' in req['experiment_id'] else q3_experiment(req)

# ----------------------------------------------------------------- (5) ledger, selftest, main
def ledger(show=True,q3_log2='-95.8491',h3_log2='-8.5',eps_log2=16,succ='0.39',A_C=2**78,A_S=2**74,DEV=2**70):
    C=2728; p7=Fraction(287309824,2**32); g=8*24576*p7; assert g==13152
    NFB=2689372601475987602319909
    Npass=NFB*g*160/Fraction(2**32)
    nL=53096854; nF7=287309824; win=2**26; cntR9=57726359870197
    q_pf=Fraction(cntR9,1)*Fraction(nF7,1)/(Fraction(win,1)*Fraction(2,1)**64)
    occ=1.0-(1.0-2.0**-LS)**(2**LS); claws_per_u=160.0*occ*2**LS/2**32
    scan_per_u=13+20*(19+(5.0/2**TB)*2*(6+occ*7))
    hit_per_claw=12.16; pf_per_claw=9.98; U=2**28
    # packed 4-byte slots on the 256-bit word RAM: a load is index shift, lane and+shift, address add, load, shift, and = 7 (+5 over 2);
    # a store is read-modify-write: index 3, address 1, load 1, mask shift/not/and 3, entry shift/or 2, store 1 = 11 (+9 over 2)
    loads_per_u=20*2*(1+5.0/2**TB); scan_per_u+=PK_LD*loads_per_u
    build_per_claw=(2**LS*(145.0/4+PK_ST))/(U*claws_per_u)
    ops_per_claw=scan_per_u/claws_per_u+hit_per_claw+pf_per_claw+build_per_claw
    step3b=2825; passes_per_cv=U*claws_per_u*float(q_pf); NCV=float(Npass)/passes_per_cv
    ALLOW=(A_C+A_S+DEV)*C; OVER=72644196; PRE=0; FIN=6*C+1600
    online=float(Npass)*ops_per_claw/float(q_pf)+float(Npass)*step3b+NCV*(C+35)
    VMAX=math.ceil((1+2.0**-eps_log2)*online)  # the hard work cap; N charges the cap, not the mean
    N=ALLOW+VMAX+OVER+PRE+FIN; tlog=math.log2(N/C)
    rows=[('allowance A_C (characteristic search)',float(A_C*C)),('allowance A_S (Step-1 solve)',float(A_S*C)),
          ('allowance DEV (development)',float(DEV*C)),('online work cap V_MAX (charged in full)',VMAX),
          ('overshoot past the work cap',OVER),('final verification',FIN)]
    if show:
        print('ops/claw = %.3f  q_pf = 2^%.4f  Npass = %.5e  NCV = %.4e'%(ops_per_claw,math.log2(float(q_pf)),float(Npass),NCV))
        for k,v in rows: print('  %-52s %28.0f'%(k,v))
        print('V_MAX = %d'%VMAX); print('N = %d'%N); print('time_log2 = log2(N/C) = %.5f'%tlog); print('score (memory 2^28.094) = %.5f'%(tlog+8.094))
    return tlog,N,float(q_pf),ops_per_claw
def selftest():
    print('selftest p1claw38'); ok=True
    # 1. S-pair claw constants match the package
    assert (SPC['F7d'],SPC['T8'],SPC['D8'],SPC['D7'],SPC['D9s'])==(0x03bff800,0xfe808000,0xfbc00800,0x20000000,0x043ff800)
    print(' S-pair claw constants OK', {k:hex(v) for k,v in SPC.items()})
    # 2. the 160-word set has 160 members and r16ok agrees
    assert len(T160)==160 and all(r16ok(w) for w in T160); print(' |S160| =',len(T160),'r16ok OK')
    # 3. a claw run on a random cv: claws equal the independent reference, occ ~ 0.632, every good pair lands in S160
    cv,_=cv_from_seed('selftest|0'); r=run_claw(cv,14,ls=18,count=True,ref=True)
    print(' claws=%d ref=%d EQUAL=%s occ=%.4f c1=%d c1c2=%d c1c2g=%d all4=%d ops=%d'%(
        r['claws'],r['refclaws'],r['claws']==r['refclaws'],r['occ_frac'],r['passes'][0],r['passes'][1],r['passes'][2],r['passes'][3],r['ops']))
    ok&= r['claws']==r['refclaws'] and abs(r['occ_frac']-0.632)<0.01
    r2=run_claw(cv,14,ls=18,count=False,ref=False,collect_all=True); bad=0
    for (a0,a1,u) in r2['allclaws']:
        if not r16ok(e16_real_p1(cv,a0,a1)): bad+=1
    print(' every claw is a true row-16 pass (E16 of the P1 pair in S160): %d claws, %d bad'%(len(r2['allclaws']),bad)); ok&= bad==0
    # 4. the ledger reproduces the claimed time_log2
    tlog,N,q,opc=ledger(show=False)
    print(' ledger time_log2 = %.5f (claim 83.72702), score %.5f'%(tlog,tlog+8.094)); ok&= abs(tlog-83.72702)<5e-4
    print('SELFTEST', 'PASS' if ok else 'FAIL'); return ok
def main():
    if len(sys.argv)>1 and sys.argv[1]=='selftest': sys.exit(0 if selftest() else 1)
    if len(sys.argv)>1 and sys.argv[1]=='ledger': ledger(); return
    sys.stdout.write(json.dumps(run_request(json.load(sys.stdin))))
if __name__=='__main__': main()
