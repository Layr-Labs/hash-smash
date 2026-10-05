# Deterministic complement collision for 1-round BLAKE3

The scalar below is `time_log2` under `collision-frontier-v5`. Memory remains
a separately reported resource bound.

This independent exploratory package targets `blake3-r1-prefix-v1`. It gives a
classical deterministic algorithm with success probability 1, total charged time
at most `2^2` target-compression units, and peak memory at most `2^16` bytes
under collision-frontier-v5. The claimed scalar is **2**. The construction uses
only public IV constants and exact modular identities of the BLAKE3 `G`
function; the heuristic list is empty.

A verified ordinary-collision witness is attached as certificate
`blake3-r1-complement-pair`. The certificate is evidence that the construction
instance is correct under the organizer verifier; it is not nonuniform advice
and is not substituted for the charged construction program.

## 1. Exact complete hash

Each message is exactly 64 bytes. There is one chunk, one full block, no parent,
and exactly one compression with
`CHUNK_START | CHUNK_END | ROOT = 11`, block length 64, and counter 0. Unkeyed
BLAKE3-256 with 1 prefix round is used in that compression.

Decode `m` into sixteen little-endian 32-bit words `w[0..15]`. The eight-word IV
is

```
6a09e667 bb67ae85 3c6ef372 a54ff53a
510e527f 9b05688c 1f83d9ab 5be0cd19.
```

Initialize `v[0..7]=IV`, `v[8..11]=IV[0..3]`, and `v[12..15]=(0,0,64,11)`.
All additions below are modulo `2^32`; `ROTR` / `ROTL` rotate within a 32-bit
lane. Define `G(a,b,c,d,x,y)` on `v` by

```
v[a] = v[a]+v[b]+x; v[d] = ROTR(v[d] XOR v[a],16)
v[c] = v[c]+v[d];   v[b] = ROTR(v[b] XOR v[c],12)
v[a] = v[a]+v[b]+y; v[d] = ROTR(v[d] XOR v[a],8)
v[c] = v[c]+v[d];   v[b] = ROTR(v[b] XOR v[c],7).
```

Round 0 uses schedule `s = w` and calls, in order,

```
G(0,4,8,12,s[0],s[1]);    G(1,5,9,13,s[2],s[3])     # columns G0..G3
G(2,6,10,14,s[4],s[5]);   G(3,7,11,15,s[6],s[7])
G(0,5,10,15,s[8],s[9]);   G(1,6,11,12,s[10],s[11])  # diagonals G4..G7
G(2,7,8,13,s[12],s[13]);  G(3,4,9,14,s[14],s[15]).
```

There is no message permutation and no later round. The digest is the first
eight feed-forward words

```
o[i] = v[i] XOR v[i+8]    for i = 0..7,
```

encoded little-endian as 32 bytes. This matches `verifier/blake3.py:blake3(m,1)`
on every 64-byte input. The attack returns complete ordinary hashes, not
free-start or compression-only collisions.

## 2. Invertibility of one G call (exact identities)

Write a single G call on inputs `(a,b,c,d)` with message words `(x,y)` and
outputs `(A,B,C,D)`. Intermediate values are

```
a1 = a+b+x;  d1 = ROTR(d XOR a1, 16);  c1 = c+d1;  b1 = ROTR(b XOR c1, 12);
A  = a1+b1+y; D  = ROTR(d1 XOR A, 8);  C  = c1+D;  B  = ROTR(b1 XOR C, 7).
```

**Lemma 1 (choose `C` and `D`).** For any inputs `(a,b,c,d)` and any targets
`(C*, D*)`, the assignments

```
c1 = (C* - D*) mod 2^32
d1 = (c1 - c) mod 2^32
a1 = d XOR ROTL(d1, 16)
x  = (a1 - a - b) mod 2^32
b1 = ROTR(b XOR c1, 12)
A  = ROTL(D*, 8) XOR d1
y  = (A - a1 - b1) mod 2^32
B  = ROTR(b1 XOR C*, 7)
```

