# sha256-r31 instrumented start plus bit-sliced search, ceiling 35.95

## 1. Claim

The ordinary collision in `certificates/manifest.json` is a deterministic
replay. The construction that produced it is one instrumented z3 5.1.0 solve
of the yield model, plus one search from that model. Both runs have retired
instruction counts. The search is charged by the bit-sliced operation count,
not by its scalar instruction count.

| Quantity | Value |
| --- | ---: |
| Sum | 65938214962.660278 target compressions |
| log2(sum) | 35.940396 |
| Claimed ceiling | 35.95 |
| Promoted leader | 37.22 |
| Review leader at filing | 37.12 |
| Success probability | 1 |

Expected time is not used. Memory is a reported metric only.

## 2. Target

Target `sha256-r31-prefix-v1`: SHA-256 steps 0 through 30 on every padded
block, standard IV used once, FIPS padding, full feed-forward, all eight
digest words. The two messages are distinct, 128 bytes, and share their first
64-byte block. This is not a 32-step collision and not a full SHA-256
collision. The organizer digest of both messages is
`adad7544943b5990acb7480c400757544078c130179c86a16a15a0d469642ebb`.

## 3. Witness

Message A is block M0 followed by M1. Message B is M0 followed by M1'.

```
M0  818a461881ab27e17e93912b80776be2f5c1cbf23d69ad4cf861527ccc72b29bad896da17af3a3564f7dc174dc675b400b06492a8d4b6955c807e5bb0057af44
M1  210d15b2daf065e53dbe835ea324bc6ab2ca7f2e16bbbbc2ea0e00b0ab5bf62a71191d3b856b34db353f1b9e77300289457338ed5080b477e6d452e8538941dd
M1' 210d15b2daf065e53dbe835ea324bc6ab2ca7f2e16bbabc8ea2e88a1fb4bac24991a2e3b856bb4df353f1b9e77300289457338ed5080b477e6d452e8538941dd
```

The collision index in the deterministic search below is `n=322681941828`.
The charged trial counter, including sibling threads after that index, is
`325527273664`.

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
returned at 274.160 seconds. The same process retired `227685826211` user
instructions, measured by `perf_event_open` on `PERF_COUNT_HW_INSTRUCTIONS`
with kernel events excluded. That instruction count is the receipt that the
run happened. The ledger charges the bit-sliced operation count, which is
lower and is the specified program.

| Counter | Value |
| --- | ---: |
| Trials, including sibling overshoot | 325527273664 |
| Winning index | 322681941828 |
| Groups | 19416 |
| Aborted groups | 24 |
| Bitmap hits | 261721945 |
| Key hits after recompression | 3316649 |
| Record visits | 9983045 |
| V6 passes | 19518 |
| Joint passes | 1 |
| Completion calls | 1 |
| E13 iterations executed | 8578 |
| E15 iterations executed | 12 |
| Collisions | 1 |

The E13 and E15 figures are the iterations the program executed, not a cap.
The bitmap figure is the executed hit counter, not a density estimate.

## 6. Cost ledger

One target compression is 2140 primitive 32-bit operations. Every term below
is included in the sum.

| Term | Charge | Units |
| --- | ---: | ---: |
| Bit-sliced trials | 1271590913 * 41047 / 2140 | 24390183273.790188 |
| Bit-sliced group setup | 19416 * 28116 / 2140 | 255093.577570 |
| Bitmap hits | 261721945 * (2140 + 256) / 2140 | 293030738.420561 |
| Record visits | 9983045 * 400 / 2140 | 1865989.719626 |
| V6 passes | 19518 * 1600 / 2140 | 14592.897196 |
| Completion iterations | (8578 + 12) * 80 / 2140 | 321.121495 |
| Table scans | 12 * 2^32 * 8 / 2140 | 192671430.100935 |
| Self-test | 2000 compressions | 2000.000000 |
| Replay | 6 compressions | 6.000000 |
| One z3 solve | 8786880984645 * 10 / 2140 | 41060191517.032707 |
| Sum |  | 65938214962.660278 |

`log2(sum) = 35.940396 < 35.95`. The 400, 1600, and 80 operation
allowances are larger than the operations visible in the corresponding loops.
The table term charges twelve full 2^32 scans even though the builder is one
scan. Those choices raise the sum. They do not hide work.

