# A sub-class search with a beta pre-filter for 2-round BLAKE3

`time_log2` under `collision-frontier-v5`; memory is reported separately.
Target: blake3-r2-prefix-v1, ordinary collision of a 60-byte and a 62-byte
message. Claim: **time_log2 = 108.9** (computed 108.8668), success 0.39 under
the heuristics H1 and H2 of Section 6.

**Credit.** This package is a derivative of submission 04638ed8 by
**Jbenisek** (co-author **tekkac**). From it come the free half-collision
(Sections 2, 3.1), the class of Y4 (3.2), the D0 family, Lemma E, the
trial structure and the shape of the packed batch. The seven-lane layout
with delayed reduction and the five-operation masked rotation are from public
ticket 2bf40fb (tekkac). Both are co-authors here. None of their work is
presented as ours, and none of it is promoted.

**What is new here.**
1. A sub-class S of 256 class members. Under the leader's seven-word model
   M, its rate for two values of an auxiliary difference beta is at least
   **20,172.0** times uniform: an exact sum with no sampling error (Sec. 7).
2. An exact **beta pre-filter** (Lemma B): a 10-bit test on one E1 word that
   every trial counted in that bound passes and 2^-10 of all trials pass.
3. **Lanes hold seven values of alpha**, so the per-alpha set-up is shared
   by 256 straight-line batches (one per member, read at a fixed address).
4. An exact ledger under faithful counting (every primitive and load, 64
   registers), executed by the shipped program and checked lane by lane:
   **15.18 operations per trial**; 15.30 with the continuation cap and
   15.32 with all caps.
5. An organizer-executed reduced-width test of model M on the algorithm's
   own filtered trials, where M predicts 8.7 times the uniform rate (Sec. 9).

H1 assumes a rate factor **f = 10,240**: the bound 20,172 divided by 1.97.
With the uniform rate instead, the same algorithm gives 122.2 (Section 10).
No full collision is exhibited.

## 1. Target and notation

H is unkeyed BLAKE3-256 with rounds 0 and 1 kept. Every message used has
n = 60 or 62 bytes. It is therefore one chunk with one block and one root
compression, with flags 11 (CHUNK_START|CHUNK_END|ROOT), block length n and
counter 0. The block is the message padded with zero bytes, read as
little-endian words w0..w15. v[0..7] = IV, v[8..11] = IV[0..3] and
v[12..15] = (0, 0, n, 11). G(a,b,c,d,x,y) is

    a1=A+B+x  d1=ROR(D^a1,16)  c1=C+d1  b1=ROR(B^c1,12)
    a2=a1+b1+y d2=ROR(d1^a2,8) c2=c1+d2 b2=ROR(b1^c2,7)

with outputs (a2,b2,c2,d2), all arithmetic modulo 2^32. The calls are named

    round 0  K0=G(0,4,8,12;w0,w1)  K1=G(1,5,9,13;w2,w3)  K2=G(2,6,10,14;w4,w5)
             K3=G(3,7,11,15;w6,w7) D0=G(0,5,10,15;w8,w9) D1=G(1,6,11,12;w10,w11)
             D2=G(2,7,8,13;w12,w13) D3=G(3,4,9,14;w14,w15)
    round 1  C0=G(0,4,8,12;w2,w6)  C1=G(1,5,9,13;w3,w10) C2=G(2,6,10,14;w7,w0)
             C3=G(3,7,11,15;w4,w13) E0=G(0,5,10,15;w1,w11) E1=G(1,6,11,12;w12,w5)
             E2=G(2,7,8,13;w9,w14)  E3=G(3,4,9,14;w15,w8)

The round-1 schedule is the standard permutation P = (2,6,3,10,7,0,4,13,1,11,12,5,9,14,15,8).
S is the state after K0..K3, X the state after round 0, Y the state after
C0..C3 and Z the final state. The digest words are o[i] = Z[i] XOR Z[i+8] for
i = 0..7. dOi denotes o[i](A) XOR o[i](B). This is the complete hash of the
profile on these inputs: standard IV, flags, true lengths, standard
permutation and feed-forward, and the full 256-bit digest.

**Fact 1 (inverting G).** From the outputs one gets backwards
b1 = ROL(b2,7)^c2, c1 = c2-d2, d1 = ROL(d2,8)^a2, B = ROL(b1,12)^c1,
C = c1-d1 and a1 = ROL(d1,16)^D. The words follow as y = a2-a1-b1 and
x = a1-A-B. Each line solves one assignment for one of its terms.

## 2. Exact part I: the half-collision (Jbenisek, 04638ed8)

**Lemma L.** Put K = IV[2]+IV[6], w4' = ((K+w4)^2)-K and w5' = w5+w4-w4'.
Then K2 with length 60 and words (w4,w5) gives the same outputs as K2 with
length 62 and (w4',w5').
*Proof.* K+w4' = (K+w4)^2. So d1 = ROR(62^(K+w4)^2,16) = ROR(60^(K+w4),16),
c1 and b1 agree, and (a1^2)+b1+w5' = a1+b1+w5 because w5'-w5 =
a1-(a1^2). The last three assignments use only equal values. QED.
K2 is the only round-0 call that reads v[14] = n, w4 or w5. So two such
messages, equal in every other word, have equal S and X.

**Fact P (pinned C3).** Fix X3=a6c3b8c5, X7=793c473a, X11=5c32535c,
X15=8367c7bb, W4=60000001, W13=29bd3f58; then W4'=5fffffff. C3 on
(X3,X7,X11,X15) with w4 = W4 or W4' gives a outputs Y3=c952ec69,
Y3'=36ac1396, b output 465cd3db (both), c outputs Y11=31fc40b2,
Y11'=a28739e3 and d output 0e0ee9ef (both). This is a finite computation.

