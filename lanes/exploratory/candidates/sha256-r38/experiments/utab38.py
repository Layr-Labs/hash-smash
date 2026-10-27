#!/usr/bin/env python3
# utab38.py - sha256-r38: the P8 two-block procedure (ePrint 2026/1120 lineage, P8 of 1a695f0b credited) with the
# P1 claw found on the u-table (proof.md Part I); own code, stdlib only. Sections: (1) SHA-256 r38; (2) P8; (3) the claw
# constants, post-filters and step 3b; (4) the u-table machine; (5) organizer experiments; (6) ledger, selftest, main.
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
PQE=list(PQ); PQE[18]=0 # accepted event does not impose E18 = E17 on bits 24,23,15 (Section 6.1)
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
_A,_E=_tx[0],_tx[1]
C16=(_A[12]+_E[12]+S1(_E[15])+CH(_E[15],_E[14],_E[13])+K[16]+s1(PMX[14])+PMX[9])&M
R16H=[int(t,16) for t in ('4b02d320 7b1ab320 7b22b320 7b3ab320 c802f320 c80ad320 c80af320 c812d320 c822f320 c82ad320 c82af320 c832d320 '
                          'cb12f320 cb1ad320 cb1af320 cb22d320 cb32f320 cb3ad320 cb3af320 fb02b320').split()]
R16F=0x405
def r16ok(e): return (e&~R16F&M) in R16H
# A.19: the 20 row-16 heads are equal mod 2^13; every head is head 0 plus d_j = T20[j] << 13.
T20=[(h-R16H[0])>>13 for h in R16H]
assert all((R16H[0]+(t<<13))&M==h for h,t in zip(R16H,T20)) and len(set(T20))==20
OFFS=(0,1,4,5,1024,1025,1028,1029)
T160=sorted(h+o for h in R16H for o in OFFS) # the 160-word row-16 set S160 (= R16W)

# --- (3) claw constants, post-filters, step 3b
# Pricing (frontier-v5, Part I.4): arith/logic/shift/imm/random 1, branch 2, S0/S1/s0/s1 8, CH 3, MAJ 4, access = addr 1 + ld/st 1.
Cc2=0x7af32e15
QPF=(57726359870197/2**58)*(287309824/2**32) # q_pf = 2^-16.1877, H1-P1 (Section 6)
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
 # scalars of the post-filter chain C1 (E5 top 3), C2 (W9 in F9), G (W8 in G'), F7 (W7 in F7)
    A2,A3,A4,A5=SAx[2],SAx[3],SAx[4],SAx[5]; E6,E7,E8,E9=SE[6],SE[7],SE[8],SE[9] # rows 2..5 and 6..9 of S (member x)
    cE5=(A5-S0(A4)-MAJ(A4,A3,A2))&M; K2E5=(cv_consts(cv)['K2']+cE5)&M
    KW9=(E9-A5-S1(E8)-CH(E8,E7,E6)-K[9])&M; cW9=(KW9-cE5)&M
    cE4=(A4-S0(A3))&M; mA=A3&A2; mB=A3|A2
    KW8=(E8-A4-S1(E7)-K[8])&M; cW8=(KW8-cE4)&M; cA=E7&E6; cB=~E7&M
    KK7c=(E7-2*A3-cv[0]+S0(A2)-S1(E6)-K[7])&M # the CH(E6,E5,E4) term is folded with a1,a0 at filter time
    D7c=(_ty[1][7]-_tx[1][7])&M # W7y - W7x = E7y - E7x
    return dict(cE5=cE5,K2E5=K2E5,KW9=KW9,cW9=cW9,cE4=cE4,mA=mA,mB=mB,KW8=KW8,cW8=cW8,cA=cA,cB=cB,A2=A2,E6=E6,KK7c=KK7c,D7c=D7c)