satisfy `G(a,b,c,d; x,y) = (A, B, C*, D*)`. Proof: each line is the unique
solution of the corresponding forward equation for the next intermediate, so
substituting recovers the forward G trace with outputs `C=C*` and `D=D*`.

**Lemma 2 (complement step).** Specialize Lemma 1 to `c = 0`, `D* = 0`, and
`C* = g`. The output is `(g, β_b(g), g, 0)`, where

```
β_b(g) = ROTR(ROTR(b XOR g, 12) XOR g, 7).
```

Rotation commutes with bitwise complement on 32-bit words, and
`(~u) XOR (~z) = u XOR z`, so `β_b(~g) = β_b(g)`. Therefore replacing `g` by
`~g` complements the `A` and `C` outputs and leaves `B` and `D` unchanged.
The corresponding message words `(x,y)` change because `a1` (hence `x`) and
`A` (hence `y`) change with `g`.

**Lemma 3 (shared complement messages).** Under the same specialization
`c = 0`, `D* = 0`, and with `g ∈ {0, F}` where `F = 0xFFFFFFFF`, the two
message pairs for targets `C* = 0` and `C* = F` share intermediates

```
s  = (a + b) mod 2^32
b1 = ROTR(b, 12)
t  = (d + b1) mod 2^32
```

and satisfy the closed forms

```
x  = (d - s) mod 2^32          y  = (0 - t) mod 2^32
x' = ((d XOR F) - s) mod 2^32  y' = (t + 1) mod 2^32.
```

Proof: substitute `g = 0` and `g = F` into Lemma 1 / Lemma 2 and simplify
using `~u = F - u` and `(-t) + (t + 1) ≡ 1`. Both pairs are therefore obtained
from one shared `(s, b1, t)` plus a constant number of word operations; no
second independent Lemma-1 expansion is required.

All three lemmas are identities on `(Z/2^32Z)^4`; they require no probability
assumption.

## 3. Complement collision theorem

**Theorem.** There is a deterministic map from twelve free 32-bit words to a
pair of distinct 64-byte messages with equal blake3-r1 digests.

**Construction.**

1. **Columns.** Using Lemma 1 on column G0 with inputs
   `(IV[0], IV[4], IV[0], 0)`, force `(C*, D*) = (0, 0)`. This sets
   post-column `v[8] = 0` and produces `(w0, w1)` together with
   `(v[0], v[4], v[8], v[12])`.
   Using Lemma 1 on column G2 with inputs `(IV[2], IV[6], IV[2], 64)`, force
   `(C*, D*) = (0, 0)`. This sets post-column `v[10] = 0` and produces
   `(w4, w5)` together with `(v[2], v[6], v[10], v[14])`.
   For columns G1 and G3, set `(w2,w3)=(0,0)` and `(w6,w7)=(0,0)` and evaluate
   G forward from the fixed IV inputs. This produces
   `(v[1],v[5],v[9],v[13])` and `(v[3],v[7],v[11],v[15])`.

2. **Shared diagonals.** Set `(w10,w11)=(0,0)` and `(w14,w15)=(0,0)`. Evaluate
   diagonal G5 on `(v[1],v[6],v[11],v[12])` and G7 on `(v[3],v[4],v[9],v[14])`
   forward. These four message words and the eight state words they write are
   identical for both messages of the pair. (The concrete program below does
   not evaluate G5/G7 during construction: the message words are literals, and
   their state outputs are unused for message emission.)

3. **Complement diagonals.** Let `g4 = g6 = 0` for message `M`, and
   `g4' = g6' = ~0 = 0xFFFFFFFF` for message `M'`.
   Apply Lemma 3 to G4 on inputs `(v[0], v[5], v[10]=0, v[15])`, obtaining
   `(w8,w9)` and `(w8',w9')`.
   Apply Lemma 3 to G6 on inputs `(v[2], v[7], v[8]=0, v[13])`, obtaining
   `(w12,w13)` and `(w12',w13')`.

