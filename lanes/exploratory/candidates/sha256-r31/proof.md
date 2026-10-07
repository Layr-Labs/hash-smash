# sha256-r31 ordinary collision, bit-blast start, scalar search

## 1. Target

The target is `sha256-r31-prefix-v1`: an ordinary collision of SHA-256 reduced to steps 0 through 30, standard IV, FIPS padding, two distinct messages, all eight digest words. The cost model is `collision-frontier-v5`. One target compression costs `C = 2140` primitive operations. Lower is better. The scored program replays one stored pair, so its success probability is 1. This package claims no 32-round collision and no full SHA-256 collision.

The promoted leader at filing is 37.22. Submission `78c1cb18` claimed 35.95 and was `not_evaluable`. This package replaces the two score-critical gaps in that dossier. It does not resubmit that archive.

## 2. Witness

The certificate messages are 128 bytes each and differ. The organizer digest of both at 31 rounds is

`05ceaa5281d83e73a8bad643e2d048a450612b5408a8a14b0f395631dc2afb26`.

The same function returns unequal digests at 32 rounds and at 64 rounds. The search printed that 31-round digest before this proof was written. `experiments/replay.py` transports this pair and no other.

## 3. What 78c1cb18 got wrong

Workflow `37664299269` returned `not_evaluable`. Three material gaps:

- `F-Z3-PRICE-NOT-UPPER-BOUND`: a 2047-instruction sample did not show that price 10 bounds every instruction of an 8.8-trillion-instruction solve, and kernel instructions were excluded. The margin was 0.107 operations per instruction.
- `F-BITSLICE-COST-NOT-AUDITABLE`: the ledger charged a 256-lane program that was not in the archive. The witness came from a scalar loop.
- `F-PEAK-MEMORY-UNMEASURED`: no peak accounting for z3 or the threaded search.

This package drops the bitslice claim. The charged search is the scalar eight-lane loop in Appendix A, which produced the witness. The z3 term is one 1.63-second bit-blast, not the 1753-second default tactic, and every instruction is charged at a uniform cap with a second full count for the kernel. Section 7 accounts for memory from the measured z3 RSS and the source allocations.

## 4. Construction

The only external input is the public 31-step characteristic of Li, Liu, Wang, Dong and Sun, as conditions in Appendix C. No published colliding pair is an input.

The starting solution is one model of that file. The charged command is z3 5.1.0 with

`(check-sat-using (then simplify bit-blast sat))`.

The same command returned the same `A1 = 0x7be1d812` on two runs. Appendix B is that model. Building the neutral-bit table from the header, which is `build_table` in Appendix A, prints `records=132096`. That is the table the search uses. It is not the 73728-record header of the rejected package.

The collision search is the scalar loop in Appendix A. It was compiled from that source and the header, then run once with seed `bb310001` and 28 threads. It stopped when the first collision was written. The final counter includes overshoot past `best_n`. Charging the final counter is the conservative choice.

| Counter | Value |
| --- | ---: |
| trials | 98721333376 |
| groups | 5894 |
| bitmap hits | 35961866 |
| record visits | 3034263 |
| V6 passes | 5935 |
| step-13 iterations | 2473 |
| step-15 iterations | 14 |
| completions | 1 |
| collisions | 1 |
| best index | 93045013307 |

## 5. Ledger

Every row is an executed counter or a static count of the archived source. There is no expected-time term and no density estimate.

| Term | Formula | Target compressions |
| --- | --- | ---: |
| Scalar trials | 98721333376 * 960 / 2140 | 44286205626.616821 |
| Bit-blast | 2 * 7221526979 * 1024 / 2140 | 6911068809.809346 |
| Table scans | 12 * 2^32 * 16 / 2140 | 385342860.201869 |
| Hit path | see below | 1360668.048598 |
| Group setup and self-test | 5894 * 2000 / 2140 + 4000 | 9508.411215 |
| Sum |  | 51583987473.087852 |

`log2(51583987473.087852) = 35.586204`. The claimed ceiling is 36.6. `2^36.6 = 104159249330.681198`, which is strictly above the sum.

The per-trial 960 is not a sample. From the fast path in Appendix A:

- schedule `s0`/`s1` and adds: 78 arithmetic operations
- 16 `RND` expansions: 16 * 26 = 416 arithmetic operations, plus 6 register moves per round
- key add: 1
- expanded load/store reading, one load per operand and one store per result, plus the bitmap test: 918 operations in total
- 960 charges that 918 and leaves 42 operations for address arithmetic the expansion does not name

A reviewer who counts only the 495 arithmetic operations will get a lower term. The ledger does not use that lower number.

The hit-path row charges executed counters, not a rate:

- 35961866 bitmap hits * 64
- 3034263 record visits * 200
- 5935 V6 passes * 500
- 1 completion * 200000
- 2473 step-13 iterations * 100
- 14 step-15 iterations * 200

The table row charges twelve full 32-bit scans at 16 operations each. The builder in Appendix A is one scan that fills V7, V8, and G16. Twelve scans are an allowance, not a measurement of extra work.

The group-setup row charges 2000 operations for each of the 5894 groups, plus 4000 for the self-test. The source's group setup is the 15-step message expansion before the trial loop. 2000 is an allowance above that expansion.

## 6. Bit-blast price

Appendix D records the process:

| Field | Value |
| --- | --- |
| z3 | 5.1.0 |
| user instructions | 7221526979 |
| kernel counter | excluded by the event attribute |
| max RSS | 61240 KB |
| user time | 1.633648 s |
| system time | 0.054653 s |

