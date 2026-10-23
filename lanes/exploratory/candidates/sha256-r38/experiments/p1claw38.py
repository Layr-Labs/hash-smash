#!/usr/bin/env python3
# p1claw38.py - sha256-r38, the A0-variant two-block procedure of ePrint 2026/1120 with the characteristic P8 of dariolina's 1a695f0b
# (data, credited) and the "P1" sum-claw that finds the row-16 passes by a meet-in-the-middle between a 2^26-slot table over the
# low variant word a0 and a scan over the free word u = W1, instead of the bit-sliced plane programs of fb176310.  Own code (no
# program of another participant is executed; P8's cells, pair and conditions are data read from the public proof of 1a695f0b,
# credited in proof.md Section 2).  Standard library only.
# Sections: (1) SHA-256 r38 reference; (2) P8 characteristic and the S pair; (3) the counted claw machine and ledger; (4) organizer
# experiments p1-online-r38 and p1-q3-r38 (stdin JSON -> stdout JSON); (5) selftest, calibrate, ledger, main.
import sys, json, hashlib, struct, math, random
from decimal import Decimal as D, getcontext

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
Cc2=0x7af32e15; RWIN=9; PK_LD=5; PK_ST=9
# Table design (proof.md Section 4).  A slot is indexed by F(a0) >> (32-ls), and the loader inserts the whole window R = 9,
# 2^AW candidates, so the occupancy is 1 - e^-(2^(AW-ls)): four candidates per slot at the full-scale pair (ls, AW) = (24, 26).
# The entry keeps the low 32-ls bits of F and the low (32-(32-ls)) bits of the a0 offset; the remaining AW-(32-(32-ls)) bits of
# the offset live in the side array `side`, indexed by the same slot (two bits per slot at full scale).
LSf=25; AW=26; SIDE_OPS=4        # a side-array read: address 1, 256-bit load 1, shift 1, and 1
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
    """Per chaining value, before its scan (counted, proof.md Section 5): the first-block words 30 (2 random 256-bit words,
    16 fields), the target compression (1 unit, not in m.ops), the claw scalars 38 (k0 29, E0base 2, PP QQ EF 3, KF 2, K2 1,
    KK7c 1), the scan start u0 (random word 1), V += the fixed work of the chaining value 1, the cap test 2, the loop 3 = 75."""
    if m: m.op(30+38+1+1+2+3)
    co=cv_consts(cv); pf=pf_consts(cv)
    st=(0x9E3779B97F4A7C15^((cv[0]<<32)|cv[1]))&0xFFFFFFFFFFFFFFFF  # experiments: the random word u0, derived from the chaining value
    st^=(st<<13)&0xFFFFFFFFFFFFFFFF; st^=st>>7; st^=(st<<17)&0xFFFFFFFFFFFFFFFF
    return co,pf,(st>>16)&M
def postfilters(m,cv,a0,u,F,pf):
    # counted chain on (a0, u, F); returns stage flags (c1,c2,g,f7).  Each segment ends with its work-counter add (V += k, 1).
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
    """The counted tests of row i (proof.md Section 3, step 3b): per word A, E, W (W not at rows 7, 8): the cell value (AND, compare-
    and-branch: 3, when the cell fixes bits) and the XOR difference (XOR, compare-and-branch: 3); the '+' pair (XOR, AND, branch: 4);
    each two-bit condition closing at row i (2 shifts, XOR, AND, branch: 6).  Stops at the first failing test."""
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
    """Step 3b on the pair (a0, a1) of chaining value cv, counted (proof.md Section 3): Step 2 of both members (E0..E5 15 each,
    W0..W9 16 each; W10..W15 are S's words), rows 16..37 of both members (per member and row: W 19, E 16, A 15 = 50), the tests of
    rows 16..21 after each of those rows with an early abort, the comparison of the eight output words (8 XOR, 7 OR, compare-and-
    branch: 17), and the work-counter add at the exit (1).  ok = rows 16..21 pass and A34..A37, E34..E37 are equal (Lemma 1)."""
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
    """One chaining value: build the 2^ls-slot table over the a0 window RWIN, insert the 2^aw candidates of that window (aw >= ls:
    the surplus saturates the table), scan the 2^LU distinct words u = u0 + n, run the post-filters on every claw and step 3b on
    every good pair.  Full scale: ls = 24, aw = 26, LU = 32 (proof.md Section 3).  The entry holds the low TB = 32-ls bits of F
    and the low 32-TB bits of the a0 offset; when aw exceeds 32-TB the remaining bits of the offset live in `side`, indexed by the
    same slot (two bits per slot at full scale).  count: charge every operation at the pricing of proof.md Section 4, the
    work-counter adds included.  ref: also count claws by an independent sorted-array search over the table."""
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
        # counted build: a0 1, E0 1, S0 8, MAJ 2, S1 8, CH 2, F 5, slot 1, entry 3, loop 3 = 34; packed store 2 + 9;
        # a side store is a read-modify-write of a byte inside a 256-bit word: address 1, load 1, shift 1, and 1,
        # or 1, store 1 = 6 (the primitive store is charged, as lane_cost/F-SIDE-STORE-OMITTED requires)
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