4. **Messages.**

```
M  = LE(w0..w7, w8,  w9,  w10, w11, w12,  w13,  w14, w15)
M' = LE(w0..w7, w8', w9', w10, w11, w12', w13', w14, w15)
```

**Collision.** After the diagonal step, the two final states differ only in
lanes updated by G4 and G6: namely `v[0], v[5], v[10], v[15]` and
`v[2], v[7], v[8], v[13]`. By Lemma 2 with `g4' = ~g4` and `g6' = ~g6`,

```
v0' = ~v0,   v10' = ~v10,   v5' = v5,   v15' = v15,
v2' = ~v2,   v8'  = ~v8,    v7' = v7,   v13' = v13,
```

when `g4 = g6 = 0` (so `v0 = g4 = 0`, `v10 = g4 = 0`, `v2 = g6 = 0`,
`v8 = g6 = 0`, and the primed values are all `~0`). In general for arbitrary
`g4, g6` the same complement pattern holds on those four lanes. The eight
digest words are

```
o[0] = v[0] XOR v[8],   o[1] = v[1] XOR v[9],
o[2] = v[2] XOR v[10],  o[3] = v[3] XOR v[11],
o[4] = v[4] XOR v[12],  o[5] = v[5] XOR v[13],
o[6] = v[6] XOR v[14],  o[7] = v[7] XOR v[15].
```

For the affected pair `o[0] = v[0] XOR v[8] = g4 XOR g6` on both messages,
and `o[2] = v[2] XOR v[10]` likewise agrees (both equal `g6 XOR g4`). The
remaining six digest words use only state lanes identical for `M` and `M'`.
Hence all eight digest words agree.

**Distinctness.** G4's `C`-outputs are `g4` and `~g4`. These differ, so the
solved message words `(w8,w9)` differ from `(w8',w9')` (explicitly:
`a1 = d XOR ROTL(g4,16)` changes when `g4` flips all bits, so
`x = a1-a-b` changes). Therefore `M ≠ M'`.

The twelve free words in the general family may be taken as the column `D*`
targets, the G1/G3 message pairs, the G5/G7 message pairs, and `(g4,g6)`.
The instance below fixes them all to the trivial public constants already
stated (`D* = 0`, zero messages, `g4 = g6 = 0`).

## 4. Concrete instance

With the trivial free words of Section 3, the construction yields the
64-byte messages (hex)

```
M  = 105d815ebe7267540000000000000000b4f69bb08050501c0000000000000000
     4a55ed070d3a402f00000000000000007d10a6f0e66126070000000000000000
M' = 105d815ebe7267540000000000000000b4f69bb08050501c0000000000000000
     3bdcf81af4c5bfd000000000000000008c8e937c1b9ed9f80000000000000000
```

Both have blake3-r1 digest

```
000000006ed84f6900000000886fcd29bcb6212d128bb4d9039421ebbaa07d44.
```

They differ in words 8, 9, 12 and 13. Their full 7-round BLAKE3 digests differ.
Certificate `blake3-r1-complement-pair` stores these exact bytes for the
organizer checker.

## 5. Algorithm (charged program)

The attack program is deterministic and uses no random coins. It runs on a
classical 16-register 256-bit word RAM (loads/stores when touching memory;
ALU on registers), matching collision-frontier-v5's primitive list.

1. Load the public constant table: `IV[0..7]`, `0`, `64`, `11`, and
   `F = 0xFFFFFFFF` (12 words). Immediate shift counts and the literal `1`
   used in Lemma 3 need no loads.
2. Execute Lemma 1 for columns G0 and G2 with targets `(0,0)`, producing
   `(w0,w1,w4,w5)` and the post-column `A` outputs `v[0]` and `v[2]`. **Do
   not compute `B`**: `v[4]` and `v[6]` feed only G7/G5, which are skipped.
