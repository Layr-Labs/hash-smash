# SHA-256 r31 collision search with an excluded-address sparse table

This package targets `sha256-r31-exploratory`, profile
`sha256-r31-prefix-v1`, under `collision-frontier-v5`. It is an analytic,
physically infeasible-memory construction. It supplies no computed collision,
experiment, or practical-attack claim. Its success bound holds for the fixed
selected hash without a random-function or balance premise.

## 1. Exact target and message domain

Write `BE_k(v)` for the k-byte big-endian encoding of v. Draw messages from

    m(u,w) = BE_32(u) || BE_4(w),
    0 <= u < 2^256, 0 <= w < 2^32.

Each message has 288 bits and exactly one padded block:

    BE_32(u) || BE_4(w) || 80 || 00 repeated 19 times || BE_8(288).

Its sixteen big-endian 32-bit words are `W[0..7]` from u, `W[8]=w`,
`W[9]=0x80000000`, `W[10..14]=0`, and `W[15]=288`.

Hash using the standard SHA-256 IV, original round indices 0 through 30,
full feed-forward, and all eight output words in standard big-endian order.
The immutable IV is

    6a09e667 bb67ae85 3c6ef372 a54ff53a
    510e527f 9b05688c 1f83d9ab 5be0cd19.

For 32-bit words define

    s0(z)=ROTR32(z,7)^ROTR32(z,18)^(z>>3)
    s1(z)=ROTR32(z,17)^ROTR32(z,19)^(z>>10)
    S0(z)=ROTR32(z,2)^ROTR32(z,13)^ROTR32(z,22)
    S1(z)=ROTR32(z,6)^ROTR32(z,11)^ROTR32(z,25)
    Ch(e,f,g)=(e&f)^((~e)&g)
    Maj(a,b,c)=(a&b)^(a&c)^(b&c).

Expand `W[t]=W[t-16]+s0(W[t-15])+W[t-7]+s1(W[t-2])` for t=16,...,30.
The constants K[0..30], in hexadecimal, are

    428a2f98 71374491 b5c0fbcf e9b5dba5 3956c25b 59f111f1 923f82a4 ab1c5ed5
    d807aa98 12835b01 243185be 550c7dc3 72be5d74 80deb1fe 9bdc06a7 c19bf174
    e49b69c1 efbe4786 0fc19dc6 240ca1cc 2de92c6f 4a7484aa 5cb0a9dc 76f988da
    983e5152 a831c66d b00327c8 bf597fc7 c6e00bf3 d5a79147 06ca6351.

For t=0,...,30, execute simultaneous updates

    T1=h+S1(e)+Ch(e,f,g)+K[t]+W[t]
    T2=S0(a)+Maj(a,b,c)
    (a,b,c,d,e,f,g,h)=(T1+T2,a,b,c,d+T1,e,f,g).

All schedule, round, and feed-forward additions are modulo 2^32. Add the
working state to the immutable IV and emit all eight resulting 32-bit words.
One such selected-round compression costs one target unit.

## 2. Primitive interface and native storage

The compression invocation reads the sixteen narrow input words and immutable
IV, uses separate schedule/round scratch, and writes eight narrow output words
O[0..7]. It preserves the input block, IV, and caller registers. Its scratch
does not alias the table, saved messages, constants, or caller state. This is
the same mathematical compression, with an explicit read-only input interface;
its internal round work is charged by the selected compression unit. Message
construction, two call/return transfers, and output packing are charged
separately below. No mutable chaining state needs resetting between samples.
Before round t=0, the compression entry initializes the eight working state
words `(a,b,c,d,e,f,g,h)` to the eight standard IV words listed above. The
round updates therefore start from the specified IV on every invocation.

The trusted cost model specifies a classical probabilistic **256-bit word
RAM**, with a 256-bit load or store as a primitive. We use word addresses:
one 256-bit address selects one 256-bit cell. Thus legal word addresses are
0 through 2^256-1. Byte counts measure storage volume; this program never
forms a 261-bit byte address or uses byte addressing. The trusted model does
not require converting a word address to a byte address before a load/store.

Set

    Q = 2^256,
    B = 2^130,
    n = ceil(9943*2^128/10000)
      = 338342757429489114221633372169407132651.

Place the dense arrays at these word addresses:

    back[r]    at r,        0 <= r < n;
    saved_u[r] at n+r,      0 <= r < n;
    saved_w[r] at 2n+r,     0 <= r < n.

