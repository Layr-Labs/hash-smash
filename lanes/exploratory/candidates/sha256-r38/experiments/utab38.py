if not __debug__:
    raise SystemExit('assertions required')
import sys,json,hashlib,struct,math,random,zlib,base64
from decimal import Decimal as D,getcontext
M=0xffffffff;NR=38
K=[0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,
     0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,
     0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,
     0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb]
IV=[0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19]
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
PQE=list(PQ); PQE[18]=0
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
T20=[(h-R16H[0])>>13 for h in R16H]
assert all((R16H[0]+(t<<13))&M==h for h,t in zip(R16H,T20)) and len(set(T20))==20
OFFS=(0,1,4,5,1024,1025,1028,1029)
T160=sorted(h+o for h in R16H for o in OFFS)
Cc2=0x7af32e15
QPF=(57726359870197/2**58)*(287309824/2**32)
ONES=(1<<256)-1
LANEPL=[sum(((l>>i)&1)<<l for l in range(256)) for i in range(8)]
AP=[(LANEPL[i],LANEPL[i]^ONES) for i in range(8)]
B2=(0,ONES)
SP_S0=[(((x>>0)&1)<<0)|(((x>>1)&1)<<4)|(((x>>2)&1)<<8)|(((x>>3)&1)<<11)|(((x>>4)&1)<<14)|(((x>>5)&1)<<17)|(((x>>10)&1)<<34)|(((x>>11)&1)<<39) for x in range(4096)]
SP_S10=[(((x>>0)&1)<<1)|(((x>>1)&1)<<5)|(((x>>7)&1)<<22)|(((x>>8)&1)<<26)|(((x>>9)&1)<<30)|(((x>>10)&1)<<35)|(((x>>11)&1)<<40) for x in range(4096)]
SP_S11=[x<<1 for x in SP_S10]
SP_K0=[(((x>>0)&1)<<3)|(((x>>1)&1)<<7)|(((x>>2)&1)<<9)|(((x>>3)&1)<<12)|(((x>>4)&1)<<15)|(((x>>5)&1)<<18)|(((x>>6)&1)<<20)|(((x>>7)&1)<<24)|(((x>>8)&1)<<28)|(((x>>9)&1)<<32)|(((x>>10)&1)<<37)|(((x>>11)&1)<<42)|(((x>>12)&1)<<44) for x in range(8192)]
SP_K1=[(((x>>2)&1)<<10)|(((x>>3)&1)<<13)|(((x>>4)&1)<<16)|(((x>>5)&1)<<19)|(((x>>6)&1)<<21)|(((x>>7)&1)<<25)|(((x>>8)&1)<<29)|(((x>>9)&1)<<33)|(((x>>10)&1)<<38)|(((x>>11)&1)<<43)|(((x>>12)&1)<<45) for x in range(8192)]
def cv_consts(cv):
    a,b,c,d,e,f,gg,h=cv
    k0=(-S0(a)-MAJ(a,b,c)-h-S1(e)-CH(e,f,gg)-K[0])&M
    E0base=(d-S0(a)-MAJ(a,b,c))&M
    PP=a&b; QQ=a|b; NAB=(~(a^b))&M; EF=e^f; FF=f; KF=(k0+Cc2-gg-K[1])&M; KFm=(KF-PP)&M; K2=(Cc2+k0)&M
    E=[]; c8=0
    for i in range(8):
        ai=LANEPL[i]; ei=(E0base>>i)&1
        if i==0: E.append((ai^ONES) if ei else ai); c8=ai if ei else 0
        elif ei: E.append(ai^c8^ONES); c8=ai|c8
        else: E.append(ai^c8); c8=ai&c8
    nc8=c8^ONES; G=(0,nc8,c8,ONES)
    EG=[(E[i],E[i]^nc8,E[i]^c8,E[i]^ONES) for i in range(8)]
    nab=(~(a^b))&255; U=[]; cu=0
    for i in range(8):
        xi=(LANEPL[i]^ONES) if (nab>>i)&1 else 0
        ei,fi=(e>>i)&1,(f>>i)&1
        yi=(ONES if ei else 0) if ei==fi else (E[i] if ei else (E[i]^ONES))
        t=xi^yi; U.append(t^cu); cu=(xi&yi)|(cu&t)
    U.append(cu)
    K_cv=(KF+(~QQ&255)-(PP&0x1F00)-5)&8191
    def _csa3(p,q,r): u=p^q; return ((p&q)|(u&r),u^r)
    T0=[]; T1=[]
    for idx in range(16):
        p,q,r,s=U[0],AP[2][idx&1],EG[6][(idx>>1)&3],B2[(idx>>3)&1]
        c1,s1=_csa3(p,q,r); cs=c1&s1; T0.append((s1^s,c1^(s1&s),cs&s))
        p,q,r,s=U[1],AP[3][idx&1],EG[7][(idx>>1)&3],B2[(idx>>3)&1]
        c1,s1=_csa3(p,q,r); T1.append((c1,s1,s1^ONES) if s else (c1,0,s1))
    CT=[T0,T1]
    for i in range(2,6): CT.append([_csa3(U[i],AP[i+2][idx&1],G[(idx>>1)&3]) for idx in range(8)])
    CT.append([(U[6]&G[idx],U[6]^G[idx]) for idx in range(4)])
    for i in (7,8): CT.append([_csa3(U[i],EG[i-7][idx&3],G[(idx>>2)&3]) for idx in range(16)])
    CT.append([(EG[2][idx&3]&G[(idx>>2)&3],EG[2][idx&3]^G[(idx>>2)&3]) for idx in range(16)])
    for i in (10,11): CT.append([_csa3(AP[i-10][idx&1],EG[i-7][(idx>>1)&3],G[(idx>>3)&3]) for idx in range(32)])
    CT.append([(LANEPL[2]^EG[5][idx],) for idx in range(4)])
    return dict(k0=k0,E0base=E0base,PP=PP,QQ=QQ,NAB=NAB,EF=EF,FF=FF,KF=KF,KFm=KFm,K2=K2,
                E0base_hi=E0base&~255,NAB_hi=(~(a^b))&0x1F00,FF_hi=f&0x1F00,EF_hi=EF&0x1F00,K_cv=K_cv,G=G,EG=EG,U=U,CT=CT)
def hfun(cv,a0):
    a,b,c,d,e,f,gg,h=cv; E0=(a0+d-S0(a)-MAJ(a,b,c))&M
    return (-S0(a0)-MAJ(a0,a,b)-gg-S1(E0)-CH(E0,e,f)-K[1])&M
def Ffun(cv,a0,co): return (a0+co['k0']+hfun(cv,a0)+Cc2)&M
def spair_claw_consts():
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
    A2,A3,A4,A5=SAx[2],SAx[3],SAx[4],SAx[5]; E6,E7,E8,E9=SE[6],SE[7],SE[8],SE[9]
    cE5=(A5-S0(A4)-MAJ(A4,A3,A2))&M; co0=cv_consts(cv); K2E5=(co0['K2']+cE5)&M; KNPHI=(0x60000000+K2E5-co0['KFm'])&M
    KW9=(E9-A5-S1(E8)-CH(E8,E7,E6)-K[9])&M; cW9=(KW9-cE5)&M
    cE4=(A4-S0(A3))&M; mA=A3&A2; mB=A3|A2; mX=A3^A2
    KW8=(E8-A4-S1(E7)-K[8])&M; cW8=(KW8-cE4)&M; cA=E7&E6; cB=~E7&M
    cW8f=(cW8+mA-cA)&M; cE4f=(cE4-mA)&M
    KK7c=(E7-2*A3-cv[0]+S0(A2)-S1(E6)-K[7])&M
    D7c=(_ty[1][7]-_tx[1][7])&M
    return dict(cE5=cE5,K2E5=K2E5,KNPHI=KNPHI,KW9=KW9,cW9=cW9,cE4=cE4,cE4f=cE4f,mA=mA,mB=mB,mX=mX,KW8=KW8,cW8=cW8,cW8f=cW8f,cA=cA,cB=cB,A2=A2,E6=E6,KK7c=KK7c,D7c=D7c)
PF_C2=16; PF_G=24; PF_F7=28
def postfilters(m,cv,a0,u,F,pf):
    E5=((u-F)+pf['K2E5']+a0)&M; m.op(3)
    m.br(); m.op(1)
    if (E5&0xE0000000)!=0xA0000000: return 0,0,0,0
    return (1,)+pf_tail(m,a0,E5,pf)
