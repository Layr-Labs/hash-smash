# sha1-r80: a fully accounted finite-domain collision search

Selected lane: **exploratory**. Selected track: **sha1-r80-exploratory**.
This package claims an ordinary complete-message collision algorithm for exactly
`sha1-r80-prefix-v1` under `collision-frontier-v3`. All resource figures below are
upper bounds, not measurements. This is an analytic baseline proposed for review;
`ready` is not qualification, an AI verdict is not mathematical proof or human
acceptance, and no executed collision or completed full-size search is asserted.

## 1. Exact hash and message family

Let N = 2^80, M = 2^160, and D be all 32-byte strings, with |D| = 2^256.
Each message is the big-endian encoding of one unsigned 256-bit integer x,
including leading zero bytes. Its original bit length is 256, below 2^64.
Let h(x) be its complete selected-profile hash, interpreted as an unsigned
160-bit integer with 96 leading zero bits in a 256-bit storage word.

The complete padded block is the 32 message bytes, byte 0x80, 23 zero bytes,
and the eight-byte big-endian encoding of 256. Thus it is exactly 64 bytes.
Represented by two consecutive big-endian 256-bit words, it is
`(x, (1 << 255) OR 256)`. No second block is used.

For completeness the selected compression is defined here. Parse that block as
16 big-endian 32-bit words W[0],...,W[15]. For t = 16,...,79 set
W[t] = ROL32(W[t-3] XOR W[t-8] XOR W[t-14] XOR W[t-16], 1).
Initialize (a,b,c,d,e) from the fixed IV
(0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476, 0xc3d2e1f0).
For each original index t = 0,...,79, choose:

| t | f(b,c,d), with NOT restricted to 32 bits | K[t] |
| --- | --- | --- |
| 0 through 19 | (b AND c) OR ((NOT b) AND d) | 0x5a827999 |
| 20 through 39 | b XOR c XOR d | 0x6ed9eba1 |
| 40 through 59 | (b AND c) OR (b AND d) OR (c AND d) | 0x8f1bbcdc |
| 60 through 79 | b XOR c XOR d | 0xca62c1d6 |

Compute v = (ROL32(a,5) + f(b,c,d) + e + K[t] + W[t]) modulo 2^32,
then simultaneously replace (a,b,c,d,e) by (v,a,ROL32(b,30),c,d).
After index 79, add the five working words respectively to the five original
IV words modulo 2^32. Concatenate all five resulting words in their original
order, each in big-endian byte order, to obtain all 20 digest bytes.
Each message and each verification starts anew with that same fixed IV.
This is all 80 prefix rounds, full feed-forward and full output; there is no
free-start choice, compression-only target, truncation or altered padding.
The organizer model charges this selected target compression one unit; its
internal schedule/round arithmetic is part of that primitive. The outer block
construction, IV loading, serialization and call bookkeeping are also charged.

## 2. Fully specified algorithm and data structures

Use two fixed RAM address ranges A and B, each containing N two-word records.
A record is `(digest, message_integer)`, occupying exactly 64 bytes.
Its order is lexicographic unsigned order: digest first, message integer second.
A record at index i occupies words `base + 2*i` and `base + 2*i + 1`.
The largest address, counter or end pointer fits well inside one 256-bit word:
the two arrays together have 4N = 2^82 words. There are no pointers per record,
variable-size messages, recursive calls, trees, buckets or hidden data structures.
The message word itself retains the entire original input and the random draw.

Initialize only the fixed code, constants and scratch state. Reserve the two
address ranges without a clearing pass: every array cell is written before its
first read. Reserving addresses in this RAM model is not a physical allocation
or a demand for a preinitialized exponential data file. All actual stores appear
in generation or merging below.

The following pseudocode specifies the algorithm, not a host program or a
submitted executable experiment. READ and WRITE mean the two-word operations
at the address just specified. Assignment/control operations are charged using
the explicit lowering budget in section 5.