# ----------------------------------------------------------------- (3c) the seven-lane bucket table (proof.md Appendix A.15)
# One 256-bit word per bucket.  bucket = F >> b covers 2^b values of F; the word holds L = 256 // (1+b+AW) lanes of
# [1 headroom][b tag][AW offset] bits.  A lookup for the target F = Wsub reads the bucket Wsub >> b and tests the lanes'
# b-bit tags against Wsub mod 2^b on every bit except bits 0 and 2 -- the two bits the P1 variant leaves free.  A lane
# whose tag passes is the claw of its stored a0 at F = (bucket << b) | tag, i.e. F agrees with Wsub on every bit except
# bits 0 and 2, exactly the predicate of the packed-slot machine.  The loader inserts the whole R = 9 window in a random
# cyclic order and keeps the first L lanes per bucket, so the retained set is a uniform random L-subset of each bucket.
BB=9; BBL=7; MATCH_OPS=18; HEAD_OPS=17; BCAST_OPS=7
def bucket_lanes(b=BB):
    return 256//(1+b+AW)
def bucket_filled(S_P,b,lanes):
    """E[min(Binomial(S_P, 2^-(32-b)), lanes)]: the expected number of filled lanes of one bucket."""
    from math import comb
    s=cum=0.0; p=1.0/2**(32-b)
    for k in range(lanes):
        pk=comb(S_P,k)*p**k*((1-p)**(S_P-k)); s+=k*pk; cum+=pk
    return s+lanes*(1-cum)
def bucket_terms(S_P=2**AW,b=BB,match=MATCH_OPS,head=HEAD_OPS,bcast=BCAST_OPS):
    """Expected counted operations per scan word u and claws per u of the bucket machine (proof.md A.15.4)."""
    lanes=bucket_lanes(b)
    filled=bucket_filled(S_P,b,lanes)
    claws=40*filled*4/2**b
    matches=claws                              # bit 35 of a lane is its filled flag and the broadcast carries it set
    strad=(5/2**b)*40*9                        # the straddle pass (tag - tg wraps): 5/2^b of the 40 window lookups, 9 each
    fixed=13+2+bcast
    pf=7+22/8+29*(53096854/2**32)+30*(57726359870197/2**58)
    per_u=fixed+20*head+strad+matches*match+claws*(pf+QPF*3014)
    return per_u,claws,filled,lanes
def run_bucket(cv,LU,b=BB,aw=AW,count=True,ref=False,collect_all=False):
    """One chaining value on the seven-lane bucket table.  Builds the 2^(32-b)-bucket table over the R = 9 window's
    2^aw candidates (random cyclic order, first BBL per bucket), scans 2^LU words u, resolves every matching lane,
    forms a0 and F, and runs the post-filters and step 3b exactly as run_claw does.  count charges the bucket machine's
    operations at proof.md A.15.4; ref counts the same claws by an independent sorted search over the retained F values."""
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
            if m: m.op(17)                      # per head: 2 bucket loads 4, W 1, bucket 1, b+2 1, the two field tests 8, branch 2
            for Wsub in (W,(W+1024)&M):
                tg=Wsub&tmask; k0=Wsub>>b
                for kk in (k0,k0+1):            # k0 + 1 is the straddle pass: tag - tg may wrap into the next bucket
                    if kk!=k0 and tg<(1<<b)-5: break
                    if m and kk!=k0: m.op(9)    # the straddle lookup: address 1, load 1, the field test 5, branch 2
                    lst=tab.get(kk)
                    if not lst: continue
                    for tag,off in lst:
                        if (((tag+(1<<b)-tg)^(1<<b))&(tmask&~5)): continue   # tag - tg in {0,1,4,5} (proof.md A.15.2)
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
    """W0..W15 of one member of the P1 variant (BOTH a0 = A0 and a1 = A1 free; A2..A15 = S, E6..E15 = S).  Port of p1claw.c variantW."""
    A={-1:cv[0],-2:cv[1],-3:cv[2],-4:cv[3]}; E={-1:cv[4],-2:cv[5],-3:cv[6],-4:cv[7]}
    A[0]=a0; A[1]=a1
    for i in range(2,16): A[i]=SA[i]
    for i in range(6): E[i]=(A[i]+A[i-4]-S0(A[i-1])-MAJ(A[i-1],A[i-2],A[i-3]))&M
    for i in range(6,16): E[i]=SEF[i]
    return [(E[i]-A[i-4]-E[i-4]-S1(E[i-1])-CH(E[i-1],E[i-2],E[i-3])-K[i])&M for i in range(16)]
