# Five-round SHA3-256: distinguished-point generic collision search, every instruction charged

The scalar below is `time_log2` under `collision-frontier-v5` with C = 1355.
Memory remains a separately reported resource bound.

This independent **exploratory** package selects `sha3-256-r5-exploratory`,
target `sha3-256-r5-prefix-v1`, cost model `collision-frontier-v5`, and policy
`paired-lanes-v1`. It submits a complete analytic algorithm, not an already
computed collision. It is the **van Oorschot-Wiener distinguished-point (DP)
search** (Journal of Cryptology, 1999) run on a single processor with every
instruction charged. It is **not** a cryptanalytic advance: the scalar sits just
above the nominal 128 because nothing is left out. Only the success-probability
lower bound uses a heuristic (H-RF, random-function); correctness and all time,
memory and preprocessing bounds hold for every run without any heuristic.

| `claim.json` field | value |
| --- | --- |
| `time_log2` | **128.03** (worst-case bound below 2^128.023 for every run, rounded up) |
| `memory_log2_bytes` | 112 |
| `success_probability` | 0.39 (bounded below by 0.3913 under H-RF) |
| `preprocessing_log2` | 0 (a few-operation setup, below one unit, already inside T) |
| `nonuniform_advice_log2_bytes` | 0 |
| `baseline_improved` | `sha3-256-r5-nominal-v2` (required identifier; no improvement over an established attack asserted) |

Prior art. A concurrent exploratory submission by `winglock` applies the same DP
method to the six-round sibling `sha3-256-r6-exploratory`; the standard DP
algorithm and birthday analysis used here are from van Oorschot-Wiener and are
textbook, not that submission's invention. This package reapplies the method to
the five-round target independently and prices it under C = 1355.

## 1. Exact complete hash

The iteration uses messages of exactly 32 bytes, a subset of the profile's
finite-byte-string domain with bit length 256 < 2^64. Write `msg(x) = LE32(x)`:
the 32 little-endian bytes of a 256-bit integer x, including zeros. This map is
injective, so any `x != x'` with equal complete digests yields two distinct
32-byte messages that collide.

H is the following complete hash. Initialize a 1600-bit state to zero, as 25
lanes A[x,y] of 64 bits indexed x+5y. The message occupies four lanes; pad it to
the one 136-byte rate block

    msg(x) || 0x06 || (102 zero bytes) || 0x80.

This is SHA3's domain suffix 01 followed by pad10*1, with delimited suffix 0x06.
There is no length trailer. The 17 little-endian 8-byte rate lanes are: lanes
A[0..3] hold the four 64-bit words of x; lane A[4] holds 0x0000000000000006;
lanes A[5..15] are zero; lane A[16] holds 0x8000000000000000. XOR these 17 lanes
into A[0],...,A[16]; from the all-zero state this just sets them. The eight
capacity lanes A[17..24] are zero. Apply rounds 0,1,2,3,4, in order, each with
the following formulas; x,y and coordinate subscripts are modulo 5:

    C[x] = XOR over y of A[x,y]
    D[x] = C[x-1] XOR ROT64(C[x+1],1)
    A[x,y] = A[x,y] XOR D[x]
    B[y,2x+3y] = ROT64(A[x,y],rho[x,y])
    A[x,y] = B[x,y] XOR ((NOT64 B[x+1,y]) AND B[x+2,y])
    A[0,0] = A[0,0] XOR RC[round].

All chi right-hand sides read the temporary B array. ROT64 rotates left within
64 bits; NOT64 complements only those bits. The rho offsets, with rows y=0,...,4
and columns x=0,...,4, are:

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

After round 4, H(msg(x)) = LE8(A[0])||LE8(A[1])||LE8(A[2])||LE8(A[3]). These are
all 256 output bits, the first 32 squeeze bytes in SHA3 order. No additional
permutation is required because 32 < 136. Absorption XORs into the 1088-bit
rate; the capacity is 512 bits and there is no Davies-Meyer feed-forward. Thus
each complete hash uses exactly one selected five-round permutation, denoted
PERM5. This is the profile's complete padded, fixed-IV hash. The prefix is the
first five Keccak-f rounds, not Keccak-p's last-round convention.

