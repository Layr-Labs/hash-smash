# A one-round ordinary collision for unkeyed BLAKE3-256

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is a
separately reported bound. The target is `blake3-r1-prefix-v1`: complete
unkeyed BLAKE3-256 with one prefix round in every compression, the standard
IV, the standard 1024-byte chunk tree, and the first 32 little-endian bytes of
the root output. This package gives a deterministic straight-line construction
of two distinct 64-byte messages whose digests are both the 32-byte zero
string. The counted program performs 475 word-RAM primitives. With the
reference price C = 222,

    475 / 222 < 2^1.30,

so the submitted bound is `time_log2 = 1.30`. The heuristic list is empty.
`baseline_improved` names the nominal display identifier
`blake3-r1-nominal-v2`. That identifier is not an established attack, a
qualified baseline, or a security bound.

## 1. The complete hash on the messages this algorithm returns

Each returned message is exactly 64 bytes, so its bit length is 512, which is
below 2^64. A 64-byte input is one chunk and one full block. There is no
parent node and no second block. The single compression uses the standard IV
as the chaining value, chunk counter 0, block length 64, and flags

    CHUNK_START | CHUNK_END | ROOT = 1 | 2 | 8 = 11.

The root compression uses output counter 0 together with those flags. The
digest is the first 32 little-endian bytes of the compression output, which
are the eight words `v[i] XOR v[i+8]` for `i = 0..7`. The other eight output
words, `v[i+8] XOR cv[i]`, are not part of this digest.

All additions below are modulo 2^32. `ROR` and `ROL` are 32-bit rotations.
The standard IV is

    IV0 = 0x6A09E667    IV1 = 0xBB67AE85    IV2 = 0x3C6EF372    IV3 = 0xA54FF53A
    IV4 = 0x510E527F    IV5 = 0x9B05688C    IV6 = 0x1F83D9AB    IV7 = 0x5BE0CD19.

The compression state starts as

    v[0..7]  = IV[0..7]
    v[8..11] = IV[0..3]
    v[12..15] = (0, 0, 64, 11).

The message is sixteen little-endian words `m[0..15]`. One round is eight G
calls. G(a, b, c, d, x, y) updates the state by

    v[a] = v[a] + v[b] + x
    v[d] = ROR(v[d] XOR v[a], 16)
    v[c] = v[c] + v[d]
    v[b] = ROR(v[b] XOR v[c], 12)
    v[a] = v[a] + v[b] + y
    v[d] = ROR(v[d] XOR v[a], 8)
    v[c] = v[c] + v[d]
    v[b] = ROR(v[b] XOR v[c], 7).

The round schedule, with message words in their initial order, is

    column:    G(0,4,8,12, m0,m1)   G(1,5,9,13, m2,m3)
               G(2,6,10,14, m4,m5)   G(3,7,11,15, m6,m7)
    diagonal:  G(0,5,10,15, m8,m9)   G(1,6,11,12, m10,m11)
               G(2,7,8,13, m12,m13)  G(3,4,9,14, m14,m15).

The BLAKE3 message permutation is applied after a round. With exactly one
round it does not change the words consumed by these eight calls. This is the
ordinary root hash of a 64-byte string. It is not a free-start compression,
and it does not change the IV, the flags, the padding rule, or the output
length.

## 2. Inverting one G call

Write the forward G call on inputs `(a, b, c, d, x, y)` as the eight
assignments

    a1 = a + b + x
    d1 = ROR(d XOR a1, 16)
    c1 = c + d1
    b1 = ROR(b XOR c1, 12)
    A  = a1 + b1 + y
    D  = ROR(d1 XOR A, 8)
    C  = c1 + D
    B  = ROR(b1 XOR C, 7).

Addition and XOR are bijections in each argument separately, and a 32-bit
rotation is a bijection. Each step can therefore be run backwards.

Lemma 1. Fix the incoming state `(a, b, c, d)` and target words `(Ct, Dt)`.
The unique message words that make the G call end at `C = Ct` and `D = Dt`,
together with the `A` and `B` that G then produces, are

    c1 = Ct - Dt
    d1 = c1 - c
    a1 = d XOR ROL(d1, 16)
    x  = a1 - a - b
    b1 = ROR(b XOR c1, 12)
    A  = d1 XOR ROL(Dt, 8)
    y  = A - a1 - b1
    B  = ROR(b1 XOR Ct, 7).

