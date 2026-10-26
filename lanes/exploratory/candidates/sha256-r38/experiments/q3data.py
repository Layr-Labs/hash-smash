"""r38-q3-deep-rate-data: the estimator layer of our registered deep-rate run O (proof.md Section 7a), recomputed
from the attached per-seed tool outputs. Corroborating evidence in r38g: the charged q3r is the inherited 2^-71.4010
(rule min(inherited, measured)); this run's Ville bound 2^-71.1939 is reported beside it. Nothing here samples SHA-256.
Tool q3walk.c (sha256 TOOL_SHA256), plan sha256 PLAN_SHA256, raw per-seed JSONs sha256 RAW_SHA256 (participant-run,
outside the sandbox). DATA: 360 lines, subset-major, k = 1..72: prefix_log2 EXACT_u1 SAMPLES_u1 EXACT_u0 (SAMPLES_u0
= 2^28); zlib + base85, DATA_SHA256 = sha256 of the text (asserted). Lr = prefix_log2 + log2(EXACT/SAMPLES) + 27; Y_k =
mean_s 2^Lr(s, k, u1); Ville: inf{m : K(m) < 100}, K(m) = 0.9 prod Y_k/m + 0.1 mean_c prod (1 + c (Y_k/m - 1)).
Trial 0 recomputes every statistic and hard-asserts EXPECT (proof.md Section 7a); no message pair."""
import sys, json, math, zlib, base64, hashlib, statistics as st
TOOL_SHA256 = 'a2b67714dbea10267a8925f7bf4c1ffd91d4cde27ed9b322b21934a3157cea2a'
PLAN_SHA256 = '17d9961009499388ae5fbb265803e69cb227e8c14b6391b893e6e7412a7a979f'
RAW_SHA256 = '82c48bb7af7f17d18c236ee16ff84c9d2f866794f0ee61c7a4bc14db8d007a49'   # sha256 over the 720 raw JSON files, u0 then u1, by file name
SUBSETS = [[4 * s + i for i in range(4)] for s in range(5)]
OFFS = [0, 1, 4, 5, 1024, 1025, 1028, 1029]
SEEDS = [[40000 + 1000 * s + k for k in range(1, 73)] for s in range(5)]
DATA_SHA256 = 'ea786749e6c3d561f7de58bd918755633faf8b313b63725f45a688a4d12ace44'
DATA = zlib.decompress(base64.b85decode(
    'c-mE(NtPwKjzj0UinoCuM}4#ZjnxGknOB}1M1-50NfZeJp#J;c8UIS_tDdvw`K^9`b?rUtI=@=_UjO~?%ztH;Hs<Vg{N`x(#GPaR?kIx?+P{1DsHczJers'
    '+$aLSxTuQ=yF`v`yUYxFvKqT4IVD2pd%S@y);ynEkqct@XlV%@vy@7}U`p#K|nx6#M>&AaRcs}|O<+OZ$+y34$0@hhwOA{QIs3uj(iWnV1&mfl#ysQv_t)'
    '+$%=RrY<?7+0ZK!=A7u*K%ttqR&>^xnurzDfR@PWJ9$q-^Z-=v@%X%AEU=Qc-bAd*#l#ham!qnk5rF0`_e~<x_zXzQd^z%44$xX?ta+xUFG^-Stl!-{5tR'
    'USM+VK*#3&k5{U1qooLuPPd%*j-lMIqf3>r-({Ag(d5)j@UgdXt_czpa+hy%-^9_HX&7p6sT|HXo&b~WY!cJo&{rW0e<^@SJn%=Q$q}I`?_tNbvtJN~rI)'
    '`-@e+TEyR%iD^yZ4UDQ-@cSNUg5(C2fbjq7eJSv7P(!ca=`$OUaKM&SUn{NR2)H(Dv=NjOp*_WepO%E4z+|YuQ5iwjX>uoqy`2=e$t^ip`yC=T6qxwRSz='
    'heml^En{Clcxt35T$IuACobno$k+6MlAxD^C2Ofjdtl$Hb+)nXiM}}b#v&@O@C0Sgyn@Af>JVObp{!VS`bH+nb<Zdk&((R9bXIzv*hjf4f_D8CLx18!UHL'
    'g8`)n0;EKiLy1~p20P|RKgjdHe#d$|w7K)6-Naq#P|Wq@$KOiCm7iqhrfr_z~a9ACyJ^ph$g5NmrKQ8qgGJ$r0rj?tBzS<bB;rC+(n9+;IAV3}6V@x)Qp7'
    '7EPQ$q6-%ZBuE}&%JO;zq?Bu3E$iVqY|!auQ;>vG{^4HH&qUtsS2$e-)R+Womo6D3Wwav8CqtX`kmTGIon=wI?FnBXc6%Z%7fH8YejapN$RyaGTx-|w0L*'
    'V&ZcO!J(ODh5mIDpA8SVX&Or_gmC^QN=X+Mo-HT-KQGo6Al>mF%80_>0AS`x7%7Yv1v<39_W$~^aiw$b_F}0C6k+TfsiJu>8qws*cy<h&0w%U(_^~CA5HZ'
    'X5=6|;YYpDQo=aQFmL)){?sN^=Jwv}IKk`P*un9dIPztp{Q(AO!@BMF5uUMn~%4ISXw~;mH@!otBQkFhJ*VtxwDZ6k!sl$f3_0fWkWn_jTYqZ5HBpd;OqM'
    '$ER2Yu5nJlvl4bSUj<D?Pt<5=eV47sfzIm=-v<Y;0$9FKu$nU?8u#UQFDhyd)iZ}o(OwIPwVF58Q?B4(R%-)g&9-T(>Y9$focdI&i5gO}3URfOfFy5LW%-'
    'GnLxUY!({JaAO;rNl=~2mhl31s|hR2E76A93x%mW@&0~CM9j_j<Cot!uLL4&W^RS&<;M(Xisl?fD7%7Qm|D1?MR9g=?n5MhT@+0XLHPTgWfb;qIZMw3>T3'
    '4{ld8Z|T`+@vaiQWTyY1u)l|uN4ss`a1l8jzs2ot*fG72l<f#W>H3U{%KaTTRSsgB;YIpZ~=CbOF@iO)9|Gmn52NR6dikyzN<$Iuod76iJ_?~F}k1H(#!5'
    '`J6=&QRnW)x3h0%PaV;-1c!KbjFaj7}sl0xP=-lqu*#KfX)@X@Jq_YB7#xB{J>GxL&w|WWQXaVCb4&i)*58eK8PgtEu+vqDgi73eF3Ya4_pHXuxtNF2X?X'
    ';7C`ik!bkk=Ency6fig3_WoHy)thlj8xv0PQ~Hy>RQqPKwbfD#Lfe5%Vu)f6cuQPFbYYlZR$S)j?$*IP##C^Kt0o=M*#1sM(o$gzBf`x9F;nQ~uXR{pXao'
    'vD4#_F@e@jB|!;SEaEH=#q|86XD{K>91nJ)TIY^cux{Xes9mi9CKV>dRD0ykB{=P@hmNF>@q^{3N*R$iQwSgJY7bA)egl^#fDB<0k12sm)s``8<X>0+r?~'
    '4YcqoPPZ(palAS^@#x>OT{#n#mb=!DT&+vF*j^lKH=f#q-lIpBGLyz*fzM9}(CWGGFOR-uOSGPJd&L&=Zy$;*eSiW%57hKZv-O&kFjWFSyX8LZd})v3*ns'
    'CgLImUy|zbwC9gC-Nq_5Y6aJZ7*YfrWJGv^rGaU1V^Qj5#<fWr-JYc0RUPf!Jfk1c;5~2LylLZROS7Yf^X#5nY5@y)=*~a#<a6H@8jaf<5`u9)T265_XH$'
    'cbSAZ@Fac-!6oX%(($Ff!FyRI!faJ)A_80&XY^o#O&>j2+-GK;!veBN8ut5zqXhu_iJvy{#@csUO(3rbIA+DY{acak!>k838O>wf&A$=uKcI#z;Tqsru$E'
    '1d(X@fD*eT#utGE{OvGOA`s!EUEJBV<L}I(eg)(R2p%P&n-L(voBv8IQfHEOaO>>Xq~oN3AJ}SwkyN=y9%;FSXMp1!r`vajjhp&+#^)TpUUHL~Y+<PE`2}'
    'W(PP)H9g*TbY2DuEy7hf+Sy*jH?j537m|SNg<t6;lZvdVuc7Xo93q#&*e&rLM59>Lo~mHI4WJ%cXVf#Sz_M#NH1%7lPO*SI)-C74Qp1}ku!C38ikS%BExH'
    'jOup-clGbMd42OqLRn#>pKLJn;}Yol2DGZJWQ;)i)A;<@0I7=0qSSg}gX{gOei5mS&AF#?9KsC0lEMB>tIj;eKL%d&!RC;CaJI|KG2+X0aGdc-Zah-a1LR'
    '}*HdacI-@W(!eE^CIBH=xd$Rpj@3XXaL5IMEv<wfp(%wnjycX1j$0al1#T6DD<6D4}7>3PfdX?z%4R|e6v%Y4xLSu-iv^xUT0pR;5pc7O+NcC;rDJZU1cq'
    '5kyKMt3iz8Y)9h5I-T>0A@(I$joIlQ)x>%^Rbg02Wd7n{{>pNYF4epR+fiDx1FfA5iN4*nn1mrp|xmdIljg`_Fgzw_PJN=`h9Tn^ZPhqMREx~Kp>WrP3{N'
    '5)TAHItyzRb2fdDCGf=roN|{6<cO?a^EUm2Fu8p(2R<rD-eiisF2x#b$AbI`0|M1*_*~4K?Zw^})HCzw;qaGub*Lc`nrmohFQ5YFx2i{D&a^k~eq>>~C$a'
    '*J?fTb$Jj#`3jPLmYk?w9t#NBL?Xf1@xHRVr8!~pgCmEFs+hwMcakJ9*W`rbCf92$FBQi~@WTYQhocwc)J8UT5I`$!pk^ija)?X8%8*XMVLDmz{fP2eVh='
    'nP)h2%Qj4Ie3z7tZXzi_a9`%3lAUQxUe>Nm^;<Hf*zcu1Hxm`6sO!Wta<9N-Yjv+A8yk$63NnDJNKH38G53Jr*(*oHCu=&!OLr=gP$cBUt%(k4R!od6caL'
    'M~LxQv)IA@O=PWGRumHLb#-Jh*s^EFTgB;l#gc}s=+uLiGXw3kWfkd>{>X;R*nI0Dim5@`Mb<*?2a}P{tt!*G*QJCIE=_V)?ULdgR!I6Bv8U|BmPIM$vF|'
    '#z(JU~6&jpxn6_vm-P|c`vPuftP7gQ6Q&;dR`OsH(ObWVTLWTTHt5s$ULcYHYh8tQn&KjMMioI2SL-2Zf76EtBD5BA%^!xY&fPL3L4O%T{fg$BHA8GOO&z'
    'JL9p2XIs3f99NR!wG=8eZ9?j3CS+RV8AfUeBSXR2!lJ-Hex%YQd>IdnpKf6|(#pUDUogwbo2ngfh$IZ~9o0V)u8FFu`=>e5(<(8qu~$wK~Fi!Bs(u38Z6{'
    'YSuC|N(u|233%Mc*YR0YL7@romUu)TPAfqche`C=e3f!cIwr<v|7>-ZaIut{h<E^0(~f7;s!3CtVJGt^n4oN>N4b=zas_831^yr@MQYFWL}`27hFIYCkRU'
    'L|=PdFT<H2o3B@5!vTKl;-=h!<+&~c!mD?T)sx%>%PDwOigWgO-F5S}dGtC{gRxZw$&#ZTVq6iG9hLE~s4q9!8-TH};(4fE!jQoCoRlcmhss^!#S0*60@2'
    'wKa32EZenT5rCoEI@3LqcXp0m#R1AnkHzMaOgJkNQl1X2e%*rB5FjeKF65SG}TFk2eeUTkR_%BX#%Oq8`TJT0`Y+W4hh1rqNaO)^+pHBlQxs*xpH7%lLiV'
    'q7ac=}a=ZZSEtx;^7iXd)HGqYqj^-Xc<dlR(QU@!8y23Kl#IjJ@G>FcICirg44B_mWI^=I;hdlz}scOvuul%kF@bFQG`V8@qDu`CI<ix5Nd*+`Ur1{6R8y'
    '4>xof-e1z>0-F&R>_00cKA9t|kLThDGL%Yk2PiHX+hb!$wFw)bp{n>h3u83acYN`~=H5<;%9|PECHfHR3yRyIR!zbq*1(hZK^?GU2KvnVp&6DH~{05SgK9'
    'q=z{Sf}Q)3<ZuWKkYi0RT3WY|*We+V;*l6;U58U8J5ierYR5+DZiti5ABQ05D<x_kAK*|D$0VbFrA{lQb;9(Z4M;qg(-ehbnv8HbM>v+$vX*~qMLAwOS@$'
    'tDh++#U(W!yiP5lh(cfu{-cr+VjvDwqJ)~tWuw1r_XGS(TTM$JQDk3h25z;cwnG|+wtMpm2C6b#cmbiiys4|2(aH|)95;b|B|QQ2`~CNYfGx6mh`3NqIRG'
    '?5*&sbWz4uxF_|N>v7&Ga|73ndM<1o<k9-ika@HCQ!oMYZ}T)<E>|O!pM9=o?Zcb92P5!r==xpDVR2<h%$B5*Ar6ez(r=2GYxvh(SYlI7USJEp{XNxf*F9'
    'pr?yklLL_)$44X;^o8Uw>bHlWoDZ+40C<E}k%d<!?fEJ@sQ&fr^ovQlELFrMdF-8a`GR0n$8&3j(nC3^sK6qXn3F@Cic4)B55=%N3A<tM|vIJqE!ZJ^z1V'
    'vS`fx%`0B?=qWWF!4`1NP0F^0$LZi#Z$Ve_oYfSSC>#cOa3Cd4jls&QOI@zm~I%OPmv+&~)d(Y`gT~+b{qOt5k0Qx|%EvSGF2FTk?&T6jj-0<5<@wf*!+!'
    'be1`B8lP=7l*drZPmSKNmN^p|#r+eEW<m@_95XSD5u=^2iMJW!s2#`yya`Lz^Qstn+Jq&HV;MXQP-Iy|#W#a}>O2N0AP?TCY`v86+b0GkW{jjo6*aPDM1B'
    '@y3T==03Zi=)8))qu*y`HC?g4+mFyYsnK4$$xJqK+PlC#P?)ac?}e2@~xuV`WD;z2RO?KTZaHf}c#Za7t}p?1Yf863wtt2^Ma3XT~?v#s-u(8g{awi5WbZ'
    'Lo7cmMP_?9IsjKFl!i+EVTggHqACp@vO#3sBLN%;<=fUo6&LTrRah#c9`>k+Fib!Y-^wkeyiPD2>#c0e?F5Smfi#2TK<KlJDu>vz*V!6q9M#1t!cPg-Yj2'
    'Us#)1v<jr*!Nrod2ZOmvO)!>!pZ^xw>d4IY<;&0H@9a4QhA!foLI}$X2HnELZrEi>0{fOxZp=`ZfyAF^eg<&npshj9XkzAfy=kn~*^#N;IdD96|3Svs-kE'
    'lkmmzzwMmPliUBwm&gu1GibH{)Uh*eHiYKJZh|*Q+4zMrgDIc-a#{|Eg{v$d7fH*6*`fn|9t5oyN^}BGa-qFEcgAW;VW~kYcY@ei?_2zKF&+bd?7qKBp&U'
    'hnX~ZH?GW#=ry$g#8&qk+GFj?$UknYYLh>k5fHX8AvM~xV*)5LU2ZY873yIaukRt1$X*B@^OgN(Z)(xT+WWgB1iYCOa3TTSHkmV!oIi9K{2v{@e%)lwH`3'
    '>h5M8{!fdKDvr#*ahP<G0<_`GGDsr!*~&Fj$lislL}#oujm5rzbPVagcRxsCKn4O)5(W&s5GKLXJ0JoA_&=N)-3OXHQHTM>`Fjq29|dPra}R^s5}nN+xWo'
    'hPuIcd%FlT>YFV<33_iu@{XIb@3-1YTQ}y4qGD5P1h-?9^sd37>zI2pX++M%m+{Ug25Z?Tw{Df=hRR_IPeU!?Ux3}yR-tx6x~q^sebIHf-KpjRp=mQB|j6'
    '3J{$JCVM(Zme5QNfh~|hk{Ow7s0Q*f0IR|G{?>3DRcdj&L<(x#j_8S2@s|wemDtlm&e=@XK&9|2P5M6-AXwUh;Bi<rSF;iew+O|>57-G{aw^&tNjKK*&uZ'
    'cnj7nZN&x7_lg5ntfgY<?0)CPl};v@qgz`M~;~OWUK-fY@;ik8MX)@EB7_!Y3;rj{KVJt?Cmipbc^~BwG{vng$XOtaPS{<??%WH>;hE6m!e={_d{{q@AiT'
    'Hb$-tnL6nVLVM4jN$1i{5fa*(NxWki%N?Qfbw^2+EhZ9`s^R?e3Zw|#5|^(R%x*bT&Rax?V%;{`X1OirpmG9W2fh`}-8cf9Iph?w=t%E~i7U9UbZ6qV3Vy'
    '?fJW(RX_qm=|?;jskT;=50SM-zXH*0*iBabc}?r<Z-Wgz3QpWhAwdWLb>8>P;>1}$HFD;w6bOT4<$kQZmg=$ow~8fWpFjlnazCctv!--STX#k{JK7H3fl^'
    'C#kVZ+H7<#bAz5BWYzlCf#8)Ww;ikO7a<vUjIxGL%fW<c%ZF7M&_GH=rZ2Z`F2T&+qYA;+v~kUvQ<JY#xF}*E(1$fiDKX?5}Q(Q*)=3_jI{O`fmzcFB`46'
    'Qt=T>00JhyiUx&4Vx7Bq8=dEH)<FLErU8JLF#5KpF{hd;d?csug@XRz_8~1Z=w=q#!DGM-r0rB=-csgM><n1tckBpJ_M)9Y&{^o;CK0n&7m}wlq29#RFN6'
    'o9sLUCw9(lRYe`Pb69Mn0kp{uurAt17m=^3wJdfC@bGBHY=|4WoIBK3dE_7Hb6V%}sC#FiyD5ytCi|9M8X?2!b5>r)niT);X;ajOSI^Kk6n(h^TNeTS%lM'
    'C-5$dc&Jh;t6Db-Ul>gwtFu3j3c9%=+sl9d2fu?59R')).decode()