def pf_tail(m,a0,E5,pf):
    s2=s3=s4=0
    w9=(pf['KW9']-E5)&M; s9=s0(w9); m.op(1+8)
    m.op(1); m.br()
    ok2=((s9&0x04400800)==0x00000800) if (w9&0x20000000) else ((s9&0x0cc01800)==0x04401000)
    m.op(1); m.br(); m.op(1)
    if ok2:
        s2=1
        a1=(E5-pf['cE5'])&M; E40=(a0-(a1&pf['mX']))&M; w8=(pf['cW8f']-E40-(pf['cB']&E5))&M; m.op(6)
        s8=s0(w8); z8=(s8&0x07818000)|((w8>>5)&0x006600c0); m.op(8+4)
        m.op(1); m.br()
        if (z8&0x02a28040)==0x02220000: ok3=True; m.op(1)
        else:
            m.br(); m.op(1)
            ok3=(z8==0x04c48040)
        if ok3:
            s3=1
            E4=(E40+pf['cE4f'])&M; maj2=MAJ(pf['A2'],a1,a0); ch2=CH(pf['E6'],E5,E4); w7=((pf['KK7c']+maj2)-ch2)&M; m.op(1+4+3+2)
            s7=s0(w7); m.op(8)
            m.op(1); m.br()
            if (w7&0x20000000)==0:
                m.op(1); m.br(); m.op(1)
                if (s7&0x04400800)==0x00400800: s4=1
            else:
                m.op(1); m.br()
                ok4=((s7&0x0cc01800)==0x04801000) if (w7&0x40000000)==0 else ((s7&0x1dc03800)==0x0d002000)
                m.op(1); m.br(); m.op(1)
                if ok4: s4=1
    return s2,s3,s4
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
NCOL=12; ROWB=19; RMASK=(1<<ROWB)-1; LANES=6; STR=42; FLD=33; CNT=252; EMPTYT=22; KEP=16
def lanes_const(v): return sum(v<<(STR*L+FLD) for L in range(LANES))
EMPTYW=lanes_const(EMPTYT); MASKW=lanes_const(0b011010); W8L=lanes_const(8); CMAIN=0; CSTR=W8L
KW=lanes_const(31); GW=lanes_const(32)
W9=9<<26; QPF=(57726359870197/2**58)*(287309824/2**32)
U_BASE=17; U_INS=22; U_DROP=9; RESET=5; A0_BASE=35; A0_RES=7; SETUP=14; ROWJ=2; XCROSS=0; READ=9; WALK=12
EXTRACT=2; CVSET=70; FBCTL=6; EPSET=6; STEP3B=3014
LAMSET=12; READC1=8; C1PRE=2
S0_LO=[S0(l) for l in range(256)]
LOG2_16={1<<i:i for i in range(16)}
GW_LO=sum(32<<(STR*L+FLD) for L in range(3)); G_L=[32<<(STR*L+FLD) for L in range(LANES)]
WALK_THRESHOLDS=[452312848583369232408156758951848022920192403265678406657081215671343251456, 452312848583369232408156758951848022925509315248816861222876829283289923584, 452312848583369232408156758951848022925509315248818070148696443637586722816, 452312848583369232408156758951848022925509315248816861222876829008412016640, 452312848583266388373324183574213337351599480842256649157094345171005341696, 452312848583369232408156735567821825631062623989860746688168129417543942144, 452312848583369232408156758951848022920192403265677197731261600767290638336, 452312848583369232408156758951848022920192403265678406657081215396465344512, 452312848583369232408156758951848022920192403265677197731261601042168545280, 452312848583369232408156735567821825625745712006719874270733286272369950720, 452312848583369232408156735567821825631062623989859537762348514513491329024, 452312848583369232408156735567821825631062623989860746688168129142666035200, 452312848583369232408156735567821825631062623989859537762348514788369235968, 452312848583369232408156735567821825625745712006721083196552900901544656896, 452312848583369232408156735567821825625745712006721083196552901176422563840, 452312848583369232408156735567821825625745712006719874270733286547247857664, 102844034832598761660882873673437648659616869565256381553967104, 452312848583266388373324160190187140051835877600158453279131187530910662656, 452312848583266388373324183574213337346282568859116985665479116929883963392, 452312848583266388373324183574213337351599480842255440231274730541830635520, 452312848583266388373324183574213337351599480842256649157094344896127434752, 452312848583266388373324183574213337351599480842255440231274730266952728576, 452312848583266388373324160190187140057152789583299325696566030401206747136, 452312848583266388373324183574213337346282568859115776739659502025831350272, 452312848583266388373324183574213337346282568859116985665479116655006056448, 452312848583266388373324183574213337346282568859115776739659502300709257216, 452312848583266388373324160190187140057152789583299325696566030676084654080, 452312848583266388373324160190187140051835877600159662204950802434963275776, 452312848583266388373324160190187140057152789583298116770746416046909947904, 452312848583266388373324160190187140057152789583298116770746415772032040960, 452312848583266388373324160190187140051835877600159662204950802160085368832, 452312848583266388373324160190187140051835877600158453279131187805788569600, 102844034832575377634685573909834406561420991602098741459288064, 102844034832598761660882868356525665519953377950028140432588800, 102844034832598761660882873673437648658407943745641752379260928, 102844034832598761660882873673437648659616869565256106676060160, 102844034832598761660882873673437648658407943745641477501353984, 102844034832575377634685579226746389702293409036941611755372544, 102844034832598761660882868356525665518744452130413236379975680, 102844034832598761660882868356525665519953377950027865554681856, 102844034832598761660882868356525665518744452130413511257882624, 102844034832575377634685579226746389702293409036941886633279488, 102844034832575377634685573909834406562629917421713645511901184, 102844034832575377634685579226746389701084483217327257458573312, 102844034832575377634685579226746389701084483217326982580666368, 102844034832575377634685573909834406562629917421713370633994240, 102844034832575377634685573909834406561420991602099016337195008, 23384026197294446691258957323460528314494920687616, 23384026197299763603242096986952143542736042065920, 23384026197299763603242098195877963157365216772096, 23384026197299763603242098195877963157640094679040, 23384026197299763603242096986952143543010919972864, 23384026197294446691258958532386347929124095393792, 23384026197294446691258958532386347929398973300736, 23384026197294446691258957323460528314769798594560, 5316911983139663491615228241121378304, 5316911983140872417434842870296084480, 5316911983140872417434843145173991424, 5316911983139663491615228515999285248, 1208925819614629174706176, 1208925819614904052613120, 274877906944]
def walk_lanes(z,m=None):
 if m:m.br()
 if z>=WALK_THRESHOLDS[0]:
  if m:m.br()
  if z>=WALK_THRESHOLDS[1]:
   if m:m.br()
   if z>=WALK_THRESHOLDS[2]:
    return [0]
   else:
    return [1]
  else:
   if m:m.br()
   if z>=WALK_THRESHOLDS[3]:
    return [0, 1]
   else:
    return [2]
 else:
  if m:m.br()
  if z>=WALK_THRESHOLDS[4]:
   if m:m.br()
   if z>=WALK_THRESHOLDS[5]:
    if m:m.br()
    if z>=WALK_THRESHOLDS[6]:
     if m:m.br()
     if z>=WALK_THRESHOLDS[7]:
      return [0, 2]
     else:
      if m:m.br()
      if z>=WALK_THRESHOLDS[8]:
       return [1, 2]
      else:
       return [0, 1, 2]
    else:
     return [3]
   else:
    if m:m.br()
    if z>=WALK_THRESHOLDS[9]:
     if m:m.br()
     if z>=WALK_THRESHOLDS[10]:
      if m:m.br()
      if z>=WALK_THRESHOLDS[11]:
       return [0, 3]
      else:
       if m:m.br()
       if z>=WALK_THRESHOLDS[12]:
        return [1, 3]
       else:
        return [0, 1, 3]
     else:
      if m:m.br()
      if z>=WALK_THRESHOLDS[13]:
       if m:m.br()
       if z>=WALK_THRESHOLDS[14]:
        return [2, 3]
       else:
        return [0, 2, 3]
      else:
       if m:m.br()
       if z>=WALK_THRESHOLDS[15]:
        return [1, 2, 3]
       else:
        return [0, 1, 2, 3]
    else:
     return [4]
  else:
   if m:m.br()
   if z>=WALK_THRESHOLDS[16]:
    if m:m.br()
    if z>=WALK_THRESHOLDS[17]:
     if m:m.br()
     if z>=WALK_THRESHOLDS[18]:
      if m:m.br()
      if z>=WALK_THRESHOLDS[19]:
       if m:m.br()
       if z>=WALK_THRESHOLDS[20]:
        return [0, 4]
       else:
        return [1, 4]
      else:
       if m:m.br()
       if z>=WALK_THRESHOLDS[21]:
        return [0, 1, 4]
       else:
        return [2, 4]
     else:
      if m:m.br()
      if z>=WALK_THRESHOLDS[22]:
       if m:m.br()
       if z>=WALK_THRESHOLDS[23]:
        if m:m.br()
        if z>=WALK_THRESHOLDS[24]:
         return [0, 2, 4]
        else:
         if m:m.br()
         if z>=WALK_THRESHOLDS[25]:
          return [1, 2, 4]
         else:
          return [0, 1, 2, 4]
       else:
        if m:m.br()
        if z>=WALK_THRESHOLDS[26]:
         return [3, 4]
        else:
         return [0, 3, 4]
      else:
       if m:m.br()
       if z>=WALK_THRESHOLDS[27]:
        if m:m.br()
        if z>=WALK_THRESHOLDS[28]:
         return [1, 3, 4]
        else:
         if m:m.br()
         if z>=WALK_THRESHOLDS[29]:
          return [0, 1, 3, 4]
         else:
          return [2, 3, 4]
       else:
        if m:m.br()
        if z>=WALK_THRESHOLDS[30]:
         return [0, 2, 3, 4]
        else:
         if m:m.br()
         if z>=WALK_THRESHOLDS[31]:
          return [1, 2, 3, 4]
         else:
          return [0, 1, 2, 3, 4]
    else:
     return [5]
   else:
    if m:m.br()
    if z>=WALK_THRESHOLDS[32]:
     if m:m.br()
     if z>=WALK_THRESHOLDS[33]:
      if m:m.br()
      if z>=WALK_THRESHOLDS[34]:
       if m:m.br()
       if z>=WALK_THRESHOLDS[35]:
        return [0, 5]
       else:
        return [1, 5]
      else:
       if m:m.br()
       if z>=WALK_THRESHOLDS[36]:
        return [0, 1, 5]
       else:
        return [2, 5]
     else:
      if m:m.br()
      if z>=WALK_THRESHOLDS[37]:
       if m:m.br()
       if z>=WALK_THRESHOLDS[38]:
        if m:m.br()
        if z>=WALK_THRESHOLDS[39]:
         return [0, 2, 5]
        else:
         if m:m.br()
         if z>=WALK_THRESHOLDS[40]:
          return [1, 2, 5]
         else:
          return [0, 1, 2, 5]
       else:
        if m:m.br()
        if z>=WALK_THRESHOLDS[41]:
         return [3, 5]
        else:
         return [0, 3, 5]
      else:
       if m:m.br()
       if z>=WALK_THRESHOLDS[42]:
        if m:m.br()
        if z>=WALK_THRESHOLDS[43]:
         return [1, 3, 5]
        else:
         if m:m.br()
         if z>=WALK_THRESHOLDS[44]:
          return [0, 1, 3, 5]
         else:
          return [2, 3, 5]
       else:
        if m:m.br()
        if z>=WALK_THRESHOLDS[45]:
         return [0, 2, 3, 5]
        else:
         if m:m.br()
         if z>=WALK_THRESHOLDS[46]:
          return [1, 2, 3, 5]
         else:
          return [0, 1, 2, 3, 5]
    else:
     if m:m.br()
     if z>=WALK_THRESHOLDS[47]:
      if m:m.br()
      if z>=WALK_THRESHOLDS[48]:
       if m:m.br()
       if z>=WALK_THRESHOLDS[49]:
        if m:m.br()
        if z>=WALK_THRESHOLDS[50]:
         return [4, 5]
        else:
         return [0, 4, 5]
       else:
        if m:m.br()
        if z>=WALK_THRESHOLDS[51]:
         return [1, 4, 5]
        else:
         return [0, 1, 4, 5]
      else:
       if m:m.br()
       if z>=WALK_THRESHOLDS[52]:
        if m:m.br()
        if z>=WALK_THRESHOLDS[53]:
         return [2, 4, 5]
        else:
         return [0, 2, 4, 5]
       else:
        if m:m.br()
        if z>=WALK_THRESHOLDS[54]:
         return [1, 2, 4, 5]
        else:
         return [0, 1, 2, 4, 5]
     else:
      if m:m.br()
      if z>=WALK_THRESHOLDS[55]:
       if m:m.br()
       if z>=WALK_THRESHOLDS[56]:
        if m:m.br()
        if z>=WALK_THRESHOLDS[57]:
         return [3, 4, 5]
        else:
         return [0, 3, 4, 5]
       else:
        if m:m.br()
        if z>=WALK_THRESHOLDS[58]:
         return [1, 3, 4, 5]
        else:
         return [0, 1, 3, 4, 5]
      else:
       if m:m.br()
       if z>=WALK_THRESHOLDS[59]:
        if m:m.br()
        if z>=WALK_THRESHOLDS[60]:
         return [2, 3, 4, 5]
        else:
         return [0, 2, 3, 4, 5]
       else:
        if m:m.br()
        if z>=WALK_THRESHOLDS[61]:
         return [1, 2, 3, 4, 5]
        else:
         return [0, 1, 2, 3, 4, 5]
