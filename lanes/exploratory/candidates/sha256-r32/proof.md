# SHA-256, 32 rounds: ordinary-collision conversion of the published 32-step characteristic

This claim is an exploratory upper bound on one attack, not a certificate that a colliding pair has already been written down. The target is complete-message SHA-256 with the fixed FIPS 180-4 IV, standard padding, feed-forward, compression steps 0 through 31 on every padded block, and equality of all 256 digest bits. One unit is one such 32-round compression. The reference cost `C = 2224` is not applied on top of these trials: each counted trial is already one target compression, or a cheaper prefix of one that is still charged as one.

The bound is `2^60.3` target compressions after one valid tuple for the 32-step characteristic is in hand. It does not include a compression count for the search that found that tuple. Declared `time_log2` is 60.3. Declared `preprocessing_log2` is 1, which pays two compressions to recheck the published semi-free-start pair and nothing else. Algorithmic success probability at this budget is at least 0.63 when the three filters below are independent and the tail rate is no worse than the charged cap.

## 1. The characteristic that is being converted

Table 5 and Table 6 of Li, Liu, Wang, and Shi, IACR ePrint 2026/1080, are a 32-step SHA-256 differential and one semi-free-start pair that follows it. The chaining value is not the FIPS IV.

```text
cv  f604f1fc eeb3a0ab a17e8834 b3c61523 e04e13b7 ad98efcc 85a314c4 8c19ae04
M'  de9958c9 dea3d356 e8c41e64 6314adfe d0f59a38 b2bcf93e 043c70b6 f15f77e4
    6a615447 4c44bb60 32d873ed bf9c1ea0 14f370a0 ac13a010 ff46f88d 1637894b
M   de9958c9 dea3d356 f8c61e65 6314adf6 d0b08a9a b73c792e 007c00b6 005b57ec
    ea415447 4c44bb60 32d873ed bf9c1ea0 14f370a0 ac13a010 ff46f88d 1637894b
```

Both messages, compressed for 32 steps from that chaining value, produce `5ccc4292 79d66eb4 23405cdc d88e2a1f 27710bb1 b91b9b8a 3def8bca fb9697ce`. The state difference is zero from step 16 through step 31 on this pair, and the schedule difference after step 8 is zero except for two bits of `W17`. Those two bits are bit 31 and bit 21, both signed `u` in Table 5.

This pair is a semi-free-start collision. It is not, by itself, an ordinary collision for this target. The 45 conditions in Section 4 of the same paper are a different attack: they produce a 35-step collision, and that published pair does not agree at 32 rounds. Nothing below reuses those 45 conditions.

Table 5 fixes the early words tightly. Counting every symbol other than `=` gives the condition totals used here:

| word | conditions | role in the two-block framework |
| --- | ---: | --- |
| `W8` | 2 | `n1` |
| `E4` | 31 | `n2` |
| `W7` | 8 | `n3` |
| `E3` | 30 | `n4` |
| `W4` | 7 | part of `Npro` |
| `W5` | 5 | part of `Npro` |
| `W6` | 5 | part of `Npro` |
| `W17` | 2 | inside the tail, not charged separately |

`Npro = 7+5+5 = 17`. The `W4`, `W5`, and `W6` marks are signed bits only, with no extra `0` or `1` symbols on those three words. Bit positions, with bit 0 the least significant bit, are:

```text
W4  bits 22, 18, 16, 12, 7, 5, 1
W5  bits 26, 24, 23, 15, 4
W6  bits 26, 22, 14, 13, 12
```

`E4` has one free bit and `E3` has two. Under the framework's count of valid tuples per starting point, `2^{2*32 - (2+31+8+30)} = 2^{-7}`. A large table of distinct `A-1` values is not free. This claim therefore prices one tuple, not a table that divides the 32-bit match.

## 2. Three filters, one tuple

The memory-efficient two-block method matches a first block against one stored tuple, then spends the second-block tail freedom. For one tuple the filters are:

1. The first block's chaining word `A-1` equals the stored value. A first block is one target compression. For a uniform 32-bit word this costs `2^32` trials.
2. The derived words `W4`, `W5`, and `W6` meet the 17 signed conditions above. Charged as an independent factor `2^17`.
3. The shared tail `(W14, W15)` makes the two branches agree from step 16 through step 31. The measured rate on the published tuple is `2^{-10.978}`. The claim charges `2^11.3`.