**Lemma H.** Two executions with equal X, equal words except w4,w5,
(X3,X7,X11,X15) as in Fact P, w13 = W13, and w4 = W4 resp. W4' agree on
digest words 0, 2, 5 and 7.
*Proof.* C0, C1, C2 read neither w4 nor w5, so their outputs are equal. C3
changes only Y3 and Y11 (Fact P). E0 reads Y0,Y5,Y10,Y15,w1,w11, and E2 reads
Y2,Y7,Y8,Y13,w9,w14, so Z0,Z5,Z10,Z15,Z2,Z7,Z8,Z13 are equal. Then
o0=Z0^Z8, o2=Z2^Z10, o5=Z5^Z13 and o7=Z7^Z15 are equal. QED.

**Step S1** (nine free words X1,X2,X5,X6,X9,X10,X12,X13,X14 → context).
Set X3,X7,X11,X15,w4=W4,w13=W13 and w15=0, then compute in order:

    p=K+W4; q=ROR(p^60,16); r=q+IV[2]; u=ROR(r^IV[6],12)
    bD1=ROL(X6,7)^X11; c=X11-X12; dD1=ROL(X12,8)^X1; S6=ROL(bD1,12)^c; S11=c-dD1
    S10=u^ROL(S6,7); b=ROL(X5,7)^X10; c=X10-X15; S5=ROL(b,12)^c
    dD0=c-S10; X0=dD0^ROL(X15,8); bD0=b
    S14=S10-r; S2=ROL(S14,8)^q; w5=S2-p-u
    d=ROL(X14,8)^X3; aD3=ROL(d,16)^S14; b=X3-aD3; X4=ROR(b^X9,7)
    c=X9-X14; S4=ROL(b,12)^c; S9=c-d
    (S1,S13,w2,w3)=COL(1,S5,S9,0)
    d=ROL(X13,8)^X2; a=ROL(d,16)^S13; b=X2-a-W13; X8=b^ROL(X7,7)
    c=X8-X13; S7=ROL(b,12)^c; S8=c-d; w12=a-S2-S7
    (S0,S12,w0,w1)=COL(0,S4,S8,0); (S3,S15,w6,w7)=COL(3,S7,S11,11)
    a=ROL(dD0,16)^S15; w8=a-S0-S5; w9=X0-a-bD0
    a=ROL(dD1,16)^S12; w10=a-S1-S6; w11=X1-a-bD1; w14=aD3-S3-S4

COL(j,sb,sc,d0) applies Fact 1 to column call Kj, whose inputs are
(IV[j],IV[4+j],IV[j],d0): b1=ROL(sb,7)^sc, c1=ROL(b1,12)^IV[4+j],
sd=sc-c1, d1=c1-IV[j], a1=ROL(d1,16)^d0, x=a1-IV[j]-IV[4+j],
sa=ROL(sd,8)^d1 and y=sa-a1-b1; it returns (sa,sd,x,y).
**Step S2/S3.** w4'=W4' and w5'=w5+W4-W4'. A is the first 60 bytes of
w0..w15. B is the first 62 bytes with w4 and w5 replaced.

**Lemma S.** For every nine words, round 0 with length 60 on these words
gives the S and X of step S1. *Proof.* Fact 1 call by call. D1, D0, D3 and
D2 have the prescribed outputs; X0, X4 and X8 are chosen so that the c
input of D0, the second word of D3 (w15=0) and the second word of D2 (W13)
come out right. The link line S10=u^ROL(S6,7) and the K2 lines make K2 with
first word W4 output (S2,S6,S10,S14). COL handles K1, K0 and K3. Every
quantity is defined before it is used. QED.

**Theorem.** For all 2^288 choices, A (60 bytes) and B (62 bytes, ending in
two zero bytes since w15 = 0) are distinct and agree on digest words
0, 2, 5 and 7. *Proof.* By Lemma S, Lemma L and Lemma H. QED.

The residual R = (dO1, dO3, dO4, dO6) depends only on E1 and E3:
o1 = E1.a ^ E3.c, o3 = E3.a ^ E1.c, o4 = E3.b ^ E1.d and o6 = E1.b ^ E3.d.
A pair is a collision iff R = 0.

## 3. Exact part II: trials, class, sub-class, filter

### 3.1 Trials (Jbenisek, 04638ed8)

A context is the output of step S1. A **trial** is (context, alpha, y). It
replaces w6..w11 and w14, executing in order:

    D0 family:   c=alpha-X15; dD0=c-S10; X0=ROL(X15,8)^dD0
                 bD0=ROR(S5^c,12); X5=ROR(bD0^alpha,7); X10=alpha
    C0 backwards: pa=X0+X4+w2; pd=ROR(X12^pa,16); pc=X8+pd; pb=ROR(X4^pc,12)
                 Y8=ROL(y,7)^pb; Y12=Y8-pc; Y0=ROL(Y12,8)^pd; w6=Y0-pa-pb
    K3, S7 kept: ka=IV3+IV7+w6; kd=ROR(ka^11,16); kc=IV3+kd; kb=ROR(IV7^kc,12)
                 S11=ROL(S7,7)^kb; S15=S11-kc; S3=ROL(S15,8)^kd; w7=S3-ka-kb
    D1, D0, D3:  d=(X11-X12)-S11; X1=ROL(X12,8)^d
                 a=ROL(d,16)^S12; w10=a-S1-S6; w11=X1-a-bD1
                 a=ROL(dD0,16)^S15; w8=a-S0-S5; w9=X0-a-bD0; w14=aD3-S3-S4

