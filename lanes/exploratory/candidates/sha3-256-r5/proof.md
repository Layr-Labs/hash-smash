# A tight generic birthday collision for sha3-256-r5-exploratory

The scalar below is `time_log2` under `collision-frontier-v5`. Memory
remains a separately reported resource bound.

This package targets sha3-256-r5-prefix-v1. It proposes a classical
randomized algorithm with success at least 0.45, total charged time at
most 2^128.5 target-compression equivalents, and peak memory at most
2^136 bytes. These are conservative analytical upper bounds, not measured
execution costs. The claimed scalar is 128.5.

The proof uses no distributional property of the selected hash and no
distributional property of the digests: every fixed function from the
chosen message domain to 256-bit strings satisfies both its probability
bound and the deterministic time cap. Fresh independent uniform coins are
the explicit RAM model's random-word primitive. No PRNG, random-oracle,
round-independence, probing-model, or differential heuristic is assumed.
Accordingly the heuristic list is empty.

## 1. Exact complete hash

Each message is exactly 64 bytes, of bit length 512 < 2^64. Two 256-bit
words u,v encode m = LE256(u) || LE256(v): the little-endian 32-byte
encoding of u followed by that of v. The encoding is a bijection onto the
2^512 byte strings of length 64, so independent uniform words produce
independent uniform messages.

H is SHA3-256 with 5 prefix rounds of the Keccak-p[1600] permutation
(rounds 0 through 4 with the original first-round constants, not the
last-round convention). Rate is 1088 bits (136 bytes), capacity 512 bits,
suffix 0x06 with pad10*1, all-zero 1600-bit initial state, standard
little-endian lane encoding. On these exactly 64-byte messages there is a
single absorption block (64 message bytes plus suffix and padding fit in
136 bytes) followed by one 5-round permutation and a 32-byte squeeze; no
second absorption, no second permutation, and no extra squeeze is ever
evaluated, so every hash evaluation, including the final verification,
costs exactly one selected 5-round sponge permutation. The reference is
verifier/keccak.py:sha3_256 with rounds = 5.

The target profile permits other message lengths and preserves the
complete standard construction. This algorithm only generates 64-byte
messages, so the one-permutation description covers every hash it
evaluates, including final verification. No uncharged absorption,
permutation, or squeeze is needed on this domain.

## 2. Algorithm and representation

Set n = 9 * 2^125, an exact integer loop bound (9 * 2^125 < 2^129). A
record is 3 256-bit words: one word holding the digest (the
little-endian integer encoding of the complete 256-bit output) followed
by the 64 message bytes in the remaining words (32 + 64 bytes occupy 3
words with the last word partially used). Unsigned comparison of the
digest word is a total order whose equality is full digest equality. Two
flat arrays A and B of n records each serve as radix source and
destination, and one array H of 2^32 native 256-bit word counters serves
as the radix histogram and position table. H has 2^37 bytes; its counters
hold values up to 2^256, so per-bucket record counts of any size up to n
and cumulative prefix positions up to n are represented exactly, with no
overflow anywhere.

1. For i = 0, ..., n-1: draw 2 fresh independent uniform 256-bit words,
   construct the 64-byte message, compute its complete H (exactly one
   selected permutation), and store the record in A[i].
2. Sort A by the full 256-bit digest using a stable
   least-significant-digit radix sort with eight passes over 32-bit
   digits. Pass p (p = 0, ..., 7) uses digit p of the digest word as its
   key and proceeds in four charged stages: (a) zero all 2^32 counters of
   H; (b) read the p-th digit of each record's digest word and increment
   that digit's counter by one; (c) prefix-sum H in place into exclusive
   scatter positions (the largest position is n, far below 2^256); (d)
   for each source record in increasing source order, read its digit's
   position from H, store the record at that destination index in the
   other array, and increment the position in H. Stability follows from
   processing sources in increasing order. Exchange source and
   destination after each pass. After pass 8 the records are sorted by
   full digest.
3. Scan the sorted array once from left to right. For each adjacent pair
   with equal digest words, compare the two stored messages. On message
   inequality this is a candidate collision; on message equality it is a
   repeated sample, which is retained and charged and never reported.
   Continue.
