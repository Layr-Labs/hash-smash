# SHA-256, 31 prefix rounds: a one-block birthday construction

This is an independent exploratory submission for target sha256-r31-prefix-v1,
track sha256-r31-exploratory, cost model collision-frontier-v5, and review
policy paired-lanes-v1. It gives a complete analytic algorithm for an ordinary
collision, with time_log2 at most 130, memory_log2_bytes at most 136, and
algorithmic success probability greater than 0.39. It does not provide a
computed collision or assert an AI or human verdict.

The required baseline_improved value sha256-r31-nominal-v2 identifies only the
organizer's nominal 128 reference. That reference is not a qualified baseline
or a proved implementation cost. Our 130 bound is below the 136 declared by
the repository's prior candidate; that candidate is not an accepted or
qualified baseline. We make no claim to beat the nominal 128 reference.
No property of SHA-256 resembling an ideal random function is assumed.

## 1. Exact target and one-block messages

All arithmetic inside the compression is on 32-bit words, as in SHA-256.
The target uses the standard fixed eight-word IV, the original SHA-256 message
schedule and constants at indices 0 through 30, 31 rounds per padded block,
all eight feed-forward additions, and the full 256-bit digest. There is no
chosen IV, compression-only relation, output truncation, or phase renumbering.

Let BE_k(v) denote the k-byte big-endian representation of v. Put

    q = 2^128, N = 2^256, D = 2^320.
    m(x,z) = BE_32(x) || BE_8(z),
    0 <= x < 2^256, 0 <= z < 2^64.

Every message is exactly 40 bytes and belongs to the target's domain of
finite byte strings shorter than 2^64 bits. Its complete FIPS padding is
exactly one 64-byte block:

    BE_32(x) || BE_8(z) || 0x80 || 15 zero bytes || BE_8(320).

Thus W[0] through W[7] encode x, W[8] and W[9] encode z, W[10] is
0x80000000, W[11] through W[14] are zero, and W[15] is 320. Subsequent
W[16] through W[30] use the standard schedule at their original indices.
The fixed IV, in state order, is

    6a09e667 bb67ae85 3c6ef372 a54ff53a
    510e527f 9b05688c 1f83d9ab 5be0cd19.

For completeness, write all additions modulo 2^32 and all rotations and NOT
on 32 bits. The schedule and round formulas are

    s0(u) = ROTR(u,7) XOR ROTR(u,18) XOR (u >> 3)
    s1(u) = ROTR(u,17) XOR ROTR(u,19) XOR (u >> 10)
    S0(u) = ROTR(u,2) XOR ROTR(u,13) XOR ROTR(u,22)
    S1(u) = ROTR(u,6) XOR ROTR(u,11) XOR ROTR(u,25)
    Ch(e,f,g) = (e AND f) XOR ((NOT e) AND g)
    Maj(a,b,c) = (a AND b) XOR (a AND c) XOR (b AND c)
    W[t] = W[t-16] + s0(W[t-15]) + W[t-7] + s1(W[t-2]),
      for 16 <= t <= 30
    T1 = h + S1(e) + Ch(e,f,g) + K[t] + W[t]
    T2 = S0(a) + Maj(a,b,c)
    (a,b,c,d,e,f,g,h) = (T1+T2,a,b,c,d+T1,e,f,g),
      simultaneously, for 0 <= t <= 30.

K[0] through K[30], in hexadecimal and original index order, are

    428a2f98 71374491 b5c0fbcf e9b5dba5 3956c25b 59f111f1 923f82a4 ab1c5ed5
    d807aa98 12835b01 243185be 550c7dc3 72be5d74 80deb1fe 9bdc06a7 c19bf174
    e49b69c1 efbe4786 0fc19dc6 240ca1cc 2de92c6f 4a7484aa 5cb0a9dc 76f988da
    983e5152 a831c66d b00327c8 bf597fc7 c6e00bf3 d5a79147 06ca6351.