EXPECT = {'exact_u0': 3677167, 'exact_u1': 230490, 'mix_u0_lin': -71.077385190428, 'mix_u0_t99': -71.1824870991, 'mix_u0_ville': -71.198155093024, 'mix_u1_lin': -71.072022745619, 'mix_u1_t99': -71.179767495579, 'mix_u1_ville': -71.193877657977, 'n_seeds': 720, 'sub0_u0_mean': -71.383170864879, 'sub0_u0_ville': -71.474995856535, 'sub0_u1_lin': -71.201459226458, 'sub0_u1_mean': -71.37806922552, 'sub0_u1_t99': -71.594870007087, 'sub0_u1_ville': -71.469866114383, 'sub1_u0_mean': -71.213524787611, 'sub1_u0_ville': -71.306453486658, 'sub1_u1_lin': -71.086373854069, 'sub1_u1_mean': -71.215351542763, 'sub1_u1_t99': -71.399626551634, 'sub1_u1_ville': -71.308269241576, 'sub2_u0_mean': -71.320703432711, 'sub2_u0_ville': -71.412655517163, 'sub2_u1_lin': -71.122767406768, 'sub2_u1_mean': -71.320899160409, 'sub2_u1_t99': -71.538129056669, 'sub2_u1_ville': -71.412777471818, 'sub3_u0_mean': -71.105353434916, 'sub3_u0_ville': -71.198494426436, 'sub3_u1_lin': -70.980041431561, 'sub3_u1_mean': -71.095267776791, 'sub3_u1_t99': -71.270500679253, 'sub3_u1_ville': -71.188376391432, 'sub4_u0_mean': -71.105278943594, 'sub4_u0_ville': -71.198515483338, 'sub4_u1_lin': -70.981929683116, 'sub4_u1_mean': -71.102676086104, 'sub4_u1_t99': -71.274837342628, 'sub4_u1_ville': -71.195869724967, 'ueff_lb99': -0.003710299162, 'ueff_mean': 0.003153534425}