```text
N := 1 << 80
for i := 0,...,N-1:
    x := one fresh independent uniform random 256-bit word
    d := h(x), using the complete one-block computation in section 1
    WRITE(A,i,(d,x))

width := 1
while width < N:                         # exactly 80 passes
    left := 0
    while left < N:
        middle := left + width
        right := middle + width         # 2*width divides N
        i := left; j := middle; k := left
        while k < right:
            if i == middle:
                source := j; j := j+1
            else if j == right:
                source := i; i := i+1
            else if READ(A,i) <= READ(A,j) in lexicographic order:
                source := i; i := i+1
            else:
                source := j; j := j+1
            WRITE(B,k,READ(A,source))
            k := k+1
        left := right
    swap the base addresses of A and B
    width := width << 1

for k := 1,...,N-1:
    (d0,x0) := READ(A,k-1)
    (d1,x1) := READ(A,k)
    if d0 == d1 and x0 != x1:
        recompute e0 := h(x0) and e1 := h(x1) from the fixed IV
        compare x0 != x1 and e0 == e1 == d0 as full-width values
        if both comparisons hold:
            return the two 32-byte big-endian messages x0,x1 and SUCCESS
        else:
            return FAILURE             # unreachable under the RAM/hash definition
return FAILURE
```

Exactly N draws and hash evaluations are made before sorting, even on an
unfavorable coin outcome. The scan stops at its first genuine candidate pair;
there are at most two further complete hash evaluations. There is only one
batch, no restart, no success amplification, no nonce rejection/resampling,
no omitted failed trial and no externally supplied table or collision.

## 3. Correctness of collision detection

Initially each stored digest is exactly the complete h of its accompanying
message. A merge copies both words together, so this invariant is preserved.
Before a pass of width w, each length-w run is lexicographically sorted.
At every merge step the first unconsumed record of each nonempty run is its
least remaining record; choosing the lesser head (left head on a tie) yields
the least remaining record of the union. Exhausting a run leaves only the
other run. Thus the output run of length 2w is sorted and is a permutation
of the two input runs. Induction from singleton runs through 80 passes proves
that the final array is a sorted permutation of the entire sampled multiset.

Every equal-digest group is contiguous, and its message words are sorted.
If any group contains two different message words, some adjacent pair in that
group differs: otherwise all adjacent words, and hence all words in the group,
would be equal. The scan therefore finds a genuine collision whenever any two
distinct sampled inputs have equal h values. Repetitions of one input alone
are skipped and are never a success. Reverification cannot fail in this
specified ideal RAM computation because the records still contain exact h
values; it explicitly checks full digests and distinct full messages.
Every SUCCESS therefore returns distinct permitted messages with equal full
`sha1-r80-prefix-v1` hashes. Conversely any genuine collision among the draws
is detected, including when repeated copies of some inputs also occur.

## 4. Unconditional algorithmic success probability

The target h is fixed. The sole probability space is the N fresh independent
uniform 256-bit random words expressly provided and charged by the organizer's
model. This is not a claim that a seeded PRNG supplies independent words, nor
that SHA-1 is a random function. There is no randomness assumption about h.
For each possible digest y, put p[y] = |{x in D : h(x)=y}| / 2^256.
Applying a fixed function separately to independent input draws produces
independent output draws with this fixed distribution p; output uniformity,
balance and collision-event independence are not needed.

For N <= M, the probability that all N outputs are distinct is N! e_N(p),
where e_N is the sum of products over all N-element subsets of the M output
labels (include zero-probability labels). Its maximum over the probability
simplex is attained by the uniform vector. Here is a self-contained proof.
Fix all coordinates except a,b; the polynomial has the form
A + (a+b)B + ab C with C >= 0. Replacing a,b by their mean preserves a+b
and increases ab, so it cannot decrease the polynomial. The simplex is
compact; choose a maximizer with minimum sum of squared coordinates among
maximizers. If any two coordinates differ, averaging either strictly
increases the polynomial, contradicting maximality, or keeps its value and
strictly decreases that sum of squares, contradicting the tie-break.
Thus that maximizer is uniform, and

```text
P(no repeated output) <= N! binom(M,N) / M^N
                      = product from i=0 to N-1 of (1-i/M)
                      <= exp(-N(N-1)/(2M)).
```

