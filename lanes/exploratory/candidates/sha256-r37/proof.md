# A distribution-free hash-table birthday search for SHA-256 r37

## Claim and scope

This package specifies a classical randomized algorithm for the exact
`sha256-r37-prefix-v1` target in the exploratory lane. Its worst-case total
charged time is less than `2^128.2` target-compression units, its peak memory is
less than `2^137.33` bytes, its preprocessing is less than `2^122.22` such time
units, and its probability of returning two distinct complete messages with equal
full 256-bit digests exceeds `0.39`. The probability is over fresh independent
algorithmic coins for the fixed target. No property resembling a random oracle,
output balance, differential independence, or pseudorandomness of SHA-256 is
assumed. `heuristics` is empty. The claim states conservative upper bounds; no
collision witness, executed full search, or novelty is asserted.

The construction is the generic birthday attack (sampling about `2^128`
uniform one-block messages) used by the organizer's earlier package for this
track, with one change: a 128-pass merge sort, which cost about 13 compression
equivalents per sample under collision-frontier-v5, is replaced by a chained hash table whose
bucket index is a randomly keyed tabulation hash of the digest. Universality of
that keyed hash gives a distribution-free bound on the expected lookup work, and
a hard cap on lookup work turns this expectation into a worst-case time bound at
a cost of at most `1/128` in success probability. The remaining ordinary work
is at most a few hundred primitives per sample, so the total is within `0.2`
bits of the sample count.

The required `baseline_improved` value `sha256-r37-nominal-v2` identifies the
organizer nominal reference, not an established attack. This package does not
claim to beat that reference's display value of 128. `ready` requests review; it
is not qualification, a trusted score, or human acceptance.

Under collision-frontier-v5 one selected target compression (standard SHA-256
schedule and constants, round indices 0 through 36 inclusive, standard wordwise
feed-forward) costs 1, and every other 256-bit word-RAM primitive costs `1/C`
with `C = 2644`. Marshaling of compression inputs and outputs is charged
separately as ordinary primitives below.

## Notation and parameters

```
n   = 2^128 + 2^121 = 129 * 2^121       number of sampled messages
M   = 2^256                             number of digest values
d   = 2^384                             size of the message domain D
k   = 132                               bucket-index width; 2^132 buckets
Q   = n^2 / 2^126 = 16641 * 2^116       cap on non-matching chain probes
C   = 2644                              ordinary primitives per compression unit
```

All of `n`, `Q`, `2^132` and every address used below are below `2^140` and fit
in one 256-bit RAM word.

## Complete messages and their hashes

In each trial obtain two fresh independent uniform 256-bit random words U and R,
and set `V = R AND (2^128 - 1)`. The complete message is the 48-byte string
`BE32(U) || BE16(V)`, where BEk denotes exactly k bytes in big-endian order.
Messages are therefore iid uniform on a domain D of size `d = 2^384`, and all
have original bit length 384, within the profile's length limit.

FIPS 180-4 padding appends byte 0x80 at offset 48, zero bytes through offset 55,
and the 64-bit big-endian bit length 384 at offsets 56 through 63. The message
fits in exactly one padded block, whose sixteen 32-bit big-endian words are

```
W[i]    = (U >> (224 - 32*i)) AND 0xffffffff     for i = 0..7
W[8+i]  = (V >> (96  - 32*i)) AND 0xffffffff     for i = 0..3
W[12]   = 0x80000000
W[13]   = 0
W[14]   = 0
W[15]   = 0x00000180   (= 384)
```

The complete hash h starts from the standard fixed IV
`6a09e667 bb67ae85 3c6ef372 a54ff53a 510e527f 9b05688c 1f83d9ab 5be0cd19`,
applies one selected 37-round compression with feed-forward to this block, and
serializes the eight resulting words big-endian. No extra padding block exists,
no chaining state is chosen, and no output bit is discarded. The algorithm packs
the eight output words into one 256-bit digest word

```
Y = sum over i = 0..7 of (o[i] << (224 - 32*i)),
```