Proof. Substitute these formulas into the forward assignments. The choice of
`c1` is exactly what `C = c1 + D` requires once `D = Dt`. The choice of `d1`
is exactly what `c1 = c + d1` requires. `ROL` undoes `ROR` by 16, so `a1` is
the unique word with `d1 = ROR(d XOR a1, 16)`. Then `x` is the unique word
with `a1 = a + b + x`. The displayed `b1` is the forward value. `ROL` undoes
`ROR` by 8, so `A` is the unique word with `Dt = ROR(d1 XOR A, 8)`, and `y`
is the unique word that produces that `A`. The last line is the forward
formula for `B` at `C = Ct`. Every step is an equivalence, so the forward
call on `(x, y)` ends at `(A, B, Ct, Dt)`.

Lemma 2. Fix `(a, b, c, d)` and target words `(Bt, Ct)`. There are unique
`(x, y, D)` such that the call ends at `B = Bt` and `C = Ct`, and

    b1 = Ct XOR ROL(Bt, 7)
    c1 = b XOR ROL(b1, 12)
    d1 = c1 - c
    D  = Ct - c1
    a1 = d XOR ROL(d1, 16)
    x  = a1 - a - b
    A  = d1 XOR ROL(D, 8)
    y  = A - a1 - b1.

Proof. `B = ROR(b1 XOR C, 7)` and `C = Ct` force `b1 = Ct XOR ROL(Bt, 7)`.
`b1 = ROR(b XOR c1, 12)` then forces `c1`. The next two lines are the unique
`d1` and `D` compatible with `c1 = c + d1` and `Ct = c1 + D`. The remaining
lines are Lemma 1 for the now-determined target `D`, and the produced `B`
equals `Bt` because `b1` was chosen for that purpose.

Two specializations are used as identities, not as extra searches.

Identity Z. If `b = c = 0` and `(Ct, Dt) = (0, 0)`, Lemma 1 collapses to
`A = B = C = D = 0`, `x = d - a`, and `y = -d`. In particular the four output
words are zero for every incoming `a` and `d`.

Identity K. If `b = c = 0` and the target is an arbitrary `(C0, D0)`, Lemma 1
gives output words that do not depend on `a` or `d`:

    c1 = C0 - D0
    A0 = c1 XOR ROL(D0, 8)
    B0 = ROR(ROR(c1, 12) XOR C0, 7),

with `C = C0` and `D = D0`.

## 3. Column and diagonal wiring

Number the four column calls 0..3 and the four diagonal calls 0..3 in the
schedule of Section 1. After the columns, the diagonal inputs are

    Gd0 reads (A, B, C, D) from columns (0, 1, 2, 3) respectively as (A, B, C, D)
    Gd1 reads columns (1, 2, 3, 0)
    Gd2 reads columns (2, 3, 0, 1)
    Gd3 reads columns (3, 0, 1, 2).

Concretely, Gd2's `b` input is column 3's `B` output and Gd2's `c` input is
column 0's `C` output. The digest words are

    h0 = A(Gd0) XOR C(Gd2)     h1 = A(Gd1) XOR C(Gd3)
    h2 = A(Gd2) XOR C(Gd0)     h3 = A(Gd3) XOR C(Gd1)
    h4 = B(Gd3) XOR D(Gd1)     h5 = B(Gd0) XOR D(Gd2)
    h6 = B(Gd1) XOR D(Gd3)     h7 = B(Gd2) XOR D(Gd0).

The initial column inputs, from the state in Section 1, are

    column 0: (IV0, IV4, IV0, 0)
    column 1: (IV1, IV5, IV1, 0)
    column 2: (IV2, IV6, IV2, 64)
    column 3: (IV3, IV7, IV3, 11).

## 4. The two messages

The program fixes the public constants `C0 = 2` and `D0 = 5`. These constants
are part of the program text. They were not produced by a search. Define

    A0, B0   by Identity K at (C0, D0)
    diff     = A0 - B0
    K        = diff - (C0 XOR ROL(B0, 8))
    L        = ROL(A0 XOR ROL(D0, 7), 12) XOR diff.