At most 2^17 further words account for all native code, public constants,
compression scratch, input/output areas, registers, and fixed working state.
Addressable code and scratch fit in the low interval starting at 3n. The
bound `3n+2^17<B` leaves ample excluded space, including room to account for
register state separately from addressable cells. Unused excluded addresses
need not be allocated or initialized.
The same fixed low-interval reserve contains a uniform native code image and
its loading buffers; no additional setup storage is assumed outside this
reserve.

The sparse table is exactly the address interval `[B,Q)`. Its cell for digest
d is at the native word address `a=d XOR R`, but only if `a>=B`. The mask R is
one fresh uniform 256-bit word drawn during setup, independently of all message
coins. No sparse table exists at excluded low addresses; those addresses are
never read or written by sparse-table lookup. The sparse table and dense arrays
are disjoint, and every native address remains at most Q-1.

Sparse and dense cells initially may contain arbitrary fixed words. Do not
clear them. Initialize count and sample counter i to zero. Initialize padding
W[9..15] once. Load all persistent constants, masks, array bases, n, B, R,
and fixed input/output cell addresses during setup. The finite register
program and compression interface preserve these constants across samples.
Setup, including the random mask and code/constant initialization, costs at
most 2^20 ordinary operations.

For a deterministic setup cap, native code encodes at most four words per
instruction, and code plus scratch/register state uses at most 2^17 words. A
load/initialize pass costs at most 6 operations per word, plus at most 2^16
fixed initialization operations for R, retained registers, constants, masks,
fixed addresses, bases, counters, padding, the uniform code image, and its
loading buffers. Hence

    6*2^17 + 2^16 < 2^20.

## 3. Search algorithm and exact sparse validation

Perform at most n samples. Each uses independent uniform 256-bit draws u,t,
then `w=t AND (2^32-1)`. Therefore messages are iid uniform on the 2^288
specified byte strings; the discarded random bits are charged.

Construct W[0..8], invoke the exact compression, and pack all eight output
words as `d=O[0]*2^224+...+O[7]`, the standard 256-bit big-endian digest.
Compute a=d XOR R. If a<B, skip this sample after charging its construction
and hash. Otherwise load r from the native cell at a. A record is present
exactly when `r<count` and `back[r]=d`.

For a missing record, write count at address a; save d,u,w in the three dense
arrays at count; and increment count. For a present record, stop the batch
and recover the saved message. If the two messages are identical, return FAIL.
Otherwise rehash both complete messages with the specified target, check full
digest equality and byte inequality, and return the collision. A failed check
returns FAIL. Exhausting n samples returns FAIL. There is no restart or
unaccounted success amplification.

To prove validation exact, maintain that each occupied dense index r<count
was created for a distinct included digest back[r], and its sparse address
back[r] XOR R contains r. This holds initially because count=0. An arbitrary
initial sparse word can pass both tests only if its dense record was already
inserted for exactly d; by the invariant that insertion already wrote this
same sparse cell. A missing digest gets a fresh dense index and a unique sparse
address because XOR with R is a bijection. There are no other writes to sparse
cells. Thus arbitrary initial contents cannot create false presence or hide
an inserted included digest. The range test precedes the dependent dense load.

## 4. Distribution-free success, including excluded addresses

Imagine all n iid message draws in advance, even if execution stops early.
They are independent of R. Let D=2^288. For the fixed target, sampled digest
probabilities are `p_y=|H^-1(y) intersect message_domain|/D`, with Q possible
digest values. No property of the fixed SHA-256 map beyond its output width
is assumed.

The probability of n distinct outputs is n!e_n(p), where e_n is the elementary
symmetric sum. Pair averaging proves its maximum is attained by uniform p.
Indeed, among maximizers choose one minimizing sum p_y^2. For two coordinates
a,b and remaining coordinates r,

    e_n(p)=ab*e_(n-2)(r)+(a+b)*e_(n-1)(r)+e_n(r).

Averaging unequal a,b preserves their sum, cannot decrease this expression,
and strictly reduces the squared sum, contradicting the choice. Hence

    Pr(any repeated digest)
      >= 1-product_(j=0)^(n-1)(1-j/Q)
      >= 1-exp(-n(n-1)/(2Q)).

