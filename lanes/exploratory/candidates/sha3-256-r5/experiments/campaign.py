#!/usr/bin/env python3
"""Reduced-budget run of the campaign CAMP of proof.md Section 5 on sha3-256-r5-prefix-v1.

Once per run, before the trials: the first block is replayed (one five-round call computes N) and the chart
is checked (Lemmas 1 and 2); the certificate of Lemma 3 is computed exactly (the round-0 quotient is T1 on
all of each set, and the round-1 quotient, a quadratic there, reduces to the constant T2 on the chart); the
18 filter planes of Lemma 4a are derived from L(T2) and every constant bit of the third-chi quotient is
checked against T3; a start-up comparison runs the finite-difference walk of Lemma 4b on set 0 with one lane
and 2^12 visits, initialised only from the visits of Gray weight at most 8, and asserts that every visit
agrees with the direct filter.  Each organizer trial is then one complete campaign with its own coins
(random.Random seeded by the trial seed): per set a uniform invertible 135 x 135 matrix (columns drawn in
turn, each redrawn while in the span of the earlier ones, at most MATRIX_CAP draws per column) and a
translation; the visit of Section 5 at reduced width (2 lanes x 8 blocks per set, i.e. the Gray indices 0
to 15, the visits of the scalar campaign of 9223524c): tables initialised from the direct filter on the
down-set, every block one word step whose operations are counted and asserted (proof.md 7.3), survivors
taken in the scalar visiting order, re-evaluated with the five native rounds and recorded as 176-byte
records (digest, fragment, padding), at most N_RED; the 32-pass byte radix sort on the digest between two
arrays; the adjacent scan; the native verification of an equal-digest pair.  In every trial whose index is
divisible by PLANT_EVERY the six random translations are replaced by six stored survivors of our
preregistered sample (proof.md 8.1), so that records, sorting and the scan run on real survivors.  Checks
beside the algorithm: the planes and the verdict of every visit against the direct filter
("fes_mismatch"), the first two chi conditions at every visit ("invalid"), and every record's digest
against the complete target hash of its message ("record_mismatch").  A trial returns a message pair only
when two distinct messages with equal complete digests are found, otherwise two nulls.  Python standard
library only; reads the organizer request on stdin.
"""
import base64
import json
import random
import struct
import sys
from math import comb

