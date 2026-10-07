# sha256-r31 bit-sliced fast path, ceiling 36.47

## 1. Claim

The ordinary collision in `certificates/manifest.json` is a deterministic
replay. The construction that produced it is charged at the executed counters
of one search, plus a three-attempt ceiling for the starting solution.

| Quantity | Value |
| --- | ---: |
| Sum | 94296828771.392059 target compressions |
| log2(sum) | 36.456490 |
| Claimed ceiling | 36.47 |
| Promoted leader | 37.22 |
| Success probability | 1 |

Expected time is not used. Memory is a reported metric only.

## 2. Target

Target `sha256-r31-prefix-v1`: SHA-256 steps 0 through 30 on every padded
block, standard IV used once, FIPS padding, full feed-forward, all eight
digest words. The two messages are distinct, 128 bytes, and share their first
64-byte block. This is not a 32-step collision and not a full SHA-256
collision. The organizer digest of both messages is
`e647f1ce4912b90b9976c5b41c56aa4d4d67ac60005391c707e390e86d6a0f2b`.

## 3. Witness

Message A is block M0 followed by M1. Message B is M0 followed by M1'.

```
M0  502b257bd2e338591d3972ec9461a4f158f5578f78c616d5e027a9687f248cc4853974c0a648ab610f6afeb61faf471a97a1b75e4658c6ce129ce1a20028731c
M1  f160290cd79952b2eb6b051bdbb584221a02ee8bbbc3160f2e52531c8a1dd6fa39da2af9973a6552db0e42199496c20f50f1cd9942e8038f2247834093acadb7
M1' f160290cd79952b2eb6b051bdbb584221a02ee8bbbc306152e72db0dda0d8cf461db3bf9973ae556db0e42199496c20f50f1cd9942e8038f2247834093acadb7
```

The collision index in the deterministic search below is `n=176264082204`.
The charged trial counter, including sibling threads after that index, is
`177335173256`.

## 4. Exact search algorithm

There is no undefined copy condition. The completion predicates are the
following equalities, evaluated in this order on the two copies of the
neutral state. `AA`, `EA` are copy A. `AB`, `EB` are copy B. `sm` draws a
32-bit word from the trial's SHAKE-256 stream. `D9` is `0x00008004`.

1. Before any draw, compute `b13` and `b13b` from the neutral state and the
   message words already fixed by the group. If `b13 != b13b`, return failure.
   This check does not increment a counter.
2. For each of at most `2^22` draws, increment the E13 counter, set
   `E13 = sm(rs)`, and set `W13 = E13 - b13`. Compute

```
A13  = E13 - AA(9) + BS0(AA(12)) + MAJ(AA(12), AA(11), AA(10))
A13b = E13 - AB(9) + BS0(AB(12)) + MAJ(AB(12), AB(11), AB(10))
```

   If `A13 != A13b`, abort the whole completion. This is an equality test,
   not a named side condition.
3. Compute

```
E14  = AA(10) + EA(10) + BS1(E13) + IF(E13, EA(12), EA(11)) + K[14] + W14
E14b = AB(10) + EB(10) + BS1(E13) + IF(E13, EB(12), EB(11)) + K[14] + W14
```

   If `(E14b - E14) mod 2^32 != 0x8004`, take the next E13 draw.
4. Compute `A14` and `A14b` from `E14`, `E14b`, `A13`, and the neutral words.
   If `A14 != A14b`, take the next E13 draw.
5. Compute

```
f15  = AA(11) + EA(11) + BS1(E14)  + IF(E14,  E13, EA(12)) + K[15]
f15b = AB(11) + EB(11) + BS1(E14b) + IF(E14b, E13, EB(12)) + K[15]
```

   If `f15 != f15b`, take the next E13 draw.
6. For each of at most `2^12` draws, increment the E15 counter, set
   `E15 = sm(rs)` and `W15 = E15 - f15`. Compute

```
E16  = AA(12) + EA(12) + BS1(E15) + IF(E15, E14,  E13) + K[16] + g
E16b = AB(12) + EB(12) + BS1(E15) + IF(E15, E14b, E13) + K[16] + g + D9
```

   If `E16 != E16b`, take the next E15 draw.
7. Compute

```
f17  = A13 + E13 + BS1(E16) + IF(E16, E15, E14)
f17b = A13 + E13 + BS1(E16) + IF(E16, E15, E14b)
```

   If `f17 != f17b`, take the next E15 draw. Otherwise set `W[13] = W13` and
   `W[15] = W15` and return success.

`BS0`, `BS1`, `IF`, and `MAJ` are the FIPS SHA-256 functions. `K[i]` is the
FIPS round constant. These seven tests are the entire completion predicate.
The earlier rejected package called some of them copy-Q checks without
writing the equalities. They are written here.

The outer search, for each group, fixes message words `m[0..14]` from the
group index and the seed, runs SHA-256 steps 0 through 14 once, then for
each `x` in `0 .. 2^24-1` sets `W[15] = x` and evaluates only the message
schedule and rounds that depend on `x`. It then forms `key = IV[0] + a` after
step 30 and tests a 24-bit bitmap of table keys. A bitmap hit recompresses
the full 31-step block and binary-searches the 73728-record table. A key
match runs the seven predicates above. The first success writes the two
second blocks and stops the other threads. The charged trial counter includes
work those threads do after the winning index.