Exact integer arithmetic gives `n(n-1)/(2Q)>0.494316244>0.4943`.
For x=4943/10000 the alternating Taylor upper bound is

    exp(-x) <= 1-x+x^2/2-x^3/6+x^4/24-x^5/120+x^6/720
             = 439199354230678086933157249 /
               720000000000000000000000000
             < 0.6099992.

Thus the repeated-digest probability exceeds 0.3900008. Repeated input has
probability at most `binomial(n,2)/D < 2^-33`. Let E be the event that some
digest repeats but no input repeats. Then

    Pr(E) > 0.3900008 - 2^-33.

On E, select the repeated digest Y whose second occurrence is earliest in
the complete sequence, breaking any remaining tie by the smaller first index.
This selection uses only the message sequence and fixed hash, independently
of R. Conditional on any such sequence, Y XOR R is uniform on Q addresses,
so its exclusion probability is exactly B/Q=2^-126.

If Y is included, both its occurrences are processed and the exact dictionary
finds their collision, unless an earlier included collision already returned
success. On E no earlier identical-input return can cause failure. It follows
that

    Pr(success) >= Pr(E)*(1-B/Q)
                >= Pr(E)-B/Q
                 > 0.3900008 - 2^-33 - 2^-126
                 > 0.39.

This argument protects one designated collision. It does not claim that no
sample is excluded, or that addresses for different digests are independent.
XOR is used only as a uniform random translation of a fixed digest.

## 5. Auditable finite native program

An assignment consisting of a listed arithmetic, Boolean, random, comparison,
load, or store operation costs one ordinary operation. BRTRUE and BRFALSE
each cost one conditional branch; testing the opposite branch sense needs no
separate NOT operation. Instruction sequencing and register operands are native,
without an interpreter. All explicit branches and address arithmetic below are
charged. Fixed input/output addresses and constants are persistent registers
initialized during setup. The unrolled code has no hidden construction loop.

The sample block draws u,t and computes w. Store w at fixed address AW8.
The eight input chunks are then generated from the unchanged register u:

    W0: z=u>>224;                         STORE(AW0,z)
    W1: z=u>>192; z=z AND MASK32;          STORE(AW1,z)
    W2: z=u>>160; z=z AND MASK32;          STORE(AW2,z)
    W3: z=u>>128; z=z AND MASK32;          STORE(AW3,z)
    W4: z=u>>96;  z=z AND MASK32;          STORE(AW4,z)
    W5: z=u>>64;  z=z AND MASK32;          STORE(AW5,z)
    W6: z=u>>32;  z=z AND MASK32;          STORE(AW6,z)
    W7: z=u AND MASK32;                    STORE(AW7,z)

The top chunk needs no mask. These are 7 shifts, 7 ANDs, and 8 stores, or
22 operations. Two explicit transfers surround the compression: branch to a
fixed HASH label, perform the one charged target compression, and branch to
fixed PACK. The primitive preserves u,w and the persistent caller state.

At PACK, execute `d=LOAD(AO0)`. For j=1,...,7, the code contains a separate
unrolled triple `d=d<<32; z=LOAD(AOj); d=d OR z`. This costs 22 operations;
there is no runtime j counter and every output word remains a narrow 32-bit
word. After packing, execute the following program. B_back=0, B_u=n, and
B_w=2n are setup-loaded bases; even addition of the zero base is charged.

    a = d XOR R
    q = (a < B)
    BRTRUE(q, NEXT)
    r = LOAD(a)
    q = (r < count)
    BRFALSE(q, INSERT)
    AR = B_back + r
    v = LOAD(AR)
    q = (v == d)
    BRTRUE(q, TERMINAL)

    INSERT:
    STORE(a, count)
    AR = B_back + count
    STORE(AR, d)
    AR = B_u + count
    STORE(AR, u)
    AR = B_w + count
    STORE(AR, w)
    count = count + 1

    NEXT:
    i = i + 1
    q = (i < n)
    BRTRUE(q, SAMPLE)
    return FAIL                 # explicit exhaustion failure after n samples

The comparison mismatch falls directly into INSERT; INSERT falls into NEXT.
Both early miss and excluded sample use already counted conditional branches.
There is no extra transfer at either join. A successful presence test branches
to terminal handling rather than restarting the sample loop.

