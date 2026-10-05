# SHA-256 r31 generic collision construction

This draft targets `sha256-r31-exploratory`, profile `sha256-r31-prefix-v1`,
under `collision-frontier-v5`. It is an analytic, infeasible-memory generic
construction and supplies no computed collision or practical-attack claim.

## Exact target and one-block hash

Define `BE_k(v)` as the `k`-byte big-endian encoding of integer `v`. The target
is standard-IV SHA-256 compression indices 0 through 30, on every padded block,
with full feed-forward and the complete 256-bit big-endian output. A sampled
message is the 36-byte string

    m(u,w) = BE32(u) || BE4(w),  0 <= u < 2^256, 0 <= w < 2^32.

Its bit length is 288, and its single padded block is

    BE32(u) || BE4(w) || 80 || 00 repeated 19 times || BE8(288).

The sixteen big-endian words are `W[0..7]` from `u`, `W[8]=w`,
`W[9]=0x80000000`, `W[10..14]=0`, and `W[15]=288`. Initialize
`(a,b,c,d,e,f,g,h)` from

    6a09e667 bb67ae85 3c6ef372 a54ff53a
    510e527f 9b05688c 1f83d9ab 5be0cd19.

For 32-bit words define

    s0(z)=ROTR32(z,7)^ROTR32(z,18)^(z>>3)
    s1(z)=ROTR32(z,17)^ROTR32(z,19)^(z>>10)
    S0(z)=ROTR32(z,2)^ROTR32(z,13)^ROTR32(z,22)
    S1(z)=ROTR32(z,6)^ROTR32(z,11)^ROTR32(z,25)
    Ch(e,f,g)=(e&f)^((~e)&g)
    Maj(a,b,c)=(a&b)^(a&c)^(b&c).

Expand `W[t]=W[t-16]+s0(W[t-15])+W[t-7]+s1(W[t-2])` for `t=16,...,30`.
The round constants `K[0..30]`, in hexadecimal, are

    428a2f98 71374491 b5c0fbcf e9b5dba5 3956c25b 59f111f1 923f82a4 ab1c5ed5
    d807aa98 12835b01 243185be 550c7dc3 72be5d74 80deb1fe 9bdc06a7 c19bf174
    e49b69c1 efbe4786 0fc19dc6 240ca1cc 2de92c6f 4a7484aa 5cb0a9dc 76f988da
    983e5152 a831c66d b00327c8 bf597fc7 c6e00bf3 d5a79147 06ca6351

For `t=0,...,30`, execute simultaneous updates

    T1=h+S1(e)+Ch(e,f,g)+K[t]+W[t]
    T2=S0(a)+Maj(a,b,c)
    (a,b,c,d,e,f,g,h)=(T1+T2,a,b,c,d+T1,e,f,g).

All schedule, round, and feed-forward additions are modulo `2^32`; Boolean
operands are 32-bit words. Add the working state to the immutable IV and emit
the eight resulting words as the full digest `d`. One selected compression is
one charged target unit.

The compression primitive reads the immutable fixed IV and input block and
writes a separate output-state scratch area. There is no mutable chaining state
to reset across samples. The wrapper preserves the current `u,w` registers;
outside the one charged target unit, it pays only for constructing the block,
two call/return transfers, and digest packing.

## Direct-address collision search

Set

    n = ceil(9943*2^128/10000)
      = 338342757429489114221633372169407132651.

Draw `n` iid uniform messages by drawing independent uniform 256-bit `u,t` and
setting `w=t AND (2^32-1)`. The discarded bits of `t` are not uncharged coins.
For digest `d`, set `h=d>>64` and `l=d AND (2^64-1)`, with `h<2^192` and
`l<2^64`.

Reserve sparse tables `T1[0..2^192-1]`, an `arena` containing at most `n`
blocks of `2^64` words, `back1[0..n-1]`, `back[0..n-1]`, and
`fwd[0..2n-1]`. Set `count1=count=0`; do not initialize these tables. Their
initial contents may be arbitrary fixed words, and every reserved cell counts
toward memory.

For each sample, compute its complete digest, then:

1. Load `x=T1[h]`. If `x<count1` and `back1[x]=h`, use `b=x`; otherwise use
   `b=count1`, increment `count1`, store `back1[b]=h`, and set `T1[h]=b`.
2. Load `r=arena[b*2^64+l]`. If `r<count` and `back[r]=d`, load the stored
   message words from `fwd[2r],fwd[2r+1]` and compare them with the current
   `u,w`. If they are equal, retain and reject this repeated input, then
   continue. Otherwise rehash both complete messages, check full digest
   equality and byte inequality, and return the pair; a failed check returns
   `FAIL`.
3. If no record was found, store `arena[b*2^64+l]=count`, `back[count]=d`,
   `fwd[2count]=u`, and `fwd[2count+1]=w`; then increment `count` and continue.

After the single batch, return `FAIL`; there is no restart. The two-level sparse
validation invariant is exact for arbitrary initial table contents: a passing
level-one check is possible exactly for an allocated prefix, and a passing
level-two check exactly for an inserted digest. Blocks are never reassigned and
different low digits use different cells. Thus every repeated digest with no
repeated input is found.

## Distribution-free success

