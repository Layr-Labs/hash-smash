# Distribution-free one-block birthday collision for SHA-256-r31

## Target and scope

This candidate searches for an **ordinary collision of two distinct complete messages** under `sha256-r31-prefix-v1`. The target starts each message at the standard SHA-256 IV, uses the original message schedule and round constants, executes round indices 0 through 30 inclusive on each padded block, adds all eight input chaining words as feed-forward, and compares all 256 output bits. We use 40-byte messages. Their standard FIPS padding fits in one 64-byte block: the 40 data bytes, `80`, fifteen zero bytes, and the 64-bit big-endian length `0000000000000140` (320 bits). Thus one message hash costs exactly one selected-round target compression. This attack changes message length within the permitted domain; it does not change the hash target.

This is a theoretical 256-bit word-RAM construction. Its enormous memory requirement is stated and charged below. It uses no differential characteristic, chosen IV, partial digest, precomputed collision, or heuristic output-distribution assumption.

## Fixed algorithm

Let `q=2^128`. Allocate an uninitialized message array `M` of `2q` 256-bit words, two uninitialized record arrays `R,Rnext` of `2q` words each, and a counter array `C` of `2^64` words. Array reservation is not a scan or zero initialization; every word read is written first. The counter array is explicitly zeroed in every radix pass.

For each index `i` from zero through `q-1`, draw **two fresh independent uniform 256-bit words** `u_i,v_i`. Form the 40-byte message `BE_32(u_i) || BE_8(v_i mod 2^64)`. Store `u_i` and its 64-bit tail in `M[2i],M[2i+1]`. Compute its complete fixed-IV 31-step digest `d_i`, and store `(d_i,i)` in the two-word record `R[2i],R[2i+1]`. The two draws make every message uniform over the `D=2^320` possible 40-byte strings; draws at different indices are independent. The algorithm performs exactly `q` message hashes even if an earlier pair could have matched.

Sort records by the entire 256-bit digest using four **stable least-significant-limb-first** counting passes, for limb positions `0..63`, `64..127`, `128..191`, `192..255`. Each pass executes the following bounded loops:

1. Store zero in every `C[b]`, `0<=b<2^64`.
2. Scan all `q` records in current order. Extract the selected 64-bit digest limb `b` and increment `C[b]` once.
3. Sweep all `2^64` buckets in ascending order with a running record count `s`. Replace `C[b]` by the starting **word offset** `2s`, then add the old bucket count to `s`.
4. Scan all `q` records in current order. At `pos=C[b]`, store both record words to `Rnext[pos],Rnext[pos+1]`, then increase `C[b]` by two. Swap the input and output array roles after the pass.

Counter and cursor values are below `2q`; stable scattering preserves the order from prior passes. Four passes therefore order every record by its full digest. The arrays need no comparison sort and no random hash-table premise.

Scan adjacent records in the final sorted array. When two neighboring records have equal digests, compare their stored message words in `M`; duplicate inputs are skipped. On the first equal-digest pair with different 40-byte messages, recompute both complete hashes from those message words and return the pair if their full 256-bit digests agree; otherwise return `FAIL`. In the stated exact-computation model the verification always agrees with the stored digests, so there are at most two rehashes. Every digest group containing two different messages has at least one adjacent boundary between different messages, so the scan finds an ordinary collision whenever one exists among the samples. A failure without such a pair scans all `q` records. There are no retries or restarts.

## Success probability for every fixed target mapping

Let `p_y` be the probability of digest `y` under a uniform 40-byte message. The target is fixed; `p` need not be close to uniform. With `R=2^256` possible digests, the probability that all `q` sampled digests differ is `q! e_q(p)`, where `e_q` is the elementary symmetric polynomial. Holding every other coordinate fixed, averaging any two unequal coordinates of `p` keeps their sum and raises their product, and cannot decrease `e_q`. Repeating this pairwise averaging shows that `e_q` is maximized when all `R` probabilities are `1/R` (zero-probability outputs can be included). Therefore