def pf_ref(cv,a0,a1):
    """The post-filter chain on the real words of both members (reference for postfilters): C1 W8y - W8x = D8, C2, G, F7 the s0
    differences of W9, W8, W7 (and W7y - W7x = D7); returned as the cumulative stage flags."""
    wx=variantW_P1(cv,a0,a1,SAx,SExF); wy=variantW_P1(cv,a0,a1,SAy,SEyF)
    c1=((wy[8]-wx[8])&M)==SPC['D8']; c2=((s0(wy[9])-s0(wx[9]))&M)==SPC['D9s']; g=((s0(wy[8])-s0(wx[8]))&M)==SPC['T8']
    f7=((s0(wy[7])-s0(wx[7]))&M)==SPC['F7d'] and ((wy[7]-wx[7])&M)==SPC['D7']
    return (int(c1),int(c1 and c2),int(c1 and c2 and g),int(c1 and c2 and g and f7))
def e16_real_p1(cv,a0,a1):
    """The real E16 of member x of the P1 claw pair (a0,a1); equals F(a0) + Phi(u), checked 0 bad by p1claw.c."""
    W=variantW_P1(cv,a0,a1,SAx,SExF); return trace(cv,W)[1][16]

# ----------------------------------------------------------------- (4) organizer experiments
# organizer budget: one request of 256 trials within 20 s (runner.py); trials 0..NWORK-1 do the work, trial NWORK runs step 3b on the
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
            # every claw is a row-16 pass by construction: verify its real E16 (both free words a0,a1) lands in the 160-word set
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
    """The seven-lane bucket machine of proof.md A.15 at a reduced size: trials 0..3 build the bucket table over the
    scaled a0 window (2^16 candidates, 2^23 buckets), scan 2^13 words u, and report the claws against an independent
    sorted-array search over the same retained F values, the distinct claw pairs, and every claw's real E16; trials 4..255
    return no pair by design.  This is a reduced-size fixture run, not success-probability evidence."""
    out=[]
    for tr in req['trials']:
        t=tr['trial']; rec=dict(trial=t,message_a_hex=None,message_b_hex=None)
        if t<NBWORK:
            cv,M0=cv_from_seed(req['experiment_id']+'|'+tr['seed'])
            r=run_bucket(cv,NB_LU,b=9,aw=NB_AW,count=True,ref=True,collect_all=True)
            bad=sum(1 for (a0,a1,u,fl) in r['allclaws'] if not r16ok(e16_real_p1(cv,a0,a1)))
            rec.update(claws=r['claws'],refclaws=r['refclaws'],claws_equal_ref=int(r['claws']==r['refclaws']),
                       distinct_pairs=len(set((a0,a1) for (a0,a1,u,fl) in r['allclaws'])),row16_bad=bad,
                       buckets=r['buckets'],occupied_lanes=r['occ'],counted_ops=r['ops'],counted_ops_build=r['ops_build'],
                       expected_claws=round(40.0*r['occ']*(1<<NB_LU)*4/2**32,6))
        out.append(rec)
    return dict(schema_version=1,trials=out)
def q3_experiment(req):
    """Evidence for H2-P1 and H3-P1.  Every claw is a row-16 pass of member x.  For every claw of the counted procedure (reduced ls),
    rebuild both members and report how many pass the tests of rows 16..21 cumulatively (step 3b's tests), the post-filter stage counts,
    and that the claws of one chaining value are distinct pairs (a0, a1).  No full collision is expected at this scale."""
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