After round 30, add each working word to its corresponding fixed-IV word.
Concatenate the eight resulting BE_4 state words in standard order. This
32-byte string is H(m); interpret it as one unsigned 256-bit digest d.
The selected-round compression, including its internal schedule, rounds, and
feed-forward, costs one target-compression unit. Interface packing, random
draws, state transfer, message construction, and storage are charged separately
below. The complete hash of each selected 40-byte message costs one such
compression, including its padding block.

## 2. Fixed algorithm

The machine is the specified classical 256-bit word RAM. For each of exactly
q sample positions, independently draw two fresh uniform 256-bit RAM words
X and Y. Set x=X and z=Y AND (2^64-1). The low 64 bits of an independent
uniform Y are uniform on 0,...,2^64-1, so each m(x,z) is independent and
uniform over the D distinct messages. This uses two fresh random-word
operations per position; no seed expansion or precomputed search substitutes
for those draws.

A record is exactly three RAM words: (digest,x,z). Allocate arrays A and B
with q records each, and a q-word counter array C. Fixed code, constants,
register spill, and output space are accounted for separately. Fill A with all
q records, hashing each complete message from the fixed IV. Do not discard
duplicate input messages during generation.

Sort the records by their complete 256-bit digest, using two stable counting
sort passes in least-significant-digit order. Set b=2^128=q and define
low(d)=d AND (b-1), high(d)=d >> 128. The following pass takes a source
array S, destination array T, and digit function f:

    for j = 0,...,b-1: C[j] = 0
    for i = 0,...,q-1: C[f(S[i].digest)] += 1
    run = 0
    for j = 0,...,b-1:
        old = C[j]; C[j] = run; run += old
    for i = 0,...,q-1:
        record = S[i]
        j = f(record.digest)
        k = C[j]; T[k] = record; C[j] = k+1

Apply the pass with f=low from A to B, then with f=high from B to A.
The counter array is cleared before each pass. It does not need any initial
contents. All q source records are initialized before each pass, and every
destination record is written once before it is read as a source. Each pass
writes in input order within a digit bucket, hence is stable. The first pass
sorts by low 128 bits; the second stable pass sorts by the high 128 bits and
then the low 128 bits. A is now sorted by all 256 digest bits. There is no
hash table, variable-length comparison, recursion, or participant experiment.

For i=1,...,q-1, inspect A[i-1] and A[i] and continue to the next i unless
their digests match and their (x,z) pairs differ. For the first such pair,
copy both messages to fixed output scratch, recompute both complete H values
from the fixed IV, and return the pair only if the full digests match and the
messages differ; return FAIL if this final verification fails. If all q-1
adjacent positions have been inspected without a qualifying pair, return
FAIL. In an exact execution, the final check cannot reject a pair found by
the scan. Equal
digests form contiguous groups; a group containing two different messages
must have an adjacent pair of different messages. The scan therefore returns
an ordinary collision whenever the sample contains one. It never treats two
copies of one message as a collision. FAIL carries no output claim.

All indices, bucket values, counts, record addresses, and byte addresses are
below 2^256. In particular, a counter can reach q but cannot overflow a
256-bit word. A record address is base+3i, implemented with additions rather
than an unpriced multiplication. The two q-bucket passes and full scan execute
on every random tape; there are no early success shortcuts, restarts, or
uncharged failed trials.

## 3. Distribution-free success bound

For each of the N possible full digest values d, let p_d be the fraction of
the D messages m(x,z) that map to d under this fixed deterministic target.
Independent uniform messages give independent draws from the same, possibly
highly nonuniform, probability vector p. No SHA-256 randomness assumption is
being made.

Let e_q(p) be the qth elementary symmetric polynomial of the N coordinates
of p. The probability of q distinct digest outputs is q! e_q(p). For any two
coordinates a and c, with all others collected into vector r,

    e_q(p) = e_q(r) + (a+c)e_(q-1)(r) + ac e_(q-2)(r).