def tq(df):   # one-sided 0.99 Student quantile (Cornish-Fisher; the reader of the registered plan uses the same)
    z = 2.3263478740
    g1 = (z**3 + z) / 4; g2 = (5*z**5 + 16*z**3 + 3*z) / 96; g3 = (3*z**7 + 19*z**5 + 17*z**3 - 15*z) / 384
    g4 = (79*z**9 + 776*z**7 + 1482*z**5 - 1920*z**3 - 945*z) / 92160
    return z + g1/df + g2/df**2 + g3/df**3 + g4/df**4


def ville_lb(x, delta=0.01, cs=(0.75, 0.5, 0.25), w1=0.9):
    def K(m):
        terms = [math.log(w1) + sum(math.log(t / m) for t in x)] if min(x) > 0 else []
        terms += [math.log((1 - w1) / len(cs)) + sum(math.log1p(c * (t / m - 1)) for t in x) for c in cs]
        mx = max(terms)
        return mx + math.log(sum(math.exp(v - mx) for v in terms))
    lo, hi = max(x) * 1e-30, max(x)
    if K(lo) < math.log(1 / delta):
        return 0.0
    for _ in range(300):
        md = math.sqrt(lo * hi)
        if K(md) >= math.log(1 / delta): lo = md
        else: hi = md
    return hi


