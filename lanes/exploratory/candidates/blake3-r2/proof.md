# One radix partition and a tagged suffix table for two-round BLAKE3

This is a concrete generic collision algorithm for `blake3-r2-prefix-v1`.
It has success probability greater than 0.39 for this fixed target, total
worst-case charged computation below 2^128.65 under collision-frontier-v5,
and peak memory below 2^136 bytes. These are analytical bounds in the specified
256-bit RAM model, not measurements of a physically executable full-size attack.

The change from the organizer candidate is algorithmic: replace 129 passes of
comparison sorting with one radix partition and a reusable, tagged direct-address
table. A separately justified sample budget and 33-byte domain reduce the
randomness and record storage. The table construction has a linear worst-case
operation bound even for adversarial digest distributions. There is no assumed
uniformity of BLAKE3 output, no assumed independent internal rounds, and no
assumed bucket sparsity. The heuristic list is empty.

This improves the checked-out generic candidate's bound 140. It does not beat
the nominal display reference 128, nor claim to beat the lower, unpromoted
structural submissions. Qualification, human acceptance, and promotion remain
separate. No historical or worldwide novelty assertion is made.

## 1. Exact target and message domain

Let K=2^128, N=511*2^119=(511/512)K, and L=N/32=511*2^114.
The algorithm samples exactly N messages, each of length 33 bytes:

    M_i = LE32(U_i) || byte(V_i).

LE32 here means all 32 little-endian bytes of a 256-bit word, including zeros;
it is not a 32-bit integer encoding. U_i is uniform in [0,2^256), and V_i
is an independent uniform byte. Thus the domain D has size 2^264. The true
message length, including a final zero byte when V_i=0, is always 33.

To produce the bytes efficiently, draw L independent uniform 256-bit words
P_t and use their 32 disjoint bytes:

    V_i = (P_(i>>5) >> (8*(i AND 31))) AND 255.

All N U words and L P words are mutually independent ideal random-word draws.
Splitting an independent uniform word into bytes produces independent uniform
bytes, exactly: each specified byte tuple has probability 2^-256. Consequently
all N messages are iid uniform on D. This is not a PRNG-based independence claim.
The deterministic seeded implementation in Section 7 is only an evidence probe.

Let H be the full unkeyed BLAKE3-256 hash with two prefix rounds in every
compression. For these messages there is one chunk and one block. The root
compression uses standard IV, counter 0, true block length 33, and flags
CHUNK_START|CHUNK_END|ROOT=11. Bytes 33 through 63 are zero-filled solely
for word loading; they are not part of the message. No extra padding or
finalization compression is performed. Its input words are the eight
little-endian 32-bit lanes of U, followed by V and seven zero words.

For complete specificity, the IV in hexadecimal is

    6a09e667 bb67ae85 3c6ef372 a54ff53a
    510e527f 9b05688c 1f83d9ab 5be0cd19.

Initialize s[0..7]=IV, s[8..11]=IV[0..3], s[12..15]=(0,0,33,11).
All following additions are modulo 2^32; ROR rotates within a 32-bit lane.
The G operation G(a,b,c,d,x,y) is

    s[a] = s[a]+s[b]+x; s[d] = ROR(s[d] XOR s[a],16)
    s[c] = s[c]+s[d];   s[b] = ROR(s[b] XOR s[c],12)
    s[a] = s[a]+s[b]+y; s[d] = ROR(s[d] XOR s[a],8)
    s[c] = s[c]+s[d];   s[b] = ROR(s[b] XOR s[c],7).

In each round, with the current message schedule w, execute

    G(0,4,8,12,w[0],w[1]);   G(1,5,9,13,w[2],w[3])
    G(2,6,10,14,w[4],w[5]);  G(3,7,11,15,w[6],w[7])
    G(0,5,10,15,w[8],w[9]);  G(1,6,11,12,w[10],w[11])
    G(2,7,8,13,w[12],w[13]); G(3,4,9,14,w[14],w[15]).

Between the two rounds replace w[i] by the old w[permutation[i]], where
permutation=(2,6,3,10,7,0,4,13,1,11,12,5,9,14,15,8).
The full compression produces s[j] XOR s[j+8] and s[j+8] XOR IV[j],
j=0..7. H is the first eight output words serialized little-endian,
exactly 256 bits. The algorithm does not change this output width.

