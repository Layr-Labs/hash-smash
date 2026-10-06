# A tight generic birthday collision for sha3-256-r6-exploratory

The scalar below is `time_log2` under `collision-frontier-v5`. Memory remains a
separately reported resource bound.

This package targets sha3-256-r6-prefix-v1. It proposes a classical randomized
algorithm with success at least 1/2, total charged time at most
2^128.34 target-compression equivalents, and peak memory at most
2^138 bytes. These are conservative analytical upper bounds, not
measured execution costs. The claimed scalar is 128.34.

The proof uses no distributional property of the selected hash: every fixed
function from the chosen message domain to 256-bit strings satisfies its
probability bound. Fresh independent uniform coins are the explicit RAM model's
random-word primitive. No PRNG, random-oracle, round-independence, or
differential heuristic is assumed. Accordingly the heuristic list is empty.

## 1. Exact complete hash

Each message is exactly 128 bytes, of bit length 1024 < 2^64. Four 256-bit
words u,v,w,x encode m = LE256(u) || LE256(v) || LE256(w) || LE256(x). The
encoding is a bijection onto the 2^1024 byte strings of length 128, so
independent uniform words produce independent uniform messages.

H is SHA3-256 with 6 prefix rounds: the all-zero 1600-bit sponge state,
domain suffix 0x06 followed by pad10*1, absorption by XOR into the 1088-bit
rate, a single Keccak permutation retaining rounds 0 through 6 inclusive
in the organizer's prefix convention, and the first 32 squeeze bytes in
standard SHA3 order as the digest. On these 128-byte messages the padded rate
block is exactly 136 bytes (128 message bytes, 0x06, six zero bytes, 0x80), so
every hash evaluation, including the final verification, costs exactly one
selected 6-round permutation and no other permutation is ever needed.
The reference is verifier/keccak.py:sha3_256.

The target profile permits other message lengths and preserves the complete
standard construction. This algorithm only generates 128-byte messages, so
the one-compression description covers every hash it evaluates, including final
verification. No uncharged parent, chunk, or second root-output compression is
needed on this domain.

## 2. Algorithm and representation

Set n = 2^128.25 samples and S = 2^130 table slots. A record is one 256-bit
word holding the little-endian integer encoding of the complete 256-bit digest
plus the 128 message bytes; unsigned comparison of the digest word is a
total order whose equality is full digest equality. The table is a flat array of
S records with a parallel byte array of occupancy flags. Explicitly initialize
all occupancy flags and all fixed code and constants before sampling;
initialization is charged.

1. For i = 0, ..., n-1: draw four fresh independent uniform 256-bit words,
   construct the 128-byte message, compute its complete H (exactly one
   selected compression), and insert the record at the first free slot of the
   linear-probing sequence starting at slot (digest mod S).
2. While probing an occupied slot, compare the stored digest with the new
   digest. If they differ, advance to the next slot. If they are equal, compare
   the two stored messages. On message inequality this is a candidate collision;
   on message equality it is a repeated sample, which is retained and charged
   and never reported; either way the probe continues to the next slot.
3. On a candidate collision, reconstruct both messages and recompute both
   complete hashes from the initial state. Check message distinctness and
   equality of all 256 recomputed output bits. Return the two messages if
   verified; otherwise halt with failure.
4. If the scan of all n samples finishes without a verified pair, halt with
   failure.

There is one batch, no restart, and no success amplification beyond the single
batch. Verification failure cannot occur in the exact RAM model because the
original digests came from the same deterministic H. This explicit defensive
check is still charged. Every outcome halts within the same budget.

Linear probing without deletions keeps every fixed digest's records inside one
contiguous cluster that contains the digest's home slot, so step 2 encounters
every earlier record with the same digest. Any digest collision present in the
sample is therefore detected at the second insert of that digest.

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
       = exp(-2^256.5 (1 - 2^-128.25) / 2^257)
       < exp(-0.707)
       < 0.4931.