## 2. Iteration function and why an f-collision is an ordinary collision

Define `f: {0,1}^256 -> {0,1}^256` by `f(x) = H(msg(x))`, read as the 256-bit
integer whose little-endian bytes are the digest. Because `msg` is injective and
H is the complete fixed-IV hash,

    f(x) = f(x') with x != x'  ==>  msg(x) != msg(x') and H(msg(x)) = H(msg(x')),

i.e. a functional collision of f is exactly an ordinary collision of the target
on two distinct 32-byte messages. No independence or distributional assumption
is used for this implication; it is a consequence of injectivity of `msg`. The
four output lanes A[0..3] are exactly the four input lanes of the next
evaluation, so one step feeds the next with no reformatting.

There is no repeated-input subtlety: the two colliding preimages produced below
are distinct points of the domain by construction, hence distinct messages.

## 3. The algorithm

Fixed constants: a point is **distinguished** (a DP) iff its low 32 bits are zero
(DP rate theta = 2^-32); maximum chain length L = 2^40; evaluation budget
K0 = 65300 * 2^112; distinguished-record cap Dcap = 2^98.

The state holds 25 lanes R0..R24, a global evaluation counter g, a table T of at
most Dcap distinguished records keyed by the 224 high bits of a DP, and a few
scalars. One PERM5 call costs one unit plus one operation to issue it; its
internals are not charged again, matching the cost model's definition of C as a
count of data-word operations excluding the selected compression's internals.

- **CHAIN** (at most 11 ordinary operations). If g >= K0, stop. Otherwise draw a
  fresh uniform 256-bit start s, write its four words into R0..R3, and set the
  per-chain evaluation counter to 0.
- **BLOCK**, the inner step, unrolled 16 times per control pass. Each evaluation:
  write the 21 non-message lanes (R4 = 0x06, R16 = 0x8000000000000000,
  R5..R15 = 0, R17..R24 = 0), call PERM5, and then test the DP predicate on the
  low 32 output bits (one AND, one compare, one branch). The output lanes already
  sit in R0..R3 as the next input. Loop control (3 operations) runs once per 16
  evaluations, so at most (21 + 1 issue + 3 DP-test)*16 + 3 = 403 ordinary
  operations per 16 evaluations, i.e. at most 403/16 = 25.1875 ordinary
  operations per evaluation besides the one PERM5 unit. Increment g per
  evaluation. If L evaluations pass with no DP, abandon the chain and go to
  CHAIN (this is a charged but almost-never-taken path, see Section 6).
- **DPFOUND.** On reaching a DP, look up its 224 high bits in T (a depth-224
  binary trie; at most 15 + 224*17 + 9 < 3832 operations, charged as at most
  2^13 operations per chain). If absent, insert the record (start s, DP value,
  chain length) and go to CHAIN. If present and the stored start differs, go to
  RELOCATE. If Dcap would be exceeded, stop (a charged, negligible-probability
  path).
- **RELOCATE** (first repeated DP). Two chains reach the same DP. Re-walk both
  from their starts, first advancing the longer one so both have equal remaining
  length, then stepping them together until their current points coincide; the
  two immediately preceding points x_a, x_b satisfy f(x_a) = f(x_b). This costs
  at most 2L evaluations, charged as 3L evaluations at (1 + 64/1355) units each.
- **OUTPUT.** Recompute f(x_a) and f(x_b) (2 PERM5 units + at most 200 ordinary
  operations), verify x_a != x_b and that all 256 output bits agree, and return
  msg(x_a), msg(x_b). One run, no restart; the run halts at its first RELOCATE.

## 4. Correctness of a returned pair