Let `Q=2^256` digest values and `D=2^288` messages. For the fixed target hash,
sampled digests are iid with probabilities `p_y=|H^-1(y) intersect D|/2^288`.
No balance, random-oracle, differential, or PRNG-independence premise is used.

If `e_n(p)` is the elementary symmetric sum, the probability of `n` distinct
outputs is `n!e_n(p)`. Pair averaging proves the uniform vector maximizes this:
at a maximizer choose one minimizing `sum p_y^2`; with other coordinates `r`,

    e_n(p)=ab*e_(n-2)(r)+(a+b)*e_(n-1)(r)+e_n(r).

Averaging unequal `a,b` preserves their sum, increases `ab`, and strictly lowers
the squared sum, a contradiction. Hence

    Pr(repeated digest) >= 1-product_(j=0)^(n-1)(1-j/Q)
                       >= 1-exp(-n(n-1)/(2Q)).

The exact integer arithmetic gives `n(n-1)/(2Q)>0.494316244>0.4943`. For
`x=4943/10000`, the alternating Taylor bound is

    1-x+x^2/2-x^3/6+x^4/24-x^5/120+x^6/720 < 0.6099992.

Thus the repeated-digest probability exceeds `0.3900008`. The repeated-input
event has probability at most `binomial(n,2)/2^288 < 2^-33`. The event “a
repeated digest and no repeated input” is sufficient for success, so subtraction
of the repeated-input event is valid even though some repeated inputs may also
contain useful collisions. Therefore

    Pr(success) > 0.3900008 - 2^-33 > 0.39.

The exact Taylor rational numerator used for the strict decimal check is

    439199354230678086933157249 /
    720000000000000000000000000 < 0.6099992.

The JSON reports the conservative lower bound `0.39`. This is one fully
charged batch, not expected stopping time or review confidence.

## Native operation ledger

The word RAM executes the fixed finite register program directly. Instruction
sequencing is native control; explicit branches, data loads/stores, address
arithmetic, random draws, comparisons, and all other ordinary operations are
charged. No interpreter or optional fetch/spill multiplier is assumed.

Generation uses 58 ordinary operations: two random draws; `u` extraction (8
ANDs, 7 shifts, 8 stores = 23); `w` extraction and store (2); seven padding or
constant stores (7); two call/return transfers (2); and digest packing (8
loads, 7 shifts, 7 ORs = 22). The longest dictionary insertion path is 37:

| Work | Operations |
| --- | ---: |
| Split digest into `h,l` | 2 |
| `T1` address, load, range test, branch | 4 |
| `back1` address, load, equality test, branch | 4 |
| Allocate prefix block and store | 5 |
| Block address, load, range test, branch | 6 |
| `back` address, load, equality test, branch | 4 |
| Insert block, back and message records | 9 |
| Sample-loop increment, test, branch | 3 |
| **Total** | **37** |

Known prefixes replace allocation with one copy. Existing records avoid the
nine insert operations; recovering the stored message costs five operations,
and comparing it with the current `u,w` costs four. Charging one extra control
transfer gives a table cap of 38. Eight base/mask loads and control transfers
produce the deterministic cap `104=58+38+8` ordinary operations per sample,
including repeated samples.
Final verification/output costs at most `2^14` ordinary operations and two
target evaluations.

Reserve at most `2^17` words for native code, public constants, target state,
and fixed workspace. Fewer than `2^14` native instructions and fewer than
`2^12` further state words fit this reserve. Loading it costs at most `2^20`
ordinary operations. The total is

    H = n+2,
    W = 104n + 2^20 + 2^14,
    T = H + W/2140,
    log2(T)=128.0602149915648 < 128.060215,

and

    P=2^20/2140,
    log2(P)=8.93660491871149 < 8.936605.

For an exact audit trail for these logarithmic bounds, let

    L=2*sum_(k=0)^15 1/((2k+1)*3^(2k+1)).

This rational satisfies `L < ln(2)`. Exact rational arithmetic verifies

    T/2^128 < sum_(j=0)^10 (((12043/200000)*L)^j)/j! < 2^0.060215

and

    (2^20)/(2140*256) < sum_(j=0)^20 (((187321/200000)*L)^j)/j! < 2^0.936605.

Preprocessing is included in `T`; actual nonuniform advice is zero, with the
schema's nonnegative log bound `0`.

## Memory and limitations

Use disjoint public word-address intervals for code/workspace (`2^17` words),
`back1` (`n`), `back` (`n`), `fwd` (`2n`), the block arena (`n*2^64`), and
`T1` (`2^192`). All corresponding byte addresses, counters, and indices fit
under 256 bits. Every reserved cell, including uncleared cells, is counted:

    M=32*(2^192+n*2^64+4n+2^17) < 2^198 bytes.

The construction is physically infeasible but valid in the specified generic
RAM model. It has no experiments, executable candidate, computed witness,
hidden search, or heuristic list. Prior public research informed this package:
@cadamcat's direct-table/accounting candidate, @ercumentyildirim's radix
direction, and @Ryun1's one-block/sample-reduction note. Those contributions
are credited as unpromoted prior work; this draft makes no claim of novelty,
best score, promotion, or human acceptance. Fresh review remains required.