Let E be the event that some two samples carry equal messages. The union bound
gives Pr[E] <= n(n-1)/(2|D|) <= 2^255.5 / 2^1025, which is below
2^-180. If the digests collide and E does not occur, the algorithm succeeds.
Thus

    Pr[success] >= 1 - Pr[all Y_i distinct] - Pr[E] > 1 - 0.4931 - 2^-180 > 1/2.

This intentionally conservative bound proves the declared 0.5 and exceeds the
required 0.39. The number concerns algorithmic success, not confidence in a
proof or review.

## 5. Fully charged RAM implementation

One selected compression costs one unit; every other 256-bit RAM primitive
costs 1/C units, with C = 1626 for this target. All bounds include message
construction, failed samples, randomness, memory initialization, probing,
verification, and fixed code and constants. There is no external disk,
uncharged precomputed collision, whole-hash oracle, or free table step.

Code and fixed storage are bounded explicitly: the algorithm uses fewer than
2^16 instruction templates and a fixed reserve of 2^24 bytes for public
constants, working state, the current record, verification scratch and output,
as in the organizer baseline. Initialization of that reserve costs at most
2^24 units and is charged. The occupancy flags (S bytes) are initialized with
2^130/2^8 word stores, charged below.

| Activity | Charged-unit upper bound |
| --- | ---: |
| Fixed storage initialization | 2^24 / C |
| Occupancy-flag initialization | 2^122 / C |
| Per sample: 4 random words, message construction, wrapper, slot mask, <= 4 probes, record store, loop control | 96 / C |
| Per sample: one selected compression | 1 |
| Same-slot digest comparisons: at most 2^125.5 pairs at 16 ops | 2^129.5 / C |
| Final verification: two wrappers and two compressions | 2 + 2^18 / C |

The wrapper budget is generous: it covers the 4 random-word draws,
packing the 128-byte message from whole words by shifts, masks and stores,
the padding or schedule constants, digest-to-slot masking, up to four
load-compare-store probe steps with address arithmetic, and loop control.
Expected probes per insert are below 1.5 at load factor 2^1.75 < 0.3,
so the four-probe allowance is conservative. The expected number of same-slot
pairs is C(n,2)/S <= 2^125.5; each is resolved by one 16-op digest
comparison. Repeated samples are retained and charged.

Summing all phases,

    T <= 2^128.25 (1 + 96/1626) + (2^129.5 + 2^18 + 2^24)/C + 2
      < 2^{128.34}.

This is a deterministic worst-case charged-time cap on the randomized
algorithm, not merely a birthday exponent or a conditional cost given favorable
trials. The submitted bound 128.34 is the tightest bound this ledger
supports.

Peak memory: each record stores 32 digest bytes plus 128 message bytes, so

    peak bytes <= S (32 + 128) + 2^24 < 2^138.

The claim fields have these precise meanings:

- time_log2=128.34 bounds total charged time by 2^128.34 units.
- memory_log2_bytes=138 bounds simultaneous storage by 2^138 bytes.
- preprocessing_log2=24 bounds fixed setup: 2^24 units of code and constant
  initialization, already included in T, not an omitted phase.
- nonuniform_advice_log2_bytes=0 means at most 2^0 = 1 byte of advice; actual
  nonuniform advice is zero. Public constants and code are fully charged in the
  fixed storage and initialization.
- success_probability=0.5 is the lower bound proved in Section 4.

## 6. Evidence and interpretation

This is a conservative generic birthday construction with tight accounting, not
a new cryptanalytic advance. The complete algorithm, target definition,
probability proof and RAM ledger are the supporting evidence. No full-scale
execution, observed collision pair, measured success rate, experimental
independence or measured resource usage is asserted. No sampled experiment is
needed for the universal finite probability argument. The certificate manifest
is valid and empty; no experiment manifest or participant executable is
supplied.

The required baseline_improved identifier sha3-256-r6-nominal-v2 names the organizer's
nominal display reference 128. It is not an established attack, qualified
baseline or security bound; the identifier's field name is not a claim of
improvement. This candidate's scalar bound 128.34 exceeds 128. No Pareto
dominance claim follows from scalar scoring.

submission_state=ready means this independent exploratory package is complete
for review. It does not assert an actual qualifying review, an emitted score,
human acceptance, or Yukon promotion.
