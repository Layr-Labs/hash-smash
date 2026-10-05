# A byte-valid generalized-internal-difference attack on five-round SHA3-256

This dossier gives a classical ordinary-collision algorithm for
`sha3-256-r5-prefix-v1`. Its charged-time bound is below `2^122` target units,
and its claimed algorithmic success probability is 0.5. Five premises are
declared as score-critical heuristics. The finite witnesses below establish
byte alignment, connector nonemptiness, the complete internal characteristic,
and one exact message-modification cluster; they do not turn the large-scale
extrapolations into theorems.

## 1. Exact target and legal messages

Every generated message has exactly 135 bytes. SHA3's delimited suffix and
`pad10*1` make its only absorbed rate block

```text
message || 0x86
```

of length 136 bytes. The capacity part of the initial 1600-bit state is zero.
The algorithm applies Keccak-f[1600] rounds 0, 1, 2, 3, and 4, with the
original round constants, once to that state and returns its first 32 bytes.
Thus each evaluation is the complete selected hash from the standard zero IV,
not a free-start permutation, compression-only relation, bit-string message,
or truncated digest.

Lanes have index `x+5y`; bits and lanes use FIPS 202's little-endian Keccak
encoding. Write `L=pi(rho(theta(.)))`, and let `chi` operate on five-bit rows.
For a state `S`, define its period-32 internal difference

```text
Delta(S) = S xor ROTATE_EACH_64_BIT_LANE_BY_32(S).
```

The lower 32 bits of each lane are the canonical representative; the upper
32 bits repeat them.

## 2. Published foundation and the byte adaptation

Dinur, Dunkelman, and Shamir, *Collision Attacks on up to 5 Rounds of SHA-3
Using Generalized Internal Differentials*, FSE 2013, ePrint 2012/672, describe
a five-round Keccak-256 attack in Sections 7 and B and give Characteristic 4
in Appendix C. Its target internal difference is reached by a one-round target
internal difference algorithm (TIDA). The following characteristic has weights
21 and 16. Its final period-32 internal difference has canonical weight 12.

Section 5.2 aggregates the possible outputs of the next chi with at most twice
that weight, hence 24 binary variables. After the following linear layer, the
first 256 output bits depend on the first complete 320-bit row before the last
chi. For period 32 that row has at most `5*32=160` free bits. Therefore every
message following the characteristic maps into a fixed output subset of size

```text
Q <= 2^(160+24) = 2^184.
```

The paper's Appendix D witness uses the pre-standard Keccak padding convention.
Parsed as its printed little-endian 32-bit words, its final rate byte is `0xcd`.
Reconstructing the associated affine TIDA cell gives rank 1493 and dimension
107, but its permitted final bytes are exactly the 64 values congruent to 1
modulo 4. The benchmark byte `0x86` is inconsistent with that particular cell.
Consequently, the printed witness is not used as a target-valid message.

The adaptation reruns the nonlinear TIDA condition with all 512 capacity bits
zero and the complete last rate byte fixed to `0x86`. It changes values and
right-hand sides, not the target characteristic or the remaining-round subset
bound.

## 3. Exact byte-valid witnesses

For a state sequence, set

```text
X_j = L(S_j)
Y_j = chi(X_j)
alpha_j = Delta(Y_j)
S_(j+1) = Y_j xor RC_j.
```

The following are the lower 32-bit lane words of `alpha_0`, `alpha_1`, and
`alpha_2`, in lane order `x+5y`. Their upper halves are identical.

```text
alpha_0:
bce01edd 68a049ee 4a602999 91603039 68a00d80
bce09e54 68a049ea 4a602999 91603099 6ca00d80
fce09e54 68a049ee 4a202999 91603099 68a00d80
bce09e54 68a049ee 4a602999 91603099 68a00d80
bce09e54 68a049ee 4a602b99 91603099 69a00d80

alpha_1:
0000808a 00004000 00000002 00000000 00000040
00000008 00004000 00000002 00000000 00000040
00000000 00000000 00000000 00000000 00000000
00000000 00000000 00000000 00000000 00000000
00000000 00000000 00000000 00000000 00000000

alpha_2:
00000008 04000000 00000000 00000000 00000000
00000000 04000000 00000000 00000000 00000000
00008000 00000080 00000000 00000000 00000000
00000082 00000080 00000000 00000000 00000000
80000000 00000000 00000000 00000000 00000000
```