RELOCATE is entered only when two chains with different starts reach a common DP.
Walk both chains forward to that DP. Since f is a function, once two chains meet
at a point they coincide ever after; let the meet point be the first common
point. Its two distinct predecessors x_a (on one chain) and x_b (on the other)
satisfy f(x_a) = f(x_b) = (meet point). They are distinct because the chains had
different starts and the walk aligns remaining lengths before stepping together,
so a coincidence of predecessors would force identical starts (Lemma 2,
Section 6, rules out the degenerate contact-on-a-start case as a bad event). By
Section 2, msg(x_a) and msg(x_b) are then two distinct 32-byte messages with
equal complete five-round SHA3-256 digests. OUTPUT re-verifies x_a != x_b and
full 256-bit digest equality before returning, so a returned pair is always a
correct ordinary collision. If the budget K0 is reached with no RELOCATE, the
run halts with failure; no pair is returned.

This correctness argument uses no distributional assumption; it is purely the
functional-graph property of f and injectivity of msg.

## 5. Fully charged time

Worst-case charged time, every run, classical 256-bit word RAM. Each PERM5 costs
one unit; every other listed primitive operation costs 1/1355 units.

| Phase | PERM5 calls (cost 1) | Ordinary operations (cost 1/1355) |
| --- | ---: | ---: |
| Setup (code, constants, counters) | 0 | at most 2^8 |
| Chaining control | 0 | at most 11 per chain |
| Evaluations (BLOCK) | at most K0 + L | at most 25.1875 per evaluation |
| DP lookups/inserts | 0 | at most 2^13 per DP-terminated chain (<= Dcap of them) |
| RELOCATE (once) | 0 | at most 3L at (1 + 64/1355) units |
| OUTPUT (once) | at most 2 | at most 200 |

The DPFOUND lookup/insert is executed only when a chain reaches a distinguished
point, hence at most Dcap = 2^98 times in total; abandoned chains incur only the
11-operation CHAIN control. The extra at most L evaluations used to run the final
in-progress chain to its distinguished point after the K0-th evaluation (the
boundary rule of Section 6, Lemma 2) are counted as PERM5 calls below.

**Bounding the number of chains (not folded into the per-evaluation coefficient).**
The per-chain control (11) and DP lookup/insert (at most 2^13) costs are charged
separately from the 25.1875-per-evaluation BLOCK envelope, and are bounded through
the number of chains, which is bounded deterministically rather than by K0. A
chain terminates either by reaching a distinguished point or by abandonment after
L evaluations with none. (i) At most Dcap = 2^98 chains terminate at a
distinguished point: each inserts exactly one record into T, the first repeated
distinguished point triggers RELOCATE and halts the run, and reaching the cap
Dcap also halts the run, so at most Dcap distinguished-point terminations occur
before the run ends. (ii) At most K0/L = 2^128/2^40 = 2^88 chains are abandoned,
since each abandoned chain spends L = 2^40 evaluations and the total number of
evaluations is at most K0. Hence the number of chains is at most Dcap + 2^88 <
2^99. The DPFOUND lookup/insert runs only on DP-terminated chains, at most
Dcap = 2^98 times, contributing at most 2^98 * 2^13 = 2^111 operations; the
11-operation CHAIN control runs once per chain, at most 2^99 * 11 < 2^103
operations. All per-chain work is therefore below 2^112 ordinary operations, i.e.
2^112/1355 < 2^102 units, negligible against K0 = 2^128. Hence

    PERM5 calls <= K0 + L + 2,
    ordinary operations W <= 25.1875 * (K0 + L) + 2^112 + 2^8 + 3L*64 + 200.

RELOCATE contributes at most 3L PERM5-equivalent = 3*2^40 units, and its ordinary
part 3L*64/1355 < 3*2^40 units; the per-chain total is below 2^102 units; all
non-BLOCK terms are below 2^103, negligible against 2^128. Therefore

    T = (PERM5 calls) + W/1355
      <= K0 * (1 + 25.1875/1355) + 2^103
       = K0 * 1.018589 + 2^103.

