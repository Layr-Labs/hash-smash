#!/usr/bin/env python3
# vt38.py - 38-step SHA-256 variant-table attack: reference construction, counted program (levers: proof.md Appendix C),
# experiments (stdin JSON -> stdout JSON), self-test (argument "selftest").  ePrint 2026/1120 Tables 3-5.
import sys, json, hashlib, struct, math, random, zlib, base64
from fractions import Fraction as F

M = 0xffffffff
K = [0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,
     0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,
     0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,
     0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb]
IV = [0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19]
R = 38
def ror(x, n): return ((x >> n) | (x << (32 - n))) & M
def S0(x): return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22)
def S1(x): return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25)
def s0(x): return ror(x, 7) ^ ror(x, 18) ^ (x >> 3)
def s1(x): return ror(x, 17) ^ ror(x, 19) ^ (x >> 10)
def CH(x, y, z): return (x & y) ^ (~x & z & M)
def MAJ(x, y, z): return (x & y) ^ (x & z) ^ (y & z)

def compress(cv, w16):
    w = list(w16)
    for i in range(16, R): w.append((s1(w[i-2]) + w[i-7] + s0(w[i-15]) + w[i-16]) & M)
    a, b, c, d, e, f, g, h = cv
    for i in range(R):
        t1 = (h + S1(e) + CH(e, f, g) + K[i] + w[i]) & M; t2 = (S0(a) + MAJ(a, b, c)) & M
        a, b, c, d, e, f, g, h = (t1 + t2) & M, a, b, c, (d + t1) & M, e, f, g
    return [(x + y) & M for x, y in zip(cv, (a, b, c, d, e, f, g, h))]

def trace(cv, w16):
    """A[i], E[i] (i = -4..R-1) and W[0..R-1] (step i: proof.md Section 1)."""
    A = {-1: cv[0], -2: cv[1], -3: cv[2], -4: cv[3]}; E = {-1: cv[4], -2: cv[5], -3: cv[6], -4: cv[7]}
    W = list(w16)
    for i in range(16, R): W.append((s1(W[i-2]) + W[i-7] + s0(W[i-15]) + W[i-16]) & M)
    for i in range(R):
        E[i] = (A[i-4] + E[i-4] + S1(E[i-1]) + CH(E[i-1], E[i-2], E[i-3]) + K[i] + W[i]) & M
        A[i] = (E[i] - A[i-4] + S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])) & M
    return A, E, W

# Table 3, MSB first (unlisted rows '='); x = message printed second; u, n = (x, y) bits (1, 0), (0, 1); '+': E_i[b] = E_{i-1}[b].
CHAR = dict(
 A={7:'=nu=============================',8:'=========n=====n====n======u====',11:'====================u=======un==',
    12:'=u===n====n======u===nu=======n=',13:'==n============n================',14:'====u=========nn========u==u====',
    15:'======n=u=======n===============',17:'==u============================='},
 E={5:'+++=============================',6:'+++=1====0==+1=====0+===1==1====',7:'uuu=0+1=11=0+00====1+===0==00=01',
    8:'100=u+010n=1nu01=01nu=00n11u1=01',9:'11000u1=n11u0000101101110=01u0uu',10:'==1010=01u00001u=010u=101==10111',
    11:'1=n000=0111100101unn00011+111u10',12:'01nuuu=110n111nu000100100+010u1n',13:'00110101110=000u00111nuu+nnnu1n1',
    14:'=010n0===00===1n=11+0100+1110001',15:'=1==1=1==0=1==11===+u011n1011=1=',16:'=u==10===n===+u1===n0=u=1==+====',
    17:'=0=====+00===+0=+==01=0=0==+====',18:'=0=====+01===n1=+==1==1===0u====',19:'==11===nn====1==n===010===11==0=',
    20:'==1====00====1==0==========1====',21:'==u====10=======1===10==========',22:'==0=============================',
    23:'==1============================='},
 W={7:'==n=============================',8:'=====u===u==========n===========',9:'==u=============================',
    10:'=====n=u=======n===n==n=n=n=u=u=',11:'============u======u=u==========',15:'=====u===n==========n===========',
    16:'==u=============================',23:'=====1=uu=====1=u=1=============',25:'==n============================='})
# Table 4 conditions in rows >= 16 (member x); W25[4]=W25[9] read as W25[4]=W25[6].
TWOBIT = [('A',14,15,0,'A',16,15),('A',14,23,0,'A',16,23),('A',14,25,0,'A',16,25),('A',15,4,0,'A',16,4),('A',15,7,0,'A',16,7),
    ('A',15,16,1,'A',16,16),('A',15,17,0,'A',16,17),('A',15,27,0,'A',16,27),('A',15,29,0,'A',16,29),('A',16,15,0,'A',17,15),
    ('A',16,23,0,'A',17,23),('A',16,25,0,'A',17,25),('A',17,9,0,'A',17,20),('A',17,6,0,'A',17,18),('A',17,8,0,'A',17,17),
    ('A',16,29,0,'A',18,29),('A',18,29,0,'A',19,29),('E',16,4,1,'E',16,23),('E',16,3,1,'E',16,8),('E',16,14,0,'E',16,28),
    ('E',16,4,0,'E',17,4),('E',16,18,0,'E',17,18),('E',18,0,1,'E',18,13),('E',17,15,0,'E',18,15),('E',17,24,0,'E',18,24),
    ('E',19,6,1,'E',19,19),('E',19,20,0,'E',19,2),('E',21,2,0,'E',21,16),('W',16,1,1,'W',16,12),('W',16,20,1,'W',16,27),
    ('W',16,8,0,'W',16,25),('W',16,14,0,'W',16,18),('W',16,4,1,'W',16,6),('W',16,22,1,'W',16,31),('W',23,0,1,'W',23,30),
    ('W',23,1,1,'W',23,31),('W',23,14,0,'W',23,21),('W',23,16,0,'W',23,25),('W',25,4,0,'W',25,6),('W',25,22,0,'W',25,31),
    ('W',25,20,0,'W',25,27)]
def _h(s): return [int(t, 16) for t in s.split()]
# Table 5: CV, M (member y), M' (member x).
PCV = _h('cd278980 1b12a052 b87cc8a6 a9e059c5 c9c3db85 6ca4b5b5 63d13ac1 c0329f1e')
PMY = _h('48fc271b 9fca20cd cc89f96f fc40396f 8b328cb4 6b91ef78 97f9b767 e2450045 3b016f58 de9804cb 66a99ea5 0ce30b8d a28cd15a 77a1e994 d28e48a0 9b5f6dbb')
PMX = _h('48fc271b 9fca20cd cc89f96f fc40396f 8b328cb4 6b91ef78 97f9b767 c2450045 3f416758 fe9804cb 63a88c0f 0ceb1f8d a28cd15a 77a1e994 d28e48a0 9f1f65bb')

def cell(s):
    m = v = d = p = 0
    for c, y in enumerate(s):
        b = 31 - c
        if y in '01un': m |= 1 << b
        if y in '1u': v |= 1 << b
        if y in 'un': d |= 1 << b
        if y == '+': p |= 1 << b
    return m, v, d, p
CELL = {k: [cell(CHAR[k].get(i, '=' * 32)) for i in range(R)] for k in 'AEW'}
PLUS = [0] + [CELL['E'][i][3] & CELL['E'][i-1][3] for i in range(1, R)]
XROW = {}
for c in TWOBIT: XROW.setdefault(max(c[1], c[5]), []).append(c)

def rowok(tx, ty, i, wcell=True):
    """Row i: cells, XOR differences, '+', W cell if wcell, conditions keyed at row i (member x)."""
    (Ax, Ex, Wx), (Ay, Ey, Wy) = tx, ty
    for k, x, y in (('A', Ax[i], Ay[i]), ('E', Ex[i], Ey[i])) + ((('W', Wx[i], Wy[i]),) if wcell else ()):
        m, v, d, _ = CELL[k][i]
        if x & m != v or x ^ y != d: return False
    if (Ex[i] ^ Ex[i-1]) & PLUS[i]: return False
    V = {'A': Ax, 'E': Ex, 'W': Wx}
    for k1, i1, b1, ne, k2, i2, b2 in XROW.get(i, ()):
        if ((V[k1][i1] >> b1) ^ (V[k2][i2] >> b2)) & 1 != ne: return False
    return True

TX = trace(PCV, PMX); TY = trace(PCV, PMY)
D7 = 0x20000000; T7 = 0x03bff800; DW16 = 0x20000000
def inF7(w): return (s0((w + D7) & M) - s0(w)) & M == T7
GBASE, GFREE = 0x35f29010, (0, 2, 10, 13, 19)
G = sorted(GBASE | sum(1 << b for j, b in enumerate(GFREE) if (k >> j) & 1) for k in range(32))
DIFF = {i: ((TX[2][i] - TY[2][i]) & M, (s0(TX[2][i]) - s0(TY[2][i])) & M) for i in (8, 9, 10, 11)}