WALK_LANE_WEIGHTS=(6,6,6,8,8,8)
WALK_INIT=1<<24
def walk_certificate():
    worst=0;bad=0
    for mask in range(1,64):
        z=GW-sum(G_L[j] for j in range(6) if mask>>j&1);meter=Mach();got=walk_lanes(z,meter)
        want=[j for j in range(6) if mask>>j&1]
        bad+=got!=want or meter.ops>sum(WALK_LANE_WEIGHTS[j] for j in want)
        worst=max(worst,meter.ops)
    prefix=max(D(sum(WALK_LANE_WEIGHTS[:p]))/p for p in range(1,7))
    if bad or worst!=18 or prefix!=7:raise ValueError('ordered lane tree certificate')
    return dict(tree_masks=63,tree_mismatches=bad,tree_max_read_ops=worst,tree_mean_claw_bound=int(prefix),tree_max_claw_bound=max(WALK_LANE_WEIGHTS))
_WALK_CERT=walk_certificate()
WALK_PROVEN=D(_WALK_CERT['tree_mean_claw_bound']);WALK_MEAN=D('6.770000');WALK_MAX_READ=_WALK_CERT['tree_max_read_ops'];WALK_MAX_CLAW=_WALK_CERT['tree_max_claw_bound']
STEP3B_MEAN=D('842.361097')
def P(u): return (s0(u)-u)&M
def build_table(r,ustart,U,m=None,ncol=NCOL):
    tab={}; ent=drop=0; cov=8*ncol
    if m: m.op(EPSET)
    for n in range(U):
        u=(ustart+n)&M; g=(P(u)-r)&M; lo=g&8191
        if m: m.op(15); m.br()
        if lo>=cov: continue
        k=((lo>>3)<<ROWB)|(g>>13); d=tab.get(k,EMPTYW); c=d>>CNT
        if m: m.op(4); m.ld(); m.op(1); m.br()
        if c>=LANES: drop+=1; continue
        sh=STR*c; lane=u|((g&7)<<FLD)
        if m: m.op(3); m.ld(); m.ld(); m.op(4); m.st()
        d=(d&~(EMPTYT<<(sh+FLD)))|(lane<<sh); d+=1<<CNT; tab[k]=d; ent+=1
    return tab,ent,drop
def table_entries(tab):
    for k,d in tab.items():
        col=k>>ROWB; row=k&RMASK
        for L in range(d>>CNT):
            ln=d>>(STR*L); yield ((row<<13)|(col<<3)|((ln>>FLD)&7))&M, ln&M
def probe_word(d,WB,C=0):
    return (((d+WB+C)&MASKW)+KW)&GW
def lanes_at(v,pos): return sum(v<<(STR*L+pos) for L in range(LANES))
T3W=lanes_at(7<<29,0); G32W=lanes_at(1<<32,0)
MT3W=MASKW|T3W; KT3W=KW|G32W|T3W; CMAIN1=0; CSTR1=W8L
def wbl(w,PHI,c1=0):
    nphi=(0x60000000-PHI)&M; lv=nphi|((32-w)<<FLD)
    b=lv|(lv<<STR); b|=b<<(2*STR); WBL0=b|((b<<(4*STR))&ONES)
    return (WBL0+c1) if c1 else WBL0
def probe_word_c1(d,WBL,C1=0):
    return (((d+(WBL+C1 if C1 else WBL))&MT3W)+KT3W)&GW
GATE2=4; GATE1=3; BATCH=8; EXTRACT_BS=20; A0_PROBE=21; CV_BS=1024; GBS=218
class Planes:
    def __init__(self,m): self.m=m; self.g=0
    def x(self,a,b): self.g+=GATE2; return a^b
    def a(self,a,b): self.g+=GATE2; return a&b
    def o(self,a,b): self.g+=GATE2; return a|b
    def n(self,a): self.g+=GATE1; return a^ONES
def bs_mask(co,cv,Hr,base,pl,ncol=NCOL):
    A=list(LANEPL)
    for i in range(8,32): A.append(ONES if (base>>i)&1 else 0); pl.g+=GATE2
    e=co['E0base']; E=[0]*32; c=0
    for i in range(32):
        ei=(e>>i)&1
        if i==0: E[0]=pl.n(A[0]) if ei else A[0]; c=A[0] if ei else 0; continue
        if ei: E[i]=pl.n(pl.x(A[i],c)); cn=pl.o(A[i],c)
        else: E[i]=pl.x(A[i],c); cn=pl.a(A[i],c)
        c=cn
    def sig(X,r1,r2,r3): return [pl.x(pl.x(X[(i+r1)%32],X[(i+r2)%32]),X[(i+r3)%32]) for i in range(13)]
    S0p=sig(A,2,13,22); S1p=sig(E,6,11,25)
    a,b,ee,ff=cv[0],cv[1],cv[4],cv[5]; MJ=[]; CHp=[]
    for i in range(13):
        ai,bi,ei,fi=(a>>i)&1,(b>>i)&1,(ee>>i)&1,(ff>>i)&1
        MJ.append((ONES if ai else 0) if ai==bi else A[i])
        CHp.append((ONES if ei else 0) if ei==fi else (E[i] if ei else pl.n(E[i])))
    def neg(X): return [(x^ONES) if x in (0,ONES) else pl.n(x) for x in X]
    konst=(co['KF']+4)&8191
    terms=[A[:13],neg(S0p),neg(MJ),neg(S1p),neg(CHp),[(ONES if (konst>>i)&1 else 0) for i in range(13)]]
    while len(terms)>2:
        X,Y,Z=terms.pop(),terms.pop(),terms.pop(); S=[]; Cc=[0]
        for i in range(13):
            t=pl.x(X[i],Y[i]); S.append(pl.x(t,Z[i])); Cc.append(pl.o(pl.a(X[i],Y[i]),pl.a(Z[i],t)))
        terms+=[S,Cc[:13]]
    X,Y=terms; F=[]; c=0
    for i in range(13):
        t=pl.x(X[i],Y[i]); F.append(pl.x(t,c)); c=pl.o(pl.a(X[i],Y[i]),pl.a(c,t))
    k=(Hr+5+1)&8191; X=[pl.n(f) for f in F]; T=[]; c=0
    for i in range(13):
        if (k>>i)&1: T.append(pl.n(pl.x(X[i],c))); c=pl.o(X[i],c)
        else: T.append(pl.x(X[i],c)); c=pl.a(X[i],c)
    lim=8*ncol+5; lt=0; eq=ONES
    for i in range(9,-1,-1):
        if (lim>>i)&1: lt=pl.o(lt,pl.a(eq,pl.n(T[i]))); eq=pl.a(eq,T[i])
        else: eq=pl.a(eq,pl.n(T[i]))
    same=pl.n(pl.o(pl.x(T[10],T[11]),pl.x(T[11],T[12])))
    return pl.a(lt,same)
class RM:
    def __init__(self,nreg=16): self.ops=0; self.loads=0; self.stores=0; self.gates=0; self.live={}; self.nreg=nreg; self.peak=0
    def _chk(self):
        self.peak=max(self.peak,len(self.live)); assert len(self.live)<=self.nreg,len(self.live)
    def load(self,name,val): self.ops+=1; self.loads+=1; self.live[name]=val; self._chk(); return name
    def free(self,*names):
        for n in names: self.live.pop(n,None)
    def store(self,name): self.ops+=1; self.stores+=1; v=self.live.pop(name); return v
    def g(self,out,f,*ins):
        self.ops+=1; self.gates+=1; v=f(*[self.live[i] for i in ins]); self.live[out]=v; self._chk(); return out