Every coefficient is nonnegative. Replacing a,c by their average preserves
their sum, increases their product, and cannot reduce e_q. More formally,
take a maximizer of e_q on the compact probability simplex that minimizes
the sum of squared coordinates among maximizers. If two coordinates differ,
averaging them gives another maximizer with strictly smaller squared sum,
a contradiction. Hence a uniform vector maximizes e_q. Since q<=N,

    Pr(all q digests differ)
      <= q! binomial(N,q)/N^q
       = product_(j=0)^(q-1) (1-j/N)
      <= exp(-q(q-1)/(2N)).

The last step applies 1-u<=exp(-u) to each factor. It does not assume
independence of collision events.

Let R be the event that two sampled *input messages* are equal. A pair of
independent uniform D-element messages matches with probability 1/D, so the
union bound gives Pr(R)<=q(q-1)/(2D). If some digest repeats and R does not
occur, the sort and scan return two different messages with identical full
hashes. No independence between those two events is assumed. Thus

    Pr(success)
      >= 1 - exp(-q(q-1)/(2N)) - q(q-1)/(2D).

For q=2^128, N=2^256, D=2^320, let

    lambda = q(q-1)/(2N) = 1/2 - 2^-129 > 499/1000,
    q(q-1)/(2D) = 2^-65 - 2^-193 < 1/1000.

The elementary degree-three exponential lower bound gives

    exp(lambda)
      > 1 + 499/1000 + (499/1000)^2/2 + (499/1000)^3/6
      = 9865254499/6000000000
      > 1000/609.

Consequently exp(-lambda)<609/1000, and

    Pr(success) > 1 - 609/1000 - 1/1000 = 0.390.

The declared success_probability of 0.39 is a strict lower bound for the
fixed algorithm with fresh independent coins. It is not model confidence,
an observed frequency, or a claim that a practical execution has finished.

## 4. Charged time and memory

The collision-frontier-v5 price for sha256-r31 is C=2140. One selected-round
compression costs 1 target-compression equivalent. Each other 256-bit word
operation, including random draws, loads/stores, additions, Boolean operations,
shifts, comparisons, branches, and construction, costs 1/2140. Computation
is summed over all processors; this algorithm has no parallel discount.

The following is a conservative executable RAM instruction budget, not a
timing measurement. A core scalar operation is one elementary assignment,
address addition, primitive operation, load, store, comparison, or branch.
Implement it using at most eight charged word operations: up to four
instruction-word fetches, two operand loads, the operation itself, and a
result store. This includes instruction fetch and operand spill, even where
fewer than eight are needed. The fixed program uses fewer than 4096
instruction slots of at most four RAM words each. Instructions carry their
operand addresses; the SHA compression is the costed target primitive, so
its internal rounds are not separately counted.

The caps below count core operations, including loop tests, increments,
address calculations, and both actual and generously allowed scratch
bookkeeping. The per-record and per-bucket ceilings apply to every iteration.

| Phase | Core operations per item | Why the ceiling covers the phase |
| --- | ---: | --- |
| Generate one record | 256 | Two fresh random draws, mask/extract z, unpack 40 bytes, use the fixed padding and IV, dispatch one compression, pack the digest, store three words, and loop control. A 32-bit-word unpack/pack uses fewer than 64 core operations; the remaining 192 cover state transfers, addressing, loads, stores, randomness, and control. |
| Clear one counter bucket | 16 | Zero store, address/index update, loop guard/branch, and scratch reloads. |
| Histogram one record | 32 | Read digest, extract one 128-bit digit, address/read/increment/write its counter, advance record position, guard/branch, and scratch reloads. |
| Prefix one counter bucket | 32 | Read old count, write current run, add old count to run, advance bucket, guard/branch, and scratch reloads. |
| Scatter one record | 48 | Read three source words, extract digit, address/read/increment/write its counter, compute destination base+3k using three additions, write three words, advance source, guard/branch, and scratch reloads. |
| Scan one adjacent position | 128 | Address/read at most six fields, compare full digests and both message fields, branch and advance; the one possible final rehash is separately charged. |