PREFIX_INDEX = 7258270406            # first block M0 = LE64(PREFIX_INDEX) || 128 zero bytes
SETS, DIM = 6, 135                   # six parameter sets of 135 free bits
LANE_BITS, WALK_BITS, LOW_BITS = 1, 3, 2   # reduced walk: 2 lanes x 2^3 blocks (production: 8, 86, 16)
DEG, VIRT = 8, 7                     # degree bound of every plane (Lemma 4a); virtual walk coordinates (4b)
L_RED, N_RED = 16, 8                 # reduced budget: visits per set, record cap (production: L, N)
MATRIX_CAP, PLANT_EVERY = 128, 4     # draws per matrix column (as in production); planted trials
SELF_BITS, SELF_LOW = 12, 4          # start-up comparison: one lane, 2^12 visits, low split 4
CHARGE = 675                         # operations charged per word step of one set (proof.md 7.3)
M32, M64 = (1 << 32) - 1, (1 << 64) - 1
RC = (0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000, 0x000000000000808B)
RHO = (0, 1, 62, 28, 27, 36, 44, 6, 55, 20, 3, 10, 43, 25, 39, 41, 45, 15, 21, 8, 18, 2, 61, 56, 14)
# Target quotients (low half XOR high half of each lane, lanes 0..24) after rounds 0, 1 and 2.
T1 = tuple(int(w, 16) for w in "746a0114 b8e201a0 6240005a 6d5804fd 858c0255 f46a0116 b8f201e0 6642005a 6d5804f5 858c0255 f46a0116 b8e201e0 6242005a 6d5804f5 858c0255 f46a0156 b8e201e0 6242005a 6d5800f5 858c0255 f46a0116 b8e201e0 6246005a 6d5804f5 858e0257".split())
T2 = tuple(int(w, 16) for w in "80008080 00000001 00000000 00000000 00008000 80000000 00000000 00000000 00000000 00008000 00000080 00000001 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00008000 00000000 00000000 00000000 00000000".split())
T3 = tuple(int(w, 16) for w in "0000000a 00000000 00000000 00000000 00000000 00000008 00000008 00000400 00000000 00000000 00000002 00000000 00000000 00000000 00000000 00000000 00000008 00000400 00000000 00000000 00000000 00000000 00000000 00000000 00000000".split())
# Chart (base85): 135 free directions and 6 correction directions (67 bytes, coordinates 0..535 of a),
# 6 bases (100 bytes), the shared quadratic coefficients (count, then pair index i*135+j and a 6-bit
# mask), linear parts (6 sets x 6 corrections x 17 bytes), constants (6 bytes), D (100 bytes).
CHART = """
0RR91000000000001yBG01yBG0000003ZMW0Du4hfIt8M01$ux0caoq04M+e0Du4hfB*mh004jh06-uB04M+g000000000000000
00000000000000000000000000000000000000000000000000000000000200000000O8000000000000000000000000000000
0000000000000000000000000000000000000000000O80000003ZMW0000000000000000001h00000002M$0sue(1OcD`00004
AOKJR01yxW0sufE1OWg50001lARquh01!|BfB*mh0000000000000000000$000000000W06_o%ARqt$000CefKUJeK@b2T06`!C
004jh000DJ5I{g80T2KH0ssI2000C40000000000005u>000000RTh*03ZMW001BW00aa8KmY;|0003Y0001l0Du4x00bmLLO=o-
0000400000000000000000000000000000000000000000000000004000000000000000000000000000000000O80000000000
00000000000000000000000000000000000000O800000000000000000000000000000001yBG0000000000000000000000000
0000000000000000000001yBG000000000000000000000000000000AOHXW0000000000000000000000000000000000000000
00000AOHXW00000000000000000000000000000$000000000000000000000000000000000000000000000000000000000000
00000000000000$00000004jh000000000000000000000000000000000000000000000004jh0000000000000000000000000
00000000310000000000000000000000000000000096100000000000003100000009610000000000000000000000IC200000
00000000000000000000LI3~&KmY&%pa1{>00blePyzxF5CH)IKp+4C0Du4h00ble06+o|QUCw|1ONyC00000000000000G00000
1ONa)000000RRDj0000G1ONa41ONa4000000RRC2000000000$1ONy?00008000000000000000000005C8xO000000003100961
000000000006+i$0003100961000005C8xG06+i$000mG00000000000000000000000000000000000000000000000;m800000
00000000000000000<BO0000003ZNB000000000006+i$03ZMW0000000002000010000000aO40000$fB*mj0000106+i$00aO4
03ZMWfB*mhKmY&$000000000000000000000000$004kO0RVu300000ga7~xAOHab004kM0RVsi00001ga80cU;u$e0001h00000
0000000000001BW0001hKmZT`0DuDkfPnx20RsR4KmmlHKmh;%0DwUN0D%Yr0RsVq0001>0D%Ak0000200000000000000000000
000020000006+i$03ZMW0000a08jt|5D)+X06-uB004jh0000a06;(j5D)+W000C4000000000006+i$00000000C400000KmY&$
AOHaX001BWP=E#y5C8)JKwtm>0KfnM001BWKtKi%5C8xG00;m80000000000000000000000;m800aO400031000001ONa400}@q
00000fB*pi00IC21ONa400=-p000005C8xG00000000mG000mGKmY&$5CCWZU;uysARs^h00004003$L5Kt%pU;v>2000C40Du4l
P!K=>Fc4?}0000W000000000000000000000000W0000G06+i`03ZMW0000a08juT5D)+X06-uR004jh0000a06;(@5D)+W002M$
000000000000000000000000000000KmY&$00001000000000000000KmY&$0000100000002M$0000000031000000000G01yBW
00IDj0000e07wAA0Vn~$01yBW1O$L?0096f06+lXfd~Nv004jx1QvjV0004K0000000aO400000000mG000mG00000001BW1OUMR
0DwRM009t$00C$q001Ze1OmYT0Du4h0001l00BTC00bxi000005C8xG000000000000000000000000000000000000000000000
5C8xG00000000000000000000000000000W000000000000000000000000000001000000000000aO40000W000010000000000
00aO40000000000004jh00000000000000000000004kM000000RVu300000ga82qAOL^>000000RVsi00000gaCm=AOL_u00000
00062000000000000000KmY&$00062AOHXW03ZMW000040000008s(}AOHaX000000Du4lKo9@`AQ1up0000000aO40000000000
000000000000aO4fI<KO000000000000;m800aO4fIt8M000000096100;m8fCK;l000002mk;8000000000000000000002mk;8
000010000000000000000000000001000000000000000000000000G000000000000000000000000G00000000000000000000
00000000000000000000000000000000000001BW00000000000000000000001BW004jh0D(XN0001h001B$001BW004jh0D%Ai
0001h0000W001BW0000006+i$0000000000000000000000000000000RR91000000000006+i$000000RR91000000000000000
00000fB*mh0000000000000000000000000000000000000000000000000000000000000000000000fB*mh000000RR910000G
0Du4z000000001B06>7q0RREu009FM1S9}800MC+0YL=7Apj8ofB``S1SAMdKtfPx000000000400000000mGfB+Z(00000001BW
K!D-^0D)it009tyBmy)b0#G;rL4e>O0D%C2009YrBmxLvLeV$`00000000O80000001yBG01yBG0000003ZMW0Du4hfIt8M01$ux
0AL^h04M+e0Du4hfB*mh004jh07xJJ04N9m0000001yBG000005C8xm00000003A3U=RcVfCB{qzyJ{e5P$>#WB^G(Xiy;lfP(=6
03ZV)5CjGQ3=kMVC=vhw00000AOHXW000000000001yBG2mk;;0000$1ONb_00000MkD}G00K}D0RaF&AOHXWkN^Mx1T+8uKmt%u
000000000$000000000003Z;600000FaSUTHb4Oa6oCN%005AL1R(?<A^-qDrvL#06oCMMKmdRM1ffJAG5|sV00000004jh00000
002M$0000000000004jh06+i$03ZMW0000W08jt|5D<U?06<^>006)M0000W06;(j5D<U>000000003100000000000000000000
00000KmY&$AOHXW001BWPyhlD5C8xGKp+4B0Du4h001BWKtKWz5C8xG0000000IC200000000000000000000000000000000000
000000000000IC20000000000000000000000000000005C8xG000mGfB+Bx00000003kFPyoUK006=O00R&N003bC0AVZuK!m^n
01yBG06_r+00;;GK)`GO000000000W0000000000000000000;06+i)000350H6R60T2Kr08{`;5KsUC005x?004jj0T2Kt00ck?
5D)+W00000002M$00000000000000000000002M$0001i000000Du4h03ZMX000000001i000000Du4h03ZMX000000000000031
0006I0Du4x000000001B06+nN0RRBt0003H1S9}B00I#>06_qNApimZfB*pi1S9}JKtd6C000000000000aO4000000000$001BW
KmY&$002P%fB+x>0096%WC3^pLXi*v0R%xH00IDj00961BmhW20+A2^00000000002mk;8000000000000000000000000000000
0000000000000002mk;800000000000000000000000000000G00000000000000000000000000000000000000C4000000000G
0000000000000C4000000000000000001BW000000000000000000000000000000000000000000000001BW000000000000000
00000000000000006+i$0000000000KmY&$00000AOHaX03ZMW000040000001*HHAV2{C0000000004Ko9@`AQ1on0000000000
fB*mh00000000000000000000fB*mh00000000000000000000000000000000000000000000000000000000ssI2000005C8xG
00000KmY&$0s#O4fB*mh5Ci}K0000000000009620000000aO4KmY&$KmY&$000000000G0000G0Du4x000000000a06+jj00033
0009R0000<003Yt06>I5000pH002P&000O;06@Vk0000000000001BW000000000000000000000000000961000000000000000
001BW00961000000000000000000000000006+i$00000000000000000000000000000000000000000000006+i$0000000000
00000000000000000000009615C8xG5D)+W00000AOHXWfB*o2U;qFB5P%>6I3NHJcmMzZfB*o200aO4fPf$X03rYoI0yg$00000
000005&$3o00>|(AQ1q73=jZ7AOO&T0sx?+0000uM<D{%paK98VFQqXZUBG+xCuZBh%|x*a1xNxHUIzs00000000040000000000
0000000000000040000000000000000000000000000000000000000000000000000000000O801yBGAP@im0000G0AK(B0DuDk
0KfnN01$)#0AK(B04P8J0DuDk001BXAOHXW00<Be0B8aL000000000006+i$000000000000000000000000000000000C42mk;8
0000006+i$00000000C42mk;8000000000000000fB*mx0000G000000001D2mk<p1OS2H0000Gh9m$WAOcW02>}3rpa6jYfB*mh
gd_l1U;<Ej0000000000000000RR91000mG1ONa4N&o-=AOHXW6#xPN5di=I2mlNKNC5x<0RR910RRF30Ra#I1^^5I2mt^900000
00000000040000000000000000000006+i)0w4eY0006c0MGye5D)+X06-uB0sw#j0006c0Kh;35D)+W0000000000000O806+i$
001BW0000000000KmY&$AOHaX001BW5P$#x5C8%IKtKQh06+i$000C4000mG5C8xG000000000001yBG00000000000000003-ka
00031000001PA~C00BWj03ZMWfB*pi00IC21ONa4002Qi000000000000000AOH{mKmZT`000002mojRAOL^>1fW0w5C9N_00C|w
3sGnQqyV9SAb<n_0)P;N0ue+YDiJ6E00000000000001h01yBG01yBG0000003ZMa0D%AifIt8M01$)#0caoq04M;20D%C2fB*mh
004vl0YD%C04M+e00000000000000100000005u>00000002M$KmY&%001BW000C4KmY;|00031Kp+4B0Du4h001NaKtKWz00000
0000000000000C4000000H6Q>0000106+i)0003103ZMW00aO)00IyQ00AKYAOL{?fB+Bz03<>{Kmr&D00000000000000006+i$
0000000000000000000006+i$000001ONa4000000000000000000001ONa400000000000000000000fB*mh000000000000000
000000000000000000000000000000fB*mh0000000000000000000000000000000ssI2000000000000000000000ssI200000
0000000000000000000000000000000000000000000000001h000000000000000000000001h000001ONa4000000000000000
000001ONa40000000000000000000000001001BW00000000mG0DwXO0D%Ai0001h004|2000000Du4h0D%Yq0004m000Oe0Du4j
000000000000000000621ONb_000000000$5I_I`0000W0000406+i&5C8xH5kMdS004pj1ONae0zg0l5C8xG000000000000000
00aO400000000000000000000000000000000000000000000000aO40000000000000000000000000000002mk;80000000000
000000000000000000000000000000000002mk;800000000000000000000000000000G000000000000000000000000000000
0000000000000000000G000000000000000000000000000000001BW00000000000000006+i$03ZMW0000W08jt`5D)+W06+i$
001BW0000W06+i$5D)+W0000000000000000Du4h0000000000000000000000000000000000$00000000000Du4h000000000$
0000000000000000000000961000000000000000000000096100008000000000000000000000000800000000000000000000
00000pa1{>KmY&$000O8Ab<e@AfbQ&022^^000Ug08jt`AcP<R0D%MmAdvuoKp03MU=aWS000000000000000000000T2K{00000
06+jB06_r&0e}Di1P}lK000005dZ)n2tfe=000000RR9%06+jB6F>j}00000000000000000002000000000000000KmY&$00002
000002mk;;00000KmY&$00000000002mk;;00000000000000000000000O80000006+i$004ji0DwRs000310AvAB074KD00EEz
AOHdYfB*pi03;wlKmrsH0000000000000000000001yBG0000000000000000D%Ai0001h0000W00961000000D%Ai01yCx0000W
0096100000000000000000000fB*mh000000096100aO40RR91fB*mh00000KnMT;00000fdBvi00IC200000KnMT;0000000000
00000000000RR910000000000000000000000000000000000000000000000RR9100000000000000000000000000000400000
000000000000000000000000000000000000000000004000000000000000000000000000000004jh00000000000000000000
0000000000009610000000000004jh0000000961000000000000000000000003100000000000000000000000310ssI200000
0000000000000000ssI2000000000000000000000000000IC20000000000000000000000IC20000000000000000000000000
0000000000000000000000000000001ONa40000000000000000000000000000000000000000000001ONa4000000000000000
00000000000000000961000001ONa4000000000400961000001ONa4000000000400000000000000000000000000000000000
0ssI20000000000000000000000000000000000000000000000ssI200000000000000000000000000000$000000000000000
0000000000000000000000000000000000$000000000000000000000000000000004jh000000000000000000000000000000
000000000000000004jh00000000000000000000000000000000031000000000000000000000003100000000000000000000
0000000000000000000000000000000000000IC20000000000000000000000IC200000000000000000000000000000000000
000000000000000000001ONa4000000000000000000001ONa400000000000000000000000000000000000000000000000000
0000800000000000000000000000080000000000000000000000000000000000000000000000000000000000mG0000000000
0000000000000mG000000000000000000000000000000000000000000000000000000006+i$0000000000000000000000000
0000000000000000000006+i$00000000000000000000000000000000IC20ssI200000000000000000000000000000000000
0000000IC20ssI200000000000000000000000005C8xG0000000000000000000000000000000000000000000005C8xG00000
000000000000000000000000W000000000000961000000000W004jh00000009610000000000004jh00000000000000000000
00000002M$06+i$fI<NPfPnx2006`Q01RLNK?DE*fItBNfB*mh00D#m08AhN!A1Z800000000000000000000000000000100000
0000000000000000000000000000000000000000000010000000000000000000000000000000006200000000000000000000
00000000000000000000000000006200000000000000000000000000000000aO400000000000000000000000000000000000
000000000000aO40000000000000000000000000000002mk;80000000000000000000000000000000000000000000002mk;8
00000000000000000000000000000G000000000000000000000000G000000000000000000000000000000000000000000000
00000000000001h0000000000000000000000000000000000000000000000001h00000000000000000000000000000000000
fB*mh00000000000000000000fB*mh00000000000000000000000000000000000000000000000000000001ONa40000000000
00000000001ONa4000000000000000000000000000000000000000000000000000000W000000000000000000000000W00000
0000000000000000000000000000000000000000000000000000000KmY&$0000000aO40000000000KmY&$0000000aO400000
0000000000000000000000000000000000000000000040000000000000000000000004000000000000000000000000000000
0000000000000000000000000000O800000000000000000000000O8000000000000000000000000000000000000000000000
000000000001yBG0000000000000000000001yBG0000000000000000000000000000000000000000000000000000000AOHXW
00000000000000000000AOHXW00000000000000000000000000000000000000000000000000000000ssI2000000000000000
000000ssI20000000000000000000000000000000000000000000000000000000AOHXW002M$000000000000000AOHXW002M$
000000000000000000000000000000000000000000000000000RR91000000000000000000000RR9100000000000000000000
0000000000000000000000000000000000000IC20000000000000000000000IC200000000000000000000000000000000000
000000000000000000005C8xG000000000000000000005C8xG00000000000000000000000000000000000000000000000000
00000KmY&$00000000000000000000KmY&$00000000000000000000000000000000000000000000000000000000000400000
000000000000000000040000000000000000000000000000000000000000000000000000000000O800000000000000000000
000O8009610000006+kM0000000R&R000000006A002M*03ZNB00s~O009sH00ICB07yWA0096%0096901yxW000621ONa400000
000000000000000000000000000000000000000400000000000000000000000041ONa40000C000000001h5E29+5TJ=-pdb+d
fJ_hoBp^W4!2<*%Admq8Ab}wQ6Tko<IAKDN!A}4a0tg8Ki4HV|iV#qdxHcdF00000002M$00000AOH~%fB+x>0000000IC&00f}`
KmY^~fB*mhAOHdY00KxrAOwH_U;q&S000mGU;qFB0Du4h0000006+kMF$DmCK#&j!1ONa4LJ$fFBp^Tp5ul<#0f7L9B!NO8KoAfK
gh64TA%O-!0f7LFAX5-vAP5ow0Du4h00000000040RRF31ONyC00000000005C8xK0{{R30006200000000005dZ)H0ssO41ON&E
0)PMj0000G0RVvr0RRjFg#bW06+nU{D4+xs0EqZNKI{#_q9V@G8Uwi=Kt13oS0KpHZ-=pBUv?_Aw^~P}pr%Jxm9nUsMX*Ho_kE++
7Px4)+47Z{IP3S4hHr2E+ux%1%M`OS5Zu!c0RV#t0RRjFg#bW06+nU{D4+xs0EqZNKI{#_;v&w`Is>^LKt04M2O!G8e}}MQA66=~
x7tUfpr&J2)$*u{Rj@?&_kE++7Px4)+47Z{IP3S4hHr2E+ux%1%M`OS5Zu!c0SJKz0RRjFg#bZ16+nU{IG_L&0En<ae(Wv5<0jkC
xC5vkKzqa~3m}5Qe}=JQ9#$*0waP}Nu%c~Onew2E6_7;t_kE++7Px4)+47Z{IP3S4hHr2E+ux%1%M`OS5Zu!c0U&`00RRjFfdD}|
6##-HIDh~Y0En;vKkO~T;v(D87z3yuKsn$kTOa_@=ZCOhA9gD=wHijHvZ6^BnUW&g&9FrG_kE++7Px4)+47Z{IP3S4hHr2E+ux%1
%M`OS5Zu!c0Vsh80RRjFfdD}|6##-HIDh~Y0En;vf9x&8qbA$XxC5vkK!3z33m^i)_lB`xUREnLwTecivZiepnbIK3osdNL_kE++
7Px4)+47Z{IP3S4hHr2E+ux%1%M`OS5Zu!c0RV#t0RRjFg#bZ16+nU{IG_L&0En<aKI|>Q;v(D8I0L93Kt04M3m}5Qe}}PRA66^0
wc19du%>NS+47=`Rj@?&_kE++7Px4)+47Z{IP3S4hHr2E+ux%1%M`OS5Zu$F0!{z}SO5WX00Dyl2_OL=E&(7t0U$^LAbtTLrvU+|
0RgN50j~i8v;hIN0Rg-L0mK0T&H(|>0Rh|r0o?%s<N*Qf0Riy=0R;j9Ap!{}0uU|&11|y)G6Enr0x&`XAVmToMgky90wYWUAW{Me
Rsthh0uW#V5Mlx#V*(&#0s(3Q18V{hcmfH50t1Hv35)_Gl>!N>0t2-I1G)kU!U74}0twv$1L^_^>jDAo0txy83Ht&G{{jgU0|OWX
2`K|0L<1nK10ePT1Ns94`vU_31Oo{K0V4zfLInxn1rX!~5bOmI00s~Q1`s3$5G4i>Ck7Bf1_5IR9cl(0dIlYP1|59{9exHKg9aUr
1|60L9hwFmsRkXb1|6^l9mED5?FItw1_Ap90RjgB3I_rd2LTla0wV_jB?k#92Lmbx0XGK;O9ujU2LW{l0fGksi3b6Z2LYQ00h|W`
r3V412LZ7M0m26Z(gy)l2nomt0pbV&9SI;N2_P{EAT<dfVhIV62?3G`1Ct2@l?efs2?Lx70iFo~q6q<{2_mHl0;dT9s0jk82?DAK
1FH!GtqCBm2?4MP0<j4LxCtS=2?D+e0l*0Y!U+S#2?ECn1IP&j%n1X{2?5Rt1Jwy2*a-vU2?Ov60UQbu9||xd3IQYv5Ge`)D+&QF
3IQ()0Wb;yGztMV3IR6?0XPZ}JPHs#3IRh35k(3CM+yN*3IRz95K9UHObP*13J_ch5M2rpUkVUq3Il2i19b`khYBFO3IoOp1Jnuu
)(Q#Q3Ipg03H%BJISU{>3jsb00YVESO$#GY3m{Vq0b2_JT?+|e3j=BkAa4r^g9`((3m~}*AkhmT<O>P$3n20fAodFh1q=y03@||q
0Y?lVNDKi=3?NGkAW#e;Q4Ang3<+8c0b2|qUkngs3=n4wAZQFAYYYi+3=w$@0ecJqj0_2p3?Y*Y0h$a6qznny3<Kf}1Mmz1@(c;~
3<CrW2^b9n)eSJ+4ItkQAm$Aq=?xI=4KVo)ApH#>01gQR4g&=aAPo*M4h}I84iOR#2_Ft1C=LNC4gok0AUO^Riw*;o4gs$Y0l*Fk
3=aYF4*~fP0Ra#J3lISe5CI?%10fIrLJ$Fe5FmmOAcGJfh!7x&5Fn2b36l^Yln?`#5D=XZ5T6hrpb#LV5DBOd5VH^gz7PY%5DCc;
Akq*C1Q7uS5g`c?0SXZT3lRYi5g`x}0TK}b84&>*5g;BB0U!|pA`t;65dk+5AW#tjQV{{e5(D@W2_q8$D-!`V69G080ZS7BY!d-7
6ah070W=gKH536h6d*YiB0&@&Llgl-6e36zAW9SgPZS_g6d+O*0aO$TSQG<U6aifnAYl|BW)ul;6a#e>33?PFd=wyu6d;Kd35^s9
x)cGs6al;x0l*Xj!4v_*6amT<0m~Ev&lCaC6amu|0oW7)*%SfW6bb1R0qqnC{1gcR6#^3#AQTk|W)%aQ6$#E20oD~D*cAcU6#?B9
0pb+_<P`zs6#?lL3GEdF?iB&`6#@1YAomp@`xOcQ6$1(u2@e(lAr>Ga770}rB3%|BUKSu<76D)uB5oD|bQS}376E=1AdwacmKFls
76RrL0p}J1>lOj<76I}W0rM6C_ZA8K76Ahn0SOlg4Hp9)7Xo7!BW@QXau*<c7Xf}334#{`kQWK07X#`S1N9dJ0~i4X7zqg&0~Z(x
D;NX$7y<hj0{j>Q02v?y836_v0S6f(2^j$k83GL%0}dG@5E&vE837y_AR`$AE*S$f83{QVAUhc$Mj0SX83~6OAc+|PiWvcz83CRd
1D_cIrx_rq86dzJ0n!;DB^m=f8UvRa0hk&BrWygL8VRf#1FaeXwi*Gt8VSQ11I`)(&>8{Z8VMg810x#{DH{+i8v!pH2{Ri5G#d~-
8v#KZ2}&CSRT~3W8v$q=31=Juu^b7(90}1J3DO)1?;Hs`9Uwm)5JepjM;#zY9Uw~`2~ZsnW*q}@9Uyug3C0~D+Z`YU9w12`0ZkqO
PaXkL9syP!0bU*fXC4969wOEr0oWb_+8zVj9w6NwBHtbZ;2s0!9s}tfAn+ao0UrqlA0Y@IArl`Ub07hEAOnLS0hJ&Doge|OAPMpy
0rwyv`5+(wAp-#+0SO^63L!8IArK-V0tF%g4k7~&A^{d60Wcx~Lm~;EA_2J~0Tv?x7$XTCBLONS2{|JPJ|hBABMGD<0jDDYts?=t
BLl}H0oNlSBqRYQBnc`c12ZHLG$ar<BoH_x2}~pdu_OaDB?&nt0X!uEK_wtUB_Kv62~Q;hRV4|(B?G`E0mvmF$t5AnB>~MP3DzY8
+$9O&B?99m0qP|Q^CckkB?&<$0YWALMkWJDCIL()0Z=9ZQYHavCIM|G0edD1$tDTgCJFB*16C&qTPF!!Ckb9B31BA)VkZf9CklHf
356#KaVZ0KDFb;a1AHk1eJKNyDFXm15CJL>11b;+DgzlR0UIg-D=Hw2DhZ$}1EeYe94sI&EeSp?39>B#%q;;qE&)3(0Zc9lQ!XJ|
E(u;PAi*vH%`OAdE&<psAmJ_vS}zG<F9Fgo2<9&X>MsFeFaz%}3G^@t12GAHG6S<U170^E;Wr>yI04-_34%KTmOLOVJ_+$acSW%f
oUF*s+zJ2=9TW&*V3LT4rH3q8N09{p000mG00>A7K!^bZT!8=*0001h05G`xO(3*`fQ5&N9RLUc00;p9$N<2L1Y}JB0000G0Du5J
VmJ*<F9`&YffWS=0R#~t@j!D$v5=go$cx+>01g}!2w`BBh=?VJC|L)Q1poj65C8xONDM%T0R&uu01^NI0Du56xcp5Zw1a?!gNY3Q
2mt^H0RYGVz>5TAO#lD@01yCx06k(j4NNZy1dxFh1q1;E5h3wFe?>45oUX_Z+zTKM859U%V3vr8C5I?k2ayFJ009sH00>A7K!^bZ
T!8=*0001h05G`xO(3*`fQ5&N9RLUc00;p9$N<2L1Y}JB0000G0Du53Vz`M6uZaPWffWP<0R#~x@j!P)u@IcB$j;mgAO;zf2w`B7
h=`?!ELlg91t0(b5C8xONDM%T0R&uu01^NI0Du56xcp5Zw1a?!hlw2k00Dpq0RYGVz>5TAO#lD@01yCx06k(j2@J0ZK#+kI1q1;E
5hd|Je?>45oUX_Z+zTKE8I%ZNV3vr8C5I?k2ayFJ009sH00>A7K!^bZT!8=*0001h05G`xO(3*`fQ5&N9RL6UfCvEq$N<2L1Y}JB
0000G0Du53Vz`M+FNsBvffWP<0R#~x@j!D$v5=go$cx+?APyK52w`BBh=?VJC|L)Q1t0(c5C8xONDM%T0R&uu01^NI0Du56xcp5Z
w1a?!gNY3Q2mt^H0RYGVz>5TAO#lD@01yCx06k(j2}~~u1dxFh1q1;E5hV*CJ|8_duJ89zhtX}wrQ4ZZVD==pwcjs{4o?#I?w>lO
iuYw$_0NR&=+7oSSg+0CZdH1T9iLe*6X=JG&uZx@2yu-SewQMZAwR}z<|wvb$PBJ~ASD^)I?*8b49Ouy54eWo)+4PJ
"""
# 8 stored survivors per set (17 bytes each, set-major), used only in planted trials.
SURVIVORS = """
k@xF3tT-y)X@qLethO_=bYgTZesOl-i4OoCSA6Xhjy~W5@|Iyeeb1ba$D4$sByLlSG1D`p<!DK)g)G8119NOwD6EOxp<m8JU8D@U
Sgl}G668Wy$4Gz1cuPyT%37@f{~)S3VX40-SF4vzUeu7(yyaWHW;Hlf`2=^}gbbBOn&1#9D#z?7Sbu@q+ey@8ieoK$Z-+()Al(rk
$kWTz2%wX()@V!rugw3$>=J+}BA$c!zCJMDF3`odXY#02uy*Olw`1!xdKlh*v%5$t?+*6#Zn0B?4ogk{uq4!iU1uZe`d8r|o)W*F
Q>xf*0uJT*<F4+WZAKXe%S5)iNoyhFR?SPT!IYhMD+azJl%P=OP@wn=$iOk{epL5*9<#4|wA;5<f{m<5WI7ffUr2ES8Ome*-ps~6
?d=6AMUvqx^X0pdW%E7>A~`NA@>>-PD*KXcm(Qkw<_$`#ESfW`baF6~WcX%pE_V#|4hKP@vYzLhytyBU%MG>~xh*V16n?u&>_+5R
Pa%rw{lnsHH(FWo8>x{zqgB=X)-Tx3FFY@5zts)|kM^&oyN3Wi_hcKK_vb-fh+hi^|CGZ(yT=JEp6zxg+>1%ab^l#0Mc?64>xH;#
;rIB<$jwdCGsqe^YrUN6et6*u8*PUm<P1&pj3iXWu~i?NPqg>vL7kUcS9@r&;i6aqL1#BmwTt06G9xp80Y8cf)m|F__U=sVbZBF8
JdK{DY(k=Ibp+=`_!=sonI_U3F|M6|-?~k2;hwfCc#|T`vMRZ(8JM6Jg#AL3j0#T(r#HkS;x37Q<{4~&*r$l20FFmPgWnSRt&_zj
IY(2V|1H7bJP#53r;Q#O>_3s_CsA;xnF?^w{|?jLWyb0a$Gf#!q*6nyMlJf=9G(-8q`-iqA;Pk8+>p)na5^;CL~6Oz_J8pdzgspL
^V#C%hy+>Mq2P0{I6TCSwe<yW_i;W}+4jCry#kccRH6GD>F85~Ov+cLXB#>$mXnD;z2nuOb)_Q8s{mWpSI^FJfb3WTuc3KKMyz_m
-SBvL<s+oZ>ZKY7T8exr
"""
KEYS = ("visits", "survivors", "records", "invalid", "column_draws", "planted", "rounds", "downset_points",
        "word_steps", "step_ops", "fes_mismatch", "radix_passes", "comparisons", "verify_calls",
        "record_mismatch", "prefix_calls")

