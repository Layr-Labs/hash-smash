#!/usr/bin/env python3
# p1claw38.py - sha256-r38: the A0-variant two-block procedure of ePrint 2026/1120 with P8 of 1a695f0b
# (credited data) and the "P1" sum-claw; own code, sibling never executed, stdlib only.
# Sections: (1) SHA-256 r38; (2) P8 and the S pair; (3) the counted claw machine and ledger; (3b) A.14 packed
# slots; (3c) the A.15 seven-lane table; (4) the organizer experiments; (5) selftest and main.
import sys, json, hashlib, struct, math, random
from decimal import Decimal as D, getcontext

# --- (1) reference
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

# --- (2) P8 characteristic and the S pair (1a695f0b)
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

# --- (3) the counted claw machine and ledger
# Pricing (collision-frontier-v5, Section 4): load, store, add, sub, and, or, xor, not, shift, imm, random = 1;
# branch = 2; S0/S1/s0/s1 = 8; CH = 3; MAJ = 4; a table access = address 1 + load/store 1.  Cc2 is F's step-0/1
# constant; R = 9 is the best a0 window (exhaustive qpf scan).
Cc2=0x7af32e15; RWIN=9; PK_LD=5; PK_ST=9
# Table design (Section 4): a slot is indexed by F(a0) >> (32-ls); the loader inserts the whole R = 9 window,
# 2^AW candidates, so occupancy is 1 - e^-(2^(AW-ls)): four per slot at (ls, AW) = (24, 26).  The entry holds
# low 32-ls bits of F and the low ls bits of the a0 offset; the rest of the offset lives in `side`, indexed by
# the same slot (two bits per slot at full scale).
LSf=25; AW=26; SIDE_OPS=4
QPF=(57726359870197/2**58)*(287309824/2**32)   # q_pf = 2^-16.1877, H1-P1 (Section 6)
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
    A2,A3,A4,A5=SAx[2],SAx[3],SAx[4],SAx[5]; E6,E7,E8,E9=SE[6],SE[7],SE[8],SE[9]      # rows 2..5 and 6..9 of S (member x)
    cE5=(A5-S0(A4)-MAJ(A4,A3,A2))&M
    KW9=(E9-A5-S1(E8)-CH(E8,E7,E6)-K[9])&M; cW9=(KW9-cE5)&M
    cE4=(A4-S0(A3))&M; mA=A3&A2; mB=A3|A2
    KW8=(E8-A4-S1(E7)-K[8])&M; cA=E7&E6; cB=~E7&M
    KK7c=(E7-2*A3-cv[0]+S0(A2)-S1(E6)-K[7])&M     # the CH(E6,E5,E4) term is folded with a1,a0 at filter time
    D7c=(_ty[1][7]-_tx[1][7])&M                   # W7y - W7x = E7y - E7x
    return dict(cE5=cE5,cW9=cW9,cE4=cE4,mA=mA,mB=mB,KW8=KW8,cA=cA,cB=cB,A2=A2,E6=E6,KK7c=KK7c,D7c=D7c)
SENT=M                                               # empty-slot marker; an entry equal to it is treated as empty (proof.md 3)
def cv_begin(m,cv):
    if m: m.op(30+38+1+1+2+3)
    co=cv_consts(cv); pf=pf_consts(cv)
    st=(0x9E3779B97F4A7C15^((cv[0]<<32)|cv[1]))&0xFFFFFFFFFFFFFFFF  # experiments: the random word u0, derived from the chaining value
    st^=(st<<13)&0xFFFFFFFFFFFFFFFF; st^=st>>7; st^=(st<<17)&0xFFFFFFFFFFFFFFFF
    return co,pf,(st>>16)&M
def postfilters(m,cv,a0,u,F,pf):
        # counted chain on (a0, u, F) -> flags (c1,c2,g,f7); each segment ends with its counter add (1).
    a1=((u-F)+cv_consts(cv)['K2']+a0)&M; m.op(3)
    E5=(a1+pf['cE5'])&M; m.op(1)
    s1f=s2=s3=s4=0
    m.br(); m.op(1)                                                  # segment 6 + V += 7
    if (E5&0xE0000000)==0xA0000000:
        s1f=1
        w9=(pf['cW9']-a1)&M; m.op(1); w9y=(w9+SPC['D9'])&M; m.op(1)
        d9=(s0(w9y)-s0(w9))&M; m.op(16+1)
        m.br(); m.op(1)                                              # segment 21 + V += 22
        if d9==SPC['D9s']:
            s2=1
            maj1=(pf['mA']|(a1&pf['mB']))&M; m.op(2)
            E4=((a0+pf['cE4'])-maj1)&M; m.op(2)
            chx=(pf['cA']^(pf['cB']&E5))&M; m.op(2)
            w8=((pf['KW8']-E4)-chx)&M; m.op(2); w8y=(w8+SPC['D8'])&M; m.op(1)
            d8=(s0(w8y)-s0(w8))&M; m.op(16+1)
            m.br(); m.op(1)                                          # segment 28 + V += 29
            if d8==SPC['T8']:
                s3=1
                maj2=MAJ(pf['A2'],a1,a0); m.op(4)
                ch2=CH(pf['E6'],E5,E4); m.op(3)
                w7=((pf['KK7c']+maj2)-ch2)&M; m.op(2); w7y=(w7+pf['D7c'])&M; m.op(1)
                d7=(s0(w7y)-s0(w7))&M; m.op(16+1)
                m.br(); m.op(1)                                      # segment 29 + V += 30
                if d7==SPC['F7d']: s4=1
    return s1f,s2,s3,s4

def rowtest(m,tx,ty,i):
    (Ax,Ex,Wx),(Ay,Ey,Wy)=tx,ty
    for k,(x,y) in enumerate(((Ax[i],Ay[i]),(Ex[i],Ey[i]),(Wx[i],Wy[i]))):
        if k==2 and i in (7,8): continue
        msk,v,df=CELLS[k][i]
        if msk:
            m.op(3)
            if (x&msk)!=v: return False
        m.op(3)
        if (x^y)!=df: return False
    if PQE[i]:
        m.op(4)
        if (Ex[i]^Ex[i-1])&PQE[i]: return False
    for (k1,i1,b1,eq,k2,i2,b2,row) in X2:
        if row==i:
            m.op(6)
            if (((tx[k1][i1]>>b1)^(tx[k2][i2]>>b2))&1)!=(0 if eq else 1): return False
    return True
def step3b(m,cv,a0,a1):
    m.op(2*(6*15+10*16))
    wx=variantW_P1(cv,a0,a1,SAx,SExF); wy=variantW_P1(cv,a0,a1,SAy,SEyF)
    tx=trace(cv,wx); ty=trace(cv,wy); ok=True
    for i in range(16,22):
        m.op(100)
        if not rowtest(m,tx,ty,i): ok=False; break
    if ok:
        m.op(100*16+17); ok=exact(tx,ty)
    m.op(1)
    return ok,wx,wy

