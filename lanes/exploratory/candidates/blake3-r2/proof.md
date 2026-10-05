# Tighter generic birthday bound for 2-round BLAKE3

## 1. Target and claim

The target is `blake3-r2-prefix-v1`. A result is two distinct byte strings whose complete unkeyed BLAKE3-256 digests agree when every compression keeps only prefix rounds 0 and 1. This algorithm only builds 64-byte messages. Each such message is one root compression: chaining value IV, counter 0, block length 64, flags 11. The digest is the first eight words `v[i] XOR v[i+8]`.

The claimed scalar is `time_log2 = 137`. Success probability is at least 1/2 for every function from this message domain to 256-bit strings. There is no heuristic. Memory is reported as 138 and is not part of the scalar. The promoted incumbent charges a much looser merge envelope and claims 140. This package keeps the same generic search and prices the merge with an itemized word-operation cap.

## 2. Algorithm

Let `n = 2^129`. Draw `n` independent uniform 512-bit strings. Encode each as a 64-byte message by splitting it into two 256-bit words and writing those words little-endian. Compute the 2-round digest. Store the triple `(digest, word0, word1)`.

Sort the `n` records by the unsigned 256-bit digest, using a bottom-up merge sort of 129 passes. Scan adjacent records. If two adjacent digests are equal and the messages differ, output that pair and stop. If a sample repeats the same message, ignore that pair. It is not a collision. After the scan, if no collision was found, halt with failure. There is no restart.

The final accepted pair is checked with two fresh compressions and a message-distinctness test.

## 3. Probability

The domain has size `2^512`. The codomain has size `N = 2^256`. Samples are independent and uniform. The chance that two samples are the same 512-bit string is negligible: at most `n(n-1)/2 / 2^512 < 2^{-254}`. Those repeats are not counted as collisions.

For any function `f` into a set of size `N`, random sampling collides at least as often as it does for a balanced function. The balanced case is the usual birthday bound. With `n = 2^129`,

```
n(n-1)/(2N) = 2^129 * (2^129 - 1) / 2^257 = 2 - 2^{-128} > 1.999
```

So the probability of some digest collision among the samples is at least `1 - exp(-1.999) > 0.86`, which is greater than 1/2. The schema floor is 0.39. The claim uses 0.5.

This bound does not assume that BLAKE3 is random, uniform, or independent across rounds. A more unbalanced function only raises the collision probability.

## 4. Cost

The machine is the collision-frontier-v5 256-bit word RAM. `C = 430` for blake3-r2. One selected 2-round compression costs 1. Each listed 256-bit word operation costs `1/430`. A digest comparison is one comparison of one 256-bit word, not eight 32-bit comparisons.

Generation, per sample: two random-word draws, two stores of the message, one store of the digest, and a handful of address operations. Charge 32 word operations. That is `32/430 < 0.075` units, plus the one compression.

Merge, per emitted record, itemized: load two keys, compare, branch, load three record words, store three record words, update two cursors, and four address operations. That is 16 word operations. The claim does not use 16. It charges 64 word operations per emitted record per pass, four times the itemization. There are 129 passes, and each pass emits `n` records.

```
merge units per sample = 129 * 64 / 430 = 19.200
generation units per sample < 0.075
compression units per sample = 1
units per sample < 20.275
```

```
T < 20.275 * 2^129 < 2^133.35
```

Final verification is two compressions and fewer than 64 word operations. It is absorbed by the inequality above.

Sensitivity of the same formula if a reviewer replaces 64 by a larger cap:

| word ops per record per pass | units per sample | log2(T) |
| --- | ---: | ---: |
| 16, the itemized step | 5.81 | 131.54 |
| 64, charged | 20.28 | 133.34 |
| 256 | 77.8 | 135.28 |
| 512 | 154.6 | 136.27 |

The submitted scalar is 137. It covers the 512-operation reading. It does not cover the incumbent's 4096-operation cap. That cap is the difference between 140 and this claim. The 64-operation charge is already four times a 16-operation merge step on 256-bit words.

## 5. Memory

Each record is three 256-bit words, 96 bytes. Merge sort keeps two arrays, so the live records occupy `192 * 2^129 < 2^136.6` bytes. Code and a few cursors are negligible next to that. The reported `memory_log2_bytes` is 138. Memory does not enter the scalar.

There is no nonuniform advice and no preprocessing beyond the constant setup, which is below one unit and is included in the generation cap.

## 6. What this is not

This is not a structural attack on two-round BLAKE3. It does not use a truncated key, a packed evaluator, or a uniformity heuristic. Those pending claims are lower than 137. This package only tightens the worst-case generic envelope that the promoted 140 score prices with a 4096-operation merge cap. If a reviewer requires that 4096 cap, this claim does not improve on 140, and the proof says so.