Evaluating the arithmetic gives

    C0 - D0              = 0xFFFFFFFD
    ROL(5, 8)            = 0x00000500
    A0                   = 0xFFFFFAFD
    ROR(0xFFFFFFFD, 12)  = 0xFFDFFFFF
    B0                   = 0xFBFFBFFF
    diff                 = 0x04003AFE
    ROL(B0, 8)           = 0xFFBFFFFB
    C0 XOR that rotate   = 0xFFBFFFF9
    K                    = 0x04403B05
    ROL(5, 7)            = 0x00000280
    A0 XOR that rotate   = 0xFFFFF87D
    ROL of that word, 12 = 0xFF87DFFF
    L                    = 0xFB87E501.

In particular `K` is not zero. The same formulas at `(C0, D0) = (0, 0)` yield
`K = L = 0`, which is why the program does not use the zero constants.

Message M. Invert every column with Lemma 2 at target `(B, C) = (0, 0)`.
Invert every diagonal with Lemma 1 at target `(C, D) = (0, 0)`. The diagonal
inputs `b` and `c` are column `B` and `C` outputs, so they are 0.

Message M'. Reuse columns 1 and 2 of M, which already end at `(B, C) = (0, 0)`.
Invert column 0 with Lemma 2 at `(B, C) = (0, K)` and column 3 with Lemma 2
at `(B, C) = (L, 0)`. Then

    Gd0 uses Lemma 1 at target (C0, D0); its b and c inputs are still 0
    Gd1 uses Lemma 1 at target (0, 0); its b and c inputs are 0
    Gd2 uses Lemma 1 at target (A0, B0); its b input is L and its c input is K
    Gd3 uses Lemma 1 at target (0, 0); its b and c inputs are 0.

The program keeps only the message words `x, y` from each inverted call, plus
the column `A` and `D` outputs that later inversions read. A column `B` or `C`
output equals the target passed into Lemma 2, so the program passes that
target through. A diagonal `B` output is not an input of any later call in a
one-round hash, so the program does not compute it. Sections 5 and 6 are
proofs about the forward hash; they are not extra program steps.

The sixteen little-endian words of M and of M' produced by this program are

    M  = b100ae1e aa9106b2 639ac88c 6b02eec6 8a471637 b8f8d085 d6aef448 d1c279e0
         8d754531 5be0cd19 89e6df1e 510e527f c5c7e39b 9b05688c 36d9f5da 1f83d9ab
    M' = 60bcafce 4a77adac 639ac88c 6b02eec6 8a471637 b8f8d085 1abc0c41 fe9271cf
         09603fc0 8c32e9d9 8c776a67 4e7dc736 0048cff1 64fc9eba 020a64f5 1f83d9ab.

Columns 1 and 2 occupy `m2..m5` and agree. As 64-byte strings they are the
certificate files `certificates/message-a.bin` and `certificates/message-b.bin`.

## 5. Both digests are zero

Message M. Every column ends at `B = C = 0`, so every diagonal call has
`b = c = 0`. Each diagonal is Lemma 1 at `(0, 0)`. Identity Z says each
diagonal ends at `A = B = C = D = 0`. Every digest word in Section 3 is then
an XOR of zeros.

Message M'. Columns 1 and 2 end at `B = C = 0`, column 3 ends at `C = 0`, and
column 0 ends at `B = 0`. Therefore Gd1 and Gd3 have `b = c = 0` and target
`(0, 0)`. Identity Z says both end at `A = B = C = D = 0`, which forces

    h1 = h3 = h4 = h6 = 0.

Gd0 has `b = c = 0` and target `(C0, D0)`. Identity K says its `A` and `B`
outputs are the `A0` and `B0` of Section 4, and its `C` and `D` outputs are
`C0` and `D0`. Gd2 is aimed at target `(A0, B0)`, so

    h0 = A0 XOR A0 = 0
    h5 = B0 XOR B0 = 0.