# ----------------------------------------------------------------- (5) ledger, selftest, main
STEP3B=3014                     # step 3b on its longest path (every test passing), counted on the P8 pair by selftest
CVSET=75                        # cv_begin: per chaining value, besides its compression
BUILD1=34+2+PK_ST               # one table candidate: 34 + store 2 + packed 9 = 45
RESET1=5                        # table reset to SENT, per 256-bit word: store 1, address add 1, loop 3 (ruling a75499a6)
def scan_terms(t,occ):
    """Expected counted operations per scan value u (the run_claw counter, work-counter adds included) at table size 2^(32-t),
    given the occupancy occ; and the claws per u.  Residue passes 4/2^t per lookup (an occupied slot's tag and an empty slot's
    marker each pass for 4 values of the window's low bits); straddles 5/2^t per window."""
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
    wbar=C+CVSET+(n0>>3)*RESET1+NC*B1+U*per_u                          # mean online work of one chaining value (upper bound: step 3b at its maximum)
    umax=fix+20*(1+22+2*10+2*8)+80*(7+22+29+30+STEP3B+SV)   # every head straddling, every slot occupied, 80 claws all reaching step 3b
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
                  b=BB,S_P=2**AW,match=MATCH_OPS,head=HEAD_OPS,bcast=BCAST_OPS,mem=28.0114):
    """The full-scale ledger of the bucket machine (proof.md A.15).  Section 7 of this proof is unchanged: q_pf, q3r,
    the Bonferroni/H3-P1 factor and the cap argument are the parent's, and only the per-u cost and the claw rate move."""
    getcontext().prec=90
    if q3_log2 is None: q3_log2=Q3P1
    C=2728; U=2**ULOG; eps=D(2)**-eps_log2
    B=2**(32-b); lanes=bucket_lanes(b)
    L2=D(2).ln(); P2=lambda x: (D(x)*L2).exp()
    p1=D(1)/8; p12=D(53096854)/D(2)**32; p12g=D(57726359870197)/D(2)**58
    q_pf=p12g*D(287309824)/D(2)**32
    per_u,claws_u,filled,lanes=bucket_terms(S_P,b,match,head,bcast)
    per_u=D(repr(per_u)); claws_u=D(repr(claws_u)); filled=D(repr(filled))
    BUILD2=34+2+1+1+2                                   # F(a0) 34 + lane read-modify-write 6 (address, load, or, and, store, loop)
    build=D(S_P)*BUILD2; reset=D(B>>3)*5
    wbar=C+CVSET+reset+build+U*per_u
    matches_ub=40*lanes*4/D(2)**b
    umax=D(13+2+bcast)+20*head+(D(5)/D(2)**b)*301+D(40*lanes)*match+matches_ub*(7+22+29+30+STEP3B)
    vmax=C+CVSET+reset+build+U*umax
    q3r=P2(q3_log2)*D(2)**32/160
    claws_lo=40*(filled-D(1)/64)*4/D(2)**b
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
              %(b,lanes,1+b+AW,32-b,37-b))
        print('load = 2^%.2f per bucket, E[filled lanes] = %.5f of %d, claws/u = %.5f'
              %(math.log2(S_P)- (32-b),float(filled),lanes,float(claws_u)))
        print('per u: fixed %d + 20 heads x %d + straddle %.4f + matches x %d + claws x (pf + q_pf step3b) = %.4f'
              %(13+2+bcast,head,float((D(5)/D(2)**b)*301),match,float(per_u)))
        print('ops/claw (scan + filters + build) = %.3f'%(float(per_u)/float(claws_u)))
        print('wbar = %.6e   N_CV = %d   V_MAX = %d'%(float(wbar),NCV,VMAX))
        print('allowances A_C 2^%d C, A_S 2^%d C, DEV 2^%d C  -> %.3f%% of V_MAX'%(A_C.bit_length()-1,A_S.bit_length()-1,DEV.bit_length()-1,100*float(ALLOW)/VMAX))
        print('time_log2 = %.5f   memory %.4f   score = %.5f'%(tlog,mem,tlog+max(0.0,mem-20)))
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
    # 4. a claw run on a random cv: claws equal the independent reference, occ ~ 0.632, distinct pairs, every claw lands in S160
    cv,_=cv_from_seed('selftest|0'); r=run_claw(cv,16,ls=15,aw=16,count=True,ref=True,collect_all=True)
    dist=len(set((a0,a1) for (a0,a1,u,fl) in r['allclaws']))
    print(' claws=%d ref=%d EQUAL=%s distinct=%d occ=%.4f c1=%d c1c2=%d c1c2g=%d all4=%d ops=%d'%(r['claws'],r['refclaws'],
        r['claws']==r['refclaws'],dist,r['occ_frac'],r['passes'][0],r['passes'][1],r['passes'][2],r['passes'][3],r['ops']))
    ok&= r['claws']==r['refclaws'] and dist==r['claws'] and abs(r['occ_frac']-(1-math.exp(-2)))<0.01   # 2^16 candidates, 2^15 slots
    bad=sum(1 for (a0,a1,u,fl) in r['allclaws'] if not r16ok(e16_real_p1(cv,a0,a1)))
    print(' every claw is a true row-16 pass (E16 of the P1 pair in S160): %d claws, %d bad'%(r['claws'],bad)); ok&= bad==0
    # 5. the counted post-filter chain equals the chain on the real words of both members (random pairs, half with C1 forced)
    import random; rr=random.Random(11); mis=0; st=[0,0,0,0]
    for k in range(60000):
        cv2=[rr.getrandbits(32) for _ in range(8)]; a0=rr.getrandbits(32); a1=rr.getrandbits(32); pf2=pf_consts(cv2)
        if k%2: a1=((0xA0000000|rr.getrandbits(29))-pf2['cE5'])&M
        fl=postfilters(Mach(),cv2,a0,(a1+hfun(cv2,a0))&M,Ffun(cv2,a0,cv_consts(cv2)),pf2); rf=pf_ref(cv2,a0,a1)
        mis+=int(tuple(fl)!=rf); st=[x+y for x,y in zip(st,rf)]
    print(' post-filter chain vs the real words: 60000 pairs, stage counts %s, %d mismatches'%(st,mis)); ok&= mis==0
    # 6. the counted run against the ledger's per-u terms at the same size (claws charged at their longest post-filter path)
    getcontext().prec=40
    fix,var,cpu=scan_terms(32-15,D(r['occ_frac']))
    chg=CVSET+2**12*RESET1+3*2**10+2**16*(BUILD1+6)+2**16*(fix+var)+r['claws']*(7+22+29+30)+len(r['goodpairs'])*STEP3B
    print(' counted ops %d (build %d) <= charge %.0f: %s'%(r['ops'],r['ops_build'],chg,r['ops']<=chg)); ok&= r['ops']<=chg
    # 7. the ledger
    tlog,N,sl,opc=ledger(show=False)
    print(' ledger time_log2 = %.5f, score %.5f, success >= %s'%(tlog,tlog+7.069,str(sl)[:12])); ok&= sl>=D('0.39')
    # 8. the seven-lane bucket machine: exact claws against an independent sorted search, distinct pairs, true row-16 passes
    cvb,_=cv_from_seed('selftest|bucket'); rb=run_bucket(cvb,13,b=9,aw=16,count=True,ref=True,collect_all=True)
    distb=len(set((a0,a1) for (a0,a1,u,fl) in rb['allclaws']))
    badb=sum(1 for (a0,a1,u,fl) in rb['allclaws'] if not r16ok(e16_real_p1(cvb,a0,a1)))
    print(' bucket: buckets=%d claws=%d ref=%d EQUAL=%s distinct=%d row16_bad=%d ops=%d'
          %(rb['buckets'],rb['claws'],rb['refclaws'],rb['claws']==rb['refclaws'],distb,badb,rb['ops']))
    ok&= rb['claws']==rb['refclaws'] and distb==rb['claws'] and badb==0 and rb['claws']>0
    # 9. the bucket ledger: the same premises, the bucket machine's per-u cost, success >= 0.39
    tb,Nb,slb=ledger_bucket(show=False)
    print(' bucket ledger time_log2 = %.5f, score %.5f, success >= %s'%(tb,tb+8.0114,str(slb)[:12]))
    ok&= slb>=D('0.39') and tb<83.0
    print('SELFTEST', 'PASS' if ok else 'FAIL'); return ok
def main():
    if len(sys.argv)>1 and sys.argv[1]=='selftest': sys.exit(0 if selftest() else 1)
    if len(sys.argv)>1 and sys.argv[1]=='ledger': ledger(); return
    if len(sys.argv)>1 and sys.argv[1]=='bucket-ledger': ledger_bucket(); return
    sys.stdout.write(json.dumps(run_request(json.load(sys.stdin))))
if __name__=='__main__': main()