The final inequality uses 1-u <= exp(-u) for 0 <= u < 1, proved for example
by integrating the inequality 1/(1-u) >= 1 for -log(1-u).
Let E be the event of a repeated output and R the event of a repeated input.
For each input-index pair, equality has probability exactly 2^-256, so the
union bound gives P(R) <= N(N-1)/(2*2^256) < 2^-97.
On E outside R there are two distinct colliding inputs. Section 3 therefore
implies, without asserting independence of E and R,

```text
P(SUCCESS) >= P(E) - P(R)
           >= 1 - exp(-N(N-1)/(2M)) - N(N-1)/(2*2^256).
```

Here N(N-1)/(2M) = 1/2 - 2^-81 > 499/1000. The positive exponential
series gives the following exact rational lower bound, so no floating-point
birthday approximation is being used:

```text
exp(499/1000) > 1 + 499/1000 + (499/1000)^2/2 + (499/1000)^3/6
             = 9865254499 / 6000000000.
6000000000 / 9865254499 < 609/1000
because 6000000000000 < 6007939989891.
```

Consequently P(SUCCESS) > 391/1000 - 2^-97 > 39/100, since 2^-97 < 1/1000.
The claim conservatively records success_probability = 0.39. It refers to
algorithmic success, not confidence in this argument or in a reviewing model.
The proof holds for every fixed function D -> {0,1}^160 and therefore for the
particular complete 80-round hash just defined, including nonuniform outputs.

## 5. Charged time in the 256-bit word-RAM model

Each load/store, add/subtract, shift, bitwise operation, comparison, conditional
branch and random-word request costs one unit. Register copies can be charged
as one word operation too. No multiplication, division, library sort, comparison
of arbitrary-size integers, unbounded instruction or free oracle lookup is used.
All indices and constants fit one word; a factor two is a shift. Record key
comparison uses at most three scalar comparisons and three branches: compare
the digests in each direction, then the messages if digests tie.
READ of a two-word record costs at most five primitives (shift index, add base,
load first word, add one to address, load second word). WRITE costs at most five
with the analogous stores. Simultaneous assignments lower to a fixed temporary.

These deliberately loose budgets dominate the direct lowering of the displayed
loops. A scalar loop test is one comparison and one branch; increments are
one addition, and there are only the explicitly displayed finite cursors.

| Component | Primitive-unit upper bound | Reason |
| --- | ---: | --- |
| Fixed program/constants/scratch setup | 2^20 | Initialization bound justified below; no search or precomputed advice |
| Generation of N complete records | 128N | Per record: 1 random request; at most 32 IV/block construction, loading and serialization operations; 1 target compression; 5 for record storage; the remaining 89 cover copies, loop control and temporaries |
| Each full merge pass | 128N | Per emitted record at most 96, plus at most 32 per merged run and 32 per pass, as expanded below |
| All 80 merge passes | 10240N | Exactly 80 times the preceding bound, including failure outcomes |
| Adjacent-record scan | 64N | Two READs cost 10, digest/message comparisons and branches at most 8, cursor/address and loop work below 46; includes the no-match case |
| Final two hashes, checks, result serialization | 256 | At most 128 per message, including complete one-block hashes and returned 32-byte strings |

For the merge bound, per emitted record allow: 8 units for loop/exhaustion
comparisons and branches; 16 for the two head READs and lexicographic decision;
16 for reading the selected record and writing both destination words; and
32 for source selection, cursor increments/copies, addresses and control
transfers. This sum is 72, below the allowance 96. The extra allowance covers
end-of-loop branching without relying on branch prediction or amortized hash
cost. The per-run allowance 32 covers left/middle/right construction, cursor
initialization, final loop exit and advancing the outer cursor. A pass contains
N/(2w) <= N/2 runs, so its total is at most 96N + 16N + 32 <= 128N.
The last inequality holds for this N; pass setup, pointer swap and width shift
fit the stated 32. No record comparison reevaluates a hash.