The canonical representative of `Delta(L(S_3))` is

```text
80008082 00000040 00000000 00000000 00000000
00000000 00000000 00040000 00100000 00000000
08000000 00000000 00000000 00000000 00020000
00000000 00000000 00020000 00000000 00000000
00000000 00000000 00000000 00010400 00000000
```

and has Hamming weight 12. Direct five-bit DDT evaluation gives full symmetric
weights 42 and 32 for the transitions to `alpha_1` and `alpha_2`; each rotated
row set appears twice, so their internal-characteristic weights are 21 and 16.

An exact Boolean encoding used variables for a legal initial state, every
linear-layer output, each chi product, and each chi output. XORs and
`t = (not a) and b` were encoded by their complete truth-table clauses. The
one-round system had 20,800 variables and 77,320 clauses. A satisfying model
was replayed independently and its fixed-beta affine cell had dimension 101.

A three-round encoding had 59,244 variables and 231,008 clauses. It produced
the following 136-byte absorbed block; the message is its first 135 bytes and
the final `86` is generated by SHA3 padding.

```text
10f685894f1faa5a6cb206aecdf996d908474f48b27cccd04d6b13bcfbedd002
6d73174a1348357555e0622bda789bdc65af1e99bc67ba322d176296ef555b5c
6edc624ed0f934ce703418bb4d2a941b8bcbceb7985755af02fe8ec0e018c664
77b7dccab03c73f887a5b68ecf4163ee2b439964cb6258cbf9f529439acbdf87
0d253364d60dcf86
```

Starting from this block followed by 64 zero bytes, direct Keccak evaluation
reproduces all three arrays above, transition weights 21 and 16, and the final
canonical weight 12. The complete five-round digest is
`748f09517d076de93fc1ecc2bfe1aeca28493dff2d215646e01bda84e61ffb65`.
This is a characteristic witness, not a collision pair.

## 4. Exact byte-valid message modification

For a fixed first-round input difference `beta_0=Delta(L(M))`, the equations

```text
Delta(X_0) = beta_0
Delta(chi(X_0)) = alpha_0
M = L^-1(X_0), with zero capacity and final byte 0x86
```

are affine in `X_0`: every fixed chi differential value set is affine. A
two-round satisfying block was found in a rank-1501, dimension-99 cell:

```text
7d23b2690a626dab8ec593232d84db8eb5d3798e338e793e81b5d29e1c3a2ed0
cd4cc070de03855194d5b95502a0e00b458c2412df326e87c43dd439c4fb63fa
23d5d41c6ddbc01c39a4cc9f2eaa8765991105b1886c3abeca774b5e41955803
521a2bdd5f31e40d2f787c4ee8eefb8ea0019250d6e0595a3ab9774f40ab5765
8c9cd09017e81c86
```

A low-Hamming-weight symmetric even-parity (LHSE) direction identified by
`(x,y_1,y_2,z)` toggles exactly

```text
A[x,y_1,z], A[x,y_1,z+32], A[x,y_2,z], A[x,y_2,z+32].
```

The cell contains 66 of the 1,600 possible LHSE directions and 55 are linearly
independent. At the displayed base, the following 14 independent directions
preserve both `alpha_0` and `alpha_1`:

```text
(0,1,2,13) (1,1,3,3)  (1,1,2,6)  (1,0,1,8)
(1,0,2,18) (2,0,1,12) (2,0,2,19) (2,0,2,20)
(2,0,2,21) (3,0,2,0)  (3,0,2,22) (3,0,2,23)
(4,1,2,4)  (4,0,2,23)
```

