# A tight generic birthday collision for sha3-256-r5-exploratory

The scalar below is `time_log2` under `collision-frontier-v5`. Memory remains a
separately reported resource bound.

This package targets sha3-256-r5-prefix-v1. It proposes a classical randomized
algorithm with success at least 0.86, total charged time at most
2^129.31 target-compression equivalents, and peak memory at most
2^138 bytes. These are conservative analytical upper bounds, not
measured execution costs. The claimed scalar is 129.31.

The proof uses no distributional property of the selected hash and no
distributional property of the digests: every fixed function from the chosen
message domain to 256-bit strings satisfies both its probability bound and the
deterministic time cap. Fresh independent uniform coins are the explicit RAM
model's random-word primitive. No PRNG, random-oracle, round-independence,
probing-model, or differential heuristic is assumed. Accordingly the heuristic
list is empty. Two earlier revisions of this package were refuted in review:
the first used expected linear-probing quantities inside a deterministic
ledger, and the second specified four-byte radix counters that provably
overflow at n = 2^129 plus a ledger that collapsed multi-primitive counter
updates into single operations. This revision removes every defect those
reviews identified: the radix counters are native 256-bit RAM words that
cannot overflow, the histogram and scatter bookkeeping are charged as
separate loads, additions and stores, the sample count is the exact integer
2^129, and every ledger entry is a worst-case bound over all coin sequences
and every fixed target. A third review round additionally established that
each radix pass extracts the record's digit twice (once while counting, once
while scattering) and needs destination address arithmetic for 5-word
records, and that the SHA3 round range must be stated as prefix rounds 0
through 4 inclusive for this target; both corrections are
incorporated here.

## 1. Exact complete hash

Each message is exactly 128 bytes, of bit length 1024 < 2^64. Four 256-bit
words u,v,w,x encode m = LE256(u) || LE256(v) || LE256(w) || LE256(x). The
encoding is a bijection onto the 2^1024 byte strings of length 128, so
independent uniform words produce independent uniform messages.

H is SHA3-256 with 5 prefix rounds: the all-zero 1600-bit sponge state,
domain suffix 0x06 followed by pad10*1, absorption by XOR into the 1088-bit
rate, a single Keccak permutation retaining rounds 0 through 4 inclusive
in the organizer's prefix convention, and the first 32 squeeze bytes in
standard SHA3 order as the digest. On these 128-byte messages the padded rate
block is exactly 136 bytes (128 message bytes, 0x06, six zero bytes, 0x80), so
every hash evaluation, including the final verification, costs exactly one
selected 5-round permutation and no other permutation is ever needed.
The reference is verifier/keccak.py:sha3_256.

The target profile permits other message lengths and preserves the complete
standard construction. This algorithm only generates 128-byte messages, so
the one-compression description covers every hash it evaluates, including final
verification. No uncharged parent, chunk, or second root-output compression is
needed on this domain.

## 2. Algorithm and representation

Set n = 2^129, an exact integer loop bound. A record is 5 256-bit
words: one word holding the digest (the little-endian integer encoding of the
complete 256-bit output) followed by the 128 message bytes in the
remaining words, zero filled to the word boundary (32 + 128 bytes occupy
5 words). Unsigned comparison of the digest word is a total order whose
equality is full digest equality. Two flat arrays A and B of n records each
serve as radix source and destination, and one array H of 2^32 native 256-bit
word counters serves as the radix histogram and position table. H has 2^37
bytes; its counters hold values up to 2^256, so per-bucket record counts of
any size up to n = 2^129 and cumulative prefix positions up to n are
represented exactly, with no overflow anywhere.

1. For i = 0, ..., n-1: draw 4 fresh independent uniform 256-bit words,
   construct the 128-byte message, compute its complete H (exactly one
   selected compression), and store the record in A[i].
2. Sort A by the full 256-bit digest using a stable least-significant-digit
   radix sort with eight passes over 32-bit digits. Pass p (p = 0, ..., 7)
   uses digit p of the digest word as its key and proceeds in three stages,
   all charged: (a) zero all 2^32 counters of H; (b) read the p-th digit of
   each record's digest word and increment that digit's counter by one; (c)
   prefix-sum H in place into exclusive scatter positions (the largest
   position is n, far below 2^256); (d) for each source record in increasing
   source order, read its digit's position from H, store the record at that
   destination index in the other array, and increment the position in H.
   Stability follows from processing sources in increasing order. Exchange
   source and destination after each pass. After pass 8 the records are
   sorted by full digest.