def run_claw(cv,LU,ls=18,aw=None,count=True,ref=False,collect_all=False):
    if aw is None: aw=ls
    TB=32-ls; RTOP=(RWIN<<aw)&M; AB=32-TB; SB=max(0,aw-AB)
    m=Mach() if count else None
    co,pf,u0=cv_begin(m,cv)
    tm=(1<<TB)-1; pmask=tm&~5; smask=(1<<ls)-1
    tab=[SENT]*(1<<ls); side=([0]*(1<<ls)) if SB else None
    if m: m.op(RESET1*((1<<ls)>>3))                   # reset to SENT, per 256-bit word (8 slots): store 1, address add 1, loop 3 = 5
    if SB and m: m.op(3*((1<<ls)>>5))                 # side reset, per 256-bit word (32 slots): store 1, address add 1, loop 3
    for i in range(1<<aw):
        a0=(RTOP|i)&M; Fv=Ffun(cv,a0,co); slot=Fv>>TB; tab[slot]=((i&((1<<AB)-1))<<TB)|(Fv&tm)
        if SB: side[slot]=i>>AB
        # counted build 34 + packed store 2+9; the side store is 6 (read-modify-write of a byte in a 256-bit
        # word: address 1, load 1, shift 1, and 1, or 1, store 1) -- lane_cost/F-SIDE-STORE-OMITTED requires it
        if m: m.op(34); m.st(); m.op(PK_ST+(6 if SB else 0))
    ops_build=m.ops if m else 0
    occ=sum(1 for e in tab if e!=SENT)
    claws=0; passes=[0,0,0,0]; goodpairs=[]; refclaws=0; allclaws=[]; collisions=[]
    if ref:
        Fs=sorted(((s<<TB)|(tab[s]&tm)) for s in range(1<<ls) if tab[s]!=SENT)
        import bisect
    def claw(a0,u,F):
        nonlocal claws
        claws+=1; a1=(u-hfun(cv,a0))&M
        s1f,s2,s3,s4=postfilters(m or Mach(),cv,a0,u,F,pf)
        for j,s in enumerate((s1f,s2,s3,s4)): passes[j]+=s
        if collect_all: allclaws.append((a0,a1,u,(s1f,s2,s3,s4)))
        if s4:
            goodpairs.append((a0,a1,u))
            ok,wx,wy=step3b(m or Mach(),cv,a0,a1)
            if ok: collisions.append((a0,a1,u,wx,wy))
    for n in range(1<<LU):
        u=(u0+n)&M; P=(s0(u)-u)&M
        if m: m.op(13)                                   # u0 + n 1, s0 8, sub 1, loop 3
        for h in R16H:
            W=(h-P)&M
            strad=(W&tm)>=tm-4
            if m: m.op(5)                                # W 1, W+1024 1, lo 1, straddle test 2
            if strad and m: m.op(1)                      # V += 23 (the two straddle lookups of this head; ls >= 22)
            for k,Wsub in enumerate((W,(W+1024)&M)):
                if k==1 and TB>10:                       # ls < 22: the second window has its own straddle test
                    strad=(Wsub&tm)>=tm-4
                    if m: m.op(3)
                idx=Wsub>>TB; e=tab[idx]
                if m: m.op(3); m.ld(); m.op(PK_LD); m.br()   # index 1, packed load 2+5, residue sub+and 2, branch 2
                if ((e-Wsub)&pmask)==0:
                    if m: m.br(); m.op(1)                # e = SENT? compare-and-branch 2, V += 3 or 10
                    if e!=SENT:
                        F=((idx<<TB)|(e&tm))&M; dd=(F-Wsub)&M
                        if m: m.op(5); m.br()            # F 3, dd 2, branch 2
                        if (dd&~5)==0:
                            if m and SB: m.op(SIDE_OPS)  # the side-array read of the a0 offset
                            claw((RTOP|((side[idx]<<AB) if SB else 0)|(e>>TB))&M,u,F)
                if strad:
                    idx2=(idx+1)&smask; e2=tab[idx2]
                    if m: m.op(2); m.ld(); m.op(PK_LD); m.br()  # idx+1, and 2, packed load 2+5, e2 = SENT? branch 2
                    if e2!=SENT:
                        F2=((idx2<<TB)|(e2&tm))&M; dd=(F2-Wsub)&M
                        if m: m.op(5); m.br(); m.op(1)   # F2 3, dd 2, branch 2, V += 8
                        if (dd&~5)==0:
                            if m and SB: m.op(SIDE_OPS)  # the side-array read of the a0 offset
                            claw((RTOP|((side[idx2]<<AB) if SB else 0)|(e2>>TB))&M,u,F2)
        if ref:
            for h in R16H:
                for o in OFFS:
                    want=((h+o)-P)&M; k=bisect.bisect_left(Fs,want)
                    if k<len(Fs) and Fs[k]==want: refclaws+=1
    return dict(occ=occ,occ_frac=occ/(1<<ls),claws=claws,refclaws=refclaws,passes=passes,goodpairs=goodpairs,allclaws=allclaws,
                collisions=collisions,ops=(m.ops if count else 0),ops_build=ops_build,u0=u0)

# --- (3c) the bucket table
# One 256-bit word per bucket, L = 256//(1+b+AW) lanes of [1 guard][b tag][AW offset]; a query reads bucket
# Wsub >> b and compares b-bit tags; a passing lane is the claw of its a0 at F = (bucket << b)|tag.  The
# loader inserts the R = 9 window in cyclic order, keeping the first L lanes per bucket.
BB=10; BBL=6; MATCH_OPS=18; HEAD_OPS=17; BCAST_OPS=7  # HEAD_OPS = A.15.2's test (counted_head)
WRAP_RATE=0.0133      # A.15.2's one indeterminacy: 1.33% of fires are wrap class t<w
def bucket_lanes(b=BB,aw=None):
    return 256//(1+b+(AW if aw is None else aw))
def bucket_filled(S_P,b,lanes):
    from math import comb
    s=cum=0.0; p=1.0/2**(32-b)
    for k in range(lanes):
        pk=comb(S_P,k)*p**k*((1-p)**(S_P-k)); s+=k*pk; cum+=pk
    return s+lanes*(1-cum)
def fill_sums(S_P,b,lanes):
    # A.15.7: sum_j P(lane j filled) and sum_j P(lane j filled)^2.  A bucket's X ~ Binomial(S_P, 2^-(32-b))
    # candidates fill its first min(X, lanes) lanes, so lane j is filled iff X >= j + 1.
    from math import comb
    p=1.0/2**(32-b); s1=s2=0.0
    for j in range(lanes):
        f=1.0-sum(comb(S_P,k)*p**k*((1-p)**(S_P-k)) for k in range(j+1))
        s1+=f; s2+=f*f
    return s1,s2
EMPTY_N=1<<15              # A.15.10: CONDITIONAL samples; chain only on a mask fire
EMPTY_CHAIN=10.30          # charged conditional mean chain cost: 10.1501 + 3 s.e.
EMPTY_ALL4=1.66e-04        # conditional 99% upper bound on all-four rate, 0 events
def ub99(k,n,z=2.326347874):
    # one-sided 99% Wilson bound for k events in n trials
    if k>=n: return 1.0
    ph=k/n
    return (ph+z*z/(2*n)+z*math.sqrt(ph*(1-ph)/n+z*z/(4*n*n)))/(1+z*z/n)
def counted_empty_chain(n=EMPTY_N):
    # A.15.10: the CONDITIONAL chain law of an empty-lane mask fire: u uniform, tested with the scan's own
    # predicate w in {0, 2^b-5, 2^b-4, 2^b-1}; only a fire runs the chain, on the resolver's word
    # F = Wsub - w (main, w = 0) or Wsub + 2^b - w (straddle); a0 = 9 << 26.
    tm=(1<<BB)-1; tot=t2=0.0; c1=c12=all4=fires=draws=0
    SJ=[s0(j) for j in range(8)]
    FJ=[[(j,(w+j)&tm) for j in range(8) if (w+j)&tm in (0,tm-4,tm-3,tm)] for w in range(1<<BB)]
    for c in range(16):
        cv,_=cv_from_seed('empty|cond|%d'%c); co,pf,u0=cv_begin(None,cv); a0=(RWIN<<AW)&M
        k=0; d=0
        while k<(n>>4):
            ub=(u0+8*d)&M; d+=1; draws+=8; h=R16H[d%20]
            sb=s0(ub); w0=(h-((sb-ub)&M))&M; w0&=tm
            for j,w in FJ[w0]:
                u=(ub+j)&M; sj=sb^SJ[j]; W=(h-((sj-u)&M))&M
                F=W+(0 if w==0 else (1<<BB)-w)
                m=Mach(); s1,s2,s3,s4=postfilters(m,cv,a0,u,F,pf)
                tot+=m.ops; t2+=m.ops*m.ops; c1+=s1; c12+=s2; all4+=s4; fires+=1; k+=1
                if k>=(n>>4): break
    mean=tot/fires; sd=math.sqrt(max(0.0,t2/fires-mean*mean)); sem=sd/math.sqrt(fires)
    return dict(n=fires,draws=draws,rate=fires/draws,mean_ops=mean,sd=sd,sem=sem,
                charge=max(EMPTY_CHAIN,mean+3*sem),c1=c1/fires,c12=c12/fires,
                all4=all4/fires,k1=c1,k2=c12,k4=all4,ub=ub99(all4,fires))
def bucket_terms(S_P=2**AW,b=BB,match=MATCH_OPS,head=HEAD_OPS,bcast=BCAST_OPS,aw=None,strad=True,wrap=WRAP_RATE):
    lanes=bucket_lanes(b,aw)
    filled=bucket_filled(S_P,b,lanes)
    claws=40*filled*(4/2**b)*(1-2/2**b)   # A.15.7: the union mask emits ONE claw per fired position, so the
                                          # both-window coincidences are not claws (rate 2/2^b of the passes)
    matches=claws                              # bit 35 of a lane is its filled flag and the broadcast carries it set
    # The fused test says a position passed, not which window: the resolution reads word 0 and, if that fails
    # its own check, word 1 (+6).  One window passed, mean extra 3; the max path charges 6.
    strd=((5/2**b)*40*9) if strad else 0.0     # the straddle pass (tag - tg wraps): 5/2^b of the 40 window lookups, 9 each
    fixed=13+2+bcast
    pf=7+22/8+29*(53096854/2**32)+30*(57726359870197/2**58)
        # A.15.6: an all-zero lane passes at w in {0,2^b-5,2^b-4,2^b-1}; each such fire is resolved.
    # A.15.10: per (head, window) READ, 20 x 2 = 40, as the claw rate and max path (280 = 40 x 7) already
    # charge.  w = 0 is accepted in the main bucket; the three wrap residues are rejected there (18) and
    # accepted in the straddle read (match+3+chain): four resolutions and four chains per empty lane.
    empty=40*((4/2**b)*(lanes-filled)*(match+3+max(pf,EMPTY_CHAIN)+3014*max(QPF,EMPTY_ALL4))
              +(3/2**b)*(lanes-filled)*match)
    per_u=fixed+20*head+strd+matches*(match+3)+claws*(pf+QPF*3014)+wrap*claws*match+empty
    return per_u,claws,filled,lanes