All `2^14=16,384` XOR combinations were exhaustively evaluated. They are
distinct legal 135-byte messages; all retain the final padded byte `0x86`, zero
capacity, and the target internal differences through rounds 0 and 1. This is
an exact instance of the paper's message-modification gain in the byte-valid
regime. It establishes neither the frequency of such cells nor independence of
different clusters.

## 5. Fixed-budget collision algorithm

### Preprocessing

The characteristic generator is a finite SAT enumeration, not an invocation of
an unspecified trail oracle. It represents every period-32 internal difference
by 800 canonical bits. Linear-layer and iota relations are XOR clauses. For each
five-bit rotated-row transition, a 10-input truth-table block forbids every
`(delta_in,delta_out)` pair with zero DDT entry and attaches the integer weight
`5-log2(DDT)` to each permitted pair. Binary adder networks constrain the two
successive weight sums to at most 21 and 16 and the last representative's
Hamming weight to at most 12. A model is extended symbolically through the next
chi and linear layer; Gaussian elimination rejects it unless the first-320-bit
variable-allocation rank is at most 24. The canonical 800-bit model is blocked
after rejection so that the same characteristic is not returned twice.

The legal-cell generator uses the same explicit clause templates. Its variables
are the 1,600 initial-state bits, linear-layer outputs, chi products, and chi
outputs. It fixes capacity to zero and the last rate byte to `0x86`, encodes
`X=L(M)` by XOR chains, encodes each chi bit as
`y_x=x_x xor ((not x_(x+1)) and x_(x+2))`, and equates
`Delta(chi(X))` to the candidate characteristic's target. A model determines
`beta_0=Delta(X)`. Fixing that beta turns every local DDT value set into affine
equations; row reduction gives the cell dimension and canonical basis. A single
clause over the 800 linear beta expressions blocks that beta before the next
attempt.

The complete preprocessing algorithm is:

1. Enumerate characteristic models as above. For each model, verify its DDT
   transitions, weights, final representative, and projected rank directly.
2. For that model, enumerate legal-cell models. Retain a cell only when its
   beta is new, its affine dimension is at least 99, and direct equation replay
   verifies its base and basis. Cells for an abandoned characteristic are
   discarded and are never mixed with another characteristic's subset.
3. Stop successfully at `K=2^24` retained cells. Across all characteristic
   models, run at most `2^26` cell attempts, each stopped after `2^48` ordinary
   operations. Stop the aggregate characteristic enumeration after `2^100`
   ordinary operations. If either cap is reached first, halt with failure.
4. For each retained cell, enumerate all 1,600 LHSE directions, retain its
   independent in-cell directions, and store the cell base, first 99 canonical
   basis vectors, beta, and LHSE list.

The concrete CNF procedure is the fixed CDCL schedule of Kissat 4.0.4,
commit `8af8e56f174b778aef3aa45af9f739b2a5f492c2`. Attempt `i` takes one fresh
256-bit random word as its solver seed; all options and the clause order above
remain fixed. Watched-literal propagation, conflict analysis, learning,
backtracking, restarts, and database reduction are charged one operation for
every load, store, bitwise operation, comparison, branch, or random word, even
when the implementation uses a narrower host word. Its wrapper stops at the
per-attempt cap. Every returned model is checked by the independent DDT,
affine, and Keccak equations, so solver soundness is not assumed. All other
loops use the same explicit counters. Published or stored states are never
accepted in place of this construction.

### Online phase

The first 99 coordinates of every retained cell give exactly `2^99` messages.
Different cells have different `beta_0`, hence are disjoint. Their union is a
domain of exactly `N=2^123` legal messages, indexed by a 24-bit cell number and
a 99-bit affine coordinate.

1. Use Floyd sampling with fresh uniform 256-bit words to select
   `B=2^119` distinct indices from this domain. A draw in `[0,j]`, where
   `j>=N-B`, masks to 123 bits and rejects values above `j`. Cap each draw at
   64 attempts and fail if the cap is reached. Since rejection is at most
   `1/16`, the union bound on this failure is at most `2^119*16^-64=2^-137`.