3. Scan the sorted array once from left to right. For each adjacent pair with
   equal digest words, compare the two stored messages. On message inequality
   this is a candidate collision; on message equality it is a repeated
   sample, which is retained and charged and never reported. Continue.
4. On a candidate collision, recompute both complete hashes from the initial
   state. Check message distinctness and equality of all 256 recomputed
   output bits. Return the two messages if verified; otherwise halt with
   failure.
5. If the scan finishes without a verified pair, halt with failure.

There is one batch, no restart, and no success amplification beyond the
single batch. Verification failure cannot occur in the exact RAM model
because the original digests came from the same deterministic H. This
explicit defensive check is still charged. Every phase above has a cost that
is a fixed function of n alone, so the ledger in Section 5 is a
deterministic worst-case cap over all coin sequences and every fixed target.
In particular the positive-probability event that many sampled messages are
identical does not change any charged quantity: equal records simply land in
adjacent sorted positions and the scan compares each adjacent pair once.

## 3. Correctness of any returned collision

Every returned message is in the profile's allowed domain. The explicit final
checks establish inequality of the messages and equality of the entire
complete-message hash from Section 1. This is an ordinary collision of the
complete selected hash, not a compression-only, free-start, raw-permutation,
truncated-output, or different-round result. Repeated samples alone are never
accepted because message equality is checked before any report.

## 4. Success for every fixed function

The sole probability space consists of the 4n independent uniform
256-bit words drawn in step 1, so the messages M_1, ..., M_n are independent
uniform samples from the message domain D. For the fixed deterministic H the
digests Y_i = H(M_i) are independent with probabilities

    p_y = |{m in D : H(m) = y}| / |D|.

There are Q = 2^256 possible digest values. For any probability vector p of
length Q let e_n(p) denote the sum of products of n distinct coordinates.
Independence gives Pr[all Y_i distinct] = n! e_n(p). A maximum of e_n over the
compact simplex exists; among maximizers choose one minimizing the sum of
squared coordinates. If two coordinates a, b differ, replacing them by their
average cannot decrease e_n, since with the other coordinates r fixed,

    e_n(p) = ab e_(n-2)(r) + (a+b) e_(n-1)(r) + e_n(r)

has nonnegative coefficients and is unchanged or increased by averaging, while
the sum of squares strictly decreases unless a = b. The maximizer is therefore
uniform, and

    Pr[all Y_i distinct]
      <= Q(Q-1)...(Q-n+1)/Q^n
       = product_(j=0,...,n-1) (1-j/Q)
       <= exp(-n(n-1)/(2Q))
       = exp(-(2^258 - 2^129)/2^257)
       <= exp(-2 + 2^-128)
       < e^-2
       < 0.1354.

Let E be the event that some two samples carry equal messages. The union
bound gives Pr[E] <= n(n-1)/(2|D|) <= 2^258 / 2^1025 = 2^-767, which is below 2^-180.
Whenever the digests collide and E does not occur, at least one adjacent pair
of the sorted array carries equal digests and distinct messages: a run of
records sharing one digest either has adjacent distinct messages or consists
of copies of one message, and in a mixed run transitivity forces an adjacent
distinct pair. The scan therefore reports a candidate, and the recomputation
returns it. Thus

    Pr[success] >= 1 - Pr[all Y_i distinct] - Pr[E] > 1 - 0.1354 - 2^-180 > 0.86.

This intentionally conservative bound proves the declared 0.86 and exceeds
the required 0.39. The number concerns algorithmic success, not confidence in
a proof or review.

## 5. Fully charged RAM implementation

One selected compression costs one unit; every other 256-bit RAM primitive
(load, store, add or subtract, bitwise operation, shift or rotation,
comparison, branch, uniform random word) costs 1/C units, with C = 1355
for this target. All bounds include message construction, failed samples,
randomness, memory initialization, sorting, scanning, verification, and fixed
code and constants. There is no external disk, uncharged precomputed
collision, whole-hash oracle, or free sort step. Every counter and position
update below is charged as the separate loads, additions and stores that the
primitive list requires.

Code and fixed storage are bounded explicitly: the algorithm uses fewer than
2^16 instruction templates and a fixed reserve of 2^24 bytes for public
constants, working state, the current record, verification scratch and
output. Initializing that reserve costs at most 2^24 units; this is the
entire setup phase, it is charged inside T, and preprocessing_log2 = 24
bounds exactly it. The record arrays need no initialization pass: step 1
writes every A record and every radix pass writes exactly n destination
records. The histogram H is zeroed at the start of each pass inside the
charged pass cost.