def postfilters(m,cv,a0,u,F,pf):
 # counted chain (a0, u, F) -> flags (c1,c2,g,f7); each segment ends with its counter add (A.31: 6,22,29,31).
    E5=((u-F)+pf['K2E5']+a0)&M; m.op(3)
    s1f=s2=s3=s4=0
    m.br(); m.op(1) # segment 5 + V += 6
    if (E5&0xE0000000)==0xA0000000:
        s1f=1
        w9=(pf['KW9']-E5)&M; m.op(1); w9y=(w9+SPC['D9'])&M; m.op(1)
        d9=(s0(w9y)-s0(w9))&M; m.op(16+1)
        m.br(); m.op(1) # segment 21 + V += 22
        if d9==SPC['D9s']:
            s2=1
            a1=(E5-pf['cE5'])&M; m.op(1)
            maj1=(pf['mA']|(a1&pf['mB']))&M; m.op(2)
            E40=(a0-maj1)&M; m.op(1)
            chx=(pf['cA']^(pf['cB']&E5))&M; m.op(2)
            w8=((pf['cW8']-E40)-chx)&M; m.op(2); w8y=(w8+SPC['D8'])&M; m.op(1)
            d8=(s0(w8y)-s0(w8))&M; m.op(16+1)
            m.br(); m.op(1) # segment 28 + V += 29
            if d8==SPC['T8']:
                s3=1
                E4=(E40+pf['cE4'])&M; m.op(1)
                maj2=MAJ(pf['A2'],a1,a0); m.op(4)
                ch2=CH(pf['E6'],E5,E4); m.op(3)
                w7=((pf['KK7c']+maj2)-ch2)&M; m.op(2); w7y=(w7+pf['D7c'])&M; m.op(1)
                d7=(s0(w7y)-s0(w7))&M; m.op(16+1)
                m.br(); m.op(1) # segment 30 + V += 31
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

# --- (4) the u-table machine (proof.md Part I.2, I.3)
# An epoch draws r (13 bits) and ustart (32 bits); G(u) = s0(u) - u - r. u is covered iff G mod 2^13 < 8 NCOL; its bucket
# is column (G mod 2^13) >> 3, row G >> 13: one 256-bit word of six 42-bit lanes [u:32][field:6][spare:4] with the
# count of filled lanes in bits 252..255; a filled field holds the tag G mod 8, an empty one holds 15. The epoch's
# chaining values scan every a0 of W9 = [9 x 2^26, 10 x 2^26) against the table.
NCOL=15; ROWB=19; RMASK=(1<<ROWB)-1; LANES=6; STR=42; FLD=32; CNT=252; EMPTYT=15; KEP=16
def lanes_const(v): return sum(v<<(STR*L+FLD) for L in range(LANES))
EMPTYW=lanes_const(EMPTYT); MASKW=lanes_const(0b011010); CMAIN=lanes_const(0b010000); CSTR=lanes_const(0b001000)
KW=lanes_const(31); GW=lanes_const(32)
W9=9<<26; QPF=(57726359870197/2**58)*(287309824/2**32)
# charges (Section 4): per u 17; covered u inserted 22, dropped 9; reset 5 per bucket; per a0 35 (+7 when q < 125);
# per probing window SETUP 25, per head ROWJ 2 (+2 on the frame-crossing straddle), per read 9, lane walk 18, per claw 2.
U_BASE=17; U_INS=22; U_DROP=9; RESET=5; A0_BASE=35; A0_RES=7; SETUP=25; ROWJ=2; XCROSS=2; READ=9; WALK=3*LANES
EXTRACT=2; CVSET=76; EPSET=6; STEP3B=3014
def P(u): return (s0(u)-u)&M
def build_table(r,ustart,U,m=None,ncol=NCOL):
    tab={}; ent=drop=0; cov=8*ncol
    if m: m.op(EPSET)
    for n in range(U):
        u=(ustart+n)&M; g=(P(u)-r)&M; lo=g&8191
        if m: m.op(15); m.br()                  # u 1, s0 8, sub 1, -r 1, and 1, loop 3; branch 2
        if lo>=cov: continue
        k=((lo>>3)<<ROWB)|(g>>13); d=tab.get(k,EMPTYW); c=d>>CNT
        if m: m.op(4); m.ld(); m.op(1); m.br()  # col, row, index (shift, add); address+load; count; full?
        if c>=LANES: drop+=1; continue
        sh=STR*c; lane=u|((g&7)<<FLD)
        if m: m.op(3); m.ld(); m.ld(); m.op(4); m.st() # lane; shift and clear mask (constant tables); and, shift, or, count add; store
        d=(d&~(EMPTYT<<(sh+FLD)))|(lane<<sh); d+=1<<CNT; tab[k]=d; ent+=1
    return tab,ent,drop
def table_entries(tab):
    for k,d in tab.items():
        col=k>>ROWB; row=k&RMASK
        for L in range(d>>CNT):
            ln=(d>>(STR*L))&((1<<38)-1); yield ((row<<13)|(col<<3)|(ln>>FLD))&M, ln&M
def probe_word(d,WB,C):
    return ((((d+WB)&MASKW)^C)+KW)&GW         # add, and, xor, add, and: a lane fired iff its guard bit (field bit 5) is 0