The three-word source and destination records are contiguous; maintained
pointers avoid unbounded address work. In the scatter phase, even counting
six source reads/address steps, three digit steps, eight counter steps, six
destination-address steps, six destination writes, and five loop/control
steps gives 34 core operations, leaving 14 within its 48-operation cap.
The other per-item caps similarly include scratch allowance. No per-record
allocation, object header, unbounded operation, or large initialization is
hidden. Initializing all q counter words is charged in each radix pass.

Multiplying each core cap by eight charged operations gives:

| Phase | Target compressions H | Other charged operations W |
| --- | ---: | ---: |
| Fixed setup | 0 | at most 2^20 |
| Generate all q records | q | at most 2048q |
| Each radix pass: clear, histogram, prefix, scatter | 0 | at most (128+256+256+384)q + 2^16 = 1024q + 2^16 |
| Both radix passes | 0 | at most 2048q + 2^17 |
| Adjacent scan | 0 | at most 1024q |
| At most one final verification and output | at most 2 | at most 8192 |

The 2^16 fixed allowance in each pass covers loop initialization, final
exit tests, base selection, and reuse of the counter array. Fixed setup
loads code/constants, clears fixed scratch, prepares the IV/padding and
array bases; it is below 2^20 ordinary operations. The two verified
complete hashes use one compression each. The final 8192 cap also includes
all interface and output instructions, so these are not omitted.

Therefore, including failed executions,

    H <= q+2,
    W <= 5120q + 2^20 + 2^17 + 8192
      = 5120q + 1187840,
    T = H + W/2140
      <= (1 + 5120/2140)q + 2 + 1187840/2140
       = (363/107)q + 2 + 1187840/2140
       < 4q = 2^130.

The final strict inequality has a margin of (65/107)q minus fewer than
558 fixed units, positive for q=2^128. This proves time_log2:130, rather
than relying on an unpriced comparison sort or on the nominal reference.
The declared preprocessing_log2:20 is a loose upper bound in compression
equivalents: the fixed setup is at most 2^20 ordinary operations and is
already included in T. There is no nonuniform search or advice.

Peak retained memory is two q-record arrays plus q counter words:

    M <= (3q + 3q + q)*32 bytes + 2^20 bytes
      = 224q + 2^20 bytes
      < 256q = 2^136 bytes.

The fixed-memory allowance includes code (under 4096 instruction slots of
four words, or 2^19 bytes), constants, IV, padding, state, indices, saved
records, spills and output (under 4096 more words, or 2^17 bytes).
No array needs zeroing except C as explicitly charged. The declared
memory_log2_bytes:136 holds on every random tape. Random words retained
as messages are already in A/B; there is no stored random tape.

Nonuniform advice is exactly zero bytes. The schema's nonnegative
nonuniform_advice_log2_bytes:0 is a one-byte upper-bound convention, not
a claim of one actual advice byte. The program and public target constants
are uniform but their storage and setup are still included above. Optional
legacy data_log2 is omitted because it is not a scored or reviewed resource.

## 5. Evidence and limitations

This package declares no heuristic premise and no experiment manifest.
The empty certificate manifest is valid. The correctness, probability,
and resource claims follow from the explicit target, random-word model,
counting-sort algorithm, and arithmetic here. A toy experiment cannot
establish full-scale execution or the all-distributions lemma. No participant
program is submitted for organizer execution.

This is an astronomically expensive theoretical construction, not a practical
SHA-256 break or a measured run. The local mechanical checker can verify
package form, but only remote review can issue the lane's AI screening
decision, and any qualifying improvement still requires the benchmark
owner's manual review and promotion. Neither AI screening nor promotion is
a mathematical proof of this argument.