2. Materialize and completely evaluate each selected message once. Retain at
   most `F=2^98` bases which reach `alpha_1`. For each retained base, test at
   most 64 independent in-cell LHSE directions, choose 13 which preserve
   `alpha_1`, and enumerate their span in Gray-code order. Skip a base if fewer
   than 13 exist.
3. Use a direct-address bitset on the `2^123` canonical message indices to
   discard repeats from overlapping clusters and the base sample. Completely
   evaluate at most `G=2^111` new cluster messages. Retain only messages which
   also reach `alpha_2`, stopping successfully when `S=2^93` distinct survivors
   have been stored. If any cap is reached first, halt with failure.
4. Stable-radix-sort survivor records by all 256 digest bits. Scan equal-digest
   runs, reconstruct two messages with different canonical indices, recompute
   both complete hashes from zero, and return them only if all 256 bits agree.
   Otherwise halt with failure.

Every returned pair is distinct and lies in the target's byte domain. Full
digest equality after the defensive replay is exactly an ordinary collision.

## 6. Success probability and five heuristic premises

The algorithm's probability space is its fresh solver choices, Floyd samples,
and random words, for this fixed target. Epistemic confidence in a premise is
not part of the success probability.

`H1-cell-abundance` is a fixed structural premise: at least `2^24` distinct
byte-valid TIDA cells of dimension at least 99 exist for the selected target
difference. Conditional on the premise it contributes factor 1, not a random
success event. The paper reports hundreds of old-padding TIDA trials, all
succeeding in under 30 seconds with dimensions 78--111, and argues that the
target has 286 difference degrees of freedom. The byte-valid evidence above
contains cells of dimensions 101 and 99. Extrapolation to `2^24` cells is not
measured.

`H2-message-modification-supply` states that, conditional on the retained cell
table, the base sample and bounded cluster procedure produce at least `2^110`
distinct messages reaching `alpha_1` with probability at least 0.9. This allows
one bit of slack on the rank-21 base frequency and one bit on the exact
`2^14` cluster. The paper sampled about `2^30` messages in each of hundreds of
TIDA subspaces and typically found about `2^23` reaching the target, an
amortized `2^7` cost and `2^14` gain. Section 4 supplies one exact byte-valid
`2^14` cluster. Dependence, overlap, and favorable-cell selection at scale remain
unproved.

`H3-remaining-transition-supply` states that the bounded cluster output leaves
at least `S=2^93` distinct messages after the weight-16 transition with
probability at least 0.9. This allows a one-bit loss relative to `2^-16` from
`2^110` inputs. The exact three-round witness proves nonemptiness and the local
DDT calculation proves the nominal weight; neither proves the selected-cluster
frequency.

`H4-subset-birthday` states that the complete digest map on the retained
survivors collides no less often than independent uniform mapping into a set of
size `Q=2^184`. With `S=2^93`, its collision probability is at least

```text
1 - exp(-S(S-1)/(2Q))
  = 1 - exp(-(2 - 2^-92))
  > 0.864.
```

The deterministic subset-size bound does not imply this random-map behavior.
This is the squeeze-attack premise used by the source construction.

`H5-bounded-construction-success` states that the characteristic and required
cell table are found within the preprocessing caps with probability at least
0.9. The paper's repeated TIDA runs and the three finite byte-valid SAT models
support feasibility, but do not establish a tail for `2^24` retained cells or
for the characteristic enumeration. Solver wall time is not used as a cost
conversion.

Conditional on the fixed H1 premise, no independence between the three 0.9
events is needed. The union bound gives total success above

```text
(1-exp(-(2-2^-92))) - 3*(1-0.9) > 0.564.
```

Subtracting the Floyd rejection bound remains above 0.564. The dossier claims
0.5, exceeding the required 0.39. This is an algorithmic success probability
conditional on the five disclosed heuristics, not a confidence score.

## 7. Charged computation

One selected five-round permutation costs one target unit. Every other listed
256-bit RAM primitive costs `1/1355` unit. The following caps include failed
trials, restarts, code and table initialization, randomness, addressing,
branches, loads/stores, message construction, deduplication, sorting, and final
checks.

Preprocessing uses at most `2^30` target calls. Its ordinary work is bounded by