**Lemma T.** For every trial, round 0 (length 60) maps the trial's words to
the context's states with S3, S11, S15, X0, X1, X5 and X10 replaced as
assigned. The four pinned X words and w4, w13, w15 are unchanged, C0 has b
output Y4 = y, and A, B agree on digest words 0, 2, 5, 7.
*Proof* (04638ed8, Lemmas K, F, Y). K0..K2 and D2 are unchanged. K3's
last four assignments give S3, S15 (by the definition of S3), S11 and S7
(by the definition of S11). D0's eight assignments give a, dD0, c, bD0, X0,
X15 (by the definition of X0), alpha and X5, for every S15. D1's give a, d,
X11-X12, bD1, X1, X12 (by the definition of X1), X11 and X6. D3 reads S3
only in its first assignment, which gives aD3 again. C0's fifth to eighth
assignments give Y0, Y12, Y8 and y (by the definitions of Y0 and Y8).
The proof of the Theorem uses only w15 = 0, the pinned X words and w4, w13,
so it applies. QED. (This is 04638ed8's Lemma T.)

Trials are distinct. Contexts differ in (X12,X13,X14), which no trial
changes; trials of a context with different alpha differ in X10; trials
with different y differ in Y4.

### 3.2 The class (Lemma Q, 04638ed8)

Name E3's assignments e1, h1, g1, f1, e2, h2, g2, f2 (in the order a, d, c,
b of G); a prime marks message B. E3's first word is w15 = 0, so
e1 = Y3+Y4 and e1' = Y3'+Y4. Then
eta = h1^h1' = ROR(e1^(e1+DY3),16) depends on Y4 only, with
DY3 = Y3'-Y3 = 6d59272d. The class is {Y4 : eta = e96d6d6b}.
**Lemma Q.** Y4 is in the class iff ((Y3+Y4) AND 6d6be96d) = 00096120:
4,096 members, with 12 free bits of e1. *Proof.* With x = ROL(eta,16) =
6d6be96d: e1^(e1+DY3) = x ⟺ (e1^x)-e1 = DY3 ⟺ 2((~e1)&x)-x = DY3
⟺ 2((~e1)&x) = dac5109a (mod 2^32). x has no bit 31, so this is
(~e1)&x = 6d62884d, i.e. e1&x = 00096120. QED. We checked it over all 2^32
values of Y4: exactly the 4,096 members give eta.

### 3.3 The sub-class S (new)

**S** is the set of the 256 class members whose e1 = Y3+Y4 has
(e1 AND 00101092) = 00000010 or 00000082. These are bits 1, 4, 7, 12, 20
read in that order as 01000 or 10100; the five bits are free bits of the
class. Members are listed in increasing order of class member number (the
12 free bits of e1 in increasing position). Two lists hold, for j < 256,
U[j] = ROL(y_j,7) and V[j] = Y3+y_j, each broadcast into all seven lanes.
S was chosen by the exact computation of Section 7 (the best 2 of 32
patterns, 7.2). Its cost is charged in Section 8.

### 3.4 Lemma E and its digest form

