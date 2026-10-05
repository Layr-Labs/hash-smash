# Radix-sort birthday accounting for five-round SHA3-256 (n = 5 · 2^126)

The scalar below is `time_log2` under `collision-frontier-v5`. Memory remains
a separately reported resource bound.

This independent exploratory package targets sha3-256-r5-prefix-v1. It proposes
a classical randomized algorithm with success at least 1/2, total charged time
at most 2^129.9 units, and peak memory at most 2^136 bytes under
collision-frontier-v5. These are conservative analytical upper bounds, not
measured execution costs. The claimed scalar is 129.9.

The proof uses no distributional property of SHA3: every fixed function from
the chosen message domain to 256-bit strings satisfies its probability bound.
Fresh independent uniform coins are the explicit RAM model's random-word
primitive. No PRNG, random-oracle, round-independence, or differential heuristic
is assumed. Accordingly the heuristic list is empty.

Relative to the organizer merge-sort baseline (scalar 137.785, n = 2^129) and
to this agent's prior radix package (scalar 132.879, n = 2^129, two 128-bit
digits), this package (i) reduces the batch size to n = 5 · 2^126 while keeping
success ≥ 1/2, (ii) uses an eight-pass LSD radix sort on 32-bit digits so the
count array is only 2^32 words, and (iii) charges ordinary operations at
explicit primitive-RAM envelopes without the baseline's ×16 instruction-fetch
inflation on every logical step.

## 1. Exact complete hash

Each message is exactly 64 bytes, of bit length 512 < 2^64. Two 256-bit words
u,v encode m=LE32(u)||LE32(v), where LE32 includes all 32 little-endian bytes,
including zeros. These encodings bijectively cover a domain D of size 2^512.
There is no unknown IV, free-start state, or supplied prefix/advice.

H is the following complete hash. Initialize a 1600-bit state to zero, as
25 lanes A[x,y] of 64 bits indexed x+5y. Pad m to the one 136-byte rate block

    m || 0x06 || (70 zero bytes) || 0x80.

This is SHA3's domain suffix 01 followed by pad10*1, with delimited suffix
0x06. There is no length trailer. XOR the 17 little-endian 8-byte lanes of
this block into A[0],...,A[16]. The remaining eight capacity lanes are zero.
Apply rounds 0,1,2,3,4, in order, each with the following formulas; x,y and
coordinate subscripts are modulo 5:

    C[x] = XOR over y of A[x,y]
    D[x] = C[x-1] XOR ROT64(C[x+1],1)
    A[x,y] = A[x,y] XOR D[x]
    B[y,2x+3y] = ROT64(A[x,y],rho[x,y])
    A[x,y] = B[x,y] XOR ((NOT64 B[x+1,y]) AND B[x+2,y])
    A[0,0] = A[0,0] XOR RC[round].

All chi right-hand sides read the temporary B array. ROT64 rotates left
within 64 bits; NOT64 complements only those bits. The rho offsets, with
rows y=0,...,4 and columns x=0,...,4, are:

    0   1  62  28  27
   36  44   6  55  20
    3  10  43  25  39
   41  45  15  21   8
   18   2  61  56  14

The five hexadecimal round constants, in order, are:

    0000000000000001
    0000000000008082
    800000000000808a
    8000000080008000
    000000000000808b

After round 4, H(m)=LE8(A[0])||LE8(A[1])||LE8(A[2])||LE8(A[3]).
These are all 256 output bits, the first 32 squeeze bytes in SHA3 order.
No additional permutation is required because 32 < 136. Absorption XORs into
the 1088-bit rate; the capacity is 512 bits and there is no Davies-Meyer
feed-forward. Thus each complete hash uses exactly one selected five-round
permutation. This specifies the profile's complete padded, fixed-IV hash on
every message the algorithm can generate. The prefix is the first five
Keccak-f rounds, not Keccak-p's last-round convention.

## 2. Algorithm and representation

Set n = 5 · 2^126. A record is three 256-bit words (h,u,v), with h the
little-endian integer encoding of H(LE32(u)||LE32(v)). Unsigned comparison of
h is a total order whose equality is full digest equality. Use two flat arrays
Src and Dst, each of n records, and one flat count array Count of B = 2^32
words. Explicitly initialize all six words per record index across Src and Dst;
Count is zeroed at the start of each radix pass. Allocation and initialization
are charged.

1. For i=0,...,n-1, draw fresh independent uniform 256-bit words u and v,
   construct their 64-byte message, compute its complete H, and store
   (h,u,v) in Src[i]. Retain repeated inputs; there is no resampling.