def stats():
    assert hashlib.sha256(DATA.encode()).hexdigest() == DATA_SHA256
    rows = [l.split() for l in DATA.strip().split('\n')]
    assert len(rows) == 360
    Lr = {1: [[0.0] * 72 for _ in range(5)], 0: [[0.0] * 72 for _ in range(5)]}
    ex = {1: 0, 0: 0}
    for i, r in enumerate(rows):
        s, k = divmod(i, 72); p = float(r[0]); e1, n1, e0 = int(r[1]), int(r[2]), int(r[3])
        assert e1 > 0 and e0 > 0 and n1 > 0
        Lr[1][s][k] = p + math.log2(e1 / n1) + 27
        Lr[0][s][k] = p + math.log2(e0 / 2**28) + 27
        ex[1] += e1; ex[0] += e0
    lin = lambda v: 2.0 ** (v + 72)
    out = {'exact_u1': ex[1], 'exact_u0': ex[0], 'n_seeds': 720}
    for u in (1, 0):
        Y = [st.mean(lin(Lr[u][s][k]) for s in range(5)) for k in range(72)]
        lY = [math.log2(y) - 72 for y in Y]
        out['mix_u%d_ville' % u] = math.log2(ville_lb(Y)) - 72
        out['mix_u%d_lin' % u] = math.log2(st.mean(Y)) - 72
        out['mix_u%d_t99' % u] = st.mean(lY) - tq(71) * st.stdev(lY) / math.sqrt(72)
        for s in range(5):
            v = Lr[u][s]; X = [lin(t) for t in v]
            out['sub%d_u%d_mean' % (s, u)] = st.mean(v)
            out['sub%d_u%d_t99' % (s, u)] = st.mean(v) - tq(71) * st.stdev(v) / math.sqrt(72)
            out['sub%d_u%d_lin' % (s, u)] = math.log2(st.mean(X)) - 72
            out['sub%d_u%d_ville' % (s, u)] = math.log2(ville_lb(X)) - 72
    D = [Lr[1][s][k] - Lr[0][s][k] for s in range(5) for k in range(72)]
    out['ueff_mean'] = st.mean(D); out['ueff_sd'] = st.stdev(D)
    out['ueff_lb99'] = st.mean(D) - tq(len(D) - 1) * st.stdev(D) / math.sqrt(len(D))
    return out