It remains to check that Gd2's own `A` and `B` outputs equal `(C0, D0)`.
Apply Lemma 1 inside Gd2, whose `b` input is `L`, whose `c` input is `K`,
and whose target is `(Ct, Dt) = (A0, B0)`:

    c1    = A0 - B0 = diff
    d1    = diff - K
    A_out = d1 XOR ROL(B0, 8)
    b1    = ROR(L XOR diff, 12)
    B_out = ROR(b1 XOR A0, 7).

The definition of `K` is `K = diff - (C0 XOR ROL(B0, 8))`, so
`d1 = C0 XOR ROL(B0, 8)` and `A_out = C0`. The definition of `L` is
`L = ROL(A0 XOR ROL(D0, 7), 12) XOR diff`, so

    L XOR diff = ROL(A0 XOR ROL(D0, 7), 12)
    b1         = A0 XOR ROL(D0, 7)
    B_out      = ROR(ROL(D0, 7), 7) = D0.

Thus `h2 = C0 XOR C0 = 0` and `h7 = D0 XOR D0 = 0`. All eight digest words of
M' are zero.

The argument uses only the bijective rewrite of G, the one-round schedule, and
the digest XOR map. It holds for every `(C0, D0)`; the constants 2 and 5 are
the instance the program runs. No property of a random oracle, of other
rounds, or of a sampled distribution is used.

## 6. The messages differ

On column 0 both messages start from `(a, b, c, d) = (IV0, IV4, IV0, 0)` and
from `Bt = 0`. Message M uses `Ct = 0`. Lemma 2 then gives `b1 = 0` and
`c1 = b = IV4`. Message M' uses `Ct = K`. Lemma 2 then gives `b1 = K` and
`c1 = IV4 XOR ROL(K, 12)`. Section 4 shows `K = 0x04403B05`, which is not
zero. Rotation is a bijection, so `ROL(K, 12)` is not zero and the two values
of `c1` differ. Then `d1 = c1 - c` differs, `a1 = ROL(d1, 16)` differs
because `d = 0` and rotation is a bijection, and the first message word
`x = a1 - a - b` differs. The two 64-byte strings therefore differ.

Direct evaluation of that same column records the two first words
`0xB100AE1E` and `0x60BCAFCE`. The inequality already proved is the distinctness
argument; these two words are the concrete outputs.

## 7. Algorithm, probability, and advice

The algorithm is Sections 4's straight-line program. It has one execution
path. It draws no random word, stores no table, sorts nothing, and does not
call the compression function. It returns the two messages. The success event
is that those messages are distinct and have equal 32-byte digests. Sections 5
and 6 prove that this event occurs. The algorithmic success probability on
the fresh coins of this algorithm is 1. There is no failure branch to
restart and no amplification cost.

The program does not hash the messages in order to discover the collision.
The equalities are identities of the round function. The certificate files
repeat the program's output so the organizer can recompute both digests with
`verifier/blake3.py`. That recomputation is the organizer's check. It is not
a step of the algorithm, and it is not charged here. An independent run of
`blake3(message, 1)` on each certificate file returns 32 zero bytes.

`nonuniform_advice_log2_bytes = 0` is the schema's unit upper bound for an
empty advice string: at most one byte, with the actual advice length equal to
zero. The constants `C0` and `D0` are uniform program text. The messages are
the output of the charged program. No precomputed collision is supplied in
place of that program. There is no omitted search to charge.

The probability space is one deterministic execution of a fixed program on a
fixed target. It is not a confidence rating for the writeup.

## 8. Word-RAM cost

The model is the classical 256-bit word RAM of `collision-frontier-v5`. One
selected compression costs 1. Every other primitive costs `1/C`, where
`C = 222` is `reference_operation_costs.blake3-r1`. This algorithm performs
zero compressions. The reference script counts a 32-bit rotation as two
shifts, one OR, and one AND with `2^32-1`, because the 256-bit machine has no
native 32-bit rotate. The numerator uses that same expansion. A 32-bit sum or
difference is a 256-bit addition or subtraction followed by one mask, except
that a chain of two subtractions is masked once: for words already reduced
modulo 2^32, the low 32 bits of `((a - b) - c) mod 2^256` equal
`(a - b - c) mod 2^32`. XOR of two such words needs no further mask. Shift
distances and the constants IV, 0, 64, 11, `C0`, and `D0` are immediate
operands, not memory loads. Assigning a name to a value already in hand is
not a primitive.