Other allowed message lengths would require the standard chunk/tree handling.
They are never generated here, so this one-compression specialization implements
the complete target for every message actually used, including verification.

## 2. Concrete algorithm

All arrays below contain 256-bit words, with explicit sizes:

| Array | Words | Meaning |
| --- | ---: | --- |
| U | N | First 32 bytes of every sampled message |
| P | L | Packed final bytes, 32 messages per word |
| A | N | Full 256-bit digests in generation order |
| B | N | Packed high digest half and original sample index |
| C | K | Low-half histogram, then starts, then ends |
| T | K | Tagged high-half lookup table |

Define MASK=K-1. Write `X[j]` for the word at byte address base_X+(j<<5).
The pseudocode specifies array accesses, not free dictionary operations.

### 2.1 Generate and count

Zero C and T in one loop over their K indices. U, P, A, and B need not be
zeroed: every element is written before its first read, as proved below.
Their storage reservation consists of constant-many base/limit calculations;
there is no assumed operating-system allocator or free initialized memory.

For t=0,...,L-1, draw one random word q, store it in P[t], and perform the
following block 32 times (it can be unrolled with constant byte positions):

    i = 32*t + r, for r=0,...,31
    u = fresh uniform 256-bit word
    U[i] = u
    v = q AND 255
    q = q >> 8
    h = H(LE32(u) || byte(v))
    A[i] = h
    b = h AND MASK
    C[b] = C[b] + 1

Every repeated input is retained and charged. Never restart or redraw it.

### 2.2 One radix partition

Convert histogram C to exclusive starts:

    running = 0
    for b=0,...,K-1:
        count = C[b]
        C[b] = running
        running = running + count

Scatter into B in sample order:

    for i=0,...,N-1:
        h = A[i]
        b = h AND MASK
        p = C[b]
        B[p] = (h AND (MASK << 128)) OR i
        C[b] = p + 1

After scattering, C[b] is the exclusive end of bucket b. Its beginning is
0 for b=0 and C[b-1] otherwise. An empty bucket has equal beginning and end.
Each packed B word stores the high 128 bits of h and the 128-bit original
index i. N<K ensures the index fits. The low half is implicit in its bucket.

### 2.3 Detect equal high halves within each bucket

Process buckets in increasing b, retaining a single cursor p initially 0:

    for b=0,...,K-1:
        end = C[b]
        tag = b << 128
        while p < end:
            packed = B[p]
            a = packed >> 128
            i = packed AND MASK
            old = T[a]
            old_id = old AND MASK
            if old_id != 0 and (old >> 128) == b:
                j = old_id - 1
                if U[i] != U[j] or V_i != V_j:
                    reconstruct M_i and M_j from U and P
                    recompute their two complete H values
                    verify messages differ and all 256 digest bits agree
                    return the two messages if verified, else failure
            else:
                T[a] = tag OR (i+1)
            p = p + 1
    return failure

The stored sample identifier is i+1, never zero. Since i+1<=N<K, it does
not carry into the tag. Initially T[a]=0 is invalid even for bucket zero.
A tag from an earlier bucket is stale and is replaced at the first access
from the current bucket. There is no per-bucket table clearing.

On encountering the same message again, leave the stored representative
unchanged. If a later message differs, it will still be detected. There is
at most one final verification, and every execution halts in the same budget.

## 3. Deterministic correctness and adversarial cases

After counting, C[b] equals the number of original digests whose low half is b.
Prefix sums allocate disjoint contiguous intervals with total size N. Each
scatter writes the next free word of exactly the appropriate interval, and
increments its cursor. Thus each B slot is written once before any read, C
ends correctly delimit every bucket, and all sampled indices occur once in B.
No uniform occupancy, expected bucket length, or distinct-input assumption is
needed. U, P, and A are fully written before scattering or detection uses them;
C and T are initialized before their first reads.

Within the current bucket b, the invariant for a high half a is: either T[a]
is invalid/stale and no item of this bucket with that high half has yet been
visited, or it points to a previously visited message in this bucket with
exactly that high half. Replacing a stale entry establishes the invariant;
retaining a representative preserves it. Therefore a valid match in T means
equality of both halves of the complete digest, not equality of a truncated
hash. Message comparison rejects identical inputs. Any digest group containing
two distinct messages eventually differs from its first representative, so
the algorithm detects a witness whenever the sample contains one.

