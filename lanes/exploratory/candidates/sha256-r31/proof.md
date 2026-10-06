# A distribution-free direct-table collision bound for the fixed-IV 31-round target

This package targets `sha256-r31-exploratory`, profile `sha256-r31-prefix-v1`, under `collision-frontier-v5`. It gives an analytic probabilistic ordinary-collision algorithm with a deterministic work cap. It uses no differential premise, stored witness, random-oracle assumption, or nonuniform advice. The required `baseline_improved` field names the organizer's nominal reference identifier; it does not assert that the nominal reference is an accepted attack or that this score beats an accepted incumbent.

## Exact target and sample space

Set `B=2^128`, `q=4073*2^116=(4073/4096)B`, and `D=2^320`. For each sample draw two **fresh independent uniform 256-bit RAM words** `X,Y`. Let the complete 40-byte message be `BE_32(X)||BE_8(Y mod 2^64)`. These are independent uniform messages over the `D`-element domain. Its FIPS-padded one-block input is the 40 message bytes, byte `80`, fifteen zero bytes and the big-endian 64-bit length `320`. Hash from the standard SHA-256 IV using the original schedule and constants, step indices 0 through 30, and all eight feed-forward additions. Keep and compare the **complete 256-bit digest**. Each sample costs one selected target compression. Returned messages must be distinct complete messages with equal complete target digests.

## Randomized direct table and complete algorithm

Split each digest into three characters of 86, 85 and 85 bits from low to high. Allocate three arrays `T_0,T_1,T_2` of lengths `2^86,2^85,2^85`, respectively, totaling `2^87` 256-bit RAM words. Fill each entry from a fresh independent uniform 256-bit word and retain its low 128 bits. Thus every table value is an independent uniform 128-bit number. Define the 128-bit bucket index

```text
h(d) = T_0[d mod 2^86]
       xor T_1[(d >> 86) mod 2^85]
       xor T_2[d >> 171].
```

All table draws and initialization operations are charged below. The tables are algorithmic random coins, not advice or a short deterministic seed expansion.

Allocate and zero `H[0..B-1]`, a dense array of bucket heads. Zero denotes an empty list. Allocate `M` with two words per source message and `R` with two words per `(complete digest,next-node)` record. Record `i` is addressed by the nonzero chain index `i+1`; `q<B`, so that index fits a 128-bit field. Uninitialized `M/R` slots are written before any read. For each sample, store its complete source message, compute its complete target digest and bucket, and traverse the bucket's existing chain. At each node compare **full digests**, not just bucket indices. At the first equal full digest, compare the two complete source messages. Return FAIL if they are identical. If distinct, independently rehash both from the fixed IV and return them only if their complete digests agree. If the chain ends without equality, insert the new `(digest,next-node)` record at the head; its record index `i` identifies source `M[i]`. If there is no digest equality after `q` samples, return FAIL. There is no restart.

Maintain one global node-inspection counter. Abort with FAIL before an inspection that would exceed the fixed integer cap

```text
L = 2^127 + 2^96 + 2^66.
```

This makes the comparison-work bound deterministic on every coin outcome, including unlucky random tables. The cap is a fixed public parameter derived from `B`, not target-specific advice.

## Bucket-comparison probability for any fixed output distribution

Condition on the complete sampled digest multiset and let `U` be its `n<=q` distinct digest values. The table randomness remains independent. For distinct `x,y` in `U`, `h(x)` and `h(y)` are independent uniform bucket values, so the number `C` of unordered pairs of distinct values in one bucket satisfies

```text
E_T C = binom(n,2)/B < B/2.
```

The three-character tabulation family is three-wise independent: an XOR dependence among one, two or three distinct keys would require every table character to occur an even number of times in each character position; an odd set of three rows cannot have that property. Four-key dependencies are handled explicitly rather than ignored.

Here is an elementary fourth-moment bound. For every character position and value, introduce an independent Rademacher sign `eps_{j,a}`. Let `Z=sum_{x in U} product_{j=0}^2 eps_{j,x_j}`. Then `E Z^4` counts exactly the ordered four-tuples in `U^4` whose character occurrences all have even multiplicity, the same condition for an XOR dependence of four tabulation hashes. For any set `S` of distinct `c`-character keys, induction gives `E Z_S^4 <= 3^c |S|^2`. To see this, slice by the last character and write `Z_S=sum_a eps_{c,a} Z_a`. Conditional fourth-moment expansion gives `E_eps Z_S^4 <= 3(sum_a Z_a^2)^2`; Cauchy-Schwarz and the induction hypothesis give `E Z_a^2 Z_b^2 <= 3^(c-1)|S_a||S_b|`. Summing yields the claim. The zero-character base is immediate. At `c=3`, there are at most `27n^2` dependent ordered four-tuples, for every possible set `U`.