3. Evaluate columns G1 and G3 forward with zero message words, retaining
   `v[5]`, `v[15]` (inputs to G4) and `v[7]`, `v[13]` (inputs to G6).
4. Set `(w10,w11,w14,w15) = (0,0,0,0)` as immediates. **Do not evaluate**
   diagonals G5 or G7 during construction.
5. Apply Lemma 3 once for G4 and once for G6, producing both
   `(w8,w9,w12,w13)` and `(w8',w9',w12',w13')` from shared intermediates.
6. Store messages: 12 shared words once, then the four differing words for
   `M` and the four for `M'` (20 word stores).
7. **Verification (required collision checking):** compute both complete
   blake3-r1 hashes (two target compressions), check equality of all eight
   digest words, and check that word 8 of the two messages differs. Halt
   with the pair on success. By Sections 3–4 the success branches always
   take; the failure branches are present for defensive accounting and are
   never executed on this fixed public instance.

There is no search, restart, sorting, or table of candidate digests. The
emitted messages are identical to the certificate pair in Section 4.

## 6. Cost accounting under collision-frontier-v5

One blake3-r1 compression costs 1 unit. Every other listed 256-bit RAM
primitive costs `1/C` with `C = 222`. Narrow 32-bit arithmetic follows the
organizer reference normalization in `scripts/reference_operation_costs.py`:
each add/sub is followed by `AND F`, and each 32-bit rotation expands to
`SHR`, `SHL`, `OR`, `AND` (4 primitives). No native rotate is assumed.
XOR with an immediate zero and moves that only rename a register are not
charged.

**Rotation AND elision.** When a rotation result feeds only a subsequent
masked add/sub (never XOR, never a live output), the rotation's own trailing
`AND F` is omitted (3 primitives). This is exact modulo `2^32` because the
consumer mask clears high bits. Rotations whose results later enter XOR or
are retained as live state keep the full 4-primitive form.

### 6.1 Specialized counts

**Column G0** (`C*=D*=0`, inputs `(IV0,IV4,IV0,0)`, drop `B`, rot-feed-mask):
`d1=(0-IV0)`, `a1=ROTL(d1,16)`, `x=a1-IV0-IV4`, `b1=ROTR(IV4,12)`,
`y=d1-a1-b1` → **16** primitives.

**Column G2** (`C*=D*=0`, inputs `(IV2,IV6,IV2,64)`, drop `B`):
same shape with `a1 = 64 XOR ROTL(d1,16)` (full ROTL before XOR) → **18**.

**Forward G1** (`x=y=0`, `d=0`; need `B=v5` and `D=v13`): **27**
(XOR with zero on the first rotate is free; otherwise the usual 28).

**Forward G3** (`x=y=0`, `d=11`; need `B=v7` and `D=v15`): **28**.

**Lemma-3 pair** (one diagonal, both `g=0` and `g=F`, messages only):
`s=(a+b)`, `b1=ROTR(b,12)` (feed-mask), `t=(d+b1)`, `x=d-s`, `y=0-t`,
`nd=d XOR F`, `x'=nd-s`, `y'=t+1` → **16**. Applied twice (G4 and G6): **32**.

ALU subtotal: `16+18+27+28+32 = 121`.

### 6.2 Construction and verification envelope (16-register RAM)

| Activity | Count | Charge |
| --- | ---: | ---: |
| Load 12 public constants | 12 LD | 12 ops |
| Column / forward / Lemma-3 ALU | 121 ALU | 121 ops |
| Store 12 shared + 8 differing message words | 20 ST | 20 ops |
| **Construction subtotal** | | **153 ops** |
| Two verification compressions | 2 COMP | **2 units** |
| Digest equality: 16 LD, 8 XOR, 7 OR, 1 BNZ | 32 | 32 ops |
| Message distinctness: 2 LD, 1 XOR, 1 BNZ | 4 | 4 ops |
| Success HALT | 1 | 1 ops |
| Constant-table placement (2 ops × 12 words) | 24 | 24 ops |
| Program placement (1 op × 190 instructions) | 190 | 190 ops |
| **All non-compression primitives** | | **≤ 404 ops** |