The scalar fast path is 501 primitive 32-bit operations per `x`. The ledger does not charge that scalar path. It charges the bit-sliced program in Section 6, which computes the same step-30 word 0. A group setup of steps 0 through 14 is charged once per group, not inside the per-trial term.

## 5. Execution record

Command, one run, 28 threads, seed `0x7231a5ed2026`, 1800-second limit. It
returned at 41 seconds.

| Counter | Value |
| --- | ---: |
| Trials, including sibling overshoot | 177335173256 |
| Winning index | 176264082204 |
| Groups | 10578 |
| Aborted groups | 17 |
| Bitmap hits | 61549763 |
| Key hits after recompression | 1110199 |
| Record visits | 3045760 |
| V6 passes | 5738 |
| Joint passes | 1 |
| Completion calls | 1 |
| E13 iterations executed | 3712 |
| E15 iterations executed | 26 |
| Collisions | 1 |

The E13 and E15 figures are the iterations the program executed, not a cap.
The previous package charged `2^16` entries times `2^22` draws and omitted
the E15 loop. This package charges 3712 and 26. The bitmap figure is the
executed hit counter, not `trials * 73728 / 2^24`.

## 6. Cost ledger

One target compression is 2140 primitive 32-bit operations. Every term below
is included in the sum.

| Term | Charge | Units |
| --- | ---: | ---: |
| Bit-sliced trials | 692715521 * 41047 / 2140 | 13286866350.694860 |
| Bit-sliced group setup | 10578 * 28116 / 2140 | 138977.125234 |
| Bitmap hits | 61549763 * (2140 + 256) / 2140 | 68912725.302804 |
| Record visits | 3045760 * 400 / 2140 | 569300.934579 |
| V6 passes | 5738 * 1600 / 2140 | 4290.093458 |
| Completion iterations | (3712 + 26) * 80 / 2140 | 139.738318 |
| Table scans | 12 * 2^32 * 8 / 2140 | 192671430.100935 |
| Self-test | 2000 compressions | 2000.000000 |
| Replay | 6 compressions | 6.000000 |
| Three z3 attempts | 3 * 6e9 * 8 * 1200 / 2140 | 80747663551.401871 |
| Sum |  | 94296828771.392059 |

`log2(sum) = 36.456490 < 36.47`. The 400, 1600, and 80 operation
allowances are larger than the operations visible in the corresponding loops.
The table term charges twelve full 2^32 scans even though the builder is one
scan. Those choices raise the sum. They do not hide work.

The bit-sliced trial term replaces the previous 525-operation scalar charge
and the previous 2000-operation group charge. The charged program is specified
here; it is not an external file. It stores each bit of 256 independent trials
in one 256-bit word. XOR, AND, OR and NOT of those words are one primitive
operation each. A 32-bit rotate or logical shift is a reindex of the 32 bit
words and emits no operation. Addition is a data-independent ripple: bit 0 is
one XOR and one AND, and each later bit is two XORs, two ANDs and one OR.
The same operation count was measured on two independent messages and at
width 1 and width 256: 22725 operations for steps 0 through 14, 5391 for the
`x`-independent expansion, and 41047 for each batch of 256 values of `x`
(dependent schedule, 16 rounds, key addition, 24-bit gather, load, compare
and branch). `692715521 = ceil(177335173256 / 256)`. The last batch is
partial and is charged in full. On 768 random inputs the bit-sliced step-30
word 0 matched `verifier.hash_functions._compress(..., rounds=31)`.

The search-only subtotal, excluding the z3 term, is 13549165219.990188,
which is `2^33.657`. The z3 term is identified separately so a reviewer can
replace it without reconstructing the search. A 600-second z3 5.1.0 run of
the stored model timed out, so this package does not replace that ceiling.

## 7. Heuristics

`H-Z3-THREE-ATTEMPT-CEILING` is the only score-critical premise that is not
an executed counter. The starting solution was produced by a local z3 5.1.0
bit-blast from the public characteristic and seed `88108363`. This package
charges three full 1200-second single-core windows, not the shorter
successful run, and not the one-window charge used by the rejected 37.0
package. Eight operations per cycle is not a measured throughput. It is an
upper allowance. The yield counters in Section 5 do not depend on this
premise.

No bitmap-density premise is used. No unmeasured completion-entry cap is
used. No omitted E15 loop remains in the formula.

## 8. Organizer experiment

`experiments/replay.py` replays the stored pair. It checks the 32-byte tuple
layout on its finite domain and returns the two messages for every organizer
trial. It does not re-run the search and does not measure attack cost. The
cost is the ledger in Section 6. The certificate check is the collision.

## 9. Relation to the promoted 37.22 package

The promoted package charges each of its 99492036640 trials a full
compression plus 32 operations. This search does not. Steps 0 through 14 are
shared inside a group. The `x`-dependent tail is the bit-sliced program in
Section 6, not a 525-operation scalar charge. The executed bitmap and
completion counters are unchanged. The resulting ceiling, 36.47, is below
the promoted 37.22 and below the 36.9 scalar package.

## Appendix A. Counted search source

The program that produced Section 5 is the following source. The completion predicates in Section 4 are this `complete` function. The 501-operation fast path is the per-x loop after the shared steps 0 through 14.

### sp_yield.h