which is exactly the 32-byte digest read as a big-endian integer; equal Y means
equal complete 256-bit digests.

## The keyed bucket function

Split a 256-bit word Y into four 64-bit chunks `y[j] = (Y >> 64*j) AND (2^64-1)`
for `j = 0..3`. During preprocessing fill four tables `T0..T3`, each of `2^64`
words, with independent uniform random 256-bit words. Define

```
g(Y) = (T0[y0] XOR T1[y1] XOR T2[y2] XOR T3[y3]) AND (2^132 - 1).
```

**Lemma 1 (universality).** For fixed distinct words `Y != Y'`,
`Pr[g(Y) = g(Y')] = 2^-132` over the table contents.

*Proof.* Choose j with `y[j] != y'[j]`. Condition on every table entry except
`Tj[y[j]]`. Every other term in `g(Y) XOR g(Y')` is then fixed, because each
chunk position uses its own table and `Tj[y'[j]]` is a different entry. The
remaining entry `Tj[y[j]]` is uniform, so the low 132 bits of
`g(Y) XOR g(Y')` are uniform and equal zero with probability exactly `2^-132`.
Averaging over the conditioning gives the claim. ∎

The tables are drawn from the algorithm's own coins before any message is
sampled, so they are independent of all messages and digests.

## Algorithm

Memory consists of disjoint regions: a fixed area of fewer than `2^15` words
(code, constants, IV, a 16-word message buffer MB, eight output words OB,
registers spill area); the four tables (`2^66` words); a head array `HD` of
`2^132` words; and a record array RA of `4n` words. A record occupies four
consecutive words `(Y, U, V, next)`. A pointer to a record is its word address,
which is never 0 because RA does not begin at address 0; the value 0 denotes the
empty chain.

Preprocessing:

1. Load the fixed constants into registers and the fixed area: masks
   `2^32-1`, `2^64-1`, `2^128-1`, `2^132-1`, the region bases, n, Q, the IV and
   the constant buffer words `MB[12..15] = 0x80000000, 0, 0, 0x180`.
2. Fill `T0..T3` with `2^66` fresh random words.
3. Set every word of HD to 0.

RA is not initialized; see the access argument below.

Main loop. Registers hold the trial counter t, the next free record address a
(initially the base of RA), the probe counter X (initially 0) and the constants.

```
for t = 1, ..., n:
    U = RANDOM256(); R = RANDOM256(); V = R AND (2^128-1)
    write W[0..11] into MB[0..11] as in the padding section
    o[0..7] = COMPRESS37_WITH_FEEDFORWARD(IV, MB[0..15])
    Y = pack(o[0..7])
    hb = HD_base + g(Y)            # address of the bucket head
    h = load(hb); p = h
    while p != 0:
        if load(p) == Y:                       # equal full digests
            if load(p+1) != U or load(p+2) != V:
                goto SUCCESS(p)               # distinct messages
            goto NEXT_TRIAL                   # repeated input: skip it
        X = X + 1
        if X > Q: return FAILURE              # work cap reached
        p = load(p+3)
    store(a) = Y; store(a+1) = U; store(a+2) = V; store(a+3) = h
    store(hb) = a; a = a + 4
  NEXT_TRIAL:
return FAILURE

SUCCESS(p):
    m0 = BE32(U) || BE16(V); m1 = BE32(load(p+1)) || BE16(load(p+2))
    recompute h(m0) and h(m1) from the fixed IV
    if m0 != m1 and h(m0) == h(m1): return (m0, m1)
    return FAILURE
```

The final check uses two more selected compressions. In the exact computation
model it cannot fail once SUCCESS is reached. There is no restart, retry, or
success amplification.

**Access argument for the uninitialized record array.** RA words are read only
through a pointer p taken from a head word or from a `next` field. A head word is
either its initial 0 or the address of a record whose four words were all stored
immediately before that head store. A `next` field is written at insertion with
the bucket's previous head value, which by induction is 0 or the address of a
completely written record. Thus every RA word that is read was previously written
by the algorithm. HD and the tables are fully initialized in preprocessing.
Records are only prepended, so each chain is a finite acyclic list ending in 0.