The product is the number of first-block compressions:

```text
32 + 17 + 11.3 = 60.3
```

So the conversion, given the tuple, is at most `2^60.3` target compressions. Each failed first block is one compression. Each tail trial is at most one compression, and only the first blocks that already passed the first two filters reach the tail. The expected number of tail trials in a run that expects one success is `2^11.3`, which is far below `2^60.3` and does not change the sum.

At a budget of `2^60.3` trials and a per-trial success probability of `2^{-60.3}`, the expected number of successes is 1. The probability of at least one success is `1 - exp(-1) > 0.632`. The declared success probability is 0.63.

Checking the published pair takes two compressions from the published chaining value. `log2(2) = 1`, which is `preprocessing_log2`. Those two compressions sit inside the same `2^60.3` ceiling.

## 3. The tail measurement

Fix `W0` through `W13` to the two published messages, including the message difference. Draw `(W14, W15)` uniformly, using the same value on both branches, because Table 5 gives those two words difference zero. Run 32 steps from the published chaining value on both branches. A trial succeeds when `A_i` and `E_i` agree for every `i` from 16 through 31. Agreement of those words from step 16 through step 31 clears the whole 8-word state by step 19, because the only earlier words still in the register are equal by step 19. The same chaining value then makes the feed-forward outputs equal.

In `2^18 = 262144` independent draws there were 130 successes. The failures split in two and then stopped:

| first disagreement | trials | fraction |
| --- | ---: | ---: |
| step 16 | 245756 | 0.9375 |
| step 19 | 16258 | 0.0620 |
| none through step 31 | 130 | 0.000496 |

`245756 + 16258 + 130 = 262144`. No trial that passed step 16 failed at step 17 or 18, and no trial that passed step 19 failed later. Passing step 16 happened on `16388 / 262144 = 2^{-4.000}` of the draws. Passing step 19 as well happened on `130 / 16388` of those, which is `2^{-6.978}`. The joint rate is

```text
-log2(130 / 262144) = 10.978
```

A normal approximation to the Poisson count, one-sided 95 percent, puts the success count at least `130 - 1.645*sqrt(130) > 111.2`. Then

```text
-log2(111.2 / 262144) < 11.21
```

The claim uses `11.3`, about a tenth of a bit above that approximation. `W16` was identical on every draw. The two-bit pattern of `W17` held on about half of the draws and is already inside the 11.3, not an extra factor. `W20` and `W22` did not need their own conditions on this characteristic.

The same sample is one published tuple, not a fresh draw of the early state. Using `11.3` for every tuple that passes the 17 conditions is an extrapolation.

## 4. What the 60.3 does not buy

The `2^{-7}` tuples-per-start figure says that producing another tuple costs further starting points. This bound does not pay for those starting points, and it does not pay for the search that produced Table 5 and Table 6. Mendel, Nad, and Schläffer (ASIACRYPT 2011) report that finding one conforming 32-step semi-free-start example took a few days on a 32-node cluster. That report is wall-clock, not a compression count, so it is not converted into an exponent here. A later improvement can divide the `2^32` match by storing many `A-1` values, or replace the factor `2^17` by a measured joint probability of the 17 bits, or put a counted price on the starting-point search. Any of those replaces this bound rather than sitting on top of a hidden discount.

Two message bits were observed to be neutral for the published tuple under the full Table 5 symbol pattern: `W13` bit 15 and `W13` bit 22. Flipping either one, alone, left the signed pattern in place. That is a lead toward more tuples. It is not used in the `2^60.3`.

## 5. Memory and advice

The online attack stores one tuple, the message difference, and the working state of one compression. That is well below `2^20` bytes. No `2^29`-entry table is built. The nonuniform advice is the published characteristic and the one published pair, under `2^12` bytes.

## 6. Heuristic statements

The score-critical premise is that, given one Table 5 tuple, uniform first-block `A-1` words and independent `W4`/`W5`/`W6` conditions multiply with the charged tail rate:

```text
T <= 2^32 * 2^17 * 2^11.3 = 2^60.3
```

The supporting premises are the tail-rate cap `2^11.3` on this tuple, the symbol counts `n1=2`, `n2=31`, `n3=8`, `n4=30` that keep the claim at one tuple, and the memory ceiling `2^20`.