Write a2, a2' for E1's fifth assignment on A, B, t = a2^a2', and f1, f1'
for E3's fourth assignment. The **test word** is
EW = (f1^f1') ^ t ^ ROR(t,1).
**Lemma D** (an identity from the substitutions in 04638ed8's proof of
Lemma E, stated here for every trial). For every trial, EW = dO1 ^ ROL(dO4,7).
*Proof.* E1's inputs Y1, Y6, Y12 and first word w12 are the same for A and B,
so d1 is equal and d2^d2' = ROR(t,8). In E3, f2^f2' = ROR((f1^f1')^(g2^g2'),7).
dO1 = t ^ (g2^g2') and dO4 = (f2^f2') ^ (d2^d2'). Substituting
g2^g2' = t^dO1 gives dO4 = ROR(EW^dO1,7). QED.
**Lemma E (04638ed8).** If R = 0 then EW = 0. (Immediate from Lemma D.)
For Y4 in the class, h1' = h1^eta, and f1^f1' = ROR(g1^g1',12) since both
read the same Y4. The batch uses these two shortcuts.

### 3.5 The beta pre-filter (new)

c1 = Y11+d1 and c1' = Y11'+d1 are E1's third assignment on A and B, with
D = Y11'-Y11 = 708af931. Let beta = ROR(c1^c1',12) and
B2 = {953908d0, 953f08d0}.
**Lemma B.** If beta is in B2 then (c1 AND 008d0953) = 00010811.
*Proof.* Put x = ROL(beta,12). Then c1^(c1+D) = x ⟺ (c1^x)-c1 = D ⟺
2(x&~c1) = D+x (mod 2^32), which fixes x&~c1 modulo 2^31, i.e. c1 on bits
0..30 of x. For 953908d0: x = 908d0953, D+x = 01180284, so x&~c1 = 008c0142
on bits 0..30 and c1&108d0953 = 10010811. For 953f08d0: x = f08d0953,
D+x = 61180284, and c1&708d0953 = 40010811. Both contain 008d0953, and on
it both values equal 00010811. QED.
Exhaustively over all 2^32 c1: 0 violations, exactly 2^22 values pass
(2^-10), 2^21 have beta 953908d0 and 2^19 have beta 953f08d0.

## 4. Algorithm and probability space

Parameters: f = 10,240, N = 2^127/f = 2^116/5, 7·256 = 1,792 trials per
group, **G_tot = ceil(2^108/35)** groups (N' = 1,792·G_tot ≥ N trials),
and GROUPS = 613,566,756 groups per context.

1. Draw one fresh uniform 256-bit word. Take X2, X5, X6, X9 from it and set
   X1 = X10 = 0. These are the only coins. The lists U, V, the masks and the
   other constants are computed once.
2. Run through contexts (X12, X13, X14) with X12 < 2^10 in a fixed order;
   there are 2^74, of which ceil(G_tot/GROUPS) < 2^73.68 are used. For each
   context run step S1 and form its resident constants (Section 5). Then for
   g = 0, 1, ..., GROUPS-1 the group holds alpha = 7g+i in lane i, i < 7:
   (a) group set-up (5.2);
   (b) for j = 0..255, straight-line: the batch (5.3) for member j in all
       lanes. If some lane passes the filter, execution falls through into
       the continuation (5.4); otherwise the filter branch jumps over it. If
       some lane of the continuation has EW = 0, then for each such lane
       run the scalar confirmation: recompute the trial (3.1), C0..C3, E1 and
       E3 for A and B, and R. If R = 0, build A and B, evaluate H(A) and
       H(B), check equality, output (A, B) and halt;
   (c) group loop: advance the alpha vector and the group counter, and test
       the continuation countdown.
3. **Hard caps.** Halt with failure after G_tot groups; at a group end where
   the continuation countdown (set to 2^-6·256·G_tot, decremented by every
   continuation) is negative, so at most 2^-6·256·G_tot + 256 continuations
   run; or when 2^96 scalar confirmations have found R ≠ 0 (their counter
   is part of the confirmation).

The probability space is the one 256-bit word of step 1. Everything else is
deterministic. The trials are the first N' trials of this order; they are
distinct (3.1) and half-colliding (Lemma T).

**Completeness.** Let a trial have R = 0 and beta in B2. If no cap has been
reached by then, the algorithm outputs a collision when it reaches that
trial: the filter flags its lane (Lemma B), the continuation computes EW = 0
for it (Lemma E), and the scalar confirmation finds R = 0. Every output is
checked with two complete hash evaluations.

## 5. Packed evaluation and the exact operation ledger

### 5.1 Machine and counting

The machine has 256-bit words and 64 registers. Every executed primitive
counts 1: add, xor, and, or, shift, compare, branch, and every load or store.
Shift amounts, immediates and fixed addresses are instruction fields (the
accepted faithful-counting reading). A packed word has seven 36-bit lanes at
offsets 36i, each holding a value modulo 2^32 with 4 guard bits. PROR(z,r) =
((z>>r) AND A_r) OR ((z<<(32-r)) AND B_r) is 5 operations: A_r and B_r select
the low 32-r and the next r bits of every lane, which drops guard bits and
bits from the neighbouring lane, so the result is reduced below 2^32. With
M = 2^32-1 in every lane, a difference is formed from XOR M plus a constant.
A rotation by 8 to the left is PROR by 24. (Layout and PROR: ticket 2bf40fb.)

### 5.2 Group set-up (per 7 values of alpha), counted 40 ALU + 11 loads

From the alpha vector a (lane i holds 7g+i, kept in a register), with
constants used only here loaded from memory (11 loads):

    c=a+(-X15); x0=(c+(-S10))^ROL(X15,8); pa=(x0+(X4+w2)) AND M
    pd=PROR(pa^X12,16); pb=PROR((pd+X8)^X4,12)
    -pc=((pd^M)+(1-X8)) AND M; ivp=((pa^M)+(pb^M)+(IV3+IV7+2)) AND M
    X5=PROR(PROR(c^S5,12)^a,7); x5w3=(X5+w3) AND M

These are the D0-family and C0-first-half lines of 3.1 in every lane. The
outputs are pb, -pc, pd, ivp = IV3+IV7-pa-pb, X5, X5+w3 and alpha, all
below 2^32. The group loop costs 6 ALU + 1 load: a+7 (load of the broadcast
7), counter increment, end test and branch, and the continuation-cap test
and branch (Section 4, step 3).

### 5.3 The batch (member j, seven alphas), counted 105 ALU + 1 load

U[j] is loaded from a fixed address; the code is straight-line over j.
Counts per value:

| part | values | ALU |
| --- | --- | ---: |
| C0 backwards | Y12=(U^pb)+(-pc) (2); ka=(PROL(Y12,8)^pd)+ivp (7) | 9 |
| K3 | kd (6), kc (1), kb (6), S11 (1), S15=S11+(kc^M)+1 (3), S3 (6), first=S3+((ka+kb)^M)+(X2+X6+1) (4) | 27 |
| D1 | d=(S11^M)+(X11-X12+1) (2), X1 (1), a=PROL(d,16)^S12 (6) | 9 |
| C1 to Y1 | qa=X1+(X5+w3) (1), qd (6), qc (1), qb (6), Y1=qa+qb+a+(-S1-S6) (3) | 17 |
| C2 | rd (6), rc=rd+alpha (1), rb (6), ra=first+rb+w0 (2), Y14 (6), Y6=PROR((rc+Y14)^rb,7) (7) | 28 |
| E1 to c1 | a1=Y1+Y6+w12 (2), d1=PROR(a1^Y12,16) (6), c1=d1+Y11 (1) | 9 |
| filter | z=(c1^FP) AND FK (2), fl=(z+M) AND bit32 (2), compare, branch (2) | 6 |

Here `first` is C2's first assignment X2+X6+w7. Lane i of fl has bit 32
clear iff (c1 AND FK) = FP, i.e. iff the lane passes. The compare and branch
test fl = bit32: the branch is taken iff no lane passes and jumps over the
inlined continuation; otherwise execution falls through into it.

### 5.4 Continuation (batches with a passing lane), counted 53 ALU + 1 load

The continuation is inlined after each batch (V[j] at a fixed address), so
no call is added; the filter branch of 5.3 jumps over it when no lane passes.

countdown decrement (1); Y9=qc+PROR(Y1^qd,8) (7); c1'=d1+Y11' (1); b1, b1' (12);
a2=a1+b1+w5, a2'=a1+b1'+(w5+2) (4); h1=PROR(Y14^V[j],16) (6, 1 load);
h1'=h1^eta (1); f1^f1'=PROR((Y9+h1)^(Y9+h1'),12) (8); t=a2^a2' (1);
EW=((f1^f1')^t^PROR(t,1)) AND M (8); flags and branch (4). The branch
jumps to the next batch iff no lane has EW = 0; otherwise execution falls
through into the lane scan and confirmations, counted in Section 8.

### 5.5 Lane bounds

With B = 2^32, every operand is below B except as follows: c<2B, x0<4B,
x0+(X4+w2)<5B; Y12<2B, ka<2B, S15<3B, (ka+kb)^M<4B, first<6B, d<2B,
qa<3B, Y1<6B, rc<2B, ra<8B, a1<8B, c1<2B; in the continuation Y9<3B,
a2<10B, Y9+h1<4B, and t<16B (an XOR of two values below 10B<2^36). All
are below 2^36, so no carry leaves a lane, and the low 32 bits of every lane are the
scalar value. The self-test measured at most 35 bits.

### 5.6 Registers

During the batches the following are resident: 12 rotation masks,
M, 1, 11, IV3, IV7, Y11, Y11', eta, FK, FP and bit32 (11), 14 per-context
constants and the 7 group outputs. That is 44 registers, and the program
records each name. Peak live batch values (born to last use, in program
order) are 9 in a batch, 8 in the continuation and 8 in the set-up, plus
3 for the group counter, the group end and the continuation countdown. So
44+9+3 = 56 ≤ 64, and no spill or store occurs.
Per-context constants are formed once per context (Section 8).

### 5.7 The counted program and its self-test

`experiments/classsearch.py` runs set-up, batch and continuation as calls on
a counting machine (one call = one operation or load) that tracks value
lifetimes, resident names and lane sums. `--selftest N [seed]` runs N seeded
cases (every fifth with words 0 or 2^32-1, every seventh in the last group)
and compares, in all seven lanes, c1, the filter flag, EW, Y4, eta, the
half-collision words and "beta in B2 implies flag" with a forward
computation from the message words; it also checks branches, the next alpha
vector, counts against the ledger, lane bits, registers, S and all 128 flag
patterns, and it compares the first three filter passes of the uncounted
copy `filter_passes` (used by experiment 4) with a scalar scan of c1 from
forward-computed states on 20 seeds. N = 2000, seed 1: 14,000/14,000 lanes,
2,000/2,000 branches, ledger counts in every case, 35 lane bits, 56
registers, 20/20 scans equal; exit status 0.
Outside the package: the forward computation equals the organizer's
`verifier/blake3.py blake3(m, 2)` on 4,000/4,000 trials (both digests), the
trial words equal an independent re-implementation written from 04638ed8's
text on 4,000/4,000, and Lemma D holds on all 4,000 real digest pairs.

### 5.8 Ledger

| per group of 1,792 trials | ALU | loads | total |
| --- | ---: | ---: | ---: |
| set-up | 40 | 11 | 51 |
| group loop | 6 | 1 | 7 |
| 256 batches | 26,880 | 256 | 27,136 |
| sum | | | **27,194 = 15.17522 per trial** |
| continuation (cap 2^-6 of batches + 256, 54 each) | | | 0.12054 per trial |

## 6. Heuristics and success probability

Let E* be the event "R = 0 and beta in B2" for a trial.

**H1 (score-critical).** Over the one random 256-bit word, the N' trials of
Section 4 behave, with respect to E*, like independent events each of
probability at least f·2^-128, f = 10,240, closely enough that P(no trial
has E*) ≤ exp(-1/2)+0.002. (N'·f·2^-128 ≥ 1/2 gives the model value.)

**H2 (supporting).** With probability at least 0.999 over the random word,
both of the following hold. (a) At most 2^-6 of the 256·G_tot batches have a
lane that passes the beta filter. (b) Fewer than 2^96 lanes of continued
batches have EW = 0 without R = 0.

**Success.** By completeness (Section 4), if some trial has E* and no cap is
hit, a collision is output. So P(success) ≥ 1 - exp(-1/2) - 0.002 - 0.001 =
0.3905 ≥ 0.39. The time bound of Section 8 holds on every run whether or
not H1 and H2 hold, because the caps are hard.

Behind H2: (a) uniform c1 passes with probability 2^-10 exactly, so a batch
continues with probability 2^-7.19 (cap: 2.3 times that); real trials gave
2,587 passes in 2,688,000 lanes and 2,580 of 384,000 batches (2^-7.22).
(b) The early test passes at 2^-29.7 per trial (7.5), at most 2^84 passes.

## 7. Our support for H1: model M and an exact bound

### 7.1 Model M and the reduction

Model M is the leader's seven-word model. In E1, A and B share d1 (Y1, Y6,
Y12 and w12 are equal), and differ only in Y11 and in w5' = w5+2. M takes
u = (d1, b1, a2) of message A uniform (equivalently d1, Y6 and a1+w5), and
(h1, Y9, w8) uniform with Y4 uniform on S, all independent. From u:

    c1=Y11+d1, c1'=Y11'+d1, beta=ROR(c1^c1',12)=b1^b1', a2'=a2+(b1^beta)-b1+2,
    tau=a2^a2', eps=c2^c2' with c2=c1+ROR(d1^a2,8), c2'=c1'+ROR(d1^a2',8),

and P_u[beta,eps,tau] = 2^-96·#{u giving these three values}. Name E3's
assignments e1, h1, g1, f1, e2, h2, g2, f2 as in 3.2.

**Lemma R.** R = 0 iff (i) eta = eps^ROL(beta^eps,1), (ii) f1^f1' =
tau^ROR(tau,1), (iii) e2^e2' = eps and (iv) g2^g2' = tau.
*Proof.* E1's output differences are tau (a), ROR(beta^eps,7) (b), eps (c)
and ROR(tau,8) (d, as d1 is shared). E3's outputs are e2, f2 =
ROR(f1^g2,7), g2 and h2 = ROR(h1^e2,8). By the formulas for o1, o3, o4, o6
in Section 2: dO1 = 0 iff (iv); dO3 = 0 iff (iii); given (iv), dO4 = 0 iff
ROR((f1^f1')^tau,7) = ROR(tau,8), i.e. (ii); given (iii), dO6 = 0 iff
ROR(eta^eps,8) = ROR(beta^eps,7), i.e. (i). QED.

In the class eta = e96d6d6b, so (i) is a condition on u alone. Since
x -> x^ROL(x,1) is linear with kernel {0, ~0}, (i) has exactly two
solutions eps for each beta, eps0 and ~eps0: eps0 = 410ad446 for 953908d0
and 410ed446 for 953f08d0. The bound uses eps0 only; dropping ~eps0 only
lowers it. Let N3_S(eps,tau) be the number of (Y4 in S, h1, Y9, w8) with
e1 = Y3+Y4, e1' = Y3'+Y4, h1' = h1^eta, g1 = Y9+h1, f1 = ROR(Y4^g1,12),
e2 = e1+f1+w8, h2 = ROR(h1^e2,8), g2 = g1+h2 (and primed likewise) that
satisfy (ii), (iii) and (iv). Under M the trial rate of E* is r_S·2^-128 with

    r_S = 2^128/(|S|·2^96) · Σ over (beta in B2, tau) of P_u[beta,eps0,tau]·N3_S(eps0,tau)
        = 2^24 · Σ P_u·N3_S.

Every term is nonnegative, so a sum over any found set of taus is a lower
bound under M.

### 7.2 The exact bound

The taus are those that Monte Carlo sampling produced with N3 > 0: 61 for
953908d0 and 29 for 953f08d0. P_u is computed exactly: beta fixes c1 on k
bits (k = 11 resp. 13, as in Lemma B), the program enumerates the 2^(32-k)
remaining values of c1 (d1 = c1-Y11) and counts (b1, a2) with a bit-serial
carry automaton. N3_S is an exact count: enumeration of the carry sign
patterns of E3's additions with a bit-serial carry DP. All 90 counts are
exact. The largest terms (spot checks; counts are #u and N3 per pattern):

| beta | tau | #u = 2^96·P_u | N3, 01000 / 10100 | term |
| --- | --- | --- | --- | ---: |
| 953908d0 | 9cdb09d2 | 2^48 | 2^35 / 2^35 | 4,096 |
| 953908d0 | 9cdb09ce | 2^45 | 2^37 / 2^37 | 2,048 |
| 953908d0 | 9edb09d2 | 2^47 | 2^35 / 2^35 | 2,048 |
| 953908d0 | 9b2b09d2 | 3·2^47 | 3·2^31 / 3·2^31 | 1,152 |
| 953f08d0 | 9cd30952 | 2^48 | 2^33 / 2^33 | 1,024 |

These five give 51%; 78 of the 90 terms are nonzero. The bound is

| beta | taus | S, pattern 01000 | S, pattern 10100 | contribution to r_S |
| --- | ---: | ---: | ---: | ---: |
| 953908d0 | 61 | 18,035.3 | 17,309.3 | 17,672.3 |
| 953f08d0 | 29 | 2,502.0 | 2,497.4 | 2,499.7 |
| **total** | 90 | 20,537.2 | 19,806.7 | **20,172.0** |

**How S was chosen.** The same 90 terms give a bound for each of the 32
patterns of e1 bits (1, 4, 7, 12, 20) (128 members each). For the 16
patterns with bit 20 = 0 they are, in decreasing order: 20,537 (01000),
19,807 (10100), 18,175, 17,565, 17,256, 16,526, 14,132, 14,051, 13,772,
13,393, 12,197, 11,821, 10,851, 10,491, 8,033 and 7,689. Every pattern with
bit 20 = 1 gives at most 155.2 (eight give 0). S is the best two of 32
under M. Its factor 2.83 over the class (7,110.4 on B2) is about 2 from
bit 20 = 0 (exact: 14,143 = 12,329 + 1,814 on those 16 patterns) and
about 1.43 from the choice within them. Structurally, the top taus need
e1 bit 12 = 0 or e1 bits 1 and 4 to differ, and S meets both.

The third beta 95390bd0, which the filter drops, contributes exactly 0 on
S: it needs e1 bit 20 = 1. The full class gives 7,124.8 on all three betas.
A rerun of both programs reproduced every term exactly (7.4).

### 7.3 Validation of the counting method

At 8-bit words (rotations 4,3,2,1) against brute force over the full model
(2^24 E1 × 2^32 E3), 9 random constant sets, every class: the exact
estimator expectation equals the brute-force class rate with 0 mismatches.
Per-member counts: 18,432 comparisons, 0 mismatches. The E1 enumeration was
also self-tested at 8 bits, with 0 mismatches. The 32-bit E3 counter is
checked against brute force only at this width.

### 7.4 Monte Carlo and reruns

Our sampling estimator stratifies on beta and samples the taus; it uses the
same exact E1 automaton and E3 counter as 7.2, so it checks the choice and
completeness of the tau lists, not the counter. Full class: 6,748 ± 252.
Restricted to S, with 2^22 draws per run:

| beta, pattern | Monte Carlo runs | exact term of 7.2 |
| --- | --- | ---: |
| 953908d0, 01000 | 17,287 ± ~1,000; 20,118 ± 3,878; 21,938 ± 9,283 | 18,035.3 |
| 953908d0, 10100 | 15,826 ± ~1,600; 19,693 ± 3,875; 21,517 ± 9,283 | 17,309.3 |
| 953f08d0, 01000 | 2,466 ± 535 | 2,502.0 |
| 953f08d0, 10100 | 2,451 ± 535 | 2,497.4 |

The figures are heavy-tailed. No sampled tau with a nonzero count was
missing from the exact list. A rerun of the same programs from scratch
reproduced all 90 E1 probabilities and E3 rows bit for bit. The only 32-bit
check of the counter by other code is the leader's: their independent
full-class estimates 7,003 ± 241 and 7,319 ± 816 against our exact 7,124.8.

### 7.5 Real trials against model M (our runs)

| statistic | real trials | model M | uniform |
| --- | --- | --- | --- |
| lane passes of the beta filter | 2^-10.02 (2,587 / 2.69M) | 2^-10 exact | |
| beta in B2 among filter passes | 0.622 (31,852 / 51,200) | 0.625 | |
| 8-bit event E8 given filter (Sec. 9) | 0.0339 ± 0.0006 (2,729 / 80,432) | 0.0342 ± 0.0001 | 0.0039 |
| early-test 8-bit event (Sec. 9) | 0.00399 (1,596 / 400,000) | 0.003945 | 0.00391 |
| Lemma E pass (32 bits), in S | 2^-29.69 (277 in 2^37.8) | 2^-29.55 (394 in 2^38.2) | 2^-32 |

The B2 share is 1.4 sd below 0.625 (a separate review run of 16,000
passes gave 0.619), so c1 may be about 1% from uniform; the effect is far
inside the margin. The Lemma E row gives real/model 0.93 (95% CI
0.79-1.08); one subset gave 73 against 96 (0.76, -1.8 sd). The E8 event
was chosen on 300,000 model draws; the figures are fresh: 12,800 filter
passes, 38,400 more from new seeds and the 29,232 passes of a 4,096-seed
run of experiment 4. On the algorithm's own filtered trials, M predicts a
residual structure 8.7 times stronger than uniform and real trials show it
at that strength. The leader's 8- and 10-bit end-to-end runs of the class
search matched the model's collision counts (9,835 vs 9,837.9; 693 vs
664.6); that is their evidence, cited here.

### 7.6 Real trials and the choice of S

None of the digest events above separates S from the rest of the class
(E8 given the filter: 0.034 in S against 0.032 outside, under M), and we
found no digest event that does at a width the organizer can test. We therefore
tested the two parts of M that the choice of S uses, on 2^36 real trials
and 2^36 fresh model draws, with members uniform over the whole class
(contexts with X1 = X10 = 0, X12 < 2^10, a new context every 4,096 trials;
B0 = the 14 other patterns with bit 20 = 0, B1 = bit 20 = 1):

| event (per trial) | real S/B0 | model S/B0 | real/model in S |
| --- | --- | --- | --- |
| E3 (iii) on bits 0..11 | 1.186 ± 0.001 | 1.185 | 1.001 (0.999-1.003) |
| E3 (iii) and (iv) for tau 9cdb09d2, bits 0..11 | 1.183 ± 0.030 | 1.176 | 0.98 (0.92-1.05) |
| E1: beta in B2 | 1.002 ± 0.001 | 1.001 | 1.001 (1.000-1.003) |
| E1: beta 953908d0 and tau ≡ 9d2 mod 2^12 | 1.003 ± 0.004 | 1.010 | 0.99 (0.98-1.00) |

The E3 side depends on the member exactly as M says (per pattern χ² 24.7
and 41.0 on 32 df; S/B1 real 2.09 and 2.12 against 2.09 and 2.08), and the
E1 side does not depend on the member. A further real-trial run (2.4M
trials, bits 2..9 of (iii)) gave a bit-20 ratio of 1.78 against 1.80. The
full S advantage itself is not visible at any width we can test.
**If the gain from choosing patterns within bit 20 = 0 were entirely
illusory, the model bound would be 14,143, still 1.38 times f.**

### 7.7 Margin and what is not shown

f = 10,240 is 1.97 times below the exact model bound 20,172.0. The bound
is exact under M and uses only beta in B2, exactly the event that the
algorithm detects. What remains is model M itself at 2^-115. It is tested
on real trials at 2^-5 (E8), 2^-8, 2^-11, 2^-21 and 2^-30 and end to end
only at small word sizes. The independence of the N' trials, which share
the four run words, is assumed exactly as in 04638ed8. No computation of
ours removes these assumptions.

## 8. Charged time, memory, preprocessing, advice

One target compression is 1 unit; every other primitive is 1/430.

- Main loop: G_tot·27,194 operations, 15.17522 per trial (5.8).
- Continuations: at most (2^-6·256·G_tot + 256)·54 operations by the cap.
- Scalar confirmations: at most 2^96 at below 2^12 operations each (trial,
  round 0, C0..C3, E1 and E3 for A and B, R, lane scan, all scalar loads and
  stores): 2^108.
- Per context: below 2^11 (step S1 below 2^10; 22 context-dependent packed
  constants at most 14 operations each; 8 stores of those kept in memory;
  at most 24 loads; initial alpha vector); 2^73.68 contexts.
- Lists (512 words): 2^18. Final check: 2 units + 2^11. One random word: 1.
- Preprocessing: 2^63 units (below). Total:

      T ≤ (G_tot·27,194 + (2^-6·256·G_tot + 256)·54 + 2^108 + 2^84.7 + 2^18
           + 2^11 + 1)/430 + 2 + 2^63  =  2^108.8668  <  2^108.9.

Here G_tot·27,194 = 2^117.6017 and the continuation cap is 2^110.6256
operations. The bound is worst case on every run; the slack to 108.9 is
0.033 bits (0.36 operations per trial).

**Memory.** The code is straight-line over the 256 members: 256·(106+54)
batch and inlined continuation instructions, plus set-up, confirmation,
step S1 and a compression routine. That is fewer than 50,000 instructions of
at most 16 bytes each (opcode, three 6-bit register fields, a shift amount
and a 32-bit address or immediate), below 800,000 bytes. Data is two lists of 256 words, about
100 constant and context words, and scratch: below 2^16 bytes. The total is
below 2^20 bytes, so memory_log2_bytes = 20.

**Preprocessing and selection.** Recomputing and selecting the constants
and eta is bounded by 2^71 operations (04638ed8), below 2^63 units. Our
selection of S, the filter and E8, with every computation of Sections 7
and 9 including the 8-bit brute-force validations, ran on one machine with
16 cores for less than 12 days: at most 16 · 12 · 86,400 core-seconds at
2^35 primitive operations each, below 2^60 operations. Together below
2^71.1 operations, i.e. below 2^63 units: preprocessing_log2 = 63 covers
both and is included in T.

**Advice.** The six constants and eta (28 bytes), the sub-class mask and two
values (12 bytes), and FK and FP (8 bytes) total 48 bytes, so
nonuniform_advice_log2_bytes = 6. The lists are computed from these.

## 9. Organizer-executed experiments

All four run `experiments/classsearch.py` (standard library only; G is
evaluated directly, never an implementation of BLAKE3) on the exact target.
The organizer recomputes both digests of every returned pair and checks the
mask event. Observations are participant output and untrusted. Our local
replay of `experiments.runner` with a subprocess executor gave the results
below for seed `hashsmash-public-seed-v1`, 256 trials each, with
byte-identical reruns.

1. **half-collision.** One trial per seed (run words, context with
   X12 < 2^10, group, lane and member of S from the seed). Event: words
   0, 2, 5, 7 equal. Prediction: 256/256 (exact). Replay: 256/256.
   Observations: the counted group of 5.2–5.4 for the same context, with
   setup_ops 46, setup_loads 12, batch_ops 105, batch_loads 1, cont_ops 53,
   cont_loads 1 and lanes_equal 7 on all 256 seeds.
2. **class-walk.** 64 consecutive members of S for one context and alpha,
   each evaluated forwards. Returns the seed member's pair. Prediction:
   256/256, and y4_equal = eta_equal = 64. Replay: 256/256; y4_equal and
   eta_equal 64 on all seeds; 15 filter passes in 16,384 trials.
3. **early-test-bits** (reduced width). Trials in algorithm order, at most
   256 per seed, until dO1 has its low 4 bits zero and dO4 has bits 25..28
   zero. Then EW has its low 4 bits zero (Lemma D). Event: those 136 bits.
   Prediction from model M: per-trial p = 0.003945, so 1-(1-p)^256 = 0.636
   (163 ± 8 of 256). Replay: 161/256, with 40,075 trials tried (p = 0.00402).
4. **filtered-residual** (reduced-width rate measurement). Trials in
   algorithm order through an uncounted copy of the batch up to the filter
   (the self-test checks it against a scalar c1 scan, 5.7); each pass is
   re-evaluated forwards. Among the first 8 filter passes, return the first
   whose dO3 is zero on bits 28, 27, 23, 22 and dO6 on bits 20, 19, 15, 14
   (E8). Prediction from model M: q = 0.0342, so 1-(1-q)^8 = 0.243
   (62 ± 7 of 256); uniform bits give 0.031 (8/256).
   Replay: 79/256 (0.309; 1,744 filter passes examined, q estimate 0.045).
   That is 2.5 binomial standard deviations above the model; a holdout
   seed of our review gave 75/256. The same program on 4,096 seeds of ours
   gave 961/4,096 (0.235). Pooled over 80,432 real filter passes (7.5),
   q = 0.0339 ± 0.0006 against the model's 0.0342, far from uniform.

Replay times were 0.2 to 1.4 s per 256-trial request on a loaded machine.

## 10. Sensitivity and limitations

For a factor f in H1 the same algorithm needs 2^127/f trials, and the time
is 108.8668 + log2(10,240/f):

| f | time_log2 | basis |
| ---: | ---: | --- |
| 20,172 (exact model bound) | 107.89 | not claimed |
| 14,143 (bound for bit 20 = 0, 7.6) | 108.40 | not claimed |
| **10,240 (claimed)** | **108.87 → 108.9** | margin 1.97 |
| 8,192 | 109.19 | margin 2.46 |
| 2,048 (04638ed8's factor) | 111.19 | |
| 1 (uniform residual) | 122.19 → 122.2 | |

If the true per-trial rate is f'·2^-128, the success bound is
1-exp(-f'/20,480)-0.003. Continuation cap 2^-5 instead of 2^-6 would give
108.878. The caps change only the success probability, never the time
bound.

Not helpful (details in our note): a bitsliced 256-lane batch (16.3 to 16.9
operations per trial counted with spills), other classes, redesigned C3
constants, a second free round-1 word, and a residual birthday. Each
round-1 column call feeds both E1 and E3.

Limitations (see 7.6, 7.7): H1 is not proved; use of model M at 2^-115 is
an extrapolation. S is the best 2 of 32 patterns under M; its advantage is
not tested on real trials at any width, only the two parts of M it uses
(7.6). All counts are the program's own; the organizer checks digests only.
S, E8 and the filter were chosen by our computations.

**Nominal baseline.** `baseline_improved` names `blake3-r2-nominal-v2`, the
organizer's nominal display reference (128) for this track. It is not an
established attack or baseline; we keep the identifier because the
organizer requires it, and claim no improvement over any reviewed result
other than the comparison with 04638ed8 stated above.