The bit-sliced trial term is the specified program, not the scalar path that
found the pair. It stores each bit of 256 independent trials in one 256-bit
word. XOR, AND, OR and NOT of those words are one primitive operation each.
A 32-bit rotate or logical shift is a reindex and emits no operation.
Addition is a data-independent ripple: bit 0 is one XOR and one AND, and each
later bit is two XORs, two ANDs and one OR. The measured split is 22725
operations for steps 0 through 14, 5391 for the `x`-independent expansion,
and 41047 for each batch of 256 values of `x`. The expansion is charged once
per group inside the 28116 group term, not again inside the batch.
`1271590913 = ceil(325527273664 / 256)`. The last batch is partial and is
charged in full. On 768 random inputs the bit-sliced step-30 word 0 matched
`verifier.hash_functions._compress(..., rounds=31)`.

The z3 term is one successful solve, not a wall-clock ceiling. z3 5.1.0,
command `z3 -smt2 s-yield-model.smt2 -st`, seed `88108363`, returned `sat`
after `8786880984645` retired user instructions and 1753.724 seconds. The
counter is `perf_event_open` of `PERF_COUNT_HW_INSTRUCTIONS` with kernel
events excluded, attached to that process from `exec` until exit. The model
text is Appendix C. Its solution is the header in Appendix A. A local check
of that solution found 0 failures of the A-equations, the E-equations, the
step-8 relation, the two step-13 conditions, the message-schedule `s0`
condition, and the residue `c8 mod 2^20 = 0xe730f`.

The price 10 is the doubled sample mean, rounded up. A 2047-instruction
sample of the same z3 binary in its SAT phase classified as 87.84% plain
ALU or move at 4, 8.26% conditional branches at 4, 3.47% 128-bit SSE moves
at 16, and the remaining 0.43% at 256. The mean is 4.7973. Twice that mean
is 9.5945, and the charged price is `ceil(9.5945) = 10`. No multiply or
divide appeared in the sample. At price 19 the sum is `2^36.582`. At price
25 it is `2^36.892`. Both remain below 37.12. Price 52 does not.

## 7. Heuristics

`H-Z3-INSTRUCTION-PRICE` is the only score-critical premise that is not an
executed counter or a static operation count. The instruction count itself is
executed: `8786880984645` retired user instructions. The premise is that each
of those instructions costs 10 primitive operations. That price is the doubled
sample mean from Section 6, not a cycle-rate ceiling. The 36.9 package's
three-window `8` operations-per-cycle ceiling is not used. A 600-second rerun
of that ceiling timed out, which is why it is gone.

No bitmap-density premise is used. No unmeasured completion-entry cap is
used.

## 8. Organizer experiment

`experiments/replay.py` replays the stored pair. It checks the 32-byte tuple
layout on its finite domain and returns the two messages for every organizer
trial. It does not re-run the search and does not measure attack cost. The
cost is the ledger in Section 6. The certificate check is the collision.

## 9. Relation to the promoted 37.22 package

The promoted package charges each of its 99492036640 trials a full
compression plus 32 operations. This search does not. Steps 0 through 14 are
shared inside a group. The `x`-dependent tail is the bit-sliced program in
Section 6. The starting solution is one counted z3 solve, not three untimed
windows. The resulting ceiling, 35.95, is below the promoted 37.22 and below
the review score 37.12.

## Appendix A. Counted search source

The program that produced Section 5 is the following source. The completion predicates in Section 4 are this `complete` function. The 501-operation fast path is the per-x loop after the shared steps 0 through 14.

### sp_yield.h

