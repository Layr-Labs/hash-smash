#!/usr/bin/env python3
# sha256-r37 own-path program (proof.md Sections 8, 9, 13). python3 lowm.py selftest | family | ledger | memory | attack N V ; stdin JSON: organizer experiments. Standard library only.
import hashlib, json, math, random, struct, sys
from fractions import Fraction as Fr
from decimal import Decimal, getcontext
import base64, zlib
_BLOB = (
'c-p<2U60(>k%sT*S2QNKT!So<r%nklpdcUEi);{Vj71Vd7gapX*ofTPc-#n#VE_9T+5N;LF^MLKU>TCnoPK#uRgwKZ1Z(*E^=}{k`uMZ|d3^QdXroOgrFJ6oSo_+GbVHq`RvSy-4MnF>OYN<b{CLct'
'YtD|tG}qEkLs!JKj`Jj)^lD>26_GdH<A41w7as<bTuC(#7Aqx{b?An9vRbFAV>eh|^QSTnUCN3Lxoz#L)M>PS&X{tl40X~j_scko&2uN3$Lg42b&}D~Rwk(#Qqdx#+4gzKgSSLRo%>pbVaVu)I!=T1'
'b&EyjzOR`<H}r$e!!VBh7W3~vMa;D?{U|zHhLnfeoYl#ta@{@`&S9PBTzxDh1uAuzi@qS{p-69eV)|~XQl>0@&5(bZ5l_AK8P70{olO0_pTarMVcE{8<TBP5*(S$s8Z=MWFi94)<VShBM(f7Dj;g)%'
'Q&*=+O{YAsW_2D));6Q;>$ZE@&ajj@{~I#OA@j^}ZmP59R2Cr1WY+h2D)!jE|0Ka}J5O1TlEGy>GT8VJg3J2n^^ljvIBQ-Kwk<k}O;c`US?#GzWw1P98Qd?nYrjsG=ih1`G0o!^dfCtKwrHN^PDkyh'
'X{y`#oAb2UH0Py|`kd>xuYp?0i$1>?U4CBse(EJpyVfm@JaZYm=J~C?ZY$*FIZb&XbT!wXv}{*(UO+jYb<CqgvwWr67Tx!sB0L#0`?(+Tni0#dW`2>Tz4m!VhP_Vr@aFAHqxs#+?}c?axt)|geLyGO'
'4zqqcY8Z0aX?XL053gVU>ghZG_8|j2pV!GxvXm*#{c@OTAI``@BhNMMuueOy(+=yj57!xU<tlv~X3mG1^}`uC93_XN<b$K^y_oMa?ZX*4Xg-YD4>9{8W<SL2hnW2kvwsltvSlIf&-nW@?NGyZs9`(Q'
'upMgH4mE6t8n#0X+o6W-P{VepVLQ~Y9ctJPHEf3(wnGiup@!{H!*;LX>(|S>%hPvH3E7{Q$5(Uup{99D_xN*te3c%M=3fRa`Ez}Im4=^qE%|lt9=}L=5_Kpgzu%8vq*~^UPH7O2U!+#^yPss}x9{Nc'
')z=R{IsNB&dODxmX?k^f`udNT94+U!Z=X)@E^oi@PT#)!%hRcR_SrC>)^Fc^bNcS9^Xa!g{o?e^yLNtiKk%-ay7Y#W%5?hQYrOsX>8t$kw&X(!PN(Vg`A7cz`-0m}^N+SuIemV){_}+{*Xzf2y1ZZ~'
'eHPK>{eSNN+ZVd>^X-#8xa&QH+X~nF-{)(+w^My#aW1#Ne_QK%A6|FC^#wWEzjYek%jx<ooy%?Fvj5$88v4_-V?IBQ|8^Swso+qx>vPR*r{VO&q1R_iUG5W?eWB~+`C40~TqQYr*|j&w$FIHHirb%O'
'%6+$Ozsn1+@?kuEn9Z|t|8N>8%H?vrq+htxbb7B|pTBUS=V$JRtNil!Pvvc=mw3eW@O`^JU+QI7`A|Np`$TRu=)bto^&fqoKDtwV@lMz4zj7jvJK2xr<<h@oq3fsEY537{l25nO<??s08g}|LbpHqm'
'^QJ`~bSOU0(|WoM=J7tL%-DTK(I^^4qi76`p)oXuCeQ?$KofV35{43n5{9z7vb(aovZ=DEvZ=C{vX|cX3Q`VI4pI&>4KfWf4H66z3=$0T3i1l_3es7~Vj+u#EEcj@$YLRjg)A1bSjeK0MI(zw7L6<#'
'Sv0a}WYNf?kwqhmMiz}M8fT}GPUGw}@@nMO$g7c8Bd<nYjl3FpHS#*M;F$%_EO=(YGYg(s@XUf|7Cf`yN}*N?wNj{+Lah{PrBEw{S}D{@p;ijDQmB<et$P1jtyFBKVk;F}Rnf3JnXY8Is-YnaQeH`U'
')j&f$<i6f>*FK+<-3Pb8w!zFyWd==QpokT*B33k&fgv`;hS<<JgFqaJ12Hixp(>#&p(>#&fhmD0fhl1qVJKlJn<|@9D5ES!S&Xt6MKFqB6v0T@NZCl)NYF^oNYKd3$jivf$jivf$jivf$jivf$jivf'
'$ji9^Fnq=E6~k8yKL>?@B38tTSkY7lhS(4rVngE$0&yS?#Kg=602CA`C{R$Kpg=)^f&v8v3JMeyC@4@+prAlOfr0`B1quoj6euWAP@tedL4kq-1qBKU6ci{ZP*9+tKtX|m0tE#M3KSG5C{R$Kpg=)^'
'f&v8v3JMeyC@4@+prAlOfr0`B1quoj6euWAP@tedL4kq-1qBKU6ci{ZP*9+tKtX|m0tE#M3KSG5C{R$Kpg=)^f&v8v3JMeyC@4@+prAlOfr0`B1quoj6euWAP@tedL4kq-1qBKU6ci{ZP*9+tKtX|m'
'0)+|`Dp06Ep#p^p6e>`tK%oMK3KS|(s6e3tg$fiZP^dtm0)+|`Dp06Ep#p^p6e>`tK%oMK3KS|(s6e3tg$fiZP^dtm0)+|`9M5z-)A3BlGaajRtkSVc$0{9%bR5!gNXH=^V|0wsF-FH29Y1vZ(D6gZ'
'4;?>r{Lt}3#}6Gpbo|iqL&pytKXm-i@k7TC9Y1vZ(D6gZ4;?>r{Lt}3#}6Gpbo|iqL&pytKXm-i@k7TC9Y1vZ(D6gZ4;?>r{Lt}3#}6Gpbo|iqL&pytKXm-i@k7TC9Y1vZ(D6gZ4;?>r{Lt}3#}6Gp'
'bo|iqL&pytKXm-i@k7TC9Y1vZ(D6gZ4;?>r{Lt}3#}6Gpbo|iqL&pytKXm-i@k7TC9Y1vZ(D6gZ4;?>r{Lt}3#}6Gpbo|iqL&pytKXm-i@x#Cm13wJ>Fz~~`4+B38{4nstzz+jI4E!+g!@v&%KMedZ'
'@Wa3l13wJ>Fz~~`4+B38{4nstzz+jI4E!+g!@v&%KMedZ@Wa3lgPY{wCONoC4sMczo8;goIk-s<ZjytW<lrVbxJeFfl7pM%;3he^Ne*t3gPY{wCONoC4sMczo8;goIk-s<ZjytW<iPL)!w(EUF#O;q'
'IdJ~K`2*(<oIkip4iFF^AV5HXfZ!%MU_rowfCT{yf}7+33IP-XC<IUlpb$VIfI<L;015#V0w@Gf2%r!^A%H>vg#Zcx6apv&Pzaz9Kp}ua0EGYw0Tco#1W*W|5I`Y-LI8yT3IP-XC<IUlpb$VIfI<L;'
'015#V0w@Gf2%r!^A%H>vg#Zcx6apv&Pzaz9Kp}ua0EGYw0Tco#1W*W|5I`Y-LI8yT3IP-XC<IUlpb$VIfI<L;015#V0w@Gf2%r!^A%H>vg#Zcx6apv&Pzaz9Kp}ua0EGYw0Tco#1W*W|5I`Y-!U7Z)'
'ps)ai1t=^)VF3yYP*{M%0u&aYumFVxC@er>0SXIHSb)L;6c(Vc0EGo8EI?ra3JXwJfWiV47ND>Ig#{=qKw$w23s6{q!g7a#<Rjc^o7o4<>|qGcmW5}_!n5UVP?#yqC`TzrDH=snnW@YeM;S*M8bjmE'
'I5WXf!BK&Ryp-UT;FaK&2$cwx2$e9DFqANqy_CJEVNj@`P(h)BY6R5?su83dq#UFi<Q3!<<Q1e7q!VNjWDx`(1Rum4#JsT1!a56OSy*sk!G*Fcth})DLRl8JSlFUbmPT0`WoeY9QI<wo8f9serBRkf'
'SsG<&l%;XH8+kSIYUI_(tC3eDuSQ;tyc&5m@@nLDW{WdhoY~^c7H76Nv&ES$&TMgJi!)oC*<z)1E2Ud0-Ad_JO1DzFmC~)0Zl!c9rCTZ8O6l&_Ej;uV9(oH8y|+POrZA%%MLgublKZNanaYfD6roa<'
'm9nhr%s4Z_QDi~I?uIYhqw-y|4Q6I4GiYWsGnyIAjHaL|XbPHwM$sr5MWbjcnu?~Psb~z1p)oXu#?d$$N8@M$O`r)h)JLg?QVpdVN;Q;fDAiCBR1#DYRAN?QR$^AdP{QCe8I?CGZ&cnWrcq3zm_~h!'
'`WW>wQZ`aHQa183@-p%=@-p%=@-p%=@-p%=@-p%=@^UUe=kf!rJi`~B;S103g=hG}GyH8(&=fQUO+lk*6pf-$G!;!nQ_)m3hQ`ns8bjk~9F3!KG=V121RCnY<>y>}&gBQGX%h%-0-;SHv<ZYZfzT!p'
'+5|$IKxh*PZ33Z9AhZdDHi6J45ZVMnn?Pt22yFtPO(3)hgf@ZDCJ@>LLYrV8FvH4Z0jU*IE2LIPt&mzFHGK!6?;!LYgua8&cM$pxLf=8?I|zLTq3<B{9fZDv(035}4np5S=sO5~2chpE^c{r0gV1*n'
'`VK<hLFhXOeFvfMAoLxCzJt(r5c&>6-$Cd*2z>`pNUe~XPK3~j5IPY;Cqn2%2%QL_6CrdWgieIei4ZywLMKA#L<pS-p%Wo=B7{za(1{Q_5ke<I=tKye2%!@pbRvXK#5O3*6lRp8h=<%EwL)rz)O0I^'
'ZiUdT5V{rHz?pGof}_ZSib3iMsVk(ekeb$p(Ap4M8$xSCXl-nRf~KG;XbKudqi7V3qN!*qnu?~PF*Jt8&=?v=<7ga>qX{&DCeTnHr5Z{#lxir|P^zI+LrG9cP)SgUS&3PRSqVc4<9?dxl?c5Op)(?M'
'Mua|y&<7E^9zxecf|JX0TH!gZ@SIk7PAfd8-3Eo3!i;j1a+IP`G?kgkjB%84l%X*+&Wtk?92FcDXfm(-J*=<3e){g=%P;fAl9KO{yy<eJ`NGGvjq=r+d@*VtNxnL=52o7LKA7b`v%T(P`>^!=?ZbSN'
'rQ26fyASd`lx|<WPWcYWv@e?PvD`k)ccAk9oqY+Ln9DcO$~Kz%yKL$+ocq)$-DLZy-U7?FpzZ_Ng5C#(LB5u?A2!PN{>nC*SaVACe%K@vpXJ*```Xj?X3wsg^H=uogL3<9tHVCC{eJ#fwvlcxpY3bq'
'3qbi6(l)Z(abMK#6`Awxs@ouobUSd~swMkez9Pja%eyaD`YkYd^Cr*LH~#der-xw;Zx)fiyy?|yM1GQQ;p}f2{4!q~$d}Q^-fAB9_{)56pyZo9`65u?J^uHwe`@3Y*>8URhyA4j%@?+|w+Q|`KKzIF'
'pN-T11B6B|3I')
B = {}
for _p in zlib.decompress(base64.b85decode(_BLOB)).decode().split('@@')[1:]: _k, _v = _p.split('\n', 1); B[_k] = _v
M32 = 0xffffffff
ONE = (1 << 256) - 1
K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
     0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
     0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
     0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
     0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354]
