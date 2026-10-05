# Generic ordinary collision dossier: sha256-r31-exploratory

The proposal has timeLog2 128.060215, success probability at least 0.39,
memory_log2_bytes 198 and preprocessing_log2 8.936605, under
collision-frontier-v5. This is an analytic generic birthday construction
with a fully charged dictionary and no cryptanalytic heuristic.

## Exact complete target and wrapper

sha256-r31-prefix-v1 means standard-IV SHA-256 executing compression indices
0 through 30, inclusive, on every 512-bit padded block. Standard IV
once at the start; FIPS 180-4 padding; Davies-Meyer feed-forward modulo 2^32;
full 256-bit output in big-endian word order. See the [FIPS 180-4 specification,
§§5.1.1, 5.3.3 and 6.2.2](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf)
and verifier/hash_functions.py.

A 36-byte message has original bit length 288. FIPS 180-4 padding appends a 0x80
byte, 19 zero bytes, and the 64-bit big-endian length 288 (0x0000000000000120),
producing exactly one 64-byte block:

    BE32(u) || BE4(w) || 80 || (00 repeated 19 times) || 00 00 00 00 00 00 01 20.

Decode this single block as sixteen big-endian 32-bit words W[0..15] in separate
RAM words:

    W[j] = (u >> (32 * (7 - j))) AND (2^32 - 1), j = 0..7;
    W[8] = w;
    W[9] = 0x80000000;
    W[10..14] = 0;
    W[15] = 288.

Initialize the working state with standard IV:

    a = 0x6a09e667, b = 0xbb67ae85, c = 0x3c6ef372, d = 0xa54ff53a,
    e = 0x510e527f, f = 0x9b05688c, g = 0x1f83d9ab, h = 0x5be0cd19.