# --- (4b) the bitsliced front end (Part II): 256 consecutive a0 per batch, one a0 per bit lane of a 256-bit plane.
# A gate is a 256-bit and/or/xor on two planes, charged 4 (two loads, the operation, a store); a not is charged 3.
# Compile-time constants (bits of the chaining value's scalars) select the gate sequence and cost nothing at run time.
ONES=(1<<256)-1; GATE2=4; GATE1=3; BATCH=8; EXTRACT_BS=29; A0_PROBE=33; CV_BS=640; GBS=2420  # GBS: gate charge of a batch at its worst constants
LANEPL=[sum(((l>>i)&1)<<l for l in range(256)) for i in range(8)]
class Planes:
    def __init__(self,m): self.m=m; self.g=0
    def x(self,a,b): self.g+=GATE2; return a^b
    def a(self,a,b): self.g+=GATE2; return a&b
    def o(self,a,b): self.g+=GATE2; return a|b
    def n(self,a): self.g+=GATE1; return a^ONES
def bs_mask(co,cv,Hr,base,pl,ncol=NCOL):
 # the set of lanes l (a0 = base + l) with ((Hr - F(a0) + 5) mod 2^13) < 8 ncol + 5 or ((... + 1024) mod 2^13) < 8 ncol + 5
    A=list(LANEPL)
    for i in range(8,32): A.append(ONES if (base>>i)&1 else 0); pl.g+=GATE2   # the batch's high bits, broadcast
    e=co['E0base']; E=[0]*32; c=0
    for i in range(32):                                   # E0 = a0 + E0base: ripple with a constant
        ei=(e>>i)&1
        if i==0: E[0]=pl.n(A[0]) if ei else A[0]; c=A[0] if ei else 0; continue
        if ei: E[i]=pl.n(pl.x(A[i],c)); cn=pl.o(A[i],c)
        else: E[i]=pl.x(A[i],c); cn=pl.a(A[i],c)
        c=cn
    def sig(X,r1,r2,r3): return [pl.x(pl.x(X[(i+r1)%32],X[(i+r2)%32]),X[(i+r3)%32]) for i in range(13)]
    S0p=sig(A,2,13,22); S1p=sig(E,6,11,25)               # only bits 0..12 of F are needed
    a,b,ee,ff=cv[0],cv[1],cv[4],cv[5]; MJ=[]; CHp=[]
    for i in range(13):
        ai,bi,ei,fi=(a>>i)&1,(b>>i)&1,(ee>>i)&1,(ff>>i)&1
        MJ.append((ONES if ai else 0) if ai==bi else A[i])                    # MAJ(a0, a, b) bit
        CHp.append((ONES if ei else 0) if ei==fi else (E[i] if ei else pl.n(E[i])))  # CH(E0, e, f) bit
    def neg(X): return [(x^ONES) if x in (0,ONES) else pl.n(x) for x in X]
    konst=(co['KF']+4)&8191                               # -X = ~X + 1 for the four subtracted terms
    terms=[A[:13],neg(S0p),neg(MJ),neg(S1p),neg(CHp),[(ONES if (konst>>i)&1 else 0) for i in range(13)]]
    while len(terms)>2:                                    # carry-save reduction mod 2^13
        X,Y,Z=terms.pop(),terms.pop(),terms.pop(); S=[]; Cc=[0]
        for i in range(13):
            t=pl.x(X[i],Y[i]); S.append(pl.x(t,Z[i])); Cc.append(pl.o(pl.a(X[i],Y[i]),pl.a(Z[i],t)))
        terms+=[S,Cc[:13]]
    X,Y=terms; F=[]; c=0
    for i in range(13):
        t=pl.x(X[i],Y[i]); F.append(pl.x(t,c)); c=pl.o(pl.a(X[i],Y[i]),pl.a(c,t))
    k=(Hr+5+1)&8191; X=[pl.n(f) for f in F]; T=[]; c=0  # t = (Hr + 5 - F) mod 2^13 = ~F + (Hr + 6)
    for i in range(13):
        if (k>>i)&1: T.append(pl.n(pl.x(X[i],c))); c=pl.o(X[i],c)
        else: T.append(pl.x(X[i],c)); c=pl.a(X[i],c)
    lim=8*ncol+5; lt=0; eq=ONES                           # (t mod 1024) < lim, and bits 10..12 all equal
    for i in range(9,-1,-1):
        if (lim>>i)&1: lt=pl.o(lt,pl.a(eq,pl.n(T[i]))); eq=pl.a(eq,T[i])
        else: eq=pl.a(eq,pl.n(T[i]))
    same=pl.n(pl.o(pl.x(T[10],T[11]),pl.x(T[11],T[12])))
    return pl.a(lt,same)