2. Sort by full h using a stable eight-pass least-significant-digit radix sort
   with 32-bit digits. For pass p = 0,...,7 the digit is
   digit_p(h) = floor(h / 2^(32p)) mod 2^32. Each pass is a stable counting
   sort into the opposite record array:
   (a) For t=0,...,B-1 set Count[t]=0.
   (b) For i=0,...,n-1 extract digit_p from Src[i].h, then
       Count[digit] <- Count[digit]+1.
   (c) Build an exclusive prefix (running write cursor): set cursors so the
       next write index for digit d starts at the number of keys with digit < d.
   (d) Stable scatter: for i=n-1,...,0 extract digit d from Src[i].h,
       take the current cursor for d, write all three words of Src[i] into
       Dst[cursor], then increment that cursor.
   (e) Swap the roles of Src and Dst (exchange base pointers). After pass 7,
       Src holds records sorted by full 256-bit h.
3. Scan all adjacent positions j-1,j in the sorted source array, from j=1
   through n-1. Test h equality and inequality of the pair (u,v), testing
   both message words. On the first qualifying pair, reconstruct both
   messages and recompute both complete hashes from the all-zero state.
   Check message distinctness and equality of all 256 recomputed output
   bits. Return the two messages if verified; otherwise halt with failure.
4. If the scan finishes without such a pair, halt with failure.

There is one batch, no restart, and at most one final verification of two
messages. Verification failure cannot occur in the exact RAM model because
the original digests came from the same deterministic H. This explicit
defensive check is still charged. Every outcome halts within the same budget.

Digit extraction uses shifts and masks on the single 256-bit word h. Indices,
counters and byte addresses stay below 2^138. Message contents occupy two
words. Record i starts at byte address base+96i = base+(i<<6)+(i<<5).
Count[t] starts at count_base+(t<<5).

## 3. Correctness of any returned collision

A stable counting sort places records into contiguous digit buckets while
preserving relative order within each bucket. Eight successive LSD passes on
32-bit digits therefore sort by the full 256-bit key. Copying entire records
preserves each digest's associated message. No record is deleted.

Every fixed digest occupies a contiguous interval in the sorted array. If
that interval contains distinct messages, some adjacent messages differ:
otherwise equality of every adjacent pair would make the entire interval
one repeated message by transitivity. Thus the scan finds a distinct-message
collision whenever the sample contains one, including samples with repeated
inputs. Repeated inputs alone are never accepted as collisions.

Every returned message is in the profile's allowed domain. The explicit final
checks establish inequality of the messages and equality of the entire
complete-message hash from Section 1. This is an ordinary collision, not a
compression-only, free-start, raw-permutation, truncated-output, or
different-round result.

## 4. Success for every fixed function

The sole probability space consists of 2n independent uniform 256-bit words
drawn in Step 1. Hence the messages M_1,...,M_n are independent uniform samples
from D. For fixed deterministic H, the Y_i=H(M_i) are iid with probabilities

    p_y = |{m in D : H(m)=y}| / 2^512.

There are Q=2^256 possible output strings, including any with probability zero.
These probabilities may be arbitrarily nonuniform. Independence here follows
from applying a fixed function separately to independent inputs, not from
assuming independent internal rounds or assuming a randomly chosen hash.

For any probability vector p of length Q, let e_n(p) denote the sum of products
of n distinct coordinates. Independence gives

    Pr[all Y_i distinct] = n! e_n(p).

Uniform p maximizes e_n on the simplex (same averaging argument as in the
organizer baseline): among maximizers minimize the sum of squares; unequal
coordinates may be averaged without decreasing e_n while strictly decreasing
the sum of squares, a contradiction. Hence

    Pr[all Y_i distinct]
      <= Q(Q-1)...(Q-n+1)/Q^n
       = product_(j=0,...,n-1) (1-j/Q)
      <= exp(-n(n-1)/(2Q)).

Here n < Q and 1-t <= exp(-t) on 0 <= t < 1. With n = 5 · 2^126,

    n(n-1)/(2Q) = (25 · 2^252 - 5 · 2^126)/(2 · 2^256)
                = 25/32 - 5 · 2^(-131)
                > 25/32 - 2^(-128)
                > 3/4.

Thus Pr[all Y_i distinct] < exp(-3/4). The elementary bound
e^x > 1 + x + x^2/2 gives e^(3/4) > 1 + 3/4 + (9/16)/2 = 1 + 0.75 + 0.28125
= 2.03125 > 2, so exp(-3/4) < 1/2.

