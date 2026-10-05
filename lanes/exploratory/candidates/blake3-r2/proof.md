# Four-lane grouped birthday search for 2-round BLAKE3

This package gives an ordinary collision algorithm for unkeyed BLAKE3-256 with
the first two compression rounds. The scalar is `time_log2` under
`collision-frontier-v5`. Memory is reported and is not part of the scalar.
The claimed bound is 127, with success probability 0.39 under one declared
heuristic. The nominal identifier `blake3-r2-nominal-v2` is not an established
attack, a qualified baseline, or a security theorem.

The message family is a grouped birthday search: `2^96` independent prefixes
of `m0..m14`, and every 32-bit value of the remaining word inside each group.
Round 0 is almost constant on a group. The varying tail and all of round 2 are
evaluated for four consecutive words at once by packing four 32-bit lanes into
each 256-bit register. A 160-bit sparse set finds candidate pairs. Every
returned pair is rehashed with two full target compressions.

Public unpromoted notes on this track already used a scalar version of the
grouped search. Those notes are not treated as proof. The message family, the
table, the probability bound, and the lane-packing evaluator are derived again
below. Packing is the change that lowers the charged word-operation count.

## 1. Exact hash

A message is 64 bytes, bit length 512, which is below `2^64`. Its sixteen
little-endian 32-bit words are `m0..m15`. There is one chunk, one block, no
parent, and one root compression. The flags are `CHUNK_START | CHUNK_END | ROOT`
= 11, the block length is 64, and both counters are 0. The chaining value is
the BLAKE3 IV

```
6a09e667 bb67ae85 3c6ef372 a54ff53a
510e527f 9b05688c 1f83d9ab 5be0cd19
```

All additions below are modulo `2^32`. `ROR` is a 32-bit right rotation.
`G(a,b,c,d,x,y)` updates the 16-word state `v` by

```
v[a] = v[a] + v[b] + x
v[d] = ROR(v[d] XOR v[a], 16)
v[c] = v[c] + v[d]
v[b] = ROR(v[b] XOR v[c], 12)
v[a] = v[a] + v[b] + y
v[d] = ROR(v[d] XOR v[a], 8)
v[c] = v[c] + v[d]
v[b] = ROR(v[b] XOR v[c], 7)
```

Round 0 calls `G` on `(0,4,8,12)`, `(1,5,9,13)`, `(2,6,10,14)`, `(3,7,11,15)`
with message pairs `(m0,m1)` through `(m6,m7)`, then on `(0,5,10,15)`,
`(1,6,11,12)`, `(2,7,8,13)`, `(3,4,9,14)` with `(m8,m9)` through `(m14,m15)`.
The message is then replaced by `m[P[i]]` where

```
P = (2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8)
```

Round 1 repeats the same eight calls on the permuted message. The digest is
the first eight words `v[i] XOR v[i+8]`, written little-endian. That is the
complete 256-bit root output. No parent and no second compression occurs for
these messages.

`m15` enters round 0 only as `y` of the last call, `G(3,4,9,14,m14,m15)`.
After the permutation, original `m15` is `x` of the last round-1 call,
`G(3,4,9,14,m15,m8)`.

## 2. Lane isolation

The machine is a classical 256-bit word RAM. One 2-round target compression
costs 1. Every other primitive costs `1/C` with `C = 430`: load, store,
addition modulo `2^256`, AND, OR, XOR, NOT, shift, comparison, conditional
branch, and a uniform random 256-bit word. A 32-bit rotation is the four
primitives in the reference: shift right, shift left, OR, AND with a mask.
No native 32-bit rotation is assumed.

Four lanes share one register. Lane `i` occupies bits `[64i, 64i+32)`. Bits
`[64i+32, 64i+64)` are a guard. The lane mask is

```
M4 = (2^32-1) * (1 + 2^64 + 2^128 + 2^192)
```

A word is lane-clean when every guard is zero.

Lemma (addition). If each lane of `x` and of `y` is an integer in
`[0, 2^32)`, then each lane of `x+y` (modulo `2^256`) equals the integer sum
of those lanes, and the carry stays inside that lane's guard. Three such
operands sum to at most `3*(2^32-1) = 2^34 - 3`, so the sum occupies at most
bits `[64i, 64i+34)` and does not reach bit `64(i+1)`.