def bs_mask_rm(co,cv,Hr,base,rm,ncol=NCOL):
    X=lambda a,b:a^b; A_=lambda a,b:a&b; O=lambda a,b:a|b; N=lambda a:a^ONES
    s0_b=S0(base)
    e_hi0=(base+co['E0base_hi'])&M; e_hi1=(e_hi0+256)&M
    s1_0=S1(e_hi0); s1_1=S1(e_hi1)
    ch_0=co['FF_hi']^(e_hi0&co['EF_hi']); ch_1=co['FF_hi']^(e_hi1&co['EF_hi'])
    k_base=Hr-co['K_cv']-(base&co['NAB_hi'])+(s0_b&0x13C0)
    k0=(k_base+(s1_0&0x107C)+ch_0)&8191; k1=(k_base+(s1_1&0x107C)+ch_1)&8191
    w_idx=SP_S0[s0_b&4095]|SP_S10[s1_0&4095]|SP_S11[s1_1&4095]|SP_K0[k0]|SP_K1[k1]
    rm.ops+=60
    CT=co['CT']; lim=8*ncol+5
    def ld_col(i,sh,msk,names):
        idx=(w_idx&msk) if sh==0 else ((w_idx>>sh) if msk==0 else ((w_idx>>sh)&msk))
        rm.ops+=(1 if (sh==0 or msk==0) else 2)+len(names)
        for nm,val in zip(names,CT[i][idx]): rm.load(nm,val)
    def csa(p,q,r,cout,sout):
        rm.g('v',A_,p,q); rm.g('u',X,p,q); rm.free(p,q); rm.g('w',A_,r,'u'); rm.g(sout,X,'u',r); rm.free('u',r)
        rm.g(cout,O,'v','w'); rm.free('v','w')
    def ha(p,q,cout,sout):
        rm.g(cout,A_,p,q); rm.g(sout,X,p,q); rm.free(p,q)
    ld_col(0,0,15,('ge','c1_0','c2_0'))
    ld_col(1,4,15,('c1','c2','s1'))
    ha('s1','c1_0','c3','t'); rm.g('c3',O,'c3','c2_0'); rm.free('c2_0')
    rm.g('ge',A_ if (lim>>1)&1 else O,'t','ge'); rm.free('t')
    for i,sh in ((2,8),(3,11),(4,14),(5,17)):
        ld_col(i,sh,7,('c1n','s1'))
        csa('s1','c1','c2','c2n','s2'); ha('s2','c3','c3n','t')
        rm.live['c1']=rm.live.pop('c1n'); rm.live['c2']=rm.live.pop('c2n'); rm.live['c3']=rm.live.pop('c3n')
        rm.g('ge',A_ if (lim>>i)&1 else O,'t','ge'); rm.free('t')
    csa('c1','c2','c3','c1n','s1')
    ld_col(6,20,3,('v','u'))
    rm.g('w',A_,'s1','u'); rm.g('t',X,'s1','u'); rm.free('s1','u'); rm.g('c2',O,'v','w'); rm.free('v','w')
    rm.live['c1']=rm.live.pop('c1n')
    rm.g('ge',A_ if (lim>>6)&1 else O,'t','ge'); rm.free('t')
    for i,sh in ((7,22),(8,26)):
        ld_col(i,sh,15,('c1n','s1'))
        csa('s1','c1','c2','c2n','t')
        rm.live['c1']=rm.live.pop('c1n'); rm.live['c2']=rm.live.pop('c2n')
        rm.g('ge',A_ if (lim>>i)&1 else O,'t','ge'); rm.free('t')
    ld_col(9,30,15,('v','u'))
    rm.g('w',A_,'c1','u'); rm.g('s1',X,'c1','u'); rm.free('c1','u'); rm.g('c1',O,'v','w'); rm.free('v','w')
    ha('s1','c2','c2n','t'); rm.live['c2']=rm.live.pop('c2n')
    rm.g('ge',A_ if (lim>>9)&1 else O,'t','ge'); rm.free('t')
    for i,sh in ((10,34),(11,39)):
        ld_col(i,sh,31,('c1n','s1'))
        csa('s1','c1','c2','c2n','T%d'%i)
        rm.live['c1']=rm.live.pop('c1n'); rm.live['c2']=rm.live.pop('c2n')
    ld_col(12,44,0,('t0',))
    rm.g('t0',X,'t0','c1'); rm.g('T12',X,'t0','c2'); rm.free('t0','c1','c2')
    rm.g('u',X,'T10','T11'); rm.g('v',X,'T11','T12'); rm.g('u',O,'u','v'); rm.g('u',O,'u','ge'); rm.g('m',N,'u')
    return rm.live['m']
def gbs_worst():
    cv=[0,M,0,0,M,0,0,0]; co=cv_consts(cv); rm=RM()
    bs_mask_rm(co,cv,(8191-6)&M,W9,rm); return rm.ops
def bs_check(seed,nb=16):
    cv,_=cv_from_seed(seed); co=cv_consts(cv); sh=Shake(seed+'|bs'); r=sh.word()&8191; Hr=(R16H[0]-r)&M; bad=n=gmax=0
    for k in range(nb):
        base=W9+((sh.word()&((1<<26)-1))&~255); rm=RM(); mask=bs_mask_rm(co,cv,Hr,base,rm); gmax=max(gmax,rm.ops)
        bad+=bin(mask^bs_mask(co,cv,Hr,base,Planes(None))).count('1')
        for l in range(256):
            t=((Hr-Ffun(cv,base+l,co))+5)&8191; want=t<8*NCOL+5 or 7168<=t<7168+8*NCOL+5
            bad+=int(want!=bool((mask>>l)&1)); n+=int(want)
    return dict(bs_batches=nb,bs_probing_lanes=n,bs_mismatches=bad,bs_gates_max=gmax,bs_gate_bound=GBS)
def scan_cv(cv,tab,r,a0s,m=None,ncol=NCOL,collect=None,bs=True,collect_all=None):
    co=cv_consts(cv); pf=pf_consts(cv); Hr=(R16H[0]-r)&M; cov=8*ncol; dense=cov+5>1024
    st=dict(a0=0,probes=0,reads=0,fired=0,claws=0,claws_all=0,passes=[0,0,0,0],good=[],coll=[],batches=0,gates=0)
    mm=m or Mach()
    def probe(a0,F,y,win):
        if not dense:
            yp=(y+1029)&M; rowb=yp>>13; u0=(yp&127)+3; w=u0&7; c1=u0>>3; c=c1-1
        else:
            yw=(y+(win<<10))&M; rowb=yw>>13; c=(yw>>3)&1023; w=yw&7; c1=c+1
        WB=lanes_const(32-w)
        PHI=(F-a0-pf['K2E5'])&M; WBL0=wbl(w,PHI); WBL1=WBL0+W8L
        if m: m.op(SETUP+LAMSET)
        st['probes']+=1
        for j in range(20):
            rowj=(rowb+T20[j])&RMASK
            if m and j: m.op(ROWJ)
            rd=[]
            if 0<=c<ncol: rd.append((c,rowj,CMAIN,WBL0))
            if w>=3:
                if c1<ncol: rd.append((c1,rowj,CSTR,WBL1))
                elif dense and c==1023: rd.append((0,(rowj+1)&RMASK,CSTR,WBL1))
            for (cc,rr,C,WBL) in rd:
                d=tab.get((cc<<ROWB)|rr,EMPTYW); st['reads']+=1
                z0=probe_word(d,WB,C)
                for L in range(LANES):
                    if not (z0>>(STR*L+FLD+5))&1:
                        st['claws_all']+=1
                        if collect_all is not None: collect_all.append((a0,(d>>(STR*L))&M,F,j,win))
                s=d+WBL; z=((s&MT3W)+KT3W)&GW
                if m: m.ld(); m.op(4); m.br()
                if z==GW: continue
                st['fired']+=1
                for L in walk_lanes(z,m):
                    u=(d>>(STR*L))&M; st['claws']+=1
                    E5=((s>>(STR*L))&M)|0xA0000000
                    if m: m.op(C1PRE)
                    fl=(1,)+pf_tail(mm,a0,E5,pf)
                    for i in range(4): st['passes'][i]+=fl[i]
                    if collect is not None: collect.append((a0,u,F,fl,j,win))
                    if fl[3]:
                        a1=(u-hfun(cv,a0))&M; st['good'].append((a0,a1,u))
                        ok,wx,wy=step3b(mm,cv,a0,a1)
                        if ok: st['coll'].append((a0,a1,u,wx,wy))
    if bs and not dense:
        if m: m.op(CV_BS)
        a0s=list(a0s); assert len(a0s)%256==0
        bases=a0s[::256]; assert all(b%256==0 and a0s[i*256:(i+1)*256]==list(range(b,b+256)) for i,b in enumerate(bases))
        for base in bases:
            rm=RM(); mask=bs_mask_rm(co,cv,Hr,base,rm,ncol); st['batches']+=1; st['gates']+=rm.ops; st['a0']+=256
            if m: m.op(rm.ops+BATCH+SBLOOP); m.br()
            s0b=S0(base); Hrp0=(Hr-co['KFm'])&M
            while mask:
                low=mask&-mask; mask^=low; l=low.bit_length()-1; a0=base|l
                e0=(a0+co['E0base'])&M; ch0=co['FF']^(co['EF']&e0); s0a=s0b^S0_LO[l]
                F0=((a0&co['NAB'])-s0a-S1(e0)-ch0)&M; y=(Hrp0-F0)&M; F=(F0+co['KFm'])&M; win=((y+5)>>10)&1
                if m: m.op(EXTRACT_BS+A0_PROBE)
                probe(a0,F,y,win)
        return st
    for a0 in a0s:
        F=Ffun(cv,a0,co); y=(Hr-F)&M; st['a0']+=1
        if m: m.op(4+26+1)
        if dense: wins=(0,1)
        else:
            q=(y+5)&1023
            if m: m.op(2); m.br()
            if q>=cov+5: continue
            v=((y+5)>>10)&7
            if m: m.op(3); m.br(); m.br()
            if v==0: wins=(0,)
            elif v==7: wins=(1,)
            else: continue
        for win in wins: probe(a0,F,y,win)
    return st
def ref_claws(cv,tab,r,a0s):
    co=cv_consts(cv); Hr=(R16H[0]-r)&M; lo={}; out=[]
    for G,u in table_entries(tab): lo.setdefault(G&8191,[]).append((G,u))
    for a0 in a0s:
        y=(Hr-Ffun(cv,a0,co))&M
        for o in OFFS:
            for (G,u) in lo.get((y+o)&8191,()):
                if (((G-y-o)&M)>>13) in T20S: out.append((a0,u))
    return out
T20S=set(T20)
class Shake:
    def __init__(self,label): self.buf=b''; self.n=0; self.lab=label.encode()
    def word(self):
        if not self.buf: self.buf=hashlib.shake_256(self.lab+struct.pack('<I',self.n)).digest(256); self.n+=1
        w=struct.unpack('<I',self.buf[:4])[0]; self.buf=self.buf[4:]; return w
