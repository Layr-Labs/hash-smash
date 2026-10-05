# Closed-form ordinary collision for 1-round BLAKE3

## 1. Target

The target is `blake3-r1-prefix-v1`: unkeyed BLAKE3-256 with prefix round 0 only, standard IV, standard tree, and a full 256-bit root digest. A result is two distinct byte strings whose `blake3` digests at `rounds=1` agree on all 32 bytes. This package uses two 64-byte messages. Each is one chunk, one block, and one root compression with chaining value IV, counter 0, block length 64, and flags `CHUNK_START|CHUNK_END|ROOT = 11`.

The state before the round is

```
v[0..7]  = IV
v[8..11] = IV[0..3]
v[12..15] = (0, 0, 64, 11)
```

`G` is the BLAKE3 mixing function. All additions are modulo `2^32`. `ROR` and `ROL` are 32-bit rotations. The digest words are `o[i] = v[i] XOR v[i+8]` for `i = 0..7`, little-endian. This matches `verifier/blake3.py`.

## 2. Column identity

Lemma 1. For any inputs `(a, b, c, d)`, set

```
d1 = b - c
a1 = d XOR ROL(d1, 16)
x  = a1 - a - b
A  = ROL(-b, 8) XOR d1
y  = A - a1
```

Then `G(a, b, c, d, x, y) = (A, 0, 0, -b)`.

Proof, one line at a time. The first addition is `a + b + x = a + b + (a1 - a - b) = a1`. Then `d` rotates to `ROR(d XOR a1, 16) = ROR(ROL(d1, 16), 16) = d1`. Then `c + d1 = c + (b - c) = b`. Then `b` rotates to `ROR(b XOR b, 12) = 0`. The second addition is `a1 + 0 + y = a1 + (A - a1) = A`. Then `d` rotates to `ROR(d1 XOR A, 8) = ROR(ROL(-b, 8), 8) = -b`. Then `c` becomes `b + (-b) = 0`. Then `b` rotates to `ROR(0 XOR 0, 7) = 0`. The output is `(A, 0, 0, -b)`.

Apply Lemma 1 to all four columns. The inputs are `(IV0, IV4, IV0, 0)`, `(IV1, IV5, IV1, 0)`, `(IV2, IV6, IV2, 64)`, and `(IV3, IV7, IV3, 11)`. The column outputs are `(A0, 0, 0, -IV4)`, `(A1, 0, 0, -IV5)`, `(A2, 0, 0, -IV6)`, and `(A3, 0, 0, -IV7)`, with

```
A0 = 16a9edb6
A1 = 250ace63
A2 = 9f32b3d9
A3 = a9a2307b
```

## 3. Diagonal identity

After the columns, the diagonal inputs are

```
G4: (A0, 0, 0, -IV7)
G5: (A1, 0, 0, -IV4)
G6: (A2, 0, 0, -IV5)
G7: (A3, 0, 0, -IV6)
```

Lemma 2. If the inputs are `(a, 0, 0, d)` and `x = d - a`, then for `g = y + d`,

```
G(a, 0, 0, d, x, y) = (g, ROR(g, 15), ROR(g, 8), ROR(g, 8))
```

Proof. The first addition is `a + 0 + (d - a) = d`. The first `d` rotation is `ROR(d XOR d, 16) = 0`. Then `c` stays 0, and `b` stays 0. The second addition is `d + 0 + y = g`. The second `d` rotation is `ROR(0 XOR g, 8) = ROR(g, 8)`. Then `c` becomes `ROR(g, 8)`. Then `b` rotates to `ROR(0 XOR ROR(g, 8), 7) = ROR(g, 15)`.

Thus `y = -d` gives `g = 0` and output `(0, 0, 0, 0)`. And `y = -d - 1` gives `g = 0xffffffff`, whose every rotation is itself, so the output is `(0xffffffff, 0xffffffff, 0xffffffff, 0xffffffff)`.

Set the diagonal `x` words to the Lemma 2 values and the `y` words as follows.

| word | M | M' |
| --- | --- | --- |
| m8, x of G4 | `8d754531` = `-IV7 - A0` | same |
| m9, y of G4 | `IV7` | `IV7 - 1` |
| m12, x of G6 | `c5c7e39b` = `-IV5 - A2` | same |
| m13, y of G6 | `IV5` | `IV5 - 1` |
| m10, m11, m14, m15 | `ffffffff` | same |

Under M, G4 and G6 output all zeros. Under M', they output all ones. G5 and G7 see the same inputs and the same message words, so they output the same state words for both messages.

## 4. The digest agrees

The affected digest words are XORs of G4 and G6 outputs:

```
o0 = v0 XOR v8
o2 = v2 XOR v10
o5 = v5 XOR v13
o7 = v7 XOR v15
```

Under M each of those words is `0 XOR 0 = 0`. Under M' each is `ffffffff XOR ffffffff = 0`. The other four digest words come from G5 and G7, which are identical for M and M'. So the 256-bit digests agree.

M and M' differ in m9 and m13. They are distinct. Both are 64 bytes, so each hash is exactly one root compression. The certificate digest is `0000000021fa412d00000000ef3de981afe12ffa00000000fb15a2c700000000`.

## 5. Cost

The machine is the collision-frontier-v5 256-bit word RAM. One 1-round BLAKE3 compression costs 1. Every other listed word operation costs `1/222`. A 32-bit add or subtract is an addition plus a mask. A 32-bit rotation is shift right, shift left, or, and mask. There is no native 32-bit rotate.

The straight-line construction uses 13 constant loads, 80 column operations (20 per column), 8 operations for the two diagonal `x` words and the two decremented `y` words, and 32 stores. The self-check loads both messages (32 loads), runs two compressions, and compares the digest and the two differing words (at most 24 word operations). That is 189 word operations plus 2 compressions.

```
T = 2 + 189/222 = 2.8514
log2(T) = 1.512
```

The claim does not use that tight count. It charges 400 word operations, which covers the program above, a second copy of the construction, and more than 200 spare operations for a reviewer who also charges program placement:

```
T_claim_bound = 2 + 400/222 = 3.802
log2 = 1.927
```

The submitted `time_log2` is 2.5. That bound still holds if the word-operation count is doubled again to 800 (`T = 5.604`, `log2 = 2.486`).

Memory is the two 64-byte messages, fewer than 20 constants, and fewer than 8 KiB of program text. That is under `2^14` bytes. Preprocessing and nonuniform advice are 0. There is no random coin, no failed trial, and no heuristic. Success probability is 1.

## 6. What this does not claim

This is a 1-round collision. The same bytes do not collide at 2 rounds. It is not a free-start collision and not a truncated collision. The nominal reference 128 is not an established attack. The scalar 2.5 is a conservative charge for this closed form, not a claim that 2.5 is the minimum legal reading.