Lemma (rotation). If `x` is lane-clean and `1 <= r <= 31`, then

```
((x >> r) OR (x << (32-r))) AND M4
```

is the packing of the four 32-bit rotations. A left shift by at most 31 moves
bit `64i+31` to bit `64i+62`, which is still inside the guard and below bit
`64(i+1)`. A right shift by at most 31 moves bit `64(i+1)` into the previous
guard, and the final AND clears every guard. The low 32 bits of each slot are
therefore exactly the rotated lane.

XOR, AND, and OR act bitwise, so they preserve the same slot split on
lane-clean inputs. The inner program masks after every addition and every
rotation, before the next XOR.

## 3. Group constants and the bijection

Fix `m0..m14`. Run round 0 through the first half of its last `G`. Those
steps do not read `m15`. Name the resulting half-state

```
ah = (v3 + v4 + m14) mod 2^32
dh = ROR(v14 XOR ah, 16)
ch = (v9 + dh) mod 2^32
bh = ROR(v4 XOR ch, 12)
S  = (ah + bh) mod 2^32
```

The second half would set `a' = (ah + bh + m15) mod 2^32 = (S + m15) mod 2^32`.
As `m15` runs through `0..2^32-1`, so does `a'`. The algorithm enumerates
`t = a'` and recovers `m15 = (t - S) mod 2^32`. That map is a bijection, so
each group still contains every 64-byte completion of its prefix exactly once.
The other round-0 outputs that do not depend on `m15` stay group constants.
Only state words `v3, v4, v9, v14` change with `t`.

## 4. Inner iteration

Each iteration handles four consecutive values `t, t+1, t+2, t+3`, packed into
one lane-clean register. Group constants used below are broadcast into all
four lanes during group setup, which is charged separately. `negS` is the
broadcast of `(-S) mod 2^32`.

Round-0 tail, 12 primitives:

```
v14 = ROR(dh XOR t, 8)          XOR and four rotation primitives
v9  = (ch + v14) AND M4         addition, AND
v4  = ROR(bh XOR v9, 7)         XOR and four rotation primitives
```

`v3` is the register `t`. Then `m15 = (t + negS) AND M4`, two primitives.
The addition lemma applies: both operands are lane-clean and smaller than
`2^32`.

Round 1 is eight ordinary `G` calls on the packed state. The last call uses
the packed `m15` as `x` and the broadcast `m8` as `y`. Each `G` is 30
primitives: three for each of the two `a` updates (`add, add, AND`), two for
each `c` update (`add, AND`), and five for each of the four rotations
(`XOR` plus four rotation primitives). Eight calls cost 240 primitives.
The eight digest words are eight XORs of `v[i]` with `v[i+8]`.

The straight-line body is `12 + 2 + 240 + 8 = 262` primitives for four
messages.

For each lane, five digest words `o0, o1, o2, o3, o5` are extracted and packed
into a 160-bit key. Extraction of one lane of one word is a shift and an AND.
Packing five extracted words is four shifts and four ORs. That is 18
primitives per lane and 72 per iteration. The key is smaller than `2^160`.

A scalar counter starts at 0 and increases by 4. The packed `t` increases by
the lane-clean constant `4` in every lane. One addition, one comparison, and
one branch control the loop, plus the addition into `t`: 4 primitives per
iteration. The last iteration uses `t = 2^32-4`, whose four lanes are
`2^32-4` through `2^32-1`. The following increment is not used as a message.

## 5. Collision table

The table is a Briggs–Torczon sparse set that is never bulk-initialized.
Dense records start at byte address 0 with stride 64. Record `i` holds the
160-bit key and a 128-bit message identifier `(group index, m15)`. `CC` is
the next free byte address, equal to `i << 6`. The sparse word for a key `K`
is the single word at address `2^160 + K`, formed by one OR because
`K < 2^160`.

On each message the program does at most the following 16 primitives, and the
cost section charges 24:

1. OR the sparse address.
2. Load the stored address.
3. Compare it with `CC`.
4. Branch to insert when it is out of range.
5. Load the dense key.
6. Compare it with `K`.
7. Branch to verification when the keys match.
8. Store the new key at `CC`.
9. Store the message identifier at `CC+32`.
10. Store `CC` into the sparse slot.
11. Add 64 to `CC`.

