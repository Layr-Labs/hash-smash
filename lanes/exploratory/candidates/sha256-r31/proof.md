# A tight generic birthday collision for sha256-r31-exploratory

The scalar below is `time_log2` under `collision-frontier-v5`. Memory remains a
separately reported resource bound.

This package targets sha256-r31-prefix-v1. It proposes a classical randomized
algorithm with success at least 0.86, total charged time at most
2^129.11 target-compression equivalents, and peak memory at most
2^137 bytes. These are conservative analytical upper bounds, not
measured execution costs. The claimed scalar is 129.11.

The proof uses no distributional property of the selected hash and no
distributional property of the digests: every fixed function from the chosen
message domain to 256-bit strings satisfies both its probability bound and the
deterministic time cap. Fresh independent uniform coins are the explicit RAM
model's random-word primitive. No PRNG, random-oracle, round-independence,
probing-model, or differential heuristic is assumed. Accordingly the heuristic
list is empty. This submission replaces an earlier table-based design whose
use of expected linear-probing quantities inside a deterministic ledger was
refuted in review; every quantity below is now a worst-case bound.

## 1. Exact complete hash

Each message is exactly 55 bytes, of bit length 440 < 2^64. Two 256-bit
words u,v encode m = LE256(u) || LE256(v)[0:23], where LE256 denotes all 32
little-endian bytes. The encoding is surjective onto the 2^440 byte strings of
length 55 and every string has exactly 2^72 preimages, so independent uniform
words produce independent uniform messages.

H is SHA-256 with 31 rounds: FIPS 180-4 padding (append 0x80, zero bytes to
56 modulo 64, then the 64-bit big-endian bit length 440), the standard fixed
IV, the standard message-word expansion and constants at their original
indices, round indices 0 through 30 inclusive, the standard feed-forward
addition of the working state into the incoming chaining state, and the full
256-bit state serialized in standard big-endian order as the digest. On these
55-byte messages the padded input is exactly one 512-bit block, so every hash
evaluation, including the final verification, costs exactly one selected
31-round compression and no other compression is ever needed. The
reference is verifier/hash_functions.py:digest.

The target profile permits other message lengths and preserves the complete
standard construction. This algorithm only generates 55-byte messages, so
the one-compression description covers every hash it evaluates, including final
verification. No uncharged parent, chunk, or second root-output compression is
needed on this domain.

## 2. Algorithm and representation

Set n = 2^129, an exact integer loop bound. A record is 3 256-bit
words: one word holding the digest (the little-endian integer encoding of the
complete 256-bit output) followed by the 55 message bytes in the
remaining words (zero filled to the word boundary; 55 bytes plus 32
digest bytes occupy 3 words). Unsigned comparison of the digest word is
a total order whose equality is full digest equality. Two flat arrays A and B
of n records each serve as radix source and destination.

1. For i = 0, ..., n-1: draw 2 fresh independent uniform 256-bit words,
   construct the 55-byte message, compute its complete H (exactly one
   selected compression), and store the record in A[i].
2. Sort A by the full 256-bit digest using a stable least-significant-digit
   radix sort with eight passes over 32-bit digits. Pass p (p = 0, ..., 7)
   uses the p-th 32-bit digit of the digest word as its key: zero a histogram
   of 2^32 four-byte counters, count the digit of each of the n records,
   prefix-sum the counters, then scatter all n records stably from the source
   array into the destination array. Exchange source and destination after
   each pass. After pass 8 the records are sorted by full digest.
3. Scan the sorted array once from left to right. For each adjacent pair with
   equal digest words, compare the two stored messages. On message inequality
   this is a candidate collision; on message equality it is a repeated sample,
   which is retained and charged and never reported. Continue the scan.
4. On a candidate collision, recompute both complete hashes from the initial
   state. Check message distinctness and equality of all 256 recomputed output
   bits. Return the two messages if verified; otherwise halt with failure.
5. If the scan finishes without a verified pair, halt with failure.

There is one batch, no restart, and no success amplification beyond the single
batch. Verification failure cannot occur in the exact RAM model because the
original digests came from the same deterministic H. This explicit defensive
check is still charged. Every phase above has a cost that is a fixed function
of n alone, so the ledger in Section 5 is a deterministic worst-case cap over
all coin sequences and every fixed target. In particular the positive-
probability event that many sampled messages are identical does not change any
charged quantity: equal records simply land in adjacent sorted positions and
the scan compares each adjacent pair once.

## 3. Correctness of any returned collision

Every returned message is in the profile's allowed domain. The explicit final
checks establish inequality of the messages and equality of the entire
complete-message hash from Section 1. This is an ordinary collision of the
complete selected hash, not a compression-only, free-start, raw-permutation,
truncated-output, or different-round result. Repeated samples alone are never
accepted because message equality is checked before any report.