def check(out):
    for key, v in EXPECT.items():
        assert abs(out[key] - v) <= (0 if isinstance(v, int) else 1e-9), (key, out[key], v)
    assert out['mix_u1_ville'] <= out['mix_u1_lin']


def serve():
    req = json.load(sys.stdin); rows = []
    for t in req['trials']:
        row = {'trial': t['trial'], 'message_a_hex': None, 'message_b_hex': None}
        if t['trial'] == 0:
            o = stats(); check(o)
            row['observations'] = {k: o[k] for k in ('mix_u1_ville', 'mix_u1_lin', 'mix_u1_t99', 'mix_u0_ville', 'ueff_mean', 'ueff_lb99',
                                                     'sub0_u1_mean', 'sub1_u1_mean', 'sub2_u1_mean', 'sub3_u1_mean', 'sub4_u1_mean',
                                                     'exact_u1', 'exact_u0', 'n_seeds')}
            row['observations']['asserted'] = 1
        rows.append(row)
    sys.stdout.write(json.dumps({'schema_version': 1, 'trials': rows}, sort_keys=True, separators=(',', ':')) + '\n')


if __name__ == '__main__':
    if '--print' in sys.argv:
        print(json.dumps(stats(), indent=1, sort_keys=True))
    else:
        serve()
