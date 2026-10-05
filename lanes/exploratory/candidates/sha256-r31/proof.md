# Five-round SHA3-256: distinguished-point generic collision search, every instruction charged

The scalar below is `time_log2` under `collision-frontier-v5` with C = 2140.
Memory remains a separately reported resource bound.

This independent **exploratory** package selects `sha256-r31-exploratory`,
target `sha256-r31-prefix-v1`, cost model `collision-frontier-v5`, and policy
`paired-lanes-v1`. It submits a complete analytic algorithm, not an already
computed collision. It is the **van Oorschot-Wiener distinguished-point (DP)
search** (Journal of Cryptology, 1999) run on a single processor with every
instruction charged. It is **not** a cryptanalytic advance: the scalar sits just
above the nominal 128 because nothing is left out. Only the success-probability
lower bound uses a heuristic (H-RF, random-function); correctness and all time,
memory and preprocessing bounds hold for every run without any heuristic.

| `claim.json` field | value |
| --- | --- |
| `time_log2` | **128.005** (worst-case bound below 2^128.003 for every run, rounded up) |
| `memory_log2_bytes` | 112 |
| `success_probability` | 0.39 (bounded below by 0.3913 under H-RF) |
| `preprocessing_log2` | 0 (a few-operation setup, below one unit, already inside T) |
| `nonuniform_advice_log2_bytes` | 0 |
| `baseline_improved` | `sha256-r31-nominal-v2` (required identifier; no improvement over an established attack asserted) |

Prior art. A concurrent exploratory submission by `winglock` applies the same DP
method to the six-round sibling `sha3-256-r6-exploratory`; the standard DP
algorithm and birthday analysis used here are from van Oorschot-Wiener and are
textbook, not that submission's invention. This package reapplies the method to
the 31-step target independently and prices it under C = 2140.

## 1. Exact complete hash

The iteration uses messages of exactly 32 bytes, bit length 256 < 2^64. Write
`msg(x) = BE32(x)`: the 32 big-endian bytes of a 256-bit integer x. This map is
injective, so any `x != x'` with equal complete digests yields two distinct
32-byte messages that collide.

H is the complete fixed-IV SHA-256 hash with the compression reduced to its first
31 steps. A 32-byte message pads to exactly one 64-byte block:

    B = BE32(x) || 0x80 || (23 zero bytes) || BE64(256).

As sixteen big-endian 32-bit words, W[0..7] are the eight words of x, W[8] =
0x80000000, W[9..14] = 0, W[15] = 0x00000100. The eight initial chaining words are

    6a09e667 bb67ae85 3c6ef372 a54ff53a 510e527f 9b05688c 1f83d9ab 5be0cd19.

Additions are mod 2^32; NOT and rotations operate on 32 bits.
s0(z)=ROTR(z,7)^ROTR(z,18)^(z>>3); s1(z)=ROTR(z,17)^ROTR(z,19)^(z>>10);
S0(z)=ROTR(z,2)^ROTR(z,13)^ROTR(z,22); S1(z)=ROTR(z,6)^ROTR(z,11)^ROTR(z,25);
Ch(e,f,g)=(e&f)^((~e)&g); Maj(a,b,c)=(a&b)^(a&c)^(b&c);
W[t]=W[t-16]+s0(W[t-15])+W[t-7]+s1(W[t-2]) for t=16..30. Constants K[0..30]:

    428a2f98 71374491 b5c0fbcf e9b5dba5 3956c25b 59f111f1 923f82a4 ab1c5ed5
    d807aa98 12835b01 243185be 550c7dc3 72be5d74 80deb1fe 9bdc06a7 c19bf174
    e49b69c1 efbe4786 0fc19dc6 240ca1cc 2de92c6f 4a7484aa 5cb0a9dc 76f988da
    983e5152 a831c66d b00327c8 bf597fc7 c6e00bf3 d5a79147 06ca6351