4. On a candidate collision, recompute both complete hashes from the
   standard IV. Check message distinctness and equality of all 256
   recomputed output bits. Return the two messages if verified; otherwise
   halt with failure.
5. If the scan finishes without a verified pair, halt with failure.

There is one batch, no restart, and no success amplification beyond the
single batch. Verification failure cannot occur in the exact RAM model
because the original digests came from the same deterministic H. This
explicit defensive check is still charged. Every phase above has a cost
that is a fixed function of n alone, so the ledger in Section 5 is a
deterministic worst-case cap over all coin sequences and every fixed
target. In particular the positive-probability event that many sampled
messages are identical does not change any charged quantity: equal
records simply land in adjacent sorted positions and the scan compares
each adjacent pair once.

## 3. Correctness of any returned collision

Every returned message is in the profile's allowed domain. The explicit
final checks establish inequality of the messages and equality of the
entire complete-message hash from Section 1. This is an ordinary
collision of the complete selected hash, not a compression-only,
free-start, raw-permutation, truncated-output, or different-round result.
Repeated samples alone are never accepted because message equality is
checked before any report.

## 4. Success for every fixed function

The sole probability space consists of the 2n independent uniform 256-bit
words drawn in step 1, so the messages M_1, ..., M_n are independent
uniform samples from the message domain D of size 2^512. For the fixed
deterministic H the digests Y_i = H(M_i) are independent with
probabilities p_y = |{m in D : H(m) = y}| / |D| over Q = 2^256 possible
digest values. For any probability vector p of length Q let e_n(p) denote
the sum of products of n distinct coordinates. Independence gives
Pr[all Y_i distinct] = n! e_n(p). A maximum of e_n over the compact
simplex exists; among maximizers choose one minimizing the sum of squared
coordinates. If two coordinates a, b differ, replacing them by their
average cannot decrease e_n, since with the other coordinates r fixed,
e_n(p) = ab e_(n-2)(r) + (a+b)e_(n-1)(r) + e_n(r) has nonnegative
coefficients and is unchanged or increased by averaging, while the sum of
squares strictly decreases unless a = b. The maximizer is therefore
uniform, and with n = 9 * 2^125,

    Pr[all Y_i distinct] <= Q(Q-1)...(Q-n+1)/Q^n
      = product_(j=0,...,n-1) (1-j/Q)
      <= exp(-n(n-1)/(2Q))
      = exp(-(81*2^250 - 9*2^125)/2^257)
      <= exp(-0.63).

Since exp(0.63) > 1 + 0.63 + 0.63^2/2 + 0.63^3/6 + 0.63^4/24 > 1.876,
exp(-0.63) < 0.533. Let E be the event that some two samples carry equal
messages. The union bound gives Pr[E] <= n(n-1)/(2|D|) < 81*2^250/2^513
< 2^-256. Whenever the digests collide and E does not occur, some
adjacent pair of the sorted array carries equal digests and distinct
messages, the scan reports a candidate, and the recomputation returns
it. Thus Pr[success] >= 1 - 0.533 - 2^-256 > 0.467.

This bound proves the declared 0.45 and exceeds the required 0.39. The
number concerns algorithmic success, not confidence in a proof or review.

## 5. Fully charged RAM implementation

One selected 5-round permutation costs one unit; every other 256-bit RAM
primitive (load, store, add or subtract, bitwise operation, shift or
rotation, comparison, branch, uniform random word) costs 1/C units, with
C = 1355 for this target. All bounds include message construction, failed
samples, randomness, memory initialization, sorting, scanning,
verification, and fixed code and constants. There is no external disk,
uncharged precomputed collision, whole-hash oracle, or free sort step.
Every counter and position update below is charged as the separate loads,
additions and stores that the primitive list requires.

Code and fixed storage are bounded explicitly: the algorithm uses fewer
than 2^16 instruction templates and a fixed reserve of 2^24 bytes for
public constants, working state, the current record, verification scratch
and output. Initializing that reserve costs at most 2^24/C units; this is
the entire setup phase, it is charged inside T, and preprocessing_log2 =
24 bounds it from above. The record arrays need no initialization pass:
step 1 writes every A record and every radix pass writes exactly n
destination records. The histogram H is zeroed at the start of each pass
inside the charged pass cost.