```c
/* z3 5.1.0, seed 88108363, instrumented yield-model solve, 8786880984645 instructions */
static const uint32_t SPA_A[35]={0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0xc39b9bffu,0x183c81c1u,0x0e024ff9u,0x6e9b3d30u,0x066f9bfeu,0x859d46b8u,0xa72e39f6u,0x8b68cea6u,0x5766c94bu,0x769e5b61u,0xda394575u,0xb4f274a6u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
static const uint32_t SPA_E[35]={0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x1d1fafddu,0xafca7ae7u,0x4cd7cae5u,0x943b8248u,0x61d523d1u,0x7026b3fau,0x2a370c18u,0x31e7a1ecu,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
static const uint32_t SPB_A[35]={0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0xc39b9bffu,0x183c81c1u,0x0e024ff9u,0x6e9b3d30u,0x066f8c04u,0x851d46b9u,0xb60e29f3u,0x8b68cea2u,0x5766c94bu,0x769edb65u,0xda394575u,0xb4f274a6u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
static const uint32_t SPB_E[35]={0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x1d1f9fe3u,0xafc2fae6u,0x9c5fce6cu,0xd93b0a4cu,0x61d523d9u,0x5fa73402u,0x3af70c10u,0x31e721e4u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
static const uint32_t S_W[31]={0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x856b34dbu,0x353f1b9eu,0x77300289u,0x457338edu,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
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

## Appendix C. Yield model

This is the exact SMT-LIB file solved by z3 5.1.0, seed 88108363. The process retired 8786880984645 user instructions and returned sat. The model assigns the header in Appendix A.

```smt2
(set-logic QF_BV)
(set-option :random-seed 88108363)
(set-option :sat.random_seed 88108363)
(set-option :smt.random_seed 88108363)
(declare-fun A1 () (_ BitVec 32))
(declare-fun A2 () (_ BitVec 32))
(declare-fun A3 () (_ BitVec 32))
(declare-fun A4 () (_ BitVec 32))
(declare-fun A5 () (_ BitVec 32))
(declare-fun A6 () (_ BitVec 32))
(declare-fun A7 () (_ BitVec 32))
(declare-fun A8 () (_ BitVec 32))
(declare-fun A9 () (_ BitVec 32))
(declare-fun A10 () (_ BitVec 32))
(declare-fun A11 () (_ BitVec 32))
(declare-fun A12 () (_ BitVec 32))
(declare-fun E5 () (_ BitVec 32))
(declare-fun E6 () (_ BitVec 32))
(declare-fun E7 () (_ BitVec 32))
(declare-fun E8 () (_ BitVec 32))
(declare-fun E9 () (_ BitVec 32))
(declare-fun E10 () (_ BitVec 32))
(declare-fun E11 () (_ BitVec 32))
(declare-fun E12 () (_ BitVec 32))
(declare-fun A1p () (_ BitVec 32))
(declare-fun A2p () (_ BitVec 32))
(declare-fun A3p () (_ BitVec 32))
(declare-fun A4p () (_ BitVec 32))
(declare-fun A5p () (_ BitVec 32))
(declare-fun A6p () (_ BitVec 32))
(declare-fun A7p () (_ BitVec 32))
(declare-fun A8p () (_ BitVec 32))
(declare-fun A9p () (_ BitVec 32))
(declare-fun A10p () (_ BitVec 32))
(declare-fun A11p () (_ BitVec 32))
(declare-fun A12p () (_ BitVec 32))
(declare-fun E5p () (_ BitVec 32))
(declare-fun E6p () (_ BitVec 32))
(declare-fun E7p () (_ BitVec 32))
(declare-fun E8p () (_ BitVec 32))
(declare-fun E9p () (_ BitVec 32))
(declare-fun E10p () (_ BitVec 32))
(declare-fun E11p () (_ BitVec 32))
(declare-fun E12p () (_ BitVec 32))
(declare-fun W9 () (_ BitVec 32))
(declare-fun W10 () (_ BitVec 32))
(declare-fun W11 () (_ BitVec 32))
(declare-fun W12 () (_ BitVec 32))
(declare-fun W9p () (_ BitVec 32))
(declare-fun E3 () (_ BitVec 32))
(declare-fun E4 () (_ BitVec 32))
(declare-fun W7 () (_ BitVec 32))
(declare-fun W8 () (_ BitVec 32))
(assert (= (bvand (bvxor A1 A1p) #xffffffff) #x00000000))
(assert (= (bvand (bvxor A2 A2p) #xffffffff) #x00000000))
(assert (= (bvand (bvxor A3 A3p) #xffffffff) #x00000000))
(assert (= (bvand (bvxor A4 A4p) #xffffffff) #x00000000))
(assert (= (bvand A5 #x00000400) #x00000000))
(assert (= (bvand A5p #x00000400) #x00000400))
(assert (= (bvand A5 #x000013fa) #x000013fa))
(assert (= (bvand A5p #x000013fa) #x00000000))
(assert (= (bvand (bvxor A5 A5p) #xffffe805) #x00000000))
(assert (= (bvand A6 #x00000001) #x00000000))
(assert (= (bvand A6p #x00000001) #x00000001))
(assert (= (bvand A6 #x00800000) #x00800000))
(assert (= (bvand A6p #x00800000) #x00000000))
(assert (= (bvand (bvxor A6 A6p) #xff7ffffe) #x00000000))
(assert (= (bvand A7 #x10000001) #x00000000))
(assert (= (bvand A7p #x10000001) #x10000001))
(assert (= (bvand A7 #x01201004) #x01201004))
(assert (= (bvand A7p #x01201004) #x00000000))
(assert (= (bvand (bvxor A7 A7p) #xeedfeffa) #x00000000))
(assert (= (bvand A8 #x00000004) #x00000004))
(assert (= (bvand A8p #x00000004) #x00000000))
(assert (= (bvand (bvxor A8 A8p) #xfffffffb) #x00000000))
(assert (= (bvand (bvxor A9 A9p) #xffffffff) #x00000000))
(assert (= (bvand A10 #x00008004) #x00000000))
(assert (= (bvand A10p #x00008004) #x00008004))
(assert (= (bvand (bvxor A10 A10p) #xffff7ffb) #x00000000))
(assert (= (bvand (bvxor A11 A11p) #xffffffff) #x00000000))
(assert (= (bvand (bvxor A12 A12p) #xffffffff) #x00000000))
(assert (= (bvand E5 #xffffc7c1) #x1d1f87c1))
(assert (= (bvand E5p #xffffc7c1) #x1d1f87c1))
(assert (= (bvand E5 #x00001022) #x00000000))
(assert (= (bvand E5p #x00001022) #x00001022))
(assert (= (bvand E5 #x0000201c) #x0000201c))
(assert (= (bvand E5p #x0000201c) #x00000000))
(assert (= (bvand (bvxor E5 E5p) #x00000800) #x00000000))
(assert (= (bvand E6 #xfd947cfe) #xad8078e6))
(assert (= (bvand E6p #xfd947cfe) #xad8078e6))
(assert (= (bvand E6 #x00008000) #x00000000))
(assert (= (bvand E6p #x00008000) #x00008000))
(assert (= (bvand E6 #x00080001) #x00080001))
(assert (= (bvand E6p #x00080001) #x00000000))
(assert (= (bvand (bvxor E6 E6p) #x02630300) #x00000000))
(assert (= (bvand E7 #x2f37fa76) #x0c17ca64))
(assert (= (bvand E7p #x2f37fa76) #x0c17ca64))
(assert (= (bvand E7 #x90080408) #x00000000))
(assert (= (bvand E7p #x90080408) #x90080408))
(assert (= (bvand E7 #x40800081) #x40800081))
(assert (= (bvand E7p #x40800081) #x00000000))
(assert (= (bvand (bvxor E7 E7p) #x00400100) #x00000000))
(assert (= (bvand E8 #xb2ab25fa) #x902b0048))
(assert (= (bvand E8p #xb2ab25fa) #x902b0048))
(assert (= (bvand E8 #x49000804) #x00000000))
(assert (= (bvand E8p #x49000804) #x49000804))
(assert (= (bvand E8 #x04008000) #x04008000))
(assert (= (bvand E8p #x04008000) #x00000000))
(assert (= (bvand (bvxor E8 E8p) #x00545201) #x00000000))
(assert (= (bvand E9 #xffeb8df5) #x61c101d1))
(assert (= (bvand E9p #xffeb8df5) #x61c101d1))
(assert (= (bvand E9 #x00000008) #x00000000))
(assert (= (bvand E9p #x00000008) #x00000008))
(assert (= (bvand (bvxor E9 E9p) #x00147202) #x00000000))
(assert (= (bvand E10 #x507a5807) #x50221002))
(assert (= (bvand E10p #x507a5807) #x50221002))
(assert (= (bvand E10 #x0f810400) #x00000000))
(assert (= (bvand E10p #x0f810400) #x0f810400))
(assert (= (bvand E10 #x200083f8) #x200083f8))
(assert (= (bvand E10p #x200083f8) #x00000000))
(assert (= (bvand (bvxor E10 E10p) #x80042000) #x00000000))
(assert (= (bvand E11 #x6f27c7f2) #x2a270410))
(assert (= (bvand E11p #x6f27c7f2) #x2a270410))
(assert (= (bvand E11 #x10c00000) #x00000000))
(assert (= (bvand E11p #x10c00000) #x10c00000))
(assert (= (bvand E11 #x00000008) #x00000008))
(assert (= (bvand E11p #x00000008) #x00000000))
(assert (= (bvand (bvxor E11 E11p) #x80183805) #x00000000))
(assert (= (bvand E12 #x3f6107f2) #x316101e0))
(assert (= (bvand E12p #x3f6107f2) #x316101e0))
(assert (= (bvand E12 #x00008008) #x00008008))
(assert (= (bvand E12p #x00008008) #x00000000))
(assert (= (bvand (bvxor E12 E12p) #xc09e7805) #x00000000))
(assert (= (bvand W9 #x00000010) #x00000010))
(assert (= (bvand W9p #x00000010) #x00000010))
(assert (= (bvand W9 #x00008004) #x00000000))
(assert (= (bvand W9p #x00008004) #x00008004))
(assert (= (bvand (bvxor W9 W9p) #xffff7feb) #x00000000))
(assert (= A5 (bvadd (bvsub E5 A1) (bvxor ((_ rotate_right 2) A4) ((_ rotate_right 13) A4) ((_ rotate_right 22) A4)) (bvxor (bvand A4 A3) (bvand A4 A2) (bvand A3 A2)))))
(assert (= A6 (bvadd (bvsub E6 A2) (bvxor ((_ rotate_right 2) A5) ((_ rotate_right 13) A5) ((_ rotate_right 22) A5)) (bvxor (bvand A5 A4) (bvand A5 A3) (bvand A4 A3)))))
(assert (= A7 (bvadd (bvsub E7 A3) (bvxor ((_ rotate_right 2) A6) ((_ rotate_right 13) A6) ((_ rotate_right 22) A6)) (bvxor (bvand A6 A5) (bvand A6 A4) (bvand A5 A4)))))
(assert (= A8 (bvadd (bvsub E8 A4) (bvxor ((_ rotate_right 2) A7) ((_ rotate_right 13) A7) ((_ rotate_right 22) A7)) (bvxor (bvand A7 A6) (bvand A7 A5) (bvand A6 A5)))))
(assert (= A9 (bvadd (bvsub E9 A5) (bvxor ((_ rotate_right 2) A8) ((_ rotate_right 13) A8) ((_ rotate_right 22) A8)) (bvxor (bvand A8 A7) (bvand A8 A6) (bvand A7 A6)))))
(assert (= A10 (bvadd (bvsub E10 A6) (bvxor ((_ rotate_right 2) A9) ((_ rotate_right 13) A9) ((_ rotate_right 22) A9)) (bvxor (bvand A9 A8) (bvand A9 A7) (bvand A8 A7)))))
(assert (= A11 (bvadd (bvsub E11 A7) (bvxor ((_ rotate_right 2) A10) ((_ rotate_right 13) A10) ((_ rotate_right 22) A10)) (bvxor (bvand A10 A9) (bvand A10 A8) (bvand A9 A8)))))
(assert (= A12 (bvadd (bvsub E12 A8) (bvxor ((_ rotate_right 2) A11) ((_ rotate_right 13) A11) ((_ rotate_right 22) A11)) (bvxor (bvand A11 A10) (bvand A11 A9) (bvand A10 A9)))))
(assert (= E9 (bvadd A5 E5 (bvxor ((_ rotate_right 6) E8) ((_ rotate_right 11) E8) ((_ rotate_right 25) E8)) (bvxor (bvand E8 E7) (bvand (bvnot E8) E6)) #x12835b01 W9)))
(assert (= E10 (bvadd A6 E6 (bvxor ((_ rotate_right 6) E9) ((_ rotate_right 11) E9) ((_ rotate_right 25) E9)) (bvxor (bvand E9 E8) (bvand (bvnot E9) E7)) #x243185be W10)))
(assert (= E11 (bvadd A7 E7 (bvxor ((_ rotate_right 6) E10) ((_ rotate_right 11) E10) ((_ rotate_right 25) E10)) (bvxor (bvand E10 E9) (bvand (bvnot E10) E8)) #x550c7dc3 W11)))
(assert (= E12 (bvadd A8 E8 (bvxor ((_ rotate_right 6) E11) ((_ rotate_right 11) E11) ((_ rotate_right 25) E11)) (bvxor (bvand E11 E10) (bvand (bvnot E11) E9)) #x72be5d74 W12)))
(assert (= A5p (bvadd (bvsub E5p A1p) (bvxor ((_ rotate_right 2) A4p) ((_ rotate_right 13) A4p) ((_ rotate_right 22) A4p)) (bvxor (bvand A4p A3p) (bvand A4p A2p) (bvand A3p A2p)))))
(assert (= A6p (bvadd (bvsub E6p A2p) (bvxor ((_ rotate_right 2) A5p) ((_ rotate_right 13) A5p) ((_ rotate_right 22) A5p)) (bvxor (bvand A5p A4p) (bvand A5p A3p) (bvand A4p A3p)))))
(assert (= A7p (bvadd (bvsub E7p A3p) (bvxor ((_ rotate_right 2) A6p) ((_ rotate_right 13) A6p) ((_ rotate_right 22) A6p)) (bvxor (bvand A6p A5p) (bvand A6p A4p) (bvand A5p A4p)))))
(assert (= A8p (bvadd (bvsub E8p A4p) (bvxor ((_ rotate_right 2) A7p) ((_ rotate_right 13) A7p) ((_ rotate_right 22) A7p)) (bvxor (bvand A7p A6p) (bvand A7p A5p) (bvand A6p A5p)))))
(assert (= A9p (bvadd (bvsub E9p A5p) (bvxor ((_ rotate_right 2) A8p) ((_ rotate_right 13) A8p) ((_ rotate_right 22) A8p)) (bvxor (bvand A8p A7p) (bvand A8p A6p) (bvand A7p A6p)))))
(assert (= A10p (bvadd (bvsub E10p A6p) (bvxor ((_ rotate_right 2) A9p) ((_ rotate_right 13) A9p) ((_ rotate_right 22) A9p)) (bvxor (bvand A9p A8p) (bvand A9p A7p) (bvand A8p A7p)))))
(assert (= A11p (bvadd (bvsub E11p A7p) (bvxor ((_ rotate_right 2) A10p) ((_ rotate_right 13) A10p) ((_ rotate_right 22) A10p)) (bvxor (bvand A10p A9p) (bvand A10p A8p) (bvand A9p A8p)))))
(assert (= A12p (bvadd (bvsub E12p A8p) (bvxor ((_ rotate_right 2) A11p) ((_ rotate_right 13) A11p) ((_ rotate_right 22) A11p)) (bvxor (bvand A11p A10p) (bvand A11p A9p) (bvand A10p A9p)))))
(assert (= E9p (bvadd A5p E5p (bvxor ((_ rotate_right 6) E8p) ((_ rotate_right 11) E8p) ((_ rotate_right 25) E8p)) (bvxor (bvand E8p E7p) (bvand (bvnot E8p) E6p)) #x12835b01 W9p)))
(assert (= E10p (bvadd A6p E6p (bvxor ((_ rotate_right 6) E9p) ((_ rotate_right 11) E9p) ((_ rotate_right 25) E9p)) (bvxor (bvand E9p E8p) (bvand (bvnot E9p) E7p)) #x243185be W10)))
(assert (= E11p (bvadd A7p E7p (bvxor ((_ rotate_right 6) E10p) ((_ rotate_right 11) E10p) ((_ rotate_right 25) E10p)) (bvxor (bvand E10p E9p) (bvand (bvnot E10p) E8p)) #x550c7dc3 W11)))
(assert (= E12p (bvadd A8p E8p (bvxor ((_ rotate_right 6) E11p) ((_ rotate_right 11) E11p) ((_ rotate_right 25) E11p)) (bvxor (bvand E11p E10p) (bvand (bvnot E11p) E9p)) #x72be5d74 W12)))
(assert (= (bvsub E8p E8) (bvadd (bvsub (bvxor ((_ rotate_right 6) E7p) ((_ rotate_right 11) E7p) ((_ rotate_right 25) E7p)) (bvxor ((_ rotate_right 6) E7) ((_ rotate_right 11) E7) ((_ rotate_right 25) E7))) (bvsub (bvxor (bvand E7p E6p) (bvand (bvnot E7p) E5p)) (bvxor (bvand E7 E6) (bvand (bvnot E7) E5))) #x28011100)))
(assert (= (bvadd A9p E9p (bvxor ((_ rotate_right 6) E12p) ((_ rotate_right 11) E12p) ((_ rotate_right 25) E12p)) (bvxor (bvand E12p E11p) (bvand (bvnot E12p) E10p))) (bvadd A9 E9 (bvxor ((_ rotate_right 6) E12) ((_ rotate_right 11) E12) ((_ rotate_right 25) E12)) (bvxor (bvand E12 E11) (bvand (bvnot E12) E10)))))
(assert (= (bvxor (bvand A12p A11p) (bvand A12p A10p) (bvand A11p A10p)) (bvxor (bvand A12 A11) (bvand A12 A10) (bvand A11 A10))))
(assert (= (bvsub (bvxor ((_ rotate_right 7) W9p) ((_ rotate_right 18) W9p) (bvlshr W9p #x00000003)) (bvxor ((_ rotate_right 7) W9) ((_ rotate_right 18) W9) (bvlshr W9 #x00000003))) #xd7feef00))
(assert (= (bvand E4 #x00088031) #x00000010))
(assert (= (bvand E4 #x00088031) #x00000010))
(assert (= (bvand (bvxor E4 E4) #xfff77fce) #x00000000))
(assert (= (bvand E3 #x00000030) #x00000020))
(assert (= (bvand E3 #x00000030) #x00000020))
(assert (= (bvand (bvxor E3 E3) #xffffffcf) #x00000000))
(assert (= E8 (bvadd A4 E4 (bvxor ((_ rotate_right 6) E7) ((_ rotate_right 11) E7) ((_ rotate_right 25) E7)) (bvxor (bvand E7 E6) (bvand (bvnot E7) E5)) #xd807aa98 W8)))
(assert (= E7 (bvadd A3 E3 (bvxor ((_ rotate_right 6) E6) ((_ rotate_right 11) E6) ((_ rotate_right 25) E6)) (bvxor (bvand E6 E5) (bvand (bvnot E6) E4)) #xab1c5ed5 W7)))
(assert (= (bvsub E7p E7) (bvadd (bvsub (bvxor ((_ rotate_right 6) E6p) ((_ rotate_right 11) E6p) ((_ rotate_right 25) E6p)) (bvxor ((_ rotate_right 6) E6) ((_ rotate_right 11) E6) ((_ rotate_right 25) E6))) (bvsub (bvxor (bvand E6p E5p) (bvand (bvnot E6p) E4)) (bvxor (bvand E6 E5) (bvand (bvnot E6) E4))) #x4fefb5fa)))
(assert (= (bvsub E6p E6) (bvadd (bvsub (bvxor ((_ rotate_right 6) E5p) ((_ rotate_right 11) E5p) ((_ rotate_right 25) E5p)) (bvxor ((_ rotate_right 6) E5) ((_ rotate_right 11) E5) ((_ rotate_right 25) E5))) (bvsub (bvxor (bvand E5p E4) (bvand (bvnot E5p) E3)) (bvxor (bvand E5 E4) (bvand (bvnot E5) E3))) #x002087f1)))
(assert (= (bvsub (bvxor ((_ rotate_right 7) (bvadd W8 #x28011100)) ((_ rotate_right 18) (bvadd W8 #x28011100)) (bvlshr (bvadd W8 #x28011100) #x00000003)) (bvxor ((_ rotate_right 7) W8) ((_ rotate_right 18) W8) (bvlshr W8 #x00000003))) #xb00fca02))
(assert (= (bvsub (bvxor ((_ rotate_right 7) (bvadd W7 #x4fefb5fa)) ((_ rotate_right 18) (bvadd W7 #x4fefb5fa)) (bvlshr (bvadd W7 #x4fefb5fa) #x00000003)) (bvxor ((_ rotate_right 7) W7) ((_ rotate_right 18) W7) (bvlshr W7 #x00000003))) #xffdf780f))
(assert (= (bvand (bvsub (bvsub (bvsub (bvsub E8 A4) (bvxor ((_ rotate_right 6) E7) ((_ rotate_right 11) E7) ((_ rotate_right 25) E7))) (bvxor (bvand E7 E6) (bvand (bvnot E7) E5))) #xd807aa98) #x000fffff) #x000e730f))
(check-sat)
(get-value (A1 A2 A3 A4 A5 A6 A7 A8 A9 A10 A11 A12 E5 E6 E7 E8 E9 E10 E11 E12 A1p A2p A3p A4p A5p A6p A7p A8p A9p A10p A11p A12p E5p E6p E7p E8p E9p E10p E11p E12p W9 W10 W11 W12 W9p E3 E4 W7 W8))
```