PI = [0] * 25
for _y in range(5):
    for _x in range(5):
        PI[_x + 5 * _y] = _y + 5 * ((2 * _x + 3 * _y) % 5)
STEPS = [(i, i % 5, RHO[i], 64 - RHO[i], PI[i]) for i in range(25)]
CHI = [(i, i - i % 5 + (i + 1) % 5, i - i % 5 + (i + 2) % 5) for i in range(25)]


def keccak_round(A, rc):
    """One Keccak-f[1600] round (theta, rho, pi, chi, iota) on 25 little-endian 64-bit lanes."""
    C = [A[x] ^ A[x + 5] ^ A[x + 10] ^ A[x + 15] ^ A[x + 20] for x in range(5)]
    D = [C[x - 1] ^ (((C[(x + 1) % 5] << 1) | (C[(x + 1) % 5] >> 63)) & M64) for x in range(5)]
    B = [0] * 25
    for i, x, r, l, p in STEPS:
        v = A[i] ^ D[x]
        B[p] = ((v << r) | (v >> l)) & M64
    out = [B[i] ^ (~B[j] & B[k]) for i, j, k in CHI]
    out[0] ^= rc
    return out


def permute(A, first, last, c, key):
    for r in range(first, last):
        A = keccak_round(A, RC[r])
        c[key] += 1
    return A