```text
trail enumeration                         <= 2^100
2^26 capped cell attempts at 2^48 each    <= 2^74
cell reduction, verification and storage  <= 2^50
```

Therefore

```text
P <= 2^30 + (2^100 + 2^74 + 2^50)/1355 < 2^90 target units.
```

For each of the `B=2^119` base probes, 8,192 ordinary operations cover: up to
64 rejection attempts at fewer than eight operations each; direct-bitset
lookup/update; decoding the cell and coordinate; XORing at most 99 five-word
basis vectors with all memory traffic and loop control; wrapper construction;
intermediate comparisons; digest retention; and counters. Hence this phase uses
at most `2^132` ordinary operations.

At most `G=2^111` cluster messages use fewer than 4,096 ordinary operations
each, or `2^123`. Initializing the `2^123`-bit visited table, preparing cells,
testing up to 64 LHSE directions for at most `F=2^98` bases, survivor record
traffic, radix sorting, scanning, reconstruction, and final checks together use
less than `2^124` further ordinary operations. Thus

```text
W_online < 2^132 + 2^124.
```

Complete target calls are bounded separately:

```text
H_online <= 2^119 + 2^111 + 64*2^98 + 2.
```

The first term evaluates every base even when an early condition fails; no
early-abort saving is needed. The second evaluates every new cluster message;
the third conservatively prices each LHSE test as a complete target call.

Combining every phase,

```text
T = P + H_online + W_online/1355
  < 2^90 + (2^119 + 2^111 + 2^104 + 2)
           + (2^132 + 2^124)/1355
  < 2^121.823
  < 2^122.
```

The claim is `time_log2=122` and `preprocessing_log2=90`. These are fixed
worst-case caps on every halting branch. A failed search consumes no more than
the same bounds.

## 8. Memory and advice

The direct visited table has `2^123` bits, exactly `2^120` bytes. Two arrays of
at most `2^93` survivor records, each below 128 bytes, use at most `2^101`
bytes. The `2^24` cell records, each containing one base, 99 five-word vectors,
the internal difference, and LHSE metadata, use less than `2^40` bytes. Code,
constants, radix counters, SAT workspace, current states, randomness, and output
fit in another `2^40` bytes. The lifetime schedule reuses cluster and sorting
buffers, so peak memory is below `2^121` bytes.

At most `2^16` bytes of nonuniform advice hold the characteristic-search
parameters, canonical finite witnesses, and fixed generator settings. The
characteristic and cells are still regenerated and charged in preprocessing;
the advice is not a stored collision or a free connector table. No external
oracle data is used.

## 9. Evidence boundary

The finite checks establish the exact target wrapper, byte-valid connector
nonemptiness, affine-cell dimensions, characteristic transitions, final
canonical weight, and one complete `2^14` message-modification span. The paper
supplies the generalized-internal-difference construction, subset-size proof,
and old-padding simulations. No full-scale `2^119` search or actual collision
pair has been executed.

No organizer experiment is declared. The two padded blocks, complete internal
difference arrays, and 14 direction coordinates above are finite mathematical
witnesses included for direct replay; reported SAT sizes and exhaustive counts
are participant evidence, not trusted runtime or statistical measurements.

The score depends on all five heuristics in Section 6. H1 and H5 extrapolate
cell and characteristic construction; H2 extrapolates cluster supply and
overlap; H3 extrapolates the remaining transition; H4 extrapolates fixed-map
birthday behavior. Failure of any premise invalidates the claimed success or
resource result. This is why the claim belongs only in the exploratory lane.

## 10. References

- Itai Dinur, Orr Dunkelman, and Adi Shamir, *Collision Attacks on up to 5
  Rounds of SHA-3 Using Generalized Internal Differentials*, FSE 2013,
  LNCS 8424, pp. 219--240, ePrint 2012/672,
  DOI `10.1007/978-3-662-43933-3_12`.
- NIST, *SHA-3 Standard: Permutation-Based Hash and Extendable-Output
  Functions*, FIPS 202, 2015, DOI `10.6028/NIST.FIPS.202`.