# Embedded (zlib + base85, LE): A2 list, A0 set, a valid (A1, A2 index) per A0, 512 sample variants, 4 SFS successes.
A2_D = 'c-jrl-OYkp0tL`QYypz{HuG@`@Fz^dn@R&B4Tv-#(trpBh_rAT@Fv>RtcU%uv$K=+NvHq(D_{A^=YP6<<tLvs+M_+%qg|J;{N$6Y{`;?d<tLwibot6pKDjPm`N^ly<tsn=B*8!U2mj!&%U6E#$#wb4Pd<e%U-`)=o&Na$`2YC-`2YC-`2YC-`0ddi?a{6azg<sO8Gpu~@n`%Qf5xBjXZ#s|#-H(L{2717pYdn>{=q-^2Y+4o{q<ZIet*5th2LLKr#1hYf6c$<U-Pf|*ZgaKd$dP;wCloe*OS$Tf5X4w-|%nvH~bs^4gZFJ!@uF*@Nf7x{2Trazkl!#{=r`tet$jJh2LK<bm8~c(`n1U<=^se`M3OA{w@EO-yZGJ9__mD+x29%<KOY`_;>s}{vH30f5*S$-|_GGcl<m49siDh$L}BfgMaYXh2LM#b>a8d3tjmA^>o_v@A>!qd;UHDo`283=eI|Dv`4!x{B}KA9rzFY2mS;9f&ajN;6Lym_z(OC{saGk|G<CXKk)kp|KK0|b>a8db6xoT^+FeZe?6U!{73#H|B?U5f8;;%ANlRk9_`Vt3%^}YRwaMQU-FmyC4b3Z@|XN2f5~6+m;5Dv$zSr9{Qki|_y>Po`2F=<7k+=e(1qV$Pp1?AiT}iZ;y>}9_)q*NetWb>d$jAqZ`YGm#b5DP{1t!2U-4J`6@SHF@mKs6f5l(%SNs*ffAA0f!Cx1Ce?8ZQ-(N3u;rG|m>CAuTKl7jY&-`cpGyj?29_`T{?Yi*W^<-7^*Zehq&0q7^{55~gU-Q@eHGj=t^Vj?}f6eb7{DXh+*M;9-&voJV*9%?v{q=OZ@L%{Z{1^TU|Aqg;f8n=Bd$dQpF8p>qSvC9(f5YGKH~bBM!{6{X{0)D@-|#p54S&Pm@cRe<;2->T;rG{bUHJX=LKl92J)N%nSN<#imH*0r<-hV@`R&mj?a{6azg<sOEq}}3^0)jgf6L$UxBM-C%ir?1{4IaW-}1No{=q-^2Y+4o{q<ZIet*5th2LLKryKu`|HgmgzwzJrZ~QlYd$dP;wCloe*OOJp-|=_+9e>B)@pt?kf5+ePcl;fH$KUaH{2jl4@DKjMUl)FVJ=cZbUoUjw_t(?u&VT2>^WXXJ{CEC4|DE3+?a?0Xy71feWYzQc{5^lq-}CqUJ%7*N^Y{Ecf6w3Z_xwG7&+i}ngMaYXh2LM#b>a8d3tjmA^>ljhKlmT~5B>-Lga5(*;I~J6v`4!x{B}KA4g3TDz(4R0`~&~MKkyIy1OLE3@DKb0|G+=+`v?EvAN+OU_t$e>`2F=l7k+;|ou2$p{wM#F|H=R4fAT;1?a?0X(XI=>T~Agc|Hwb`kNhM5$UpLr{3HL!Kk|?KBmc-h@{j!f!9Vy1e_i<f^;{Qzf4$I!-(OFs7ypa@#sA`e@xS<A{4aicv`2fi>%wo>lhw>W^UwS<|I9!0&-^q0%s=zb{4@W|Kl9K0GrxcE5B|Yl7k+;|*M;9-FLdGe*VF0E|K@-5zxm(%Z~iy`o8KPo(H`x(@Z0rdweT<e3;)8u@Gtxe|H8lUFZ>Jt!oTn@{0slW?;rewfAH6Z-(Syl;rG`IUHJXO@_(vHYs>'
A0_D = 'c-ke?(TOWD429uJ(nj8<10xn=j2R}7-F->Y!<3RX^fslWl!5zs@59d-BFmDFmGSwxeoYR%f39Pv7&nTsP>c)3IKQu77$1spP>eUl*eS-1Vk{KnLNU&}{QIn#>ZKa#{&atSP0sIhZ@N<)`**s_Il54|%UOEfoxkTe-1naxpLzFPe=qvdAH{gn$?p3`CyVb3ot#fOPdPa7#_qQp#aJlDg<_l!Ige}SU7+(X(0LaV-gUkOI^P1FZ-LIYK<8Va^DWT%7U+BnbiM^T-vXU)F}*t;b3Q)dc%|8Rh28g!Vk{Kq;}t!hyn6D7P7dF1I@xi<;<pQ(oDVtP{QR3C^`H7r{iZ%MCf-DksmIi#Gt_(NF)L3hKPoROFDf4@532dA*{iv$nX7rLS*tm#8LRnLXIJM|XIAl5d=+2C*K@ut@6l&(6Yt&s-u;oz<vQ!@S-n&z)krn`20f~gO@B>)O@B>)P0gmirf$<;Q@iP}so&IZ>NoY9`bBP$TjUnGMQ)K><QBO_ZjoE$7P&=kkz3?$&TitH*e14#ZDQLwXLy+f_BHHk*wL_~VL!Y547(Y2v)jv<*voDw1Kmyrx}A)_z4TwW{Myyu>&lxtJ@Oxk$@C86d|m$mc<G&`'
A0P_D = 'c-jqAc~s2_82!FaLQ&Ea<1If~TG6zjdW%V7EaO-vrjBMYjlxWWV`OBh%ut>vqSq#&(h%jfdA;{AXlRVFoyhO^d#Ok!jHZQp%e?>Zx#!;R-tYR%$OvqsqUVS7tHH2ulHL<sYb#g>ykoC6FF@1VgNB!Isb)mWDqIyGpmTy8+hV>I%x(KbKhagELeU;N?i0fO1JMJ&NV;)Dou^?G+D0j~qah;ch$Nf7=sC~1;QR+y1{%;1c#5loRxdy91x(J?u_dsvKDa#t2g0kg9`LBKh8e(l9{$W%B#b>F_NB?Qy!a=8k8))<DSEt+FN2SA9qS{&<!U}(3*Krw-We}Os?RvVP8WH9A%5L>fc+a@Cont@s#K-4lJYO)>O<lDaDOfVo-dI~KBkoSLuGGi&BH9|OL`URXo<y)4aEW1=t++Q-vu`fBPX(C8$MN%N87s!49V~;Qfb+RnoI{-1yv|#h%)J~9ky0{)`wvdTS|JUmA$8-N5)NSr8%O2<`{79AJwxP!-u5RkB6FmwO$Ngd(??NXxlN>%tlI&^-<_(SdhOso~D<ET5o&A!<&hsTk6AnF}&`6!L~rPuB^)sZLx+ggcZt4c^ySgaW!8@RezObGiG@!b)m5AUAVanzrWC8-i*W4Axs?YIz2%=n<^UYOjj^R6)cXWv)dI~0SuK0`a|$>&r#72^u{iIFa>vdX_(K+rnB4_jPV`EbYZ|~b9lhihE$y|lwLf{zl0HP{%-^EtjvaQgHF%prz*I_9+K8l%nkut0riV<Rx8DXE9E!H&`>GsBe(a`0)z#Ffd(6l`tG#xCLXLEuU!FoEBs`YROlcQXH)*QdP@-6%sdtFp0)?sYn?#(y+ZO8trZ_tyrQ6Q(mBL}jsk0H<uUov7K$hds*i^IH`*1q>94ip7y&I)dz!9c#a)r&A<dlVB~By5`V;0`=!PE~D&c8oxn2mLg~|B|n6)&c*AF+}n8Ka||1KqW7C!V{Fy^32z26dwF{`Hhn~Zl8L~<>a91BrsNFVIm9)s0Jh2uoJdq`l&1*ZX-B@dU+&Exh1ACk#t!m;ehJYk&6INk;CeK~{KKuMZImPXv;o6EJp+R|)AJq<JKCErj)W$6cZd_I`x^OVB;{7ubx=BiBOO|HT^CW993Ja6*DdETfU3(u~na7plX!O=J0;wKGq?f@Kkkv~&S9R>lDNLylE{@e@iPPtmv;3?Ns!)5TfmfN3+y@?s35!6P`Og63Dnk6z~SC6e#r;R#OKN^fZ``AP<e0N;G0BTM~wMa2ATxyw%6RT^D_c80!y{0V8+7T#mq9;R6yEoCwKQ3wKfKz0;tdsVYo)vr2?njJP2yyOvx!o{yeHA+vr>+~@dmdYw4mR~cQnjC0PIHc?iF4@L`WcpOD2&$XMuXtiN%IxtQc~r2DSjYHGMiL3eoQ<$L<SF}VErtCtcS);b+&GcoY7b_vaE78Z$&rlEYW_lGpH>Icyil0>xZVbyIWl>4fJR2(d3n6D1vvh%Vaw02yiy8!>5mj=s$;Iu^pEN_m;-gMMF%l%q+)+#YIdvM%=EItfYp=8Y?Eb{e;AU7O!(0oQw&DzLyc^j&M`7QC!n>D_h0S>6V|cTb0cWC*Lh%>(+G_q*^r;&C{_;Xt1~Ee}l$*$(9UMlmV}Ss3rcA|8R`QM{+ZT|El2=p)V&ycAKWfIt+N@jz2YeC)m<^&Ju^x*Ll{SELs!BCBrhIO7=U2#TD=u;lbV(QyHG<(6O!1y}C*`pPso-;!D8$rnEzjza^G)V{rErFJ>ccQe5XvAbe4x8xKu`&lQi!@q@s)8P9E+Z@!Orntd!AFeS38YB?O9en57aMrY=+g-}g@w|$FTs)yCl@ww&lH+08r$NvL^Veafm{PD<1=^wOk>wFDDT~Qj_3HO^v_07Tm0jGbDum'
VS_D = 'c-jq@c_7qV8^_P{)U}g+o!<<X>=M@&X0%A9dRugfdh3#IiY{$ea@|*5vL&I&5;w9X!Wda*23Mt2mr_}0riDuTCaGE8`Rn|3&Uv2m{XU=PISpG<w76SIj)_VZWr>#AGrTrua@g6TL(oLR&2Kue{>3u7Q<2GY*u$;2v24fiwbnFV5UKYnSTs(-M&%bQ)-+yU-BH735R-Y?g`L49;lsSeq9^1=7&l$E5Y&vBrQWUhBvZ}0Q<I#Jac2vwNqlgy8qFS!JM}fi55VkPbc@eR+-o=MCOZUyS&_XzijleAbkS%xIW)BHnsAEf7e%^qgNae$k#d0&ls|ZOMp!{E=NcTN%b@tr!!*x2%wK<4Uv>drq$St5eaGE~+9jQ)Bs)5}fEI!-uObbEs&HLzf4=Al(Xwex6!OWhFRQDc-GV;z+r{4Bv6*+RSrQG6W1Ei)%gB<8t31bb;q|L{TR}U?nkqH68bi}_S$eY#AlNqH;M0y}!y$#NFIarEx0p`hXLq_T<&0^|cv^gIQgHS_3$+PPSOm<K6hdQyS&eraN>ppgL<&%-_e_n-#C%7qS|%U29~##c=)ha=HyY26K-GEvkCGk`uXI%w3t{11t84*6+2r`oCTCFP<aYflYQ+A;(kmnVBp@z{!(BnhKfbo2W-@%Ird+t6@K0Vfk|(X3=Tl1U!M^lkt#1xPT;O+_Jfx7_sy)VzIHJ{VCcO&Aw}wpK`~{a|PPz-ULF@c!ThTD7-YN1Hj*z1^Zd}0y^8Ry>J@XlsWY5VG&4KI<kG-ia_@yFFUy==)O*>pAx8dd;{T%KBlIu}qDvN?I&qH<Px>r7~nIoXUyw5Ywz7=03ZYrRTWB&a<JLxHCJ#?KTs3Cz@FWFE^$cT&JNc!NPb!-*6wpX7%^kV#kFO2niOeR6PJ2Zd%0EyCJ(FCm|WIK~3Oef<{D%&VANCyVfg~v%(Y%XDTV)CE-bE0&z&~bl~D2}*1)lctSMNU7umBxs{`1qDW(JS&Nt2#rV2AsXa`O+oOx2MQiS_pTWCe)w*4y_h3r2=EfU&Q3dy~{nb%Uzlc%hwq=S-iu!S+D8@gJj@Q;>wE-B;#|w67wzEao(!Q-!r*QTeEX9shQeLm(;+%jMg+!GAZ1p(n&jx%Xx1d=C|U*nb-=Ufc$aIwNbVbtXO{YB*UO|b0Cvmh`VOcQ+gIuBXd$XOUSjS{%mRku2#2irmG-ZA*GFLNLqT%m5akb;Yz=~tOkA!>WSw16H$bMyYUqKwPHU-FTkKfm4)-)VWzLEEvo?+q?($|ra+?5)Seqcx(4k#nBCYE>z6eDBhm#yosuY6aMYk#$R$grALz<M3i~PHG;Jg9oBUENI6?ev70N8$;^NqxLU}!imD36&b--y#S2TGHG5zdx+8Gq5IzAq~L=H`Ut@pl-v*GSV^cei?dqv6ZHpZqW=g`zppLa<`b{P2WB5zp(D2?{izc~p%u)t871LV_83L_dH+g?z$=)&lnb5G?iXq>)k>^O~6iELF7LYvv#WFIz`Y+8Rzlt`LC@2(TwBc`hQEXiHiRCgp-dJ8tVzGO&ZL9KsPG0hHL*h<<yv#5LK!11X-FxmCSg4u|(p=T)X_ZWI9z)d;~-@0i<vJp6_ywPC#2q+7Ub@W0|H$Y|Kg2%|I|5`P6hYa;kpAe6MaqewJSuI>nQ)s05VCVdO-s9R(K?$;`PcZpLrr~}UUtV3O!3!a7EpybVM7&_Fb6%bUH9D(Iokdk^<|31)(0;?%;&l{k@9#}@EyIWZS!6EQPjYzQSaN5T4g};d-b2TpHC`jP$R3kwP0>M8&+tFN+d@oq3^Mf;aZTjBdW&v+dn3TkX8@n?NGR;|Cr0(XJVq2Y3VM{KJK=}q==m+S<ZUabNKT?&#X%eD1MqrpWRL$&JT5M~EHs8u1)m>fF>s)La-N`>+?7N+2rm-e1KKf3E#!q>uceM+p!ie{?HjmnsY|0m(WY)*yU#=Xy!|_OVkx|+feczCUR!sHDJ&<_(BoduR|5+dw~QNtzbi*eFhJf~*Jp_TfvUmqO7H9Vr?a9ijfH>xFFI3X1lzVA%#_u`*4DQMR0y6IKTK6e)YRWSpSOUteT}uE7o%oKU!&9wEFC=A+(6Q}{&s=<u*81DQ?i}#>*WzjG(dW@j<nDmuu?ffSJDq&y{Q`F9`Mk(aEh@BH|I|1Q6-pgcfSv_3%~C3YG$@!BXhnDJsQ;(PSUDYkcDR=PsrnxeF$8{w;(%f8J?mh60goq*HuD`JH`thCXqnrruMdZq$I@AqTYslaSZ2CIVe6nl*_dsLHheoR|F8RR|g$^-r&0USuVp76_yW_uv$^?nF3E14ukPdY-$d^FzT|E?0~MNGIQA|gr_>6m&0nTF;7=~5Q++4mQ37&jPi>``~~FNT|HIlztH3EIG5FdJLAkVC}o@pW*5o#sZ@O|aruNJya;tF0{czuTqfc{t#(+4`!l)TpW`I;f(;{2PYa)tzyl_^i-ytXx7m9BVv={@k)w1JlGvI88xDpq>9H4e5a!NzEXzJr)-ONG-AF3=In{59z#;mU5+fV$FYLM8zn8S-Cp$`f;i9vCR>d;%O~d}Y(NkDU4Jp%q!B9h8l=tZb&}eq~icM91j)Hn(mcmJt1GnYM5vF(m9xSnQwrs*wo2W{k8#s8p()NlW8Gj~ir>Wou#!*M_kNEm@!BPebEqA*)%d0p@xT>mRHQ97EP)E)J+6r|oK?ZrLZq&%^LE*p4bVXl@a<)wwJsq`X>~vay*qA$Uc_t*`%5S}r^RRfxwVNA6q7r1snQXj5+g-}+L+zH4D(PbIjV&k@DuVq-izJ3EQag3Zg{@>|Z*Dc^h3SG|eaZ|Yf@{hI$s{K?IZYrW*8C^uUVA|HL?M$3L^sA5O*9YK3Q5JnC#3l3a*m}8i|(gcO1t3ighvja3!r5#C&TR<ZoB-w)b%1Bu&pr?{z-yjdn~1auy(L&iNFNzy>ihO#FNxtkEbx-<C;}j7st~{-jssXIES2n%`TKK1vl-NG@(8`xT)15I!3lP2T%+(>{w-+Ez5`C?SHf}LQreZqkL97);y>%vXo%oSR0||Bmb$pmbeturxq9qo{;x7?L~}Fu%z&+o*X(yeqw7fZ(@vwZzbQD40Y?5%by^x)Vo|hj(obYCXJ^_6w5~x_zV)ISkTtFnHV!%L8J=5J8f{L!jP$CrTsk_X2x!{3kOO6oa$Wh4hVZuP|6D=ukUuAWyGV$vipXjyW}2UTuX~U^~#!Bu?tMKzGM0{VR`4y7O6j+xF4D1(}xvG4o>dx@q@*82Z<ZZ^pzLUj-m6zf{XH{;qkD(I1<7RHn#~!iG?MjiS+{4?0my-@h69#lyr#<;Te@;Aku;Kgrl82Gx9p@Qo%?!S(%e~QW6Hgw*}`3xWw{FNvot9JaT$7ISWWo&(=DIHFk`2o~TnKqbZk<Ny<Sx(mz`taQA>m66-o%_+u!M_ajMZ3KMqtk@f0vNwiNuKCfb52qI?>7Aj0%2gP%reE7B`!sBc+Ee}n1EmW55hKj{{ESe?8&S*P$KStGeck*ay=oS`MC#Mv><ACCH3Pd^&7*AxwA~U5^l3zf_n&DihMQ-oQ^cpvY-Z@|AGN<vdj=G0@sCm0$g(ZuNlkZhJB{^`56E%<3h5kFW9rR4`Y~rB>a>1=XF7_0}5S7?{^>Q_jBv*G!Jz!DFjJnhZz9#IclH<^;xX(!C6{w6Fddm8sp?s^4+@A`2Pal)~0g2tKo5h<zXgZbLp-7&I9@WV&GM{l#7GHywTqP^XLx^)UoDgLabpwwJvMN}i9AG2v0)w^om&EtLZB<^5Bmz7h<f;g1Fkz!qEvtZ;nwCbNe=ug(kP`g^1bkh?pq)i%sj77sqS3ni4%sc(c7KC<r!|SKi_?$~STo&)s*`JgJ-eR9NJacttR(S-zc-H+3M+}yjO*N)T)1J^LF8rlU)3I`@doldKV`AJfTCj7KJeh8Volaud8h2jyI#igBinCmoIk%EfAKZ2=h4Z~J1YzEdANLv)4($%4VjiXlsn>YDeltKaOU)ICU+azlN!tw>Oz;-{bX7JmO8R@S#oqmS6MUL@qp9MODTeW@BCF{p|DQz3nl*!EDv^{nDztDjj4Z&Z^M6+B}K9^_{jdjjBbyX=K`C=_hEkStNJ&qz(i-$Po3suozTj~g^%>eOJ$-o;<txZD<98eGW>n%b{Oiu<1~LgsosE`PBUWFK9M5S00sXa%(?#|eg*Hm1;b=p!@M$49@$35wB(Ji;OYs69HUWN%=R_-lIJg8PRj1V3f_P#{Toca4{)LuV%)x09KHuR^?WH;kV+=|4xbr|CgBr{%9vl!tn_DPsS|ia@Aad0prVd@uKgWkuirXZW<bh5_*gLXaE&nCT3P~w4}Fi#goAlyx8=AJRQ<2YOv;Cd)cr237x;gr$_HT'
SFS_D = 'c-jltn_$KyrTzbej&#Oyhw18fwSOC>-f^3)dFa8Z$N9mG#j*;)B4Qj<oveh9?tW(Ui_iL>z+W~W59vQH`iAEuALRdj5u6hlye)g?^w{XF^~YA)M(*WbtKr-$|C%T2V$Y%}FBg_C@aVg=J5_!@0sXbnd+iSa_0L_pU(>CZ`!TBi-1ylMvYFegI~VOg>mzNo^iToUw$FJtZS4Hjw|~o!<%x*CwkJ3z>Ow&vo7ACzJsS*GEdA$jK-sl7!S!0Djq#kBo-3nbncf%Y_c5w!=A2M>iF3(Y_iz_iuSOv@w-V6*LfuEs0jPi0g87;y*xVXWo4GAH%zppb0BH-Q?Gw@~Ch#4PC|oeDPjs{3ypCxbMXqkRYAPmaRC}H!SD?&c`P)r4b58VaVvFnl`}X0UqKB3nZ)HyXwm8sHU)}fnmozuGr!ITBIyH*1xs`za-0y$XoPhf0E|{%ZhSjZm6StK;x3fPHV7+Rpx|Nogg8YLBcAd*Jc`GVE>SjF=J6JW*{8!M<7UyU3dCv~LkqV!{mBhqnWxp-xw}az?$3MP#D*p0dd%xA~@~qE+en(70T&?*#IT*3Im4N<TpCkDW0QE~Roz2OD&8+|_UrXT'