The remaining charged primitives cover the address arithmetic and the move of
the message identifier. Garbage in the sparse array cannot cause a false key
match: an in-range pointer is accepted only when the dense key equals `K`.

A key match does not return immediately. Both messages are rebuilt from the
stored group prefix and the two values of `m15`, then hashed with two full
2-round compressions. The pair is returned only when the messages differ and
all 256 digest bits agree. If the 160-bit keys match and the full digests do
not, the new message is not stored. The program counts these verification
attempts and stops with failure after `2^110` of them. Stopping enforces the
time cap whether or not a collision exists.

## 6. Algorithm

1. For each of `2^96` groups, draw 448 fresh uniform bits, store them as
   `m0..m14`, and compute the group constants of Section 3. Charge at most
   8192 word primitives for the whole setup of one group, including the
   broadcasts and the prefix store.
2. For that group, run the iteration of Section 4 for every aligned block of
   four `t` values. Insert each lane into the table.
3. On a key match, spend two target compressions and at most 4096 word
   primitives to rebuild, rehash, and test the pair. Return on success.
   Abort after `2^110` such attempts.
4. If the groups end with no verified collision, fail.

Every accepted message is 64 bytes. The final test uses the complete root
hash of Section 1, not a free-start compression and not a truncated digest.
There is no advice string and no stored collision.

## 7. Heuristic H1

H1 states that, for the failure events in Section 8, the `2^128` digests of
these messages may be analyzed as mutually independent and uniform in
`{0,1}^256`.

H1 is not a theorem. Messages that share `m0..m14` differ by one word, and
the two-round map is deterministic. The experiments in Section 11 test only
20-bit projections of `2^10` messages. They can support plausibility. They do
not prove independence at `2^128`. The claimed success probability is the
probability inside this model, minus an explicit allowance, not a measured
frequency and not a confidence score.

## 8. Success probability given H1

Let `N = 2^128` and `Q = 2^256`. Under H1 the probability of no full-digest
collision is

```
N! / Q^N * (ways to choose N outputs)
  = product_{j=0}^{N-1} (1 - j/Q)
  <= exp(-N(N-1)/(2Q))
```

using `1-x <= exp(-x)`. The exponent equals

```
2^128 * (2^128 - 1) / 2^257 = 1/2 - 2^{-129}
```

So the bound is `exp(-1/2) * exp(2^{-129})`.

The alternating series for `exp(-1/2)`, stopped after the positive degree-10
term, is an upper bound because the next term is negative and the terms then
decrease. That partial sum is the rational

```
2253801941 / 3715891200
```

which is smaller than `60653066/100000000`. Also `exp(y) < 1 + y + 2y^2` for
`0 < y < 1/2`, so `exp(2^{-129}) < 1 + 2^{-128}`. Therefore

```
Pr[F1] < 60653066/100000000 + 2^{-128}
```

F2 is the event that some full collision is missed because a different digest
with the same 160-bit key occupies the slot. Any such miss gives three
distinct messages `X, Y, Z` with equal 160-bit keys on `X` and `Y`, equal full
digests on `Y` and `Z`, and unequal full digests on `X` and `Y`. Under H1 a
fixed triple has probability below `2^{-256} * 2^{-160} = 2^{-416}`. There are
fewer than `2^{384}` triples, so `Pr[F2] < 2^{-32}`.

Fcap is the event of at least `2^110` key matches. The number of unordered
pairs that collide on a fixed 160-bit projection has expectation below
`N(N-1)/2 * 2^{-160} < 2^{95}`. Each match event is one such later message.
Markov's inequality gives `Pr[Fcap] <= 2^{95}/2^{110} = 2^{-15}`.

F3 is a repeated 448-bit prefix. A union bound over the `2^96` groups is
below `2^{191}/2^{448} = 2^{-257}`.

The algorithm succeeds unless one of these events occurs. Hence

```
Pr[success] > 1 - 60653066/100000000 - 2^{-14}
```

because `2^{-128} + 2^{-15} + 2^{-32} + 2^{-257} < 2^{-14}`. The right-hand
side equals

```
39346934/100000000 - 1/16384
```

Subtracting `0.39 = 39/100` leaves