## Correctness of the search

Call a trial *processed* if its loop body ran to `NEXT_TRIAL` or to an insertion.
Two invariants hold after every processed trial:

- (I1) for every processed trial i there is a stored record whose fields equal
  `(Y_i, U_i, V_i)`: either its own record or, if it was skipped as a repeated
  input, the stored record with the same digest and the same message;
- (I2) no two stored records have the same Y. An insertion happens only after
  the whole chain of `g(Y)` was searched without finding Y, and records with
  equal Y always lie in the same bucket.

**Lemma 2.** If the run is not stopped by the work cap and there exist trials
`i < j` with `Y_i = Y_j` and `(U_i,V_i) != (U_j,V_j)`, the algorithm returns a
pair of distinct messages with equal complete digests.

*Proof.* Let j be the smallest index for which such an i exists. SUCCESS can be
reached at a trial j' only through such a pair with `j' >= j`, so all trials
before j were processed. By (I1) a stored record holds `(Y_i, U_i, V_i)`, and by
(I2) it is the only stored record with digest `Y_j`. It lies in bucket `g(Y_j)`,
so trial j's chain walk reaches it (no abort by assumption). Its message differs
from trial j's message, so SUCCESS is reached with two distinct messages of equal
Y, hence equal complete digests. ∎

## The work cap holds except with probability below 1/128

Consider the hypothetical run that ignores the cap. The digest sequence, which
trials are inserted or skipped, and the stopping trial depend only on the
messages: equality of Y and messages decides every branch except how many
non-matching records are passed, and records with equal Y share a bucket for
every key. Hence the set S_j of stored records when trial j starts is a function
of the messages alone, and by (I2) its digests are distinct, with
`|S_j| <= j - 1`.

At trial j, X increases once for each record in S_j whose digest differs from
`Y_j` but whose bucket equals `g(Y_j)`. Conditioning on all messages and using
Lemma 1 with the independence of the tables,

```
E[increase at trial j | messages] <= (j - 1) * 2^-132,
E[X_total] <= sum_{j=1..n} (j - 1) * 2^-132 = n(n-1) / 2^133.
```

The real run aborts only if the hypothetical count exceeds Q. By Markov's
inequality,

```
Pr[abort] <= E[X_total] / Q <= (n(n-1)/2^133) / (n^2/2^126) < 2^-7 = 1/128.
```

## Distribution-free success bound

Fix h. For each 256-bit digest y let `p_y = |{m in D : h(m) = y}| / d`. A fixed
function applied to iid inputs gives iid outputs with this distribution, which
need not be uniform. For `2 <= n <= M`, the probability that all n outputs are
distinct is `n! e_n(p_1, ..., p_M)`, where `e_n` is the elementary symmetric
polynomial of degree n, since each set of n distinct labels has n! orders.

This is maximized by the uniform distribution. Holding all other coordinates
fixed, `e_n` has the form `A + (a+b)B + abE` in any two coordinates a, b, with
`E >= 0`. Replacing a and b by their average keeps their sum and cannot decrease
`e_n`. On the compact simplex, choose a maximizer of `e_n` that minimizes the sum
of squares among all maximizers. If two coordinates differed, averaging them
would either increase `e_n` or keep it while strictly decreasing the sum of
squares, a contradiction either way. Hence the uniform point is a maximizer, and
for every fixed h

```
Pr[no repeated output] <= prod_{i=0..n-1} (1 - i/M) <= exp(-n(n-1)/(2M)),
```

using `1 - z <= exp(-z)`. No pairwise-independence assumption is used.

Let `E_out` be the event that two trials have equal Y, `E_in` the event that two
trials have the same message, and A the abort event. On `E_out` minus `E_in`
there is a pair as in Lemma 2, so success holds outside A. Each of the
`n(n-1)/2` trial pairs has equal messages with probability `1/d`, so a union
bound gives

```
Pr[success] >= 1 - exp(-n(n-1)/(2M)) - n(n-1)/(2d) - Pr[A].
```

For the chosen parameters, `n^2 / 2^257 = 129^2 * 2^242 / 2^257 = 16641/32768`,
so

```
x = n(n-1)/2^257 = 16641/32768 - n/2^257 > 0.5078,
n(n-1)/(2d) < n^2 / 2^385 < 2^-128.
```

Using the series lower bound for `exp`,

```
exp(0.5078) > 1 + 0.5078 + 0.5078^2/2 + 0.5078^3/6 + 0.5078^4/24 > 1.6613,
```

and `1.6613 * 0.602 = 1.0001026 > 1`, so `exp(-x) < 1/1.6613 < 0.602`. Therefore

```
Pr[success] > 1 - 0.602 - 1/128 - 2^-128 = 0.3901875 - 2^-128 > 0.39.
```

The bound holds for every fixed function on these messages with a 256-bit
output, including the exact reduced SHA-256 profile. It neither extrapolates
from fewer rounds nor uses a property of the target. The ideal independent
random-word primitive belongs to the collision-frontier-v5 model.

## Complete operation ledger

One target compression costs 1; every ordinary primitive costs `1/2644`. Every
load, store, addition, bitwise operation, shift, comparison, conditional branch,
unconditional jump, and random word is counted, including address arithmetic
and loop control. Unconditional jumps are charged as
primitives even though the model lists only conditional branches, and the few
register-to-register moves (such as `p = h`) are not itemized but fit the
headroom described below. The program uses a fixed set of at most 32 registers;
loading constants into them is in the fixed overhead. All bounds hold on every random
tape and are summed over all processors.

### Per-trial work, excluding non-matching chain probes

| Step | Primitives, at most |
| --- | ---: |
| Two random words and the 128-bit mask | 3 |
| Unpack U into `MB[0..7]`: shift, mask, address add, store per word | 32 |
| Unpack V into `MB[8..11]`: shift, mask, address add, store per word | 16 |
| Compression input/output traffic: 24 input loads and 8 output stores, each with an address add (the compression itself is priced as 1 unit) | 64 |
| Pack Y: per word an address add, a load, a shift and an OR | 32 |
| Bucket g: 3 shifts, 3 masks, 4 table-address adds, 4 loads, 3 XORs, 1 width mask, 1 head-address add | 19 |
| Load the bucket head | 1 |
| End of chain (`p != 0` test and branch) then insertion: 3 address adds, 4 record stores, 1 head store, 1 pointer add | 11 |
| or instead a matching probe and skip: test `p != 0`, load and compare Y, 2 address adds, 2 loads, 2 compare-and-branch pairs, jump | 14 |
| Trial counter increment, comparison, branch | 3 |
| Total with the larger of the two alternatives | 184 |

A trial reaches either the insertion or a single matching probe, not both. The
claim charges `256` primitives per trial, which leaves more than 35 percent of
headroom over this explicit count for register spills or a less favorable
encoding.

### Non-matching chain probes

Each non-matching probe executes the `p != 0` test and branch (2), a Y load (1),
a compare and branch (2), the X increment (1), the comparison with Q and branch
(2), an address add and a `next` load (2), and a jump (1): 11 primitives. The
claim charges 16. At most `Q + 1` such probes execute, because the run stops as
soon as X exceeds Q. The single extra probe is in the fixed overhead.

### Preprocessing

- Clearing HD: an unrolled loop writes four words per iteration with four
  address adds and four stores, plus a pointer add, a comparison and a branch:
  11 primitives per 4 words, under `3 * 2^132` in total.
- Filling the tables: per word one random draw, one store, one address
  increment, plus amortized loop control, under 4 primitives, so `2^68` total.
- Constants, MB padding words, IV and register setup: under `2^20`.

### Fixed overhead

Under `2^25` primitives in total cover the preprocessing constants, the one
probe beyond Q, the SUCCESS reconstruction of two messages and their marshaling
(about 300 primitives), comparison of digests and messages, and output. The two
verification compressions are charged as 2 units.

### Total

| Category | Selected compressions | Ordinary primitives, at most |
| --- | ---: | ---: |
| n trials | n | `256 n` |
| Non-matching probes | 0 | `16 Q` |
| Clearing HD | 0 | `3 * 2^132` |
| Random tables | 0 | `2^68` |
| Fixed overhead and verification | 2 | `2^25` |

In units of `2^121`, using `n = 129 * 2^121`, `Q = 16641 * 2^116`:

```
2644 n   = 341076   * 2^121
256 n    =  33024   * 2^121
16 Q     =   8320.5 * 2^121
3*2^132  =   6144   * 2^121
```

so

```
2644 T <= 2644(n + 2) + 256n + 16Q + 3*2^132 + 2^68 + 2^25
        = 388564.5 * 2^121 + 5288 + 2^68 + 2^25
        < 388565.5 * 2^121.