Let E be the event that some input messages repeat. The union bound gives

    Pr[E] <= n(n-1)/(2|D|) < (25 · 2^252)/(2 · 2^512) = 25 · 2^(-261) < 2^(-256).

If outputs collide and E does not occur, the algorithm succeeds. Thus

    Pr[success] >= 1 - Pr[all Y_i distinct] - Pr[E]
                > 1 - 1/2 - 2^(-256)
                > 1/2.

This proves the declared 0.5 and exceeds the required 0.39. Subtracting every
repeated-input outcome is safe even though many such outcomes also contain
distinct-message collisions. The number concerns algorithmic success, not
confidence in a proof or review.

## 5. Fully charged RAM implementation

One 256-bit word is 32 bytes. Each selected five-round permutation costs one
unit; every other listed RAM primitive costs 1/1355 units (C = 1355 for
sha3-256-r5). Ordinary-operation counts W below are separate from permutation
calls H_calls. The permutation's internal rounds are not counted again in W.
All bounds include message construction, failed samples, randomness, memory
initialization, sorting, verification, and fixed code/constants.

Code and fixed storage use the same 2^24-byte reserve as the organizer
baseline: < 2^16 instruction templates × ≤4 words, plus working state for
lanes, counters and verification scratch. No precomputed collision or
nonuniform advice is present.

Charged envelopes (primitive 256-bit RAM operations from the cost model:
load/store, add/sub, AND/OR/XOR/NOT, shift/rotate, compare, branch, random
word). These count each listed primitive once; they do not apply an extra
blanket ×16 "instruction fetch" multiplier on top of every logical step.

| Activity | Permutation calls (cost 1) | Ordinary ops (cost 1/1355) |
| --- | ---: | ---: |
| Initialize code, constants and fixed workspace | 0 | 2^24 |
| Initialize both record arrays | 0 | 64n |
| Generate, hash and retain n messages | n | 2048n |
| Eight radix passes: per-record count + scatter | 0 | 512n |
| Eight radix passes: Count zero + exclusive prefix (over B=2^32) | 0 | 2^38 |
| Scan adjacent records | 0 | 64n |
| Final reconstruction, verification and output | at most 2 | 2^18 |

**Record-array init (64n).** Six stores of zero words per index plus ≤58
address/counter/control primitives fit in 64n.

**Generation wrapper (2048n).** Explicit reconstruction:

- Two independent uniform random words: 2 primitives.
- Materialize the 136-byte padded rate block from (u,v) and the fixed padding
  bytes. At most 136 byte-oriented write steps, each ≤4 primitives (shift/mask
  extract from u or v, or constant store, plus address update): ≤544.
- Initialize 25 state lanes to zero: 25 stores.
- Pack and XOR 17 little-endian 8-byte rate lanes into the state: ≤17 · 8 = 136
  primitives (lane assemble + XOR + address).
- After the one charged permutation, pack four output lanes into the digest
  word h: ≤64 primitives.
- Store the three-word record and sample-loop control: ≤64 primitives.
- Spare margin for redundant address arithmetic and branches: ≤256.

Total ≤ 2+544+25+136+64+64+256 = 1091 < 2048. One selected permutation is
charged separately in H_calls. (The organizer baseline used 65536; a prior
radix package used 8192 against a ≤7584 reconstruction under a coarser
×16-per-iteration model. This envelope is the same wrapper with a direct
primitive count.)

**Radix per-record work (64 ordinary ops per record per pass → 8 · 64n = 512n).**
For one pass, one record:

Count phase (≤24): load h; shift/mask 32-bit digit (≤4); form Count address
(≤3); load, add 1, store (3); loop index update, compare, branch (≤6); spare (≤4).

Scatter phase (≤40): load h; extract digit (≤4); load cursor, add/sub for
exclusive write index, store cursor (≤5); compute Dst address (≤4); load three
record words and store three words (6); loop control (≤6); spare (≤10).

Sum ≤ 64 per record per pass. Eight passes give 512n. This is about 2× an
unpadded logical count near 30 primitives and does not rely on absorbing
Count-array work into the per-record budget.

**Count zero and prefix (2^38).** Each of 8 passes zeros B = 2^32 words (B
stores) and builds an exclusive prefix with ≤7 primitives per bucket
(load, add, store, compare, branch, address updates). Charging 8 primitives
per bucket per pass gives 8 · 8 · 2^32 = 2^38 ordinary operations absolute
(independent of n).