def gbs_worst():
 # the gate charge of bs_mask at the constants that select the dearer gate at every bit (E0base all ones: ripple
 # with not/xor/or; e = 0, f = 1: CH is a not; a != b: MAJ is a variable plane; Hr + 6 = 1..1 mod 2^13): 2,420
    pl=Planes(None); bs_mask(dict(E0base=M,KF=(8191-4)&M),[0,M,0,0,0,M,0,0],(8191-6)&M,W9,pl); return pl.g
def bs_check(seed,nb=16):
 # bs_mask against the scalar predicate on nb random batches of a seed-drawn chaining value and r
    cv,_=cv_from_seed(seed); co=cv_consts(cv); sh=Shake(seed+'|bs'); r=sh.word()&8191; Hr=(R16H[0]-r)&M; bad=n=gmax=0
    for k in range(nb):
        base=W9+((sh.word()&((1<<26)-1))&~255); pl=Planes(None); mask=bs_mask(co,cv,Hr,base,pl); gmax=max(gmax,pl.g)
        for l in range(256):
            t=((Hr-Ffun(cv,base+l,co))+5)&8191; want=t<125 or 7168<=t<7293
            bad+=int(want!=bool((mask>>l)&1)); n+=int(want)
    return dict(bs_batches=nb,bs_probing_lanes=n,bs_mismatches=bad,bs_gates_max=gmax,bs_gate_bound=GBS)
def scan_cv(cv,tab,r,a0s,m=None,ncol=NCOL,collect=None,bs=True):
    co=cv_consts(cv); pf=pf_consts(cv); Hr=(R16H[0]-r)&M; cov=8*ncol; dense=cov+5>1024
    st=dict(a0=0,probes=0,reads=0,fired=0,claws=0,passes=[0,0,0,0],good=[],coll=[],batches=0,gates=0)
    mm=m or Mach()
    def probe(a0,F,y,win):
        yw=(y+(win<<10))&M; row0=yw>>13; c=(yw>>3)&1023; w=yw&7; WB=lanes_const(16-w)
        if m: m.op(SETUP)
        st['probes']+=1
        for j in range(20):
            rowj=(row0+T20[j])&RMASK
            if m: m.op(ROWJ)
            rd=[]
            if c<ncol: rd.append((c,rowj,CMAIN))
            if w>=3:
                if c+1<ncol: rd.append((c+1,rowj,CSTR))
                elif c==1023: rd.append((0,(rowj+1)&RMASK,CSTR)); m and m.op(XCROSS)
            for (cc,rr,C) in rd:
                d=tab.get((cc<<ROWB)|rr,EMPTYW); z=probe_word(d,WB,C); st['reads']+=1
                if m: m.ld(); m.op(5); m.br()
                if z==GW: continue
                st['fired']+=1
                if m: m.op(WALK)
                for L in range(LANES):
                    if (z>>(STR*L+FLD+5))&1: continue
                    u=(d>>(STR*L))&M; st['claws']+=1
                    if m: m.op(EXTRACT)
                    fl=postfilters(mm,cv,a0,u,F,pf)
                    for i in range(4): st['passes'][i]+=fl[i]
                    if collect is not None: collect.append((a0,u,F,fl,j,win))
                    if fl[3]:
                        a1=(u-hfun(cv,a0))&M; st['good'].append((a0,a1,u))
                        ok,wx,wy=step3b(mm,cv,a0,a1)
                        if ok: st['coll'].append((a0,a1,u,wx,wy))
    if bs and not dense:
        if m: m.op(CV_BS)
        a0s=list(a0s); assert a0s[0]%256==0 and len(a0s)%256==0
        for base in range(a0s[0],a0s[0]+len(a0s),256):
            pl=Planes(m); mask=bs_mask(co,cv,Hr,base,pl,ncol); st['batches']+=1; st['gates']+=pl.g; st['a0']+=256
            if m: m.op(pl.g+BATCH); m.br()
            while mask:
                low=mask&-mask; mask^=low; l=low.bit_length()-1; a0=base+l
                F=Ffun(cv,a0,co); y=(Hr-F)&M; v=((y+5)>>10)&7
                if m: m.op(EXTRACT_BS+A0_PROBE)
                probe(a0,F,y,0 if v==0 else 1)
        return st
    for a0 in a0s:
        F=Ffun(cv,a0,co); y=(Hr-F)&M; st['a0']+=1
        if m: m.op(4+26+1)                       # a0 1, loop 3, F 26, y 1
        if dense: wins=(0,1)
        else:
            q=(y+5)&1023
            if m: m.op(2); m.br()
            if q>=cov+5: continue
            v=((y+5)>>10)&7
            if m: m.op(3); m.br(); m.br()     # v (shift, and), V += 7, two branches
            if v==0: wins=(0,)
            elif v==7: wins=(1,)
            else: continue
        for win in wins: probe(a0,F,y,win)
    return st