```c
/* z3 5.1.0 bit-blast, seed 88108363, constraints (a)-(e) plus residue e730f */
static const uint32_t SPA_A[35]={0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x227944b9u,0xdeee29b6u,0xab41c5e0u,0x632d7f31u,0xfad053ffu,0xd9ffe4b8u,0x89bf5274u,0x578fe155u,0xa180a1bau,0xbeea7fa3u,0x1354799cu,0xe7f656d6u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
static const uint32_t SPA_E[35]={0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x1d1fa7ddu,0xada878e7u,0x4cd7cae5u,0x943bc249u,0x61c503d1u,0x7026b3fau,0x2a2f041du,0xf1f1c9e8u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
static const uint32_t SPB_A[35]={0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x227944b9u,0xdeee29b6u,0xab41c5e0u,0x632d7f31u,0xfad04405u,0xd97fe4b9u,0x989f4271u,0x578fe151u,0xa180a1bau,0xbeeaffa7u,0x1354799cu,0xe7f656d6u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
static const uint32_t SPB_E[35]={0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x1d1f97e3u,0xada0f8e6u,0x9c5fce6cu,0xd93b4a4du,0x61c503d9u,0x5fa73402u,0x3aef0415u,0xf1f149e0u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
static const uint32_t S_W[31]={0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x973a6552u,0xdb0e4219u,0x9496c20fu,0x50f1cd99u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
```

### opcount.c

```c

#include <stdio.h>
#include <stdint.h>
static unsigned long ops;
static uint32_t R(uint32_t x,int n){ops+=1; return (x>>n)|(x<<(32-n));}
static uint32_t X(uint32_t a,uint32_t b){ops+=1; return a^b;}
static uint32_t A(uint32_t a,uint32_t b){ops+=1; return a+b;}
static uint32_t AN(uint32_t a,uint32_t b){ops+=1; return a&b;}
static uint32_t NT(uint32_t a){ops+=1; return ~a;}
static uint32_t SH(uint32_t x,int n){ops+=1; return x>>n;}
static uint32_t BS0(uint32_t x){return X(X(R(x,2),R(x,13)),R(x,22));}
static uint32_t BS1(uint32_t x){return X(X(R(x,6),R(x,11)),R(x,25));}
static uint32_t s0(uint32_t x){return X(X(R(x,7),R(x,18)),SH(x,3));}
static uint32_t s1(uint32_t x){return X(X(R(x,17),R(x,19)),SH(x,10));}
static uint32_t IF(uint32_t x,uint32_t y,uint32_t z){return X(AN(x,y),AN(NT(x),z));}
static uint32_t MAJ(uint32_t x,uint32_t y,uint32_t z){return X(X(AN(x,y),AN(x,z)),AN(y,z));}
int main(void){
  uint32_t x=1,c17=2,c19=3,c21=4,c22=5,c23=6,c24=7,c25=8,c26=9,c27=10,c28=11,c29=12,c30=13;
  uint32_t K[31]={0};
  ops=0;
  uint32_t w17=A(s1(x),c17), w19=A(s1(w17),c19), w21=A(s1(w19),c21), w22=A(c22,x);
  uint32_t w23=A(s1(w21),c23), w24=A(A(s1(w22),w17),c24), w25=A(s1(w23),c25);
  uint32_t w26=A(A(s1(w24),w19),c26), w27=A(s1(w25),c27), w28=A(A(s1(w26),w21),c28);
  uint32_t w29=A(A(s1(w27),w22),c29), w30=A(A(A(s1(w28),w23),s0(x)),c30);
  uint32_t AA=1,B=2,C=3,D=4,E=5,F=6,G=7,H=8,T1,T2,m16=9,m18=10,m20=11;
  #define RND(w,k) T1=A(A(A(A(H,BS1(E)),IF(E,F,G)),(k)),(w)); T2=A(BS0(AA),MAJ(AA,B,C)); H=G; G=F; F=E; E=A(D,T1); D=C; C=B; B=AA; AA=A(T1,T2);
  RND(x,K[15]) RND(m16,K[16]) RND(w17,K[17]) RND(m18,K[18]) RND(w19,K[19]) RND(m20,K[20]) RND(w21,K[21]) RND(w22,K[22])
  RND(w23,K[23]) RND(w24,K[24]) RND(w25,K[25]) RND(w26,K[26]) RND(w27,K[27]) RND(w28,K[28]) RND(w29,K[29]) RND(w30,K[30])
  uint32_t key=A(0x6a09e667u,AA);
  ops+=6; /* bitmap index: two shifts, two ands, one shift, one compare */
  (void)key;(void)w30;
  printf("trial_ops %lu per_compression %.6f\n", ops, ops/2140.0);
  return 0;
}
```

### r31yield.c