Write `C=sum_e I_e` over unordered distinct-value pairs. Each `Var(I_e)<1/B`. Two edges sharing a vertex have zero covariance by three-wise independence. Two disjoint edges also have zero covariance unless their four incidence vectors XOR to zero; in that exceptional case covariance is at most `1/B`. Every unordered disjoint edge pair has eight ordered four-tuple representations. Thus

```text
Var_T(C) <= E_T C + 27n^2/(4B) < (1/2+27/4)B < 8B.
Pr_T[C > 2^127+2^96 | U] <= 8B/2^192 = 8/2^64.
```

The bound holds conditionally for *every* sampled digest multiset, so it also holds without conditioning. When `C<=2^127+2^96`, every unsuccessful node inspection before the first repeated full digest compares a distinct pair counted in `C`. At that first repeat, if its bucket holds `t` distinct values, `t(t-1)/2<=C< B`, hence `t<2^66`; its final successful chain search adds fewer than `2^66` inspections. The global cap `L` therefore cannot interrupt a first repeated-digest search on this event. The proof does not assume uniform target outputs or typical bucket sizes.

For any fixed map from the `D` possible messages to at most `R=2^256` complete digests, write `p_y` for its output probabilities. The no-repeat probability is `q! e_q(p)`. Pairwise averaging two unequal probabilities raises this elementary symmetric polynomial: terms using both coordinates contain their nonnegative product. Hence the no-repeat probability is maximal for uniform mass on all `R` outputs. The union bound for repeated complete inputs, followed by the independent table-cap bound, gives

```text
Pr[ordinary collision returned]
 >= 1-exp[-q(q-1)/(2R)] - q(q-1)/(2D) - 8/2^64
 > 0.390063564323593001 > 0.39.
```

On the event of no repeated input, any repeated digest gives distinct messages, and the first such digest repeat is found before the cap except on the tabulation-tail event. This is algorithmic probability over fresh sample and table coins with the target held fixed. The declared `success_probability` is the conservative `0.39`; `heuristics` is empty.

## All-outcomes work and memory

One selected target compression costs one unit; each other primitive 256-bit RAM operation costs `1/2140`. Loads, stores, additions, bitwise operations, shifts, comparisons, branches and fresh random-word draws are counted. Every pointer, record index, counter, cap and table address fits one 256-bit word.

The three tables contain `2^87` entries. Filling each takes at most six ordinary operations: random draw, low-128 mask, store, pointer advance, compare and branch. Zeroing the `B` heads takes at most six operations per head, including two operations of margin. The per-sample envelope of 72 ordinary operations includes:

| Work | Operations per sample |
| --- | ---: |
| Two fresh draws, 40-byte message storage, extraction of the ten variable 32-bit block words, fixed padding, packing all eight output words into one digest, compression interface and sample loop | at most 48 |
| Three-character tabulation lookup and bucket-head load | at most 14 |
| Digest/next insertion, head replacement and record control | at most 10 |

The 48-operation sample ceiling has a concrete 44-operation scalar implementation: two random draws; one mask to retain the 64-bit tail; three operations to store the two source words; fourteen shifts/masks to extract eight 32-bit words from the 256-bit prefix and two to extract the 32-bit tail words; fourteen shift/OR operations to pack the eight already-masked feed-forward output words into one full digest; three record-store/address operations; and five pointer/index/loop operations. Four operations remain for the compression interface. The fixed W10 padding word, W11..W14 zero words, W15 length word and IV are compile-time constants; the target compression core itself is charged separately. The record stores happen after a failed bucket search and are conservatively charged again within the ten-operation insertion allowance. The 14-operation hash lookup consists of four shifts/masks to extract the three characters, three table-address additions and three loads, two XORs, and bucket-head address plus load. An inspected node costs at most 16 operations, including chain test, record address and full-digest load/compare, next-pointer load, budget update/test, branches and margin. A single source-message comparison, two independent verification rehashes and final output logic fit a fixed `2^24` ordinary-operation allowance plus two selected target compressions. All `q` sample compressions and the full global inspection cap are charged even if the algorithm stops early. Thus, for **every** coin outcome,

```text
W <= 72q + 16L + 6B + 6*2^87 + 2^24;
T <= q+2+W/2140;
log2(T) = 128.04877013199268057... < 128.049.
```

`M` and `R` use `4q` words, `H` uses `B`, and the tabulation tables use `2^87`. Including `2^24` scratch bytes,

```text
32(4q+B+2^87)+2^24
 = (159.28125000001455...)*2^128 bytes < 2^136 bytes.
```

This is an astronomical theoretical upper bound, not an executed collision search and not an attack on full 64-round SHA-256. The local package check validates schema and certificate consistency; it does not prove the mathematical argument. Exploratory AI screening, human review and promotion are separate outcomes.