def _dec(s): return zlib.decompress(base64.b85decode(s))
EMB = {}
def emb():
    if not EMB:
        EMB['A2'] = list(struct.unpack('<768I', _dec(A2_D)))
        EMB['A0'] = list(struct.unpack('<256I', _dec(A0_D)))
        b = _dec(A0P_D); EMB['A0P'] = [struct.unpack_from('<IH', b, 6 * k) for k in range(256)]
        b = _dec(VS_D); EMB['VS'] = [struct.unpack_from('<BIH', b, 7 * k) for k in range(len(b) // 7)]
        b = _dec(SFS_D); EMB['SFS'] = [struct.unpack_from('<43I', b, 172 * k) for k in range(len(b) // 172)]
    return EMB

def variant(a0, a1, a2):
    """Variant: per member (A[0..15], E[4..15], W[8..15]) with A0..A2 replaced, and c7 (W7x = c7 - A_{-1})."""
    out = []
    for (A_, E_, W_) in (TX, TY):
        A = {i: A_[i] for i in range(16)}; A[0], A[1], A[2] = a0, a1, a2
        E = {i: E_[i] for i in range(4, 16)}
        for i in (4, 5, 6): E[i] = (A[i] + A[i-4] - S0(A[i-1]) - MAJ(A[i-1], A[i-2], A[i-3])) & M
        W = {i: W_[i] for i in range(8, 16)}
        for i in (8, 9, 10): W[i] = (E[i] - A[i-4] - E[i-4] - S1(E[i-1]) - CH(E[i-1], E[i-2], E[i-3]) - K[i]) & M
        out.append((A, E, W))
    (A, E, _), _ = out
    c7 = (E[7] - 2 * A[3] + S0(A[2]) + MAJ(A[2], A[1], A[0]) - S1(E[6]) - CH(E[6], E[5], E[4]) - K[7]) & M
    return out, c7

def valid(var):
    """E cells of rows 4..8 (with '+') and the published dW_i, ds0(W_i), i = 8..11."""
    (Ax, Ex, Wx), (Ay, Ey, Wy) = var
    for i in range(4, 9):
        m, v, d, _ = CELL['E'][i]
        if Ex[i] & m != v or Ex[i] ^ Ey[i] != d or (PLUS[i] and (Ex[i] ^ Ex[i-1]) & PLUS[i]): return False
    return all(((Wx[i] - Wy[i]) & M, (s0(Wx[i]) - s0(Wy[i])) & M) == DIFF[i] for i in (8, 9, 10, 11))

def words(cv, A, E):
    """Step-2 words W0..W7."""
    A = dict(A); E = dict(E)
    for j in range(4): A[-1-j] = cv[j]; E[-1-j] = cv[4+j]
    for i in range(4): E[i] = (A[i] + A[i-4] - S0(A[i-1]) - MAJ(A[i-1], A[i-2], A[i-3])) & M
    return [(E[i] - A[i-4] - E[i-4] - S1(E[i-1]) - CH(E[i-1], E[i-2], E[i-3]) - K[i]) & M for i in range(8)]

def pair(cv, var):
    (Ax, Ex, Wx), (Ay, Ey, Wy) = var
    return words(cv, Ax, Ex) + [Wx[i] for i in range(8, 16)], words(cv, Ay, Ey) + [Wy[i] for i in range(8, 16)]

def yz0(cv, a0):
    """Y = W1 - A1, Z0 = W0 + s1(W14) (Lemma 5)."""
    a, b, c, d, e, f, g, h = cv
    hh = (d - S0(a) - MAJ(a, b, c)) & M; e0 = (a0 + hh) & M
    Y = (-S0(a0) - MAJ(a0, a, b) - g - S1(e0) - CH(e0, e, f) - K[1]) & M
    W0 = (a0 + hh - d - h - S1(e) - CH(e, f, g) - K[0]) & M
    return Y, (W0 + s1(TX[2][14])) & M

def c9x(a2):
    e6 = (TX[0][6] + a2 - S0(TX[0][5]) - MAJ(TX[0][5], TX[0][4], TX[0][3])) & M
    A, E = TX[0], TX[1]
    return (E[9] - 2 * A[5] + S0(A[4]) + MAJ(A[4], A[3], a2) - S1(E[8]) - CH(E[8], E[7], e6) - K[9]) & M

def outcome(cv, a0, a1, a2):
    """Row 16, W7 in F7, deepest row held, traces."""
    var, c7 = variant(a0, a1, a2); wx, wy = pair(cv, var); tx = trace(cv, wx); ty = trace(cv, wy)
    r16 = rowok(tx, ty, 16); deep = 15
    for i in range(16, R):
        if not rowok(tx, ty, i): break
        deep = i
    return r16, inF7(wx[7]), deep, (tx, ty, wx, wy)

# Counted program: 256-bit words, <= 64 registers; cost 1 per add, sub, and, or, xor, shl, shr, ld/st, rand, jmp, 2 per
# conditional branch, f38 = 1 unit.  Levers L0..L5: proof.md Appendix C.
REG = {}   # region bases
for k, nm in enumerate(('HDR', 'ENT', 'F7', 'A2T', 'GT', 'SCR'), 1): REG[nm] = k << 200
REG['RL'] = 8 << 200
M4 = sum(M << 64 * k for k in range(4)); L64 = (1 << 64) - 1; W256 = (1 << 256) - 1
DELTA, FLAG, BIAS = 1 << 199, 1 << 33, 1 << 32
# fields word: A1 | U << 32 | A1^A0 << 64 | vE << 96 | A2 index << 128 | g index << 138 | S0(A1) << 144 | KCA << 224

class Asm:
    def __init__(s): s.c = []; s.lab = {}; s.n = 0
    def __call__(s, *ins): s.c.append(ins)
    def L(s, nm): s.lab[nm] = len(s.c)
    def new(s, p='L'): s.n += 1; return '%s%d' % (p, s.n)

def rot32(a, d, x, n1, n2, n3, shr3=False, t1='t1', t2='t2', D='D'):
    """d = ROTR(x,n1) ^ ROTR(x,n2) ^ (SHR or ROTR)(x,n3), low 32 bits; x masked; 7 operations."""
    a('shl', D, x, 32); a('or', D, D, x)
    a('shr', t1, D, n1); a('shr', t2, D, n2); a('xor', t1, t1, t2)
    a('shr', t2, x if shr3 else D, n3); a('xor', d, t1, t2)

def gen_prologue(a):
    """Group prologue: two random words -> M0, CV1 = F(IV, M0), per-CV values."""
    a('rand', 'r0'); a('rand', 'r1')
    for k in range(16):
        r = 'r0' if k < 8 else 'r1'; s_ = 32 * (k % 8)
        if s_: a('shr', 'm%d' % k, r, s_); a('and', 'm%d' % k, 'm%d' % k, M)
        else: a('and', 'm%d' % k, r, M)
    a('f38', ['m%d' % k for k in range(16)], ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
    rot32(a, 'S0a', 'a', 2, 13, 22)
    a('and', 't1', 'a', 'b'); a('or', 't2', 'a', 'b'); a('and', 't2', 't2', 'c'); a('or', 't1', 't1', 't2')
    a('sub', 'hh', 'd', 'S0a'); a('sub', 'hh', 'hh', 't1')
    rot32(a, 'S1e', 'e', 6, 11, 25)
    a('xor', 't1', 'f', 'g'); a('and', 't1', 't1', 'e'); a('xor', 't1', 't1', 'g')
    a('sub', 'y0p', 'hh', 'd'); a('sub', 'y0p', 'y0p', 'h'); a('sub', 'y0p', 'y0p', 'S1e'); a('sub', 'y0p', 'y0p', 't1')
    a('add', 'y0p', 'y0p', (s1(TX[2][14]) - K[0]) & M)
    a('xor', 'abx', 'a', 'b'); a('and', 'aba', 'a', 'b'); a('xor', 'efx', 'e', 'f'); a('add', 'gk', 'g', K[1])
    a('and', 'hhm', 'hh', M); rep4(a, 'hh4', 'hhm')
    for x in ('efx', 'f', 'abx', 'aba'): rep4(a, x + '4', x)
    a('and', 'gkm', 'gk', M); rep4(a, 'gk4', 'gkm'); a('and', 'y0pm', 'y0p', M); rep4(a, 'y0p4', 'y0pm')

def rep4(a, d, x): a('shl', 't1', x, 64); a('or', 't1', 't1', x); a('shl', d, 't1', 128); a('or', d, d, 't1')

def gen_pack(a, p):   # L3: four A0 in 64-bit lanes (23 ops)
    a0s = [emb()['A0'][4 * p + k] for k in range(4)]; A0P = sum(x << 64 * k for k, x in enumerate(a0s))
    NS0 = sum((4 << 32) + (-S0(x) & M) << 64 * k for k, x in enumerate(a0s))
    a('add', 'E0p', 'hh4', A0P); a('and', 'E0p', 'E0p', M4)
    a('shl', 'D', 'E0p', 32); a('or', 'D', 'D', 'E0p')
    a('shr', 't1', 'D', 6); a('shr', 't2', 'D', 11); a('xor', 't1', 't1', 't2'); a('shr', 't2', 'D', 25)
    a('xor', 'S1p', 't1', 't2'); a('and', 'S1p', 'S1p', M4)
    a('and', 'Chp', 'E0p', 'efx4'); a('xor', 'Chp', 'Chp', 'f4')
    a('and', 'Mjp', 'abx4', A0P); a('xor', 'Mjp', 'Mjp', 'aba4')
    a('rsub', 'Y0p', NS0, 'Mjp')
    a('sub', 'Yp', 'Y0p', 'S1p'); a('sub', 'Yp', 'Yp', 'Chp'); a('sub', 'Yp', 'Yp', 'gk4'); a('and', 'Yp', 'Yp', M4)
    a('add', 'Z0p', 'y0p4', A0P); a('and', 'Z0p', 'Z0p', M4)
    a('shl', 'YZp', 'Yp', 32); a('or', 'YZp', 'YZp', 'Z0p')

def gen_block(a, j, k, rare):   # L1 entry loop
    if k == 0: a('and', 't1', 'YZp', L64)
    elif k == 3: a('shr', 't1', 'YZp', 192)
    else: a('shr', 't1', 'YZp', 64 * k); a('and', 't1', 't1', L64)
    a('add', 'I', 't1', REG['HDR'] | j << 64)
    ctx = dict(E0=('E0p', 64 * k), Y=('YZp', 64 * k + 32), Y0=('Y0p', 64 * k), k=k)
    nxt = a.new('next'); loop, sel, xit = a.new('loop'), a.new('sel'), a.new('xit')
    a('ld', 'OFF', 'I'); a('bz', 'OFF', nxt); a('sub', 'NE', 'NE', 'OFF')
    a.L(loop)
    a('ld', 'EN', 'OFF'); a('add', 'OFF', 'OFF', 1); a('sub', 'W7', 'EN', 'a'); a('ld', 'FL', 'W7'); a('bz', 'FL', loop)
    a('bne', 'FL', 2, sel)
    a.L(xit); a('add', 'NE', 'NE', 'OFF')
    a.L(nxt)
    rare.append((j, emb()['A0'][j], ctx, sel, loop, xit))

def gen_rare(a, j, a0, ctx, sel, loop, xit):
    last = a.new('r17last')
    a.L(sel); a('bne', 'FL', 1, last); gen_w7(a, j, a0, ctx, loop)
    a.L(last); gen_w7(a, j, a0, ctx, xit)

def lane(a, ctx, name, tmp):
    src, sh = ctx[name]
    if sh == 0: return src
    a('shr', tmp, src, sh); return tmp

def gen_w7(a, j, a0, ctx, back):
    a('add', 'NW', 'NW', 1); a('add', 'PF', 'OFF', DELTA - 1); a('ld', 'F', 'PF')
    Y0 = lane(a, ctx, 'Y0', 'tY0')
    a('add', 'E1', 'F', 'c'); a('add', 'E1', 'E1', Y0); a('and', 'E1', 'E1', M)
    rot32(a, 'S1E1', 'E1', 6, 11, 25)
    E0 = lane(a, ctx, 'E0', 'tE0')
    a('xor', 't1', E0, 'e'); a('and', 't1', 't1', 'E1'); a('xor', 'ChE1', 't1', 'e')
    a('shr', 'Q', 'F', 64); a('and', 't1', 'a', 'Q'); a('shr', 'U', 'F', 32)
    a('sub', 'W2', 'U', 't1'); a('sub', 'W2', 'W2', 'f'); a('sub', 'W2', 'W2', 'S1E1'); a('sub', 'W2', 'W2', 'ChE1')
    a('and', 'W2', 'W2', M)
    rot32(a, 's0W2', 'W2', 7, 18, 3, shr3=True)
    a('shr', 'KC', 'F', 224); Y = lane(a, ctx, 'Y', 'tY')
    a('add', 'E17', 's0W2', 'KC'); a('add', 'E17', 'E17', Y)
    a('obs', 'E17')
    a('shr', 'VE', 'F', 96); a('xor', 't1', 'E17', 'VE'); a('and', 't1', 't1', GREC[0][1]); a('bnz', 't1', back)
    a('add', 'N1', 'N1', 1)
    a('and', 'E17', 'E17', M)
    a('shr', 'PG', 'F', 138); a('and', 'PG', 'PG', 31); a('shl', 'PG', 'PG', 4); a('add', 'PG', 'PG', REG['GT'])
    a('add', 'P3', 'PG', 3); a('ld', 't1', 'P3'); a('add', 'A17', 'E17', 't1'); a('and', 'A17', 'A17', M)
    a('add', 'P3', 'PG', 5); a('ld', 't2', 'P3'); a('and', 't1', 'A17', GREC[0][4]); a('bne', 't1', 't2', back)
    a('shr', 't1', 'A17', 11); a('xor', 't1', 't1', 'A17'); a('and', 't1', 't1', 0x200)
    a('shr', 't2', 'A17', 12); a('xor', 't2', 't2', 'A17'); a('and', 't2', 't2', 0x40); a('or', 't1', 't1', 't2')
    a('shr', 't2', 'A17', 9); a('xor', 't2', 't2', 'A17'); a('and', 't2', 't2', 0x100); a('or', 't1', 't1', 't2')
    a('bnz', 't1', back)
    a('add', 'N2', 'N2', 1)
    deep = a.new('deep'); a('jmp', deep); a.L(deep)
    a('and', 'A1', 'F', M); a('shr', 'S0A1', 'F', 144); a('and', 'S0A1', 'S0A1', M)
    a('shr', 'P2', 'F', 128); a('and', 'P2', 'P2', 1023); a('shl', 'P2', 'P2', 2); a('add', 'P2', 'P2', REG['A2T'])
    a('ld', 'A2r', 'P2'); a('and', 'A2', 'A2r', M)
    a('xor', 't1', 'a', a0); a('and', 't1', 't1', 'A1'); a('and', 't2', 'a', a0); a('xor', 'MjA1', 't1', 't2')
    a('add', 'E2', 'A2', 'b'); a('sub', 'E2', 'E2', 'S0A1'); a('sub', 'E2', 'E2', 'MjA1')
    a('ld', 't1', 'PG'); a('sub', 'W17', 'E17', 't1'); a('and', 'W17', 'W17', M)
    if ctx['k']: a('shr', 'E0', 'E0p', 64 * ctx['k']); a('and', 'E0', 'E0', M)
    else: a('and', 'E0', 'E0p', M)
    gen_deep(a, j, a0, back)

def gen_deep(a, j, a0, back):
    """Rows 18..37 of both members through scratch memory, every condition."""
    sx = lambda m, k, i: REG['SCR'] + 256 * m + 64 * k + i + 8      # m member, k 0:A 1:E 2:W, i row (-8..)
    def st(r, m, k, i): a('sti', sx(m, k, i), r)
    def ld(r, m, k, i): a('ldi', r, sx(m, k, i))
    A0r = TX[0]
    # E2 masked, E3, W3, E4, W4, E5, W5, E6, W6, W7
    a('and', 'E2', 'E2', M)
    a('shr', 'S0A2', 'A2r', 64); a('and', 'S0A2', 'S0A2', M)
    a('xor', 't1', 'A1', a0); a('and', 't1', 't1', 'A2'); a('and', 't2', 'A1', a0); a('xor', 't1', 't1', 't2')
    a('add', 'E3', 'a', A0r[3]); a('sub', 'E3', 'E3', 'S0A2'); a('sub', 'E3', 'E3', 't1'); a('and', 'E3', 'E3', M)
    def wstep(dst, Ei, Ai4, Ei4, Em1, Em2, Em3, k):
        rot32(a, 'S1t', Em1, 6, 11, 25)
        a('xor', 't3', Em2, Em3); a('and', 't3', 't3', Em1); a('xor', 't3', 't3', Em3)
        a('sub', dst, Ei, Ai4); a('sub', dst, dst, Ei4); a('sub', dst, dst, 'S1t'); a('sub', dst, dst, 't3')
        a('add', dst, dst, (-K[k]) & M); a('and', dst, dst, M)
    wstep('W3', 'E3', 'a', 'e', 'E2', 'E1', 'E0', 3)
    a('xor', 't1', 'A1', A0r[3]); a('and', 't1', 't1', 'A2'); a('and', 't2', 'A1', A0r[3]); a('xor', 't1', 't1', 't2')
    a('rsub', 'E4', (A0r[4] + a0 - S0(A0r[3])) & M, 't1'); a('and', 'E4', 'E4', M)
    wstep('W4', 'E4', a0, 'E0', 'E3', 'E2', 'E1', 4)
    a('shr', 'E5', 'A2r', 128); a('and', 'E5', 'E5', M); a('add', 'E5', 'E5', 'A1'); a('and', 'E5', 'E5', M)
    wstep('W5', 'E5', 'A1', 'E1', 'E4', 'E3', 'E2', 5)
    a('shr', 'E6', 'A2r', 96); a('and', 'E6', 'E6', M)
    wstep('W6', 'E6', 'A2', 'E2', 'E5', 'E4', 'E3', 6)
    a('sub', 'W7', 'EN', 'a'); a('and', 'W7', 'W7', M)
    # W2..W17 of both members
    for i, r in ((2, 'W2'), (3, 'W3'), (4, 'W4'), (5, 'W5'), (6, 'W6')):
        st(r, 0, 2, i); st(r, 1, 2, i)
    st('W7', 0, 2, 7); a('add', 't1', 'W7', D7); a('and', 't1', 't1', M); st('t1', 1, 2, 7)
    for m in (0, 1):   # W8 = E8 - A4 - E4 - S1(E7) - CH(E7, E6, E5) - K8 (E7, E8 per member)
        At, Et = (TX, TY)[m][0], (TX, TY)[m][1]
        a('xor', 't3', 'E6', 'E5'); a('and', 't3', 't3', Et[7]); a('xor', 't3', 't3', 'E5')
        a('rsub', 't1', (Et[8] - At[4] - S1(Et[7]) - K[8]) & M, 'E4'); a('sub', 't1', 't1', 't3'); a('and', 't1', 't1', M)
        st('t1', m, 2, 8)
    a('add', 'P3', 'P2', 1); a('ld', 'A2r2', 'P3')       # record word 1: c9x | c9y<<32 | W10x<<64 | W10y<<96
    for m in (0, 1):
        a('shr', 't1', 'A2r2', 32 * m); a('and', 't1', 't1', M); a('sub', 't1', 't1', 'A1'); a('and', 't1', 't1', M); st('t1', m, 2, 9)
        a('shr', 't1', 'A2r2', 64 + 32 * m); a('and', 't1', 't1', M); st('t1', m, 2, 10)
        for i in range(11, 16): a('sti', sx(m, 2, i), (TX, TY)[m][2][i])
    a('add', 'P3', 'PG', 6); a('ld', 't1', 'P3'); st('t1', 0, 2, 16); a('sub', 't1', 't1', DW16); a('and', 't1', 't1', M); st('t1', 1, 2, 16)
    st('W17', 0, 2, 17); st('W17', 1, 2, 17)
    # states rows 13..17
    for m in (0, 1):
        for i in (13, 14, 15):
            for k in (0, 1): a('sti', sx(m, k, i), (TX, TY)[m][k][i])
        for k in (0, 1):
            a('add', 'P3', 'PG', 7 + 2 * m + k); a('ld', 't1', 'P3'); st('t1', m, k, 16)
    st('A17', 0, 0, 17); st('E17', 0, 1, 17); st('E17', 1, 1, 17)
    a('sub', 't1', 'A17', DW16); a('and', 't1', 't1', M); st('t1', 1, 0, 17)
    # rows 18..37
    for i in range(18, R):
        for m in (0, 1):
            ld('u1', m, 2, i - 2); ld('u2', m, 2, i - 7); ld('u3', m, 2, i - 15); ld('u4', m, 2, i - 16)
            rot32(a, 'v1', 'u1', 17, 19, 10, shr3=True); rot32(a, 'v2', 'u3', 7, 18, 3, shr3=True)
            a('add', 'u2', 'u2', 'v1'); a('add', 'u2', 'u2', 'v2'); a('add', 'u2', 'u2', 'u4'); a('and', 'wi', 'u2', M)
            st('wi', m, 2, i)
            ld('e1', m, 1, i - 1); ld('e2', m, 1, i - 2); ld('e3', m, 1, i - 3); ld('e4', m, 1, i - 4); ld('a4', m, 0, i - 4)
            rot32(a, 'v1', 'e1', 6, 11, 25)
            a('xor', 't3', 'e2', 'e3'); a('and', 't3', 't3', 'e1'); a('xor', 't3', 't3', 'e3')
            a('add', 'ei', 'a4', 'e4'); a('add', 'ei', 'ei', 'v1'); a('add', 'ei', 'ei', 't3'); a('add', 'ei', 'ei', 'wi')
            a('add', 'ei', 'ei', K[i]); a('and', 'ei', 'ei', M); st('ei', m, 1, i)
            ld('b1', m, 0, i - 1); ld('b2', m, 0, i - 2); ld('b3', m, 0, i - 3)
            rot32(a, 'v1', 'b1', 2, 13, 22)
            a('and', 't3', 'b1', 'b2'); a('or', 't4', 'b1', 'b2'); a('and', 't4', 't4', 'b3'); a('or', 't3', 't3', 't4')
            a('sub', 'ai', 'ei', 'a4'); a('add', 'ai', 'ai', 'v1'); a('add', 'ai', 'ai', 't3'); a('and', 'ai', 'ai', M)
            st('ai', m, 0, i)
            if m == 0: ld('xa', 0, 0, i); ld('xe', 0, 1, i); ld('xw', 0, 2, i)
        # row i checks (member x)
        for k, xr, yr in ((0, 'xa', 'ai'), (1, 'xe', 'ei'), (2, 'xw', 'wi')):
            m_, v_, d_, _ = CELL['AEW'[k]][i]
            if m_: a('and', 't1', xr, m_); a('bne', 't1', v_, back)
            a('xor', 't1', xr, yr); a('bne', 't1', d_, back)
        if PLUS[i]: ld('t2', 0, 1, i - 1); a('xor', 't1', 'xe', 't2'); a('and', 't1', 't1', PLUS[i]); a('bnz', 't1', back)
        for k1, i1, b1, ne, k2, i2, b2 in XROW.get(i, ()):
            ld('t1', 0, 'AEW'.index(k1), i1); ld('t2', 0, 'AEW'.index(k2), i2)
            a('shr', 't1', 't1', b1); a('shr', 't2', 't2', b2); a('xor', 't1', 't1', 't2'); a('and', 't1', 't1', 1)
            a('bne', 't1', ne, back)
    a('succ', j, 'EN')

class Machine:
    def __init__(s, randwords, bucket, cvforce=None):
        s.rw = list(randwords); s.bucket = bucket; s.cvforce = cvforce; s.r = {}; s.ops = 0; s.units = 0
        s.mem = {}; s.ent = {}; s.nent = 1; s.succ = None; s.cv = None; s.m0 = None; s.trace = []; s.obs = []; s.gis = []
    def load(s, addr):
        reg, off = addr >> 200, addr & ((1 << 200) - 1)
        if reg == 0 and addr < 1 << 34: return int(inF7(addr & M)) + 2 * (addr >> 33 & 1)
        if reg == 1:
            j, idx = off >> 64, off & ((1 << 64) - 1); es = s.bucket(j, idx >> 32, idx & M); base = REG['ENT'] + s.nent
            for i, (a1, k) in enumerate(es):
                w0, w1, gi = entry(s.cv, j, a1, k, i == len(es) - 1)
                s.ent[base + i] = w0; s.ent[base + i + DELTA] = w1; s.gis.append(gi)
            s.nent += len(es) + 1; s.trace.append((j, idx >> 32, idx & M, len(es)))
            return base if es else 0
        if reg == 2: return s.ent[addr]
        if reg == 4: return A2REC[off >> 2][off & 3]
        if reg == 5: return GREC[off >> 4][off & 15]
        return s.mem.get(addr, 0)
    def store(s, addr, val): s.mem[addr] = val
    def run(s, code):
        c, lab, r = code.c, code.lab, s.r; pc = 0; n = len(c); W = (1 << 256) - 1
        def v(x): return x if isinstance(x, int) else r.get(x, 0)   # registers start at zero
        while pc < n:
            ins = c[pc]; op = ins[0]; pc += 1
            if op == 'add': r[ins[1]] = (v(ins[2]) + v(ins[3])) & W; s.ops += 1
            elif op == 'sub': r[ins[1]] = (v(ins[2]) - v(ins[3])) & W; s.ops += 1
            elif op == 'rsub': r[ins[1]] = (ins[2] - v(ins[3])) & W; s.ops += 1
            elif op == 'and': r[ins[1]] = v(ins[2]) & v(ins[3]); s.ops += 1
            elif op == 'or': r[ins[1]] = v(ins[2]) | v(ins[3]); s.ops += 1
            elif op == 'xor': r[ins[1]] = v(ins[2]) ^ v(ins[3]); s.ops += 1
            elif op == 'shl': r[ins[1]] = (v(ins[2]) << ins[3]) & W; s.ops += 1
            elif op == 'shr': r[ins[1]] = v(ins[2]) >> ins[3]; s.ops += 1
            elif op == 'ld': r[ins[1]] = s.load(v(ins[2])); s.ops += 1
            elif op == 'ldi': r[ins[1]] = s.mem.get(ins[2], 0); s.ops += 1
            elif op == 'sti': s.mem[ins[1]] = v(ins[2]); s.ops += 1
            elif op == 'st': s.store(v(ins[1]), v(ins[2])); s.ops += 1
            elif op == 'bz': s.ops += 2; pc = lab[ins[2]] if v(ins[1]) == 0 else pc
            elif op == 'bnz': s.ops += 2; pc = lab[ins[2]] if v(ins[1]) != 0 else pc
            elif op == 'bne': s.ops += 2; pc = lab[ins[3]] if v(ins[1]) != v(ins[2]) else pc
            elif op == 'jmp': s.ops += 1; pc = lab[ins[1]]
            elif op == 'rand': r[ins[1]] = s.rw.pop(0); s.ops += 1
            elif op == 'f38':
                s.units += 1; s.m0 = [r[x] for x in ins[1]]
                cv = s.cvforce if s.cvforce is not None else compress(IV, s.m0); s.cv = cv
                for x, y in zip(ins[2], cv): r[x] = y
            elif op == 'succ': s.succ = (ins[1], v(ins[2])); return
            elif op == 'halt_ok': return
            elif op == 'obs': s.obs.append(v(ins[1]))
            else: raise ValueError(op)

A2REC = []; GREC = []
def tables():
    """A2 records (4 words) and G records (16 words)."""
    if A2REC: return
    A, E = TX[0], TX[1]
    for a2 in emb()['A2']:
        e6 = (A[6] + a2 - S0(A[5]) - MAJ(A[5], A[4], A[3])) & M
        e5b = (A[5] - S0(A[4]) - MAJ(A[4], A[3], a2)) & M
        var, _ = variant(A[0], A[1], a2); (_, _, Wx), (_, _, Wy) = var
        w0 = a2 | ((Wx[10] + s1(TX[2][15])) & M) << 32 | S0(a2) << 64 | e6 << 96 | e5b << 128
        cx = c9x(a2); cy = (cx - DIFF[9][0]) & M
        A2REC.append((w0, cx | cy << 32 | Wx[10] << 64 | Wy[10] << 96, 0, 0))
    for g in G:
        rec = []
        for m, (A_, E_, W_) in enumerate((TX, TY)):
            w16 = g if m == 0 else (g - DW16) & M
            e16 = (A_[12] + E_[12] + S1(E_[15]) + CH(E_[15], E_[14], E_[13]) + K[16] + w16) & M
            a16 = (e16 - A_[12] + S0(A_[15]) + MAJ(A_[15], A_[14], A_[13])) & M
            rec.append((e16, a16, (A_[13] + E_[13] + S1(e16) + CH(e16, E_[15], E_[14]) + K[17]) & M,
                        (-A_[13] + S0(a16) + MAJ(a16, A_[15], A_[14])) & M))
        (e16, a16, c17, a17), (e16y, a16y, _, _) = rec
        mE, vE, _, _ = CELL['E'][17]; mA, vA, _, _ = CELL['A'][17]
        for k1, i1, b1, ne, k2, i2, b2 in XROW[17]:          # conditions against row 16 fold into masks
            if i1 == 16:
                bit = ((e16 if k1 == 'E' else a16) >> b1 & 1) ^ ne
                if k2 == 'E': mE |= 1 << b2; vE |= bit << b2
                else: mA |= 1 << b2; vA |= bit << b2
        p = PLUS[17]; mE |= p; vE |= e16 & p
        GREC.append((c17, mE, vE, a17, mA, vA, g, a16, e16, a16y, e16y, 0, 0, 0, 0, 0))

def ebase(j, a1, k):   # P5 list words: c7 + BIAS, fields word without g
    E = emb(); a0 = E['A0'][j]; a2 = E['A2'][k]; c7 = variant(a0, a1, a2)[1]; k10 = A2REC[k][0] >> 32 & M
    u = (a2 - S0(a1) - K[2] - (a1 & a0)) & M
    return c7 + BIAS, a1 | u << 32 | (a1 ^ a0) << 64 | k << 128 | S0(a1) << 144 | (k10 + a1 & M) << 224

def gimm(gi): return GREC[gi][2] << 96 | gi << 138 | GREC[gi][0] << 224

def gindex(cv, j, a1, k):
    E = emb(); wx = pair(cv, variant(E['A0'][j], a1, E['A2'][k])[0])[0]
    w16 = (s1(wx[14]) + wx[9] + s0(wx[1]) + wx[0]) & M
    return G.index(w16) if w16 in G else ALIVE[0]

def entry(cv, j, a1, k, last=False):
    c7p, fl = ebase(j, a1, k); gi = gindex(cv, j, a1, k)
    return c7p + FLAG * last, (fl + gimm(gi)) & W256, gi

def _du(ins):
    """(defs, uses) of an instruction (register names only)."""
    op = ins[0]; S = lambda x: [x] if isinstance(x, str) else []
    if op in ('add', 'sub', 'and', 'or', 'xor'): return [ins[1]], S(ins[2]) + S(ins[3])
    if op == 'rsub': return [ins[1]], [ins[3]]
    if op in ('shl', 'shr', 'ld'): return [ins[1]], [ins[2]]
    if op in ('ldi', 'rand'): return [ins[1]], []
    if op == 'sti': return [], S(ins[2])
    if op == 'st': return [], [ins[1]] + S(ins[2])
    if op in ('bz', 'bnz'): return [], [ins[1]]
    if op == 'bne': return [], S(ins[1]) + S(ins[2])
    if op == 'f38': return list(ins[2]), list(ins[1])
    if op == 'succ': return [], [ins[2]]
    if op == 'obs': return [], [ins[1]]
    return [], []

def regalloc(a, k=64):
    """Liveness on the CFG, greedy colouring with k registers: virtual -> 'R<n>'."""
    c, lab = a.c, a.lab; n = len(c)
    succ = []
    for pc, ins in enumerate(c):
        op = ins[0]
        if op == 'jmp': succ.append([lab[ins[1]]])
        elif op in ('bz', 'bnz'): succ.append([pc + 1, lab[ins[2]]])
        elif op == 'bne': succ.append([pc + 1, lab[ins[3]]])
        elif op in ('succ', 'halt_ok'): succ.append([])
        else: succ.append([pc + 1] if pc + 1 < n else [])
    du = [_du(ins) for ins in c]; live = [set() for _ in range(n + 1)]; changed = True
    while changed:
        changed = False
        for pc in range(n - 1, -1, -1):
            out = set().union(*[live[s] for s in succ[pc]]) if succ[pc] else set()
            d, u = du[pc]; inn = (out - set(d)) | set(u)
            if inn != live[pc]: live[pc] = inn; changed = True
    adj = {}
    for pc in range(n):
        out = set().union(*[live[s] for s in succ[pc]]) if succ[pc] else set()
        for d in du[pc][0]:
            adj.setdefault(d, set())
            for x in out:
                if x != d: adj[d].add(x); adj.setdefault(x, set()).add(d)
        for u in du[pc][1]: adj.setdefault(u, set())
    col = {}
    for v in sorted(adj, key=lambda v: -len(adj[v])):
        used = {col[x] for x in adj[v] if x in col}
        col[v] = min(r for r in range(k + 1) if r not in used)
        if col[v] >= k: raise ValueError('more than %d registers needed' % k)
    return {v: 'R%d' % r for v, r in col.items()}

def rename(a, mp):
    b = Asm(); b.lab = dict(a.lab); b.n = a.n
    for ins in a.c:
        b.c.append(tuple([ins[0]] + [mp.get(x, x) if isinstance(x, str) and x in mp else
                                      ([mp[y] for y in x] if isinstance(x, list) else x) for x in ins[1:]]))
    return b

def gen_epilogue(a, caps):
    """Halt if a work counter exceeds its cap; group counter and loop."""
    halt = a.new('halt')
    for r, cap in zip(('NE', 'NW', 'N1', 'N2'), caps):
        a('rsub', 't1', cap, r); a('shr', 't1', 't1', 255); a('bnz', 't1', halt)   # cap - r < 0 (two's complement)
    a('add', 'NG', 'NG', 1)
    a.lab_pending = halt

RMAP = {}; PCACHE = {}
CAPS = (1 << 200,) * 4; NGROUPS = 1     # the interpreter runs one group
def program(js, alloc=True):
    key = (tuple(js), alloc)
    if key not in PCACHE: PCACHE[key] = _program(js, alloc)
    return PCACHE[key]

def _program(js, alloc=True):
    tables(); a = Asm(); a.L('group'); gen_prologue(a); rare = []
    for p in sorted({j // 4 for j in js}):
        gen_pack(a, p)
        for k in range(4):
            if 4 * p + k in js: gen_block(a, 4 * p + k, k, rare)
    gen_epilogue(a, CAPS)
    a('bne', 'NG', NGROUPS, 'group')                   # group loop (2 operations)
    a.L(a.lab_pending); a('halt_ok',)
    for r in rare: gen_rare(a, *r)
    if not alloc: return a
    if not RMAP: RMAP.update(regalloc(_program([0, 1, 4, 5], False)))   # two packs
    return rename(a, RMAP)

def _c(op): return 2 if op in ('bz', 'bnz', 'bne') else 0 if op in ('f38', 'obs', 'succ', 'halt_ok') else 1
def _cost(ins): return sum(_c(i[0]) for i in ins)

# Declared counts (cert.py; proof.md 5.1, 5.3)
DECL = dict(pro=95, ep=19, pack=61, ent=6, w7=46, n1=28, deep=3155, count=150, fill=240, hdr=(4, 8, 10),
            enum=(44, 10, 67, 38))

def counts():   # static path costs
    p = _program([0, 1, 2, 3], False); c, L = p.c, p.lab
    ix = lambda t: [i for i, x in enumerate(c) if x[:len(t)] == t]
    def upto(i, ops):
        n = 0
        while c[i][0] not in ops: n += _c(c[i][0]); i = L[c[i][1]] if c[i][0] == 'jmp' else i + 1
        return n + _c(c[i][0])
    pk, ep = ix(('add', 'E0p'))[0], ix(('rsub', 't1', CAPS[0], 'NE'))[0]
    ent = max(upto(L[k], ('bz',)) for k in L if k[:4] == 'loop')
    b = [Asm() for _ in range(8)]
    gen_build_pass(b[0], 0); gen_build_pass(b[1], 1); gen_zero(b[2]); gen_prefix(b[3]); gen_flag(b[4])
    gen_enum_setup(b[5]); gen_enum(b[6]); gen_enum_outer(b[7]); r0 = b[6].lab['ret' + min(b[6].lab)]
    return dict(pro=_cost(c[:pk]), ep=_cost(c[ep:ix(('bne', 'NG'))[0] + 1]), pack=_cost(c[pk:ep]) - 4 * ent, ent=ent,
                w7=max(4 + upto(L[k] + (k[0] == 's'), ('bnz',)) for k in L if k[:3] in ('sel', 'r17')),
                n1=max(_cost(c[i:j]) for i, j in zip(ix(('add', 'N1')), ix(('add', 'N2')))),
                deep=max(upto(i, ('succ',)) for i in ix(('add', 'N2'))), count=_cost(b[0].c), fill=_cost(b[1].c),
                hdr=tuple(_cost(x.c) for x in b[2:5]), enum=(_cost(b[5].c), _cost(b[7].c),
                _cost(b[6].c[:r0]) + _cost(b[6].c[-3:]), _cost(b[6].c[r0:-3])))

# Organizer experiment vt-q3-smc-r38: a reduced replica of the preregistered SMC (proof.md 6.2, 10.1).
Q3X = dict(K=20, NP=64, MS={17: 128, 18: 4, 19: 4, 20: 1, 21: 1, 22: 1}, MT=512, POOL_LOG2=-101.45)

def _step(A, E, W, i):
    E[i] = (A[i-4] + E[i-4] + S1(E[i-1]) + CH(E[i-1], E[i-2], E[i-3]) + K[i] + W[i]) & M
    A[i] = (E[i] - A[i-4] + S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])) & M

def _sched(W, i): return (s1(W[i-2]) + W[i-7] + s0(W[i-15]) + W[i-16]) & M

def _base():
    p = []
    for (A_, E_, W_) in (TX, TY):
        A = [0] * R; E = [0] * R; W = [0] * R
        for i in range(12, 16): A[i], E[i] = A_[i], E_[i]
        for i in range(8, 16): W[i] = W_[i]
        p += [A, E, W]
    return p

def _rowok(p, i):
    return rowok((p[0], p[1], p[2]), (p[3], p[4], p[5]), i)

def _copy(p): return [x[:] for x in p]

def smc_replica(rng, variants):
    """One replicate: estimate, survivors, tail successes, pairs, failed rebuilds."""
    NP, MS, MT = Q3X['NP'], Q3X['MS'], Q3X['MT']; est = 32 / 2.0 ** 32; parts = []; stages = []
    for _ in range(NP):
        p = _base(); g = G[rng.randrange(32)]; p[2][16] = g; p[5][16] = (g - DW16) & M
        _step(p[0], p[1], p[2], 16); _step(p[3], p[4], p[5], 16)
        if not _rowok(p, 16): raise AssertionError('G')
        parts.append(p)
    for i in range(17, 23):
        m, v, _, _ = CELL['E'][i]; pq = PLUS[i]; fb = bin(m).count('1') + bin(pq).count('1'); surv = []
        for p in parts:
            for _ in range(MS[i]):
                q = _copy(p); Ax, Ex, Wx, Ay, Ey, Wy = q
                e = (rng.getrandbits(32) & ~m & M) | v
                if pq: e = (e & ~pq & M) | (Ex[i-1] & pq)
                Wx[i] = (e - (Ax[i-4] + Ex[i-4] + S1(Ex[i-1]) + CH(Ex[i-1], Ex[i-2], Ex[i-3]) + K[i])) & M
                dw = (s1(Wx[i-2]) - s1(Wy[i-2]) + Wx[i-7] - Wy[i-7] - (T7 if i == 22 else 0)) & M
                Wy[i] = (Wx[i] - dw) & M
                _step(Ax, Ex, Wx, i); _step(Ay, Ey, Wy, i)
                if _rowok(q, i): surv.append(q)
        stages.append(len(surv)); est *= len(surv) / (NP * MS[i]) * 2.0 ** -fb
        if not surv: return 0.0, stages, 0, [], 0
        parts = [surv[rng.randrange(len(surv))] for _ in range(NP)]
    m23, v23, _, _ = CELL['W'][23]
    tb = [(30, 0, 1), (31, 1, 1), (21, 14, 0), (25, 16, 0)]       # W23 two-bit conditions imposed (bit, from, ne)
    f = bin(m23).count('1') + len(tb); wt = 2.0 ** (32 - f) / 287309824; hits = bad = 0; pairs = []
    VW = {}
    for p in parts:
        for _ in range(MT):
            vi = rng.randrange(len(variants)); j, a1, k = variants[vi]; a0, a2 = emb()['A0'][j], emb()['A2'][k]
            if vi not in VW: (_, _, Wvx), (_, _, Wvy) = variant(a0, a1, a2)[0]; VW[vi] = (Wvx, Wvy)
            Wvx, Wvy = VW[vi]
            w = (rng.getrandbits(32) & ~m23 & M) | v23
            for b, c, ne in tb: w = (w & ~(1 << b) & M) | ((((w >> c) & 1) ^ ne) << b)
            w7 = (w - s1(p[2][21]) - p[2][16] - s0(Wvx[8])) & M
            if not inF7(w7): continue
            q = _copy(p); Ax, Ex, Wx, Ay, Ey, Wy = q
            for i in (8, 9, 10): Wx[i], Wy[i] = Wvx[i], Wvy[i]
            Wx[23] = w; Wy[23] = (s1(Wy[21]) + Wy[16] + s0(Wy[8]) + w7 + D7) & M; ok = True
            for i in range(23, R):
                if i > 23: Wx[i] = _sched(Wx, i); Wy[i] = _sched(Wy, i)
                _step(Ax, Ex, Wx, i); _step(Ay, Ey, Wy, i)
                if not _rowok(q, i): ok = False; break
            if not ok: continue
            hits += 1; r_ = rebuild(q, w7, a0, a1, a2)
            if r_ is None: bad += 1
            else: pairs.append(r_)
    stages.append(hits)
    return est * hits * wt / (NP * MT), stages, hits, pairs, bad

def rebuild(q, w7, a0, a1, a2):
    """W0..W7, CV1 by inverting steps 7..0; returned only as a verified SFS collision."""
    Wx = q[2]; W = {7: w7}
    for i in range(8, 16): W[i] = Wx[i]
    W[6] = (Wx[22] - s1(Wx[20]) - W[15] - s0(w7)) & M
    for i in (5, 4, 3, 2, 1, 0): W[i] = (Wx[i+16] - s1(Wx[i+14]) - W[i+9] - s0(W[i+1])) & M
    var, _ = variant(a0, a1, a2); (A, E, _), _ = var; A = dict(A); E = dict(E)
    for i in range(7, -1, -1):
        A[i-4] = (E[i] - A[i] + S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])) & M
        E[i-4] = (E[i] - A[i-4] - S1(E[i-1]) - CH(E[i-1], E[i-2], E[i-3]) - K[i] - W[i]) & M
    cv = [A[-1], A[-2], A[-3], A[-4], E[-1], E[-2], E[-3], E[-4]]
    if not valid(var): return None
    wx, wy = pair(cv, var)
    if wx[:8] != [W[i] for i in range(8)] or wx == wy or compress(cv, wx) != compress(cv, wy) or not inF7(wx[7]): return None
    tx, ty = trace(cv, wx), trace(cv, wy)
    for i in range(-4, R):
        for k in 'AE':
            m, v, d, _ = CELL[k][i] if i >= 0 else (0, 0, 0, 0)
            X = tx['AE'.index(k)][i]; Yv = ty['AE'.index(k)][i]
            if X & m != v or X ^ Yv != d: return None
        if i >= 0 and (tx[1][i] ^ tx[1][i-1]) & PLUS[i]: return None
        if i >= 16 and not rowok(tx, ty, i): return None
    return cv, wx, wy

def q3_experiment(req):
    V = emb()['VS']; K_ = Q3X['K']; rows = []; zs = []; allp = []; okall = True
    for tr in req['trials']:
        t = tr['trial']; row = dict(trial=t, message_a_hex=None, message_b_hex=None)
        if t < K_:
            seed = bytes.fromhex(tr['seed'])
            rng = random.Random(int.from_bytes(hashlib.shake_256(b'vt-q3' + seed).digest(32), 'big'))
            z, st, hits, pairs, bad = smc_replica(rng, V); zs.append(z); allp += pairs
            good = hits > 0 and bad == 0 and len(pairs) == hits; okall &= good
            row['observations'] = dict([('log2_estimate', math.log2(z) if z > 0 else -1000.0), ('tail_successes', hits),
                ('verified_pairs', len(pairs)), ('failed_rebuilds', bad)] + [('survivors_row%d' % (17 + i), n) for i, n in enumerate(st[:6])])
            if good:
                cv, wx, wy = pairs[0]
                row['message_a_hex'] = (struct.pack('>8I', *cv) + struct.pack('>16I', *wx)).hex()
                row['message_b_hex'] = (struct.pack('>8I', *cv) + struct.pack('>16I', *wy)).hex()
        elif t == K_:
            zbar = sum(zs) / len(zs) if zs else 0.0
            row['observations'] = dict(log2_pooled_mean=math.log2(zbar) if zbar > 0 else -1000.0, replicates=len(zs))
            if okall and len(zs) == K_ and zbar >= 2.0 ** Q3X['POOL_LOG2']:
                cv, wx, wy = allp[-1]
                row['message_a_hex'] = (struct.pack('>8I', *cv) + struct.pack('>16I', *wx)).hex()
                row['message_b_hex'] = (struct.pack('>8I', *cv) + struct.pack('>16I', *wy)).hex()
        rows.append(row)
    return dict(schema_version=1, trials=rows)

# Organizer experiment vt-ram-r38 (proof.md 10.2).
def ram_experiment(req):
    E = emb(); rows = {}; ok0 = counts() == DECL
    for tr in sorted(req['trials'], key=lambda tr: tr['trial'] % 8):   # one program at a time
        t = tr['trial']; js = [(32 * t + k) % 256 for k in range(32)]
        if (tuple(js), True) not in PCACHE: PCACHE.clear()
        rb = hashlib.shake_256(b'vt-ram' + bytes.fromhex(tr['seed'])).digest(64)
        rw = [int.from_bytes(rb[:32], 'little'), int.from_bytes(rb[32:], 'little')]
        mach = Machine(rw, lambda j, Y, Z0: [E['A0P'][j]]); mach.run(program(js)); m0, cv = mach.m0, mach.cv
        mis = (not ok0) + (cv != compress(IV, m0) or m0 != [(rw[k // 8] >> 32 * (k % 8)) & M for k in range(16)])
        ref = []; n1 = n2 = 0
        for (j, Y, Z0, n), jj, gi in zip(mach.trace, js, mach.gis):
            a1, k = E['A0P'][jj]; wx = pair(cv, variant(E['A0'][jj], a1, E['A2'][k])[0])[0]
            mis += j != jj or (Y, Z0) != yz0(cv, E['A0'][jj]) or n != 1
            if inF7(wx[7]):
                w = trace(cv, wx)[2][17]; ref.append((w, gi)); g = GREC[gi]; e = (w + g[0]) & M; x = (e + g[3]) & M
                n1 += e & g[1] == g[2]
                n2 += e & g[1] == g[2] and x & g[4] == g[5] and not (x >> 11 ^ x) & 0x200 | (x >> 12 ^ x) & 0x40 | (x >> 9 ^ x) & 0x100
        cnt = [mach.r.get(RMAP[x], 0) for x in ('NE', 'NW', 'N1', 'N2')]
        charge = DECL['pro'] + DECL['ep'] + 8 * DECL['pack'] + sum(x * DECL[y] for x, y in zip(cnt, ('ent', 'w7', 'n1', 'deep')))
        mis += len(mach.trace) != 32 or len(mach.obs) != len(ref) or [(o - GREC[g][0]) & M for o, (_, g) in zip(mach.obs, ref)] != [w for w, _ in ref]
        mis += cnt != [32, len(ref), n1, n2] or mach.ops > charge or mach.succ is not None
        a1, k = E['A0P'][js[0]]; ws = pair(cv, variant(E['A0'][js[0]], a1, E['A2'][k])[0])
        h = [None if mis else struct.pack('>32I', *(m0 + w)).hex() for w in ws]
        rows[t] = dict(trial=t, message_a_hex=h[0], message_b_hex=h[1], observations=dict(blocks=len(mach.trace),
                       w7_passes=len(ref), mismatches=mis, ops=mach.ops, units=mach.units, charge=charge, first_tests=cnt[2]))
    return dict(schema_version=1, trials=[rows[tr['trial']] for tr in req['trials']])

# Table construction (P6, proof.md 5.1), counted code.
def gen_build_pass(a, fill):   # count or fill pass over R_j for one Y
    lp = a.new('bl'); a.L(lp)
    a('ld', 'EB', 'P'); a('add', 'q', 'P', 1); a('ld', 'C9', 'q')
    if fill: a('add', 'q', 'P', 2); a('ld', 'EBc', 'q')
    a('and', 'A1', 'EB', M); a('add', 'U', 'Y', 'A1'); a('and', 'U', 'U', M)
    rot32(a, 'sU', 'U', 7, 18, 3, shr3=True)
    a('sub', 'X', 'sU', 'A1'); a('add', 'X', 'X', 'C9')
    for gi in ALIVE:
        a('rsub', 'Z', G[gi], 'X'); a('and', 'Z', 'Z', M)
        if not fill: a('add', 'Aw', 'YB', 'Z'); a('ld', 'c', 'Aw'); a('add', 'c', 'c', 1); a('st', 'Aw', 'c')
        else:
            a('add', 'Aw', 'YB', 'Z'); a('ld', 'o', 'Aw'); a('sub', 'o', 'o', 1); a('add', 'e', 'EB', gimm(gi))
            a('st', 'o', 'EBc'); a('add', 'o2', 'o', DELTA); a('st', 'o2', 'e'); a('st', 'Aw', 'o')
    a('add', 'P', 'P', 3); a('bne', 'P', 'PE', lp)

def gen_zero(a):
    lp = a.new('zl'); a.L(lp); a('st', 'I', 0); a('add', 'I', 'I', 1); a('bne', 'I', 'IE', lp)

def gen_prefix(a):
    lp, sk = a.new('pl'), a.new('ps'); a.L(lp)
    a('ld', 'c', 'I'); a('bz', 'c', sk); a('add', 'OFF', 'OFF', 'c'); a('st', 'I', 'OFF')
    a.L(sk); a('add', 'I', 'I', 1); a('bne', 'I', 'IE', lp)

def gen_flag(a):
    lp, sk = a.new('fl'), a.new('fs'); a.L(lp)
    a('ld', 'h', 'I'); a('bz', 'h', sk); a('sub', 't', 'h', 1); a('ld', 'e', 't'); a('or', 'e', 'e', FLAG); a('st', 't', 'e')
    a.L(sk); a('add', 'I', 'I', 1); a('bne', 'I', 'IE', lp)

def build_selftest(j=0):
    E = emb(); a0 = E['A0'][j]; a1 = E['A0P'][j][0]; m = Machine([], None); m.load = lambda ad: m.mem.get(ad, 0)
    lst = [(a1, k) for k in range(768) if valid(variant(a0, a1, E['A2'][k])[0])] + [(x, k) for jj, x, k in E['VS'] if jj == j]
    for i, (x, k) in enumerate(lst):
        c7p, fl = ebase(j, x, k)
        for t, w in enumerate((fl, c9x(E['A2'][k]), c7p)): m.mem[REG['RL'] + 3 * i + t] = w
    HB = REG['HDR'] | j << 64; r = random.Random(9); Ys = [r.getrandbits(32) for _ in range(2)]; ops = []; off = REG['ENT'] + 1
    for fill in (0, 1):
        a = Asm(); gen_build_pass(a, fill); a('halt_ok',); n0 = m.ops
        for Y in Ys: m.r = {'Y': Y, 'YB': HB + (Y << 32), 'P': REG['RL'], 'PE': REG['RL'] + 3 * len(lst)}; m.run(a)
        ops.append(F(m.ops - n0, len(Ys) * len(lst)))
        for ad in sorted(ad for ad in m.mem if ad >> 200 == 1 and not fill):   # sparse prefix
            if m.mem[ad]: off += m.mem[ad]; m.mem[ad] = off
    for ad in sorted(ad for ad in m.mem if ad >> 200 == 1):   # sparse flag pass
        if m.mem[ad]: m.mem[m.mem[ad] - 1] = m.mem.get(m.mem[ad] - 1, 0) | FLAG
    m.mem[off - 1] |= FLAG; ref = {}; bad = 0
    for Y in Ys:
        for x, k in lst:
            X = (s0((Y + x) & M) - x + c9x(E['A2'][k])) & M
            for gi in ALIVE: ref.setdefault(HB + (Y << 32) + ((G[gi] - X) & M), []).append(gi)
    for ad, gis in ref.items():
        h = m.mem[ad]; Y, Z0 = (ad - HB) >> 32, (ad - HB) & M; want = []; got = []
        for x, k in lst:
            w16 = (s0((Y + x) & M) - x + Z0 + c9x(E['A2'][k])) & M
            if w16 in G and G.index(w16) in ALIVE: c7p, fl = ebase(j, x, k); want.append((c7p, (fl + gimm(G.index(w16))) & W256))
        for i in range(len(gis)):
            w = m.mem[h + i]; f = w >> 33 & 1; bad += f != (i == len(gis) - 1); got.append((w - FLAG * f, m.mem[h + i + DELTA]))
        bad += sorted(got) != sorted(want)
    return len(lst), len(ref), max(map(len, ref.values())), bad, ops


# Variant enumeration (P5, proof.md 5.1), counted code: A1 = st + i (i < 2^29) per (A0, A2 record kk).
def gen_enum_setup(a, wl=1 << 29):
    (A, E, W), (_, Ey, _) = TX, TY
    a('and', 't', 'a2', A[4] ^ A[3]); a('xor', 't', 't', A[4] & A[3])
    a('rsub', 'b5', (A[5] - S0(A[4])) & M, 't')
    a('add', 'e6', 'a2', (A[6] - S0(A[5]) - MAJ(A[5], A[4], A[3])) & M); a('and', 'e6', 'e6', M)
    a('add', 'c9x', 't', (E[9] - 2 * A[5] + S0(A[4]) - S1(E[8]) - K[9]) & M)
    a('and', 'u', 'e6', ~E[8] & M); a('xor', 'u', 'u', E[8] & E[7]); a('sub', 'c9x', 'c9x', 'u'); a('and', 'c9x', 'c9x', M)
    a('sub', 'c9y', 'c9x', DIFF[9][0]); a('and', 'c9y', 'c9y', M)
    a('xor', 'Q', 'a2', A[3]); a('and', 'P', 'a2', A[3])
    a('add', 'c4', 'a0', (A[4] - S0(A[3])) & M)
    a('and', 'hx', 'e6', E[7]); a('and', 'hy', 'e6', Ey[7])
    rot32(a, 'sa', 'a2', 2, 13, 22); rot32(a, 'se', 'e6', 6, 11, 25)
    a('add', 'r7', 'sa', (E[7] - 2 * A[3] - K[7]) & M); a('sub', 'r7', 'r7', 'se')
    a('and', 'PA', 'a2', 'a0'); a('xor', 'QA', 'a2', 'a0'); a('xor', 'ne6', 'e6', M); a('shl', 'KS', 'kk', 64)
    a('and', 'a1', 'e6', 0xe0000000); a('sub', 'a1', 'a1', 'b5'); a('and', 'a1', 'a1', M)
    a('add', 'aend', 'a1', wl); a('and', 'aend', 'aend', M)
    a('shl', 'KS', 'kk', 128); a('add', 'a2k', 'a2', -K[2] & M)

def gen_enum(a):
    (A, E, W), (_, Ey, _) = TX, TY
    lp, nx = a.new('el'), a.new('en')
    a.L(lp)
    a('add', 'e5', 'b5', 'a1'); a('and', 'e5', 'e5', M)
    a('xor', 't', 'e6', 'e5'); a('and', 't', 't', PLUS[6]); a('bnz', 't', nx)
    a('sub', 'w9x', 'c9x', 'a1'); a('and', 'w9x', 'w9x', M); a('sub', 'w9y', 'c9y', 'a1'); a('and', 'w9y', 'w9y', M)
    rot32(a, 'sx', 'w9x', 7, 18, 3, shr3=True); rot32(a, 'sy', 'w9y', 7, 18, 3, shr3=True)
    a('sub', 'd', 'sx', 'sy'); a('and', 'd', 'd', M); a('bne', 'd', DIFF[9][1], nx)
    a('and', 't', 'a1', 'Q'); a('xor', 't', 't', 'P'); a('sub', 'e4', 'c4', 't')
    for m, (E_, h) in enumerate(((E, 'hx'), (Ey, 'hy'))):
        w = ('w8x', 'w8y')[m]
        a('and', 'u', 'e5', ~E_[7] & M); a('xor', 'u', 'u', h)
        a('rsub', w, (E_[8] - A[4] - S1(E_[7]) - K[8]) & M, 'e4'); a('sub', w, w, 'u'); a('and', w, w, M)
    a('sub', 'd', 'w8x', 'w8y'); a('and', 'd', 'd', M); a('bne', 'd', DIFF[8][0], nx)
    rot32(a, 'sx', 'w8x', 7, 18, 3, shr3=True); rot32(a, 'sy', 'w8y', 7, 18, 3, shr3=True)
    a('sub', 'd', 'sx', 'sy'); a('and', 'd', 'd', M); a('bne', 'd', DIFF[8][1], nx)
    a.L('ret' + lp)
    a('and', 'mj', 'a1', 'QA'); a('xor', 'mj', 'mj', 'PA')
    a('and', 'v', 'e6', 'e5'); a('and', 'w', 'ne6', 'e4'); a('xor', 'v', 'v', 'w')
    a('add', 'c7', 'r7', 'mj'); a('sub', 'c7', 'c7', 'v'); a('and', 'c7', 'c7', M)
    rot32(a, 's', 'a1', 2, 13, 22); a('and', 's', 's', M)
    a('sub', 'u', 'a2k', 's'); a('and', 't', 'a1', 'a0'); a('sub', 'u', 'u', 't'); a('and', 'u', 'u', M)
    a('xor', 'qq', 'a1', 'a0'); a('add', 'kc', 'a1', 'k10')
    a('or', 'ebc', 'c7', BIAS); a('or', 'eb', 'a1', 'KS')
    a('shl', 'u', 'u', 32); a('or', 'eb', 'eb', 'u'); a('shl', 'qq', 'qq', 64); a('or', 'eb', 'eb', 'qq')
    a('shl', 'kc', 'kc', 224); a('or', 'eb', 'eb', 'kc'); a('shl', 's', 's', 144); a('or', 'eb', 'eb', 's')
    a('st', 'LP', 'eb'); a('add', 'q', 'LP', 1); a('st', 'q', 'c9x'); a('add', 'q', 'LP', 2); a('st', 'q', 'ebc')
    a('add', 'LP', 'LP', 3)
    a.L(nx)
    a('add', 'a1', 'a1', 1); a('and', 'a1', 'a1', M); a('bne', 'a1', 'aend', lp)

def gen_enum_outer(a):
    a('add', 'ra', 'kk', 'kk'); a('add', 'ra', 'ra', 'ra'); a('add', 'ra', 'ra', REG['A2T']); a('ld', 'a2w', 'ra')
    a('and', 'a2', 'a2w', M); a('shr', 'k10', 'a2w', 32); a('and', 'k10', 'k10', M)
    a('add', 'kk', 'kk', 1); a('bne', 'kk', 768, 'top')

def enum_selftest(j=0, L=4096):
    E = emb(); a0 = E['A0'][j]; a1k, k = E['A0P'][j]; a2 = E['A2'][k]; RL = REG['RL']
    sa = Asm(); gen_enum_setup(sa); sa('halt_ok',); la = Asm(); gen_enum(la); la('halt_ok',); bad = found = ops = 0
    for w in (0, 1):
        m = Machine([], None); m.load = lambda addr: m.mem.get(addr, 0)
        m.r = {'a0': a0, 'a2': a2, 'kk': k, 'LP': RL, 'k10': A2REC[k][0] >> 32 & M}; m.run(sa); setup = m.ops
        lo = ((m.r['a1'] if w else a1k) - L // 2) & M
        m.r['a1'] = lo; m.r['aend'] = (lo + L) & M; m.run(la); ops += m.ops - setup
        got = [tuple(m.mem[RL + i + t] for t in range(3)) for i in range(0, m.r['LP'] - RL, 3)]
        want = [(lambda c, f: (f, c9x(a2), c))(*ebase(j, x, k)) for x in ((lo + i) & M for i in range(L))
                if valid(variant(a0, x, a2)[0])]
        found += len(want); bad += got != want
    cand, ret = DECL['enum'][2:]
    return found, bad, setup, ops, 2 * L * cand + found * ret

def row17(gi):
    """Number of E17 passing both row-17 tests of G[gi] (bitwise with carry)."""
    _, mE, vE, a17, mA, vA = GREC[gi][:6]; st = {(0, 0): 1}
    for b in range(32):
        nx = {}
        for (cy, kb), n in st.items():
            for e in ((vE >> b & 1,) if mE >> b & 1 else (0, 1)):
                s = e + (a17 >> b & 1) + cy; x = s & 1; k = kb | (x << (6, 8, 9).index(b) if b in (6, 8, 9) else 0)
                if mA >> b & 1 and x != vA >> b & 1 or b in (18, 17, 20) and x != kb >> (18, 17, 20).index(b) & 1: continue
                nx[s >> 1, k] = nx.get((s >> 1, k), 0) + n
        st = nx
    return sum(st.values())

def bucket_run(cv, js, bk):
    m = Machine([1, 2], lambda j, Y, Z0: list(bk.get(j, [])), cvforce=cv); m.run(program(js)); return m

def sfs_check():
    E = emb(); good = tot = 0
    for t in E['SFS']:
        a0, a1, a2 = t[:3]; cv = list(t[3:11]); j, k = E['A0'].index(a0), E['A2'].index(a2); dec = E['A0P'][j]
        r16, w7, deep, (tx, ty, wx, wy) = outcome(cv, a0, a1, a2)
        for pos in range(3):
            bk = [dec, dec]; bk.insert(pos, (a1, k)); m = bucket_run(cv, [j], {j: bk}); tot += 1
            good += (r16 and w7 and deep == R - 1 and m.succ == (j, entry(cv, j, a1, k, pos == 2)[0])
                     and compress(cv, wx) == compress(cv, wy) and wx != wy)
    return good, tot

def selftest():
    """Expected output: proof.md Appendix A.1."""
    E = emb(); ok = True; rng = random.Random(5)
    tx, ty = trace(PCV, PMX), trace(PCV, PMY)
    c1 = compress(PCV, PMX) == compress(PCV, PMY) and all(rowok(tx, ty, i) for i in range(16, R))
    print('1 published pair collides, rows 16..37 hold:', c1); ok &= c1
    n = 0
    for g in G:
        q = _base()
        for i in range(12, 16):
            for k in range(3): q[k][i], q[3 + k][i] = tx[k][i], ty[k][i]
        q[2][16] = g; q[5][16] = (g - DW16) & M; _step(q[0], q[1], q[2], 16); _step(q[3], q[4], q[5], 16); n += _rowok(q, 16)
    print('2 G: %d values, %d pass row 16' % (len(G), n)); ok &= n == 32
    t = [row17(gi) for gi in range(32)]; ok &= sum(t) == 1 << 20 and ALIVE == [i for i in range(32) if t[i]]
    print('2 row 17 holds for some E17 for %d words of G (both tests: %d = 2^20 values in all); never for %s'
          % (len(ALIVE), sum(t), ' '.join('%08x' % G[i] for i in range(32) if not t[i])))
    a2bad = 0
    for a2 in E['A2']:
        (Ax, Ex, Wx), (Ay, Ey, Wy) = variant(TX[0][0], TX[0][1], a2)[0]; m, v, _, _ = CELL['E'][6]
        a2bad += not (Ex[6] & m == v and not (Ex[7] ^ Ex[6]) & PLUS[7] and
                      ((Wx[10] - Wy[10]) & M, (s0(Wx[10]) - s0(Wy[10])) & M) == DIFF[10])
    print('3 A2 list: %d distinct values, %d violate the A2-only conditions' % (len(set(E['A2'])), a2bad)); ok &= a2bad == 0
    pb = sum(not valid(variant(E['A0'][j], a1, E['A2'][k])[0]) for j, (a1, k) in enumerate(E['A0P']))
    vb = sum(not valid(variant(E['A0'][j], a1, E['A2'][k])[0]) for j, a1, k in E['VS'])
    print('4 invalid embedded variants: %d of 256, %d of %d' % (pb, vb, len(E['VS']))); ok &= pb == 0 and vb == 0
    nb = 0
    for t in range(300):
        j, a1, k = E['VS'][rng.randrange(len(E['VS']))]; cv = [rng.getrandbits(32) for _ in range(8)]
        var, c7 = variant(E['A0'][j], a1, E['A2'][k]); wx, wy = pair(cv, var); tx, ty = trace(cv, wx), trace(cv, wy)
        for i in range(16):
            for kk in (0, 1):
                m, v, d, _ = CELL['AE'[kk]][i]
                nb += tx[kk][i] & m != v or tx[kk][i] ^ ty[kk][i] != d
            nb += bool((tx[1][i] ^ tx[1][i-1]) & PLUS[i])
        Y, Z0 = yz0(cv, E['A0'][j]); w16 = (s1(wx[14]) + wx[9] + s0(wx[1]) + wx[0]) & M
        nb += wx[7] != (c7 - cv[0]) & M or wx[1] != (Y + a1) & M or w16 != (s0((Y + a1) & M) - a1 + Z0 + c9x(E['A2'][k])) & M
        nb += any(((tx[2][i] - ty[2][i]) & M, (s0(tx[2][i]) - s0(ty[2][i])) & M) != ((TX[2][i] - TY[2][i]) & M, (s0(TX[2][i]) - s0(TY[2][i])) & M) for i in range(8, 16))
        nb += tx[2][17] != ty[2][17] or (tx[2][16] - ty[2][16]) & M != DW16
    print('5 variant soundness, 300 random chaining values: %d mismatches' % nb); ok &= nb == 0
    g, n = sfs_check()
    print('6 counted program on the semi-free-start vectors (entry first/middle/last): %d of %d found and verified' % (g, n)); ok &= g == n == 12
    c = counts(); print('7 static costs', c, '== declared:', c == DECL); ok &= c == DECL
    regs = {x for ins in program(list(range(8))).c for x in ins[1:] for x in (x if isinstance(x, list) else [x])
            if isinstance(x, str) and x[:1] == 'R' and x[1:].isdigit()}
    print('8 physical registers: %d' % len(regs)); ok &= len(regs) <= 64
    for j in (0, 5):
        v, nb, mb, bad, ops = build_selftest(j); ok &= bad == 0 and ops == [150, 240]
        print('9 table build, toy A0 index %d: %d variants, %d buckets (largest %d), %d mismatches; ops per (Y, variant): '
              'count %s, fill %s' % (j, v, nb, mb, bad, ops[0], ops[1]))
    for j in (0, 5):
        found, bad, setup, ops, bound = enum_selftest(j); ok &= bad == 0 and ops <= bound
        print('10 variant enumeration, toy A0 index %d: 8192 candidates, %d valid, %d mismatches; setup %d; executed %d <= %d'
              % (j, found, bad, setup, ops, bound))
    print('SELFTEST', 'OK' if ok else 'FAILED')
    return ok

tables(); ALIVE = [i for i in range(32) if row17(i)]   # L0
assert counts() == DECL, 'operation counts differ from the declared ledger counts'


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'selftest': sys.exit(0 if selftest() else 1)
    req = json.loads(sys.stdin.read())
    out = q3_experiment(req) if req['experiment_id'].startswith('vt-q3') else ram_experiment(req)
    sys.stdout.write(json.dumps(out, sort_keys=True, separators=(',', ':')))