def run_bucket(cv,LU,b=BB,aw=AW,count=True,ref=False,collect_all=False):
    m=Mach() if count else None
    co,pf,u0=cv_begin(m,cv)
    RTOP=(RWIN<<aw)&M; tmask=(1<<b)-1
    tab={}; filled=[]
    rot=(u0^((cv[0]<<1)|cv[1]))&((1<<aw)-1)
    for n in range(1<<aw):
        i=(n+rot)&((1<<aw)-1); a0=(RTOP|i)&M
        Fv=Ffun(cv,a0,co); bk=Fv>>b; tg=Fv&tmask
        lst=tab.get(bk)
        if lst is None: tab[bk]=[(tg,i)]
        elif len(lst)<BBL: lst.append((tg,i))
        if m: m.op(34)                          # a0 1, E0 1, S0 8, MAJ 2, S1 8, CH 2, F 5, tag 1, loop 3, branch 3
        if m: m.ld(); m.op(4); m.st()           # lane read-modify-write: address 1, load 1(+1), or 1, and 1, store 1(+1)
    ops_build=m.ops if count else 0
    occ=sum(len(v) for v in tab.values())
    claws=0; passes=[0,0,0,0]; goodpairs=[]; refclaws=0; collisions=[]; allclaws=[]
    if ref:
        import bisect
        Fs=sorted(((bk<<b)|tg) for bk,lst in tab.items() for tg,off in lst)
    def claw(a0,u,F):
        nonlocal claws
        claws+=1; a1=(u-hfun(cv,a0))&M
        s1f,s2,s3,s4=postfilters(m or Mach(),cv,a0,u,F,pf)
        for j,s in enumerate((s1f,s2,s3,s4)): passes[j]+=s
        if collect_all: allclaws.append((a0,a1,u,(s1f,s2,s3,s4)))
        if s4:
            goodpairs.append((a0,a1,u))
            ok,wx,wy=step3b(m or Mach(),cv,a0,a1)
            if ok: collisions.append((a0,a1,u,wx,wy))
    for n in range(1<<LU):
        u=(u0+n)&M; P=(s0(u)-u)&M
        if m: m.op(13)                          # u0 + n 1, s0 8, sub 1, loop 3
        w=(R16H[0]-P)&tmask
        if m: m.op(2+BCAST_OPS)                 # w 2, the broadcast tag word 2^2 shifts + (2^2-1) ors = 7
        for h in R16H:
            W=(h-P)&M
            if m: m.op(HEAD_OPS)                # A.15.2's counted head (probe_two): 2 x (address, load, add, and, add, and, or) + branch 2 + setup = 17
            for Wsub in (W,(W+1024)&M):
                tg=Wsub&tmask; k0=Wsub>>b
                for kk in (k0,k0+1):            # k0 + 1 is the straddle pass: tag - tg may wrap into the next bucket
                    if kk!=k0 and tg<(1<<b)-5: break
                    if m and kk!=k0: m.op(9)    # the straddle lookup: address 1, load 1, the field test 5, branch 2
                    lst=tab.get(kk)
                    if not lst: continue
                    for tag,off in lst:
                        df=((kk<<b)|tag)-Wsub
                        if df not in (0,1,4,5): continue   # A.15.9: the WORD difference, not the tag difference
                        if m: m.op(MATCH_OPS)   # halving 3x3, extract 2+1+1+2, window check 2, branch 2
                        claw((RTOP|off)&M,u,(kk<<b)|tag)
        if ref:
            for h in R16H:
                for o in OFFS:
                    want=((h+o)-P)&M; k=bisect.bisect_left(Fs,want)
                    if k<len(Fs) and Fs[k]==want: refclaws+=1
    return dict(occ=occ,occ_frac=(occ/(len(tab) or 1))/BBL,claws=claws,refclaws=refclaws,passes=passes,
                goodpairs=goodpairs,collisions=collisions,ops=(m.ops if count else 0),ops_build=ops_build,
                buckets=len(tab),u0=u0,rot=rot,allclaws=allclaws)

SExF=[_tx[1][i] for i in range(16)]; SEyF=[_ty[1][i] for i in range(16)]
def variantW_P1(cv,a0,a1,SA,SEF):
    A={-1:cv[0],-2:cv[1],-3:cv[2],-4:cv[3]}; E={-1:cv[4],-2:cv[5],-3:cv[6],-4:cv[7]}
    A[0]=a0; A[1]=a1
    for i in range(2,16): A[i]=SA[i]
    for i in range(6): E[i]=(A[i]+A[i-4]-S0(A[i-1])-MAJ(A[i-1],A[i-2],A[i-3]))&M
    for i in range(6,16): E[i]=SEF[i]
    return [(E[i]-A[i-4]-E[i-4]-S1(E[i-1])-CH(E[i-1],E[i-2],E[i-3])-K[i])&M for i in range(16)]
def pf_ref(cv,a0,a1):
    wx=variantW_P1(cv,a0,a1,SAx,SExF); wy=variantW_P1(cv,a0,a1,SAy,SEyF)
    c1=((wy[8]-wx[8])&M)==SPC['D8']; c2=((s0(wy[9])-s0(wx[9]))&M)==SPC['D9s']; g=((s0(wy[8])-s0(wx[8]))&M)==SPC['T8']
    f7=((s0(wy[7])-s0(wx[7]))&M)==SPC['F7d'] and ((wy[7]-wx[7])&M)==SPC['D7']
    return (int(c1),int(c1 and c2),int(c1 and c2 and g),int(c1 and c2 and g and f7))
def e16_real_p1(cv,a0,a1):
    W=variantW_P1(cv,a0,a1,SAx,SExF); return trace(cv,W)[1][16]

# --- (3d) the b = 10 / AW = 25 pin design (unfiled): b + AW = 35; straddle pass not in the 19, charged 9.
WID7=36; LANES7=7; HEAD_OPS_SHARED=19; HEAD_OPS_MERGED=17
def lane_geom(b):
    aw=35-b
    return aw,1+b+aw,256//(1+b+aw)
def bcast(x,wid=WID7,lanes=LANES7):
    assert 0<=x<(1<<wid)
    return x*((1<<(wid*lanes))-1)//((1<<wid)-1)
def probe19(w0,w1,W,b,aw,count=True):
    tmask=(1<<b)-1; WIDL=WID7*LANES7*2; LAN=LANES7*2
    HALF=bcast(1<<35,WID7,LAN); Mt=bcast(((tmask&~5)<<aw),WID7,LAN); ONE=bcast(1,WID7,LAN)
    seq=[]; ops=0
    seq+=[('W = h - P',1)]; ops+=1
    seq+=[('bucket index k0 = W >> b',1)]; ops+=1
    seq+=[('the second address k1 = k0 + 1024/2^b (one add on the byte address)',1)]; ops+=1
    seq+=[('the two bucket accesses (address + load each)',4)]; ops+=4
    seq+=[('merge the two 256-bit halves into one 504-bit register',1)]
    dd=w0|(w1<<(WID7*LANES7)); ops+=1
    seq+=[('T = W & (2^b-1), shared by all 20 heads (charged once per u)',0)]; T=W&tmask
    seq+=[('B = the broadcast of T << AW into the 14 lanes (charged once per u)',0)]
    B=T*bcast(1<<aw,WID7,LAN)
    seq+=[('u = (d | HALF) - B: one subtraction for both windows',2)]; u=(dd|HALF)-B; ops+=2
    seq+=[('a = u & Mt: the masked tag difference (bits 0 and 2 free)',1)]; a=u&Mt; ops+=1
    seq+=[('z = (a | HALF) - ONE: the flag clears iff the field was zero',2)]; z=(a|HALF)-ONE; ops+=2
    seq+=[('mm = d & ~z: filled lanes only (not 1, and 1)',2)]; mm=dd&~z; ops+=2
    seq+=[('branch if mm, and its two outcomes',2)]; ops+=2
    assert ops==HEAD_OPS_MERGED and ops<=HEAD_OPS_SHARED, (ops,seq)
    return mm,(ops if count else 0)