For fixed storage/setup one may encode the straight-line control code for these
loops and the READ/WRITE/comparison macros in at most 4096 instructions, each
with at most four 256-bit words (opcode and up to three operands). This is a
loose direct construction: fewer than 128 displayed scalar statements, each
expanding into fewer than 32 allowed instructions; loops use backward branches
rather than unrolling N iterations or 80 passes. Hash is the charged target
compression primitive, not an embedded attack library. Thus instruction storage
is at most 2^19 bytes. Reserve a further 2^19 bytes for constants, register
slots, two current padded blocks, IVs, digest serialization, result messages,
and all scratch state. Even storing the 80 schedule words uses only 2560 bytes
when each is placed in an entire 256-bit word. Loading and initializing all
these at most 2^15 words, with at most 16 operations per word, costs at most
2^19 operations, below the setup allowance 2^20. This allocation includes code
and its initialization rather than treating it as free advice.

The final worst-case bound, for every coin outcome, is therefore

```text
T <= 2^20 + 128N + 10240N + 64N + 256
   = 2^20 + 10432N + 256
   < 16384N = 2^94.
```

There is no preprocessing search, discarded random batch or separate success
amplification to add. The bounds charge all N trials including failures and
any repeated input. Online randomness is N random-word operations, producing
256N bits in total; no exponential extra random tape is retained outside the
already charged message records. Claimed time_log2 = 94 is an upper bound on
all primitive units, whose common scoring name is target-compressions.

## 6. Peak memory, data, advice and nominal comparison

Both arrays must coexist throughout sorting. Each holds 2N words of 32 bytes,
so they jointly occupy 128N = 2^87 bytes. The fixed code/constants/scratch cap
above adds at most 2^20 bytes, including temporary records and both returned
messages. Addresses, loop variables and base pointers are inside that cap.
No recursive merge stack or retained randomness beyond the arrays exists.
Therefore peak memory <= 2^87 + 2^20 < 2^88 bytes, establishing
memory_log2_bytes = 88. The 256-bit address space easily covers this memory.
This is a theoretical RAM budget, not a claim that existing physical hardware
can carry out this search.

Data is chosen-message hash work, with no externally obtained dataset: N random
sampled messages and at most two selected messages recomputed for verification.
Thus at most N+2 complete one-block evaluations, fewer than 2^81. There are at
most N distinct chosen messages; the verification inputs are retained members
of the same sample. data_log2 = 81 is the conservative log2 upper bound on
message-evaluation count, not input bytes or memory. The actual sampled input
volume is 32N bytes (at most 32(N+2) including verification processing); this
is already represented by charged work/storage, not uncharged external data.

Preprocessing is only fixed program/constant/scratch initialization, bounded
by 2^20 primitive units and included in total T. Hence preprocessing_log2 = 20.
There is zero nonuniform advice and no precomputed collision, external search,
secret seed or target-specific table. The schema's nonnegative log field cannot
encode log2(0); nonuniform_advice_log2_bytes = 0 means the safe upper bound of
one byte on the actual zero advice bytes. The uniform program and public fixed
hash constants remain charged in memory and setup, independent of that field.

The claimed scalar would be 94 + 88 = 182 if the selected lane qualifies and
the organizer emits a score. The required baseline_improved identifier
`sha1-r80-nominal-v2` points to an organizer nominal reference exponent 80.
That entry is not an established attack, qualified baseline, security bound
or proved time-memory implementation. This submission does not claim to beat
that display number, claim cryptanalytic novelty, or establish Pareto dominance.
The purpose is a complete conservative baseline under the actual charged model.

## 7. Evidence scope and independent lane binding

heuristics is empty because the probability and resource arguments above use
only the fixed target definition, the organizer's explicit random-word RAM
model, and proved finite mathematical statements. There is no empirical
extrapolation, output-balance premise, PRNG premise or external citation needed
to assess a material step. A finite toy run would not execute this resource
regime; no experiment is declared and no candidate program is supplied.
The version-2 certificate manifest is intentionally empty: no explicit witness
has been generated, and none is needed for the analytic existence/success claim.

This package binds its own selected exploratory lane and exact 80-round target.
Its rigorous counterpart may carry the same full argument, but has its own
lane binding, candidate fingerprint and required selected-lane review. A verdict
or score on another package or lane is not evidence of this package's qualification.