| Activity | Charged-unit upper bound |
| --- | ---: |
| Fixed storage initialization (the whole preprocessing phase) | 2^24 / C |
| Per sample: 2 random-word draws, message construction, compression wrapper, digest packing into the record word, record assembly, loop control | 96 / C |
| Per sample: one selected 5-round permutation | 1 |
| Radix sort, per record per pass: digit access 3 + counter increment 3 + scatter position 3 + record transfer 6 + loop control 1 = 16 ops; eight passes | 128 / C |
| Histogram zeroing (2^32 stores) and prefix sum (2^32 loads, 2^32 adds, 2^32 stores) per pass: 2^34 ops; eight passes | 2^37 / C |
| Scan: per adjacent pair, digest compare (4 ops) and on equality message compare (at most 12 ops): at most 16 ops per pair, n-1 pairs | 16n / C |
| Final verification: two wrappers, two permutations, distinctness and digest comparison, output | 2 + 2^10 / C |

The generation wrapper budget is generous: 2 random-word draws, packing
the 64-byte message (at most 16 word stores), the permutation call and
loop control (at most 8), packing the 32 digest bytes into one
record word (at most 16 shifts and ORs), storing the 2 message words (at
most 4), and address arithmetic (at most 8); the total is below 60, well
inside the charged 96. The scan bound covers the all-repeated-samples
worst case.

Summing all phases with n = 9 * 2^125 and C = 1355,

    T <= n * (1 + 240/1355) + 2^24/C + 2^37/C + 2 + 2^10/C
      < 1.18 * n + 2^30
      = 1.18 * 9 * 2^125 + 2^30
      = 10.62 * 2^125 + 2^30
      < 2^128.41.

This is a deterministic worst-case charged-time cap over every coin
sequence and every fixed target: 1 + 240/1355 < 1.18, 1.18 * 9 = 10.62 <
2^3.41 = 10.629, and the additive 2^30 is absorbed far below
the 128.5 cap. The submitted bound 128.5 carries about 6% headroom over
the ledger.

Peak memory: two record arrays of n 3-word records, the histogram H of
2^32 counters (2^37 bytes), and fixed storage:

    peak bytes <= 2 * n * 96 + 2^37 + 2^24
                = 18 * 2^125 * 96 + 2^37 + 2^24
                < 2^135.76 + 2^37 + 2^24
                < 2^136.

The claim fields have these precise meanings:

- time_log2=128.5 bounds total charged time by 2^128.5 units.
- memory_log2_bytes=136 bounds simultaneous storage by 2^136 bytes,
  including both record arrays, the histogram, and fixed storage.
- preprocessing_log2=24 bounds the fixed setup from above, already
  included in T, not an omitted phase. There is no other initialization.
- nonuniform_advice_log2_bytes=0 means at most 2^0 = 1 byte of advice;
  actual nonuniform advice is zero. Public constants and code are fully
  charged in the fixed storage and initialization.
- success_probability=0.45 is the lower bound proved in Section 4.

## 6. Evidence and interpretation

This is a conservative generic birthday construction with tight, fully
deterministic, primitive-accurate accounting, not a new cryptanalytic
advance. The complete algorithm, target definition, probability proof and
RAM ledger are the supporting evidence. No full-scale execution, observed
collision pair, measured success rate, experimental independence or
measured resource usage is asserted. No sampled experiment is needed for
the universal finite probability argument. The certificate manifest is
valid and empty; no experiment manifest or participant executable is
supplied.

The required baseline_improved identifier sha3-256-r5-nominal-v2 names the
organizer's nominal display reference 128. It is not an established
attack, qualified baseline or security bound; the identifier's field name
is not a claim of improvement. This candidate's scalar bound 128.5 exceeds
128 but improves the promoted best 137.785. No Pareto dominance claim follows
from scalar scoring.

submission_state=ready means this independent exploratory package is
complete for review. It does not assert an actual qualifying review, an
emitted score, human acceptance, or Yukon promotion.