The price is 1024 primitive operations per instruction. That is the maximum per-form price in the promoted r31 filing `50592e75` (integer divide). It is applied to every retired user instruction. It is not a mean of a sample. The kernel counter was excluded, so the formula charges a second copy of the same count. System time was 3.3 percent of user time, so the second copy is larger than the kernel time ratio.

This term is the only conversion from machine instructions to word-RAM operations. It is score-critical in the sense that the construction must be charged. It is not score-critical for the ceiling 36.6, because the ceiling stays above the sum under the substitutions in Section 8.

## 7. Memory

Memory is a reported metric. It is not in the time sum.

The bit-blast process was measured at 61240 KB maximum resident set, which is 62697472 bytes.

The search allocations in Appendix A are:

- `recs`: `sizeof(rec_t) * 2^20`. `rec_t` is six 32-bit words, so the allocation is 24 MiB. The run stored 132096 records.
- `bitmap`: `2^18` eight-byte words, 2 MiB.
- V7 and V8 in `build_table`: 1024 and 65536 words.
- 28 POSIX threads. The default stack is 8 MiB, so 224 MiB.

The two phases are sequential. The search bound is 24 + 2 + 224 = 250 MiB, plus the small stack arrays. `2^30` bytes is 1024 MiB and covers both the measured z3 RSS and the search bound. The claim uses `memory_log2_bytes = 30`.

## 8. Why 36.6 survives the rejected substitutions

The rejected 35.95 claim had 0.107 operations of margin per z3 instruction. This ceiling is set above the hostile substitution, not above the ledger by a fraction.

| Substitution | log2 of the recomputed sum |
| --- | ---: |
| Ledger: 960 operations/trial, price 1024, kernel doubled | 35.586204 |
| Price 4096, same trial allowance | 36.0736 |
| 1600 operations/trial, price 1024 | 36.2391 |
| Both: 1600 operations/trial and price 4096, kernel still doubled | 36.567532 |

`36.567532 < 36.6`. A reviewer who raises the uniform price from 1024 to 4096 and the per-trial allowance from 960 to 1600 at the same time does not cross the claimed ceiling. A substitution past both of those bounds is a different claim and is not asserted here.

Dropping the bit-blast term would lower the sum. The failure mode that remains is a refusal of every instruction conversion, including the conversion in the promoted filing this cap cites. The scalar source, the trial counter, and the witness do not depend on that conversion.

## 9. What is not charged as a probability

The organizer experiment replays the stored pair. It does not rerun the search and does not support a success-probability inference. The probability claim is 1 because the scored program is that replay.

No published collision is read. The characteristic is a condition table. The bit-blast model contains those conditions and the yield residue `0xe730f`.

## 10. Credit

The characteristic and the step-20 cancellation framework come from the ASIACRYPT 2024 31-step SHA-256 attack and the restatement in ePrint 2026/1080. The uniform instruction-cap idea follows the per-form table in promoted filing `50592e75`, but the cap here is the table maximum applied to every instruction, not that filing's measured mean. The bit-blast tactic, the header, the seed `bb310001`, the trial counter, and the pair are from this run.

## 11. Next step

Do not resubmit this package unchanged. If the uniform cap is rejected outright, replace the bit-blast term with a word-RAM solver whose operation counter is in the archive. Do not return to price 10, to a 2047-instruction sample, or to a bitslice that is not the witness-producing source.

## Appendix A. Charged search source

The program below is the witness-producing search. It is included here because the candidate layout admits no auxiliary directory.

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
#include "sp_bb.h"

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

## Appendix B. Starting solution header

```c
/* z3 5.1.0 check-sat-using (then simplify bit-blast sat), seed 88108363 */
static const uint32_t SPA_A[35]={0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x7be1d812u,0x0d6243c7u,0x528a89fcu,0xe02e7b31u,0xf9d073ffu,0xb0f7e0b8u,0xe1be51f4u,0xf4d7011du,0x82c600bau,0xdd683113u,0xfc4793afu,0xd50183adu,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
static const uint32_t SPA_E[35]={0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x1d1fa7ddu,0xad8b7ae7u,0x4cd7cae5u,0x947fc049u,0x61c121d1u,0xf02293fau,0x2a3f3c18u,0x7171b9e9u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
static const uint32_t SPB_A[35]={0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x7be1d812u,0x0d6243c7u,0x528a89fcu,0xe02e7b31u,0xf9d06405u,0xb077e0b9u,0xf09e41f1u,0xf4d70119u,0x82c600bau,0xdd68b117u,0xfc4793afu,0xd50183adu,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
static const uint32_t SPB_E[35]={0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x1d1f97e3u,0xad83fae6u,0x9c5fce6cu,0xd97f484du,0x61c121d9u,0xdfa31402u,0x3aff3c10u,0x717139e1u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
static const uint32_t S_W[31]={0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0xf9f25bdau,0xc1da1425u,0xbc67ec46u,0x1746d234u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};

```

## Appendix C. Bit-blast model

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
(check-sat-using (then simplify bit-blast sat))
(get-value (A1 A2 A3 A4 A5 A6 A7 A8 A9 A10 A11 A12 E5 E6 E7 E8 E9 E10 E11 E12 A1p A2p A3p A4p A5p A6p A7p A8p A9p A10p A11p A12p E5p E6p E7p E8p E9p E10p E11p E12p W9 W10 W11 W12 W9p E3 E4 W7 W8))

```

## Appendix D. Instruction receipt

```text
z3 5.1.0
command: z3 -smt2 search/bitblast-model.smt2
tactic: (check-sat-using (then simplify bit-blast sat))
user_instructions: 7221526979
kernel_counter: excluded
maxrss_kb: 61240
utime_sec: 1.633648
stime_sec: 0.054653
child_status: 0
model_A1: 7be1d812
repeated: same A1 on the prior 0.898 s run

```