TERMINAL is a fixed label outside the sample loop. It branches only to the
fixed terminal labels `TERMINAL_HASH` and `TERMINAL_PACK`, so terminal work
cannot fall through into dictionary code or the sample loop. `TERMINAL`
computes the two saved-message addresses, loads the saved u,w,
checks byte inequality, and returns FAIL on identical inputs. Otherwise it
reconstructs and rehashes both messages at `TERMINAL_HASH`, packs their
outputs at `TERMINAL_PACK`, checks all 256 digest bits and the message
inequality, and emits the two 36-byte messages. All recovery, checks,
construction, serialization, terminal transfers and output use at most 2^14
ordinary operations and two further target evaluations. This ample finite
allowance covers fewer than 512 direct shifts, masks, loads, stores, arithmetic,
comparisons and branches needed for the two fixed-length messages, including
byte serialization. The exhaustion branch after the nth sample performs its
explicit failure return within the same 2^14 terminal bookkeeping allowance;
no further search occurs in terminal handling.

## 6. Operation ledger and exact bounds

The generation/serialization count is

| Work | Ordinary operations per sample |
| --- | ---: |
| Two independent uniform random draws | 2 |
| Extract/store W[0..7] | 22 |
| Mask w and store W[8] | 2 |
| Compression call/return transfers | 2 |
| Load/pack eight digest words | 22 |
| **Generation total** | **50** |

The longest nonterminal dictionary path is a stale in-range sparse record
whose dense digest fails equality:

| Work | Ordinary operations per sample |
| --- | ---: |
| XOR, exclusion comparison/branch | 3 |
| Sparse load, range comparison/branch | 3 |
| Dense address/load/equality/branch | 4 |
| Insertion, including count increment | 8 |
| Sample increment/comparison/branch | 3 |
| **Dictionary and control total** | **21** |

The r>=count insertion path costs 17; an excluded sample costs 6; a present
record exits to terminal handling after 10. Thus **71 ordinary operations per
sample** is a deterministic cap, including all failed/skipped samples. All
table and address operations are ordinary charges in addition to compression.
For at most n samples and one terminal phase,

    H = n+2,
    W = 71n + 2^20 + 2^14,
    T = H + W/2140,
    log2(T) = 128.0388413407722310... < 128.038842.

Setup is included in T, with

    P=2^20/2140,
    log2(P)=8.93660491871149... < 8.936605.

For an exact audit of the decimal logarithmic upper bounds, define the rational

    L=2*sum_(k=0)^15 1/((2k+1)*3^(2k+1)).

The positive-series identity for ln(2) gives L<ln(2). Exact rational arithmetic
verifies, with c=19421/500000=0.038842,

    T/2^128 < sum_(j=0)^10 ((c*L)^j)/j! < exp(c*ln(2)) = 2^c,

and

    (2^20)/(2140*256)
      < sum_(j=0)^20 (((187321/200000)*L)^j)/j!
      < 2^0.936605.

The strict second inequalities follow because the finite positive exponential
sum is below its infinite series and L<ln(2). Actual nonuniform advice is zero;
the schema's nonnegative logarithmic advice bound is 0.

## 7. Memory, limitations and attribution

There are Q-B reserved sparse cells, 3n dense cells, and at most 2^17 words
for all other storage, including code and registers. Every sparse cell counts,
including cells never visited and arbitrary initial contents. Thus

    M <= 32*(2^256-2^130+3n+2^17) < 2^261 bytes.

This storage bound does not append auxiliary arrays beyond a full address
space: auxiliary arrays occupy the excluded low interval and sparse entries
occupy only its complement. The highest sparse address is exactly 2^256-1,
which fits one 256-bit address. All dense sums stay below B. No operation
forms an overflowing scaled byte pointer.

The construction is physically infeasible. Its costs and success are analytic
bounds under the specified word-RAM model, not measured performance. There is
no hidden preprocessing search, seeded-PRNG independence premise, heuristic
list, experimental extrapolation, or computed collision.

Prior public work informed this package: @cadamcat's direct-table/accounting
candidate, @ercumentyildirim's radix direction, @Ryun1's one-block/sample-reduction
note, and @pepedesigner's public one-level direct-table direction, including
the submissions identified as 3e7793eb and 14a4f59. These are credits for prior
ideas, not assertions that their resource claims or review statuses establish
this result. This package makes no claim of novelty, current best score,
promotion, or human acceptance. Fresh review remains required.