def ref_claws(cv,tab,r,a0s):
 # independent search: every retained entry whose G equals one of the 160 targets y + 2^13 t_j + o (o in OFFS)
    co=cv_consts(cv); Hr=(R16H[0]-r)&M; lo={}; out=[]
    for G,u in table_entries(tab): lo.setdefault(G&8191,[]).append((G,u))
    for a0 in a0s:
        y=(Hr-Ffun(cv,a0,co))&M
        for o in OFFS:
            for (G,u) in lo.get((y+o)&8191,()):
                if (((G-y-o)&M)>>13) in T20S: out.append((a0,u))
    return out
T20S=set(T20)

# --- (5) organizer experiments: 256 trials in 20 s; working trials then fixed checks; the rest return no pair.
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
def probe_exhaustive():
 # every (kind, w, lane, tag) of the six-lane test against the scalar definitions, on words with random u fields
    sh=Shake('probe|exhaustive'); bad=n=0
    for kind,C in ((0,CMAIN),(1,CSTR)):
        for w in range(8):
            WB=lanes_const(16-w)
            for rep in range(24):
                tags=[(rep*5+L*3+w)%9 for L in range(LANES)]; tags=[EMPTYT if t==8 else t for t in tags]
                d=sum(((sh.word()|(t<<FLD))<<(STR*L)) for L,t in enumerate(tags))|((rep%7)<<CNT)
                z=probe_word(d,WB,C)
                for L,t in enumerate(tags):
                    fired=not (z>>(STR*L+FLD+5))&1
                    want=t!=EMPTYT and ((t-w) in (0,1,4,5) if kind==0 else (t+8-w) in (0,1,4,5))
                    bad+=int(fired!=want); n+=1
    return n,bad
def online_trial(seed,U=1<<17,NA=1<<17):
    sh=Shake(seed+'|epoch'); r=sh.word()&8191; ustart=sh.word(); cv,M0=cv_from_seed(seed)
    m=Mach(); tab,ent,drop=build_table(r,ustart,U,m); bops=m.ops
    base=sh.word()&((1<<26)-1)&~(NA-1); a0s=range(W9+base,W9+base+NA)
    col=[]; m2=Mach(); st=scan_cv(cv,tab,r,a0s,m2,collect=col)
    ref=sorted(ref_claws(cv,tab,r,a0s)); got=sorted((a0,u) for (a0,u,F,fl,j,win) in col)
    e16bad=sum(1 for (a0,u,F,fl,j,win) in col if not r16ok(e16_real_p1(cv,a0,(u-hfun(cv,a0))&M)))
    pfmis=sum(1 for (a0,u,F,fl,j,win) in col if pf_ref(cv,a0,(u-hfun(cv,a0))&M)!=tuple(fl))
    return cv,M0,st,dict(entries=ent,dropped=drop,claws=st['claws'],ref_claws=len(ref),   # at most 16 observations
        claws_equal_ref=int(got==ref),claw_e16_bad=e16bad,postfilter_ref_mismatch=pfmis,probes=st['probes'],
        reads=st['reads'],scan_ops=m2.ops,c1=st['passes'][0],c1c2=st['passes'][1],good_pairs=len(st['good']),
        step3b_collisions=len(st['coll']),expected_claws_milli=int(round(1000*160.0*ent*NA/2**32)),distinct_pairs=len(set(got)))