All N digests may share their low half: this only makes one large bucket,
whose items still require one lookup each. The same high half may occur in
all K low-half buckets: tags separate them. Every sample may be a repetition
of one message: all comparisons remain bounded and no false witness returns.
There are at most N high-table lookups, N message comparisons, N scatters,
and K bucket iterations in every case. No linked-list traversal, hash-table
resize, insertion retry, or comparison sort is hidden in the bound.

The final full-hash checks are redundant in the exact RAM computation, but
charged. They cannot fail for a genuine detected pair. The result is an
ordinary complete-hash collision for the selected two-round profile.

## 4. Success probability without a hash heuristic

For fixed H on D, let p_y be the fraction of D mapping to digest y. There are
Q=2^256 possible digests. Applying a fixed function to independent messages
gives iid digests with this fixed, possibly highly nonuniform distribution.

Let e_N(p) be the elementary symmetric polynomial of degree N. Independence
implies Pr[all digests distinct]=N! e_N(p). Uniform p maximizes e_N: a maximum
exists on the compact probability simplex; among maximizers choose one with
minimum sum of squared coordinates. If two coordinates x,y differ, holding
the others r fixed gives

    e_N(p)=xy e_(N-2)(r)+(x+y)e_(N-1)(r)+e_N(r).

Averaging x and y cannot decrease this polynomial, because its coefficients
are nonnegative. It strictly decreases the sum of squared coordinates,
contradicting the choice. Thus a maximizing vector is uniform, and

    Pr[all digests distinct]
      <= product_(j=0,...,N-1)(1-j/Q)
      <= exp(-N(N-1)/(2Q)).

Let E be the event that any two input messages are equal. The union bound is

    Pr[E] <= N(N-1)/(2*2^264) < 1/512.

If some digests agree and E does not occur, Section 3 guarantees success.
Subtracting all repeated-input outcomes is conservative; many also contain
distinct-message collisions. Consequently

    Pr[success] >= 1-exp(-N(N-1)/(2Q))-Pr[E].

For N=(511/512)2^128,

    N(N-1)/(2Q) = (511/512)^2/2 - N/2^257 > 249/500.

The gap before subtracting N/2^257 exceeds 0.000048, whereas the subtracted
term is less than 2^-129. This is an exact finite-N statement.

To check the final probability without numerical transcendental rounding,
put x=249/500 and S=sum_(k=0,...,5) x^k/k!. The positive exponential series
gives exp(x)>S, hence

    Pr[success] > 1-1/S-1/512
                = 411002016533346913 / 1053058771947306496
                > 39/100.

The rational lower bound is approximately 0.39029352. The tighter exponential
expression is approximately 0.39033921, but neither approximation is needed
for the declaration 0.39. All randomness is algorithmic, not reviewer confidence.

The 33-byte domain is deliberate. A 32-byte domain could be mapped injectively
to 256-bit digests, so a universal distinct-message collision guarantee would
be impossible there. The extra byte makes the repeated-input deduction small
enough while keeping the entire experiment on a single complete root block.

## 5. Charged 256-bit RAM program and operation envelopes

Prices are those of collision-frontier-v5: each selected compression costs 1;
each listed ordinary word primitive costs 1/430. The implementation has a
fixed finite register set and uses flat word arrays. Register moves/constants
may conservatively be charged as one word operation. Ordinary operations
include every data load/store, mask, shift, add/subtract, comparison, conditional
branch, random word, cursor update, and fixed-loop control. They do not include
an interpreter's implementation overhead: this is the specified RAM program,
not the Python evidence probe. No multiplication, division, or multiword address
operation is needed. Strides use shifts; all addresses fit in one 256-bit word.

The chosen envelopes leave slack beyond the following explicit translations.
All loop bounds and digit widths are compile-time constants; the 32 samples
within one pool-word iteration can be unrolled. Register reassignment is
covered by the bounds, even when not itself a listed arithmetic primitive.

### 5.1 Generation: at most 128N + 10L ordinary operations

For each U_i draw, retain, hash, and count:

| Ordinary work for one sample | Upper bound |
| --- | ---: |
| Random U draw, store U, extract next byte from q, shift q, and advance U pointer | 5 |
| Extract eight 32-bit lanes of U (8 masks and 7 shifts) | 15 |
| Write the 16 compression message words, including V and seven zeros | 16 |
| Load/copy the public IV, counter, length and flag parameters and organize the call | 24 |
| Read eight returned digest lanes and pack them (8 loads, 7 shifts, 7 ORs) | 22 |
| Store A and advance its pointer | 2 |
| Histogram: mask low half, shift and add its byte address, load, increment, store | 6 |
| Sample index update and remaining moves/control allowance | 10 |
| Subtotal | 100 |