```
346934/100000000 - 1/16384
```

The first term is larger because `346934 * 16384 > 100000000`. The difference
is positive, so the model probability is greater than 0.39. The claim uses
0.39 and leaves the extra margin as allowance for H1.

## 9. Charged time

Listed primitives per iteration of four messages:

| Piece | Primitives |
| --- | ---: |
| Round-0 tail, `m15`, eight `G` calls, eight digest XORs | 262 |
| Five-word key extraction for four lanes | 72 |
| Table probe and possible insert, charged at 24 each | 96 |
| Loop addition, comparison, and branch | 4 |
| Listed total | 434 |

`434/4 = 108.5` primitives per message. The charge is 192 per message. The
83.5 unused primitives per message cover register moves, reloading a group
constant, and extra address arithmetic. Reloading every message word once per
iteration would add 15 loads per four messages. Reloading and storing every
`G` operand, 10 memory primitives on each of eight calls, would add 80 per
iteration, which is 20 per message and still inside the 83.5.

Word primitives therefore satisfy

```
W <= 192 * 2^128 + 8192 * 2^96 + 4096 * 2^110 + 2^20
```

Target compressions are only the capped verifications:

```
H <= 2 * 2^110 = 2^111
```

With `C = 430`,

```
8192/430 * 2^96 < 2^5 * 2^96 = 2^101
4096/430 * 2^110 < 2^4 * 2^110 = 2^114
2^20/430 < 2^12
```

and `2^111 + 2^101 + 2^12 < 2^115 - 2^114`, so

```
T = H + W/C < (192/430) * 2^128 + 2^115
  = 2^127 * (192/215 + 2^{-12})
```

Now `1 - 192/215 = 23/215` and `23/215 > 2^{-12}` because
`23 * 4096 = 94208 > 215`. Thus `T < 2^127`. The bound includes setup, every
message, the table, failed verifications, and the final successful rehash.
It is a cap on every run, not an expectation and not a conditional cost.

The same arithmetic with 214 word primitives per message still has a main
term below `2^127`. The submitted charge is 192, not 214.

## 10. Memory and the other fields

Sparse addresses are below `2^161` words. At 32 bytes per word the address
span is below `2^166` bytes, which is inside the reported `2^167` bytes.
Dense records write at most `2^128 * 64` bytes. Prefixes write
`2^96 * 64` bytes. Bytes actually stored are below `2^135`. The reported
memory figure is the address span, because the sparse array is a flat table.

`preprocessing_log2 = 101` bounds the group-setup term `2^101` already inside
`T`. `nonuniform_advice_log2_bytes = 0` means no advice; the schema cannot
represent log2 of zero, and the real advice length is zero. Code and the IV
are charged in the `2^20` fixed term. `success_probability = 0.39` is the
lower bound of Section 8. `data_log2` is omitted.

`baseline_improved` is the required nominal identifier. This scalar is not
claimed to be a security bound, and it is not claimed to improve a promoted
qualified attack. Promotion of any earlier package is a separate event.

## 11. Experiments and limits

`experiments/grouped_birthday.py` searches two scaled families and returns one
pair whose digests match on the low 20 bits of the big-endian digest integer,
or two nulls. The spread layout is 32 prefixes by 32 consecutive final words.
The single-group layout is one prefix and 1024 consecutive final words.
For `N = 2^10` and a 20-bit mask, `C(N,2)/2^20` is just under `1/2`, so an
independent uniform model succeeds with probability about `1 - exp(-1/2)`,
near 0.39. The organizer recomputes both digests with the trusted 2-round
function. A returned pair is evidence only for that pair. The program's
operation count is not an attack cost.

The local reference implementation of the packed evaluator was compared with
`verifier/blake3.py` on random prefixes, on the all-zero and all-ones
prefixes, and on the extreme `t` values `0` and `2^32-1`. Those checks are
development checks. They are not organizer evidence.

This is not a differential cryptanalysis of BLAKE3. A generic 256-bit
collision search cannot go far below `2^128` compressions; the saving is that
shared round-0 work and four-lane packing are charged as word primitives at
`1/430`, not as one compression per message. H1 can be false for a
pathological schedule even if the experiments look ordinary. The time bound
does not depend on H1. The success probability does.