```text
Pr[all digests differ] <= (R)_q/R^q
                       <= exp[-q(q-1)/(2R)]
                       = exp[-(1/2-2^-129)].
```

A repeated **input** is not an ordinary collision. By a union bound its probability is at most `q(q-1)/(2D) < 2^-65`. Subtracting this possible false event, irrespective of dependence, gives

```text
Pr[at least one equal-digest, distinct-message pair]
  >= 1 - exp[-(1/2-2^-129)] - 2^-65
  > 0.3934 > 0.39.
```

The sorting and scan are deterministic and exhaustive after the `q` independent input draws. The success bound is distribution-free for the actual fixed-IV SHA-256-r31 target; it does not model its outputs as independent uniform random strings.

## Charged work and memory

Under `collision-frontier-v5`, one selected-round target compression costs one unit and every other 256-bit word-RAM primitive costs `1/2140` units. A load, store, addition, shift, mask, comparison, conditional branch, or independent 256-bit random draw counts as one primitive. Control flow and addressing are included; a compression's internals are not charged twice. Maintain 256-bit pointers to the next two-word records, so no per-record multiplication is required. Extracting a 64-bit limb costs one shift and one mask.

The following are conservative **worst-case** operation ceilings for every coin outcome:

| Phase | Target compressions | Other 256-bit word primitives |
| --- | ---: | ---: |
| Fixed setup, final output and checks | at most 2 rehashes | at most `2^24` |
| Draw, form, hash and store `q` messages | `q` | at most `32q` |
| Four complete stable radix passes | 0 | at most `4(12+20)q + 2^74` |
| Full adjacent scan, including message comparisons | 0 | at most `32q` |

The 32-operation input cap covers two draws, tail masking, padding shifts/ORs, four data/record stores, pointer and index increments, loop comparison and branch, and call interface. Each pass's 12-operation histogram cap covers digest load, limb shift/mask, counter address/load/add/store, record-pointer increment, comparison and branch. Its 20-operation scatter cap covers two record loads, limb shift/mask, counter and output address arithmetic, cursor load/add/store, two record stores, pointer increment, comparison and branch; an explicit straight-line implementation uses no more than 16, leaving four for addressing details. The 32-operation final-scan cap includes all worst-case digest and message loads/comparisons, index-to-message addressing, pointer increments and branches, even when adjacent digests are equal throughout. The bucket allowance is generous: across four passes, zeroing and prefix sweeps each use at most 64 primitives per bucket, so their total is `4*2*64*2^64=2^73`; the `2^74` cap also covers sweep initialization and exits. All uninitialized record/message arrays are populated before reading, so they incur no implicit zeroing scan. Every failed trial and the full sort/scan are included.

Consequently, with `q=2^128`,

```text
H <= q+2
W <= (32 + 4*32 + 32)q + 2^74 + 2^24
  = 192q + 2^74 + 2^24
T <= H + W/2140 < 2^128.125 target-compression units.
```

The declared `time_log2=128.125` rounds this strict upper bound upward. A `preprocessing_log2=20` bound generously covers the fixed setup; the two `2^64`-bucket sweeps per pass are already in total time. The six `q`-word-equivalent message/record arrays use `192q` bytes. `C` uses `2^69` bytes; code, constants and fixed scratch stay below `2^24` bytes. Their total is less than `256q=2^136` bytes, so `memory_log2_bytes=136` is an upper bound. All counters, offsets and addresses are below `6q<2^131` and fit in one 256-bit word. Actual nonuniform advice is zero bytes; the schema's `nonuniform_advice_log2_bytes=0` is the one-byte upper-bound convention.

No experiment is declared because executing `2^128` hashes is infeasible. The proof is an analytic word-RAM bound with an astronomically large memory footprint. Passing a mechanical checker or AI screening would not make it a practical collision search, a mathematical certification by the reviewer, or a human-accepted promoted result.