The envelope 128 permits 28 additional moves/loads/control operations. A
compression is charged separately, exactly once per sample, so its internal
G calls, state evolution and feed-forward are not also charged as ordinary
operations. The wrapper does not treat whole-hash serialization as free:
33 bytes are represented exactly by eight full words, V and the true length.

For each group of 32 samples, the additional random P draw, its retained store,
pool pointer and group cursor updates, loop comparison/branch, and working-q
copy use at most 10 operations. No per-sample PRNG, byte-array allocation,
external random source or message database is assumed. Thus W_gen<=128N+10L.

### 5.2 Table initialization: at most 8K operations

Use two running byte pointers, one into C and one into T. Each iteration has
two zero stores, two pointer increments, one end comparison and one branch:
six operations, within eight per index. Initial bases, ends and loop constants
belong to fixed setup. U, P, A and B are initialized by their actual writes;
Section 3 proves that no unspecified initial word is ever read.

### 5.3 Prefix scan: at most 8K operations

One C load, one C store, one running-total addition, pointer increment,
comparison and branch use six operations per bucket, within eight. C values
and the final running total are at most N<K, so arithmetic never overflows.

### 5.4 Scatter: at most 24N operations

A literal per-item translation uses: A load and pointer advance (2); low-half
mask (1); C address shift/add and load (3); retain high half and OR sample
index (2); B address shift/add and store (3); C cursor increment/store (2);
index increment, comparison and branch (3). This totals 16. Eight spare
operations cover register moves and alternative explicit cursor handling.
There are exactly N scatter iterations, not a bucket-length-dependent search.

### 5.5 Detection: at most 64N + 12K operations

The outer bucket loop has one end load, one tag shift, cursor advances and
loop comparison/branch, plus the failed inner comparison/branch for each
bucket. This takes at most 12K operations, including empty buckets.

Per visited B item, a conservative translation is:

| Work | Upper bound |
| --- | ---: |
| Load B and advance its running pointer; extract high half and index | 4 |
| Address T by high half and load its word | 3 |
| Extract identifier, test validity, extract tag, compare tag (including branches) | 6 |
| Stale-entry path: index+1, OR tag, store; or recover prior index on match | 3 |
| Address/load both U words and compare with branch | 8 |
| Address/load two P words, derive two byte positions, extract and compare bytes | 18 |
| Item cursor update and successful inner-loop comparison/branch | 3 |
| Subtotal, overcharging mutually exclusive paths | 45 |

For example, one P access uses index>>5, byte-address shift/add, and load
(4); byte position uses AND31 and shift3 (2); extraction uses shift and
AND255 (2). Two such accesses plus comparison and branch total 18. The 64
envelope has 19 spare operations for moves and alternate pointer handling.
Early exit only decreases work. No more than N message comparisons can occur.
Final reconstruction/output and verification are charged below separately.

### 5.6 Fixed work, memory and total time

Use fewer than 2^16 fixed instruction templates, each encoded in at most four
256-bit words. The program consists of the constant loops above, 32 unrolled
generation wrappers, the displayed target core and serialization. Their
straight-line sizes are far below this template cap. Reserve 2^24 bytes for
all code, public constants, at most 64 registers, state/message/output scratch,
array descriptors and loop variables. Parameter copies and any wrapper spills
are covered above; one compression can reuse its 16 state registers for output.

Reserve 2^40 ordinary operations for loading/initializing this fixed region,
base/limit arithmetic, finite code generation, and the at-most-once final
witness reconstruction/comparison/output. This is a generous explicit bound:
the reserve contains 2^19 words, whose initialization needs fewer than 16
operations each; the finite program construction and final two wrappers are
smaller still. There is no advice search or target-dependent preprocessing.

There are at most N+2 selected compressions, including final verification.
Combining the envelopes, with L=N/32,

    H_calls <= N+2,
    W <= 128N+10L + 8K+8K + 24N + 64N+12K + 2^40
       = (216+10/32)N + 28K + 2^40.

Therefore the total charged computation, including all failed samples, is

    T_total <= N+2 + ((216+10/32)N+28K+2^40)/430
             = (5513627/3522560) K + 2 + 2^40/430
             < (783/500) K
             < 2^128.65.