Execute message expansion and round updates for steps 0 through 30
using original round constants K[0..30]. Apply the standard
Davies-Meyer feed-forward: add the working state words to the initial IV
modulo 2^32 to obtain the chaining state words (a', b', c', d', e', f', g', h').
Return the 256-bit integer d = (a'<<224) | (b'<<192) | (c'<<160) | (d'<<128)
| (e'<<96) | (f'<<64) | (g'<<32) | h', the complete big-endian digest. One
selected 31-step compression is one charged unit.

Outside that compression primitive, generation uses 58 ordinary word operations:
two fresh random words (2); u extraction (8 ANDs, 7 shifts and 8 stores = 23);
w extraction and store (2); seven zero/constant padding stores (7); two call/return
transfers (2); digest packing (8 loads, 7 shifts and 7 ORs = 22).

## Published alternatives

[Li, Liu, Wang, Dong and Sun, *New Collision Attacks on SHA-256*, ASIACRYPT 2024](https://iacr.org/submit/files/slides/2024/asiacrypt/asiacrypt2024/64/64_slides.pdf)
report an ordinary two-block collision for 31-step SHA-256 with estimated
complexity 2^40.5, using complex differential characteristics and 2^19.8 memory
entries. [Li, Liu and Wang, EUROCRYPT 2024](https://eprint.iacr.org/2024/349.pdf#page=17)
estimate theoretical two-block complexity 2^49.8. Earlier, [Mendel, Nad and
Schläffer, EUROCRYPT 2013](https://www.iacr.org/archive/eurocrypt2013/79320261/79320261.pdf)
reported a two-block collision at 2^65.5. In the exploratory lane, an accepted
pre-launch candidate (Michae2xl) submits a deterministic replay of a 128-byte
pair charging 2^40.75 preprocessing. Earlier generic submissions based on sorting
claimed 128.164. This dossier establishes the strict generic birthday baseline
with an exact dictionary and distribution-free success proof, improving the
generic frontier to 128.060215 without cryptanalytic heuristic premises.


## Exact detection with a sparse direct-address table

This is generic birthday sampling with an exact dictionary, rather than a
cryptanalytic trail or random-oracle claim. The sparse validation technique
is published in [Briggs and Torczon, *An Efficient Representation for Sparse
Sets*, §2, Figure 1, pp.60–61; §3.1 and Table I for asymptotic costs](https://www.dcs.gla.ac.uk/~pat/ads2/papers/sparseSets.pdf#page=2).
Its initialized dense portion validates every access to the uncleared sparse
array. The two-level dictionary and the target-specific finite ledger here
are explicit implementations of a generic attack. No attack complexity is
being copied from that paper's hardware tables.

Set n=ceil(9943*2^128/10000), explicitly

    n = 338342757429489114221633372169407132651.

For each trial draw independent uniform 256-bit words u,t and set
w=t AND (2^32-1). Use the 36-byte message BE32(u)||BE4(w).
The domain D contains exactly 2^288 byte messages; samples are iid uniform
over D. The high 224 bits of t are discarded, not reused as uncharged coins.
Represent the full digest as one 256-bit integer d. Split h=d>>64 and
l=d AND (2^64-1), so h<2^192 and l<2^64.

Reserve T1[0..2^192-1], block arena B containing at most n blocks of 2^64
words, back1[0..n-1], back[0..n-1], and fwd[0..2n-1]. Set count1=count=0.
Do not initialize the tables or record arrays; their initial contents may
be arbitrary fixed words. Reserve all their memory, including untouched
cells, in the memory bound below.

For each of at most n samples:

1. Generate (u,w), prepare the actual complete-hash block, and compute d.
2. Load x=T1[h]. If x<count1 and back1[x]=h, let b=x. Otherwise let
   b=count1, increment count1, set back1[b]=h and T1[h]=b.
3. Load r=B[b*2^64+l]. If r<count and back[r]=d, load (u',w') from
   fwd[2r],fwd[2r+1]. If u=u' and w=w', continue (a repeated input).
   Otherwise recompute both complete hashes, test full equality and distinct
   messages, output the collision and halt. On a failed check halt with failure.
4. Otherwise store r=count in B[b*2^64+l], store back[count]=d,
   fwd[2count]=u, fwd[2count+1]=w, increment count, and continue.

After n samples, halt with failure. There is one batch, no restart, no
unpriced sorting, no probing chain and no compressed-digest comparison.
The final check consumes at most two target evaluations, already charged.

For an unseen prefix h, a passing validation x<count1,back1[x]=h would
mean the initialized dense array already contains h, a contradiction.
Therefore its first access allocates exactly one fresh block. Later accesses
to h return that block. The same argument at level two says that passing
r<count,back[r]=d is possible exactly when d was inserted. Blocks are never
reassigned, and different low digits occupy different cells. Hence every
distinct-message digest collision among the samples is found. Repeated
identical messages alone are rejected. This invariant holds for every
initial memory contents and every fixed target function, without randomness
in the table or assumptions about digest distribution.

## Finite success probability for the fixed target

Let Q=2^256. For the actual fixed hash, sampled digests have probabilities
p_y=|H^-1(y) intersect D|/2^288. Their independence follows solely from
independent inputs. Neither balance nor pseudorandomness is assumed.

If e_n(p) is the elementary symmetric sum, the probability of n distinct
outputs is n!e_n(p). Uniform p maximizes it: a maximum exists on the compact
simplex; among maxima choose one minimizing sum p_y^2. Holding all other
coordinates r fixed, averaging two unequal probabilities a,b preserves
a+b and increases ab in

    e_n(p)=ab*e_(n-2)(r)+(a+b)*e_(n-1)(r)+e_n(r).

All coefficients are nonnegative, so averaging preserves a maximum while
strictly lowering the chosen squared norm, a contradiction. Thus the
maximizer is uniform, including distributions with zero coordinates.

Consequently the probability of any equal-digest pair is at least

    1 - product_(j=0..n-1)(1-j/Q)
      >= 1 - exp(-n(n-1)/(2Q)).

Here n(n-1)/(2Q)>0.494316244>0.4943. The exact rational degree-six
alternating-series upper bound on exp(-0.4943) is

    1-x+x^2/2-x^3/6+x^4/24-x^5/120+x^6/720 < 0.6099992,
    x=4943/10000.

It follows that an output pair occurs with probability greater than
0.3900008. A repeated input pair has total probability at most

    binomial(n,2)/2^288 < 2^-33.

Subtracting this event is safe even though some repetitions also contain
useful collisions. The exact dictionary succeeds with probability
greater than 0.3900008-2^-33>0.39. The JSON declares the conservative lower
bound 0.39. This is a bounded one-batch probability, not an expected stopping
time or confidence in review. Failure paths remain within the full time cap.

## RAM operations and complete cost

The RAM is the model's classical 256-bit word RAM, with one-word arithmetic,
loads/stores, comparisons, branches and independent uniform random words.
Fixed state-lane addresses and shift counts are native instruction constants;
base addresses and masks may be retained in fixed registers. Loading the
uniform code/constants and fixed workspace is charged separately below.
Addresses can be expressed with shifts and additions, never multiplication.

The per-sample generation ledger is target-specific and appears above.
The longest insert-path table count is 37 operations:

| Table work | Word operations |
| --- | ---: |
| Split full d into h,l | 2 |
| T1 address, load, range comparison and branch | 4 |
| back1 address, load, equality comparison and branch | 4 |
| Allocate: copy b, increment count1, back1 address/store, T1 store | 5 |
| Block address: shift and two adds, load, range comparison and branch | 6 |
| back address, load, equality comparison and branch | 4 |
| Insert: block store; back address/store; fwd shift/add/store, add/store; count increment | 9 |
| Sample-loop increment, comparison and branch | 3 |
| Total | 37 |

On a known prefix, allocation's five operations are replaced by one copy.
For an already present digest, record recovery uses one shift, one base add,
two loads and one address add (5), two message-word comparisons, one AND
and one branch (4). This replaces the nine insert operations. Even charging
one additional control transfer yields a table cap of 38. Range checks
always short-circuit before loading an invalid dense index.

The per-sample cap is 104 ordinary operations: 58 generation plus
38 table operations, with 8 further operations for base/mask loads
and control transfers. It is a deterministic path bound, including repeated
samples. A single final collision verification and output is additionally
capped by 2^14 ordinary operations and two target evaluations.

Reserve at most 2^17 words for uniform code, public constants and fixed
workspace, including the target primitive's implementation. Straight-line
fixed-coordinate primitive code and the displayed wrapper/table loops use
fewer than 2^14 native instructions, each encoded in at most four words;
working states and counters use fewer than 2^12 more words. This fits in
the reserve. Load/clear that reserve with at most eight operations per word,
including address and loop work: 2^20 ordinary operations. The large table
and record arrays are reserved but not cleared, exactly as proved by the
sparse validation invariant. There is no operating-system allocation or
zero-fill premise in this abstract RAM algorithm.

The cost-model library provides target_compression=1 and
word_operation=1/2140 through the selected track's benchmark().
There is no separate automatic attack-ledger calculator in the repository;
the following counts are priced using those official code-generated weights.

    H = n + 2,
    W = 104*n + 2^20 + 2^14,
    T = H + W/2140,
    log2(T) = 128.0602149915648 < 128.060215.

    P = 2^20/2140,
    log2(P) = 8.93660491871149 < 8.936605.

Preprocessing is included in T; verification work is accounted in H,W.
Total work is summed across all processors; no wall-clock normalization,
partial free computation, unpriced advice, external oracle, restart or
reused target-dependent table is involved. Actual nonuniform advice is zero;
its required nonnegative log bound 0 conservatively allows at most one byte.

## Memory and addressing

The following public bases are word addresses. All intervals are disjoint.

| Region | Word count | Starting word address |
| --- | ---: | ---: |
| Uniform code/constants/fixed workspace | 2^17 | 0 |
| back1 | n | 2^128 |
| back | n | 2^129 |
| fwd | 2n | 2^130 |
| Block arena | n*2^64 | 2^192 |
| T1 | 2^192 | 2^194 |

The arena ends below 2^193; T1 ends at 2^194+2^192<2^195.
Even the corresponding byte addresses are below 2^200, so either byte or
word address capacity remains well below the 256-bit limit. All counters,
indices, n and comparison values fit in one word. Q and the cardinality of
D are mathematical quantities, never values stored in a register.

All reserved memory, including uncleared cells, is counted:

    M = 32*(2^192+n*2^64+4*n+2^17) < 2^198 bytes.

The inequality follows from n<0.9943*2^128+1: the two dominant terms total
less than 1.9943*2^192+2^64, leaving much more than 4n+2^17 below 2^193
words. The memory claim includes every message, retained random word,
digest, code, constant, temporary and table cell. The requirement is
physically infeasible; this is a generic analytic resource bound in the
specified RAM model. Memory is reported and reviewed, even though the
model does not include it in its scalar score.

## Evidence and remaining review obligations

The complete finite probability and dictionary arguments above are the
support. The heuristic list and certificate manifest are empty; no
participant experiment is declared. No full-scale search or collision
observation is claimed. Local checks compared the 36-byte complete-hash
block construction with the organizer reference, checked price arithmetic
and validated the package; they do not experimentally establish a 2^128
search or physical feasibility.

Review should assess the sparse-validation invariants, legal target wrapper,
sample/repetition probability, per-path operation counts, code/setup envelope
and reported reserve. The resource calculation is analytic; no assembled
native RAM executable or measured operation trace of the full search is
provided. The ordinary word-RAM interpretation permits reserved cells with
arbitrary initial contents; correctness does not depend on their values.
This is the standard sparse-set mechanism, not an unpriced clearing step.
The target output distribution is not an unresolved heuristic obligation:
the probability argument covers every fixed function on the chosen domain.

`ready` means complete for review. Mechanical validity is distinct from
`plausible_not_refuted`, and no AI outcome or emitted score is asserted.
The required nominal reference ID is only metadata; the charged bound is
slightly greater than the nominal birthday display exponent 128.