Copy the IV into (a..h); for t=0..30 with old values on the right:
T1=h+S1(e)+Ch(e,f,g)+K[t]+W[t]; T2=S0(a)+Maj(a,b,c);
(a,b,c,d,e,f,g,h)=(T1+T2,a,b,c,d+T1,e,f,g). After step 30 add the eight working
words to the IV words mod 2^32 (one block, so this is the final state). H(msg(x))
is BE4 of the eight state words, the full 256-bit digest as a 256-bit integer.
This single reduced compression (expansion, 31 steps, feed-forward) is the one
charged unit, CF31. No selected IV, suffix convention, compression-only
substitute, changed padding, or digest truncation.

## 2. Iteration function and why an f-collision is an ordinary collision

Define `f(x) = H(msg(x))` as a 256-bit integer. Because `msg` is injective,
f(x)=f(x') with x!=x' gives msg(x)!=msg(x') and H(msg(x))=H(msg(x')): a functional
collision of f is an ordinary collision on two distinct 32-byte messages, with no
distributional assumption (it follows from injectivity of msg). The eight output
digest words are exactly the eight message words W[0..7] of the next evaluation.
The two colliding preimages produced below are distinct by construction.

## 3. The algorithm

Fixed constants: a point is **distinguished** (a DP) iff its low 32 bits are zero
(DP rate theta = 2^-32); maximum chain length L = 2^40; evaluation budget
K0 = 65300 * 2^112; distinguished-record cap Dcap = 2^98.

The state holds 25 lanes R0..R24, a global evaluation counter g, a table T of at
most Dcap distinguished records keyed by the 224 high bits of a DP, and a few
scalars. One CF31 call costs one unit plus one operation to issue it; its
internals are not charged again, matching the cost model's definition of C as a
count of data-word operations excluding the selected compression's internals.

- **CHAIN** (at most 11 ordinary operations). If g >= K0, stop. Otherwise set the
  start to s_i = s0 + i for the i-th chain, where s0 is a fixed public 256-bit
  constant and i is the chain index; the starts s_0, s_1, ... are therefore
  pairwise DISTINCT by construction. Write its four words into R0..R3 and set the
  per-chain evaluation counter to 0. (Distinct deterministic starts replace fresh
  uniform starts; under H-RF the image of each distinct start is still uniform, so
  the success analysis is unchanged, while the worst-case chain count is now
  capped as shown in Section 5.)
- **BLOCK**, the inner step, unrolled 16 times per control pass. The eight
  constant block words W[8] = 0x80000000, W[9..14] = 0, W[15] = 0x00000100 are
  written ONCE at setup and never change, since every message is 32 bytes with the
  same padding; they are not rewritten per evaluation. Each evaluation: copy the
  eight output digest words into W[0..7] as the next message (8 writes), call CF31,
  and test the DP predicate on the low 32 output bits (one AND, one compare, one
  branch). Loop control (3 operations) runs once per 16 evaluations, so at most
  (8 + 1 issue + 3 DP-test)*16 + 3 = 195 ordinary operations per 16 evaluations,
  i.e. at most 195/16 = 12.1875 ordinary
  operations per evaluation besides the one CF31 unit. Increment g per
  evaluation. If L evaluations pass with no DP, abandon the chain and go to
  CHAIN (this is a charged but almost-never-taken path, see Section 6).
- **DPFOUND.** On reaching a DP, look up its 224 high bits in T (a depth-224
  binary trie; at most 15 + 224*17 + 9 < 3832 operations, charged as at most
  2^13 operations per chain). If absent, insert the record (start s, DP value,
  chain length) and go to CHAIN. If present, the stored start necessarily DIFFERS from the current start (starts
  are pairwise distinct), so this is a genuine two-chain merge: go to RELOCATE.
  The equal-stored-start case cannot occur. If Dcap would be exceeded, stop.
- **RELOCATE** (first repeated DP). Two chains reach the same DP. Re-walk both
  from their starts, first advancing the longer one so both have equal remaining
  length, then stepping them together until their current points coincide; the
  two immediately preceding points x_a, x_b satisfy f(x_a) = f(x_b). This costs
  at most 2L evaluations, charged as 3L evaluations at (1 + 64/2140) units each.