IV = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
R = 37
def ror(x, n): return ((x >> n) | (x << (32 - n))) & M32
def S0(x): return (((x >> 2) | (x << 30)) & M32) ^ (((x >> 13) | (x << 19)) & M32) ^ (((x >> 22) | (x << 10)) & M32)
def S1(x): return (((x >> 6) | (x << 26)) & M32) ^ (((x >> 11) | (x << 21)) & M32) ^ (((x >> 25) | (x << 7)) & M32)
def s0(x): return (((x >> 7) | (x << 25)) & M32) ^ (((x >> 18) | (x << 14)) & M32) ^ (x >> 3)
def s1(x): return (((x >> 17) | (x << 15)) & M32) ^ (((x >> 19) | (x << 13)) & M32) ^ (x >> 10)
def CH(x, y, z): return (x & y) ^ (~x & z & M32)
def MAJ(x, y, z): return (x & y) ^ (x & z) ^ (y & z)
def trace(cv, w16, n=R):
    A = {-1: cv[0], -2: cv[1], -3: cv[2], -4: cv[3]}; E = {-1: cv[4], -2: cv[5], -3: cv[6], -4: cv[7]}
    W = list(w16)
    for i in range(16, max(n, 16)): W.append((s1(W[i-2]) + W[i-7] + s0(W[i-15]) + W[i-16]) & M32)
    for i in range(n):
        E[i] = (A[i-4] + E[i-4] + S1(E[i-1]) + CH(E[i-1], E[i-2], E[i-3]) + K[i] + W[i]) & M32
        A[i] = (E[i] - A[i-4] + S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])) & M32
    return A, E, W
def compress(cv, w16):
    A, E, _ = trace(cv, w16)
    return [(c + o) & M32 for c, o in zip(cv, [A[R-1], A[R-2], A[R-3], A[R-4], E[R-1], E[R-2], E[R-3], E[R-4]])]
def digest(msg):
    m = msg + b'\x80' + b'\x00' * ((55 - len(msg)) % 64) + struct.pack('>Q', 8 * len(msg))
    h = IV
    for k in range(0, len(m), 64): h = compress(h, list(struct.unpack('>16I', m[k:k+64])))
    return struct.pack('>8I', *h)
CHA = {6:'=nu=============================',7:'==========n====n====n======n====',10:'======u===========u=============',
    11:'====u=====u=========u=n====u==n=',12:'=nu=============================',13:'====u=========u=u=======n==u====',
    14:'======u=n=======n===============',16:'==u============================='}
CHE = {4:'000=============================',5:'111=0=====1==0=====01===++01====',6:'uuu=1011=00=10111=0111=0++1011==',
    7:'10n=u01001n00n00010nu110unuu0001',8:'011=1n+1=n11u1101=001u1u1010=u=1',9:'1=0110+=001=1100=+110100111u=0=+',
    10:'10n001u110101==01+u1101011=1110+',11:'=01un000011101=n0n0u1uu101011u1u',12:'01101uuuuunu010110110n1u0u0uu0n0',
    13:'0+10n110111unn+0n101110110001001',14:'=+0=1000000111+=1==1n010u0=0101=',15:'=u==01===n=011n01==u0=u=1==+====',
    16:'=0=====+=0===11=+==01=0=0==+====',17:'=0======01===u1=+==0==1===1u====',18:'=======uu=======n=====1====1====',
    19:'=======00====1==0==========1====',20:'==u====10=======1===00==========',21:'==0=============================',
    22:'==1============================='}
CHW = {6:'==n=============================',7:'=====u===u==========n===========',8:'==u=============================',
    9:'=====u=u=======n===u==n=u=n=u=n=',10:'============n======u=n==========',14:'=0===u===n=1=1====1=u=1=====1=1=',
    15:'==u=============================',22:'=====0=nn=====1=u=1=============',24:'==n============================='}
def _signed_rows(fn):
    out = ({}, {}, {})
    for ln in fn.splitlines():
        t = ln.split()
        if len(t) == 5 and t[0] == 'row' and int(t[1]) <= 15:
            for k in range(3): out[k][int(t[1])] = ''.join(c if c in 'nu' else '=' for c in t[2 + k])
    return out
_sg = _signed_rows(B['chi'])
for _d, _g in zip((CHA, CHE, CHW), _sg):
    for _i in [i for i in _d if i <= 15]: del _d[_i]
    _d.update({i: v for i, v in _g.items() if v != '=' * 32})
assert CHE[15][27] == '='; CHE[15] = CHE[15][:27] + '+' + CHE[15][28:]
X2 = [('A',15,15,'!','A',16,15),('A',15,23,'=','A',16,23),('A',15,25,'=','A',16,25),('A',16,9,'!','A',16,20),
    ('A',16,18,'!','A',16,6),('A',16,8,'=','A',16,17),('A',15,29,'=','A',17,29),('A',17,29,'=','A',18,29),
    ('E',15,4,'=','E',16,4),('E',17,0,'!','E',17,13),('E',16,15,'=','E',17,15),
    ('E',18,6,'!','E',18,19),('E',18,2,'=','E',18,20),('E',20,2,'!','E',20,16),
    ('W',6,1,'=','W',6,12),('W',6,8,'!','W',6,25),('W',6,14,'=','W',6,18),
    ('W',7,0,'=','W',7,28),('W',7,9,'=','W',7,30),('W',7,1,'=','W',7,18),
    ('W',8,1,'!','W',8,12),('W',8,8,'!','W',8,25),('W',8,14,'=','W',8,18),
    ('W',22,31,'!','W',22,1),('W',22,30,'!','W',22,0),('W',22,16,'!','W',22,25),('W',22,14,'!','W',22,21),
    ('W',24,4,'!','W',24,6),('W',24,22,'=','W',24,31),('W',24,20,'!','W',24,27)]
X2 = [e for e in X2 if max(e[1], e[5]) >= 15]
def cell(s):
    m = v = d = p = 0
    for c, sym in enumerate(s):
        b = 31 - c
        if sym in '01un': m |= 1 << b
        if sym in '1u': v |= 1 << b
        if sym in 'un': d |= 1 << b
        if sym == '+': p |= 1 << b
    return m, v, d, p
EQ = '=' * 32
CELLS = {k: {i: cell(t.get(i, EQ)) for i in range(-4, R)} for k, t in (('A', CHA), ('E', CHE), ('W', CHW))}
def row_ok(x, y, i, checkW=True):
    for k, X, Y in (('A', x[0], y[0]), ('E', x[1], y[1])):
        m, v, d, p = CELLS[k][i]
        if (X[i] & m) != v or (X[i] ^ Y[i]) != d: return False
        if k == 'E' and i > -4:
            q = p & CELLS['E'][i-1][3]
            if q and ((X[i] ^ X[i-1]) & q): return False
    if checkW and i >= 0:
        m, v, d, _ = CELLS['W'][i]
        if (x[2][i] & m) != v or (x[2][i] ^ y[2][i]) != d: return False
    return True
def x2_ok(x, r):
    D = {'A': x[0], 'E': x[1], 'W': x[2]}
    for (k1, i1, b1, op, k2, i2, b2) in X2:
        if max(i1, i2) != r: continue
        a, c = (D[k1][i1] >> b1) & 1, (D[k2][i2] >> b2) & 1
        if (op == '=') != (a == c): return False
    return True