def cv_from_seed(seed):
    sh=Shake(seed)
    for _ in range(CLS_TRY):
        M0=[sh.word() for _ in range(16)]; cv=compress(IV,M0)
        if kept(cv): return cv,M0
    raise RuntimeError('no kept chaining value')
def spair_obs():
    m=Mach(); ok,wx,wy=step3b(m,PCV,SAx[0],SAx[1])
    return dict(step3b_P8_pair_ok=int(ok and wx==PMX and wy==PMY),step3b_P8_pair_ops=m.ops)
def probe_exhaustive():
    sh=Shake('probe|exhaustive'); bad=n=0
    for kind,C in ((0,CMAIN),(1,CSTR)):
        for w in range(8):
            WB=lanes_const(32-w)
            for rep in range(24):
                tags=[(rep*5+L*3+w)%9 for L in range(LANES)]; tags=[EMPTYT if t==8 else t for t in tags]
                d=sum(((sh.word()|(t<<FLD))<<(STR*L)) for L,t in enumerate(tags))|((rep%7)<<CNT)
                z=probe_word(d,WB,C)
                for L,t in enumerate(tags):
                    fired=not (z>>(STR*L+FLD+5))&1
                    want=t!=EMPTYT and ((t-w) in (0,1,4,5) if kind==0 else (t+8-w) in (0,1,4,5))
                    bad+=int(fired!=want); n+=1
    return n,bad
C1EDGE=(0,1,2,(1<<29)-2,(1<<29)-1,1<<29,(1<<29)+1,(1<<30)-1,1<<30,M-1,M,0xA0000000,0x9fffffff,0xbfffffff,0xc0000000)
def probe_c1_exhaustive():
    sh=Shake('probe|c1'); bad=n=npass=0
    phis=(0,1,2,M,M-1,0x60000000,0x5fffffff,0x80000000)
    for kind in (0,1):
        for w in range(8):
            for rep in range(24):
                PHI=phis[rep] if rep<len(phis) else sh.word(); WBL=wbl(w,PHI)+(W8L if kind else 0)
                tags=[(rep*5+L*3+w)%9 for L in range(LANES)]; tags=[EMPTYT if t==8 else t for t in tags]
                us=[]
                for L in range(LANES):
                    k=sh.word()%4
                    if k==0: us.append(sh.word())
                    elif k==1: us.append((PHI+0xA0000000+sh.word()%(1<<29))&M)
                    else: us.append((PHI+C1EDGE[sh.word()%len(C1EDGE)])&M)
                d=sum(((u|(t<<FLD))<<(STR*L)) for L,(u,t) in enumerate(zip(us,tags)))|((rep%7)<<CNT)
                z=probe_word_c1(d,WBL)
                for L,(u,t) in enumerate(zip(us,tags)):
                    fired=not (z>>(STR*L+FLD+5))&1
                    want=t!=EMPTYT and ((t-w) in (0,1,4,5) if kind==0 else (t+8-w) in (0,1,4,5)) and (((u-PHI)&M)>>29)==5
                    bad+=int(fired!=want); n+=1; npass+=int(want)
    i=0
    for kind in (0,1):
        for w in range(8):
            for t in list(range(8))+[EMPTYT]:
                for v in range(8):
                    for hi in (0,1):
                        PHI=sh.word()%((7-v)*(1<<29)+1) if hi else M-sh.word()%(1<<28)
                        while True:
                            u=(PHI+(v<<29)+(sh.word()&((1<<29)-1)))&M
                            if int(u>=PHI)==hi: break
                        WBL=wbl(w,PHI)+(W8L if kind else 0)
                        P0=i%LANES; us=[sh.word() for _ in range(LANES)]; ts=[sh.word()%9 for _ in range(LANES)]
                        ts=[EMPTYT if x==8 else x for x in ts]; us[P0]=u; ts[P0]=t; i+=1
                        d=sum(((uu|(tt<<FLD))<<(STR*L)) for L,(uu,tt) in enumerate(zip(us,ts)))|((i%7)<<CNT)
                        z=probe_word_c1(d,WBL)
                        for L,(uu,tt) in enumerate(zip(us,ts)):
                            fired=not (z>>(STR*L+FLD+5))&1
                            want=tt!=EMPTYT and ((tt-w) in (0,1,4,5) if kind==0 else (tt+8-w) in (0,1,4,5)) and (((uu-PHI)&M)>>29)==5
                            bad+=int(fired!=want); n+=1; npass+=int(want)
    return n,bad,npass