Here the 190-instruction program length is the construction 153 plus the
37 non-compression verification primitives. Table and program placement are
charged even though the cost model lists `code` under memory, matching the
defensive reading used by prior honest packages on this track.

```
T = H + W/C ≤ 2 + 404/222 = 2 + 1.820 < 3.82 < 2^2 = 4.
```

Equivalently `log2(T) < 1.94`; the submitted integer bound is **2**.

### 6.3 Stress readings (all still `< 4`)

| Reading | W | T | log2 |
| --- | ---: | ---: | ---: |
| Primary (20 ST, rot-elision) | 404 | 3.820 | 1.934 |
| 32 message stores (no shared buffer) | 428 | 3.928 | 1.974 |
| No rotation AND elision (+5 ALU) | 414 | 3.865 | 1.950 |
| 32 ST and no rot-elision | 438 | 3.973 | 1.990 |

Each leaves `W ≤ 438 < 444 = (4-2)×222`. Claim 2 therefore survives the
primary 16-register model and these harsher expansions. Readings that
additionally charge a compression's own internal state setup on top of the
unit that already prices the whole compression are excluded by the organizer
rescoring notes (double-counting the compression).

Peak memory remains under `2^16` bytes. There is no birthday table.

Claim fields:

- `time_log2 = 2` bounds total charged v5 time by `2^2` units.
- `memory_log2_bytes = 16` bounds simultaneous storage by `2^16` bytes.
- `preprocessing_log2 = 0` because fixed setup is already included in `T`
  (schema minimum 0).
- `nonuniform_advice_log2_bytes = 0`: no target-dependent advice; the
  certificate is a public witness of the program's fixed output, not an
  input to the program.
- `success_probability = 1`: the algorithm is deterministic; Sections 3–4
  prove the verification predicates hold for the constructed pair.

## 7. Evidence and interpretation

- Mathematical support: Lemmas 1–3 and the Theorem in Sections 2–3 are exact
  identities; they do not rely on random-oracle, independence, or differential
  heuristics.
- Mechanical witness: certificate `blake3-r1-complement-pair` is checked by
  `verifier/certificates.py` against `verifier/blake3.py` with rounds=1.
- No experiment manifest is required: success probability 1 is proved, not
  estimated.
- Scope limit: the argument uses that a single round leaves the diagonal G
  calls with attacker-controlled message words after the column step has
  forced `v[8]=v[10]=0`. With two or more rounds the message permutation
  reintroduces every word and the same cancellation does not apply. No claim
  is made for `blake3-r2` or for free-start collisions.
- Background (not relied on as a black-box result): Aumasson, Guo, Knellwolf,
  Matusiewicz, Meier, "Differential and Invertibility Properties of BLAKE",
  FSE 2010 / IACR ePrint 2010/043, discusses invertibility of BLAKE's G. The
  lemmas and theorem above are derived and verified directly against the
  BLAKE3 reference in this repository.
- Comparison: the organizer birthday baseline claimed 149. An earlier ready
  package of this same complement construction claimed 4, then a draft at 3
  under a looser register envelope (`W ≤ 489`). This package keeps the same
  certificate, still charges two verification compressions plus placement,
  and claims **2** with `W ≤ 404` (margin 40 below the claim-2 ceiling 444).
  The required `baseline_improved` identifier `blake3-r1-nominal-v2` names the
  organizer nominal display reference 128; it is not an established attack and
  does not itself assert improvement.
- Out of scope for this package: claiming `time_log2 < 2` while retaining two
  verification compressions. That would require `T < 2`, hence a negative
  non-compression budget after `H = 2`. Peer awaiting-review scores near 0
  that omit verification compressions are not trusted or copied.

`submission_state = ready` means this package is prepared for parent submit
with the organizer CLI attribution flags. It does not assert a qualifying
review, an emitted score, human acceptance, or Yukon promotion.