def h8(s): return [int(t, 16) for t in s.split()]
_S = json.loads(B['S']); CV0, MX, MY = _S['CV'], _S['MX'], _S['MY']
_LS = [ln.split() for ln in B['Lstar'].splitlines() if ln.strip()]; W14X = int(_LS[0][0], 16); assert all(int(a, 16) == W14X for a, b in _LS)
LW15 = [int(b, 16) for a, b in _LS]
def lstar(l): return (W14X, LW15[l]), (W14X ^ 0x04400800, LW15[l] ^ 0x20000000)
_KC = json.loads(B['consts']); D6, T6, D7, T7, D8, T8 = (_KC[k] for k in ('D6', 'T6', 'D7', 'T7', 'D8', 'T8'))
assert (MY[6] - MX[6]) & M32 == D6 and (MY[7] - MX[7]) & M32 == D7 and (MY[8] - MX[8]) & M32 == D8 and (-(MY[14] - MX[14])) & M32 == T6
def inF(w, d, t): return ((s0((w + d) & M32) - s0(w)) & M32) == t
F6 = lambda w: inF(w, D6, T6)
F7 = lambda w: inF(w, D7, T7)
_tx = trace(CV0, MX, 14)
SA = [_tx[0][i] for i in range(14)]; SE = _tx[1]
A1, A2, A3, A4 = SA[1], SA[2], SA[3], SA[4]
E5, E6, E7 = SE[5], SE[6], SE[7]
C4 = (A4 - S0(A3) - MAJ(A3, A2, A1)) & M32
W8C = (SE[8] - A4 - S1(E7) - CH(E7, E6, E5) - K[8]) & M32
C6 = (E6 - 2 * A2 + S0(A1) - S1(E5) - K[6]) & M32
K3C = (A3 - S0(A2)) & M32
def in_G(a0):
    e4 = (a0 + C4) & M32
    if e4 >> 29 != 4: return False
    w = (W8C - e4) & M32
    return ((w >> 29) & 1) == 1 and inF(w, D8, T8)
def k3of(a0): return (K3C - MAJ(A2, A1, a0)) & M32
def ne4of(a0): return ~(a0 + C4) & M32
def c7of(a0):
    e4 = (a0 + C4) & M32
    return (E7 - A3 - k3of(a0) - S1(E6) - CH(E6, E5, e4) - K[7]) & M32
def w6of(a0, am1, am2):
    e4 = (a0 + C4) & M32; e3 = (k3of(a0) + am1) & M32
    return (C6 - am2 + MAJ(A1, a0, am1) - CH(E5, e4, e3)) & M32
def class_members(c7, base, mask):
    out, s = [], 0
    while True:
        a = base ^ s
        if in_G(a) and c7of(a) == c7: out.append(a)
        s = (s - mask) & mask
        if s == 0: break
    return sorted(out)
C7S = [int(x, 16) for x in B['c7'].split()]; NCLS = len(C7S); NCB = (NCLS + 255) // 256
_ZC = (E7 - A3 - S1(E6) - K[7] - K3C) & M32
def fibre(c7):
    D = (c7 - _ZC) & M32; out = []
    def rec(i, a, cs, br):
        if i == 32: out.append(a); return
        c4, a1, a2, e5, e6, d = (C4 >> i) & 1, (A1 >> i) & 1, (A2 >> i) & 1, (E5 >> i) & 1, (E6 >> i) & 1, (D >> i) & 1
        for ab in (0, 1):
            m = a2 if a1 == a2 else ab; e4b = ab ^ c4 ^ cs; v = e5 if e6 else e4b
            if m ^ v ^ br != d: continue
            rec(i + 1, a | (ab << i), (ab & c4) | (ab & cs) | (c4 & cs), ((1 - m) & v) | ((1 - m) & br) | (v & br))
    rec(0, 0, 0, 0); return out
_KL = {}
def klass(ci):
    if ci not in _KL:
        mem = [a for a in fibre(C7S[ci]) if in_G(a)]; an = M32; o = 0
        for x in mem: an &= x; o |= x
        _KL[ci] = (C7S[ci], an, o & ~an, len(mem), tuple(sorted(x ^ an for x in mem)))
    return _KL[ci]
def new_rows(tx, ty): return [({**t[0]}, {**t[1]}, {i: t[2][i] for i in range(16)}) for t in (tx, ty)]
def step_rows(X, Y, t):
    for (A_, E_, W_) in (X, Y):
        E_[t] = (A_[t-4] + E_[t-4] + S1(E_[t-1]) + CH(E_[t-1], E_[t-2], E_[t-3]) + K[t] + W_[t]) & M32
        A_[t] = (E_[t] - A_[t-4] + S0(A_[t-1]) + MAJ(A_[t-1], A_[t-2], A_[t-3])) & M32
def setup_l():
    L = []
    for l in range(len(LW15)):
        (x14, x15), (y14, y15) = lstar(l)
        tx = trace(CV0, MX[:14] + [x14, x15], 16); ty = trace(CV0, MY[:14] + [y14, y15], 16)
        base = (tx[0][12] + tx[1][12] + S1(tx[1][15]) + CH(tx[1][15], tx[1][14], tx[1][13]) + K[16]) & M32
        L.append(dict(l=l, tx=tx, ty=ty, base=base, C16=(base + s1(x14) + MX[9]) & M32,
                      dW16=(s1(y14) - s1(x14) + MY[9] - MX[9]) & M32))
    return L
def row16_ok(Ld, e16):
    X, Y = new_rows(Ld['tx'], Ld['ty'])
    X[2][16] = (e16 - Ld['base']) & M32; Y[2][16] = (X[2][16] + Ld['dW16']) & M32
    step_rows(X, Y, 16)
    return row_ok(X, Y, 16) and x2_ok(X, 16)
E16M, E16V = CELLS['E'][16][0], CELLS['E'][16][1]
FEASIBLE_L = list(range(len(LW15)))
class Shake:
    def __init__(self, seed): self.seed = seed.encode(); self.k = 0; self.buf = b''; self.pos = 0
    def __call__(self):
        if self.pos + 32 > len(self.buf):
            self.buf = hashlib.shake_256(self.seed + b'|' + str(self.k).encode()).digest(1 << 14); self.k += 1; self.pos = 0
        v = int.from_bytes(self.buf[self.pos:self.pos + 32], 'little'); self.pos += 32; return v
    def below(self, n): return self() % n
class Mach:
    def __init__(self): self.n = 0