```

Now `(5741/5000) * 2^128 * 2644 = 388587.6224 * 2^121`, so
`T < (5741/5000) * 2^128 = 1.1482 * 2^128`. Since
`5741^5 = 6236454157912944701 < 6250000000000000000 = 2 * 5000^5`,
`1.1482 < 2^0.2`, and

```
T < 2^128.2.
```

The claim `time_log2 = 128.2` is this rounded-up bound. The unrounded ledger is
about `2^128.1993`. Preprocessing, already included in T, satisfies

```
P <= (3*2^132 + 2^68 + 2^20) / 2644 < 0.01816 * 2^128 < 2^122.22,
```

since `48/2644 < 0.018155` and `2^-5.78 > 0.01819`.

For context only (not used in any bound): the organizer's earlier package for
this track, which this one replaces, charged `34304` ordinary primitives per
sample, mostly for 128 merge passes, and claimed `2^132`.
The sample count here is larger by the factor `129/128`, to pay for the
`1/128` abort allowance; the ordinary work drops from about 13 to about 0.15
compression units per sample.

## Peak memory, code, and advice

| Region | Bytes |
| --- | ---: |
| Head array HD, `2^132` words | `2^137` |
| Record array RA, `4n` words | `128 n = 129 * 2^128` |
| Tables `T0..T3`, `2^66` words | `2^71` |
| Code, constants, IV, MB, OB, registers spill, output | `< 2^20` |

The total is less than `2^137 + 129*2^128 + 2^72 = 2^137 * (1 + 129/512) + 2^72`.
Since `1 + 129/512 = 1.251953...` and `2^0.33 > 1.2570`, peak memory is below
`2^137.33` bytes. Addresses are below `2^133` words and fit in one RAM word.
Feasibility on existing hardware is not asserted; the resource model admits
this RAM size, and memory does not enter the score.

The program is uniform. It uses only public profile constants and the fixed
numerical parameters stated here. The random tables come from algorithmic coins
at run time and are charged as preprocessing time and memory. There is no
target-dependent nonuniform advice and no precomputed collision.
`nonuniform_advice_log2_bytes = 0` records an upper bound of one byte, which
covers zero bytes.

## Evidence and source context

The success and resource arguments are fully contained above. The empty
certificate manifest asserts no witness. No experiment is declared or needed.
None of the bounds relies on sampled toy behavior, timing, a seeded PRNG, or
execution of the infeasible search.

Context sources, not missing proof steps:

- NIST, FIPS 180-4, Sections 5.1.1, 5.3.3 and 6.2.2: standard SHA-256 padding,
  initialization, schedule and feed-forward. The organizer profile fixes the
  37-round prefix. `https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf`.
- J. L. Carter and M. N. Wegman, *Universal classes of hash functions*, JCSS
  18(2), 1979: universal hashing and expected chain length. Lemma 1 is proved
  directly here for the tabulation family used.
- M. Bellare and T. Kohno, *Hash Function Balance and Its Impact on Birthday
  Attacks*, 2004: fixed functions, iid inputs, and trivial repeated-input matches.
- The organizer's earlier package for this track: sampling layout and the uniform
  maximization argument, reused here with the sort replaced by the keyed table.
  Everything needed from it is restated above.