## 4. Success for every fixed function

The sole probability space consists of the 2n independent uniform
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

Let E be the event that some two samples carry equal messages. The union bound
gives Pr[E] <= n(n-1)/(2|D|) <= 2^258 / 2^441, which is below
2^-253. Whenever the digests collide and E does not occur, at least one
adjacent pair of the sorted array carries equal digests and distinct messages:
a run of records sharing one digest either has adjacent distinct messages or
consists of copies of one message, and in a mixed run transitivity forces an
adjacent distinct pair. The scan therefore reports a candidate, and the
recomputation returns it. Thus

    Pr[success] >= 1 - Pr[all Y_i distinct] - Pr[E] > 1 - 0.1354 - 2^-253 > 0.86.

This intentionally conservative bound proves the declared 0.86 and exceeds the
required 0.39. The number concerns algorithmic success, not confidence in a
proof or review.

## 5. Fully charged RAM implementation

One selected compression costs one unit; every other 256-bit RAM primitive
costs 1/C units, with C = 2140 for this target. All bounds include message
construction, failed samples, randomness, memory initialization, sorting,
scanning, verification, and fixed code and constants. There is no external
disk, uncharged precomputed collision, whole-hash oracle, or free sort step.

Code and fixed storage are bounded explicitly: the algorithm uses fewer than
2^16 instruction templates and a fixed reserve of 2^24 bytes for public
constants, working state, the current record, verification scratch and output.
Initializing that reserve costs at most 2^24 units; this is the entire setup
phase, it is charged inside T, and preprocessing_log2 = 24 bounds exactly it.
The record arrays need no initialization pass: step 1 writes every A record
and every radix pass writes exactly n destination records. The radix histogram
is zeroed at the start of each pass and then prefix-summed, both charged below
as a fixed per-pass cost independent of the sample values.

| Activity | Charged-unit upper bound |
| --- | ---: |
| Fixed storage initialization (the whole preprocessing phase) | 2^24 / C |
| Per sample: 2 random words, message construction, compression wrapper, record assembly, loop control | 96 / C |
| Per sample: one selected compression | 1 |
| Radix sort: eight passes, each record 3 words: per pass 1 digit read + 1 histogram increment + 6 record loads/stores = 8 ops; total 64 ops per record | 64 / C |
| Histogram zeroing plus prefix sum: at most 2^33 ops per pass, eight passes | 2^36 / C |
| Scan: one comparison of adjacent digest words plus, on equality, one message comparison: at most 6 ops per adjacent pair, n-1 pairs | 6 / C |
| Final verification: two wrappers, two compressions, output | 2 + 2^10 / C |

The wrapper budget is generous: it covers the 2 random-word draws,
packing the 55-byte message from whole words by shifts, masks and
stores, the padding or schedule constants (fixed, since the message length is
fixed), and loop control. The scan bound covers the all-repeated-samples
worst case, in which every adjacent pair is compared and none is reported.

Summing all phases,

    T <= 2^129 (1 + 166/2140) + 2^24/C + 2^36/C + 2 + 2^10/C
      < 2^{129.11}.

This is a deterministic worst-case charged-time cap on the randomized
algorithm over every coin sequence and every fixed target, not merely a
birthday exponent or a conditional cost given favorable trials. The submitted
bound 129.11 is the tightest bound this ledger supports.

Peak memory: two record arrays of n records, the radix histogram of 2^32
four-byte counters (2^34 bytes), and fixed storage:

    peak bytes <= 2 * n * 32 * 3 + 2^34 + 2^24
               = 2^130 * 96 + 2^34 + 2^24
               < 2^137.

The claim fields have these precise meanings:

- time_log2=129.11 bounds total charged time by 2^129.11 units.
- memory_log2_bytes=137 bounds simultaneous storage by 2^137 bytes,
  including both record arrays, the histogram, and fixed storage.
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
deterministic accounting, not a new cryptanalytic advance. The complete
algorithm, target definition, probability proof and RAM ledger are the
supporting evidence. No full-scale execution, observed collision pair, measured
success rate, experimental independence or measured resource usage is asserted.
No sampled experiment is needed for the universal finite probability argument.
The certificate manifest is valid and empty; no experiment manifest or
participant executable is supplied.

The required baseline_improved identifier sha256-r31-nominal-v2 names the organizer's
nominal display reference 128. It is not an established attack, qualified
baseline or security bound; the identifier's field name is not a claim of
improvement. This candidate's scalar bound 129.11 exceeds 128. No Pareto
dominance claim follows from scalar scoring.

submission_state=ready means this independent exploratory package is complete
for review. It does not assert an actual qualifying review, an emitted score,
human acceptance, or Yukon promotion.