The last comparison can be checked entirely with integers:
783^20 < 2^13 * 500^20, so 783/500 < 2^(13/20).
The leading coefficient's diagnostic logarithm is 128.6463774; the upward
rounded declaration 128.65 accommodates fixed work with ample margin.
It is a worst-case work cap, not an expectation conditioned on finding a pair.

The storage bounds include all arrays simultaneously, even though A can be
released after scattering:

    peak bytes <= 32*(3N+L+2K) + 2^24
                = 97N+64K+2^24
                < 161K+2^24 < 256K = 2^136.

These byte addresses, counters, offsets, all K-sized table indices, N and i+1
fit in one 256-bit word. No per-entry pointer, object header, recursive stack,
OS virtual-memory mapping, lazy-zero service, or retained randomness is omitted.
The enormous memory is an abstract allowance, not a physical feasibility claim.

Preprocessing consists of table zeroing and fixed setup, at most
(8K+2^40)/430 < K/32 = 2^123 compression equivalents, already included in
T_total. Subsequent histogram and lookup work are also in the total.
Nonuniform advice is exactly zero; the schema's log2 field is set to 0,
an upper bound of one byte because log2(0) is not representable. Public code
and constants are charged in the fixed storage and initialization reserve.
The deprecated optional data_log2 field is omitted as instructed by the schema.

## 6. Comparisons and alternatives

The organizer starting point uses 2^129 iid 64-byte messages, two arrays of
three-word records and 129 merge passes, declaring time_log2=140 and memory
137. This proposal changes the sample size, domain, representation and actual
detector. It is not just a new number for the old operation envelope.

Two full 128-bit radix passes are a viable alternative, but the second pass
is unnecessary when only equality detection is required. A tagged suffix
table permits one partition, one lookup per record and no clearing between
buckets. Ordinary chaining or early bucket-pair enumeration would need an
occupancy assumption or a worse worst-case bound; neither is used here.
Structural differentials and amortized related-message families might beat
this score, but would need new target-specific probability evidence. This
package instead preserves the organizer's universal fixed-function guarantee.

The nominal reference ID blake3-r2-nominal-v2 is retained as required metadata;
the field name baseline_improved does not assert improvement over 128. The
probability requirement is 0.39; the inherited stronger 0.5 was not a track
requirement. We explicitly lower the declaration and prove the new bound.

## 7. Executable evidence and its exact limits

The declared `partition-detector` experiment runs through the organizer's
bounded networkless Python executor. It implements the same partition/tag
detector with eight-bit halves of a 16-bit key, hence 256 table slots, and
at most 255 sample indices so the nonzero identifier fits. The hash primitive
is still the complete two-round BLAKE3 profile on exactly 33-byte messages.
Only the experiment's matching predicate masks the digest to its first two
bytes. The organizer independently checks those 16 bits for returned pairs.

Before processing organizer seeds, the program checks the detector against
an independent all-pairs oracle on all 4^5 key assignments to five distinct
messages, using keys {0,1,8,9}, and all 4^3 assignments to three message types
combined with all 3^5 five-sample sequences. These finite checks cover invalid
slot zero, stale tags, duplicate messages, repeated representatives, and both
varying key halves. Additional explicit cases include all-equal low halves,
all-equal high halves across buckets, the highest legal identifier and no
collision. Assertions abort execution on any disagreement.

For each supplied seed, SHAKE-256 deterministically generates 255 inputs of
33 bytes; the exact reduced-round hash is evaluated, its low 16 bits are fed
to the detector, and one found pair or two nulls are returned. Distinct inputs
with a repeated 16-bit key are found whenever they exist in that sample.
The full-size program uses both 128-bit halves of all 256 output bits; it
does not replace the target with this truncated test.

The program also checks the exact rational probability inequality and integer
cost-rounding inequality from Sections 4 and 5. Its observations are participant
assertions, not organizer-certified operation counts. The cost proof is the
explicit RAM translation above, not a timing or a Python instruction count.

No masked collision is presented as a full collision. No extrapolation from
16 to 256 bits, empirical independence, seed-derived ideal randomness, or
measured full-scale cost is needed for the analytical claim. The universal
probability argument and invariants are self-contained. No full 256-bit
collision, full-scale run, proof-assistant verification or human acceptance
is asserted. The certificate manifest is intentionally valid and empty.