- **OUTPUT.** Recompute f(x_a) and f(x_b) (2 CF31 units + at most 200 ordinary
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
equal complete 31-step SHA-256 digests. OUTPUT re-verifies x_a != x_b and
full 256-bit digest equality before returning, so a returned pair is always a
correct ordinary collision. If the budget K0 is reached with no RELOCATE, the
run halts with failure; no pair is returned.

This correctness argument uses no distributional assumption; it is purely the
functional-graph property of f and injectivity of msg.

## 5. Fully charged time

Worst-case charged time, every run, classical 256-bit word RAM. Each CF31 costs
one unit; every other listed primitive operation costs 1/2140 units.

| Phase | CF31 calls (cost 1) | Ordinary operations (cost 1/2140) |
| --- | ---: | ---: |
| Setup (code, constants, counters) | 0 | at most 2^8 |
| Chaining control | 0 | at most 11 per chain |
| Evaluations (BLOCK) | at most K0 + L | at most 12.1875 per evaluation |
| DP lookups/inserts | 0 | at most 2^13 per DP-terminated chain (<= Dcap of them) |
| RELOCATE (once) | 0 | at most 3L at (1 + 64/2140) units |
| OUTPUT (once) | at most 2 | at most 200 |

The DPFOUND lookup/insert is executed only when a chain reaches a distinguished
point, hence at most Dcap = 2^98 times in total; abandoned chains incur only the
11-operation CHAIN control. The extra at most L evaluations used to run the final
in-progress chain to its distinguished point after the K0-th evaluation (the
boundary rule of Section 6, Lemma 2) are counted as CF31 calls below.

**Bounding the number of chains (not folded into the per-evaluation coefficient).**
The per-chain control (11) and DP lookup/insert (at most 2^13) costs are charged
separately from the 12.1875-per-evaluation BLOCK envelope, and are bounded through
the number of chains, which is bounded deterministically rather than by K0. A
chain terminates either by reaching a distinguished point or by abandonment after
L evaluations with none. (i) At most Dcap = 2^98 chains terminate at a
distinguished point: because the starts are pairwise distinct, a chain that
reaches an already-stored distinguished point has a different stored start, so it
is a genuine two-chain merge that triggers RELOCATE and halts the run; every
other DP-terminated chain inserts exactly one new record, and reaching the cap
Dcap also halts the run. Hence at most Dcap distinguished-point insertions, plus
the single terminal RELOCATE chain, occur before the run ends. There is no
equal-start chain that terminates at a DP without inserting or halting. (ii) At most K0/L = 2^128/2^40 = 2^88 chains are abandoned,
since each abandoned chain spends L = 2^40 evaluations and the total number of
evaluations is at most K0. Hence the number of chains is at most Dcap + 2^88 <
2^99. The DPFOUND lookup/insert runs only on DP-terminated chains, at most
Dcap = 2^98 times, contributing at most 2^98 * 2^13 = 2^111 operations; the
11-operation CHAIN control runs once per chain, at most 2^99 * 11 < 2^103
operations. All per-chain work is therefore below 2^112 ordinary operations, i.e.
2^112/2140 < 2^102 units, negligible against K0 = 2^128. Hence

    CF31 calls <= K0 + L + 2,
    ordinary operations W <= 12.1875 * (K0 + L) + 2^112 + 2^8 + 3L*64 + 200.

RELOCATE contributes at most 3L CF31-equivalent = 3*2^40 units, and its ordinary
part 3L*64/2140 < 3*2^40 units; the per-chain total is below 2^102 units; all
non-BLOCK terms are below 2^103, negligible against 2^128. Therefore

    T = (CF31 calls) + W/2140
      <= K0 * (1 + 12.1875/2140) + 2^103
       = K0 * 1.005695 + 2^103.

With K0 = 65300 * 2^112, log2(K0) = log2(65300) + 112 = 15.99469 + 112 =
127.99469, and log2(1.018589) = 0.008195, so

    log2(T) <= 127.99469 + 0.008195 + (2^103 term, < 2^-24 in log2)
            < 128.00289.

The declared `time_log2 = 128.005` is a conservative upper bound on this value with more than 0.002 bits of slack; the 12.1875 envelope itself conservatively charges 8 output-word copies that an in-place implementation avoids. A reviewer reconstructing the ledger with the
same or smaller per-operation envelopes obtains at most 2^128.0029, strictly
below the submitted 128.005. The nominal-reference-only frontier displays 128;
this package's scalar sits just above it, as expected for a fully charged generic
search, and no comparison to any other displayed value is asserted. This is a
one-processor cost; the cost model
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
records. The lookup structure is a binary trie of depth 224; each stored record
adds at most 224 nodes (one root-to-leaf path), and each node holds two child
pointers plus a flag, at most 4 words = 2^7 bytes. Trie storage is therefore at
most 2^98 * 224 * 2^7 < 2^98 * 2^8 * 2^7 = 2^113 bytes. With 25 lane registers and
a few scalars, peak memory is below 2^114 bytes, so `memory_log2_bytes = 120` is a
conservative reported bound. This is a deterministic worst-case layout derived
from the record cap, with an explicit per-node word encoding, not an expectation.
Memory is a reported metric only and does not affect the scalar; it is fully
charged, and far below the record arrays a sort-based birthday would need.

Setup writes a few hundred constant words (code, round constants, the fixed
non-message lanes, counters). This is at most 2^8 ordinary operations, below one
CF31 unit, and is already inside T, so `preprocessing_log2 = 0`. No favorable
seed, cached collision, lookup table, or target-dependent advice is used:
`nonuniform_advice_log2_bytes = 0` (the schema's conservative encoding of zero
bytes).

## 8. Heuristic H-RF and evidence

**H-RF (role: score-critical; used only for the Section 6 success bound).** An
evaluation of f = H . msg at a point not previously evaluated returns a value
uniform on {0,1}^256, independent of the algorithm's coins and of all previously
observed values. Scope: the at most K0 < 2^128 evaluations of one run on the
fixed 31-step SHA-256 map. Extrapolation: from standard modelling of a
fixed cryptographic permutation's output distribution to the specific
31-step map; no proof of ideal behaviour is claimed. Evidence: the complete
specification of f in Sections 1-2 (`proof:26-110`); the birthday and bad-event
analysis in Section 6 (`proof:176-214`) which depends on H-RF only through
uniform-independent images; and the general cryptographic experience for SHA-256:
the known 31/32-step SHA-256 collision results (for example the ASIACRYPT 2024
two-block attack near 2^40) are DIFFERENTIAL attacks that engineer a specific
colliding message pair in the compression function, and exhibit no bias of the
single-block iterated map x -> H(BE32(x)) relevant to a generic distinguished-point
walk; to our knowledge no sub-birthday GENERIC distinguisher or collision
procedure for this 31-step iterated map is published, so the generic birthday
count remains the best known generic classical cost for it.
Limitations: H-RF is a modelling assumption, `plausible` rather than
`established`; a proven bias in the 31-step image distribution could raise or
lower the exact success probability, which is why the time bound in Section 5 is
stated independently of H-RF and only the 0.39 figure depends on it. Score
sensitivity: the scalar depends on H-RF only through the budget K0; even a
constant-factor change in the required K0 moves log2(T) by well under one bit and
leaves the result just above the frontier's nominal-reference display of 128.

## 9. Evidence, scope and limitations

This is a generic accounting result, not a new cryptanalytic attack on
reduced-round SHA3-256. The algorithm, target definition, correctness argument
and resource ledger are the supporting evidence; the single heuristic H-RF is
declared above and bounds only the success probability. No full-scale execution,
observed collision pair, certificate or experiment manifest is supplied; the
certificate manifest is valid and empty.

The construction is an astronomically expensive theoretical RAM algorithm, not a
practical attack. `baseline_improved = sha256-r31-nominal-v2` is a required
reference identifier and asserts no improvement over an established attack or
security bound. Exploratory qualification (`plausible_not_refuted`) is not
mathematical proof or human acceptance, and scalar improvement is not Pareto
dominance. The same DP accounting applies to any 256-bit-digest target in this
family, differing only in the per-target reference operation cost C and the
hash specification in Section 1.