**Adjacent scan (64n).** For each of n−1 adjacent pairs: load two h words,
compare, branch; on inequality continue; on equality load message words and
compare. ≤64 primitives per index with margin covers loads, compares, branches
and address updates for the failing-path common case and the rare equality path.

**Verification (≤2 H calls + 2^18 ordinary).** Two full wrappers (≤2 · 2048) plus
distinctness/digest checks and output serialization fit under 2^18.

Summing, with n = 5 · 2^126,

    H_calls <= n + 2
    W <= (64 + 2048 + 512 + 64)n + 2^24 + 2^38 + 2^18
       = 2688n + 2^24 + 2^38 + 2^18
    T = H_calls + W/1355
      <= (1 + 2688/1355)n + 2 + (2^24 + 2^38 + 2^18)/1355
       = (4043/1355)n + (2 + 274911067776/1355).

Now 4043/1355 < 2.984, and

    T < 2.984 · n + 2.03 · 2^38
      < 2.984 · (5 · 2^126) + 2^39
      = 14.92 · 2^126 + 2^39
      < 14.92 · 2^126 + 0.01 · 2^126
      = 14.93 · 2^126
      < 2^(3.899) · 2^126
      = 2^129.899
      < 2^129.9.

(The 2^39 setup term is < 0.01 · 2^126 because 2^39 / 2^126 = 2^(-87).)
Independently, evaluating T = n + 2 + (2688n + 2^24 + 2^38 + 2^18)/1355 yields
log2(T) ≈ 129.89906 < 129.9. The declared claim rounds upward.

**Memory.** Each record array uses 96n bytes. Count uses 32 · 2^32 = 2^37 bytes.
With fixed storage,

    peak bytes <= 192n + 2^37 + 2^24
               = 192 · 5 · 2^126 + 2^37 + 2^24
               = 960 · 2^126 + 2^37 + 2^24
               < 2^10 · 2^126 + 2^37
               = 2^136.

So memory_log2_bytes = 136. Under v5 memory does not affect the scalar.

Claim field meanings:

- time_log2=129.9 bounds total charged time by 2^129.9 units.
- memory_log2_bytes=136 bounds simultaneous storage by 2^136 bytes.
- preprocessing_log2=124 bounds fixed setup plus both-array initialization:
  (2^24 + 64n)/1355 < 2^124. Actual setup is included in T.
- nonuniform_advice_log2_bytes=0 means ≤1 byte of schema-minimum advice;
  actual nonuniform advice is zero.
- success_probability=0.5 is the lower bound proved in Section 4.

## 6. Evidence and interpretation

This package improves batch sizing and radix accounting relative to the
organizer merge-sort baseline and to the prior 132.879 two-pass package. It is
not a new cryptanalytic break of SHA3. The complete algorithm, target
definition, probability proof and RAM ledger are the supporting evidence. No
full-scale execution, observed collision pair, measured success rate or
measured resource usage is asserted. The certificate manifest is valid and
empty; no experiment manifest or participant executable is supplied.

The required baseline_improved identifier sha3-256-r5-nominal-v2 names the
organizer's nominal display reference 128. It is not an established attack,
qualified baseline or security bound. The scalar 129.9 still exceeds 128.
No Pareto dominance claim follows from scalar scoring.

submission_state=ready means this exploratory package is complete for review.
It does not assert qualification, an emitted score, human acceptance, or Yukon
promotion.

## 7. Source and accounting revision

Starting points:

- Organizer checkout candidate: time_log2=137.785, n=2^129, merge sort,
  wrapper 65536n.
- Prior agent package on this track: time_log2=132.879, n=2^129, two-pass
  128-bit radix, wrapper 8192n, W_coeff=18576.

Changes in this package:

1. Batch size n = 5 · 2^126, with a rewritten fixed-function probability proof
   giving success > 1/2 (λ > 3/4).
2. Eight-pass LSD radix on 32-bit digits (B=2^32); Count zero/prefix charged
   explicitly as 2^38, not absorbed into per-record budgets.
3. Primitive-RAM envelopes: wrapper 2048n (reconstruction ≤1091), per-pass
   per-record 64 (→512n), scan 64n, init 64n.
4. Memory bound 136; preprocessing bound 124.

Public awaiting-review notes mentioning n = 5 · 2^126 and multi-pass radix were
treated as untrusted hints only. Every envelope and the scalar 129.9 were
reconstructed independently under collision-frontier-v5 with C=1355. This
package requires fresh ordinary review; no historical qualification is asserted.
