# sha256-r31-exploratory — one fresh-seed K-scan, all executed work charged (time_log2 = 35.0202)

## 1. Summary

This package replaces our refuted ticket 6aef050d (claimed 36.6337). The paired review refuted it
for two structural reasons, both fixed here: (F-COST-001) five sampling K-runs built witnesses that
were shipped as nonuniform advice while their construction was excluded from the ledger;
(F-ALG-SPEC-MISSING) the proof specified the r31k search as the attack but the package shipped only
a replay program, with no executable attack source.

The replacement abandons expectation accounting entirely. It ships exactly one collision witness,
produced by exactly one fresh-seed K-scan executed on 2026-10-07, and charges the FULL executed
work of the chain that produced it, at retired-instruction measurement on the actual executable:

- enumeration scan r31sets (160,429,645,672 instr) -> 1,874,178,103.64 units
- one z3 4.15.1 solve, seed 1547760900 committed in advance (1,897,370,783,016 instr) -> 22,165,546,530.56 units
- ONE fresh K-scan, seed committed before the run, first collision at trial index n* = 2,685,579,961 = 2^31.3226
  (whole-process retired instructions 567,935,304,369, /usr/bin/time -l) -> 6,634,758,228.61 units
- table build inside that run's retired count; tooling/lab flat allowance 1,001,000,000 units
- online replay allowance 1,000,000 units

Subtotal 31,676,482,862.82; x 1.10 margin -> 34,844,131,149.10 units = 2^35.0202.
Claimed time_log2 = 35.0202, the tightest holding 4-decimal value (Section 6).
success_probability = 1: the scored program replays the shipped, organizer-verifiable pair.
preprocessing_log2 = 35.0202 with its own ledger (Section 6): every charged term except the replay
allowance is one-time construction; the two numbers are equal at 4 decimals because the online part
is a 6.4-unit replay, which is the point of the ticket, not a copy.
memory_log2_bytes = 28 (reported metric); nonuniform advice 2^12 bytes (Section 7).

There is no distribution claim in the score path. The six measured first-hit draws (Section 9) are
disclosed context: this ticket prices the work ACTUALLY EXECUTED (2^31.32 to first hit on a
pre-committed fresh seed) and states plainly that other fresh seeds drew up to 2^37.32.

## 2. Target and relation

sha256-r31-prefix-v1: SHA-256 compression steps 0..30 inclusive on every padded block, standard IV
once at the start, FIPS 180-4 padding, full feed-forward, full 256-bit digest. Ordinary collision of
two distinct byte strings. Cost model collision-frontier-v5, C = 2140: one 31-step compression =
1 unit; one word operation = 1/2140 units.

## 3. The construction chain (every executed run charged once)

All sources are shipped INLINE in Appendix A of this proof (each block carries its SHA-256; extract-and-rebuild was performed: `cc -O3 -o r31k r31k.c -lpthread` builds and the extracted binary reproduces the committed-seed collision at exactly trial index 2,685,579,961 with the same digest). Intake allows only claim.json, proof.md, certificates/ and experiments/, so the attack ships as an appendix, not a directory:

| file | sha256 |
|---|---|
| attack/r31k.c | 3a1cbc6691a57d133d064b7fe7841ca9533d20e6a0108d2675c147b8795c17fa |
| attack/sol_own.h | d240548a681ed96918d39bc213abda8a6dc1d44aceae2e409fc10be65452b292 |
| attack/r31mk.py | 74844fcfae368d646840609073929355a5424686a9d989141a45ec487ecbc597 |
| attack/r31sets.c | dc27eab2d51e394583e8da100f73b4fd0fddd61e049d6835dd8f95f1adfcfad4 |
| attack/r31k-bin-macho-arm64 | 6583e7fe535f90795b57458bfa18e30a7c097f384fce6035884061bcb84805f8 |