LM = sum(M32 << (64 * k) for k in range(4)); M256 = ONE
def bc(x): return sum((x & M32) << (64 * k) for k in range(4))
def first_block(mc, rng):
    r = [rng(), rng()]; mc.n += 2; w = []
    for k in range(16):
        x = r[k // 8]
        if k % 8: x >>= 32 * (k % 8); mc.n += 1
        if k % 8 != 7: x &= M32; mc.n += 1
        w.append(x & M32)
    return w
RBASE = 0
def cv_pre(mc, cv):
    Am1, Am2, Am3, Am4, Em1, Em2, Em3, Em4 = cv
    mc.n += 4; mj = (Am1 & Am2) | (Am3 & (Am1 | Am2))
    mc.n += 11; e0b = (Am4 - S0(Am1) - mj) & M32
    mc.n += 3; ch = (Em1 & (Em2 ^ Em3)) ^ Em3
    mc.n += 16; kap0 = (e0b - Am4 - Em4 - S1(Em1) - ch - K[0]) & M32
    mc.n += 5 + 42; n12 = Am1 & Am2
    return dict(e0b=e0b, kap0=kap0, C=((kap0 - e0b) & M32) + RBASE, x12=Am1 ^ Am2, n12=n12, X=Em1 ^ Em2, Em2=Em2, kap1=(A1 - K[1] - Em3 - n12) & M32)
M64 = (1 << 64) - 1
def bc64(x): return sum(x << (64 * k) for k in range(4))
def recompute_w67(mc, a0, a, b):
    mc.n += RECOMP; return w6of(a0, a, b), (c7of(a0) - a) & M32
def step3b(mc, cv, a0, w6, w7, ls, Lt):
    Am1, Am2, Am3, Am4, Em1, Em2, Em3, Em4 = cv
    Ar = {-1: Am1, -2: Am2, -3: Am3, -4: Am4, 0: a0, 1: SA[1], 2: SA[2], 3: SA[3], 4: SA[4], 5: SA[5]}
    Er = {-1: Em1, -2: Em2, -3: Em3, -4: Em4}
    for i in range(6): Er[i] = (Ar[i] + Ar[i-4] - S0(Ar[i-1]) - MAJ(Ar[i-1], Ar[i-2], Ar[i-3])) & M32
    W = {i: (Er[i] - Ar[i-4] - Er[i-4] - S1(Er[i-1]) - CH(Er[i-1], Er[i-2], Er[i-3]) - K[i]) & M32 for i in range(6)}
    mc.n += 201
    w8 = (W8C - (a0 + C4)) & M32
    for l in ls:
        mc.n += 2 + 6
        Ld = Lt[l]; (x14, x15), (y14, y15) = lstar(l)
        Wx = [W[0], W[1], W[2], W[3], W[4], W[5], w6, w7, w8] + MX[9:14] + [x14, x15]
        Wy = [W[0], W[1], W[2], W[3], W[4], W[5], (w6 + D6) & M32, (w7 + D7) & M32, (w8 + D8) & M32] + MY[9:14] + [y14, y15]
        X, Y = new_rows(Ld['tx'], Ld['ty'])
        for i in range(16): X[2][i] = Wx[i]; Y[2][i] = Wy[i]
        ok = True
        for t in range(16, R):
            for (_, _, Ww) in (X, Y): Ww[t] = (s1(Ww[t-2]) + Ww[t-7] + s0(Ww[t-15]) + Ww[t-16]) & M32
            step_rows(X, Y, t); mc.n += ROWCOMP + ROWCHECK + 1
            if t < 22 and not (row_ok(X, Y, t) and x2_ok(X, t)): ok = False; break
        if ok and any(X[0][t] != Y[0][t] or X[1][t] != Y[1][t] for t in range(R - 4, R)): ok = False
        if ok: return l, Wx[:16], Wy[:16]
    return None
_D1C = sum(1 << k for k in (11, 22, 26, 18, 30, 28)); _D1S = (1 << 22) | (1 << 26)
_D2C = sum(1 << k for k in (11, 12, 22, 23, 26, 27, 18, 19, 30, 31, 28, 29)); _D2S = (1 << 11) | (1 << 23) | (1 << 27)
def draw_F7(rng):
    r = rng(); w = r & M32
    if (r >> 32) % 65: return (w & ~_D1C & M32) | _D1S | (((w >> 1) & 1) << 18) | (((w >> 9) & 1) << 30) | ((w & 1) << 28)
    return (w & ~_D2C & M32) | _D2S | (((w >> 1) & 1) << 18) | (((w >> 2) & 1) << 19) | (((w >> 9) & 1) << 30) | (((w >> 10) & 1) << 31) | ((w & 1) << 28) | (((w >> 1) & 1) << 29)
def invert_cv(Av, Ev, W):
    a = {i: Av[i] for i in range(4, 8)}; e = {i: Ev[i] for i in range(4, 8)}
    for i in range(7, -1, -1):
        T1 = (a[i] - S0(a[i-1]) - MAJ(a[i-1], a[i-2], a[i-3])) & M32
        a[i-4] = (e[i] - T1) & M32
        e[i-4] = (T1 - S1(e[i-1]) - CH(e[i-1], e[i-2], e[i-3]) - K[i] - W[i]) & M32
    return [a[-1], a[-2], a[-3], a[-4], e[-1], e[-2], e[-3], e[-4]]
def words_from_cv(cv, a0):
    out = []
    for Sx in (SA, SAy):
        A = {-1: cv[0], -2: cv[1], -3: cv[2], -4: cv[3]}; E = {-1: cv[4], -2: cv[5], -3: cv[6], -4: cv[7]}
        for i in range(14): A[i] = Sx[i]
        A[0] = a0
        for i in range(14): E[i] = (A[i] + A[i-4] - S0(A[i-1]) - MAJ(A[i-1], A[i-2], A[i-3])) & M32
        out.append([(E[i] - A[i-4] - E[i-4] - S1(E[i-1]) - CH(E[i-1], E[i-2], E[i-3]) - K[i]) & M32 for i in range(14)])
    return out
SAy = [trace(CV0, MY, 14)[0][i] for i in range(14)]
IMP = {18: (0x30040c22, 0x20000c02), 19: (1 << 29, 1 << 29)}
PAT = ((0, 0), (0x20040420, 1 << 29), (0x10040822, 0), (0x30000c02, 1 << 29),
       (0x10040820, 0), (0x30000c00, 1 << 29), (0x00000002, 0), (0x20040422, 1 << 29))
L28 = [l for l in range(32) if l not in (0, 2, 16, 18)]
def sfs_trial(rng, Lt, cls=None, env=None, cap=1 << 11, restarts=12, tail_cap=1 << 19, pat=0, bud=None):
    c = rng.below(NCLS) if cls is None else cls; members = env.members(c); a0 = members[rng.below(len(members))]
    LL = FEASIBLE_L if pat > 3 else L28; l = LL[rng.below(len(LL))]; Ld = Lt[l]
    for attempt in range(restarts):
        X, Y = new_rows(Ld['tx'], Ld['ty']); tries = []; dead = False
        for t in range(16, 22):
            m, v, _, _ = CELLS['E'][t]
            if t == 16: m |= 1 << 23; v |= (1 << 23) if pat > 3 else 0
            if t == 17: m |= 1 << 24; v |= (((X[1][16] >> 24) & 1) ^ (1 if pat > 3 else 0)) << 24
            if t in IMP: m |= IMP[t][0]; v |= IMP[t][1] ^ PAT[pat][t - 18]
            dW = (s1(Y[2][t-2]) - s1(X[2][t-2]) + Y[2][t-7] - X[2][t-7] + (T6 if t == 21 else 0)) & M32
            base = (X[0][t-4] + X[1][t-4] + S1(X[1][t-1]) + CH(X[1][t-1], X[1][t-2], X[1][t-3]) + K[t]) & M32
            n = 0
            while True:
                n += 1
                if n > cap: dead = True; break
                X[2][t] = (((rng() & M32) & ~m | v) - base) & M32; Y[2][t] = (X[2][t] + dW) & M32
                step_rows(X, Y, t)
                if row_ok(X, Y, t) and x2_ok(X, t): break
            if dead: break
            tries.append(n)
        if not dead: break
    if dead: return None
    w8x = (W8C - ((a0 + C4) & M32)) & M32
    mw, vw, _, _ = CELLS['W'][22]; n = 0
    while True:
        n += 1
        if n > tail_cap: return None
        if bud is not None:
            bud[0] -= 1
            if bud[0] < 0: return None
        w22 = rng() & M32
        w7 = draw_F7(rng); w6 = (w22 - s1(X[2][20]) - X[2][15] - s0(w7)) & M32
        if not inF(w6, D6, T6): continue
        Xc = [dict(d) for d in X]; Yc = [dict(d) for d in Y]
        Xc[2][6], Xc[2][7], Xc[2][8] = w6, w7, w8x
        Yc[2][6], Yc[2][7], Yc[2][8] = (w6 + D6) & M32, (w7 + D7) & M32, (w8x + D8) & M32
        for t in range(22, R):
            for (_, _, W_) in (Xc, Yc): W_[t] = (s1(W_[t-2]) + W_[t-7] + s0(W_[t-15]) + W_[t-16]) & M32
            step_rows(Xc, Yc, t)
            if t >= 25 and (Xc[0][t] != Yc[0][t] or Xc[1][t] != Yc[1][t]): break
        if R - 1 in Xc[0] and all(Xc[0][t] == Yc[0][t] and Xc[1][t] == Yc[1][t] for t in range(R - 4, R)): break
    tries.append(n)
    W = dict(Xc[2])
    for i in range(5, -1, -1): W[i] = (W[i + 16] - s1(W[i + 14]) - W[i + 9] - s0(W[i + 1])) & M32
    mx = [W[i] for i in range(16)]; my = mx[:6] + [Yc[2][i] for i in range(6, 16)]
    Avar = {i: SA[i] for i in range(14)}; Avar[0] = a0
    Evar = {4: (a0 + C4) & M32, 5: SE[5], 6: SE[6], 7: SE[7]}
    cv = invert_cv(Avar, Evar, W)
    wx, wy = words_from_cv(cv, a0)
    ok = wx == mx[:14] and wy == my[:14] and compress(cv, mx) == compress(cv, my) and mx != my
    tx, ty = trace(cv, mx), trace(cv, my)
    ok = ok and all(row_ok(tx, ty, i, i not in (6, 7)) for i in range(-4, 22)) and all(x2_ok(tx, r) for r in range(8, 22))
    ok = ok and in_G(a0) and c7of(a0) == C7S[c] and mx[8] != MX[8] and inF(mx[6], D6, T6) and inF(mx[7], D7, T7)
    return cv, mx, my, dict(class_index=c, variant_index=members.index(a0), l=l, pattern=pat, checks_passed=int(ok), restarts=attempt, proposals_row16=tries[0], proposals_tail=tries[-1])
class CN: n = 0
class Pl:
    __slots__ = ('v', 'c', 'f')
    def __init__(s, v, c=None, f=0): s.v = v; s.c = c; s.f = f
    def tv(s): return s.v ^ (ONE if s.f else 0)
Z0 = Pl(0, 0); Z1 = Pl(ONE, 1)
def dyn(v): return Pl(v)
def inv(a): return (Z1 if a.c == 0 else Z0) if a.c is not None else Pl(a.v, None, a.f ^ 1)
def xor(a, b):
    if a.c is not None: return b if a.c == 0 else inv(b)
    if b.c is not None: return a if b.c == 0 else inv(a)
    CN.n += 1; return Pl(a.v ^ b.v, None, a.f ^ b.f)
def and_(a, b):
    if a.c is not None: return Z0 if a.c == 0 else b
    if b.c is not None: return Z0 if b.c == 0 else a
    if a.f and b.f: CN.n += 1; return Pl(a.v | b.v, None, 1)
    if not a.f and not b.f: CN.n += 1; return Pl(a.v & b.v)
    CN.n += 2; return Pl(a.tv() & b.tv())
def or_(a, b):
    if a.c is not None: return Z1 if a.c == 1 else b
    if b.c is not None: return Z1 if b.c == 1 else a
    if a.f and b.f: CN.n += 1; return Pl(a.v & b.v, None, 1)
    if not a.f and not b.f: CN.n += 1; return Pl(a.v | b.v)
    CN.n += 2; return Pl(a.tv() | b.tv())
def force(a):
    if a.c is not None or not a.f: return a
    CN.n += 1; return Pl(a.v ^ ONE)
def add(A, B, cin=Z0, need=None):
    n = len(A); out = [None] * n; c = cin; top = max(need) if need is not None else n - 1
    for j in range(top + 1):
        a, b = A[j], B[j]
        if a.c is not None: a, b = b, a
        if b.c is not None:
            xy = a if b.c == 0 else inv(a)
            if need is None or j in need: out[j] = xor(xy, c)
            if j < top: c = and_(a, c) if b.c == 0 else or_(a, c)
        else:
            xy = xor(a, b)
            if need is None or j in need: out[j] = xor(xy, c)
            if j < top: c = xor(a, and_(xy, xor(a, c)))
    return out
def sub(A, B, need=None): return add(A, [inv(b) for b in B], Z1, need)
def scal(s): return [dyn(ONE if (s >> j) & 1 else 0) for j in range(32)]
def bgen(js): return sum(2 if j == 0 else 3 for j in js)
def planes_from_values(vals): return [sum(((v >> j) & 1) << L for L, v in enumerate(vals)) for j in range(32)]
FA, AA = A1 ^ A2, A1 & A2
MASK17, ALWAYS = (int(x, 16) for x in B['masks'].split())
NEEDW = (1, 2, 3, 8, 9, 10, 12, 13, 14, 15, 16, 18, 19, 20, 25, 26, 27, 29, 30, 31)
NEEDF7 = (0, 1, 2, 9, 10, 11, 12, 18, 19, 22, 23, 26, 27, 28, 29, 30, 31)
MB = [j for j in range(32) if (MASK17 >> j) & 1]
NBA = [j for j in range(32) if not (ALWAYS >> j) & 1]
KZB = list(range(29))
def f6_test(w):
    common = or_(xor(w[14], w[18]), xor(w[1], w[12]))
    bcc = or_(or_(xor(w[15], w[19]), inv(xor(w[9], w[26]))), xor(w[2], w[13]))
    X_ = or_(or_(xor(xor(w[16], w[20]), w[31]), inv(xor(xor(w[10], w[27]), w[31]))), xor(xor(w[3], w[14]), w[31]))
    return and_(xor(w[8], w[25]), inv(or_(common, and_(w[29], or_(bcc, and_(w[30], X_))))))
def f7_test(w):
    c1 = or_(or_(xor(w[1], w[18]), xor(w[0], w[28])), xor(w[9], w[30]))
    A = and_(and_(inv(w[11]), w[22]), w[26])
    B = and_(and_(w[11], inv(w[12])), and_(and_(inv(w[22]), w[23]), and_(inv(w[26]), w[27])))
    return and_(inv(c1), or_(A, and_(inv(or_(or_(xor(w[2], w[19]), xor(w[1], w[29])), xor(w[10], w[31]))), B)))
def w6_sums(SP, zq, zCB3, zKZ, zb, need):
    a = [SP[j] if (ALWAYS >> j) & 1 else (or_(SP[j], zb[j]) if (MASK17 >> j) & 1 else zb[j]) for j in range(32)]
    e4 = add(a, [Z1 if (C4 >> j) & 1 else Z0 for j in range(32)], need={j for j in range(32) if (E5 >> j) & 1})
    e3 = sub(zKZ, [SP[j] if ((FA >> j) & 1 and (MASK17 >> j) & 1) else Z0 for j in range(32)], need={j for j in range(32) if not (E5 >> j) & 1})
    W6a = add(zCB3, [and_(SP[j], zq[j]) if (MASK17 >> j) & 1 else Z0 for j in range(32)])
    return sub(W6a, [e4[j] if (E5 >> j) & 1 else e3[j] for j in range(32)], need=need)
def w6_batch(SP, zq, zCB3, zKZ, zb, full=False):
    W = w6_sums(SP, zq, zCB3, zKZ, zb, set(range(32)) if full else set(NEEDW))
    return f6_test({j: W[j] for j in NEEDW}), (W if full else None)
def f6_sub(W, cu):
    Wc = sub(W, [Z1 if (cu >> j) & 1 else Z0 for j in range(32)], need=set(NEEDW))
    return f6_test({j: Wc[j] for j in NEEDW})
def measure_ops():
    r = random.Random(7); zb = {j: dyn(ONE if r.getrandbits(1) else 0) for j in NBA}; w6 = {}; sub_ = {}
    for k, cube in ((0, 0),):
        SP = {j: (Z0 if (cube >> j) & 1 else dyn(r.getrandbits(256))) for j in MB}
        for full in (False, True):
            CN.n = 0; p, W = w6_batch(SP, scal(r.getrandbits(32)), scal(r.getrandbits(32)), scal(r.getrandbits(32)), zb, full); w6[(k, full)] = CN.n + (1 if p.f else 0)
        for cu in (1, 4, 5, 8, 9, 12, 13):
            if cu & ~cube: continue
            CN.n = 0; p = f6_sub(W, cu); sub_[(k, cu)] = CN.n + (1 if p.f else 0)
    C7 = [dyn(r.getrandbits(256)) for j in range(32)]
    CN.n = 0; W = add(C7, scal(r.getrandbits(32)), need=set(NEEDF7)); p = f7_test({j: W[j] for j in NEEDF7}); f7 = CN.n + (1 if p.f else 0)
    return w6, sub_, f7
import random
W6_OPS, SUBF_OPS, F7_OPS = measure_ops()
CTRL_FB = 16
PARTCH = [(0, 11), (11, 11), (22, 11), (33, 11), (44, 11), (55, 9)]
def part_fixed(r): return (1 if r in (0, 3) else 2) + sum((1 if k in (0, 5) else 2) + 1 for k in range(6))
SCAN_FIX = sum(part_fixed(r) for r in range(4))
SCAN_LANE = 8
CLS_LANE = 6
EXTR = (1, 2, 2, 1)
PLACE = 7
GROUP_BODY = 31
PROBE = (11, 12, 12, 12)
SURV_FIX, SURV_LANE, EX_OPS = 11, 7, 34
ZLOADS = len(MB) + len(KZB) + 32 + len(NBA)
SWEEP_OVH = 3 + 2 * ZLOADS
CUBE_CAND = ()
def sp_loads(k): return 2 * (len(MB) - k) + 2
RUN_CU = 7
SPILL = 64
CF_CLASS = 6
CUBE_D = {0: 0}
def cprep_ops(): return 10 + 6 + bgen(range(32)) + bgen(KZB) + bgen(NBA) + 2 * (32 + len(KZB) + len(NBA)) + 1
FB_DET = 2 + 1 + 1 + 2 + 2 + bgen(MB) + 2 * len(MB) - 1 + 81
CT_DET = ((NCLS + 255) // 256) * (2 + bgen(range(32)) + 63 + F7_OPS + 1 + SCAN_FIX)
FIXED = 30 + CTRL_FB + FB_DET + CT_DET
RARE_LOOKUP, RECOMP, ROWCHECK, ROWCOMP = 2, 35, 53, 106
PAD_OPS = 7
def S0pack(a0): return a0 | ((~S0(a0) & M32) << 32)
def entry_of(s): return s | (S0(s) << 32)
class ListData:
    def __init__(self, mask, s):
        Ss = set(s); self.cube = sum(1 << b for b in CUBE_CAND if all((t ^ (1 << b)) in Ss for t in s))
        self.mask = mask; self.s = s; self.n = len(s); self.k = bin(self.cube).count('1')
        reps = [t for t in s if not t & self.cube]; assert len(reps) << self.k == self.n
        self.reps = reps; self.nr = len(reps); self.nb = (self.nr + 255) // 256; self.nl = [min(256, self.nr - 256 * b) for b in range(self.nb)]
        self.planes = []; self.words = []
        for b in range(self.nb):
            lanes = [reps[256 * b + L] if L < self.nl[b] else reps[0] for L in range(256)]
            pv = planes_from_values(lanes); self.planes.append({j: dyn(pv[j]) for j in MB if not (self.cube >> j) & 1})
            self.words.append([sum(entry_of(lanes[64 * r + i]) << (64 * r) for r in range(4)) for i in range(64)])
class Cls:
    def __getitem__(self, ci):
        c7, base, mask, n, _ = klass(ci); return dict(c7=c7, base=base, mask=mask, n=n, lid=ci, BP=S0pack(base))
class Env:
    def __init__(self):
        self.Lt = setup_l(); self.lid = list(range(NCLS)); self.lists = {}; self.cls = Cls()
        c7s = C7S; self.C7B = [[dyn(v) for v in planes_from_values((c7s[256 * b:256 * b + 256] + [c7s[0]] * 256)[:256])] for b in range(NCB)]
        self.build_r16()
    def getlist(self, lid):
        if lid not in self.lists:
            k = klass(lid); self.lists[lid] = ListData(k[2], list(k[4]))
        return self.lists[lid]
    def members(self, ci): return [self.cls[ci]['base'] | s for s in self.getlist(self.lid[ci]).s]
    def memset(self, ci):
        if not hasattr(self, 'ms'): self.ms = {}
        if ci not in self.ms: self.ms[ci] = set(self.members(ci))
        return self.ms[ci]
    def build_r16(self):
        self.LC = {}; self.VA = {}
        for l in FEASIBLE_L:
            L = self.Lt[l]; tx = L['tx']; a12, a13, a14, a15 = (tx[0][i] for i in (12, 13, 14, 15))
            self.LC[l] = dict(C=L['C16'], cxA=(-a12 + S0(a15) + MAJ(a15, a14, a13)) & M32, Ex15=tx[1][15], Ax15=a15)
            self.VA[l] = 0x20000000 | ((~a15) & 0x8000) | (a15 & 0x00800000) | (a15 & 0x02000000)
        ML, VL, MM, VM = E16M & 0xfff, E16V & 0xfff, (E16M >> 12) & 0xfff, (E16V >> 12) & 0xfff
        LOp = [0] * 4096; LOc = [0] * 4096; MID0 = [0] * 4096; MID1 = [0] * 4096
        for l in FEASIBLE_L:
            c = self.LC[l]; Clo = c['C'] & 0xfff; Cmid = (c['C'] >> 12) & 0xfff
            for lo in range(4096):
                t = lo + Clo; el = t & 0xfff
                if (el & ML) == VL and not ((el ^ c['Ex15']) & 0x10): LOp[lo] |= 1 << l
                if t >> 12: LOc[lo] |= 1 << l
            for mid in range(4096):
                for cin, T in ((0, MID0), (1, MID1)):
                    if (((mid + Cmid + cin) & 0xfff) & MM) == VM: T[mid] |= 1 << l
        self.LOw = [LOp[i] | ((LOp[i] & LOc[i]) << 64) for i in range(4096)]; self.MIDw = [MID0[i] | ((MID0[i] ^ MID1[i]) << 64) for i in range(4096)]
    def filt(self, u):
        T = self.LOw[u & 0xfff] & self.MIDw[(u >> 12) & 0xfff]
        return (T ^ (T >> 64)) & ((1 << len(FEASIBLE_L)) - 1)
    def exact(self, u, l):
        c = self.LC[l]; e = (u + c['C']) & M32; A = (e + c['cxA']) & M32
        t = ((e & E16M) ^ E16V) | ((e ^ c['Ex15']) & 0x10) | ((A & 0x22808000) ^ self.VA[l])
        x1, x2, x3 = A ^ (A >> 11), A ^ (A >> 12), A ^ (A >> 9)
        return (t | (((x1 & 0x200) | (x2 & 0x40) | (x3 & 0x100)) ^ 0x240)) == 0, EX_OPS
def r16_ref(Env_, u, l):
    e = (Env_.LC[l]['C'] + u) & M32
    return (e & E16M) == E16V and row16_ok(Env_.Lt[l], e)
class Mc:
    def __init__(self): self.n = 0; self.cat = {}; self.cnt = {}
    def add(self, c, k): self.n += k; self.cat[c] = self.cat.get(c, 0) + k
    def count(self, c, k=1): self.cnt[c] = self.cnt.get(c, 0) + k
def scan_parts(mc, cat, plane, per_lane):
    out = []
    for r in range(4):
        part = (plane >> (64 * r)) & M64
        for (sh, w) in PARTCH:
            c = (part >> sh) & ((1 << w) - 1)
            while c: out.append((r, sh + (c & -c).bit_length() - 1)); c &= c - 1
    mc.add(cat, SCAN_FIX + per_lane * len(out)); return out
def packed_u(Gw, pre):
    Sw = Gw >> 32; E0 = (Gw + bc(pre['e0b'])) & LM; mj = Gw & bc(pre['x12']); ch = (E0 & bc(pre['X'])) ^ bc(pre['Em2'])
    d = (E0 | (E0 << 32)) & M256; S1E = (((d >> 6) ^ (d >> 11)) ^ (d >> 25)) & LM
    W1 = (sum((pre['kap1'] + 1 + (3 << 32)) << (64 * k) for k in range(4)) + Sw - mj - S1E - ch) & LM
    d1 = (W1 | (W1 << 32)) & M256; s0W = (((d1 >> 7) ^ (d1 >> 18)) ^ (W1 >> 3)) & LM
    U = (E0 + s0W + bc64(pre['C'])) & M256
    for k in range(4): assert (U >> (64 * k)) & M64 < 3 << 32
    return U
def process_cv(mc, cv, env, stats, check=None, only=None):
    found = []; x, am2 = cv[0], cv[1]
    plane = 0; cls = []
    for b in range(NCB):
        mc.add('ct', 2 + bgen(range(32)) + 63)
        CN.n = 0; W = add(env.C7B[b], scal((-x) & M32), need=set(NEEDF7)); p = f7_test({j: W[j] for j in NEEDF7}); assert CN.n + (1 if p.f else 0) == F7_OPS
        mc.add('ct', F7_OPS + 1); pb = force(p).v & ((1 << min(256, NCLS - 256 * b)) - 1); plane |= pb << (256 * b)
        if only is not None: pb &= sum(1 << (c - 256 * b) for c in only if 256 * b <= c < 256 * b + 256); mc.add('ct', 1)
        cls += [256 * b + 64 * r + i for (r, i) in scan_parts(mc, 'ct', pb, CLS_LANE)]
    if check: check('classes', cv, None, plane)
    stats['classes'] = stats.get('classes', 0) + len(cls)
    cb = (C6 - am2) & M32; q = A1 ^ x; CB2 = (cb + (A1 & x)) & M32; KXA = (K3C - AA + x) & M32
    mc.add('fb', FB_DET)
    zq = scal(q); zqd = {j: (zq[j] if (MASK17 >> j) & 1 else Z0) for j in range(32)}
    pre = cv_pre(Mach(), cv); mems = []
    for ci in cls:
        c = env.cls[ci]; lst = env.getlist(c['lid']); base = c['base']; B = lst.cube; k = lst.k
        CB3 = (CB2 + (base & q)) & M32; KZ = (KXA - (base & FA)) & M32
        mc.add('cprep', cprep_ops() + CF_CLASS); mc.count('cls_l%d' % c['lid']); zCB3 = scal(CB3); zKZ = scal(KZ); zb = {j: dyn(ONE if (base >> j) & 1 else 0) for j in NBA}
        I = q & B; Q0 = B ^ I; m = 1 << bin(I).count('1'); full = Q0 != 0; wst = {}
        def gather(pv, cu, nl, b):
            BPc = c['BP'] ^ CUBE_D[cu]; mc.count('planes')
            for (r, i) in scan_parts(mc, 'scan', pv, SCAN_LANE):
                e = ((lst.words[b][i] >> (64 * r)) & M64) ^ BPc; mc.count('rep_r%d_m%d' % (r, m))
                if not I: mc.add('member', EXTR[r] + PLACE); mems.append((e, ci, 0))
                else:
                    mc.add('member', EXTR[r] + 12 * m - 2); mems.append((e, ci, 0)); ii = 0
                    while True:
                        ii = (ii - I) & I
                        if not ii: break
                        mems.append((e ^ CUBE_D[ii], ci, 0))
        for sw in range((lst.nb + 1) // 2):
            mc.add('sweep', SWEEP_OVH); mc.count('sweeps')
            for b in [b for b in (2 * sw, 2 * sw + 1) if b < lst.nb]:
                mc.add('sweep', sp_loads(k)); mc.count('mainb_k%d_f%d' % (k, full)); SP = dict(lst.planes[b]); SP.update({bb: Z0 for bb in CUBE_CAND if (B >> bb) & 1})
                CN.n = 0; p, W = w6_batch(SP, zqd, zCB3, zKZ, zb, full); assert CN.n + (1 if p.f else 0) == W6_OPS[(k, full)]
                mc.add('w6', W6_OPS[(k, full)]); pv = force(p).v
                if lst.nl[b] < 256: pv &= (1 << lst.nl[b]) - 1; mc.add('w6', 1); mc.count('partial')
                if full: wst[b] = W; mc.add('spill', SPILL); mc.count('spills')
                if check: check('plane', cv, (ci, b, 0), pv)
                mc.count('runs_l%d' % c['lid']); gather(pv, 0, lst.nl[b], b)
        if full:
            for b in range(lst.nb):
                mc.add('spill', SPILL); mc.count('spills'); cu = 0
                while True:
                    cu = (cu - Q0) & Q0
                    if not cu: break
                    mc.add('runs', RUN_CU); mc.count('subb_k%d_cu%d' % (k, cu)); CN.n = 0; p = f6_sub(wst[b], cu); assert CN.n + (1 if p.f else 0) == SUBF_OPS[(k, cu)]
                    mc.add('w6', SUBF_OPS[(k, cu)]); pv = force(p).v
                    if lst.nl[b] < 256: pv &= (1 << lst.nl[b]) - 1; mc.add('w6', 1); mc.count('partial')
                    if check: check('plane', cv, (ci, b, cu), pv)
                    mc.count('runs_l%d' % c['lid']); gather(pv, cu, lst.nl[b], b)
    stats['pairs'] = stats.get('pairs', 0) + len(mems); stats['goodset'] = {(m[1], m[0] & M32) for m in mems}
    for g in range(0, len(mems), 4):
        grp = mems[g:g + 4]
        if len(grp) < 4: mc.add('member', PAD_OPS); mc.count('pad', 4 - len(grp)); grp = grp + [grp[-1]] * (4 - len(grp))
        Gw = 0
        for k in range(4): Gw |= grp[k][0] << (64 * k)
        U = packed_u(Gw, pre); mc.add('group', GROUP_BODY); mc.count('groups')
        for k in range(4):
            mc.add('probe', PROBE[k]); u = (U >> (64 * k)) & M32; G = env.filt(u)
            if check: check('filt', cv, (grp[k], u), G)
            if not G: continue
            mc.add('surv', SURV_FIX); mc.count('survlanes'); ls = []
            for l in FEASIBLE_L:
                if (G >> l) & 1:
                    ok, ops = env.exact(u, l); mc.add('surv', SURV_LANE + ops); mc.count('survl')
                    if ok: ls.append(l)
            if ls:
                a0 = grp[k][0] & M32; stats['r16'] = stats.get('r16', 0) + 1; mc.add('rare', 1 + RARE_LOOKUP)
                w6, w7 = recompute_w67(Mach(), a0, x, am2); mc.add('rare', RECOMP)
                r = step3b(mc, cv, a0, w6, w7, ls, env.Lt)
                if r: found.append((a0, r))
    return found
def u_ref(cv, a0):
    Ar = {-1: cv[0], -2: cv[1], -3: cv[2], -4: cv[3], 0: a0}; Er = {-1: cv[4], -2: cv[5], -3: cv[6], -4: cv[7]}
    Er[0] = (Ar[0] + Ar[-4] - S0(Ar[-1]) - MAJ(Ar[-1], Ar[-2], Ar[-3])) & M32
    W0 = (Er[0] - Ar[-4] - Er[-4] - S1(Er[-1]) - CH(Er[-1], Er[-2], Er[-3]) - K[0]) & M32
    Er[1] = (A1 + Ar[-3] - S0(a0) - MAJ(a0, Ar[-1], Ar[-2])) & M32
    W1 = (Er[1] - Ar[-3] - Er[-3] - S1(Er[0]) - CH(Er[0], Er[-1], Er[-2]) - K[1]) & M32
    return (W0 + s0(W1)) & M32
def online_trial(rng, env, max_fb=64, sample=12, ncls=3):
    bad = dict(cls=0, plane=0, goodset=0, addr=0, row16=0, cells=0); st = dict(); mc = Mc(); firstpair = []; nprobe = [0]
    def check(kind, cv, a, b):
        if kind == 'classes':
            for c in range(NCLS): bad['cls'] += ((b >> c) & 1) != int(F7((C7S[c] - cv[0]) & M32))
            bad['cls'] += (b >> NCLS) != 0
        elif kind == 'plane':
            ci, bi, cc = a; lst = env.getlist(env.cls[ci]['lid']); base = env.cls[ci]['base']
            for L in range(256):
                want = int(F6(w6of(base | lst.reps[256 * bi + L] | cc, cv[0], cv[1]))) if L < lst.nl[bi] else 0
                bad['plane'] += ((b >> L) & 1) != want
        else:
            (ent, ci, idx), u = a; G = b; a0 = ent & M32; nprobe[0] += 1
            bad['addr'] += u != u_ref(cv, a0) or a0 not in env.memset(ci)
            if G or nprobe[0] % 16 == 0:
                for l in FEASIBLE_L:
                    r = r16_ref(env, u, l); bad['row16'] += (r and not (G >> l) & 1) or env.exact(u, l)[0] != r
    for f in range(max_fb):
        w = first_block(Mach(), rng); cv = compress(IV, w); st['fb'] = st.get('fb', 0) + 1; mc.add('fixed', 30 + CTRL_FB)
        pc = [c for c in range(NCLS) if F7((C7S[c] - cv[0]) & M32)]
        if not pc: mc.add('fixed', FB_DET + CT_DET); continue
        use = pc[:ncls]; st['m0'] = w
        found = process_cv(mc, cv, env, st, check, use)
        want = {(c, a0) for c in use for a0 in env.members(c) if F6(w6of(a0, cv[0], cv[1]))}
        got = st['goodset']; bad['goodset'] += want != got
        for (c, a0) in sorted(got)[:2]:
            wx, wy = words_from_cv(cv, a0)
            if not (inF(wx[7], D7, T7) and inF(wx[6], D6, T6) and F7((c7of(a0) - cv[0]) & M32)): bad['cells'] += 1
            if len(firstpair) < sample:
                for l in FEASIBLE_L:
                    (x14, x15), (y14, y15) = lstar(l); tx = trace(cv, wx + [x14, x15], 16); ty = trace(cv, wy + [y14, y15], 16)
                    if not all(row_ok(tx, ty, i, i not in (6, 7)) for i in range(-4, 16)): bad['cells'] += 1
                firstpair.append((wx, wy))
        break
    if firstpair: firstpair[0] = (st['m0'],) + firstpair[0]
    obs = dict(first_blocks=st.get('fb', 0), classes=st.get('classes', 0), good_pairs=st.get('pairs', 0), groups=mc.cnt.get('groups', 0), survivors=mc.cnt.get('survl', 0),
               row16_pairs=st.get('r16', 0), counted_ops=mc.n, class_lane_mismatches=bad['cls'], pass_lane_mismatches=bad['plane'], goodset_mismatches=bad['goodset'],
               address_mismatches=bad['addr'], row16_mismatches=int(bad['row16']), cell_mismatches=bad['cells'], pairs_cell_checked=len(firstpair))
    return (firstpair[0] if firstpair else None), obs
def detect(env, cv, mx, my, c, a0):
    mc = Mc(); st = dict(); fnd = process_cv(mc, cv, env, st, None, [c])
    return int(any(f[0] == a0 and f[1][1] == mx and f[1][2] == my for f in fnd)), mc.n
def run_request(req):
    env = Env(); eid = req['experiment_id']; out = []; bud = [1 << 20]
    for tr in req['trials']:
        t = tr['trial']; rng = Shake(eid + '|' + tr['seed']); rec = dict(trial=t, message_a_hex=None, message_b_hex=None)
        if eid.startswith('a0-sfs') and t < 8:
            r = sfs_trial(rng, env.Lt, (7 * t) % NCLS, env, pat=4 + t % 4, bud=bud)
            if r:
                cv, mx, my, obs = r
                if True:
                    a0v = env.members(obs['class_index'])[obs['variant_index']]
                    obs['detected_by_counted_program'], obs['counted_ops'] = detect(env, cv, mx, my, obs['class_index'], a0v)
                rec['message_a_hex'] = struct.pack('>24I', *(cv + mx)).hex(); rec['message_b_hex'] = struct.pack('>24I', *(cv + my)).hex(); rec['observations'] = obs
        elif eid.startswith('a0-online') and t < 8:
            pair, obs = online_trial(rng, env); rec['observations'] = obs
            if pair and obs['class_lane_mismatches'] == obs['pass_lane_mismatches'] == obs['goodset_mismatches'] == obs['address_mismatches'] == obs['row16_mismatches'] == obs['cell_mismatches'] == 0:
                m0, wx, wy = pair; (x14, x15), (y14, y15) = lstar(13)
                rec['message_a_hex'] = struct.pack('>32I', *(m0 + wx + [x14, x15])).hex(); rec['message_b_hex'] = struct.pack('>32I', *(m0 + wy + [y14, y15])).hex()
        out.append(rec)
    return dict(schema_version=1, trials=out)
C_REF = 2644
_ST = json.loads(B['stats']); P7 = Fr(_ST['F7'], 1 << 32); P6 = Fr(_ST['F6'], 1 << 32); R16F = Fr(_ST['R16'], 1 << 32)
NSURV = len(FEASIBLE_L); MU = Fr(NSURV, 256); PNZ = Fr(_ST['PNZ'], 1 << 24)
Q3_LOG2 = float(B['q3']); SLACK = Fr(1, 1 << 12); HIST = json.loads(B['hist']); NVAR = sum(n * c for n, c in HIST)
PRICE = 2 ** 21.427; T_AC = 8 * 4044 + 29.45; T_AS = 2 * 2188.09 + 0.37; T_PRE = 90.0; DEV_UNITS = 2 ** 42
AC_UNITS = int(T_AC * PRICE); AS_UNITS = int(T_AS * PRICE); PRE_OPS = int(T_PRE * PRICE * C_REF)
CLASS_TYPES = [(n, 0, c) for n, c in HIST]
from math import comb
def lane_costs(nls): return sum(SCAN_LANE + EXTR[L // 64] for nl in nls for L in range(nl))
def memcost(j): return PLACE if j == 0 else 12 * (1 << j) - 2
def subsets(mask): return [s for s in range(16) if s & ~mask == 0]
def class_det(n, k, Q0):
    nr = n >> k; nb = (nr + 255) // 256; nsw = (nb + 1) // 2; part = 1 if nr % 256 else 0; full = Q0 != 0
    tot = cprep_ops() + CF_CLASS + nsw * SWEEP_OVH + nb * (sp_loads(k) + W6_OPS[(k, full)] + SCAN_FIX) + part
    if full:
        tot += 2 * nb * SPILL
        for cu in subsets(Q0):
            if cu: tot += nb * (RUN_CU + SUBF_OPS[(k, cu)] + SCAN_FIX) + part
    return tot
def class_run_cost(n, k, Q0):
    nr = n >> k; nb = (nr + 255) // 256; nls = [min(256, nr - 256 * b) for b in range(nb)]; j = k - bin(Q0).count('1')
    return lane_costs(nls) + nr * memcost(j)
def class_expected(n, k):
    cube = {3: 0xd, 1: 0x1, 0: 0}[k]; tot = Fr(0)
    for Q0 in subsets(cube): tot += Fr(1, 1 << k) * (class_det(n, k, Q0) + (1 << bin(Q0).count('1')) * P6 * class_run_cost(n, k, Q0))
    return tot
def class_max(n, k):
    cube = {3: 0xd, 1: 0x1, 0: 0}[k]
    return max(class_det(n, k, Q0) + (1 << bin(Q0).count('1')) * class_run_cost(n, k, Q0) for Q0 in subsets(cube))
def expected():
    ct_var = CLS_LANE * NCLS * P7; perclass = pairs = Fr(0)
    for (n, k, cnt) in CLASS_TYPES:
        perclass += cnt * P7 * class_expected(n, k); pairs += cnt * P7 * P6 * n
    groups = (pairs + 3) / 4; grp = groups * (GROUP_BODY + sum(PROBE)) + PAD_OPS; lanes = 4 * groups
    surv = lanes * (PNZ * SURV_FIX + MU * (SURV_LANE + EX_OPS))
    c3b_row = ROWCOMP + ROWCHECK + 1; c3b_pair = 201 + RECOMP + 1 + RARE_LOOKUP; c3b_l = 2 + 6 + 2 * c3b_row
    rare = lanes * R16F * (c3b_pair + c3b_l + 19 * Fr(1, 512) * c3b_row)
    return dict(ct_var=ct_var, perclass=perclass, grp=grp, surv=surv, rare=rare, g=pairs, vbar=ct_var + perclass + grp + surv + rare)
def vmax_fb_value():
    tot = Fr(0); c3b_row = ROWCOMP + ROWCHECK + 1; c3b_pair = 201 + RECOMP + 1 + RARE_LOOKUP; c3b_l = 2 + 6 + 2 * c3b_row
    for (n, k, cnt) in CLASS_TYPES: tot += cnt * class_max(n, k)
    lanes = NVAR + 3
    tot += Fr(lanes, 4) * (GROUP_BODY + sum(PROBE)) + PAD_OPS + lanes * (SURV_FIX + NSURV * (SURV_LANE + EX_OPS)) + lanes * Fr(11, 10) * (c3b_pair + NSURV * (c3b_l + 19 * c3b_row))
    return tot + 24 + CLS_LANE * NCLS
DISC = 8.5
def ledger(q3_log2=Q3_LOG2, show=True, ac_units=AC_UNITS, slack=SLACK, pre_ops=PRE_OPS, as_units=AS_UNITS, dev_units=DEV_UNITS, fin=1600):
    C = C_REF; ex = expected(); g, vbar = ex['g'], ex['vbar']; vmax_fb = vmax_fb_value()
    fl = math.floor(q3_log2); q3ex = Fr(2) ** fl * Fr(math.floor(2 ** (q3_log2 - fl) * 2 ** 40), 2 ** 40)
    getcontext().prec = 60
    def mu_req(pcap):
        x = Decimal('0.61') - Decimal(pcap.numerator) / Decimal(pcap.denominator) - Decimal(2) ** -60
        return Fr(int(math.floor(-x.ln() / (Decimal(1) - (Decimal(-DISC) * Decimal(2).ln()).exp()) * 10 ** 8)) + 1, 10 ** 8)
    pa = Fr(1, 1 << 24)
    for _ in range(8):
        XREQ = mu_req(pa); nfb = int(-(-XREQ // (g * len(FEASIBLE_L) * q3ex))); pcap = Fr(vmax_fb) / (slack * slack * nfb * vbar); pa2 = Fr(math.ceil(pcap * 10 ** 8), 10 ** 8)
        if pa2 == pa: break
        pa = pa2
    assert pcap <= pa and XREQ >= mu_req(pa)
    VMAX = math.ceil((1 + slack) * nfb * vbar)
    T = Fr(ac_units + as_units + dev_units) + nfb + Fr(nfb * FIXED + VMAX + math.ceil(vmax_fb) + pre_ops + fin, C) + 6
    tl = math.ceil(math.log2(T) * 1e5) / 1e5; p5 = int(round(tl * 100000))
    out = dict(g=float(g), vbar=float(vbar), fixed=FIXED, mu_req=float(XREQ), nfb=nfb, log2_nfb=math.log2(nfb), VMAX=VMAX, vmax_fb=float(vmax_fb), pcap_log2=math.log2(float(pcap)),
               time_log2=tl, log2_T=math.log2(T), T_num=T.numerator, T_den=T.denominator,
               tight_up=T.numerator ** 100000 <= (2 ** p5) * T.denominator ** 100000, tight_down=T.numerator ** 100000 > (2 ** (p5 - 1)) * T.denominator ** 100000,
               success_lower_bound=1 - math.exp(-(1 - 2.0 ** -DISC) * float(XREQ)) - float(pa) - 2.0 ** -60, pcap_assumed=pa,
               per_fb_units=float(1 + Fr(FIXED, C) + vbar / C), preprocessing_log2=math.log2(ac_units + as_units + dev_units + Fr(pre_ops, C)), slack=str(slack),
               parts={k: float(v) for k, v in ex.items() if k not in ('g', 'vbar')})
    assert out['tight_up'] and out['tight_down'] and out['success_lower_bound'] > 0.39
    if show:
        for k, v in out.items(): print('%-18s %s' % (k, v))
    return out
def selftest():
    rr = random.Random(1); env = Env(); bad = 0
    tot = 0
    for ci in SAMP:
        c7, base, mask, n, _ = klass(ci); mem = env.members(ci); tot += len(mem)
        bad += len(mem) != n or any((not in_G(a)) or c7of(a) != c7 or (a & mask) != (a ^ base) for a in mem)
    print('sample classes %d, variants %d, mismatches %d' % (len(SAMP), tot, bad))
    print('W6_OPS (k, full):', W6_OPS, 'SUBF_OPS:', SUBF_OPS, 'F7_OPS', F7_OPS, 'FIXED', FIXED)
    bad = 0
    for _ in range(20000): bad += not F7(draw_F7(Shake(str(rr.random()))))
    print('F7 sampler violations', bad)
    bad = tot = 0
    for ci in SAMP:
        lst = env.getlist(env.lid[ci]); base = env.cls[ci]['base']; B = lst.cube
        for _ in range(60):
            x = rr.getrandbits(32); am2 = rr.getrandbits(32); I = (A1 ^ x) & B
            for t_ in rr.sample(lst.reps, 8):
                for f in range(16):
                    if f & ~B: continue
                    tot += 1; bad += w6of(base | t_ | f, x, am2) != w6of(base | t_ | (f & ~I), x, am2)
    print('invariance of W6x under the flips of the bits of I: %d checks, %d mismatches' % (tot, bad))
    bad = tot = ps = 0
    for ci in SAMP:
        lst = env.getlist(env.lid[ci]); base = env.cls[ci]['base']; B = lst.cube
        for _ in range(3):
            x = rr.getrandbits(32); am2 = rr.getrandbits(32); cb = (C6 - am2) & M32; q = A1 ^ x
            zq = scal(q); zqd = {j: (zq[j] if (MASK17 >> j) & 1 else Z0) for j in range(32)}
            zb = {j: dyn(ONE if (base >> j) & 1 else 0) for j in NBA}
            zC = scal((cb + (A1 & x) + (base & q)) & M32); zK = scal((K3C - AA + x - (base & FA)) & M32); Q0 = B & ~q
            for b in range(lst.nb):
                SP = dict(lst.planes[b]); SP.update({bb: Z0 for bb in CUBE_CAND if (B >> bb) & 1})
                for full in (False, True):
                    CN.n = 0; p, W = w6_batch(SP, zqd, zC, zK, zb, full); assert CN.n + (1 if p.f else 0) == W6_OPS[(lst.k, full)]; pv = force(p).v
                    for L in range(lst.nl[b]):
                        e = F6(w6of(base | lst.reps[256 * b + L], x, am2)); tot += 1; ps += e; bad += e != bool((pv >> L) & 1)
                for cu in subsets(Q0):
                    if not cu: continue
                    CN.n = 0; p = f6_sub(W, cu); assert CN.n + (1 if p.f else 0) == SUBF_OPS[(lst.k, cu)]; pv = force(p).v
                    for L in range(lst.nl[b]):
                        e = F6(w6of(base | lst.reps[256 * b + L] | cu, x, am2)); tot += 1; ps += e; bad += e != bool((pv >> L) & 1)
    print('w6 plane lanes %d, F6 passes %d, mismatches %d' % (tot, ps, bad))
    bad = tot = 0
    for _ in range(200):
        x = rr.getrandbits(32) if rr.random() < 0.5 else (C7S[rr.randrange(NCLS)] - draw_F7(Shake(str(rr.random())))) & M32
        pv = 0
        for b in range(NCB):
            W = add(env.C7B[b], scal((-x) & M32), need=set(NEEDF7)); pv |= (force(f7_test({j: W[j] for j in NEEDF7})).v & ((1 << min(256, NCLS - 256 * b)) - 1)) << (256 * b)
        for c in range(NCLS): tot += 1; bad += ((pv >> c) & 1) != int(F7((C7S[c] - x) & M32))
    print('class-test lanes %d, mismatches %d' % (tot, bad))
    bad = nm = 0
    for _ in range(300):
        u = rr.getrandbits(32); G = env.filt(u)
        for l in FEASIBLE_L:
            r = r16_ref(env, u, l); nm += r; bad += env.exact(u, l)[0] != r or (r and not (G >> l) & 1)
    for _ in range(6000):
        l = rr.choice(FEASIBLE_L); e = (rr.getrandbits(32) & ~E16M & M32) | E16V; u = (e - env.LC[l]['C']) & M32; G = env.filt(u)
        r = r16_ref(env, u, l); nm += r; bad += env.exact(u, l)[0] != r or (r and not (G >> l) & 1)
    print('row-16 checks: members seen %d, mismatches %d' % (nm, bad))
    bad = tot = 0; ext = [0, 1, M32, M32 - 1, 1 << 31, (1 << 31) - 1]
    for _ in range(100):
        cv = [rr.choice(ext) if rr.random() < 0.3 else rr.getrandbits(32) for _ in range(8)]; pre = cv_pre(Mach(), cv)
        ci = rr.choice(SAMP); mem = env.members(ci); chunk = [rr.choice(mem) for _ in range(4)]
        U = packed_u(sum(S0pack(a) << (64 * k) for k, a in enumerate(chunk)), pre)
        for k, a0 in enumerate(chunk): tot += 1; bad += ((U >> (64 * k)) & M64) % (1 << 32) != u_ref(cv, a0)
    print('packed u lanes %d, mismatches %d' % (tot, bad))
    mx = max(S0(a) for c in SAMP for a in env.members(c)); print('max S0 over the family variants %#x' % mx, mx <= 0xffffff58)
def family():
    import collections as co
    h = co.Counter(); o = 0; a = M32
    mx = 0
    for ci in range(NCLS): c = klass(ci); h[c[3]] += 1; o |= c[2]; a &= c[2]; assert c[3] >= 3456; mx = max(mx, max(S0(c[1] | t) for t in c[4]))
    print('classes %d variants %d' % (NCLS, sum(n * c for n, c in h.items())), 'hist ok', sorted(h.items()) == [tuple(x) for x in HIST], 'masks %x %x' % (o, a), (o, a) == (MASK17, ALWAYS), 'max S0 %#x' % mx, mx <= 0xffffff58)
def attack(nfb, vmax, seed='attack'):
    env = Env(); rng = Shake(seed); V = 0
    for f in range(nfb):
        w = first_block(Mach(), rng); cv = compress(IV, w); mc = Mc()
        for (a0, (l, bx, by)) in process_cv(mc, cv, env, {}):
            ma, mb = struct.pack('>32I', *(w + bx)), struct.pack('>32I', *(w + by))
            if ma != mb and digest(ma) == digest(mb): return ma, mb
        V += mc.n
        if V > vmax: return None
    return None
def memory_bytes(env=None):
    env = env or Env(); W = 32; lists = list({(L.mask, tuple(L.s)): L for L in (env.getlist(l) for l in range(NCLS))}.values())
    tab = dict(
        s_planes=sum(sum(len(p) for p in L.planes) for L in lists) * W, s_entries=sum(L.nb for L in lists) * 64 * W, cube_deltas=8 * W, sum_spill=224 * W, c7_planes=32 * NCB * W,
        lo_table=4096 * W, mid_table=4096 * W, scan_table=2048 * W, class_descriptors=NCLS * 4 * W, row16_constants=len(FEASIBLE_L) * 4 * W,
        z_planes=ZLOADS * W, characteristic_and_Lstar=1280 * W, chaining_value_constants=64 * W, code=1 << 16)
    return tab, sum(tab.values())
SAMP = tuple(sorted(set(int(i * (NCLS - 1) / 7) for i in range(8))))
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'ledger': ledger()
    elif len(sys.argv) > 3 and sys.argv[1] == 'attack': r = attack(int(sys.argv[2]), int(sys.argv[3])); print('collision found' if r else 'no collision (cap reached)', r)
    elif len(sys.argv) > 1 and sys.argv[1] == 'memory':
        tab, tot = memory_bytes()
        for k, v in tab.items(): print('%-26s %9d' % (k, v))
        print('total %d bytes = 2^%.4f (claimed memory bound 2^29)' % (tot, math.log2(tot)))
    elif len(sys.argv) > 1 and sys.argv[1] == 'selftest': selftest()
    elif len(sys.argv) > 1 and sys.argv[1] == 'family': family()
    else: sys.stdout.write(json.dumps(run_request(json.loads(sys.stdin.read())), separators=(',', ':')))