def sha3_r5(message, c, key):
    """The complete target hash: SHA3-256 padding, prefix rounds 0..4 on every absorbed block."""
    data = bytearray(message) + b"\x06"
    data += bytes(-len(data) % 136)
    data[-1] |= 0x80
    A = [0] * 25
    for off in range(0, len(data), 136):
        block = struct.unpack("<17Q", bytes(data[off:off + 136]))
        A = [u ^ v for u, v in zip(A[:17], block)] + A[17:]
        A = permute(A, 0, 5, c, key)
    return struct.pack("<4Q", *A[:4])


def quotient_is(A, target):
    return all((v ^ (v >> 32)) & M32 == t for v, t in zip(A, target))


def spread(v):
    """800-bit value a (word j = high half of lane j) -> 1600-bit state with a_j in both halves."""
    return sum((((v >> (32 * j)) & M32) * 0x100000001) << (64 * j) for j in range(25))


def decode_chart():
    b = base64.b85decode("".join(CHART.split()))
    pos = 0

    def take(k):
        nonlocal pos
        pos += k
        return int.from_bytes(b[pos - k:pos], "little")
    U = [take(67) for _ in range(DIM)]
    R = [take(67) for _ in range(6)]
    BASE = [take(100) for _ in range(SETS)]
    Q = []
    for _ in range(take(2)):
        ij, m = take(2), take(1)
        Q.append((ij // DIM, ij % DIM, m))
    LIN = [[take(17) for _ in range(6)] for _ in range(SETS)]
    CON = [take(1) for _ in range(SETS)]
    Dv = take(100)
    assert pos == len(b)
    return U, R, BASE, Q, LIN, CON, Dv


U, R, BASE, Q, LIN, CON, DIFF = decode_chart()
US = [spread(v) for v in U]                       # free directions in state form
RS = [spread(v) for v in R]                       # correction directions in state form
DLO = sum(((DIFF >> (32 * j)) & M32) << (64 * j) for j in range(25))   # D in the low halves
# polar rows of the six correction quadratics: POLAR[k][l] = sum of e_i over pairs {i, l} in q_k
POLAR = [[0] * DIM for _ in range(6)]
for _i, _j, _m in Q:
    for _k in range(6):
        if (_m >> _k) & 1:
            POLAR[_k][_i] ^= 1 << _j
            POLAR[_k][_j] ^= 1 << _i
_sb = base64.b85decode("".join(SURVIVORS.split()))
PLANT = [[int.from_bytes(_sb[17 * (8 * p + t):17 * (8 * p + t) + 17], "little") for t in range(8)]
         for p in range(SETS)]


def corrections(p, y):
    """6-bit vector c_p(y): constants, linear parts and the shared quadratic part."""
    c = CON[p]
    for k in range(6):
        c ^= ((LIN[p][k] & y).bit_count() & 1) << k
    for i, j, m in Q:
        if (y >> i) & (y >> j) & 1:
            c ^= m
    return c


def point(p, y):
    """a_p(y) = base_p + U y + R c_p(y) (Lemma 2), in state form."""
    s, m = spread(BASE[p]), y
    while m:
        bit = m & -m
        s ^= US[bit.bit_length() - 1]
        m ^= bit
    c = corrections(p, y)
    for k in range(6):
        if (c >> k) & 1:
            s ^= RS[k]
    return s


class Walk:
    """Visits y_i = A Gray(i) + b of one set in Gray order (Lemma 4): one free-direction XOR, six derivative
    parities and at most six correction-direction XORs per step.  Used for the direct filter."""

    def __init__(self, p, cols, b):
        self.p, self.cols, self.y, self.i, self.tab = p, cols, b, 0, {}
        self.s = point(p, b)
        self.c0 = CON[p]

    def prepare(self, bit):
        v = self.cols[bit]
        fu, masks, m = 0, [0] * 6, v
        while m:
            low = m & -m
            l = low.bit_length() - 1
            fu ^= US[l]
            for k in range(6):
                masks[k] ^= POLAR[k][l]
            m ^= low
        t = (fu, masks, corrections(self.p, v) ^ self.c0)
        self.tab[bit] = t
        return t

    def next(self):
        if self.i:
            bit = (self.i & -self.i).bit_length() - 1
            fu, masks, k6 = self.tab.get(bit) or self.prepare(bit)
            self.s ^= fu
            for k in range(6):
                if ((masks[k] & self.y).bit_count() ^ (k6 >> k)) & 1:
                    self.s ^= RS[k]
            self.y ^= self.cols[bit]
        self.i += 1
        return self.s


def invertible_columns(rng, c):
    """Uniform invertible matrix: column k is drawn uniformly until it leaves the span of columns 0..k-1,
    at most MATRIX_CAP draws per column (Lemma 9); None if a cap is reached."""
    pivots, cols = {}, []
    for _ in range(DIM):
        for _ in range(MATRIX_CAP):
            c["column_draws"] += 1
            col = v = rng.getrandbits(DIM)
            while v and v.bit_length() - 1 in pivots:
                v ^= pivots[v.bit_length() - 1]
            if v:
                pivots[v.bit_length() - 1] = v
                cols.append(col)
                break
        else:
            return None
    return cols


def radix_sort(records, c):
    """Stable LSD byte radix on digest bytes 31..0, two arrays of 176-byte records."""
    n, w = len(records), 176
    if n < 2:
        return records
    a, b = bytearray(b"".join(records)), bytearray(n * w)
    for d in range(31, -1, -1):
        c["radix_passes"] += 1
        count = [0] * 256
        for i in range(n):
            count[a[w * i + d]] += 1
        start, run = [], 0
        for v in count:
            start.append(run)
            run += v
        for i in range(n):
            key = a[w * i + d]
            dst = w * start[key]
            start[key] += 1
            b[dst:dst + w] = a[w * i:w * i + w]
        a, b = b, a
    return [bytes(a[w * i:w * i + w]) for i in range(n)]


# ---- quotient algebra (Section 2) and the filter planes (Lemma 4a) ----

def rot32(w, r):
    r %= 32
    return ((w << r) | (w >> (32 - r))) & M32 if r else w


def lin32(W):
    """Theta, rho and pi on 25 words of 32 bits: the linear layer acting on quotients."""
    C = [W[x] ^ W[x + 5] ^ W[x + 10] ^ W[x + 15] ^ W[x + 20] for x in range(5)]
    Dd = [C[x - 1] ^ rot32(C[(x + 1) % 5], 1) for x in range(5)]
    B = [0] * 25
    for i, x, r, l, p in STEPS:
        B[p] = rot32(W[i] ^ Dd[x], r)
    return B


def words(v):
    return [(v >> (32 * j)) & M32 for j in range(25)]


def quo(A):
    return [(v ^ (v >> 32)) & M32 for v in A]


def native(a, rounds):
    """Lanes after rounds 0..rounds-1 of X(a), a an 800-bit value."""
    A = list(struct.unpack("<25Q", (spread(a) ^ DLO).to_bytes(200, "little")))
    for r in range(rounds):
        A = keccak_round(A, RC[r])
    return A


def filter_planes():
    """Lemma 4a.  On the chart the third chi gets the quotient E2 = L(T2); bit z of output word i is
    chi(E2)_i + iota (a constant) + x_j E2_k + E2_j x_k at bit z (x: low halves entering that chi).  Every bit
    that does not depend on x must equal T3; the others are the planes (identical bits merged)."""
    e = lin32(list(T2))
    cst = [e[i] ^ (~e[j] & e[k] & M32) for i, j, k in CHI]
    cst[0] ^= (RC[2] ^ (RC[2] >> 32)) & M32
    planes, seen, varying = [], {}, 0
    for i, j, k in CHI:
        for z in range(32):
            dep = frozenset(d for d, f in (((j, z), e[k]), ((k, z), e[j])) if f >> z & 1)
            want = T3[i] >> z & 1
            if not dep:
                assert (cst[i] >> z & 1) == want, "a constant bit of the third-chi quotient differs from T3"
                continue
            varying += 1
            key = (dep, cst[i] >> z & 1)
            if key in seen:
                assert seen[key] == want                   # an identical bit asks for the same value
                continue
            seen[key] = want
            planes.append((i, z, want))
    assert varying == 19 and [32 * i + z for i, z, t in planes] == [
        103, 111, 127, 135, 143, 159, 163, 170, 202, 291, 385, 417, 449, 483, 490, 522, 586, 611]   # 618 = 490
    return planes


PLANES = filter_planes()
NPL = len(PLANES)


def evaluate(s):
    """Direct filter at the chart point with state s = spread(a): (planes XOR their T3 bits, first two chi
    conditions hold, quotient after rounds 0..2 equals T3)."""
    A = keccak_round(list(struct.unpack("<25Q", (s ^ DLO).to_bytes(200, "little"))), RC[0])
    ok = quotient_is(A, T1)
    A = keccak_round(A, RC[1])
    ok = ok and quotient_is(A, T2)
    A = keccak_round(A, RC[2])
    bits = 0
    for h, (i, z, t) in enumerate(PLANES):
        bits |= ((((A[i] ^ (A[i] >> 32)) >> z) ^ t) & 1) << h
    return bits, ok, quotient_is(A, T3)


def chart_certificate():
    """Lemma 3, both chi conditions on every chart point, for each set p.  S_p = {B_p + U y + R t}.
    (i) The round-0 quotient is affine in a (the input quotient is D): it equals T1 at B_p and at B_p plus
    each of the 141 directions, hence on all of S_p.  (ii) Then the second chi gets the quotient e1 = L(T1),
    and the round-1 quotient is chi(e1) + L_e1(x) + iota with x = L(low halves after round 0): quadratic on
    S_p, with constant alpha (at B_p), linear coefficients lambda_v (unit points) and quadratic coefficients
    L_e1(L(chipolar(L(d_u), L(d_v)))).  Substituting t = c_p(y): the constant must be T2, every linear and
    quadratic coefficient must vanish, and no coefficient may involve t beyond its linear term."""
    dirs = U + R
    nv = len(dirs)
    ones = sum(1 << (32 * v) for v in range(nv))
    hi = [0] + [ones * ((M32 << r) & M32) for r in range(1, 32)]
    lo = [0] + [ones * (M32 >> (32 - r)) for r in range(1, 32)]

    def rot(X, r):
        r %= 32
        return ((X << r) & hi[r]) | ((X >> (32 - r)) & lo[r]) if r else X
    M = [lin32(words(d)) for d in dirs]              # differences entering the first chi (low halves)
    pack = [sum(M[v][j] << (32 * v) for v in range(nv)) for j in range(25)]
    e1 = [ones * w for w in lin32(list(T1))]
    for p in range(SETS):
        A0 = native(BASE[p], 1)
        assert quo(A0) == list(T1)
        f0 = quo(keccak_round(A0, RC[1]))
        lam = []
        for d in dirs:
            A = native(BASE[p] ^ d, 1)
            assert quo(A) == list(T1)
            lam.append([u ^ v for u, v in zip(quo(keccak_round(A, RC[1])), f0)])
        mu = lam[DIM:]
        acc = list(f0)
        for k in range(6):
            if CON[p] >> k & 1:
                acc = [u ^ v for u, v in zip(acc, mu[k])]
        assert acc == list(T2)
        for u in range(DIM):
            acc = list(lam[u])
            for k in range(6):
                if LIN[p][k] >> u & 1:
                    acc = [a ^ b for a, b in zip(acc, mu[k])]
            assert not any(acc)
        want = [[0] * 25 for _ in range(nv)]
        for i, j, m in Q:
            w = [0] * 25
            for k in range(6):
                if m >> k & 1:
                    w = [a ^ b for a, b in zip(w, mu[k])]
            for g in range(25):
                want[i][g] ^= w[g] << (32 * j)
                want[j][g] ^= w[g] << (32 * i)
        for u in range(nv):
            Mu = M[u]
            P = [((Mu[j] * ones) & pack[k]) ^ (pack[j] & (Mu[k] * ones)) for i, j, k in CHI]
            C = [P[x] ^ P[x + 5] ^ P[x + 10] ^ P[x + 15] ^ P[x + 20] for x in range(5)]
            Dd = [C[x - 1] ^ rot(C[(x + 1) % 5], 1) for x in range(5)]
            B = [0] * 25
            for i, x, r, l, q in STEPS:
                B[q] = rot(P[i] ^ Dd[x], r)
            assert [(B[j] & e1[k]) ^ (e1[j] & B[k]) for i, j, k in CHI] == want[u]


# ---- the finite-difference visit (Lemma 4b, Section 5 step 3) ----

class Layout:
    """Row addresses of the derivative tables: walk bits m, 2^lane_bits lanes, low split of `low` bits.
    Row of a set S of walk coordinates: off[|S|] + sum of C(s_l, l) over its elements s_1 < s_2 < ...;
    the coordinates m..m+VIRT-1 are virtual (the walk value never depends on them: their rows stay zero)."""

    def __init__(self, m, lane_bits, low):
        self.m, self.lanes, self.low = m, 1 << lane_bits, low
        self.lanemask, self.lowmask = (1 << self.lanes) - 1, (1 << low) - 1
        self.virt = ((1 << VIRT) - 1) << m            # k* = k + virt has at least DEG set bits when k >= 1
        self.off = [0]
        for j in range(DEG + 1):
            self.off.append(self.off[-1] + comb(m + VIRT, j))
        self.lowrow, self.lowq = [], []
        for w in range(1 << low):
            bits = [s for s in range(low) if w >> s & 1][:DEG]
            acc, row = 0, []
            for j in range(1, DEG + 1):
                if j <= len(bits):
                    acc += comb(bits[j - 1], j)
                row.append(self.off[j] + acc)
            self.lowrow.append(row)
            self.lowq.append(len(bits))
        self.high = [[0] * DEG for _ in range(DEG + 1)]

    def row(self, S):
        r, l = self.off[bin(S).count("1")], 0
        while S:
            low = S & -S
            l += 1
            r += comb(low.bit_length() - 1, l)
            S ^= low
        return r

    def recompute(self, H):
        """High rows for the 2^low steps that share H = k* >> low; returns its operation count (<= 2^10)."""
        ops, hb, pos = 1, [], 0
        while len(hb) < DEG and H >> pos:
            ops += 4
            if H >> pos & 1:
                hb.append(pos)
                ops += 3
            pos += 1
        for q in range(DEG):
            acc = 0
            for j in range(q + 1, min(DEG, q + len(hb)) + 1):
                acc += comb(self.low + hb[j - q - 1], j)
                self.high[q][j - 1] = acc
                ops += 6
        assert ops <= 1024
        return ops

    def chain(self, ks):
        """Rows of the sets of the lowest 1..DEG set bits of k* (from the low and high tables)."""
        w = ks & self.lowmask
        lo, hi = self.lowrow[w], self.high[self.lowq[w]]
        return [lo[j] + hi[j] for j in range(DEG)]


def step_ops(nsets):
    """Operations of one word step for nsets sets (proof.md 7.3): 49 shared, per set 3 + 35 per plane."""
    return 49 + nsets * (3 + NPL * (4 * DEG + 3))


assert step_ops(SETS) + 1 <= SETS * CHARGE           # 3847 + 1 (high rows, amortised) <= 6 x 675


def fes_init(lay, value):
    """Tables of one set from the direct filter on the down-set: value[z] = the planes' lane words at walk
    point z, wt(z) <= DEG.  The Moebius transform on the down-set gives the coefficients of degree <= DEG;
    TAB[S] = XOR of COEF[S + W] over W inside (S >> 1) & ~S with |S| + |W| <= DEG; F = COEF[0]."""
    coef = {z: list(v) for z, v in value.items()}
    for t in range(lay.m):
        bit = 1 << t
        for z, v in coef.items():
            if z & bit:
                for h, u in enumerate(coef[z ^ bit]):
                    v[h] ^= u
    tab = {}
    for S, v0 in coef.items():
        if not S:
            continue
        size, free = bin(S).count("1"), (S >> 1) & ~S
        v, W = list(v0), free
        while W:
            if size + bin(W).count("1") <= DEG:
                for h, u in enumerate(coef[S | W]):
                    v[h] ^= u
            W = (W - 1) & free
        tab[lay.row(S)] = v
    return tab, list(coef[0])


def fes_step(k, lay, sets, c):
    """Word step k >= 1 of every set in `sets` (pairs of tables and F words), with the operations of
    proof.md 7.3 counted and asserted; returns the survivor lane masks."""
    ks = k + lay.virt
    ops = 6                                    # k* += 1, compare, branch; w = k* AND mask; w == 0, branch
    if not ks & lay.lowmask:
        c["step_ops"] += lay.recompute(ks >> lay.low)
    rows = lay.chain(ks)
    ops += 3 + 5 * DEG                         # low row address, load of the high row; per level 2 adds,
    masks = []                                 # 2 loads, 1 add
    for tab, F in sets:
        chain = [tab.get(r) for r in rows]     # None: a virtual row (zero)
        acc = 0
        ops += 1                               # clear the accumulator
        for h in range(NPL):
            r = chain[DEG - 1]
            v = r[h] if r else 0
            ops += 2                           # deepest level: address add, load
            for j in range(DEG - 2, -1, -1):
                r = chain[j]
                if r:
                    v ^= r[h]
                    r[h] = v
                else:
                    assert not v
                ops += 4                       # address add, load, XOR, store
            v ^= F[h]
            F[h] = v
            acc |= v
            ops += 5                           # F: address add, load, XOR, store; OR into the accumulator
        ops += 2                               # survivor test: compare with all ones, branch
        masks.append(lay.lanemask & ~acc)
    assert ops == step_ops(len(sets))
    c["step_ops"] += ops
    c["word_steps"] += len(sets)
    return masks


def selftest():
    """Start-up comparison at the production degree bound: set 0, one lane, 2^SELF_BITS visits; the tables
    use only the visits of Gray weight <= DEG; every visit's planes must equal the direct filter, and every
    chain row must equal the colex row of the lowest set bits of k*."""
    lay = Layout(SELF_BITS, 0, SELF_LOW)
    rng = random.Random(4242)
    c = dict.fromkeys(KEYS, 0)
    cols = invertible_columns(rng, c)
    walk = Walk(0, cols, rng.getrandbits(DIM))
    ref, value = [], {}
    for i in range(1 << SELF_BITS):
        bits, ok, surv = evaluate(walk.next())
        assert ok and surv == (bits == 0)
        ref.append(bits)
        z = i ^ (i >> 1)
        if bin(z).count("1") <= DEG:
            value[z] = [bits >> h & 1 for h in range(NPL)]
    tab, F = fes_init(lay, value)
    lay.recompute(lay.virt >> lay.low)
    for k in range(1, 1 << SELF_BITS):
        fes_step(k, lay, [(tab, F)], c)
        assert sum((F[h] & 1) << h for h in range(NPL)) == ref[k]
        x, prefix, rows = k + lay.virt, 0, []
        for _ in range(DEG):
            low = x & -x
            prefix |= low
            x ^= low
            rows.append(lay.row(prefix))
        assert rows == lay.chain(k + lay.virt)
    return len(value)


def setup():
    """First-block replay (one five-round call), the chart checks of Lemmas 1 and 2, the certificate of
    Lemma 3 and the start-up comparison of Lemma 4b."""
    c = dict.fromkeys(KEYS, 0)
    first = list(struct.unpack("<17Q", PREFIX_INDEX.to_bytes(8, "little") + bytes(128))) + [0] * 8
    N = struct.pack("<25Q", *permute(first, 0, 5, c, "prefix_calls"))
    for p in range(SETS):
        block = bytes(u ^ v for u, v in zip((spread(BASE[p]) ^ DLO).to_bytes(200, "little"), N))
        assert block[136:] == bytes(64) and block[135] == 0x86 and block[131] == 0x86
    pivots = {}
    for v in U + R:
        while v and v.bit_length() - 1 in pivots:
            v ^= pivots[v.bit_length() - 1]
        assert v
        pivots[v.bit_length() - 1] = v
    for p in range(SETS):
        for q in range(p + 1, SETS):
            v = BASE[p] ^ BASE[q]
            while v and v.bit_length() - 1 in pivots:
                v ^= pivots[v.bit_length() - 1]
            assert v
    chart_certificate()
    selftest()
    return N, c["prefix_calls"] // 5


def trial(index, seed, N, M0, lay):
    rng = random.Random(int(seed, 16))
    c = dict.fromkeys(KEYS, 0)
    coins = []
    for p in range(SETS):
        cols = invertible_columns(rng, c)
        if cols is None:
            return None, c, []                       # setup cap reached: the campaign fails
        b = rng.getrandbits(DIM)
        if index % PLANT_EVERY == 0:
            b = PLANT[p][(index // PLANT_EVERY) % 8]
            c["planted"] += 1
        coins.append((cols, b))
    lanes, flip, blocks = lay.lanes, lay.lanes - 1, 1 << WALK_BITS
    sets, ref = [], []
    for p, (cols, b) in enumerate(coins):           # tables from the direct filter on the down-set, which
        walk, value, rp = Walk(p, cols, b), {}, []   # at this width holds every visit
        for i in range(lanes * blocks):
            bits, ok, surv = evaluate(walk.next())
            c["rounds"] += 3
            c["downset_points"] += 1
            c["invalid"] += not ok
            k, cp = divmod(i, lanes)
            lane = cp ^ (flip if k & 1 else 0)
            v = value.setdefault(k ^ (k >> 1), [0] * NPL)
            for h in range(NPL):
                v[h] |= (bits >> h & 1) << lane
            rp.append((bits, surv))
        sets.append(fes_init(lay, value))
        ref.append(rp)
    lay.recompute(lay.virt >> lay.low)
    records = []
    for k in range(blocks):
        if k:
            masks = fes_step(k, lay, sets, c)
        else:
            masks = []
            for tab, F in sets:
                acc = 0
                for v in F:
                    acc |= v
                masks.append(lay.lanemask & ~acc)
        odd = flip if k & 1 else 0
        for p, (tab, F) in enumerate(sets):         # check beside the algorithm: every visit of the block
            for cp in range(lanes):
                lane = cp ^ odd
                bits, surv = ref[p][lanes * k + cp]
                got = sum((F[h] >> lane & 1) << h for h in range(NPL))
                c["fes_mismatch"] += got != bits or (masks[p] >> lane & 1) != surv
                c["visits"] += lanes * k + cp < L_RED
        for cp in range(lanes):                      # survivors in the scalar order: i = lanes k + c', then p
            i = lanes * k + cp
            for p in range(SETS):
                if i >= L_RED or not masks[p] >> (cp ^ odd) & 1:
                    continue
                cols, b = coins[p]
                g, y = i ^ (i >> 1), b
                while g:
                    low = g & -g
                    y ^= cols[low.bit_length() - 1]
                    g ^= low
                X = (point(p, y) ^ DLO).to_bytes(200, "little")
                A = permute(list(struct.unpack("<25Q", X)), 0, 1, c, "rounds")
                ok = quotient_is(A, T1)
                A = permute(A, 1, 2, c, "rounds")
                ok = ok and quotient_is(A, T2)
                A = permute(A, 2, 3, c, "rounds")
                if not (ok and quotient_is(A, T3)):
                    continue                         # not reached: counted by the check above
                A = permute(A, 3, 5, c, "rounds")
                c["survivors"] += 1
                fragment = bytes(u ^ v for u, v in zip(X[:135], N[:135]))
                records.append(struct.pack("<4Q", *A[:4]) + fragment + bytes(9))
                if len(records) == N_RED:
                    break
            if len(records) == N_RED:
                break
        if len(records) == N_RED:
            break
    c["records"] = len(records)
    pair = None
    ordered = radix_sort(records, c)
    for r1, r2 in zip(ordered, ordered[1:]):
        c["comparisons"] += 1
        if r1[:32] == r2[:32]:
            m1, m2 = M0 + r1[32:167], M0 + r2[32:167]
            if m1 != m2 and sha3_r5(m1, c, "verify_calls") == sha3_r5(m2, c, "verify_calls"):
                pair = (m1, m2)
                break
    check = dict.fromkeys(KEYS, 0)
    for r in records:
        c["record_mismatch"] += sha3_r5(M0 + r[32:167], check, "rounds") != r[:32]
    c["verify_calls"] //= 5                           # rounds -> five-round calls
    return pair, c, records


def main():
    request = json.loads(sys.stdin.read())
    N, calls = setup()
    M0 = PREFIX_INDEX.to_bytes(8, "little") + bytes(128)
    lay = Layout(WALK_BITS, LANE_BITS, LOW_BITS)
    out = []
    for t in request["trials"]:
        pair, c, _ = trial(t["trial"], t["seed"], N, M0, lay)
        c["prefix_calls"] = calls if t["trial"] == 0 else 0    # the one replay, reported once
        row = {"trial": t["trial"], "message_a_hex": None, "message_b_hex": None}
        if pair:
            row["message_a_hex"], row["message_b_hex"] = pair[0].hex(), pair[1].hex()
        row["observations"] = {k: c[k] for k in KEYS}
        out.append(row)
    sys.stdout.write(json.dumps({"schema_version": 1, "trials": out}, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()