Per Lemma 2 call, counting only values the program retains:

    ROL(Bt, 7)                         4
    XOR with Ct                        1
    ROL(b1, 12)                        4
    XOR with b                         1
    d1 = c1 - c, masked                2
    D  = Ct - c1, masked               2
    ROL(d1, 16)                        4
    XOR with d                         1
    x  = a1 - a - b, masked once       3
    ROL(D, 8)                          4
    XOR with d1                        1
    y  = A - a1 - b1, masked once      3

That is 30 primitives. The program executes it six times: four columns of M
and the two columns of M' that differ. Columns 1 and 2 are computed once and
used in both messages. Subtotal 180.

Per Lemma 1 call, again omitting the unused diagonal `B`:

    c1 = Ct - Dt, masked               2
    d1 = c1 - c, masked                2
    ROL(d1, 16)                        4
    XOR with d                         1
    x  = a1 - a - b, masked once       3
    XOR of b and c1                    1
    ROR by 12                          4
    ROL(Dt, 8)                         4
    XOR with d1                        1
    y  = A - a1 - b1, masked once      3

That is 25 primitives. Eight diagonal calls cost 200.

The closure that produces `A0`, `B0`, `K`, and `L` is

    one masked subtraction             2
    ROL(D0, 8) and one XOR             5
    one ROR by 12                      4
    one XOR and one ROR by 7           5
    one masked subtraction             2
    one ROL, one XOR, one masked sub   7
    one ROL and one XOR                5
    one ROL and one XOR                5

That is 35 primitives.

Each message is 16 lanes of 32 bits, 512 bits, hence two 256-bit words. The
program packs each word by placing lane 0 in the low 32 bits and combining
lanes 1..7 with a shift by `32, 64, ..., 224` and an OR. The lane invariant is
that every live lane lies in `0 .. 2^32-1` and already occupies the low 32
bits, which holds for the IV immediates, for `K` and `L`, and for every
masked arithmetic result and every expanded rotation. Shifts by multiples of
32 therefore land in disjoint lanes and need no extra mask. Four output words
cost `4 * (7 + 7) = 56` packing primitives and 4 stores.

| Block | Times | Each | Total |
| --- | ---: | ---: | ---: |
| Closure | 1 | 35 | 35 |
| Lemma 2 columns | 6 | 30 | 180 |
| Lemma 1 diagonals | 8 | 25 | 200 |
| Packing | 4 | 14 | 56 |
| Stores | 4 | 1 | 4 |
| Total W | | | 475 |

The primitive mix is 87 subtractions, 113 masks, 136 shifts, 82 ORs, 53 XORs,
and 4 stores, which sums to 475. Then

    T = W / C = 475 / 222 = 2.1396... < 2^1.30,

because `2^1.30 > 2.46` and `2.46 * 222 = 546.12 > 475`. The submitted
`time_log2` is this upper bound, 1.30. The inequality still holds if a
reconstruction adds the 71 further primitives that fit under 546. The program
specified above does not perform those extra operations.

`preprocessing_log2 = 10` means the setup performs fewer than `2^10 = 1024`
word primitives. The entire algorithm is that setup: 475 is less than 1024.
Those primitives are already the whole of `W`. They are not added a second
time. There is no per-message trial loop beyond the one construction.

## 9. Memory

Live values are the IV immediates, fewer than 64 intermediate 256-bit words,
and the two 64-byte messages. Sixty-four words occupy 2048 bytes. Charging a
generous 32 bytes of code per primitive for 475 primitives accounts for under
16 KiB of straight-line code, and the certificate buffers are 128 bytes. The
peak, including code, constants, working state, and the returned messages, is
under `2^20` bytes. `memory_log2_bytes = 20`. No table, sampled message, or
advice string is retained. Parallelism is not used; the bound is total work.

## 10. Scope

The construction uses one round. The message permutation and a second round
are outside this claim. The nominal reference 128 and the current promoted
figure are display or leaderboard facts; neither is an assumption of the
proof. The certificate is one witness of the program's output. The proof of
Sections 5 and 6 is the reason every execution succeeds.