With K0 = 65300 * 2^112, log2(K0) = log2(65300) + 112 = 15.99469 + 112 =
127.99469, and log2(1.018589) = 0.026576, so

    log2(T) <= 127.99469 + 0.026576 + (2^103 term, < 2^-24 in log2)
            < 128.02127.

The declared `time_log2 = 128.03` is a conservative upper bound on this value
with more than 0.008 bits of slack. A reviewer reconstructing the ledger with the
same or smaller per-operation envelopes obtains at most 2^128.0213, strictly
below the submitted 128.03 and far below the organizer nominal-display reference
of 129 and the baseline 137.785. This is a one-processor cost; the cost model
charges total work across processors, and a parallel DP search has the same total
work, so parallelization does not change the scalar.

## 6. Success probability (uses heuristic H-RF)

Let N = 2^256. Model each evaluation of f at a never-before-seen point as
returning a value uniform on {0,1}^256, independent of all coins and prior
observations (heuristic H-RF, Section 8). Under H-RF the first K0 evaluations
visit points whose images are, until the first internal coincidence, independent
uniform draws.

**Lemma 1 (birthday).** The probability that the first K0 evaluations contain no
pair with equal image is at most `prod_{j=0}^{K0-1}(1 - j/N) <= exp(-K0(K0-1)/(2N))`.

**Budget value.** K0 = 65300 * 2^112, so

    K0(K0-1)/(2N) >= (K0^2 - K0)/2^257
                   = 65300^2/2^33 - negligible
                   = 4264090000/8589934592 - negligible
                   = 0.496405 - negligible
                   > 0.49430 = -ln(0.61).

Hence the probability of at least one image coincidence within the budget is at
least `1 - exp(-0.49640) = 0.39131 > 0.39`.

**Lemma 2 (a coincidence is converted to a returned collision).** An image
coincidence between two evaluations means two points with equal f-value. From
that common point both predecessors' chains continue deterministically to the
same next distinguished point, so the two chains share a stored DP and RELOCATE
is triggered. To close the boundary case, after the K0-th evaluation any chain
still in progress is run to its next distinguished point (at most L further
evaluations, already inside the per-chain and L-bounded negligible terms of
Section 5), so a coincidence arising near the budget boundary is still resolved
to a shared stored DP before the run concludes. The only ways a coincidence
fails to yield a returned, distinct collision are the bad events below;
subtracting their total probability keeps the bound above 0.39.

**Bad events.** Throughout, the number of chains is at most 2^99 and the number
of stored distinguished points is at most Dcap = 2^98, both deterministic from
Section 5, so no expectation is used as if it were a maximum. (B1) a fresh start
equals an already-visited point: the number of starts is at most the number of
chains < 2^99, and each start hits the at most K0 < 2^128 previously-visited
points with probability at most K0/N <= 2^-128, so the union bound gives at most
2^99 * 2^-128 = 2^-29. (B2) the first coincidence falls within the current chain
(a self-collision giving a cycle rather than a two-chain merge): at most (current
chain length)/N per step, at most L/N each, summed over K0 steps, at most
L*K0/N <= 2^40*2^128/2^256 = 2^-88. (B3) a chain produces L consecutive non-DP
outputs and is abandoned exactly when it would otherwise have produced the
detecting DP: under H-RF the chance a given chain reaches length L is
(1-theta)^L <= exp(-L*theta) = exp(-2^8) < 2^-369, and there are at most 2^99
chains, total < 2^-270. (B4) the record cap Dcap = 2^98 is reached before contact:
the number of distinguished points among K0 evaluations is, under H-RF, a sum of
at most K0 independent indicators each of probability theta, with mean mu =
K0*theta < 2^96; by a multiplicative Chernoff bound the probability it exceeds
Dcap = 2^98 = 4*mu is at most (e^3/4^4)^mu <= exp(-mu) < exp(-2^95), negligible.

Summing, the total bad-event probability is at most 2^-29 + 2^-88 + 2^-270 +
negligible < 2.4e-9. Therefore

    Pr(success) >= 0.39131 - 2.4e-9 > 0.39.