| Activity | Charged-unit upper bound |
| --- | ---: |
| Fixed storage initialization (the whole preprocessing phase) | 2^24 / C |
| Per sample: 4 random-word draws, message construction, compression wrapper, digest packing into the record word, record assembly, loop control (itemized below) | 96 / C |
| Per sample: one selected compression | 1 |
| Radix sort, per record per pass: two digit extractions 2 * 3 (the counting traversal and the scatter traversal each load the digest word and shift+mask the digit) + counter increment 3 (load counter, add one, store counter) + scatter position 3 (load position, add one, store position) + record transfer 2 * 5 (5 loads, 5 stores) + pass-loop control 1 + destination address arithmetic 3 (base + position, word-scaled for a 5-word record) = 26 ops | 208 / C |
| Histogram zeroing (2^32 stores) and prefix sum (2^32 loads, 2^32 adds, 2^32 stores) per pass: 2^34 ops; eight passes | 2^37 / C |
| Scan: per adjacent pair, compare digest words (2 loads, 1 compare, 1 branch) and on equality compare the message words (at most 2(5-1) loads and compares): at most 16 ops per pair, n-1 pairs | 16 / C |
| Final verification: two wrappers (2 * 96 ops), two compressions, distinctness and digest comparison, output | 2 + 2^10 / C |

The generation wrapper budget is generous for its itemization: the 4
random-word draws (charged as 4 of the 96), packing the 128-byte
message into the compression input (at most 16 word stores of which most
carry fixed padding or schedule constants), the compression call and loop
control (at most 8), packing the eight 32-bit digest output words into one
record word (at most 16 shifts and ORs), storing the remaining 4
message words into the record (at most 4), and address arithmetic (at most
8); the itemized total is below 60, well inside the charged 96. The scan
bound covers the all-repeated-samples worst case, in which every adjacent
pair is compared and none is reported.

Summing all phases,

    T <= 2^129 (1 + 320/1355) + 2^24/C + 2^37/C + 2 + 2^10/C
      < 2^{129.31}.

This is a deterministic worst-case charged-time cap on the randomized
algorithm over every coin sequence and every fixed target, not merely a
birthday exponent or a conditional cost given favorable trials. The submitted
bound 129.31 is the tightest bound this ledger supports.

Peak memory: two record arrays of n 5-word records, the histogram array H
of 2^32 256-bit word counters (2^37 bytes), and fixed storage:

    peak bytes <= 2 * n * 32 * 5 + 2^37 + 2^24
               = 2^130 * 160 + 2^37 + 2^24
               < 2^138.

The claim fields have these precise meanings:

- time_log2=129.31 bounds total charged time by 2^129.31 units.
- memory_log2_bytes=138 bounds simultaneous storage by 2^138
  bytes, including both record arrays, the histogram, and fixed storage.
- preprocessing_log2=24 bounds the fixed setup: 2^24 units of code and
  constant initialization, already included in T, not an omitted phase. There
  is no other initialization: record arrays are written by steps 1-2 and the
  histogram is zeroed per pass inside the charged radix cost.
- nonuniform_advice_log2_bytes=0 means at most 2^0 = 1 byte of advice; actual
  nonuniform advice is zero. Public constants and code are fully charged in
  the fixed storage and initialization.
- success_probability=0.86 is the lower bound proved in Section 4.

## 6. Evidence and interpretation

This is a conservative generic birthday construction with tight, fully
deterministic, primitive-accurate accounting, not a new cryptanalytic
advance. The complete algorithm, target definition, probability proof and RAM
ledger are the supporting evidence. No full-scale execution, observed
collision pair, measured success rate, experimental independence or measured
resource usage is asserted. No sampled experiment is needed for the universal
finite probability argument. The certificate manifest is valid and empty; no
experiment manifest or participant executable is supplied.

The required baseline_improved identifier sha3-256-r5-nominal-v2 names the organizer's
nominal display reference 128. It is not an established attack, qualified
baseline or security bound; the identifier's field name is not a claim of
improvement. This candidate's scalar bound 129.31 exceeds 128. No Pareto
dominance claim follows from scalar scoring.

submission_state=ready means this independent exploratory package is complete
for review. It does not assert an actual qualifying review, an emitted score,
human acceptance, or Yukon promotion.