def c1_of(cv,a0,u): return pf_ref(cv,a0,(u-hfun(cv,a0))&M)[0]
def online_trial(seed,U=1<<17,NA=1<<17):
    sh=Shake(seed+'|epoch'); r=sh.word()&8191; ustart=sh.word(); cv,M0=cv_from_seed(seed)
    m=Mach(); tab,ent,drop=build_table(r,ustart,U,m); bops=m.ops
    sbs=sorted(list(dict.fromkeys(SEL[sh.word()%NSEL] for _ in range(4*NA//256)))[:NA//256]); a0s=sel_a0s(sbs)
    col=[]; cola=[]; m2=Mach(); st=scan_cv(cv,tab,r,a0s,m2,collect=col,collect_all=cola)
    ref=sorted(ref_claws(cv,tab,r,a0s)); allc=sorted((a0,u) for (a0,u,F,j,win) in cola)
    ref1=sorted(x for x in ref if c1_of(cv,*x)); got=sorted((a0,u) for (a0,u,F,fl,j,win) in col)
    e16bad=sum(1 for (a0,u,F,j,win) in cola if not r16ok(e16_real_p1(cv,a0,(u-hfun(cv,a0))&M)))
    pfmis=sum(1 for (a0,u,F,fl,j,win) in col if pf_ref(cv,a0,(u-hfun(cv,a0))&M)!=tuple(fl))
    return cv,M0,st,dict(entries=ent,claws=st['claws_all'],ref_claws=len(ref),
        claws_equal_ref=int(allc==ref),c1_claws=st['claws'],c1_claws_equal_ref=int(got==ref1),claw_e16_bad=e16bad,
        postfilter_ref_mismatch=pfmis,probes=st['probes'],reads=st['reads'],scan_ops=m2.ops,c1c2=st['passes'][1],
        good_pairs=len(st['good']),step3b_collisions=len(st['coll']),expected_claws_milli=int(round(1000*160.0*ent*NA/2**32)),
        distinct_pairs=len(set(allc)))
def dense_trial(seed,U=1<<16,NA=1<<13,rows=True):
    sh=Shake(seed+'|dense'); r=sh.word()&8191; ustart=sh.word(); cv,M0=cv_from_seed(seed)
    tab,ent,drop=build_table(r,ustart,U,None,ncol=1024)
    base=sh.word()&((1<<26)-1)&~(NA-1); a0s=range(W9+base,W9+base+NA)
    col=[]; cola=[]; st=scan_cv(cv,tab,r,a0s,None,ncol=1024,collect=col,collect_all=cola)
    ref=sorted(ref_claws(cv,tab,r,a0s)); allc=sorted((a0,u) for (a0,u,F,j,win) in cola)
    ref1=sorted(x for x in ref if c1_of(cv,*x)); got=sorted((a0,u) for (a0,u,F,fl,j,win) in col)
    cum=[0]*22; bad=pfmis=0
    for (a0,u,F,fl,j,win) in col: pfmis+=int(pf_ref(cv,a0,(u-hfun(cv,a0))&M)!=tuple(fl))
    for (a0,u,F,j,win) in cola:
        a1=(u-hfun(cv,a0))&M; wx=variantW_P1(cv,a0,a1,SAx,SExF); wy=variantW_P1(cv,a0,a1,SAy,SEyF)
        tx=trace(cv,wx); ty=trace(cv,wy); e16=tx[1][16]
        bad+=int(not r16ok(e16) or ((e16-R16H[j]-(win<<10))&M) not in (0,1,4,5))
        if rows:
            for i in range(16,22):
                if rowok(tx,ty,i): cum[i]+=1
                else: break
    return dict(entries=ent,claws=st['claws_all'],ref_claws=len(ref),claws_equal_ref=int(allc==ref),c1_claws=st['claws'],
        c1_claws_equal_ref=int(got==ref1),row16_bad=bad,postfilter_ref_mismatch=pfmis,
        rows_le16=cum[16],rows_le17=cum[17],rows_le18=cum[18],rows_le19=cum[19],rows_le20=cum[20],rows_le21=cum[21],
        c1c2=st['passes'][1],expected_claws_milli=int(round(1000*160.0*ent*NA/2**32)))
NON=4; NDE=4
def walk_mean_obs(seed,n=1<<17):
    sh=Shake(seed+'|walk'); ops=cl=rd=bad=s1=s2=s12=0; us=sh.word()
    def bucket():
        k=0; x=sh.word()/2**32; e=c=math.exp(-8)
        while x>c and k<40: k+=1; e*=8/k; c+=e
        v=sorted(((sh.word()-us)&M,sh.word()&7) for _ in range(k))[:LANES]; d=EMPTYW
        for L,(u,t) in enumerate(v): d=(d&~(EMPTYT<<(STR*L+FLD)))|((((u+us)&M)|(t<<FLD))<<(STR*L)); d+=1<<CNT
        return d
    for i in range(n):
        w=sh.word()&7; PHI=sh.word(); W=wbl(w,PHI); x=y=0
        for off in ((0,8) if w>=3 else (0,)):
            d=bucket(); z=(((d+W+(W8L if off else 0))&MT3W)+KT3W)&GW; rd+=1
            if z==GW: continue
            m=Mach(); F=walk_lanes(z,m); x+=m.ops; y+=len(F)
            for l in F:
                t=(d>>(STR*l+FLD))&63; uq=(d>>(STR*l))&M
                bad+=not(t<8 and (t+off-w) in ((1,4,5) if off else (0,1,4,5)) and ((uq-PHI)&M)>>29==5)
        ops+=x; cl+=y; s1+=x*x; s2+=y*y; s12+=x*y
    R=ops/cl; se=math.sqrt(max(0,(s1-2*R*s12+R*R*s2)/(n-1))/n)/(cl/n)
    return dict(walk_draws=n,walk_reads=rd,walk_claws=cl,walk_ops=ops,walk_lane_mismatch=bad,walk_mean_ppm=int(1e6*R),walk_se_ppm=int(1e6*se),walk_ucb99_ppm=int(1e6*(R+2.326*se)),walk_charge_ppm=int(WALK_MEAN*10**6))
def wcv_obs(seed,K=16,U=1<<16,NA=1<<10):
    sh=Shake(seed+'|wcv'); r=sh.word()&8191; tab,_,_=build_table(r,sh.word(),U,None,ncol=1024); lo={}; n=q=0
    for G,u in table_entries(tab): lo.setdefault(G&8191,[]).append((G,u))
    b=W9+(sh.word()&((1<<26)-1)&~(NA-1)); Hr=(R16H[0]-r)&M
    for k in range(K):
        cv,_=cv_from_seed(seed+'|wcv%d'%k); co=cv_consts(cv); p={}
        def f(x):
            while p.setdefault(x,x)!=x: x=p[x]
            return x
        for a0 in range(b,b+NA):
            y=(Hr-Ffun(cv,a0,co))&M
            for o in OFFS:
                for (G,u) in lo.get((y+o)&8191,()):
                    if (((G-y-o)&M)>>13) in T20S: p[f((0,a0))]=f((1,u))
        J=len({f(x) for x in list(p) if x[0]==0}); n+=J; q+=J*(J-1)
    return dict(wcv_cvs=K,wcv_events=n,wcv_mean_ppm=int(1e6*n/K),wcv_ratio_ppm=int(1e6*q/n) if n else 0)
def r17(s):
 h=Shake(s);w=h.word;o=[0]*4;V=variantW_P1
 for _ in[0]*200:
  a=w();A=w();c=[w()for _ in o*2]
  for i in 2,0:
   x=trace(c,V(c,a,A,SAx,SExF));y=trace(c,V(c,a,A,SAy,SEyF))
   for k in 0,1:o[i+k]+=cellok(k,17,x[k][17],y[k][17])
   c[7]=(x[1][16]+c[7]-R16H[w()%20])&M
 return dict(cA=o[0],cE=o[1],uA=o[2],uE=o[3])
def sm(s):
 h=Shake(s);p=pf_consts([0]*8);N=1<<15;e=[0,0,0];d=[0,0,0]
 for _ in[0]*N:
  E=5<<29|h.word()>>3;a=W9+(h.word()&((1<<26)-1));t=pf_tail(Mach(),a,E,p);r=pf_ref([0]*8,a,(E-p['cE5'])&M)[1:]
  for i in 0,1,2:e[i]+=t[i];d[i]+=r[i]
 return dict(n=N,e2=e[0],d2=d[0],e3=e[1],d3=d[1],e4=e[2],d4=d[2])
def stc(s):
 h=Shake(s);p=pf_consts([0]*8);ob=dict(pairs=48)
 for d,w,k in('sel',0,0),('w9',1,0),('cls',0,1):
  c=[0,0]
  for _ in[0]*48:
   for _ in[0]*(1<<20):
    r=g_draw(h,p,w)
    if r is None:continue
    q,a,A=r;cv=[h.word()for _ in[0]*7]
    if k:cv[0]=cls_cv0(cv[0])
    if f7c(p,q,cv[0]):break
   t=T160[h.word()%160];cv.append(0);u=(A+hfun(cv,a))&M;cv[7]=(Ffun(cv,a,cv_consts(cv))+P(u)-t)&M
   x=trace(cv,variantW_P1(cv,a,A,SAx,SExF));y=trace(cv,variantW_P1(cv,a,A,SAy,SEyF))
   for j in 0,1:c[j]+=cellok(j,17,x[j][17],y[j][17])
  ob['a17_'+d],ob['e17_'+d]=c
 return ob
def run_request(req):
    out=[]; eid=req['experiment_id']
    for tr in req['trials']:
        t=tr['trial']; rec=dict(trial=t,message_a_hex=None,message_b_hex=None); s=eid+'|'+tr['seed']
        if 'online' in eid:
            if t<NON:
                cv,M0,st,obs=online_trial(s); rec['observations']=obs
                if st['coll'] and obs['claw_e16_bad']==0:
                    a0,a1,u,wx,wy=st['coll'][0]
                    rec['message_a_hex']=struct.pack('>32I',*(M0+wx)).hex(); rec['message_b_hex']=struct.pack('>32I',*(M0+wy)).hex()
            elif t==NON: rec['observations']=spair_obs()
            elif t==NON+1:
                n,bad=probe_exhaustive(); n1,bad1,np1=probe_c1_exhaustive()
                rec['observations']=dict(probe_lanes_checked=n,probe_mismatches=bad,c1test_lanes_checked=n1,c1test_mismatches=bad1,c1test_firing_lanes=np1)
            elif t==NON+2:
                ob=bs_check(s); ob['bs_gate_worst']=gbs_worst(); rec['observations']=ob
            elif t==NON+3: rec['observations']=sel_rates(s)
            elif t==NON+4: rec['observations']=cls_rates(s)
        else:
            if t<NDE: rec['observations']=dense_trial(s)
            elif t==NDE: rec['observations']=spair_obs()
            elif t==NDE+1: rec['observations']=cls_msg(s)
            elif t==NDE+2: rec['observations']=wcv_obs(s)
            elif t==NDE+3: rec['observations']=r17(s)
            elif t==NDE+4:rec['observations']=sm(s)
            elif t==NDE+7:rec['observations']=stc(s)
        if t==9:rec['observations']=walk_certificate()
        elif t==11 and 'online' in eid:rec['observations']=walk_mean_obs(s)
        elif t==10:
            _,n,s,info=ledger(False)
            rec['observations']=dict(ledger_N=n,ledger_NCV=info['NCV'],walk_init=WALK_INIT,walk_mean_ppm=int(WALK_MEAN*10**6),walk_proven=int(WALK_PROVEN),walk_max_read=WALK_MAX_READ,walk_max_claw=WALK_MAX_CLAW,step3b_mean_ppm=int(STEP3B_MEAN*10**6),step3b_max=STEP3B)
        out.append(rec)
    return dict(schema_version=1,trials=out)
SEL_Z='eNrt2b9KxDAcB/BvYjkiOHS8sfSE7h5cRiP4Dj7ADV3FwmVNwaGDg4/gOzi4trj4Jl3dbqy/Xr3BAwep0Dv4fpp/TUKHhF8yFCCiiUS/9H92I20HreROyva9LEvV3JRKSRJceqJpJYB2Q1MfDN2Pjf9r/2o3vrvzb+1ma/2Mq010RLGfpDqRqE+llidJf3oYG/++KLwvpJS68Ot8sbfe5TPuANGE8a/7E0AifZ//Of7tlbX5arlcZYsszW128H3NHSDi/U9EvP+J6HiEXQL0UwQDJy0l9S1cXIdhvAqhnxJduLjviFDjXJnLCsHhkQtIdMrxb8L3IVDJmwEqJyfA8yxuMEfcOIQXmLqCC6GCCZEz/TSF2n3M//Jz7wvv5eA3'
def _sel():
    bm=zlib.decompress(base64.b64decode(SEL_Z)); return [(q<<2)|1 for q in range(1<<16) if (bm[q>>3]>>(q&7))&1]
SEL=_sel(); SEL_SHA='150659fc4312d162c842c12db3defee46bb330f77158ac35bafb9930f52414da'
assert len(SEL)==4096 and hashlib.sha256(','.join(map(str,SEL)).encode()).hexdigest()==SEL_SHA
SELS=set(SEL); NSEL=len(SEL); NA_SEL=NSEL*256; N12=53096854
G_SEL=2051404269120
MSG_LO='-0.0362'
SBLOOP=7; KEP_SEL=20
CLS_MASK=63<<24; CLS_VAL=12<<24; SELJ=6; SELT=3; M0RAND=16; F7R='0.11985'; F7R_HI='0.12136'; F7C_MEAN='0.1206148'; MSG_CLS='-0.0225'; CLS_TRY=4096
def kept(cv): return (cv[0]&CLS_MASK)==CLS_VAL
def g_draw(sh,pf,w=0):
    for _ in range(1<<12):
        E5=0xA0000000|(sh.word()&0x1fffffff); w9=(pf['KW9']-E5)&M
        if (s0((w9+SPC['D9'])&M)-s0(w9))&M==SPC['D9s']: break
    a0=W9+((sh.word()&((1<<26)-1))if w else(SEL[sh.word()%NSEL]<<8)+(sh.word()&255)); a1=(E5-pf['cE5'])&M
    maj1=(pf['mA']|(a1&pf['mB']))&M; E40=(a0-maj1)&M; chx=(pf['cA']^(pf['cB']&E5))&M; w8=((pf['cW8']-E40)-chx)&M
    if (s0((w8+SPC['D8'])&M)-s0(w8))&M!=SPC['T8']: return None
    E4=(E40+pf['cE4'])&M; return (MAJ(pf['A2'],a1,a0)-CH(pf['E6'],E5,E4))&M,a0,a1
def f7c(pf,q,cv0): w7=(pf['KK7c']-cv0+q)&M; return (s0((w7+pf['D7c'])&M)-s0(w7))&M==SPC['F7d']
def cls_cv0(w): return (w&~CLS_MASK&M)|CLS_VAL
def cls_rates(seed,n=1<<15,m=16):
    sh=Shake(seed+'|cls'); pf=pf_consts([0]*8); g=fc=fu=0
    for i in range(n):
        r=g_draw(sh,pf)
        if r is None: continue
        g+=1; q=r[0]
        for j in range(m): fc+=f7c(pf,q,cls_cv0(sh.word())); fu+=f7c(pf,q,sh.word())
    return dict(draws=n,g_pairs=g,cv0_per_pair=m,f7_cls=fc,f7_all=fu,f7_cls_exp_milli=int(round(1000*g*m*float(F7C_MEAN))),
                f7_all_exp_milli=int(round(1000*g*m*287309824/2**32)))
def cls_msg(seed,n=1<<6):
    sh=Shake(seed+'|clsmsg'); pf=pf_consts([0]*8); px=trace(IV,PMX)[2]; py=trace(IV,PMY)[2]
    T23=px[23]^py[23]; T25=(py[25]-px[25])&M; ob={}
    for side in ('all','cls'):
        c=dict(pairs=0,e16_bad=0,pf_bad=0,dw23=0,dw25=0)
        for i in range(n):
            for _ in range(1<<20):
                r=g_draw(sh,pf)
                if r is None: continue
                q,a0,a1=r; cv=[sh.word() for _ in range(7)]
                if side=='cls': cv[0]=cls_cv0(cv[0])
                if f7c(pf,q,cv[0]): break
            t=T160[sh.word()%160]; cv.append(0); u=(a1+hfun(cv,a0))&M
            cv[7]=(Ffun(cv,a0,cv_consts(cv))+P(u)-t)&M
            wx=variantW_P1(cv,a0,a1,SAx,SExF); wy=variantW_P1(cv,a0,a1,SAy,SEyF)
            wx=trace(cv,wx)[2]; wy=trace(cv,wy)[2]
            c['pairs']+=1; c['e16_bad']+=e16_real_p1(cv,a0,a1)!=t; c['pf_bad']+=pf_ref(cv,a0,a1)!=(1,1,1,1)
            c['dw23']+=(wx[23]^wy[23])==T23; c['dw25']+=((wy[25]-wx[25])&M)==T25
        for k,v in c.items(): ob[k+'_'+side]=v
    return ob
def sel_a0s(sbs): return [W9+(sb<<8)+l for sb in sbs for l in range(256)]
def sel_rates(seed,n=1<<15):
    sh=Shake(seed+'|sel'); pf=pf_consts([0]*8); c=dict(gs=0,gw=0,fs=0,fw=0)
    def a1draw():
        while True:
            E5=0xA0000000|(sh.word()&0x1fffffff); w9=(pf['KW9']-E5)&M
            if (s0((w9+SPC['D9'])&M)-s0(w9))&M==SPC['D9s']: return E5
    def g_and_q(a0,E5):
        a1=(E5-pf['cE5'])&M; maj1=(pf['mA']|(a1&pf['mB']))&M; E40=(a0-maj1)&M; chx=(pf['cA']^(pf['cB']&E5))&M
        w8=((pf['cW8']-E40)-chx)&M
        if (s0((w8+SPC['D8'])&M)-s0(w8))&M!=SPC['T8']: return None
        E4=(E40+pf['cE4'])&M; return (MAJ(pf['A2'],a1,a0)-CH(pf['E6'],E5,E4))&M
    def f7(q,cv0):
        w7=(pf['KK7c']-cv0+q)&M; return (s0((w7+pf['D7c'])&M)-s0(w7))&M==SPC['F7d']
    for i in range(n):
        E5=a1draw(); sb=SEL[sh.word()%NSEL]; q=g_and_q(W9+(sb<<8)+(sh.word()&255),E5)
        if q is not None:
            c['gs']+=1; c['fs']+=f7(q,sh.word())
        q=g_and_q(W9+(sh.word()&((1<<26)-1)),E5)
        if q is not None: c['gw']+=1; c['fw']+=f7(q,sh.word())
    return dict(sel_ok=int(len(SEL)==4096),draws=n,g_sel=c['gs'],f7_sel=c['fs'],g_w9=c['gw'],f7_w9=c['fw'],
                g_sel_exp_milli=int(round(1000*n*G_SEL/(NA_SEL*N12))),g_w9_exp_milli=int(round(1000*n*57726359870197/2**26/N12)))
CENSUS12={'complete': True, 'reference_control_passed': True, 'reference_15': {'minimum': 44436632, 'maximum': 44543396, 'rotations': 8192, 'sum': 364428388980}, 'candidate_12': {'minimum': 35546342, 'maximum': 35641736, 'rotations': 8192, 'sum': 291542711184}}
def column_parameters(ncol,census=None):
    if ncol not in (12,14,15):raise ValueError('supported column count is 12, 14 or 15')
    if ncol==15:lo,hi,mean=44436632,44543396,'44485887.327'
    else:
        evidence=CENSUS12 if census is None else census
        if not evidence or not evidence.get('complete') or not evidence.get('reference_control_passed'):raise ValueError('complete measured %d-column census required'%ncol)
        ref=evidence['reference_15'];actual=evidence['candidate_%d'%ncol]
        if (ref['minimum'],ref['maximum'],ref['rotations'])!=(44436632,44543396,8192):raise ValueError('15-column census control')
        if actual['rotations']!=8192 or 15*actual['sum']!=ncol*ref['sum']:raise ValueError('census mean identity')
        lo,hi=actual['minimum'],actual['maximum'];mean=str(D(actual['sum'])/8192)
    limit=8*ncol+5;reads=26*ncol;table=ncol*(1<<19)*32;online=table+(2<<20)
    return dict(ncol=ncol,coverage_limit=8*ncol,probe_limit=limit,probing_low_words=2*limit,reads_per_head=reads,table_bytes=table,complete_online_peak_bytes=online,complete_peak_bytes=max(online,211431424),E_LO=lo,E_HI=hi,E_MEAN=mean,COV=8*ncol*(1<<19),NB=ncol*(1<<19),conservative_first_block_ratio=str(D(44436632)/lo),conservative_first_block_ratio_numerator=44436632,conservative_first_block_ratio_denominator=lo)
Q3P1='-96.0530'
def ledger(show=True,q3_log2=Q3P1,eps_log2=16,succ='0.39',A_C=2**60,A_S=2**60,DEV=2**60,mem=None,kep=None,bs=True,c1=True,sel=True,cls=True,ncol=NCOL,census=None):
    getcontext().prec=90
    geo=column_parameters(ncol,census);E_LO=geo['E_LO'];E_HI=geo['E_HI'];E_MEAN=geo['E_MEAN'];COV=geo['COV'];NB=geo['NB']
    if mem is None:mem=str(D(geo['complete_peak_bytes']).ln()/D(2).ln())
    cls=cls and sel
    if kep is None: kep=(KEP_SEL if sel else KEP)+(SELJ if cls else 0)
    kf=D(2)**-SELJ if cls else 1; st=SELT if cls else 0
    C=2728; L2=D(2).ln(); P2=lambda x: (D(x)*L2).exp(); NA=2**26; eps=D(2)**-eps_log2; K=2**kep
    p12=D(53096854)/D(2)**32; p12g=D(57726359870197)/D(2)**58; q_pf=p12g*D(287309824)/D(2)**32; q_pf_hi=q_pf
    pf=6+D(PF_C2)/8+PF_G*p12+PF_F7*p12g
    pres=D(geo['probe_limit'])/1024; pprobe=D(geo['probing_low_words'])/8192
    reads=D(20)*geo['reads_per_head']/geo['probing_low_words']; xc=D(20)*10/geo['probing_low_words']
    probe=SETUP+20*ROWJ+reads*(READ+WALK)+xc*XCROSS
    claw=EXTRACT+pf+q_pf*STEP3B
    ca_hi=D(160)*E_HI/D(2)**32; ca_lo=D(160)*E_LO/D(2)**32
    if c1:
        probe=SETUP+LAMSET+19*ROWJ+reads*READC1+xc*XCROSS
        claw=(WALK_MEAN+C1PRE+PF_C2+8*PF_G*p12+8*PF_F7*p12g+8*q_pf*STEP3B)/8
    fe=D(GBS+BATCH+2)/256
    if sel:
        NA=NA_SEL; gsel=D(G_SEL)/(D(NA_SEL)*N12); f7lo=f7hi=D(F7R) if cls else D(287309824)/D(2)**32
        if cls: f7hi=D(F7R_HI)
        q_pf=p12*gsel*f7lo; q_pf_hi=p12*gsel*f7hi; p12g=p12*gsel
        claw=(WALK_MEAN+C1PRE+PF_C2+8*PF_G*p12+8*PF_F7*p12g+8*q_pf_hi*STEP3B_MEAN)/8
        fe=D(GBS+BATCH+2+SBLOOP)/256
    per_a0=(fe+pprobe*(EXTRACT_BS+A0_PROBE+probe)+ca_hi*claw) if bs else (A0_BASE+pres*A0_RES+pprobe*probe+ca_hi*claw)
    wbar=C+M0RAND+st+FBCTL+kf*(CVSET+(CV_BS if bs else 0)+NA*per_a0)
    build=EPSET+NB*RESET+D(2)**32*U_BASE+E_HI*U_INS+(COV-E_HI)*U_DROP
    a0max=(D(GBS+BATCH+2)/256+EXTRACT_BS+A0_PROBE if bs else A0_BASE+A0_RES)+SETUP+20*(ROWJ+XCROSS)+40*(READ+WALK)+40*LANES*(EXTRACT+6+PF_C2+PF_G+PF_F7+STEP3B)
    if c1: a0max=D(GBS+BATCH+2)/256+EXTRACT_BS+A0_PROBE+SETUP+LAMSET+19*ROWJ+20*XCROSS+40*(READC1+WALK_MAX_READ)+40*LANES*(C1PRE+PF_C2+PF_G+PF_F7+STEP3B)
    if sel: a0max+=D(SBLOOP)/256
    vmax=int(C+M0RAND+st+FBCTL+CVSET+(CV_BS if bs else 0)+NA*a0max)
    q3r=P2(q3_log2)*D(2)**32/160
    if sel: q3r*=P2(MSG_LO)
    if cls: q3r*=P2(MSG_CLS)
    lam=kf*NA*ca_lo*q_pf*q3r*(1-D(2)**D('-8.5'))*(1-D(2)**-25)
    target=1-D(succ)-D(2)**-60
    NCV=int((-(target).ln()/lam))+1
    while 1-(-(NCV-1)*lam).exp()-D(2)**-60>=D(succ): NCV-=1
    NE=-(-NCV//K)
    VCV=int(((1+eps)*NCV*wbar).to_integral_value(rounding='ROUND_CEILING'))
    VMAX=NE*int(build)+VCV
    bern=(eps**2*NCV*wbar)/(2*vmax*(1+eps/3)); succ_lb=1-(-NCV*lam).exp()-(-bern).exp()-D(2)**-60
    ALLOW=(A_C+A_S+DEV)*C; OVER=int(max(vmax,build)); FIN=6*C+1600+WALK_INIT; N=ALLOW+VMAX+OVER+FIN
    tlog=float((D(N)/C).ln()/L2); score=tlog+float(D(mem))-20
    if show:
        print('u-table: %d columns x 2^%d rows, %d lanes, %d bytes; retained entries %d .. %d (mean %s) of %d covered'
              %(ncol,ROWB,LANES,32*NB,E_LO,E_HI,E_MEAN,COV))
        print('claws/a0 = %.6f (charged %.6f); q_pf = 2^%.4f; tag-only chain (55328d60) %.6f + q_pf x step 3b %.6f per claw'
              %(float(ca_lo),float(ca_hi),float(q_pf.ln()/L2),float(pf),float(q_pf*STEP3B)))
        if c1: print('C1 in the bucket test: per C1-claw walk %s + %d + segments %d + %d x P(C2|C1) %.6f + %d x P(C2 G|C1) %.6f + 8 q_pf_hi x step 3b %.6f = %.6f'
              %(WALK_MEAN,C1PRE,PF_C2,PF_G,float(8*PF_G*p12),PF_F7,float(8*PF_F7*p12g),float(8*q_pf_hi*(STEP3B_MEAN if sel else STEP3B)),float(8*claw)))
        if sel: print('selection: %d sub-blocks (%d a0) per scanned chaining value; P(G | C1 C2, SEL) = %.9f (W9: %.9f) = x%.4f; F7 rate %.5f; q_pf = 2^%.4f; epoch 2^%d first blocks'
              %(NSEL,NA_SEL,float(gsel),float(D(57726359870197)/D(2)**26/N12),float(gsel*D(2)**26*N12/D(57726359870197)),float(f7lo),float(q_pf.ln()/L2),kep))
        if cls: print('class ((cv0 >> 24) & 63) == 12: 2^-%d of first blocks kept, %d+%d ops per first block; F7 rate %s (99%% lower bound); message channel 2^%s charged'%(SELJ,SELT,FBCTL,F7R,MSG_CLS))
        if c1: print('per a0: front end (%d + %d + 2)/256 = %.6f + %.6f x (%d + %d + probe %.4f [setup %d + %d, %d heads x %d, %.1f reads x %d (tag and C1 test), %.1f x %d]) + %.6f C1-claws x %.6f = %.6f ops; per claw %.4f'
              %(GBS,BATCH+(SBLOOP if sel else 0),float(fe),float(pprobe),EXTRACT_BS,A0_PROBE,float(probe),SETUP,LAMSET,19,ROWJ,float(reads),READC1,float(xc),XCROSS,float(ca_hi/8),float(8*claw),float(per_a0),float(per_a0/ca_lo)))
        elif bs: print('per a0: front end (%d + %d + 2)/256 = %.6f + %.6f x (%d + %d + probe %.4f) + %.6f x claw %.6f = %.6f ops; per claw %.4f'
              %(GBS,BATCH,float(D(GBS+BATCH+2)/256),float(pprobe),EXTRACT_BS,A0_PROBE,float(probe),float(ca_hi),float(claw),float(per_a0),float(per_a0/ca_lo)))
        else: print('per a0: base %d + %.6f (resolve) + %.6f x probe %.4f + %.6f x claw %.6f = %.6f ops; per claw %.4f'
              %(A0_BASE,float(pres*A0_RES),float(pprobe),float(probe),float(ca_hi),float(claw),float(per_a0),float(per_a0/ca_lo)))
        print('epoch build %d ops (%.4f%% of an epoch of 2^%d first blocks)'%(int(build),100*float(build/(K*wbar)),kep))
        print('wbar = %.6e  vmax = %d  N_CV = %d  epochs = %d  V_MAX = %d'%(float(wbar),int(vmax),NCV,NE,VMAX))
        print('allowances A_C + A_S + DEV = 2^%.5f compressions = %.4f%% of N;  N = %d'%(float((D(A_C+A_S+DEV)).ln()/L2),100*float(D(ALLOW)/N),N))
        print('time_log2 = %.7f  memory 2^%s  score = %.7f  success >= %s'%(tlog,mem,score,str(succ_lb)[:22]))
    return tlog,N,succ_lb,dict(per_a0=per_a0,wbar=wbar,NCV=NCV,ca_lo=ca_lo,ca_hi=ca_hi,probe=probe,claw=claw,build=int(build),vmax=vmax,NE=NE,VCV=VCV,VMAX=VMAX,ALLOW=ALLOW,OVER=OVER,FIN=FIN,geometry=geo)
def selftest():
    print('selftest utab38'); ok=True
    assert (SPC['F7d'],SPC['T8'],SPC['D8'],SPC['D7'],SPC['D9s'])==(0x03bff800,0xfe808000,0xfbc00800,0x20000000,0x043ff800)
    assert len(T160)==160 and all(r16ok(w) for w in T160) and len(T20S)==20; print(' S-pair constants, |S160| = 160: OK')
    o=spair_obs(); print(' step 3b on the P8 pair:',o); ok&= o['step3b_P8_pair_ok']==1 and o['step3b_P8_pair_ops']==STEP3B
    n,bad=probe_exhaustive(); print(' six-lane test against the scalar definitions: %d lane checks, %d mismatches'%(n,bad)); ok&= bad==0
    n,bad,np1=probe_c1_exhaustive(); print(' combined tag and C1 test (Lemma B\'\'): %d lane checks, %d firing, %d mismatches'%(n,np1,bad)); ok&= bad==0 and np1>0
    for s in range(1,1<<LANES):
        z=GW^sum(G_L[L] for L in range(LANES) if (s>>L)&1); mw=Mach(); got=walk_lanes(z,mw)
        ok&= got==[L for L in range(LANES) if (s>>L)&1] and mw.ops<=WALK_MAX_CLAW*len(got)
    gw=gbs_worst(); ob=bs_check('selftest|bs',nb=64)
    print(' bitsliced front end:',ob,'worst-constant gate charge',gw); ok&= ob['bs_mismatches']==0 and gw==GBS and ob['bs_gates_max']<=GBS
    for sd in ('selftest|a','selftest|b'):
        cv,M0,st,ob=online_trial(sd); print(' online',sd,ob)
        ok&= ob['claws_equal_ref']==1 and ob['c1_claws_equal_ref']==1 and ob['claw_e16_bad']==0 and ob['postfilter_ref_mismatch']==0 and ob['claws']>0
        ob=dense_trial(sd,NA=1<<13); print(' dense ',sd,ob)
        ok&= ob['claws_equal_ref']==1 and ob['c1_claws_equal_ref']==1 and ob['row16_bad']==0 and ob['postfilter_ref_mismatch']==0 and ob['c1_claws']>0
    tab={}; rr=random.Random(5); keep={}
    for i in range(64):
        u=rr.getrandbits(32); g=(rr.randrange(4)<<3)|rr.randrange(8); k=((g>>3)<<ROWB)|7; d=tab.get(k,EMPTYW); c=d>>CNT
        if c<LANES:
            sh=STR*c; d=(d&~(EMPTYT<<(sh+FLD)))|((u|((g&7)<<FLD))<<sh); d+=1<<CNT; tab[k]=d; keep.setdefault(k,[]).append((g&7,u))
    rec={k:[((d>>(STR*L+FLD))&63,(d>>(STR*L))&M) for L in range(d>>CNT)] for k,d in tab.items()}
    emp=all(((d>>(STR*L+FLD))&63)==EMPTYT for k,d in tab.items() for L in range(d>>CNT,LANES))
    print(' retention: %d buckets, first six kept in insertion order %s, empty lanes marked %s'%(len(tab),rec==keep,emp)); ok&= rec==keep and emp
    cv,_=cv_from_seed('selftest|ops'); sh=Shake('selftest|ops'); r=sh.word()&8191
    tab,ent,drop=build_table(r,sh.word(),1<<16); m=Mach(); a0s=range(W9,W9+(1<<16)); st=scan_cv(cv,tab,r,a0s,m)
    chg=CV_BS+st['batches']*(GBS+BATCH+2+SBLOOP)+st['probes']*(EXTRACT_BS+A0_PROBE+SETUP+LAMSET+19*ROWJ+20*XCROSS)+st['reads']*READC1
    chg+=st['claws']*(WALK_MAX_CLAW+C1PRE+PF_C2+PF_G+PF_F7)+len(st['good'])*STEP3B
    print(' counted scan ops %d <= itemised charge %d: %s (probes %d of %d a0, reads %d)'%(m.ops,chg,m.ops<=chg,st['probes'],st['a0'],st['reads']))
    ok&= m.ops<=chg and abs(st['probes']/st['a0']-2*(8*NCOL+5)/8192)<0.003
    ob=sel_rates('selftest|sel',n=1<<13); print(' selection rates (sampled):',ob)
    ok&= ob['sel_ok']==1 and ob['g_sel']>ob['g_w9']
    oc=cls_rates('selftest|cls',n=1<<13,m=8); om=cls_msg('selftest|cls',n=16); print(' class rates (sampled):',oc,om)
    ok&= oc['f7_cls']>oc['f7_all'] and om['e16_bad_all']==0 and om['e16_bad_cls']==0 and om['pf_bad_all']==0 and om['pf_bad_cls']==0
    tlog,N,sl,_=ledger(show=False); print(' ledger time_log2 = %.7f, success >= %s'%(tlog,str(sl)[:12])); ok&= sl>=D('0.39')
    print('SELFTEST','PASS' if ok else 'FAIL'); return ok
def main():
    a=sys.argv[1] if len(sys.argv)>1 else ''
    if a=='selftest': sys.exit(0 if selftest() else 1)
    if a=='ledger': ledger(); return
    if a=='ledger-allow70': ledger(A_C=2**70,A_S=2**70,DEV=2**70); return
    if a=='ledger-base': ledger(cls=False); return
    if a=='ledger-scalar': ledger(bs=False,c1=False,sel=False); return
    sys.stdout.write(json.dumps(run_request(json.load(sys.stdin))))
if __name__=='__main__': main()