def dense_trial(seed,U=1<<16,NA=1<<13,rows=True):
 # full-frame coverage (NCOL = 1024): every scanned u is covered, both windows probed; claws checked as above and,
 # optionally, both members rebuilt and the tests of rows 16..21 applied in order (cumulative counts)
    sh=Shake(seed+'|dense'); r=sh.word()&8191; ustart=sh.word(); cv,M0=cv_from_seed(seed)
    tab,ent,drop=build_table(r,ustart,U,None,ncol=1024)
    base=sh.word()&((1<<26)-1)&~(NA-1); a0s=range(W9+base,W9+base+NA)
    col=[]; st=scan_cv(cv,tab,r,a0s,None,ncol=1024,collect=col)
    ref=sorted(ref_claws(cv,tab,r,a0s)); got=sorted((a0,u) for (a0,u,F,fl,j,win) in col)
    cum=[0]*22; bad=pfmis=0
    for (a0,u,F,fl,j,win) in col:
        a1=(u-hfun(cv,a0))&M; wx=variantW_P1(cv,a0,a1,SAx,SExF); wy=variantW_P1(cv,a0,a1,SAy,SEyF)
        tx=trace(cv,wx); ty=trace(cv,wy); e16=tx[1][16]
        bad+=int(not r16ok(e16) or ((e16-R16H[j]-(win<<10))&M) not in (0,1,4,5))
        pfmis+=int(pf_ref(cv,a0,a1)!=tuple(fl))
        if rows:
            for i in range(16,22):
                if rowok(tx,ty,i): cum[i]+=1
                else: break
    return dict(entries=ent,claws=st['claws'],ref_claws=len(ref),claws_equal_ref=int(got==ref),row16_bad=bad,
        postfilter_ref_mismatch=pfmis,distinct_pairs=len(set(got)),rows_le16=cum[16],rows_le17=cum[17],
        rows_le18=cum[18],rows_le19=cum[19],rows_le20=cum[20],rows_le21=cum[21],c1=st['passes'][0],
        c1c2=st['passes'][1],expected_claws_milli=int(round(1000*160.0*ent*NA/2**32)))
NON=4; NDE=4
def run_request(req):
    out=[]; eid=req['experiment_id']
    for tr in req['trials']:
        t=tr['trial']; rec=dict(trial=t,message_a_hex=None,message_b_hex=None); s=eid+'|'+tr['seed']
        if 'online' in eid:
            if t<NON:
                cv,M0,st,obs=online_trial(s); rec['observations']=obs
                if st['coll'] and obs['claw_e16_bad']==0:   # step 3b accepted: rows 16..21 pass and the outputs are equal
                    a0,a1,u,wx,wy=st['coll'][0]
                    rec['message_a_hex']=struct.pack('>32I',*(M0+wx)).hex(); rec['message_b_hex']=struct.pack('>32I',*(M0+wy)).hex()
            elif t==NON: rec['observations']=spair_obs()
            elif t==NON+1:
                n,bad=probe_exhaustive(); rec['observations']=dict(probe_lanes_checked=n,probe_mismatches=bad)
            elif t==NON+2:
                ob=bs_check(s); ob['bs_gate_worst']=gbs_worst(); rec['observations']=ob
        else:
            if t<NDE: rec['observations']=dense_trial(s)
            elif t==NDE: rec['observations']=spair_obs()
        out.append(rec)
    return dict(schema_version=1,trials=out)