```c
// sha256-r31 relaxed-W20 first-block search from the published starting solution.
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <time.h>
#include <unistd.h>
#include <stdatomic.h>
#include "sp_yield.h"

static const uint32_t K[31]={0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
 0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
 0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
 0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351};
static const uint32_t IV[8]={0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};
#define R(x,n) (((x)>>(n))|((x)<<(32-(n))))
#define BS0(x) (R(x,2)^R(x,13)^R(x,22))
#define BS1(x) (R(x,6)^R(x,11)^R(x,25))
#define s0(x) (R(x,7)^R(x,18)^((x)>>3))
#define s1(x) (R(x,17)^R(x,19)^((x)>>10))
#define IF(x,y,z) (((x)&(y))^(~(x)&(z)))
#define MAJ(x,y,z) (((x)&(y))^((x)&(z))^((y)&(z)))
#define D5 0xfffff006u
#define D6 0x002087f1u
#define D7 0x4fefb5fau
#define D8 0x28011100u
#define D9 0x00008004u
#define D18 0xffff7ffcu
#define C6 0x00000ffau
#define C7 0xffdf780fu
#define C8 0xb00fca02u
#define IDX(i) ((i)+4)
#define AA(i) SPA_A[IDX(i)]
#define EA(i) SPA_E[IDX(i)]
#define AB(i) SPB_A[IDX(i)]
#define EB(i) SPB_E[IDX(i)]

typedef struct { uint32_t key, A0, E3, E4, W7, W8; } rec_t;
static rec_t *recs; static int nrec;
static uint64_t *bitmap; /* 2^24 bits on key>>8 */
static uint32_t G16[64]; static int ng16;
static uint32_t s1inv_col[32];

static void compress31(const uint32_t cv[8], const uint32_t m[16], uint32_t out[8]) {
  uint32_t W[31]; for(int t=0;t<16;t++) W[t]=m[t];
  for(int t=16;t<31;t++) W[t]=s1(W[t-2])+W[t-7]+s0(W[t-15])+W[t-16];
  uint32_t a=cv[0],b=cv[1],c=cv[2],d=cv[3],e=cv[4],f=cv[5],g=cv[6],h=cv[7];
  for(int t=0;t<31;t++){ uint32_t T1=h+BS1(e)+IF(e,f,g)+K[t]+W[t]; uint32_t T2=BS0(a)+MAJ(a,b,c);
    h=g; g=f; f=e; e=d+T1; d=c; c=b; b=a; a=T1+T2; }
  out[0]=cv[0]+a; out[1]=cv[1]+b; out[2]=cv[2]+c; out[3]=cv[3]+d; out[4]=cv[4]+e; out[5]=cv[5]+f; out[6]=cv[6]+g; out[7]=cv[7]+h;
}
static void digest(const uint32_t m0[16], const uint32_t m1[16], uint32_t out[8]) {
  uint32_t cv[8], cv2[8], pad[16]={0}; pad[0]=0x80000000u; pad[15]=1024;
  compress31(IV,m0,cv); compress31(cv,m1,cv2); compress31(cv2,pad,out);
}
static uint32_t s1inv(uint32_t y){ uint32_t x=0; for(int k=0;k<32;k++) if(y>>k&1) x^=s1inv_col[k]; return x; }
static void build_s1inv(void){
  uint32_t val[32], comb[32]; for(int i=0;i<32;i++){ uint32_t b=1u<<i; val[i]=s1(b); comb[i]=b; }
  for(int k=0;k<32;k++){ int p=-1; for(int i=k;i<32;i++) if(val[i]>>k&1){p=i;break;}
    if(p<0){fprintf(stderr,"s1 singular\n");exit(1);} uint32_t tv=val[k],tc=comb[k]; val[k]=val[p];comb[k]=comb[p];val[p]=tv;comb[p]=tc;
    for(int i=0;i<32;i++) if(i!=k && (val[i]>>k&1)){ val[i]^=val[k]; comb[i]^=comb[k]; } }
  for(int k=0;k<32;k++) s1inv_col[k]=comb[k];
  for(int t=0;t<1000;t++){ uint32_t y=(uint32_t)(t*2654435761u+12345); if(s1(s1inv(y))!=y){fprintf(stderr,"s1inv bad\n");exit(1);} }
}
static int cmprec(const void*a,const void*b){ uint32_t x=((const rec_t*)a)->key,y=((const rec_t*)b)->key; return x<y?-1:x>y; }
static void build_table(void){
  static uint32_t V7[1024],V8[65536]; int n7=0,n8=0; uint32_t w=0;
  do{ if((uint32_t)(s0(w+D8)-s0(w))==C8) V8[n8++]=w; if((uint32_t)(s0(w+D7)-s0(w))==C7) V7[n7++]=w;
      if((uint32_t)(s1(w+D9)-s1(w))==D18) G16[ng16++]=w; w++; }while(w!=0);
  uint32_t cm4=0,va4=0,cm3=0,va3=0; const char*r4="============0===0=========01===0",*r3="==========================10====";
  for(int k=0;k<32;k++){ uint32_t b=1u<<(31-k); if(r4[k]!='='){cm4|=b; if(r4[k]=='1')va4|=b;} if(r3[k]!='='){cm3|=b; if(r3[k]=='1')va3|=b;} }
  uint32_t lhs7=(EB(7)-EA(7))-(BS1(EB(6))-BS1(EA(6)))-D7, lhs6=(EB(6)-EA(6))-(BS1(EB(5))-BS1(EA(5)))-D6;
  recs=malloc(sizeof(rec_t)*(1<<20)); nrec=0;
  for(int i=0;i<n8;i++){ uint32_t W8=V8[i]; uint32_t E4=EA(8)-AA(4)-BS1(EA(7))-IF(EA(7),EA(6),EA(5))-K[8]-W8;
    if((E4&cm4)!=va4) continue; if((uint32_t)(IF(EB(6),EB(5),E4)-IF(EA(6),EA(5),E4))!=lhs7) continue;
    uint32_t A0=E4-AA(4)+BS0(AA(3))+MAJ(AA(3),AA(2),AA(1));
    for(int j=0;j<n7;j++){ uint32_t W7=V7[j]; uint32_t E3=EA(7)-AA(3)-BS1(EA(6))-IF(EA(6),EA(5),E4)-K[7]-W7;
      if((E3&cm3)!=va3) continue; if((uint32_t)(IF(EB(5),E4,E3)-IF(EA(5),E4,E3))!=lhs6) continue;
      uint32_t Am1=E3-AA(3)+BS0(AA(2))+MAJ(AA(2),AA(1),A0);
      recs[nrec++]=(rec_t){Am1,A0,E3,E4,W7,W8}; } }
  qsort(recs,nrec,sizeof(rec_t),cmprec);
  bitmap=calloc(1<<18,8); for(int i=0;i<nrec;i++){ uint32_t b=recs[i].key>>8; bitmap[b>>6]|=1ull<<(b&63); }
  fprintf(stderr,"V7=%d V8=%d G16=%d records=%d\n",n7,n8,ng16,nrec);
}

typedef struct { uint64_t trials, keyhits, recs, v6, joint, both, comp_try, comp_ok, coll, it13, it15, overshoot, bmhits, groups; } ctr_t;
static ctr_t ctrs[64];
static atomic_int stop_flag; static atomic_int live_threads; static pthread_mutex_t out_mu=PTHREAD_MUTEX_INITIALIZER;
static FILE *outf; static atomic_uint_fast64_t total_coll;

static uint64_t sm(uint64_t *s){ uint64_t z=(*s+=0x9e3779b97f4a7c15ull); z=(z^(z>>30))*0xbf58476d1ce4e5b9ull; z=(z^(z>>27))*0x94d049bb133111ebull; return z^(z>>31); }

/* returns 1 if completion found; fills W[0..15] */
static int complete(uint32_t W[16], uint32_t g, uint64_t *rs, ctr_t *cc){
  uint32_t W14=s1inv(g-W[9]-s0(W[1])-W[0]); W[14]=W14;
  if((uint32_t)(s1(W14)+W[9]+s0(W[1])+W[0])!=g) return 0;
  uint32_t b13=AA(9)+EA(9)+BS1(EA(12))+IF(EA(12),EA(11),EA(10))+K[13];
  uint32_t b13b=AB(9)+EB(9)+BS1(EB(12))+IF(EB(12),EB(11),EB(10))+K[13];
  if(b13!=b13b) return 0;
  for(int t=0;t<(1<<22);t++){
    cc->it13++; uint32_t E13=(uint32_t)sm(rs); uint32_t W13=E13-b13;
    uint32_t A13=E13-AA(9)+BS0(AA(12))+MAJ(AA(12),AA(11),AA(10));
    uint32_t A13b=E13-AB(9)+BS0(AB(12))+MAJ(AB(12),AB(11),AB(10)); if(A13!=A13b) return 0;
    uint32_t E14=AA(10)+EA(10)+BS1(E13)+IF(E13,EA(12),EA(11))+K[14]+W14;
    uint32_t E14b=AB(10)+EB(10)+BS1(E13)+IF(E13,EB(12),EB(11))+K[14]+W14;
    if((uint32_t)(E14b-E14)!=0x8004u) continue;
    uint32_t A14=E14-AA(10)+BS0(A13)+MAJ(A13,AA(12),AA(11)), A14b=E14b-AB(10)+BS0(A13)+MAJ(A13,AB(12),AB(11));
    if(A14!=A14b) continue;
    uint32_t f15=AA(11)+EA(11)+BS1(E14)+IF(E14,E13,EA(12))+K[15], f15b=AB(11)+EB(11)+BS1(E14b)+IF(E14b,E13,EB(12))+K[15];
    if(f15!=f15b) continue;
    for(int u=0;u<(1<<12);u++){
      cc->it15++; uint32_t E15=(uint32_t)sm(rs); uint32_t W15=E15-f15;
      uint32_t E16=AA(12)+EA(12)+BS1(E15)+IF(E15,E14,E13)+K[16]+g, E16b=AB(12)+EB(12)+BS1(E15)+IF(E15,E14b,E13)+K[16]+g+D9;
      if(E16!=E16b) continue;
      uint32_t A15=E15-AA(11)+BS0(A14)+MAJ(A14,A13,AA(12));
      uint32_t f17=A13+E13+BS1(E16)+IF(E16,E15,E14), f17b=A13+E13+BS1(E16)+IF(E16,E15,E14b); (void)A15;
      if(f17!=f17b) continue;
      W[13]=W13; W[15]=W15; return 1; } }
  return 0;
}

static int process_hit(int tid, const uint32_t m0[16], uint64_t *rs, int verbose){ int found=0;
  ctr_t *c=&ctrs[tid]; c->bmhits++; uint32_t cv[8]; compress31(IV,m0,cv);
  int lo=0,hi=nrec; while(lo<hi){int mid=(lo+hi)/2; if(recs[mid].key<cv[0]) lo=mid+1; else hi=mid;}
  if(lo>=nrec || recs[lo].key!=cv[0]) return 0;
  c->keyhits++;
  for(int r=lo;r<nrec && recs[r].key==cv[0];r++){
    const rec_t *q=&recs[r]; c->recs++;
    uint32_t a[35],e[35];
    a[IDX(-1)]=cv[0];a[IDX(-2)]=cv[1];a[IDX(-3)]=cv[2];a[IDX(-4)]=cv[3];e[IDX(-1)]=cv[4];e[IDX(-2)]=cv[5];e[IDX(-3)]=cv[6];e[IDX(-4)]=cv[7];
    a[IDX(0)]=q->A0; for(int i=1;i<=12;i++) a[IDX(i)]=AA(i); e[IDX(3)]=q->E3; e[IDX(4)]=q->E4; for(int i=5;i<=12;i++) e[IDX(i)]=EA(i);
#define Ax(i) a[IDX(i)]
#define Ex(i) e[IDX(i)]
    Ex(0)=Ax(0)+Ax(-4)-BS0(Ax(-1))-MAJ(Ax(-1),Ax(-2),Ax(-3));
    Ex(1)=Ax(1)+Ax(-3)-BS0(Ax(0))-MAJ(Ax(0),Ax(-1),Ax(-2));
    Ex(2)=Ax(2)+Ax(-2)-BS0(Ax(1))-MAJ(Ax(1),Ax(0),Ax(-1));
    uint32_t W[16]; for(int i=0;i<=6;i++) W[i]=Ex(i)-Ax(i-4)-Ex(i-4)-BS1(Ex(i-1))-IF(Ex(i-1),Ex(i-2),Ex(i-3))-K[i];
    W[7]=q->W7; W[8]=q->W8; for(int i=9;i<=12;i++) W[i]=S_W[i]; W[13]=W[14]=W[15]=0;
    int v6=((uint32_t)(s0(W[6]+D6)-s0(W[6]))==C6);
    if(!v6) continue;
    c->v6++;
    uint32_t tgt=0u-(uint32_t)(s0(W[5]+D5)-s0(W[5])); uint32_t c18=W[11]+s0(W[3])+W[2];
    int gsel=-1; for(int k=0;k<ng16;k++){ uint32_t w18=s1(G16[k])+c18; if((uint32_t)(s1(w18+D18)-s1(w18))==tgt){gsel=k;break;} }
    if(gsel<0) continue;
    c->joint++; c->both++;
    c->comp_try++;
    uint32_t Wc[16]; memcpy(Wc,W,sizeof W);
    if(!complete(Wc,G16[gsel],rs,c)) { if(verbose) fprintf(stderr,"completion failed\n"); continue; }
    c->comp_ok++;
    uint32_t Wb[16]; memcpy(Wb,Wc,sizeof Wc); Wb[5]+=D5; Wb[6]+=D6; Wb[7]+=D7; Wb[8]+=D8; Wb[9]+=D9;
    uint32_t h1[8],h2[8]; digest(m0,Wc,h1); digest(m0,Wb,h2);
    if(memcmp(h1,h2,32)==0 && memcmp(Wc,Wb,64)!=0){
      c->coll++; atomic_fetch_add(&total_coll,1); found=1;
      pthread_mutex_lock(&out_mu);
      fprintf(outf,"COLLISION tid=%d\nM0 ",tid); for(int i=0;i<16;i++) fprintf(outf,"%08x",m0[i]);
      fprintf(outf,"\nM1 "); for(int i=0;i<16;i++) fprintf(outf,"%08x",Wc[i]);
      fprintf(outf,"\nM1b "); for(int i=0;i<16;i++) fprintf(outf,"%08x",Wb[i]);
      fprintf(outf,"\nDIGEST "); for(int i=0;i<8;i++) fprintf(outf,"%08x",h1[i]); fprintf(outf,"\n"); fflush(outf);
      pthread_mutex_unlock(&out_mu);
    } else if(verbose) fprintf(stderr,"digest mismatch\n");
    if(found) return 1;
  }
  return found;
}

static uint64_t seed_base; static double time_limit;
#define LANES 8
static int NTH; static _Atomic uint64_t best_n = UINT64_MAX;
static void *worker(void *arg){
  int tid=(int)(intptr_t)arg; ctr_t *c=&ctrs[tid]; atomic_fetch_add(&live_threads,1);
  uint32_t m[16];
  for(uint64_t g=(uint64_t)tid; ; g+=(uint64_t)NTH){
    uint64_t bn=atomic_load(&best_n);
    if(atomic_load(&stop_flag)) break;
    if(bn!=UINT64_MAX && g > (bn>>24)) break;
    c->groups++; uint64_t rs=seed_base ^ (g*0x9e3779b97f4a7c15ull) ^ 0x5bd1e9955bd1e995ull;
    for(int i=0;i<15;i++) m[i]=(uint32_t)sm(&rs);
    uint64_t crs=seed_base ^ (g*0xd1b54a32d192ed03ull) ^ 0x2545f4914f6cdd1dull; /* completion coins */
    uint32_t a=IV[0],b=IV[1],cc=IV[2],d=IV[3],e=IV[4],f=IV[5],gg=IV[6],h=IV[7];
    for(int t=0;t<15;t++){ uint32_t T1=h+BS1(e)+IF(e,f,gg)+K[t]+m[t]; uint32_t T2=BS0(a)+MAJ(a,b,cc); h=gg; gg=f; f=e; e=d+T1; d=cc; cc=b; b=a; a=T1+T2; }
    const uint32_t m16=s1(m[14])+m[9]+s0(m[1])+m[0], m18=s1(m16)+m[11]+s0(m[3])+m[2], m20=s1(m18)+m[13]+s0(m[5])+m[4];
    const uint32_t c17=m[10]+s0(m[2])+m[1], c19=m[12]+s0(m[4])+m[3], c21=m[14]+s0(m[6])+m[5], c22=s1(m20)+s0(m[7])+m[6];
    const uint32_t c23=m16+s0(m[8])+m[7], c24=s0(m[9])+m[8], c25=m18+s0(m[10])+m[9], c26=s0(m[11])+m[10];
    const uint32_t c27=m20+s0(m[12])+m[11], c28=s0(m[13])+m[12], c29=s0(m[14])+m[13], c30=m[14];
    int aborted=0;
    for(uint32_t base=0; base < (1u<<24); base+=LANES){
      uint32_t key[LANES];
      for(int j=0;j<LANES;j++){
        uint32_t x=base+(uint32_t)j;
        uint32_t w17=s1(x)+c17, w19=s1(w17)+c19, w21=s1(w19)+c21, w22=c22+x, w23=s1(w21)+c23, w24=s1(w22)+w17+c24;
        uint32_t w25=s1(w23)+c25, w26=s1(w24)+w19+c26, w27=s1(w25)+c27, w28=s1(w26)+w21+c28, w29=s1(w27)+w22+c29, w30=s1(w28)+w23+s0(x)+c30;
        uint32_t A=a,B=b,C=cc,D=d,E=e,F=f,G=gg,H=h,T1,T2;
#define RND(w,k) T1=H+BS1(E)+IF(E,F,G)+(k)+(w); T2=BS0(A)+MAJ(A,B,C); H=G; G=F; F=E; E=D+T1; D=C; C=B; B=A; A=T1+T2;
        RND(x,K[15]) RND(m16,K[16]) RND(w17,K[17]) RND(m18,K[18]) RND(w19,K[19]) RND(m20,K[20]) RND(w21,K[21]) RND(w22,K[22])
        RND(w23,K[23]) RND(w24,K[24]) RND(w25,K[25]) RND(w26,K[26]) RND(w27,K[27]) RND(w28,K[28]) RND(w29,K[29]) RND(w30,K[30])
        key[j]=IV[0]+A;
      }
      for(int j=0;j<LANES;j++){ uint32_t bi=key[j]>>8; if(bitmap[bi>>6]>>(bi&63)&1){ uint32_t mm[16]; memcpy(mm,m,60); mm[15]=base+(uint32_t)j;
          if(process_hit(tid,mm,&crs,0)){ uint64_t n=(g<<24)|(uint64_t)(base+(uint32_t)j); uint64_t cur=atomic_load(&best_n);
            while(n<cur && !atomic_compare_exchange_weak(&best_n,&cur,n)){}
            pthread_mutex_lock(&out_mu); fprintf(outf,"INDEX n=%llu group=%llu j=%u\n",(unsigned long long)n,(unsigned long long)g,base+(uint32_t)j); fflush(outf); pthread_mutex_unlock(&out_mu); } } }
      c->trials+=LANES;
      if((base & 0xfffff)==0){ uint64_t bb=atomic_load(&best_n); if(atomic_load(&stop_flag) || (bb!=UINT64_MAX && g > (bb>>24))){ aborted=1; break; } }
    }
    if(aborted) { c->overshoot++; break; }
  }
  atomic_fetch_sub(&live_threads,1);
  return NULL;
}
static void selftest(void){
  /* kernel check: compare fast key against compress31 for random blocks */
  uint64_t r2=7; for(int t=0;t<2000;t++){ uint32_t m[16]; for(int i=0;i<16;i++) m[i]=(uint32_t)sm(&r2);
    uint32_t a=IV[0],b=IV[1],cc=IV[2],d=IV[3],e=IV[4],f=IV[5],g=IV[6],h=IV[7];
    for(int s=0;s<15;s++){ uint32_t T1=h+BS1(e)+IF(e,f,g)+K[s]+m[s]; uint32_t T2=BS0(a)+MAJ(a,b,cc); h=g; g=f; f=e; e=d+T1; d=cc; cc=b; b=a; a=T1+T2; }
    const uint32_t m16=s1(m[14])+m[9]+s0(m[1])+m[0], m18=s1(m16)+m[11]+s0(m[3])+m[2], m20=s1(m18)+m[13]+s0(m[5])+m[4];
    const uint32_t c17=m[10]+s0(m[2])+m[1], c19=m[12]+s0(m[4])+m[3], c21=m[14]+s0(m[6])+m[5], c22=s1(m20)+s0(m[7])+m[6];
    const uint32_t c23=m16+s0(m[8])+m[7], c24=s0(m[9])+m[8], c25=m18+s0(m[10])+m[9], c26=s0(m[11])+m[10];
    const uint32_t c27=m20+s0(m[12])+m[11], c28=s0(m[13])+m[12], c29=s0(m[14])+m[13], c30=m[14];
    uint32_t x=m[15];
    uint32_t w17=s1(x)+c17, w19=s1(w17)+c19, w21=s1(w19)+c21, w22=c22+x, w23=s1(w21)+c23, w24=s1(w22)+w17+c24;
    uint32_t w25=s1(w23)+c25, w26=s1(w24)+w19+c26, w27=s1(w25)+c27, w28=s1(w26)+w21+c28, w29=s1(w27)+w22+c29, w30=s1(w28)+w23+s0(x)+c30;
    uint32_t A=a,B=b,C=cc,D=d,E=e,F=f,G=g,H=h,T1,T2;
    RND(x,K[15]) RND(m16,K[16]) RND(w17,K[17]) RND(m18,K[18]) RND(w19,K[19]) RND(m20,K[20]) RND(w21,K[21]) RND(w22,K[22])
    RND(w23,K[23]) RND(w24,K[24]) RND(w25,K[25]) RND(w26,K[26]) RND(w27,K[27]) RND(w28,K[28]) RND(w29,K[29]) RND(w30,K[30])
    uint32_t ref[8]; compress31(IV,m,ref); if(ref[0]!=IV[0]+A){fprintf(stderr,"KERNEL MISMATCH\n");exit(3);} }
  fprintf(stderr,"kernel check OK\n");
}

int main(int argc,char**argv){
  int nth=argc>1?atoi(argv[1]):1; time_limit=argc>2?atof(argv[2]):10; seed_base=argc>3?strtoull(argv[3],0,16):0x7231a5ed2026u;
  const char*outp=argc>4?argv[4]:"collisions.txt";
  outf=stderr; build_s1inv(); build_table(); selftest();
  if(time_limit<=0) return 0;
  outf=fopen(outp,"a");
  pthread_t th[64]; struct timespec t0,t1; clock_gettime(CLOCK_MONOTONIC,&t0);
  NTH=nth;
  for(int i=0;i<nth;i++) pthread_create(&th[i],0,worker,(void*)(intptr_t)i);
  double last=0;
  while(1){ sleep(1); clock_gettime(CLOCK_MONOTONIC,&t1); double el=(t1.tv_sec-t0.tv_sec)+(t1.tv_nsec-t0.tv_nsec)*1e-9;
    int fin = el>=time_limit || access("STOP",F_OK)==0 || (el>2 && atomic_load(&live_threads)==0);
    if(el-last>=30 || fin){ last=el; ctr_t s={0}; for(int i=0;i<nth;i++){ s.trials+=ctrs[i].trials; s.keyhits+=ctrs[i].keyhits; s.recs+=ctrs[i].recs; s.v6+=ctrs[i].v6; s.joint+=ctrs[i].joint; s.both+=ctrs[i].both; s.comp_try+=ctrs[i].comp_try; s.comp_ok+=ctrs[i].comp_ok; s.coll+=ctrs[i].coll; }
      printf("t=%.0f trials=%llu (2^%.3f) rate=%.3e/s keyhits=%llu rechits=%llu v6=%llu joint=%llu both=%llu comp=%llu/%llu coll=%llu\n",el,
        (unsigned long long)s.trials, s.trials? __builtin_log2((double)s.trials):0.0, s.trials/el,(unsigned long long)s.keyhits,(unsigned long long)s.recs,(unsigned long long)s.v6,(unsigned long long)s.joint,(unsigned long long)s.both,(unsigned long long)s.comp_ok,(unsigned long long)s.comp_try,(unsigned long long)s.coll);
      fflush(stdout); }
    if(fin) break; }
  atomic_store(&stop_flag,1); for(int i=0;i<nth;i++) pthread_join(th[i],0);
  ctr_t s={0}; for(int i=0;i<nth;i++){ s.trials+=ctrs[i].trials; s.keyhits+=ctrs[i].keyhits; s.recs+=ctrs[i].recs; s.v6+=ctrs[i].v6; s.joint+=ctrs[i].joint; s.both+=ctrs[i].both; s.comp_try+=ctrs[i].comp_try; s.comp_ok+=ctrs[i].comp_ok; s.coll+=ctrs[i].coll; }
  { uint64_t i13=0,i15=0,ov=0,bm=0,gr=0; for(int i=0;i<nth;i++){i13+=ctrs[i].it13; i15+=ctrs[i].it15; ov+=ctrs[i].overshoot; bm+=ctrs[i].bmhits; gr+=ctrs[i].groups;} uint64_t bn=atomic_load(&best_n);
    printf("DET best_n=%llu it13=%llu it15=%llu aborted_groups=%llu bitmap_hits=%llu groups=%llu\n",(unsigned long long)bn,(unsigned long long)i13,(unsigned long long)i15,(unsigned long long)ov,(unsigned long long)bm,(unsigned long long)gr);
    for(int i=0;i<nth;i++) printf("THREAD %d trials=%llu\n",i,(unsigned long long)ctrs[i].trials); }
  printf("FINAL trials=%llu keyhits=%llu rechits=%llu v6=%llu joint=%llu both=%llu comp=%llu/%llu coll=%llu\n",(unsigned long long)s.trials,(unsigned long long)s.keyhits,(unsigned long long)s.recs,(unsigned long long)s.v6,(unsigned long long)s.joint,(unsigned long long)s.both,(unsigned long long)s.comp_ok,(unsigned long long)s.comp_try,(unsigned long long)s.coll);
  return 0;
}
```