def lane_index(mask,wid=WID7):
    out=[]
    while mask:
        low=mask&-mask; out.append((low.bit_length()-1)//wid); mask^=low
    return out
def probe_masks(b=BB,aw=AW,lanes=None):
    lanes=lanes or 256//(1+b+aw); st=1+b+aw
    MLOW=sum(1<<(L*st+aw+p) for L in range(lanes) for p in range(1,b) if p!=2)
    G=sum(1<<(L*st+aw+b) for L in range(lanes))
    return st,MLOW,G,G-sum(1<<(L*st+aw) for L in range(lanes))
def probe_two(d0,d1,w,m=None,b=BB,aw=AW,lanes=None,masks=None):
    lanes=lanes or 256//(1+b+aw); st,MLOW,G,K=masks or probe_masks(b,aw,lanes)
    WB=sum(((1<<b)-w)<<(L*st+aw) for L in range(lanes))
    Z=None
    for j,d in enumerate((d0,d1)):
        if m: m.op(2)                           # address 1 + 256-bit load 1
        r=d+WB
        if m: m.op(1)                           # add 1: the bias, every lane
        a=r&MLOW
        if m: m.op(1)                           # and 1: the forced tag bits
        if j: Z&=(a+K)&G
        else: Z=(a+K)&G
        if m: m.op(2)                           # add 1 (K: the field carry) + and 1 (G)  [NOT eliminated, not priced]
        if m: m.op(1)                           # and 1: the fail-planes of the two windows merge (De Morgan)
    if m: m.op(3)                               # compare-and-branch 2 + setup 1 (k_i = k_base + c_i)
    return Z
def counted_head(exhaustive=True,b=BB,aw=AW):
    import random
    lanes=256//(1+b+aw); st,MLOW,G,K=probe_masks(b,aw,lanes); tmask=(1<<b)-1
    def word(tags):
        v=0
        for L,t in enumerate(tags): v|=((t&tmask)<<(L*st+aw))|((L*7+3)&((1<<aw)-1))
        return v
    def fire(Z,L): return 1-((Z>>(L*st+aw+b))&1)      # guard bit 0 = the field carried out = the lane passed
    def ref(t,w): return (t-w) in (0,1,4,5)
    def wrap(t,w): return t<w and ((t-w)%(1<<b)) in (0,1,4,5)
    rnd=random.Random(38); bad=wr=fires=n=one=both=0
    ws=range(1<<b) if exhaustive else [rnd.randrange(1<<b) for _ in range(44)]+[508,509,510,511]
    for w in ws:
        for t0 in range(1<<b):
            ts=range(1<<b) if w==0 else [((t0*197+w*97+13)&tmask)]    # w = 0: the full (tag, tag) truth table
            for t1 in ts:
                Z=probe_two(word([t0]*lanes),word([t1]*lanes),w,lanes=lanes,masks=(st,MLOW,G,K))
                n+=lanes
                for L in range(lanes):
                    got=fire(Z,L); p0=ref(t0,w); p1=ref(t1,w)
                    wr+=int(wrap(t0,w) or wrap(t1,w)); fires+=got
                    one+=int(p0!=p1); both+=int(p0 and p1)
                    if got!=(1 if (p0 or p1) else 0) and not (got and (wrap(t0,w) or wrap(t1,w))): bad+=1
    m=Mach(); probe_two(word([0]*lanes),word([0]*lanes),0,m,lanes=lanes,masks=(st,MLOW,G,K))
    return dict(compared=n,bad=bad,wraps=wr,fires=fires,ops=m.ops,lanes=lanes,stride=st,onewin=one,both=both)
def counted_empty(b=BB,aw=AW,empty=2):
    lanes=256//(1+b+aw); st,MLOW,G,K=probe_masks(b,aw,lanes); tmask=(1<<b)-1
    def word(tags):
        v=0
        for L,t in enumerate(tags):
            if t is not None: v|=((t&tmask)<<(L*st+aw))|((L*7+3)&((1<<aw)-1))
        return v
    emp=list(range(empty)); w0=word([None if L in emp else 0x1ff-(L%3) for L in range(lanes)]); hits=[]; bad=0
    for w in range(1<<b):
        Z=probe_two(w0,w0,w,lanes=lanes,masks=(st,MLOW,G,K))
        for L in emp:
            if not (Z>>(L*st+aw+b))&1:
                hits.append(w); bad+=int(((0-w)%(1<<b)) not in (0,1,4,5))
    want=sorted({0,(1<<b)-5,(1<<b)-4,(1<<b)-1})
    return dict(watched=sorted(set(hits))==want,residues=sorted(set(hits)),want=want,bad=bad,empty=empty,lanes=lanes)
def run_bucket_packed(cv,LU,b=10,aw=None,count=True,ref=True,collect_all=False):
    aw0,wid,lanes=lane_geom(b)
    if aw is None: aw=aw0
    if aw>aw0: raise SystemExit('run_bucket_packed: AW must not exceed 35 - b (%d)'%aw0)
    m=Mach() if count else None
    co,pf,u0=cv_begin(m,cv)
    RTOP=(RWIN<<aw0)&M; tmask=(1<<b)-1; NB=1<<(32-b); DELTA=1024>>b; OFFM=(1<<aw)-1
    tab={}; cnt={}; kept=[]
    rot=(u0^((cv[0]<<1)|cv[1]))&((1<<aw)-1)
    for n in range(1<<aw):
        i=(n+rot)&((1<<aw)-1); a0=(RTOP|i)&M
        Fv=Ffun(cv,a0,co); bk=Fv>>b; tg=Fv&tmask
        c=cnt.get(bk,0)
        if c<lanes:
            tab[bk]=tab.get(bk,0)|((1<<35|(tg<<aw)|i)<<(wid*c)); cnt[bk]=c+1; kept.append((bk<<b)|tg)
        if m: m.op(34)                          # a0 1, E0 1, S0 8, MAJ 2, S1 8, CH 2, F 5, tag 1, loop 3, branch 3
        if m: m.ld(); m.op(4); m.st()           # lane read-modify-write: address 1, load 1(+1), or 1, and 1, store 1(+1)
    ops_build=m.ops if count else 0
    claws=0; passes=[0,0,0,0]; goodpairs=[]; refclaws=0; collisions=[]; allclaws=[]; strad=0
    if ref:
        import bisect
        Fs=sorted(kept)
    def claw(a0,u,F):
        nonlocal claws
        claws+=1; a1=(u-hfun(cv,a0))&M
        s1f,s2,s3,s4=postfilters(m or Mach(),cv,a0,u,F,pf)
        for j,s in enumerate((s1f,s2,s3,s4)): passes[j]+=s
        if collect_all: allclaws.append((a0,a1,u,(s1f,s2,s3,s4)))
        if s4:
            goodpairs.append((a0,a1,u))
            ok,wx,wy=step3b(m or Mach(),cv,a0,a1)
            if ok: collisions.append((a0,a1,u,wx,wy))
    for n in range(1<<LU):
        u=(u0+n)&M; P=(s0(u)-u)&M
        if m: m.op(13)                          # u0 + n 1, s0 8, sub 1, loop 3
        for h in R16H:
            W=(h-P)&M; k0=W>>b; k1=(k0+DELTA)&(NB-1)
            w0=tab.get(k0,0); w1=tab.get(k1,0)
            mm,o=probe19(w0,w1,W,b,aw,count)
            if m and count: m.op(HEAD_OPS_MERGED)    # the itemised 17 of A.15.2 (the review's 19 is charged nowhere)
            if mm:
                for li in lane_index(mm):
                    if li<LANES7: kk,w,j,Wsub=k0,w0,li,W
                    else: kk,w,j,Wsub=k1,w1,li-LANES7,(W+1024)&M
                    lane=(w>>(wid*j))&((1<<wid)-1); off=lane&OFFM
                    tag=(lane>>aw)&tmask; F=((kk<<b)|tag)&M
                    if m: m.op(MATCH_OPS)       # extract 4, the F reconstruct 3, the window check 2, branch 2 (as filed)
                    if ((F-Wsub)&M) not in (0,1,4,5): continue   # the window check: drops a wrapped tag (5/2^b of heads)
                    claw((RTOP|off)&M,u,F)
            T=W&tmask
            if T>=(1<<b)-5:
                strad+=1
                for kk,w in ((k0+1,tab.get((k0+1)&(NB-1),0)),(k1+1,tab.get((k1+1)&(NB-1),0))):
                    if m: m.op(9)               # the straddle lookup: address 1, load 1, the field test 5, branch 2
                    for li in lane_index(w&bcast(1<<35)):
                        lane=(w>>(wid*li))&((1<<wid)-1); off=lane&OFFM
                        tag=(lane>>aw)&tmask
                        if ((tag+(1<<b)-T)&(tmask&~5)): continue
                        if m: m.op(MATCH_OPS)
                        if ((((kk<<b)|tag)-W)&M) not in (0,1,4,5): continue
                        claw((RTOP|off)&M,u,((kk<<b)|tag)&M)
        if ref:
            for h in R16H:
                for o2 in OFFS:
                    want=((h+o2)-P)&M; k=bisect.bisect_left(Fs,want)
                    if k<len(Fs) and Fs[k]==want: refclaws+=1
    return dict(b=b,aw=aw,lanes=lanes,buckets=len(tab),occ=len(kept),claws=claws,refclaws=refclaws,passes=passes,
                goodpairs=goodpairs,collisions=collisions,ops=(m.ops if count else 0),ops_build=ops_build,
                strad=strad,u0=u0,rot=rot,allclaws=allclaws)
def counted_fused(ntrials=None,b=BB,aw=AW):
    import random
    ntrials=ntrials or 40000*2**(b-9)
    rr=random.Random(7); lanes=bucket_lanes(b,aw); st=1+b+aw; tmask=(1<<b)-1; W=(1<<b)//2; p=4.0/2**b
    f7=pas=coin=bad=0
    def word(qs):
        v=0
        for j,q in enumerate(qs):
            t=(W+(rr.choice((0,1,4,5)) if q else rr.choice((2,3,6,7))))&tmask
            v|=((1<<(b+aw))|(t<<aw)|rr.getrandbits(aw))<<(j*st)
        return v
    for _ in range(ntrials):
        p0=[rr.random()<p for _ in range(lanes)]; p1=[rr.random()<p for _ in range(lanes)]
        z7=probe_two(word(p0),word(p1),W,b=b,aw=aw,lanes=lanes)
        u=[int(not (z7>>(j*st+aw+b))&1) for j in range(lanes)]
        np0=sum(p0); np1=sum(p1); c=sum(1 for j in range(lanes) if p0[j] and p1[j])
        em=sum(1 for j in range(lanes) if p0[j] or p1[j])
        f7+=sum(u); pas+=np0+np1; coin+=c
        bad+=int(sum(u)!=em or np0+np1!=em+c or any(u[j]!=int(p0[j] or p1[j]) for j in range(lanes)))
    return dict(trials=ntrials,b=b,union_fires=f7,window_passes=pas,coincidences=coin,emitted=f7,bad=bad,
                rate=float(coin)/pas if pas else 0.0)
def fused_table(cv,LU=10,b=BB,aw=25,keep=BBL):
    co,pf,u0=cv_begin(None,cv)
    RTOP=(RWIN<<aw)&M; tmask=(1<<b)-1; st=1+b+aw; nl=bucket_lanes(b,aw); OFFM=(1<<aw)-1
    rot=(u0^((cv[0]<<1)|cv[1]))&OFFM
    pos=[]; skip=0
    for n in range(1<<LU):
        u=(u0+n)&M; P=(s0(u)-u)&M
        for h in R16H:
            W=(h-P)&M
            if (W&tmask)>(1<<b)-6: skip+=1; continue
            pos.append((u,W))
    need=set(k for _,W in pos for k in (W>>b,((W+1024)&M)>>b))
    tab={}
    for n in range(1<<aw):
        i=(n+rot)&OFFM; Fv=Ffun(cv,(RTOP|i)&M,co); bk=Fv>>b
        if bk in need:
            lst=tab.get(bk,())
            if len(lst)<keep: tab[bk]=lst+(((1<<(aw+b))|((Fv&tmask)<<aw)|i),)
    def word(bk):
        w=0
        for j,v in enumerate(tab.get(bk,())): w|=v<<(st*j)
        return w
    def pas(w,j,T):
        return bool(w&(1<<(st*j+aw+b))) and ((((w>>(st*j+aw))&tmask)-T)&tmask) in (0,1,4,5)
    em=ref=coin=bad=mis=emp=p1c=p2c=0
    for (u,W) in pos:
        T=W&tmask; w1=word(W>>b); w2=word(((W+1024)&M)>>b)
        Z=probe_two(w1,w2,T,b=b,aw=aw)
        for j in range(nl):
            f1=pas(w1,j,T); f2=pas(w2,j,T); mk=1-((Z>>(st*j+aw+b))&1)
            if mk and not (f1 or f2): emp+=1; continue      # an empty lane reading tag 0: A.15.6's empty-lane charge
            if mk!=(f1 or f2): mis+=1
            ref+=f1+f2; p1c+=f1; p2c+=f2; coin+=1 if (f1 and f2) else 0
            if mk:
                w=w1 if f1 else w2
                a0=(RTOP|((w>>(st*j))&OFFM))&M; a1=(u-hfun(cv,a0))&M
                em+=1; bad+=0 if r16ok(e16_real_p1(cv,a0,a1)) else 1
    s1,s2=fill_sums(1<<aw,b,nl); pred=(s2/s1)*(2.0/2**b)   # A.15.7: exact share of passes that coincide
    return dict(b=b,aw=aw,u=1<<LU,positions=len(pos),skipped=skip,emitted=em,ref=ref,coincidences=coin,
                empty_fires=emp,mask_bad=mis,row16_bad=bad,load=(1<<aw)/2**(32-b),p1=p1c,p2=p2c,
                rate=float(coin)/em if em else 0.0,pred=pred,charged=2.0/2**b,fill1=s1,fill2=s2)
# --- (4) organizer experiments
# organizer budget: 256 trials in 20 s (runner.py); trials 0..NWORK-1 work, trial NWORK runs step 3b on the
# P8 pair itself, the rest return no pair.
NWORK=8; ONLINE_LS=16; ONLINE_AW=17; ONLINE_LU=12; Q3_LS=16; Q3_AW=17; Q3_LU=13
NBWORK=4; NB_AW=16; NB_LU=13
class Shake:
    def __init__(self,label): self.buf=b''; self.n=0; self.lab=label.encode()
    def word(self):
        if not self.buf: self.buf=hashlib.shake_256(self.lab+struct.pack('<I',self.n)).digest(256); self.n+=1
        w=struct.unpack('<I',self.buf[:4])[0]; self.buf=self.buf[4:]; return w
def cv_from_seed(seed):
    sh=Shake(seed); M0=[sh.word() for _ in range(16)]; return compress(IV,M0),M0
def spair_obs():
    m=Mach(); ok,wx,wy=step3b(m,PCV,SAx[0],SAx[1])
    return dict(step3b_P8_pair_ok=int(ok and wx==PMX and wy==PMY),step3b_P8_pair_ops=m.ops)
def online_experiment(req):
    out=[]; LU=req.get('lu',ONLINE_LU)
    for tr in req['trials']:
        t=tr['trial']; rec=dict(trial=t,message_a_hex=None,message_b_hex=None)
        if t<NWORK:
            ls=req.get('ls',ONLINE_LS); aw=req.get('aw',ONLINE_AW)
            cv,M0=cv_from_seed(req['experiment_id']+'|'+tr['seed'])
            r=run_claw(cv,LU,ls=ls,aw=aw,count=True,ref=True,collect_all=True)
                        # a claw is a row-16 pass by construction: verify its real E16 lands in the 160-word set
            bad=0; verified=0; pfmis=0
            exp_claws=160.0*r['occ']*(1<<LU)/2**32
            for (a0,a1,u,fl) in r['allclaws']:
                if r16ok(e16_real_p1(cv,a0,a1)): verified+=1
                else: bad+=1
                pfmis+=int(pf_ref(cv,a0,a1)!=fl)
            rec['observations']=dict(occ_frac=round(r['occ_frac'],6),claws=r['claws'],ref_claws=r['refclaws'],
                claws_equal_ref=int(r['claws']==r['refclaws']),expected_claws=round(exp_claws,1),
                distinct_pairs=len(set((a0,a1) for (a0,a1,u,fl) in r['allclaws'])),postfilter_ref_mismatch=pfmis,
                c1=r['passes'][0],c1c2=r['passes'][1],c1c2g=r['passes'][2],all4=r['passes'][3],
                good_pairs=len(r['goodpairs']),step3b_collisions=len(r['collisions']),
                claw_e16_bad=bad,claw_e16_in_S160=verified,counted_ops=r['ops'])
            if r['collisions'] and bad==0:      # step 3b found rows 16..21 and A34..A37, E34..E37 equal: a collision (Lemma 1)
                a0,a1,u,wx,wy=r['collisions'][0]
                rec['message_a_hex']=struct.pack('>32I',*(M0+wx)).hex()
                rec['message_b_hex']=struct.pack('>32I',*(M0+wy)).hex()
        elif t==NWORK:
            rec['observations']=spair_obs()
        out.append(rec)
    return dict(schema_version=1,trials=out)
def bucket_experiment(req):
    out=[]
    for tr in req['trials']:
        t=tr['trial']; rec=dict(trial=t,message_a_hex=None,message_b_hex=None)
        if t<NBWORK:
            cv,M0=cv_from_seed(req['experiment_id']+'|'+tr['seed'])
            r=run_bucket(cv,NB_LU,b=BB,aw=NB_AW,count=True,ref=True,collect_all=True)
            bad=sum(1 for (a0,a1,u,fl) in r['allclaws'] if not r16ok(e16_real_p1(cv,a0,a1)))
            rec['observations']=dict(claws=r['claws'],refclaws=r['refclaws'],claws_equal_ref=int(r['claws']==r['refclaws']),
                       distinct_pairs=len(set((a0,a1) for (a0,a1,u,fl) in r['allclaws'])),row16_bad=bad,
                       buckets=r['buckets'],occupied_lanes=int(r['occ']),counted_ops=r['ops'],counted_ops_build=r['ops_build'],
                       expected_claws=round(40.0*r['occ']*(1<<NB_LU)*4/2**32,6))
        elif t==NBWORK:                             # A.15.10: the CONDITIONAL empty-lane fire law
            r=counted_empty_chain()
            rec['observations']=dict(empty_draws=r['draws'],empty_n=r['n'],
                       empty_rate_e7=int(round(1e7*r['rate'])),empty_ops_milli=int(round(1000*r['mean_ops'])),
                       empty_sd_milli=int(round(1000*r['sd'])),empty_charge_milli=int(round(1000*r['charge'])),
                       empty_c1=r['k1'],empty_c12=r['k2'],empty_all4=r['k4'],empty_ub_e7=int(round(1e7*r['ub'])))
        elif t==NBWORK+1:                           # A.15.7: the binding resolver's accounting, organizer-executed
            r=counted_fused()
            rec['observations']=dict(fused_trials=r['trials'],fused_fires=r['union_fires'],
                       fused_passes=r['window_passes'],fused_coincidences=r['coincidences'],
                       fused_mismatches=r['bad'])
        out.append(rec)
    return dict(schema_version=1,trials=out)
def q3_experiment(req):
    out=[]; ls=req.get('ls',Q3_LS); aw=req.get('aw',Q3_AW); LU=req.get('lu',Q3_LU)
    for tr in req['trials']:
        t=tr['trial']; rec=dict(trial=t,message_a_hex=None,message_b_hex=None)
        if t<NWORK:
            cv,_=cv_from_seed(req['experiment_id']+'|'+tr['seed'])
            r=run_claw(cv,LU,ls=ls,aw=aw,count=False,ref=False,collect_all=True)
            cum=[0]*22; npass=0
            for (a0,a1,u,fl) in r['allclaws']:
                wx=variantW_P1(cv,a0,a1,SAx,SExF); wy=variantW_P1(cv,a0,a1,SAy,SEyF)
                if not r16ok(trace(cv,wx)[1][16]): continue
                npass+=1; tx=trace(cv,wx); ty=trace(cv,wy)
                for i in range(16,22):
                    if rowok(tx,ty,i): cum[i]+=1
                    else: break
            rec['observations']=dict(claws=r['claws'],distinct_pairs=len(set((a0,a1) for (a0,a1,u,fl) in r['allclaws'])),
                row16_passes=npass,rows_le16=cum[16],rows_le17=cum[17],rows_le18=cum[18],rows_le19=cum[19],rows_le20=cum[20],
                rows_le21=cum[21],c1=r['passes'][0],c1c2=r['passes'][1],c1c2g=r['passes'][2],all4=r['passes'][3])
        elif t==NWORK:
            rec['observations']=spair_obs()
        out.append(rec)
    return dict(schema_version=1,trials=out)
def run_request(req):
    if 'online' in req['experiment_id']: return online_experiment(req)
    if 'bucket' in req['experiment_id']: return bucket_experiment(req)
    return q3_experiment(req)

# --- (5) ledger, selftest, main
STEP3B=3014                     # step 3b on its longest path (every test passing), counted on the P8 pair by selftest
CVSET=75                        # cv_begin: per chaining value, besides its compression
BUILD1=34+2+PK_ST               # one table candidate: 34 + store 2 + packed 9 = 45
RESET1=5                        # table reset to SENT, per 256-bit word: store 1, address add 1, loop 3 (ruling a75499a6)
def scan_terms(t,occ):
    fix=13+20*(5+(3 if t>10 else 0))+40*(3+2+PK_LD+2)
    if t<=10: strad=20*(D(5)/2**t)*(23+2*8*occ)
    else: strad=20*(D(5)/2**t)*(1+11+8*occ)+20*(D(5)/2**t)*(11+8*occ)
    res=40*(D(4)/2**t)*(3+7*occ)
    return fix,strad+res,160*occ*2**(32-t)/D(2)**32
Q3P1='-96.0791'                 # q3 of P1 good pairs before row 16: registered q3_model -96.0133 + min(0, D_LB) of the registered paired run (proof.md Section 9)
def ledger(show=True,q3_log2=None,eps_log2=16,succ='0.39',A_C=2**78,A_S=2**74,DEV=2**70,ULOG=32,lsf=None,aw=None):
    # Amendment (proof.md A.13): the procedure scans all 2^ULOG words u per chaining value.  Section 7 of
    # this proof already takes E[K] over all 2^32 scan words (K = 2^32 x 1.58030 x q_pf), so U = 2^28 in the
    # ledger under-amortised the per-chaining-value fixed work (the compression, CVSET, the table reset and
    # the 2^26-slot table build).  Nothing else changes: the loader, the entry, q_pf, q3 on R = 9 and the
    # SENT correction stay exactly as in Sections 2-9.
    getcontext().prec=90
    if q3_log2 is None: q3_log2=Q3P1
    LSF=LSf if lsf is None else lsf; AWW=AW if aw is None else aw
    C=2728; t=32-LSF; n0=2**LSF; U=2**ULOG; eps=D(2)**-eps_log2; NC=2**AWW
    L2=D(2).ln(); P2=lambda x: (D(x)*L2).exp()
    occ=1-(1-D(1)/n0)**NC                              # expected occupied fraction of the 2^LSF slots (2^AWW candidates)
    SV=SIDE_OPS if AWW>32-t else 0                     # the side-array read, when the a0 offset does not fit the entry
    # the side store is a read-modify-write of a byte inside a 256-bit word: address 1, load 1, shift 1, and 1,
    # or 1, store 1 = 6.  It carries the primitive store (lane_cost/F-SIDE-STORE-OMITTED).
    B1=BUILD1+(6 if SV else 0)
    p1=D(1)/8; p12=D(53096854)/D(2)**32; p12g=D(57726359870197)/D(2)**58
    q_pf=p12g*D(287309824)/D(2)**32                     # Pr[C1 and C2 and G and F7] per claw (H1-P1)
    pf=7+22*p1+29*p12+30*p12g                           # post-filter segments per claw, work-counter adds included
    fix,var,cpu=scan_terms(t,occ)
    per_u=fix+var+cpu*(pf+q_pf*STEP3B+SV)
    wbar=C+CVSET+(n0>>3)*RESET1+NC*B1+U*per_u       # mean online work of one cv (step 3b at its maximum)
    umax=fix+20*(1+22+2*10+2*8)+80*(7+22+29+30+STEP3B+SV)   # every head straddling, 80 claws at step 3b
    vmax=C+CVSET+(n0>>3)*RESET1+NC*B1+U*umax                           # maximum online work of one chaining value
    q3r=P2(q3_log2)*D(2)**32/160                        # success probability of a good pair (it has passed row 16), H2-P1
    cpu_lo=160*(n0*occ-D(1)/64)/D(2)**32                # claws per u, success side (the one entry equal to SENT may hide)
    lam1=U*cpu_lo*q_pf*q3r*(1-D(2)**D('-8.5'))          # per chaining value: Pr[some success] >= this (Bonferroni, H3-P1)
    target=1-D(succ)-D(2)**-60
    NCV=int((-(target).ln()/lam1))+1
    while 1-(-(NCV-1)*lam1).exp()-D(2)**-60>=D(succ): NCV-=1
    VMAX=int(((1+eps)*NCV*wbar).to_integral_value(rounding='ROUND_CEILING'))
    bern=(eps**2*NCV*wbar)/(2*vmax*(1+eps/3))           # Bernstein exponent: Pr[cap halts] <= exp(-bern)
    succ_lb=1-(-NCV*lam1).exp()-(-bern).exp()-D(2)**-60
    ALLOW=(A_C+A_S+DEV)*C; OVER=int(vmax); FIN=6*C+1600
    N=ALLOW+VMAX+OVER+FIN;   # the procedure's own N_CV first blocks are charged inside wbar (C + CVSET each)
    tlog=float((D(N)/C).ln()/L2)
    opc=(fix+var)/cpu+pf+SV+(NC*B1+(n0>>3)*RESET1)/(U*cpu)
    rows=[('allowance A_C = 2^78 x C',A_C*C),('allowance A_S = 2^74 x C',A_S*C),('allowance DEV = 2^70 x C',DEV*C),
          ('online work cap V_MAX (charged in full; includes the N_CV first blocks)',VMAX),
          ('overshoot OVER (one chaining value at its maximum)',OVER),('final verification FIN = 6 C + 1,600',FIN)]
    if show:
        print('occ = %.6f  claws/u = %.5f  q_pf = 2^%.4f  ops/claw (scan+filters+build) = %.3f  step 3b = %d'%(
            occ,cpu,float(q_pf.ln()/L2),opc,STEP3B))
        print('table 2^%d slots, 2^%d candidates, occ = %.6f, side %d bit(s) per slot'%(LSF,AWW,occ,SV and (AWW-(32-t))))
        print('per u: fixed %d + straddle/residue %.4f + claws %.4f = %.4f'%(fix,var,cpu*(pf+q_pf*STEP3B+SV),per_u))
        print('wbar = %.6e  vmax = %d  passes/cv = %.2f  N_CV = %d'%(wbar,OVER,U*cpu_lo*q_pf,NCV))
        print('Bernstein exponent = %.4e  ->  Pr[cap halts] <= 2^-%.0f'%(bern,float(bern/L2)))
        print('success lower bound = %s'%str(succ_lb)[:24])
        for k,v in rows: print('  %-52s %32d'%(k,v))
        print('N = %d'%N); print('time_log2 = log2(N/C) = %.5f'%tlog); print('score (memory 2^27.069, the measured peak) = %.5f'%(tlog+7.069)); print('scan words per chaining value 2^%d'%ULOG)
    return tlog,N,succ_lb,opc
def ledger_bucket(show=True,q3_log2=None,eps_log2=16,succ='0.39',A_C=2**78,A_S=2**74,DEV=2**70,ULOG=32,
                  b=BB,S_P=2**AW,match=MATCH_OPS,head=HEAD_OPS,bcast=BCAST_OPS,mem=27.0241,aw=None,strad=True,
                  wrap=WRAP_RATE):
    getcontext().prec=90
    if q3_log2 is None: q3_log2=Q3P1
    C=2728; U=2**ULOG; eps=D(2)**-eps_log2
    awv=AW if aw is None else aw
    B=2**(32-b); lanes=bucket_lanes(b,awv)
    L2=D(2).ln(); P2=lambda x: (D(x)*L2).exp()
    p1=D(1)/8; p12=D(53096854)/D(2)**32; p12g=D(57726359870197)/D(2)**58
    q_pf=p12g*D(287309824)/D(2)**32
    per_u,claws_u,filled,lanes=bucket_terms(S_P,b,match,head,bcast,awv,strad,wrap)
    per_u=D(repr(per_u)); claws_u=D(repr(claws_u)); filled=D(repr(filled))
    BUILD2=34+2+4+2                                     # F(a0) 34 + run_bucket's ld() 2 + (or, and, index) 4 + st() 2 = 42
    LANE_BUILD=4                                        # A.15.6: guard/tag, shift, index, placement -- retained lanes only
    build=D(S_P)*BUILD2+LANE_BUILD*filled*B; reset=D(B)*5   # one whole 256-bit word per bucket: 2^21 words reset, not 2^20
    wbar=C+CVSET+reset+build+U*per_u
    # A deterministic maximum, not an expectation (lane_cost/F-CAP-MAX-USES-EXPECTATIONS): heads read buckets
    # b and b+1 fully filled, all 12 lanes match at step 3b's longest path plus a wrap resolution.  This path only.
    lane_max=D(match+6)+D(7+22+29+30+STEP3B)+D(match+6)
    umax=D(13+2+bcast)+20*head+D(20*6)+D(20*2*lanes)*lane_max
    vmax=C+CVSET+reset+build+U*umax
    q3r=P2(q3_log2)*D(2)**32/160
    claws_lo=40*(filled-D(1)/64)*(4/D(2)**b)*(1-2/D(2)**b)   # A.15.7: emitted rate, not the 40-window population
    lam1=U*claws_lo*q_pf*q3r*(1-D(2)**D('-8.5'))
    target=1-D(succ)-D(2)**-60
    NCV=int((-(target).ln()/lam1))+1
    while 1-(-(NCV-1)*lam1).exp()-D(2)**-60>=D(succ): NCV-=1
    VMAX=int(((1+eps)*NCV*wbar).to_integral_value(rounding='ROUND_CEILING'))
    bern=(eps**2*NCV*wbar)/(2*vmax*(1+eps/3))
    succ_lb=1-(-NCV*lam1).exp()-(-bern).exp()-D(2)**-60
    ALLOW=(A_C+A_S+DEV)*C; OVER=int(vmax); FIN=6*C+1600
    N=ALLOW+VMAX+OVER+FIN
    tlog=float((D(N)/C).ln()/L2)
    if show:
        print('bucket table: b = %d, %d lanes of %d bits per 256-bit word, 2^%d buckets, table 2^%d bytes'
              %(b,lanes,1+b+awv,32-b,37-b))
        print('load = 2^%.2f per bucket, E[filled lanes] = %.5f of %d, claws/u = %.5f'
              %(math.log2(S_P)- (32-b),float(filled),lanes,float(claws_u)))
        s1,s2=fill_sums(S_P,b,lanes)
        print('A.15.7 coincidence share: exact per-position (sum f^2 / sum f) x 2/2^b = %.6f, charged %.6f (1 - 2/2^b)'
              %((s2/s1)*(2.0/2**b),2.0/2**b))
        print('per u: fixed %d + 20 heads x %d + straddle %.4f + matches x %d + wrap %.4f + claws x (pf + q_pf step3b) = %.4f'
              %(13+2+bcast,head,float((D(5)/D(2)**b)*40*9),match+3,float(D(repr(wrap))*claws_u*match),float(per_u)))
        print('ops/claw (scan + filters + build) = %.3f'%(float(per_u)/float(claws_u)))
        print('wbar = %.6e   N_CV = %d   V_MAX = %d'%(float(wbar),NCV,VMAX))
        print('vmax (maximum online work of one chaining value, OVER) = %d'%int(vmax))
        print('allowances A_C 2^%d C, A_S 2^%d C, DEV 2^%d C  -> %.3f%% of V_MAX'%(A_C.bit_length()-1,A_S.bit_length()-1,DEV.bit_length()-1,100*float(ALLOW)/VMAX))
        print('time_log2 = %.7f   memory %.4f   score = %.7f'%(tlog,mem,tlog+max(0.0,mem-20)))
    return tlog,N,succ_lb
def selftest():
    print('selftest p1claw38'); ok=True
    # 1. S-pair claw constants match the package
    assert (SPC['F7d'],SPC['T8'],SPC['D8'],SPC['D7'],SPC['D9s'])==(0x03bff800,0xfe808000,0xfbc00800,0x20000000,0x043ff800)
    print(' S-pair claw constants OK', {k:hex(v) for k,v in SPC.items()})
    # 2. the 160-word set has 160 members and r16ok agrees
    assert len(T160)==160 and all(r16ok(w) for w in T160); print(' |S160| =',len(T160),'r16ok OK')
    # 3. step 3b on the P8 pair: every test passes, the outputs are equal, and its count is the ledger's STEP3B
    o=spair_obs(); print(' step 3b on the P8 pair:',o); ok&= o['step3b_P8_pair_ok']==1 and o['step3b_P8_pair_ops']==STEP3B
        # 4. claw run: claws = reference, occ ~ 0.632, every claw in S160
    cv,_=cv_from_seed('selftest|0'); r=run_claw(cv,16,ls=15,aw=16,count=True,ref=True,collect_all=True)
    dist=len(set((a0,a1) for (a0,a1,u,fl) in r['allclaws']))
    print(' claws=%d ref=%d EQUAL=%s distinct=%d occ=%.4f c1=%d c1c2=%d c1c2g=%d all4=%d ops=%d'%(r['claws'],r['refclaws'],
        r['claws']==r['refclaws'],dist,r['occ_frac'],r['passes'][0],r['passes'][1],r['passes'][2],r['passes'][3],r['ops']))
    ok&= r['claws']==r['refclaws'] and dist==r['claws'] and abs(r['occ_frac']-(1-math.exp(-2)))<0.01
    bad=sum(1 for (a0,a1,u,fl) in r['allclaws'] if not r16ok(e16_real_p1(cv,a0,a1)))
    print(' every claw is a true row-16 pass (E16 of the P1 pair in S160): %d claws, %d bad'%(r['claws'],bad)); ok&= bad==0
        # 5. post-filter chain = the chain on the real words (half with C1 forced)
    import random; rr=random.Random(11); mis=0; st=[0,0,0,0]
    for k in range(60000):
        cv2=[rr.getrandbits(32) for _ in range(8)]; a0=rr.getrandbits(32); a1=rr.getrandbits(32); pf2=pf_consts(cv2)
        if k%2: a1=((0xA0000000|rr.getrandbits(29))-pf2['cE5'])&M
        fl=postfilters(Mach(),cv2,a0,(a1+hfun(cv2,a0))&M,Ffun(cv2,a0,cv_consts(cv2)),pf2); rf=pf_ref(cv2,a0,a1)
        mis+=int(tuple(fl)!=rf); st=[x+y for x,y in zip(st,rf)]
    print(' post-filter chain vs the real words: 60000 pairs, stage counts %s, %d mismatches'%(st,mis)); ok&= mis==0
        # 6. counted run <= the ledger's per-u charge at the same size
    getcontext().prec=40
    fix,var,cpu=scan_terms(32-15,D(r['occ_frac']))
    chg=CVSET+2**12*RESET1+3*2**10+2**16*(BUILD1+6)+2**16*(fix+var)+r['claws']*(7+22+29+30)+len(r['goodpairs'])*STEP3B
    print(' counted ops %d (build %d) <= charge %.0f: %s'%(r['ops'],r['ops_build'],chg,r['ops']<=chg)); ok&= r['ops']<=chg
    # 7. the ledger
    tlog,N,sl,opc=ledger(show=False)
    print(' ledger time_log2 = %.5f, score %.5f, success >= %s'%(tlog,tlog+7.069,str(sl)[:12])); ok&= sl>=D('0.39')
        # 8. bucket machine: claws = sorted-search reference, distinct pairs, true row-16 passes
    cvb,_=cv_from_seed('selftest|bucket'); rb=run_bucket(cvb,13,b=9,aw=16,count=True,ref=True,collect_all=True)
    distb=len(set((a0,a1) for (a0,a1,u,fl) in rb['allclaws']))
    badb=sum(1 for (a0,a1,u,fl) in rb['allclaws'] if not r16ok(e16_real_p1(cvb,a0,a1)))
    print(' bucket: buckets=%d claws=%d ref=%d EQUAL=%s distinct=%d row16_bad=%d ops=%d'
          %(rb['buckets'],rb['claws'],rb['refclaws'],rb['claws']==rb['refclaws'],distb,badb,rb['ops']))
    ok&= rb['claws']==rb['refclaws'] and distb==rb['claws'] and badb==0 and rb['claws']>0
    # 9. the bucket ledger: the same premises, the bucket machine's per-u cost, success >= 0.39
    tb,Nb,slb=ledger_bucket(show=False)
    chg=math.ceil(tb*1e4-1e-9)/1e4                 # the charge is the exact value rounded UP at 4 decimals
    print(' bucket ledger time_log2 = %.7f charged %.4f, score %.4f at memory 2^27.0224, success >= %s'%(tb,chg,chg+7.0224,str(slb)[:12]))
    ok&= slb>=D('0.39') and tb<D('83.92')
    ch=counted_head(exhaustive=False)
    print(' A.15.2 probe_two executed: %d comparisons, %d mismatches, %d ops per head'
          %(ch['compared'],ch['bad'],ch['ops']))
    ok&= ch['bad']==0 and ch['ops']==HEAD_OPS
    # 10. A.15.2 rewritten: the shared zero-detect (probe19) at b=10 is the filed predicate, and the packed
    #     seven-lane machine's claws equal an independent sorted search over the retained F values.
    awq,widq,lnq=lane_geom(10); assert (awq,widq,lnq)==(25,36,7) and lane_geom(9)==(26,36,7)
    assert bcast(1)*0==0 and bcast((1<<36)-1)==(1<<252)-1   # 7 x 36 = 252 bits of the 256-bit word
    print(' geometry: b=10 -> AW=%d, %d-bit lanes, %d lanes/word ' % (awq,widq,lnq) +
          '(b + AW = 35 keeps the seven-lane word at every b <= 10)')
    import random as _r; rg=_r.Random(4242); bq=10; awq2=35-bq; tq=(1<<bq)-1
    def rand_word():
        lanes=[]; w=0; tags=[]
        for k in range(LANES7):
            f=rg.getrandbits(1); tg=rg.choice([rg.getrandbits(bq),0,1,4,5,tq]) if rg.random()<0.8 else rg.getrandbits(bq)
            off=rg.getrandbits(awq2)
            lanes.append(f); tags.append(tg)
            w|=(f<<35|(tg<<awq2)|off)<<(widq*k)
        return w,lanes,tags
    bad_mask=0; ncase=0
    for _ in range(3000):
        w0,l0,t0=rand_word(); w1,l1,t1=rand_word()
        T=rg.choice([0,1,4,5,tq,tq-1,tq-4,tq-5,rg.getrandbits(bq)])
        mm,o=probe19(w0,w1,T,bq,awq2,count=True); assert o<=HEAD_OPS_SHARED
        got=sum((1<<35)<<(widq*k) for k in range(LANES7)
                if l0[k] and (mm>>(35+widq*k))&1 and (t0[k]-T) in (0,1,4,5))   # probe + the resolution's window check
        got|=sum((1<<35)<<(widq*(LANES7+k)) for k in range(LANES7)
                 if l1[k] and (mm>>(35+widq*(LANES7+k)))&1 and (t1[k]-T) in (0,1,4,5))
        e=sum((1<<35)<<(widq*k) for k in range(LANES7) if l0[k] and (t0[k]-T) in (0,1,4,5))
        e|=sum((1<<35)<<(widq*(LANES7+k)) for k in range(LANES7) if l1[k] and (t1[k]-T) in (0,1,4,5))
        bad_mask+=int(got!=e); ncase+=1
    print(' probe19 vs the filed predicate on %d random 14-lane words: %d mismatches, %d itemised operations '
          '(head charged at %d)'%(ncase,bad_mask,o,HEAD_OPS_SHARED)); ok&= bad_mask==0
    cvq,_=cv_from_seed('selftest|packed'); rq=run_bucket_packed(cvq,12,b=10,aw=20,count=True,ref=True,collect_all=True)
    K2=cv_consts(cvq)['K2']
    def exact(a0,u,F):
        Pv=(s0(u)-u)&M
        return any(((h+o-Pv)&M)==F for h in R16H for o in OFFS)
    badq=0
    for (a0,a1,u,fl) in rq['allclaws']:
        Fv=(u-a1+K2+a0)&M                      # F recovered from the claw's own a1, not from the machine's bookkeeping
        badq+=int(not exact(a0,u,Fv))
    print(' packed b=10 AW=25 (fixture 2^20): buckets=%d retained=%d claws=%d ref=%d EQUAL=%s, claws failing the '
          'definition F = h+o-P: %d'%(rq['buckets'],rq['occ'],rq['claws'],rq['refclaws'],rq['claws']==rq['refclaws'],badq))
    ok&= rq['claws']==rq['refclaws'] and rq['claws']>0 and badq==0
    print('SELFTEST', 'PASS' if ok else 'FAIL'); return ok
def main():
    if len(sys.argv)>1 and sys.argv[1]=='selftest': sys.exit(0 if selftest() else 1)
    if len(sys.argv)>1 and sys.argv[1]=='ledger': ledger(); return
    if len(sys.argv)>1 and sys.argv[1]=='bucket-ledger': ledger_bucket(); return
    if len(sys.argv)>1 and sys.argv[1]=='counted-head':
        # A.15.2 executed: the two-window test of one head, counted, then the ledger it prices.
        r=counted_head(exhaustive=not (len(sys.argv)>2 and sys.argv[2]=='quick'))
        print('A.15.2 executed on %d-bit lanes, %d lanes of a 256-bit word, %d (tag, window, lane) comparisons:'
              %(r['stride'],r['lanes'],r['compared']))
        print('  address 1, load 1, add 1, and 1, add 1, and 1, and 1     (7)  x 2 windows (the merge `and`)')
        print('  compare-and-branch 2, setup 1                            = %d per head'%r['ops'])
        print('  mismatches %d; one-window-only cases %d, both-window %d; wrap class %d of %d fires (%.2f%%)'
              %(r['bad'],r['onewin'],r['both'],r['wraps'],r['fires'],100.0*r['wraps']/max(1,r['fires'])))
        print('  the ledger charges the wider panel rate %.2f%% (A.15.2): the wrap term never under-charges'
              %(100.0*WRAP_RATE))
        ledger_bucket()
        sys.exit(0 if (r['bad']==0 and r['ops']==HEAD_OPS) else 1)
    if len(sys.argv)>1 and sys.argv[1]=='empty-chain':
        r=counted_empty_chain()
        print('A.15.10 executed: %d fires out of %d draws (rate %.7f vs 4/2^b %.7f); mean chain ops %.4f '
              '(sem %.4f, claw law 10.1145), C1 %d (%.5f), C1C2 %d (%.6f), all-four %d, 99%% upper %.2e, '
              'charged %.3f / %.2e'%(r['n'],r['draws'],r['rate'],4/2**BB,r['mean_ops'],r['sem'],r['k1'],
              r['c1'],r['k2'],r['c12'],r['k4'],r['ub'],r['charge'],max(QPF,r['ub'])))
        sys.exit(0 if abs(r['mean_ops']-10.1145)<=3*r['sem'] and abs(r['rate']-4/2**BB)<5e-4 else 1)
    if len(sys.argv)>1 and sys.argv[1]=='empty-lanes':
        r=counted_empty()
        print('A.15.6 executed: %d of %d lanes empty; fire residues %s (predicted %s), unexplained %d, rate 4/2^%d'
              %(r['empty'],r['lanes'],r['residues'],r['want'],r['bad'],BB))
        sys.exit(0 if (r['bad']==0 and r['watched']) else 1)
    if len(sys.argv)>1 and sys.argv[1]=='fused-resolver':
        r=counted_fused()
        print('A.15.7 executed: %d trials at b=%d; union fires %d, window passes %d, coincidences %d, emitted %d, '
              'mismatches %d; coincidence/window-pass %.5f vs 2/2^b %.5f'
              %(r['trials'],r['b'],r['union_fires'],r['window_passes'],r['coincidences'],r['emitted'],r['bad'],
                r['rate'],2.0/2**r['b']))
        sys.exit(0 if (r['bad']==0 and r['emitted']==r['union_fires'] and r['coincidences']>0) else 1)
    if len(sys.argv)>1 and sys.argv[1]=='probe-head':
        r=counted_head(exhaustive=False)
        print(' probe_two: %d comparisons, %d mismatches, %d ops per head (target %d)'
              %(r['compared'],r['bad'],r['ops'],HEAD_OPS)); return
    if len(sys.argv)>1 and sys.argv[1]=='bucket-ledger10':
        # the b = 10 / AW = 25 design: seven 36-bit lanes, 2^22 buckets, table 2^27 bytes, A.15.2's shared
        # zero-detect at HEAD_OPS_SHARED = 19, and the online table as the memory cell (substitution H6).
        ledger_bucket(b=10,S_P=2**25,aw=25,head=HEAD_OPS_SHARED,mem=27.0); return
    if len(sys.argv)>1 and sys.argv[1]=='fused-table':
        LU=int(sys.argv[2]) if len(sys.argv)>2 else 10
        awv=int(sys.argv[3]) if len(sys.argv)>3 else 25
        cv,_=cv_from_seed(sys.argv[4] if len(sys.argv)>4 else 'fused|table')
        r=fused_table(cv,LU,aw=awv)
        print('A.15.7 on real bucket words: b=%d aw=%d load %.2f, %d scan words x %d fused positions, %d wrap-class '
              'positions skipped; emitted %d, two-window references %d, coincidences %d, empty-lane fires %d, union-mask '
              'mismatches %d, row-16 bad %d; word-1 %d word-2 %d; emitted + coincidences == references: %s; coincidence/emitted '
              '%.5f vs per-position model %.5f, charged %.5f'
              %(r['b'],r['aw'],r['load'],r['u'],r['positions'],r['skipped'],r['emitted'],r['ref'],r['coincidences'],
                r['empty_fires'],r['mask_bad'],r['row16_bad'],r['p1'],r['p2'],
                r['emitted']+r['coincidences']==r['ref'],r['rate'],r['pred'],r['charged']))
        sys.exit(0 if (r['mask_bad']==0 and r['row16_bad']==0 and r['coincidences']>0 and r['emitted']>0
                       and r['emitted']+r['coincidences']==r['ref']) else 1)
    sys.stdout.write(json.dumps(run_request(json.load(sys.stdin))))
if __name__=='__main__': main()