# --- (6) ledger, selftest, main
# E_LO, E_HI: the least and the largest number of retained entries of the full-scale table over all 8192 values of r
# (exhaustive count over all 2^32 u, Part I.5); COV: covered u per epoch, exactly 120 x 2^19 for every r (P is balanced
# mod 2^13). The ledger charges the cost terms at E_HI and the success terms at E_LO.
E_LO=44436632; E_HI=44543396; E_MEAN='44485887.327'; COV=120*2**19; NB=NCOL*2**ROWB
Q3P1='-96.0791'
def ledger(show=True,q3_log2=Q3P1,eps_log2=16,succ='0.39',A_C=2**78,A_S=2**74,DEV=2**70,mem='27.92',kep=KEP,bs=True):
    getcontext().prec=90
    C=2728; L2=D(2).ln(); P2=lambda x: (D(x)*L2).exp(); NA=2**26; eps=D(2)**-eps_log2; K=2**kep
    p12=D(53096854)/D(2)**32; p12g=D(57726359870197)/D(2)**58; q_pf=p12g*D(287309824)/D(2)**32
    pf=6+D(22)/8+29*p12+31*p12g                               # A.31 folded segments, per claw
    pres=D(125)/1024; pprobe=D(250)/8192                      # Pr[q < 125], Pr[a window probes] (H1: y uniform)
    reads=D(20)*195/125; xc=D(20)*5/125                       # reads per probing window, frame-crossing heads
    probe=SETUP+20*ROWJ+reads*(READ+WALK)+xc*XCROSS           # the lane walk charged on every read
    claw=EXTRACT+pf+q_pf*STEP3B
    ca_hi=D(160)*E_HI/D(2)**32; ca_lo=D(160)*E_LO/D(2)**32   # claws per a0
    per_a0=(D(GBS+BATCH+2)/256+pprobe*(EXTRACT_BS+A0_PROBE+probe)+ca_hi*claw) if bs else (A0_BASE+pres*A0_RES+pprobe*probe+ca_hi*claw)
    wbar=C+CVSET+(CV_BS if bs else 0)+NA*per_a0
    build=EPSET+NB*RESET+D(2)**32*U_BASE+E_HI*U_INS+(COV-E_HI)*U_DROP
    a0max=(D(GBS+BATCH+2)/256+EXTRACT_BS+A0_PROBE if bs else A0_BASE+A0_RES)+SETUP+20*(ROWJ+XCROSS)+40*(READ+WALK)+40*LANES*(EXTRACT+6+22+29+31+STEP3B)
    vmax=int(C+CVSET+(CV_BS if bs else 0)+NA*a0max)
    q3r=P2(q3_log2)*D(2)**32/160
    lam=NA*ca_lo*q_pf*q3r*(1-D(2)**D('-8.5'))*(1-D(2)**-25)
    target=1-D(succ)-D(2)**-60
    NCV=int((-(target).ln()/lam))+1
    while 1-(-(NCV-1)*lam).exp()-D(2)**-60>=D(succ): NCV-=1
    NE=-(-NCV//K)
    VCV=int(((1+eps)*NCV*wbar).to_integral_value(rounding='ROUND_CEILING'))
    VMAX=NE*int(build)+VCV
    bern=(eps**2*NCV*wbar)/(2*vmax*(1+eps/3)); succ_lb=1-(-NCV*lam).exp()-(-bern).exp()-D(2)**-60
    ALLOW=(A_C+A_S+DEV)*C; OVER=int(max(vmax,build)); FIN=6*C+1600; N=ALLOW+VMAX+OVER+FIN
    tlog=float((D(N)/C).ln()/L2); score=tlog+float(D(mem))-20
    if show:
        print('u-table: %d columns x 2^%d rows, %d lanes, %d bytes; retained entries %d .. %d (mean %s) of %d covered'
              %(NCOL,ROWB,LANES,32*NB,E_LO,E_HI,E_MEAN,COV))
        print('claws/a0 = %.6f (charged %.6f); q_pf = 2^%.4f; post-filter chain %.6f + q_pf x step 3b %.6f per claw'
              %(float(ca_lo),float(ca_hi),float(q_pf.ln()/L2),float(pf),float(q_pf*STEP3B)))
        if bs: print('per a0: front end (%d + %d + 2)/256 = %.6f + %.6f x (%d + %d + probe %.4f) + %.6f x claw %.6f = %.6f ops; per claw %.4f'
              %(GBS,BATCH,float(D(GBS+BATCH+2)/256),float(pprobe),EXTRACT_BS,A0_PROBE,float(probe),float(ca_hi),float(claw),float(per_a0),float(per_a0/ca_lo)))
        else: print('per a0: base %d + %.6f (resolve) + %.6f x probe %.4f + %.6f x claw %.6f = %.6f ops; per claw %.4f'
              %(A0_BASE,float(pres*A0_RES),float(pprobe),float(probe),float(ca_hi),float(claw),float(per_a0),float(per_a0/ca_lo)))
        print('epoch build %d ops (%.4f%% of an epoch of 2^%d chaining values)'%(int(build),100*float(build/(K*wbar)),kep))
        print('wbar = %.6e  vmax = %d  N_CV = %d  epochs = %d  V_MAX = %d'%(float(wbar),int(vmax),NCV,NE,VMAX))
        print('allowances A_C + A_S + DEV = 2^%.5f compressions = %.4f%% of N;  N = %d'%(float((D(A_C+A_S+DEV)).ln()/L2),100*float(D(ALLOW)/N),N))
        print('time_log2 = %.7f  memory 2^%s  score = %.7f  success >= %s'%(tlog,mem,score,str(succ_lb)[:22]))
    return tlog,N,succ_lb,dict(per_a0=per_a0,wbar=wbar,NCV=NCV,ca_lo=ca_lo,ca_hi=ca_hi,probe=probe,claw=claw)
def selftest():
    print('selftest utab38'); ok=True
    assert (SPC['F7d'],SPC['T8'],SPC['D8'],SPC['D7'],SPC['D9s'])==(0x03bff800,0xfe808000,0xfbc00800,0x20000000,0x043ff800)
    assert len(T160)==160 and all(r16ok(w) for w in T160) and len(T20S)==20; print(' S-pair constants, |S160| = 160: OK')
    o=spair_obs(); print(' step 3b on the P8 pair:',o); ok&= o['step3b_P8_pair_ok']==1 and o['step3b_P8_pair_ops']==STEP3B
    n,bad=probe_exhaustive(); print(' six-lane test against the scalar definitions: %d lane checks, %d mismatches'%(n,bad)); ok&= bad==0
    gw=gbs_worst(); ob=bs_check('selftest|bs',nb=64)
    print(' bitsliced front end:',ob,'worst-constant gate charge',gw); ok&= ob['bs_mismatches']==0 and gw==GBS and ob['bs_gates_max']<=GBS
    # 1. every claw equals the independent search, is a true row-16 pass, and its post-filter flags are the real ones
    for sd in ('selftest|a','selftest|b'):
        cv,M0,st,ob=online_trial(sd); print(' online',sd,ob)
        ok&= ob['claws_equal_ref']==1 and ob['claw_e16_bad']==0 and ob['postfilter_ref_mismatch']==0 and ob['claws']>0
        ob=dense_trial(sd,NA=1<<13); print(' dense ',sd,ob)
        ok&= ob['claws_equal_ref']==1 and ob['row16_bad']==0 and ob['postfilter_ref_mismatch']==0 and ob['claws']>0
    # 2. retention and the lane format at load: 64 u forced into four buckets of one row (synthetic placement)
    tab={}; rr=random.Random(5); keep={}
    for i in range(64):
        u=rr.getrandbits(32); g=(rr.randrange(4)<<3)|rr.randrange(8); k=((g>>3)<<ROWB)|7; d=tab.get(k,EMPTYW); c=d>>CNT
        if c<LANES:
            sh=STR*c; d=(d&~(EMPTYT<<(sh+FLD)))|((u|((g&7)<<FLD))<<sh); d+=1<<CNT; tab[k]=d; keep.setdefault(k,[]).append((g&7,u))
    rec={k:[((d>>(STR*L+FLD))&15,(d>>(STR*L))&M) for L in range(d>>CNT)] for k,d in tab.items()}
    emp=all(((d>>(STR*L+FLD))&63)==EMPTYT for k,d in tab.items() for L in range(d>>CNT,LANES))
    print(' retention: %d buckets, first six kept in insertion order %s, empty lanes marked %s'%(len(tab),rec==keep,emp)); ok&= rec==keep and emp
    # 3. the counted scan agrees with the ledger's per-a0 charge at reduced occupancy (lane walk charged only on fires)
    cv,_=cv_from_seed('selftest|ops'); sh=Shake('selftest|ops'); r=sh.word()&8191
    tab,ent,drop=build_table(r,sh.word(),1<<16); m=Mach(); a0s=range(W9,W9+(1<<16)); st=scan_cv(cv,tab,r,a0s,m)
    chg=CV_BS+st['batches']*(GBS+BATCH+2)+st['probes']*(EXTRACT_BS+A0_PROBE+SETUP+20*ROWJ+20*XCROSS)+st['reads']*(READ+WALK)
    chg+=st['claws']*(EXTRACT+6+22+29+31)+len(st['good'])*STEP3B
    print(' counted scan ops %d <= itemised charge %d: %s (probes %d of %d a0, reads %d)'%(m.ops,chg,m.ops<=chg,st['probes'],st['a0'],st['reads']))
    ok&= m.ops<=chg and abs(st['probes']/st['a0']-250/8192)<0.003
    tlog,N,sl,_=ledger(show=False); print(' ledger time_log2 = %.7f, success >= %s'%(tlog,str(sl)[:12])); ok&= sl>=D('0.39')
    print('SELFTEST','PASS' if ok else 'FAIL'); return ok
def main():
    a=sys.argv[1] if len(sys.argv)>1 else ''
    if a=='selftest': sys.exit(0 if selftest() else 1)
    if a=='ledger': ledger(); return
    if a=='ledger-reduced': ledger(A_C=2**60,A_S=2**60,DEV=2**60); return
    if a=='ledger-scalar': ledger(bs=False); return
    sys.stdout.write(json.dumps(run_request(json.load(sys.stdin))))
if __name__=='__main__': main()