`success_probability = 0.39` is this proven lower bound under H-RF; it is a
property of the fixed algorithm's coins, not confidence in the proof or in any
review. All failed trials, abandoned chains, the RELOCATE walk and the final
verification are charged in Section 5 regardless of outcome.

## 7. Memory, preprocessing, advice

The DP table stores at most Dcap = 2^98 records deterministically (the run halts
if the cap is reached), each a 256-bit DP value, a 256-bit start and a counter
(3 words = 96 bytes < 2^7 bytes), for at most 2^98 * 2^7 = 2^105 bytes of
records. The lookup structure is a binary trie of depth 224; its node count is at
most 224 per stored record (one root-to-leaf path), each node a constant few
words, so trie storage is at most 2^98 * 224 * 2^5 < 2^111 bytes. With 25 lane
registers and a few scalars, peak memory is below 2^112 bytes, so
`memory_log2_bytes = 112`. This is a deterministic worst-case layout derived from
the record cap, not an expectation. Memory is a reported metric only and does not
affect the scalar; nonetheless it is fully charged, and is far below the record
arrays a sort-based birthday would need.

Setup writes a few hundred constant words (code, round constants, the fixed
non-message lanes, counters). This is at most 2^8 ordinary operations, below one
PERM5 unit, and is already inside T, so `preprocessing_log2 = 0`. No favorable
seed, cached collision, lookup table, or target-dependent advice is used:
`nonuniform_advice_log2_bytes = 0` (the schema's conservative encoding of zero
bytes).

## 8. Heuristic H-RF and evidence

**H-RF (role: score-critical; used only for the Section 6 success bound).** An
evaluation of f = H . msg at a point not previously evaluated returns a value
uniform on {0,1}^256, independent of the algorithm's coins and of all previously
observed values. Scope: the at most K0 < 2^128 evaluations of one run on the
fixed five-round SHA3-256 map. Extrapolation: from standard modelling of a
fixed cryptographic permutation's output distribution to the specific
five-round map; no proof of ideal behaviour is claimed. Evidence: the complete
specification of f in Sections 1-2 (`proof:26-110`); the birthday and bad-event
analysis in Section 6 (`proof:176-214`) which depends on H-RF only through
uniform-independent images; and the general cryptographic experience that
round-reduced Keccak output statistics match a random map closely enough that
the generic birthday count is the best known classical collision cost (to our
knowledge no sub-birthday classical ordinary-collision attack on five-round
SHA3-256 is published; the known round-reduced-Keccak collision advances rely on
differential structure for far fewer rounds or are quantum and out of scope).
Limitations: H-RF is a modelling assumption, `plausible` rather than
`established`; a proven bias in the five-round image distribution could raise or
lower the exact success probability, which is why the time bound in Section 5 is
stated independently of H-RF and only the 0.39 figure depends on it. Score
sensitivity: the scalar depends on H-RF only through the budget K0; even a
constant-factor change in the required K0 moves log2(T) by well under one bit and
leaves the result below the 129 display reference.

## 9. Evidence, scope and limitations

This is a generic accounting result, not a new cryptanalytic attack on
reduced-round SHA3-256. The algorithm, target definition, correctness argument
and resource ledger are the supporting evidence; the single heuristic H-RF is
declared above and bounds only the success probability. No full-scale execution,
observed collision pair, certificate or experiment manifest is supplied; the
certificate manifest is valid and empty.

The construction is an astronomically expensive theoretical RAM algorithm, not a
practical attack. `baseline_improved = sha3-256-r5-nominal-v2` is a required
reference identifier and asserts no improvement over an established attack or
security bound. Exploratory qualification (`plausible_not_refuted`) is not
mathematical proof or human acceptance, and scalar improvement is not Pareto
dominance. The same DP accounting applies to any 256-bit-digest target in this
family, differing only in the per-target reference operation cost C and the
hash specification in Section 1.