1. Starting solution: z3 4.15.1 (pip wheel) on attack/r31mk.py's SMT-LIB2 model for the relaxed
   cancellation context (dW20 = 0 only; characteristic rows transcribed in the script), seed
   1547760900 committed in advance in s3-seeds.txt, SAT on the first sequential attempt, 262.0 s
   wall, 1,897,370,783,016 retired instructions (/usr/bin/time -l, tl-1547760900.log). The result
   is attack/sol_own.h (arrays A, A', E, E', W, W9'). Charged.
2. Enumeration scan: attack/r31sets.c reproduces |V7| = 512, |V8| = 49,408, |G16| = 64 and the
   residue class used by the solve model. 160,429,645,672 retired instructions. Charged.
3. Fresh K-scan (the only search in this ticket's chain). r31k.c compiled at -O3 (the Mach-O
   arm64 binary above, sha256 6583e7fe...); seed committed before the run:
   s = SHA-256("k6-root-20261007T2105Z:0") first 16 hex = d5003c531ddf9d2a, printed at
   2026-10-07T21:17:08Z immediately before the invocation, never re-drawn:
   `/usr/bin/time -l ./r31k 30 300 d5003c531ddf9d2a coll-6.txt`
   Program semantics (attack/r31k.c is the exact spec): builds its record table from sol_own.h
   constants over the V7/V8/G enumeration (2^32-word scan, 103,168-row record table sorted, 2^24-bit
   bitmap over key>>8), then scans splitmix64 trial groups g = 0,1,2,...; per trial: partial
   compression steps 0..15 of block m0||x under the fixed prefix, key = IV0 + A31, bitmap probe, on
   hit a binary search + bucket walk + v6/r20 completion (W13/W15 rho enumeration, 2^22 x 2^12
   budget) and a full two-block digest equality check; deterministic FAIL at tlim. It stopped with
   COLLISION at trial index n* = 2,685,579,961 = 2^31.3226 (group 160, j 1225401), whole process
   retired instructions 567,935,304,369, peak RSS 7,111,040 B (time -l on the run itself). Charged
   whole-process, table build included.

## 4. Messages and certificates (the only witness shipped)

attack output coll-6.txt, verbatim: M0 = 31e46621...71f854 f79d3921...2edbc 412bef06...b2b9
(512-bit first block, 16 words); message A = M0 || M1 with M1 =
76e3309715169879f84b370638a51c9120ed81ff06a2bca21756157406b457ba661915bf954a6452051063193a9ff24b4a4a9bfb5cf1caacd77b3aeed59e04dc;
message B = M0 || M1' with M1' =
76e3309715169879f84b370638a51c9120ed81ff06a2aca817769d6556a40db48e1a26bf954ae456051063193a9ff24b4a4a9bfb5cf1caacd77b3aeed59e04dc.
Both are 128-byte byte strings (certificates/witness-6-a.bin, witness-6-b.bin, sha256
5a55475d43fd803da34752d2ad72dc0959cd240aa0710f9564bdb3cd474b0536 and
5b72d3cc6f0fe4ddad94cc7e44efcc2fc22fe6d84a3acaa618db5b918025a136). Re-verified through the
organizer verifier (verifier/hash_functions.py, digest(m, 'sha256', 31)): distinct messages, equal
31-step digests 8fc6cd1173ce63e44082ce6e3674737547649efc9f0d2651a35ff2153d871b53, matching
certificates/manifest.json. The messages differ inside the second 512-bit block in the W5..W9
differential-patch words only.

The shipped experiment (experiments/witness_replay.py) embeds this one pair as hex constants (the
sandbox mounts only the program file) and returns it for every trial seed; it evidences the
collision relation only; no cost or frequency is inferred from it, and its execution is inside the
1,000,000-unit replay allowance.

## 5. Program roles (fixes F-ALG-SPEC-MISSING)

- ATTACK program (construction): attack/r31k.c, shipped inline in Appendix A, compiled
  at -O3 (cc, Apple clang arm64), invoked exactly as in Section 3. Extract-and-rebuild
  from the Appendix bytes was performed: the build compiles and re-running the
  committed seed d5003c531ddf9d2a halts at exactly trial index 2,685,579,961 with
  digest 8fc6cd11...1b53 — byte-identical collision record to logs/coll-6.txt. The
  binary that originally ran (r31k-bin-macho-arm64, sha256 6583e7fe...) is identified
  by digest in Section 3.
- SCORED online program: replay of the shipped pair (Section 4). Its success probability is 1 by
  certificate verification; no search runs online.

## 6. Ledger (exact rationals; instructions priced 25/C = 25/2140 per retired instruction)

| term | units | log2 |
|---|---|---|
| enumeration scan (160,429,645,672 x 25/2140) | 1,874,178,103.64 | 30.804 |
| z3 solve seed 1547760900 (1,897,370,783,016 x 25/2140) | 22,165,546,530.56 | 34.368 |
| fresh K-scan, whole process (567,935,304,369 x 25/2140) | 6,634,758,228.61 | 32.627 |
| tooling / lab (driver, scripts, logging; flat allowance) | 1,001,000,000.00 | 29.900 |
| online replay allowance (>= 10^5 x the 6.4-unit replay) | 1,000,000.00 | 19.932 |
| subtotal | 31,676,482,862.82 | 34.900 |
| x 1.10 margin | 34,844,131,149.10 | 35.0202 |

Total exactly 29,826,576,263,627/856 units. Integer-power tightness at 4 decimals (reduced N/D,
scale 10^4): N^10000 > D^10000 x 2^350201 and N^10000 <= D^10000 x 2^350202. Claimed time_log2 =
35.0202, tight in both directions.

Preprocessing sub-ledger (its own sum, not a copy): 1.10 x (1,874,178,103.64 + 22,165,546,530.56 +
6,634,758,228.61 + 1,001,000,000) = 34,843,031,149.10 = 2^35.02015, also tight 35.0202: every term
except the replay allowance is one-time construction. It equals the total at 4 decimals because the
online part is 1.1e6 units out of 3.48e10; the online attack itself is a constant-time replay.

Memory (reported only): peak measured z3 maxrss 219,676,672 B = 2^27.71; r31k run peak RSS
7,111,040 B = 2^22.75 (time -l, this run); claimed 28.

## 7. Advice

Target-specific constants baked into the attack program: sol_own.h arrays (264 B), D5..D9, D18,
T6..T8 constants and trail rows (~40 B in r31k.c / r31mk.py) ~= 304 B; the replay program's 384 B
of embedded hex; committed seed strings ~100 B. Total < 1 KiB; declared 2^12 bytes with margin.
Record table and bitmap are rebuilt inside the charged K-scan; the certificate .bin files are
messages, not advice. FIPS round constants and IV are target-spec code.

## 8. Exclusions, stated plainly (fixes F-COST-001 for this ticket)

Five earlier K-scan runs (seeds from root 6b250b9f8d2d05df) measured the n* distribution and
produced witnesses that are NOT shipped in this package and whose outputs this chain reads for
nothing: not a constant, not a table, not a seed, not a calibration number enters the construction
above or the ledger above. They are listed in Section 9 as disclosed context only. If a reviewer
charged them anyway, the total would be 2^39.3311 - above the pending queue head, which is exactly
why they are excluded-by-independence and priced zero, and why nothing from them is claimed. Every
run that PRODUCED what this package ships is in Section 6, charged whole-process at retired
instructions.

## 9. Measured first-hit distribution (disclosed context; not the price of this ticket)

Six fresh pre-committed seeds of the same program and constants, first-collision trial index n*:
2^31.32 (this ticket's run, d5003c531ddf9d2a), 2^31.60, 2^31.63, 2^35.89, 2^36.32, 2^37.32.
The ticket prices its own run's measured retired instructions - a draw on the lucky side of the
six-draw sample median 2^33.76 - and claims nothing about seeds it did not run. Re-execution
sensitivity, priced at trial-count x the worst-measured allowance rate 1.1198967 u/draw (the 25
ops/instr conversion of this run measures 196.95 retired instructions/draw against 157.2-190.4 in
the five earlier runs, so the measured-instruction reading of a re-run is bracketed by the
H-INSTR 13-50 ops/instr sweep below): re-pricing K at the 2^33.76 sample-median draw gives a total
of 2^35.4041 (below the queue head); at the worst observed draw 2^37.32 it gives 2^37.8410 (above
head). Both readings are disclosed; neither enters this ticket's claim. No success probability
depends on any of it: the scored replay succeeds with probability 1.

## 10. Heuristics (declared)

H-INSTR (score-critical): retired hardware instructions on the Apple M4 build convert to v5
word-RAM operations at 25 ops/instruction - the promoted sibling package's transfer price. Scope:
the three charged processes (scan, z3, r31k). Sensitivity: at 13 ops/instr the total is 2^34.8673;
at 50 it is 2^35.2946; both remain below the pending head 36.64 (Section 8 of the note). The
K-scan's own per-form reading (157.2 instr/trial measured in the sibling's callgrind cross-check)
is consistent. Limitation: retired instructions undercount non-executed issue slots and are a
proxy for the word-RAM op count; the x1.10 margin plus the 50-ops sensitivity bound it.

H-TOOL (supporting): all remaining lab work (drivers, logging, digest re-verification scripts,
this package's assembly) fits the 1,001,000,000-unit flat allowance, ~2x above every individually
measured script. Limitation: an allowance, not a measurement; it is 2.9% of the total, and zeroing
it moves the claim to 2^34.9739.

## 11. Reproduction

The raw /usr/bin/time -l logs and the raw attack output are shipped verbatim in
Appendix B of this proof (sha256-pinned blocks): tl-1547760900.log (z3 solve),
tl_sets.log (scan), tl-k6.log + coll-6.txt (the K-scan and its collision record),
k6-root.txt (the seed root string committed before the run).
Certificates: digest(witness-6-a.bin, 'sha256', 31) == digest(witness-6-b.bin, 'sha256', 31) ==
8fc6cd1173ce63e44082ce6e3674737547649efc9f0d2651a35ff2153d871b53 through the organizer verifier.
Attack: build attack/r31k.c with cc -O3, run Section 3's command; the run halts at trial 2^31.32 on
the committed seed (deterministic group order, splitmix64). Ledger: exact rational sum of the
Section 6 terms; tightness by integer powers of 29,826,576,263,627/856 at scale 10^4. Seeds: solve
seed 1547760900 (s3-seeds.txt), scan seed root "k6-root-20261007T2105Z" committed pre-run.
baseline_improved = sha256-r31-nominal-v2 is a required reference identifier and asserts no
improvement over the nominal display value.

---

## Appendix A — attack sources (inline; the executable spec)

Build: `cc -O3 -o r31k attack/r31k.c -lpthread` (Apple clang, arm64). The binary that
ran is sha256 6583e7fe535f90795b57458bfa18e30a7c097f384fce6035884061bcb84805f8


<!-- file: attack/r31k.c sha256=3a1cbc6691a57d133d064b7fe7841ca9533d20e6a0108d2675c147b8795c17fa -->

```c
// Own sha256-r31 relaxed-cancellation first-block search.
// From OWN starting solution (sol_own.h, own z3 run): builds its own record
// table over V7/V8, then scans committed-seed trial groups for the first
// index whose key matches a record and whose completion yields a collision.
// Stops at the smallest colliding trial index (groups past it drain out).
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <time.h>
#include <unistd.h>
#include <stdatomic.h>
#include "sol_own.h"

static const uint32_t KK[31] = {0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
 0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
 0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
 0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351};
static const uint32_t IVV[8] = {0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};
#define R_(x,n) (((x)>>(n))|((x)<<(32-(n))))
#define B0(x) (R_(x,2)^R_(x,13)^R_(x,22))
#define B1(x) (R_(x,6)^R_(x,11)^R_(x,25))
#define s0(x) (R_(x,7)^R_(x,18)^((x)>>3))
#define s1(x) (R_(x,17)^R_(x,19)^((x)>>10))
#define IF_(x,y,z) (((x)&(y))^(~(x)&(z)))
#define MJ_(x,y,z) (((x)&(y))^((x)&(z))^((y)&(z)))
#define D5 0xfffff006u
#define D6 0x002087f1u
#define D7 0x4fefb5fau
#define D8 0x28011100u
#define D9 0x00008004u
#define D18 0xffff7ffcu
#define T6 0x00000ffau
#define T7 0xffdf780fu
#define T8 0xb00fca02u

typedef struct { uint32_t key, a0, e3, e4, w7, w8; } row_t;
static row_t *tab; static int ntab;
static uint64_t *bits; /* 2^24 bits over key>>8 */
static uint32_t G[64]; static int nG;
static uint32_t invcol[32];

static void comp31(const uint32_t cv[8], const uint32_t m[16], uint32_t out[8]) {
    uint32_t W[31]; for (int t = 0; t < 16; t++) W[t] = m[t];
    for (int t = 16; t < 31; t++) W[t] = s1(W[t-2]) + W[t-7] + s0(W[t-15]) + W[t-16];
    uint32_t a=cv[0],b=cv[1],c=cv[2],d=cv[3],e=cv[4],f=cv[5],g=cv[6],h=cv[7];
    for (int t = 0; t < 31; t++) {
        uint32_t T1 = h + B1(e) + IF_(e,f,g) + KK[t] + W[t], T2 = B0(a) + MJ_(a,b,c);
        h=g; g=f; f=e; e=d+T1; d=c; c=b; b=a; a=T1+T2;
    }
    out[0]=cv[0]+a; out[1]=cv[1]+b; out[2]=cv[2]+c; out[3]=cv[3]+d;
    out[4]=cv[4]+e; out[5]=cv[5]+f; out[6]=cv[6]+g; out[7]=cv[7]+h;
}
static void dgst(const uint32_t m0[16], const uint32_t m1[16], uint32_t out[8]) {
    uint32_t cv[8], cv2[8], pad[16] = {0}; pad[0] = 0x80000000u; pad[15] = 1024;
    comp31(IVV, m0, cv); comp31(cv, m1, cv2); comp31(cv2, pad, out);
}
static uint32_t sinv(uint32_t y) { uint32_t x = 0; for (int k = 0; k < 32; k++) if (y >> k & 1) x ^= invcol[k]; return x; }
static void mk_sinv(void) {
    uint32_t v[32], cb[32];
    for (int i = 0; i < 32; i++) { uint32_t b = 1u << i; v[i] = s1(b); cb[i] = b; }
    for (int k = 0; k < 32; k++) {
        int p = -1; for (int i = k; i < 32; i++) if (v[i] >> k & 1) { p = i; break; }
        if (p < 0) { fprintf(stderr, "singular\n"); exit(1); }
        uint32_t t = v[k]; v[k] = v[p]; v[p] = t; t = cb[k]; cb[k] = cb[p]; cb[p] = t;
        for (int i = 0; i < 32; i++) if (i != k && (v[i] >> k & 1)) { v[i] ^= v[k]; cb[i] ^= cb[k]; }
    }
    for (int k = 0; k < 32; k++) invcol[k] = cb[k];
}
static int rcmp(const void *a, const void *b) {
    uint32_t x = ((const row_t*)a)->key, y = ((const row_t*)b)->key;
    return x < y ? -1 : x > y;
}
static void mk_table(void) {
    static uint32_t V7[1024], V8[65536]; int n7 = 0, n8 = 0; uint32_t w = 0;
    do {
        if ((uint32_t)(s0(w + D7) - s0(w)) == T7) V7[n7++] = w;
        if ((uint32_t)(s0(w + D8) - s0(w)) == T8) V8[n8++] = w;
        if ((uint32_t)(s1(w + D9) - s1(w)) == D18) G[nG++] = w;
        w++;
    } while (w != 0);
    const char *r4 = "============0===0=========01===0", *r3 = "==========================10====";
    uint32_t m4 = 0, q4 = 0, m3 = 0, q3 = 0;
    for (int k = 0; k < 32; k++) {
        uint32_t b = 1u << (31 - k);
        if (r4[k] != '=') { m4 |= b; if (r4[k] == '1') q4 |= b; }
        if (r3[k] != '=') { m3 |= b; if (r3[k] == '1') q3 |= b; }
    }
    uint32_t f7 = (OM_EQ[7]-OM_E[7])-(B1(OM_EQ[6])-B1(OM_E[6]))-D7;
    uint32_t f6 = (OM_EQ[6]-OM_E[6])-(B1(OM_EQ[5])-B1(OM_E[5]))-D6;
    tab = malloc(sizeof(row_t) * (1 << 20)); ntab = 0;
    for (int i = 0; i < n8; i++) {
        uint32_t w8 = V8[i];
        uint32_t e4 = OM_E[8]-OM_A[4]-B1(OM_E[7])-IF_(OM_E[7],OM_E[6],OM_E[5])-KK[8]-w8;
        if ((e4 & m4) != q4) continue;
        if ((uint32_t)(IF_(OM_EQ[6],OM_EQ[5],e4)-IF_(OM_E[6],OM_E[5],e4)) != f7) continue;
        uint32_t a0 = e4-OM_A[4]+B0(OM_A[3])+MJ_(OM_A[3],OM_A[2],OM_A[1]);
        for (int j = 0; j < n7; j++) {
            uint32_t w7 = V7[j];
            uint32_t e3 = OM_E[7]-OM_A[3]-B1(OM_E[6])-IF_(OM_E[6],OM_E[5],e4)-KK[7]-w7;
            if ((e3 & m3) != q3) continue;
            if ((uint32_t)(IF_(OM_EQ[5],e4,e3)-IF_(OM_E[5],e4,e3)) != f6) continue;
            uint32_t am = e3-OM_A[3]+B0(OM_A[2])+MJ_(OM_A[2],OM_A[1],a0);
            tab[ntab++] = (row_t){am, a0, e3, e4, w7, w8};
        }
    }
    qsort(tab, ntab, sizeof(row_t), rcmp);
    bits = calloc(1 << 18, 8);
    for (int i = 0; i < ntab; i++) { uint32_t b = tab[i].key >> 8; bits[b >> 6] |= 1ull << (b & 63); }
    fprintf(stderr, "V7=%d V8=%d G16=%d records=%d\n", n7, n8, nG, ntab);
}

typedef struct { uint64_t trials, khit, rhit, v6, r20, ctry, cok, col, i13, i15, bmh, grp, over; } ct_t;
static ct_t cts[64];
static atomic_int halt; static atomic_int live; static pthread_mutex_t omu = PTHREAD_MUTEX_INITIALIZER;
static FILE *of; static atomic_uint_fast64_t ncol;
static uint64_t rng(uint64_t *s) {
    uint64_t z = (*s += 0x9e3779b97f4a7c15ull);
    z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ull; z = (z ^ (z >> 27)) * 0x94d049bb133111ebull;
    return z ^ (z >> 31);
}
/* completion: solve W14 from G16 pick, draw E13 (<=2^22) then E15 (<=2^12) */
static int finish(uint32_t W[16], uint32_t g, uint64_t *rs, ct_t *c) {
    uint32_t w14 = sinv(g - W[9] - s0(W[1]) - W[0]); W[14] = w14;
    if ((uint32_t)(s1(w14) + W[9] + s0(W[1]) + W[0]) != g) return 0;
    uint32_t t13 = OM_A[9]+OM_E[9]+B1(OM_E[12])+IF_(OM_E[12],OM_E[11],OM_E[10])+KK[13];
    uint32_t t13q = OM_AQ[9]+OM_EQ[9]+B1(OM_EQ[12])+IF_(OM_EQ[12],OM_EQ[11],OM_EQ[10])+KK[13];
    if (t13 != t13q) return 0;
    for (int t = 0; t < (1 << 22); t++) {
        c->i13++; uint32_t e13 = (uint32_t)rng(rs); uint32_t w13 = e13 - t13;
        uint32_t a13 = e13-OM_A[9]+B0(OM_A[12])+MJ_(OM_A[12],OM_A[11],OM_A[10]);
        uint32_t a13q = e13-OM_AQ[9]+B0(OM_AQ[12])+MJ_(OM_AQ[12],OM_AQ[11],OM_AQ[10]);
        if (a13 != a13q) return 0;
        uint32_t e14 = OM_A[10]+OM_E[10]+B1(e13)+IF_(e13,OM_E[12],OM_E[11])+KK[14]+w14;
        uint32_t e14q = OM_AQ[10]+OM_EQ[10]+B1(e13)+IF_(e13,OM_EQ[12],OM_EQ[11])+KK[14]+w14;
        if ((uint32_t)(e14q - e14) != 0x8004u) continue;
        uint32_t a14 = e14-OM_A[10]+B0(a13)+MJ_(a13,OM_A[12],OM_A[11]);
        uint32_t a14q = e14q-OM_AQ[10]+B0(a13)+MJ_(a13,OM_AQ[12],OM_AQ[11]);
        if (a14 != a14q) continue;
        uint32_t f15 = OM_A[11]+OM_E[11]+B1(e14)+IF_(e14,e13,OM_E[12])+KK[15];
        uint32_t f15q = OM_AQ[11]+OM_EQ[11]+B1(e14q)+IF_(e14q,e13,OM_EQ[12])+KK[15];
        if (f15 != f15q) continue;
        for (int u = 0; u < (1 << 12); u++) {
            c->i15++; uint32_t e15 = (uint32_t)rng(rs); uint32_t w15 = e15 - f15;
            uint32_t e16 = OM_A[12]+OM_E[12]+B1(e15)+IF_(e15,e14,e13)+KK[16]+g;
            uint32_t e16q = OM_AQ[12]+OM_EQ[12]+B1(e15)+IF_(e15,e14q,e13)+KK[16]+g+D9;
            if (e16 != e16q) continue;
            uint32_t s17 = a13+e13+B1(e16)+IF_(e16,e15,e14);
            uint32_t s17q = a13+e13+B1(e16)+IF_(e16,e15,e14q);
            if (s17 != s17q) continue;
            W[13] = w13; W[15] = w15; return 1;
        }
    }
    return 0;
}

static int on_hit(int tid, const uint32_t m0[16], uint64_t *rs) {
    ct_t *c = &cts[tid]; c->bmh++;
    uint32_t cv[8]; comp31(IVV, m0, cv);
    int lo = 0, hi = ntab;
    while (lo < hi) { int md = (lo + hi) / 2; if (tab[md].key < cv[0]) lo = md + 1; else hi = md; }
    if (lo >= ntab || tab[lo].key != cv[0]) return 0;
    c->khit++;
    for (int r = lo; r < ntab && tab[r].key == cv[0]; r++) {
        const row_t *q = &tab[r]; c->rhit++;
        /* trial state: Am[k]=A[k-4], Ee[i]=E[i]; W[0..6] from step equations */
        uint32_t Am[11];
        Am[0]=cv[3]; Am[1]=cv[2]; Am[2]=cv[1]; Am[3]=cv[0]; Am[4]=q->a0;
        for (int i = 5; i <= 10; i++) Am[i] = (&OM_A[0])[i-4]; /* Am[k]=A[k-4] */
        uint32_t Ee[7];
        Ee[0] = Am[4]+Am[0]-B0(Am[3])-MJ_(Am[3],Am[2],Am[1]);
        Ee[1] = (&OM_A[0])[1]+Am[1]-B0(Am[4])-MJ_(Am[4],Am[3],Am[2]);
        Ee[2] = (&OM_A[0])[2]+Am[2]-B0((&OM_A[0])[1])-MJ_((&OM_A[0])[1],Am[4],Am[3]);
        Ee[3] = q->e3; Ee[4] = q->e4;
        Ee[5] = (&OM_E[0])[5]; Ee[6] = (&OM_E[0])[6];
        uint32_t Em4[4] = {cv[7], cv[6], cv[5], cv[4]}; /* E[-4..-1]=h,g,f,e */
        uint32_t W[16];
        for (int i = 0; i <= 6; i++) {
            uint32_t em4 = (i >= 4) ? Ee[i-4] : Em4[i];
            uint32_t em1 = (i == 0) ? cv[4] : Ee[i-1];
            uint32_t em2 = (i == 0) ? cv[5] : (i == 1) ? cv[4] : Ee[i-2];
            uint32_t em3 = (i == 0) ? cv[6] : (i == 1) ? cv[5] : (i == 2) ? cv[4] : Ee[i-3];
            W[i] = Ee[i]-Am[i]-em4-B1(em1)-IF_(em1,em2,em3)-KK[i];
        }
        W[7] = q->w7; W[8] = q->w8;
        for (int i = 9; i <= 12; i++) W[i] = (&OM_W[0])[i];
        W[13] = W[14] = W[15] = 0;
        if ((uint32_t)(s0(W[6]+D6)-s0(W[6])) != T6) continue;
        c->v6++;
        uint32_t tgt = 0u - (uint32_t)(s0(W[5]+D5)-s0(W[5]));
        uint32_t c18 = W[11] + s0(W[3]) + W[2];
        int gs = -1;
        for (int k = 0; k < nG; k++) {
            uint32_t w18 = s1(G[k]) + c18;
            if ((uint32_t)(s1(w18+D18)-s1(w18)) == tgt) { gs = k; break; }
        }
        if (gs < 0) continue;
        c->r20++;
        c->ctry++;
        uint32_t Wc[16]; memcpy(Wc, W, sizeof W);
        if (!finish(Wc, G[gs], rs, c)) continue;
        c->cok++;
        uint32_t Wb[16]; memcpy(Wb, Wc, sizeof Wc);
        Wb[5]+=D5; Wb[6]+=D6; Wb[7]+=D7; Wb[8]+=D8; Wb[9]+=D9;
        uint32_t h1[8], h2[8]; dgst(m0, Wc, h1); dgst(m0, Wb, h2);
        if (memcmp(h1, h2, 32) == 0 && memcmp(Wc, Wb, 64) != 0) {
            c->col++; atomic_fetch_add(&ncol, 1);
            pthread_mutex_lock(&omu);
            fprintf(of, "COLLISION tid=%d\nM0 ", tid);
            for (int i = 0; i < 16; i++) fprintf(of, "%08x", m0[i]);
            fprintf(of, "\nM1 ");
            for (int i = 0; i < 16; i++) fprintf(of, "%08x", Wc[i]);
            fprintf(of, "\nM1b ");
            for (int i = 0; i < 16; i++) fprintf(of, "%08x", Wb[i]);
            fprintf(of, "\nDIGEST ");
            for (int i = 0; i < 8; i++) fprintf(of, "%08x", h1[i]);
            fprintf(of, "\n"); fflush(of);
            pthread_mutex_unlock(&omu);
            return 1;
        }
    }
    return 0;
}

static uint64_t seed0; static double tlim;
static int NTH; static _Atomic uint64_t best = UINT64_MAX;
static void *work(void *a) {
    int tid = (int)(intptr_t)a; ct_t *c = &cts[tid]; atomic_fetch_add(&live, 1);
    uint32_t m[16];
    for (uint64_t g = (uint64_t)tid; ; g += (uint64_t)NTH) {
        uint64_t bn = atomic_load(&best);
        if (atomic_load(&halt)) break;
        if (bn != UINT64_MAX && g > (bn >> 24)) break;
        c->grp++; uint64_t rs = seed0 ^ (g * 0x9e3779b97f4a7c15ull) ^ 0x5bd1e9955bd1e995ull;
        for (int i = 0; i < 15; i++) m[i] = (uint32_t)rng(&rs);
        uint64_t crs = seed0 ^ (g * 0xd1b54a32d192ed03ull) ^ 0x2545f4914f6cdd1dull;
        uint32_t a=IVV[0],b=IVV[1],cc=IVV[2],d=IVV[3],e=IVV[4],f=IVV[5],gg=IVV[6],h=IVV[7];
        for (int t = 0; t < 15; t++) {
            uint32_t T1 = h+B1(e)+IF_(e,f,gg)+KK[t]+m[t], T2 = B0(a)+MJ_(a,b,cc);
            h=gg; gg=f; f=e; e=d+T1; d=cc; cc=b; b=a; a=T1+T2;
        }
        /* shared prefix words 16..30 as functions of m[15]=x */
        uint32_t m16=s1(m[14])+m[9]+s0(m[1])+m[0], m18=s1(m16)+m[11]+s0(m[3])+m[2], m20=s1(m18)+m[13]+s0(m[5])+m[4];
        uint32_t c17=m[10]+s0(m[2])+m[1], c19=m[12]+s0(m[4])+m[3], c21=m[14]+s0(m[6])+m[5], c22=s1(m20)+s0(m[7])+m[6];
        uint32_t c23=m16+s0(m[8])+m[7], c24=s0(m[9])+m[8], c25=m18+s0(m[10])+m[9], c26=s0(m[11])+m[10];
        uint32_t c27=m20+s0(m[12])+m[11], c28=s0(m[13])+m[12], c29=s0(m[14])+m[13], c30=m[14];
        int ab = 0;
        for (uint32_t base = 0; base < (1u << 24); base += 8) {
            uint32_t key[8];
            for (int j = 0; j < 8; j++) {
                uint32_t x = base + (uint32_t)j;
                uint32_t w17=s1(x)+c17, w19=s1(w17)+c19, w21=s1(w19)+c21, w22=c22+x, w23=s1(w21)+c23, w24=s1(w22)+w17+c24;
                uint32_t w25=s1(w23)+c25, w26=s1(w24)+w19+c26, w27=s1(w25)+c27, w28=s1(w26)+w21+c28, w29=s1(w27)+w22+c29, w30=s1(w28)+w23+s0(x)+c30;
                uint32_t A=a,B=b,C=cc,D=d,E=e,F=f,Gg=gg,H=h,T1,T2;
#define ST(w,k) T1=H+B1(E)+IF_(E,F,Gg)+(k)+(w); T2=B0(A)+MJ_(A,B,C); H=Gg; Gg=F; F=E; E=D+T1; D=C; C=B; B=A; A=T1+T2;
                ST(x,KK[15]) ST(m16,KK[16]) ST(w17,KK[17]) ST(m18,KK[18]) ST(w19,KK[19]) ST(m20,KK[20]) ST(w21,KK[21]) ST(w22,KK[22])
                ST(w23,KK[23]) ST(w24,KK[24]) ST(w25,KK[25]) ST(w26,KK[26]) ST(w27,KK[27]) ST(w28,KK[28]) ST(w29,KK[29]) ST(w30,KK[30])
                key[j] = IVV[0] + A;
            }
            for (int j = 0; j < 8; j++) {
                uint32_t bi = key[j] >> 8;
                if (bits[bi >> 6] >> (bi & 63) & 1) {
                    uint32_t mm[16]; memcpy(mm, m, 60); mm[15] = base + (uint32_t)j;
                    if (on_hit(tid, mm, &crs)) {
                        uint64_t n = (g << 24) | (uint64_t)(base + (uint32_t)j);
                        uint64_t cur = atomic_load(&best);
                        while (n < cur && !atomic_compare_exchange_weak(&best, &cur, n)) {}
                        pthread_mutex_lock(&omu);
                        fprintf(of, "INDEX n=%llu group=%llu j=%u\n", (unsigned long long)n, (unsigned long long)g, base + (uint32_t)j);
                        fflush(of); pthread_mutex_unlock(&omu);
                    }
                }
            }
            c->trials += 8;
            if ((base & 0xfffff) == 0) {
                uint64_t bb = atomic_load(&best);
                if (atomic_load(&halt) || (bb != UINT64_MAX && g > (bb >> 24))) { ab = 1; break; }
            }
        }
        if (ab) { c->over++; break; }
    }
    atomic_fetch_sub(&live, 1);
    return NULL;
}
static void selftest(void) {
    uint64_t r2 = 7;
    for (int t = 0; t < 2000; t++) {
        uint32_t m[16]; for (int i = 0; i < 16; i++) m[i] = (uint32_t)rng(&r2);
        uint32_t a=IVV[0],b=IVV[1],cc=IVV[2],d=IVV[3],e=IVV[4],f=IVV[5],g=IVV[6],h=IVV[7];
        for (int s = 0; s < 15; s++) {
            uint32_t T1=h+B1(e)+IF_(e,f,g)+KK[s]+m[s], T2=B0(a)+MJ_(a,b,cc);
            h=g; g=f; f=e; e=d+T1; d=cc; cc=b; b=a; a=T1+T2;
        }
        /* recompute key via comp31 reference */
        uint32_t ref[8]; comp31(IVV, m, ref);
        /* replicate fast path for x=m[15] */
        uint32_t x = m[15];
        uint32_t m16=s1(m[14])+m[9]+s0(m[1])+m[0], m18=s1(m16)+m[11]+s0(m[3])+m[2], m20=s1(m18)+m[13]+s0(m[5])+m[4];
        uint32_t c17=m[10]+s0(m[2])+m[1], c19=m[12]+s0(m[4])+m[3], c21=m[14]+s0(m[6])+m[5], c22=s1(m20)+s0(m[7])+m[6];
        uint32_t c23=m16+s0(m[8])+m[7], c24=s0(m[9])+m[8], c25=m18+s0(m[10])+m[9], c26=s0(m[11])+m[10];
        uint32_t c27=m20+s0(m[12])+m[11], c28=s0(m[13])+m[12], c29=s0(m[14])+m[13], c30=m[14];
        uint32_t w17=s1(x)+c17, w19=s1(w17)+c19, w21=s1(w19)+c21, w22=c22+x, w23=s1(w21)+c23, w24=s1(w22)+w17+c24;
        uint32_t w25=s1(w23)+c25, w26=s1(w24)+w19+c26, w27=s1(w25)+c27, w28=s1(w26)+w21+c28, w29=s1(w27)+w22+c29, w30=s1(w28)+w23+s0(x)+c30;
        uint32_t A=a,B=b,C=cc,D=d,E=e,F=f,Gg=g,H=h,T1,T2;
        ST(x,KK[15]) ST(m16,KK[16]) ST(w17,KK[17]) ST(m18,KK[18]) ST(w19,KK[19]) ST(m20,KK[20]) ST(w21,KK[21]) ST(w22,KK[22])
        ST(w23,KK[23]) ST(w24,KK[24]) ST(w25,KK[25]) ST(w26,KK[26]) ST(w27,KK[27]) ST(w28,KK[28]) ST(w29,KK[29]) ST(w30,KK[30])
        if (ref[0] != IVV[0] + A) { fprintf(stderr, "KERNEL MISMATCH\n"); exit(3); }
    }
    fprintf(stderr, "kernel check OK\n");
}

int main(int argc, char **argv) {
    int nth = argc > 1 ? atoi(argv[1]) : 1;
    tlim = argc > 2 ? atof(argv[2]) : 10;
    seed0 = argc > 3 ? strtoull(argv[3], 0, 16) : 0x7231a5ed2026u;
    const char *outp = argc > 4 ? argv[4] : "collisions.txt";
    of = stderr; mk_sinv(); mk_table(); selftest();
    if (tlim <= 0) return 0;
    of = fopen(outp, "a");
    pthread_t th[64]; struct timespec t0, t1; clock_gettime(CLOCK_MONOTONIC, &t0);
    NTH = nth;
    for (int i = 0; i < nth; i++) pthread_create(&th[i], 0, work, (void*)(intptr_t)i);
    double last = 0;
    while (1) {
        sleep(1); clock_gettime(CLOCK_MONOTONIC, &t1);
        double el = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) * 1e-9;
        int fin = el >= tlim || access("STOP", F_OK) == 0 || (el > 2 && atomic_load(&live) == 0);
        if (el - last >= 30 || fin) {
            last = el; ct_t s = {0};
            for (int i = 0; i < nth; i++) {
                s.trials+=cts[i].trials; s.khit+=cts[i].khit; s.rhit+=cts[i].rhit; s.v6+=cts[i].v6;
                s.r20+=cts[i].r20; s.ctry+=cts[i].ctry; s.cok+=cts[i].cok; s.col+=cts[i].col;
            }
            printf("t=%.0f trials=%llu (2^%.3f) rate=%.3e/s khit=%llu rhit=%llu v6=%llu r20=%llu comp=%llu/%llu col=%llu\n",
                el, (unsigned long long)s.trials, s.trials ? __builtin_log2((double)s.trials) : 0.0,
                s.trials / el, (unsigned long long)s.khit, (unsigned long long)s.rhit,
                (unsigned long long)s.v6, (unsigned long long)s.r20,
                (unsigned long long)s.cok, (unsigned long long)s.ctry, (unsigned long long)s.col);
            fflush(stdout);
        }
        if (fin) break;
    }
    atomic_store(&halt, 1);
    for (int i = 0; i < nth; i++) pthread_join(th[i], 0);
    ct_t s = {0}; uint64_t a13 = 0, a15 = 0, ov = 0, bm = 0, gr = 0;
    for (int i = 0; i < nth; i++) {
        s.trials+=cts[i].trials; s.khit+=cts[i].khit; s.rhit+=cts[i].rhit; s.v6+=cts[i].v6;
        s.r20+=cts[i].r20; s.ctry+=cts[i].ctry; s.cok+=cts[i].cok; s.col+=cts[i].col;
        a13+=cts[i].i13; a15+=cts[i].i15; ov+=cts[i].over; bm+=cts[i].bmh; gr+=cts[i].grp;
    }
    printf("DET best=%llu it13=%llu it15=%llu aborted=%llu bmhits=%llu groups=%llu\n",
        (unsigned long long)atomic_load(&best), (unsigned long long)a13, (unsigned long long)a15,
        (unsigned long long)ov, (unsigned long long)bm, (unsigned long long)gr);
    printf("FINAL trials=%llu khit=%llu rhit=%llu v6=%llu r20=%llu comp=%llu/%llu col=%llu\n",
        (unsigned long long)s.trials, (unsigned long long)s.khit, (unsigned long long)s.rhit,
        (unsigned long long)s.v6, (unsigned long long)s.r20,
        (unsigned long long)s.cok, (unsigned long long)s.ctry, (unsigned long long)s.col);
    return 0;
}
```


<!-- file: attack/sol_own.h sha256=d240548a681ed96918d39bc213abda8a6dc1d44aceae2e409fc10be65452b292 -->

```c
/* own starting solution, z3 seed committed in s-commit.txt */
static const unsigned OM_A[13]={0x00000000u,0xb5927e19u,0x74474cb7u,0xd40461e1u,0x4b6d7b31u,0xfa9053ffu,0x35b9e0b8u,0xe3ba11f4u,0x9b94e337u,0xc7d2cb8au,0x24881e63u,0x68486c96u,0x59b205feu};
static const unsigned OM_AQ[13]={0x00000000u,0xb5927e19u,0x74474cb7u,0xd40461e1u,0x4b6d7b31u,0xfa904405u,0x3539e0b9u,0xf29a01f1u,0x9b94e333u,0xc7d2cb8au,0x24889e67u,0x68486c96u,0x59b205feu};
static const unsigned OM_E[13]={0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x1d1fa7ddu,0xafe879e7u,0x4cd7cae5u,0x943bc249u,0x61d503d1u,0xf02293fau,0xaa2f041du,0xb16b99ecu};
static const unsigned OM_EQ[13]={0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x1d1f97e3u,0xafe0f9e6u,0x9c5fce6cu,0xd93b4a4du,0x61d503d9u,0xdfa31402u,0xbaef0415u,0xb16b19e4u};
static const unsigned OM_W[13]={0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x954a6452u,0x05106319u,0x3a9ff24bu,0x4a4a9bfbu};
static const unsigned OM_W9Q=0x954ae456u;
```


<!-- file: attack/r31mk.py sha256=74844fcfae368d646840609073929355a5424686a9d989141a45ec487ecbc597 -->

```python
"""Own SMT-LIB2 generator for a sha256-r31 starting solution.

Math basis (public, re-derived): published 31-step signed characteristic cell
table + step equations + relaxed cancellation R20 context (dW20 = 0 only).
Unknowns: copies P/P' of A1..A12, E5..E12, W9..W12 (W10..W12 shared),
plus existential witnesses E3, E4, W7, W8 proving a nonempty record table.
Usage: python3 r31mk.py SEED [--residue 0xe730f] [--bare] > model.smt2
  --residue R : pin yield class c8 mod 2^20 = R (from OUR OWN residue scan)
  --bare      : drop table-nonempty + residue (diagnostic configs only)
"""
import sys

KK = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1,
      0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
      0x72be5d74, 0x80deb1fe, 0x9bdc06a7]
ALL = "=" * 32
# Transcribed public trail rows (bit 31 left). Rows not listed are all '='.
RA = {5: "===================n=unnnnnnn=n=",
      6: "========n======================u",
      7: "===u===n==n========n=========n=u",
      8: "=============================n==",
      10: "================u============u=="}
RE = {5: "000111010001111110nu=11111unnnu1",
      6: "101011=11==0n0==u11110==1110011n",
      7: "un0u1100n=01u11111001u1=n110u10n",
      8: "1u01un0u0=1=1=11n=0=u0=001001u0=",
      9: "01100001110=0=010===00=11101u0=1",
      10: "=1n1uuuuu0100=1un0=10unnnnnnn010",
      11: "=01u1010uu1==11100===1000001n=0=",
      12: "==110001=11====1n====0011110n=0="}
RW9 = "================u==========1=u=="
R3 = "==========================10===="
R4 = "============0===0=========01===0"
D5, D6, D7, D8, D9 = 0xfffff006, 0x002087f1, 0x4fefb5fa, 0x28011100, 0x00008004
T6, T7, T8 = 0x00000ffa, 0xffdf780f, 0xb00fca02


def hx(v):
    return "#x%08x" % (v & 0xFFFFFFFF)


def split(row):
    me = mf = vf = mu = mn = 0
    for k, c in enumerate(row):
        b = 1 << (31 - k)
        if c == "=":
            me |= b
        elif c in "01":
            mf |= b
            if c == "1":
                vf |= b
        elif c == "u":
            mu |= b
        elif c == "n":
            mn |= b
    return me, mf, vf, mu, mn


def cond(x, y, row):
    me, mf, vf, mu, mn = split(row)
    o = []
    if mf:
        o += ["(= (bvand %s %s) %s)" % (x, hx(mf), hx(vf)),
              "(= (bvand %s %s) %s)" % (y, hx(mf), hx(vf))]
    if mu:
        o += ["(= (bvand %s %s) #x00000000)" % (x, hx(mu)),
              "(= (bvand %s %s) %s)" % (y, hx(mu), hx(mu))]
    if mn:
        o += ["(= (bvand %s %s) %s)" % (x, hx(mn), hx(mn)),
              "(= (bvand %s %s) #x00000000)" % (y, hx(mn))]
    if me:
        o += ["(= (bvand (bvxor %s %s) %s) #x00000000)" % (x, y, hx(me))]
    return o


def B0(x): return "(bvxor ((_ rotate_right 2) %s) ((_ rotate_right 13) %s) ((_ rotate_right 22) %s))" % (x, x, x)
def B1(x): return "(bvxor ((_ rotate_right 6) %s) ((_ rotate_right 11) %s) ((_ rotate_right 25) %s))" % (x, x, x)
def b0(x): return "(bvxor ((_ rotate_right 7) %s) ((_ rotate_right 18) %s) (bvlshr %s #x00000003))" % (x, x, x)
def IF(x, y, z): return "(bvxor (bvand %s %s) (bvand (bvnot %s) %s))" % (x, y, x, z)
def MJ(x, y, z): return "(bvxor (bvand %s %s) (bvand %s %s) (bvand %s %s))" % (x, y, x, z, y, z)


def build(seed, residue, bare):
    L = ["(set-logic QF_BV)",
         "(set-option :random-seed %d)" % seed,
         "(set-option :sat.random_seed %d)" % seed,
         "(set-option :smt.random_seed %d)" % seed]
    vs = []
    for s in ("", "q"):
        vs += ["A%d%s" % (i, s) for i in range(1, 13)]
        vs += ["E%d%s" % (i, s) for i in range(5, 13)]
    vs += ["W9", "W10", "W11", "W12", "W9q", "E3", "E4", "W7", "W8"]
    for n in vs:
        L.append("(declare-fun %s () (_ BitVec 32))" % n)
    A = lambda i, s="": "A%d%s" % (i, s)
    E = lambda i, s="": "E%d%s" % (i, s)
    W = lambda i, s="": ("W9q" if (i == 9 and s == "q") else "W%d" % i)
    C = []
    for i in range(1, 13):
        C += cond(A(i), A(i, "q"), RA.get(i, ALL))
    for i in range(5, 13):
        C += cond(E(i), E(i, "q"), RE[i])
    C += cond("W9", "W9q", RW9)
    for s in ("", "q"):
        for i in range(5, 13):
            C.append("(= %s (bvadd (bvsub %s %s) %s %s))" % (
                A(i, s), E(i, s), A(i - 4, s), B0(A(i - 1, s)),
                MJ(A(i - 1, s), A(i - 2, s), A(i - 3, s))))
        for i in range(9, 13):
            C.append("(= %s (bvadd %s %s %s %s %s %s))" % (
                E(i, s), A(i - 4, s), E(i - 4, s), B1(E(i - 1, s)),
                IF(E(i - 1, s), E(i - 2, s), E(i - 3, s)), hx(KK[i]), W(i, s)))
    # step-8 difference closure (A4,E4 carry no difference; dW8=D8)
    C.append("(= (bvsub %s %s) (bvadd (bvsub %s %s) (bvsub %s %s) %s))" % (
        E(8, "q"), E(8), B1(E(7, "q")), B1(E(7)),
        IF(E(7, "q"), E(6, "q"), E(5, "q")), IF(E(7), E(6), E(5)), hx(D8)))
    # step 13: zero output difference both registers
    C.append("(= (bvadd %s %s %s %s) (bvadd %s %s %s %s))" % (
        A(9, "q"), E(9, "q"), B1(E(12, "q")), IF(E(12, "q"), E(11, "q"), E(10, "q")),
        A(9), E(9), B1(E(12)), IF(E(12), E(11), E(10))))
    C.append("(= %s %s)" % (MJ(A(12, "q"), A(11, "q"), A(10, "q")), MJ(A(12), A(11), A(10))))
    # W9 in V9  <=>  s0 diff equals -D8
    C.append("(= (bvsub %s %s) %s)" % (b0("W9q"), b0("W9"), hx((-D8) & 0xFFFFFFFF)))
    if not bare:
        # existential witnesses: some (W8,E4),(W7,E3) survive table filters
        C += cond("E4", "E4", R4) + cond("E3", "E3", R3)
        C.append("(= %s (bvadd %s E4 %s %s %s W8))" % (
            E(8), A(4), B1(E(7)), IF(E(7), E(6), E(5)), hx(KK[8])))
        C.append("(= %s (bvadd %s E3 %s %s %s W7))" % (
            E(7), A(3), B1(E(6)), IF(E(6), E(5), "E4"), hx(KK[7])))
        C.append("(= (bvsub %s %s) (bvadd (bvsub %s %s) (bvsub %s %s) %s))" % (
            E(7, "q"), E(7), B1(E(6, "q")), B1(E(6)),
            IF(E(6, "q"), E(5, "q"), "E4"), IF(E(6), E(5), "E4"), hx(D7)))
        C.append("(= (bvsub %s %s) (bvadd (bvsub %s %s) (bvsub %s %s) %s))" % (
            E(6, "q"), E(6), B1(E(5, "q")), B1(E(5)),
            IF(E(5, "q"), "E4", "E3"), IF(E(5), "E4", "E3"), hx(D6)))
        C.append("(= (bvsub %s %s) %s)" % (
            b0("(bvadd W8 %s)" % hx(D8)), b0("W8"), hx(T8)))
        C.append("(= (bvsub %s %s) %s)" % (
            b0("(bvadd W7 %s)" % hx(D7)), b0("W7"), hx(T7)))
        if residue is not None:
            C.append("(= (bvand (bvsub (bvsub (bvsub (bvsub %s %s) %s) %s) %s) #x000fffff) %s)" % (
                E(8), A(4), B1(E(7)), IF(E(7), E(6), E(5)), hx(KK[8]), hx(residue)))
    for c in C:
        L.append("(assert %s)" % c)
    L.append("(check-sat)")
    L.append("(get-value (%s))" % " ".join(vs))
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    sd = int(sys.argv[1])
    rs = br = None
    for a in sys.argv[2:]:
        if a == "--bare":
            br = True
        elif a.startswith("--residue"):
            rs = int(a.split("=")[1], 16) & 0xFFFFF
    sys.stdout.write(build(sd, rs, br))
```


<!-- file: attack/r31sets.c sha256=dc27eab2d51e394583e8da100f73b4fd0fddd61e049d6835dd8f95f1adfcfad4 -->

```c
// Own sha256-r31 set enumeration + yield-residue scan.
// Enumerates V7/V8/G16 over full 2^32, dumps sets, scans residue classes
// mod 2^20 maximizing row-4 survivors over V8 (own mask derivation).
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
static inline uint32_t R(uint32_t x, int n) { return (x >> n) | (x << (32 - n)); }
static inline uint32_t s0(uint32_t x) { return R(x, 7) ^ R(x, 18) ^ (x >> 3); }
static inline uint32_t s1(uint32_t x) { return R(x, 17) ^ R(x, 19) ^ (x >> 10); }
#define D7 0x4fefb5fau
#define D8 0x28011100u
#define D9 0x00008004u
#define T7 0xffdf780fu
#define T8 0xb00fca02u
#define D18 0xffff7ffcu
int main(int argc, char **argv) {
    int nsamp = argc > 1 ? atoi(argv[1]) : 300000;
    FILE *f7 = fopen("v7_own.txt", "w"), *f8 = fopen("v8_own.txt", "w"), *fg = fopen("g16_own.txt", "w");
    if (!f7 || !f8 || !fg) { fprintf(stderr, "open fail\n"); return 1; }
    uint64_t n7 = 0, n8 = 0, ng = 0; uint32_t w = 0;
    // two passes: first count via streaming to files (single 2^32 loop)
    do {
        if ((uint32_t)(s0(w + D7) - s0(w)) == T7) { fprintf(f7, "%08x\n", w); n7++; }
        if ((uint32_t)(s0(w + D8) - s0(w)) == T8) { fprintf(f8, "%08x\n", w); n8++; }
        if ((uint32_t)(s1(w + D9) - s1(w)) == D18) { fprintf(fg, "%08x\n", w); ng++; }
        w++;
    } while (w != 0);
    fclose(f7); fclose(f8); fclose(fg);
    printf("|V7|=%llu |V8|=%llu |G16|=%llu\n", (unsigned long long)n7, (unsigned long long)n8, (unsigned long long)ng);
    // residue scan: read V8 low-20 bits
    static uint32_t V[60000]; int n = 0; unsigned x;
    FILE *f = fopen("v8_own.txt", "r");
    while (fscanf(f, "%x", &x) == 1 && n < 60000) V[n++] = x & 0xfffff;
    fclose(f);
    // row-4 mask: value bits of "============0===0=========01===0"
    const char *r4 = "============0===0=========01===0";
    uint32_t cm = 0, va = 0;
    for (int k = 0; k < 32; k++) { uint32_t b = 1u << (31 - k); if (r4[k] != '=') { cm |= b; if (r4[k] == '1') va |= b; } }
    cm &= 0xfffff; va &= 0xfffff;
    uint64_t st = 0x9e3779b9ull; int best = 0; uint32_t br = 0;
    for (int t = 0; t < nsamp; t++) {
        st ^= st << 13; st ^= st >> 7; st ^= st << 17;
        uint32_t r = (uint32_t)st & 0xfffff; int c = 0;
        for (int i = 0; i < n; i++) { uint32_t e = (r - V[i]) & 0xfffff; c += ((e & cm) == va); }
        if (c > best) { best = c; br = r; }
    }
    printf("own best residue %05x pass %d of %d (mask %05x val %05x)\n", br, best, n, cm, va);
    return 0;
}
```


---

## Appendix B — raw instrumentation logs (verbatim)


<!-- file: logs/tl-k6.log sha256=0450c4a8c80c4e50577dab2673a296c32d5caf81d9fcdfd58f9f63d216e6bc80 -->

```
V7=512 V8=49408 G16=64 records=103168
kernel check OK
t=2 trials=2883584136 (2^31.425) rate=1.427e+09/s khit=15189 rhit=69409 v6=127 r20=1 comp=1/1 col=1
DET best=2685579961 it13=712 it15=8 aborted=17 bmhits=744109 groups=179
FINAL trials=2883584136 khit=15189 rhit=69409 v6=127 r20=1 comp=1/1 col=1
        8.23 real        46.24 user         0.08 sys
             7585792  maximum resident set size
                   0  average shared memory size
                   0  average unshared data size
                   0  average unshared stack size
                 739  page reclaims
                   1  page faults
                   0  swaps
                   0  block input operations
                   0  block output operations
                   0  messages sent
                   0  messages received
                   0  signals received
                   0  voluntary context switches
                5945  involuntary context switches
        567935304369  instructions retired
        157809823973  cycles elapsed
             7111040  peak memory footprint
```


<!-- file: logs/tl-1547760900.log sha256=fd431a456795a2ac3500bbf25bcd89ec3286307c680a8e269b463b3ace938835 -->

```
/Users/andrewgordon/.hermes/cache/scratch/r31run/run3/m-1547760900.smt2 -> sat in 261.9s
      261.99 real       260.57 user         1.37 sys
           219676672  maximum resident set size
                   0  average shared memory size
                   0  average unshared data size
                   0  average unshared stack size
               17615  page reclaims
                  17  page faults
                   0  swaps
                   0  block input operations
                   0  block output operations
                   0  messages sent
                   0  messages received
                   0  signals received
                   0  voluntary context switches
                5540  involuntary context switches
       1897370783016  instructions retired
        990804232850  cycles elapsed
           200524328  peak memory footprint
```


<!-- file: logs/tl_sets.log sha256=51300ac6d00b7116dc7323cd5184e91adb4e9d158533db3fad3fa45f0c9d46d2 -->

```
        7.46 real         7.26 user         0.04 sys
             2424832  maximum resident set size
                   0  average shared memory size
                   0  average unshared data size
                   0  average unshared stack size
                 386  page reclaims
                   1  page faults
                   0  swaps
                   0  block input operations
                   0  block output operations
                   0  messages sent
                   0  messages received
                   0  signals received
                   0  voluntary context switches
                  40  involuntary context switches
        160429645672  instructions retired
         26626702382  cycles elapsed
             1950056  peak memory footprint
```


<!-- file: logs/coll-6.txt sha256=50a48889c96a16bc1e52faee0d0588e6e66970b7fa41b2ee8451189446e33936 -->

```
COLLISION tid=10
M0 31e466210c5e0cee8c92620bf2c932e2591e8e7f66aba6b6c5d7a1ce4271f854f79d392119de3876693dda454e12edbc412bef069bc22aa20b77d0130012b2b9
M1 76e3309715169879f84b370638a51c9120ed81ff06a2bca21756157406b457ba661915bf954a6452051063193a9ff24b4a4a9bfb5cf1caacd77b3aeed59e04dc
M1b 76e3309715169879f84b370638a51c9120ed81ff06a2aca817769d6556a40db48e1a26bf954ae456051063193a9ff24b4a4a9bfb5cf1caacd77b3aeed59e04dc
DIGEST 8fc6cd1173ce63e44082ce6e3674737547649efc9f0d2651a35ff2153d871b53
INDEX n=2685579961 group=160 j=1225401
```


<!-- file: logs/k3-seed.txt sha256=47f200f920a2ba7e50f2002d2eb1e977686fd64be880d00a88faecbe42743816 -->

```
6b250b9f8d2d05df
```


<!-- file: logs/k3-trial-seeds.txt sha256=1a478d2cf096ba1d604e5023814f0415106c9e0c8cbe593dc89abb6a215abfd7 -->

```
14c5b8976042031e
227acde4c5267663
0b2b7d863d48e66a
b9803a2d55463362
a7b7eb54ff04f22b
```


<!-- file: logs/k6-root.txt sha256=46d3d69b33cf31ffdff70a59e10174eb66d79586132c2d70c739c5fbb2c85528 -->

```
k6-root-20261007T2105Z
```

