# Deterministic complement collision for 1-round BLAKE3 (B-vanishing columns)

The scalar below is `time_log2` under `collision-frontier-v5`. Memory remains
a separately reported resource bound.

This exploratory package targets `blake3-r1-prefix-v1`. It gives a classical
deterministic algorithm with success probability 1, total charged time at most
`2^1.85` target-compression units, and peak memory at most `2^16` bytes. The
construction uses only public IV constants and exact modular identities of the
BLAKE3 `G` function; the heuristic list is empty.

## 0. Ledger at a glance (for reviewers)

```
T  = H + W / C,      H = 2 verification compressions,   C = 222 (blake3-r1)
P  = LD + ALU + ST + V            (straight-line program length, instructions)
W  = P            (execute every instruction once)
   + P            (program placement: 1 op per instruction)
   + 2·LD         (constant-table placement: 2 ops per table word)
   = 2·(LD + ALU + ST + V) + 2·LD
V  = 37           (digest EQ 32 + distinctness 4 + HALT 1)
LD = 9            (IV[0..7] and F = 0xFFFFFFFF)
```

| Row | ALU | ST | P | W | T | log2 T |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Primary program (Section 5) | 75 | 20 | 141 | 300 | 3.351 | 1.745 |
| Harshest stress (full mask, full rotates, 32 ST) | 87 | 32 | 165 | **348** | 3.568 | **1.835** |
| Claim-1.85 ceiling `(2^1.85 − 2)·222` | | | | 356.31 | 3.605 | 1.85 |

The claimed scalar **1.85** is sized to the **maximum** of the full stress
lattice (Section 6.3), not to the primary stream: `348 ≤ 356` (margin 8 ops).
Both verification compressions and all placement are inside `T`.

**Skeptic-review card (what this claim charges).** Ledger identity
`W = 2(LD+ALU+ST+V)+2LD` with `LD=9`, `V=37`, `H=2`, `C=222`. Primary stream
`ALU=75`, `ST=20` ⇒ `W=300`. Full `{chain, elide, ST∈{20,32}}` lattice max
`ALU=87`, `ST=32` ⇒ `W=348`. Claim `1.85` covers that max (`348 ≤ 356.31`);
it is not an as-run reading of the primary alone. Certificate is a witness of
the Section 4 instance, not advice. Omit-verify (`H=0`), memory-only placement,
and native 1-op narrow ROT are rejected (Section 6.4).

Reading chain: Lemmas 1–5 (exact identities) → Theorem (collision family) →
concrete instance (Section 4) → charged RAM program (Section 5) → cost lattice
(Section 6). Certificate `blake3-r1-complement-pair` is a mechanical witness of
the Section 4 instance, not advice and not a substitute for charged checking.

## 1. Exact complete hash

Each message is exactly 64 bytes. There is one chunk, one full block, no
parent, and exactly one compression with `CHUNK_START | CHUNK_END | ROOT = 11`,
block length 64, and counter 0. Unkeyed BLAKE3-256 with 1 prefix round is used
in that compression.

Decode `m` into sixteen little-endian 32-bit words `w[0..15]`. The IV is

```
6a09e667 bb67ae85 3c6ef372 a54ff53a
510e527f 9b05688c 1f83d9ab 5be0cd19.
```

Initialize `v[0..7]=IV`, `v[8..11]=IV[0..3]`, `v[12..15]=(0,0,64,11)`. All
additions are modulo `2^32`; `ROTR`/`ROTL` rotate a 32-bit lane.
`G(a,b,c,d,x,y)` is

```
v[a] = v[a]+v[b]+x; v[d] = ROTR(v[d] XOR v[a],16)
v[c] = v[c]+v[d];   v[b] = ROTR(v[b] XOR v[c],12)
v[a] = v[a]+v[b]+y; v[d] = ROTR(v[d] XOR v[a],8)
v[c] = v[c]+v[d];   v[b] = ROTR(v[b] XOR v[c],7).
```

Round 0 uses schedule `s = w`:

```
G(0,4,8,12,s[0],s[1]);    G(1,5,9,13,s[2],s[3])     # columns G0..G3
G(2,6,10,14,s[4],s[5]);   G(3,7,11,15,s[6],s[7])
G(0,5,10,15,s[8],s[9]);   G(1,6,11,12,s[10],s[11])  # diagonals G4..G7
G(2,7,8,13,s[12],s[13]);  G(3,4,9,14,s[14],s[15]).
```

There is no message permutation and no later round. The digest is
`o[i] = v[i] XOR v[i+8]` for `i = 0..7`, little-endian, 32 bytes. This matches
`verifier/blake3.py:blake3(m,1)` on every 64-byte input. The attack returns
complete ordinary hashes, not free-start or compression-only collisions.

## 2. Exact identities for one G call

For a G call on inputs `(a,b,c,d)` with message words `(x,y)` and outputs
`(A,B,C,D)`:

```
a1 = a+b+x;  d1 = ROTR(d XOR a1,16);  c1 = c+d1;  b1 = ROTR(b XOR c1,12);
A  = a1+b1+y; D = ROTR(d1 XOR A,8);   C  = c1+D;  B  = ROTR(b1 XOR C,7).
```

**Lemma 1 (choose `C`, `D`).** For any inputs and targets `(C*,D*)`:
`c1 = C*−D*`, `d1 = c1−c`, `a1 = d XOR ROTL(d1,16)`, `x = a1−a−b`,
`b1 = ROTR(b XOR c1,12)`, `A = ROTL(D*,8) XOR d1`, `y = A−a1−b1`,
`B = ROTR(b1 XOR C*,7)` give `G(a,b,c,d;x,y) = (A,B,C*,D*)`. Each line is the
unique solution of the corresponding forward equation.

**Lemma 2 (complement step; any `b`, `d`).** Take `c = 0`, `D* = 0`,
`C* = g`. Then `c1 = d1 = A = g`, and the outputs are
`(g, β_b(g), g, 0)` with `β_b(g) = ROTR(ROTR(b XOR g,12) XOR g, 7)`.
Rotation commutes with complement and `(~u) XOR (~z) = u XOR z`, so
`β_b(~g) = β_b(g)`: replacing `g` by `~g` complements `A` and `C` and leaves
`B` and `D` unchanged. (`d` affects only `a1`, hence the message words.)

**Lemma 3 (both complement messages in closed form).** Under Lemma 2 with
`g = 0` (message `M`) and `g = F = 0xFFFFFFFF` (message `M'`), put
`s = a+b`, `t = d + ROTR(b,12)`. Then

```
x = d − s        y  = −t
x' = ~(d + s)    y' = t + 1.
```

Proof. For `g = 0`: `a1 = d`, `b1 = ROTR(b,12)`, `x = d−s`, `y = 0−d−b1 = −t`.
For `g = F`: `a1' = d XOR F = ~d`, `b1' = ROTR(~b,12) = ~b1`,
`x' = ~d − s = (F−d) − s = ~(d+s)`, and
`y' = F − ~d − ~b1 = F − (F−d) − (F−b1) = d + b1 − F = t + 1 (mod 2^32)`.

**Corollary 3b (`b = 0`).** If `b = 0` then `s = a`, `t = d`:
`x = d−a`, `x' = (d+a) XOR F`, `y = −d`, `y' = d+1 = (d − F) mod 2^32`.
If moreover `d = −k` for a loaded public word `k`, then `y = k` needs no
instruction.

**Lemma 4 (zero-`a1` column, `d = 0`).** Set `x = −(a+b)`. Then `a1 = 0`,
`d1 = ROTR(0,16) = 0`, `c1 = c`, `b1 = β := ROTR(b XOR c,12)`. For any `D*`,
`A = ROTL(D*,8)`, `y = A − β`, and the outputs are
`(A, ROTR(β XOR (c+D*),7), c+D*, D*)`. Two specializations:

- **4a (`C = 0`).** `D* = −c`: outputs `(ROTL(−c,8), ·, 0, −c)`.
- **4b (`B = 0`).** `D* = β − c`: then `C = β` and `B = ROTR(β XOR β,7) = 0`;
  outputs `(ROTL(β−c,8), 0, β, β−c)`.

**Lemma 5 (`B`-vanishing column, any `d`).** Take Lemma 1 with
`(C*,D*) = (0, −b)`. Then `c1 = b`, `b1 = ROTR(b XOR b,12) = 0`,
`B = ROTR(0 XOR 0,7) = 0`, and with `d1 = b−c`, `a1 = d XOR ROTL(d1,16)`:
`x = a1−a−b`, `A = ROTL(−b,8) XOR d1`, `y = A − a1`; outputs `(A, 0, 0, −b)`.

All lemmas are identities on `(Z/2^32Z)^4`; no probability assumption is used.

## 3. Complement collision theorem

**Theorem.** The construction below maps public IV constants to two distinct
64-byte messages with equal blake3-r1 digests.

1. **Columns.**
   - G0, inputs `(IV0, IV4, IV0, 0)`: Lemma 4a. Post-column
     `v0 = ROTL(−IV0,8)`, `v8 = 0`, `v12 = −IV0`.
   - G2, inputs `(IV2, IV6, IV2, 64)`: Lemma 1 with `(C*,D*) = (0,0)`.
     `v2 = d1 = −IV2`, `v10 = 0`, `v14 = 0`.
   - G1, inputs `(IV1, IV5, IV1, 0)`: Lemma 4b. `v5 = 0`, `v9 = β1`,
     `v13 = D1 := β1 − IV1` with `β1 = ROTR(IV5 XOR IV1, 12)`.
   - G3, inputs `(IV3, IV7, IV3, 11)`: Lemma 5. `v7 = 0`, `v11 = 0`,
     `v15 = −IV7`.
2. **Shared diagonals.** `(w10,w11,w14,w15) = (0,0,0,0)` for both messages.
   G5 on lanes `(1,6,11,12)` and G7 on `(3,4,9,14)` read only lanes untouched
   by G4/G6 and use identical message words, so their outputs are identical
   for `M` and `M'`. (The program does not evaluate them during construction.)
3. **Complement diagonals.** G4 has inputs `(v0, v5=0, v10=0, v15=−IV7)` and G6
   has `(v2, v7=0, v8=0, v13=D1)`, so both satisfy Lemma 2 (`c = 0`) with
   `b = 0`. Corollary 3b with `g = 0` for `M` and `g = F` for `M'` gives

   ```
   w8  = −IV7 − v0       w8'  = (−IV7 + v0) XOR F     w9 = IV7   w9'  = 1 − IV7
   w12 = D1 − v2         w12' = (D1 + v2) XOR F       w13 = −D1  w13' = D1 + 1
   ```
4. **Messages.** `M = LE(w0..w7, w8, w9, 0, 0, w12, w13, 0, 0)` and
   `M' = LE(w0..w7, w8', w9', 0, 0, w12', w13', 0, 0)`.

**Collision.** The final states differ only in lanes written by G4/G6. By
Lemma 2, `v0, v10` (G4 `A`, `C`) and `v2, v8` (G6 `A`, `C`) are complemented
and `v5, v15, v7, v13` (the `B`, `D` outputs) are unchanged. Hence
`o0 = v0 XOR v8 = g4 XOR g6` and `o2 = v2 XOR v10 = g6 XOR g4` agree on both
messages (`~g4 XOR ~g6 = g4 XOR g6`), and the other six digest words use only
lanes identical for `M` and `M'`.

**Distinctness.** `w8 = d−a` and `w8' = ~(d+a)` with `d = −IV7`, `a = v0`.
Equality would force `d − a ≡ −d − a − 1`, i.e. `2d ≡ −1 (mod 2^32)`, which has
no solution (left side even, right side odd). So `M ≠ M'` for every IV.

**Why this beats the previous instance.** The earlier package (same diagonal
complement, filed at 1.9) forced `D = 0` on G1/G3, leaving
`b = ROTR(IV,7) ≠ 0` in the diagonals; each diagonal then needed a masked
`a+b` and a fresh rotate `ROTR(IV,19)`. Here G1/G3 force `B = 0` instead
(Lemmas 4b and 5), so the diagonal `b`-input vanishes and Corollary 3b needs
no rotation at all, while G0 uses the zero-`a1` column (Lemma 4a) that shares
`−IV0` between `w0` and `v0`. Every column still uses exactly two narrow
rotations. Within Lemma 1 a column skips the `a1` rotate only if `c1 = c`,
the `b1` rotate only if `c1 = b`, and the `A` rotate only if `D* = 0`; under
the required outputs (`C = 0`, or `B = 0`) these conditions are pairwise
incompatible for the IV inputs, so two rotations per column is the floor of
this parameterization.

## 4. Concrete instance

```
M  = 1ac7e7441ae995b4efe892a979a1c5c9b4f69bb08050501c48f4aed6e079c2d1
     529905ae19cde05b0000000000000000194b99e159a8d55a0000000000000000
M' = 1ac7e7441ae995b4efe892a979a1c5c9b4f69bb08050501c48f4aed6e079c2d1
     8333c765e8321fa40000000000000000ca9b4497a8572aa50000000000000000
```

Both have blake3-r1 digest

```
00000000fd12b1a600000000efa6e4d069871b2b00000000a13b329e00000000.
```

They differ only in words 8, 9, 12, 13; word 9 of `M` is `IV7 = 5be0cd19`.
Their full 7-round BLAKE3 digests differ. A forward trace of the reference
round gives post-column `v5 = v7 = v8 = v10 = v11 = v14 = 0`,
`v0 = f6199995 = ROTL(−IV0,8)`, `v2 = c3910c8e = −IV2`,
`v13 = a52a57a7 = D1`, `v15 = a41f32e7 = −IV7`, and final
`(v0, v2, v8, v10) = (0,0,0,0)` for `M` and `(F,F,F,F)` for `M'`; digest words
`o0, o2, o5, o7` are zero. Certificate `blake3-r1-complement-pair` stores
these exact bytes for the organizer checker.

## 5. Algorithm (charged program)

Deterministic straight-line program on the classical 16-register 256-bit word
RAM of collision-frontier-v5; no random coins, no search, no restarts.

1. Load `IV[0..7]` and `F` (9 LD). Immediates: shift counts and the target's
   own small parameters `11` (flags) and `64` (block length); `0` is the zero
   register (subtrahend base). No literal `1` is used (`d+1` is computed as
   `(d − F) AND F`).
2. Columns and diagonals, exactly as listed below (75 ALU in the primary
   reading; bracket = primary / full-mask stress primitive count).
3. Store the 12 shared and the 4+4 differing message words (20 ST).
4. **Verification (required collision checking).** Compute both complete
   blake3-r1 hashes (2 target compressions), compare all eight digest words
   (16 LD, 8 XOR, 7 OR, 1 BNZ), check word 8 differs (2 LD, 1 XOR, 1 BNZ),
   HALT (1). Total `V = 37` non-compression primitives. By Sections 3–4 the
   success branch always takes; the failure branch is still charged.

```
G0 [13/15]  n0  = (0 − IV0) & F                    [2/2]
            w0  = (n0 − IV4) & F                   [2/2]
            β0  = ROTR(IV4 XOR IV0, 12)            [1+3 / 1+4]
            v0  = ROTL(n0, 8)                      [3/4]
            w1  = (v0 − β0) & F                    [2/2]
G2 [15/19]  d1  = (0 − IV2) & F          (= v2)    [2/2]
            a1  = 64 XOR ROTL(d1, 16)              [1+3 / 1+4]
            w4  = (a1 − IV2 − IV6) & F             [3/4]
            b1  = ROTR(IV6, 12)                    [3/4]
            w5  = (d1 − a1 − b1) & F               [3/4]
G1 [14/17]  w2  = (0 − IV1 − IV5) & F              [3/4]
            β1  = ROTR(IV5 XOR IV1, 12)            [1+3 / 1+4]
            D1  = (β1 − IV1) & F         (= v13)   [2/2]
            A1  = ROTL(D1, 8)                      [3/4]
            w3  = (A1 − β1) & F                    [2/2]
G3 [17/20]  e1  = (IV7 − IV3) & F                  [2/2]
            a3  = 11 XOR ROTL(e1, 16)              [1+3 / 1+4]
            w6  = (a3 − IV3 − IV7) & F             [3/4]
            n7  = (0 − IV7) & F          (= v15)   [2/2]
            A3  = e1 XOR ROTL(n7, 8)               [1+3 / 1+4]
            w7  = (A3 − a3) & F                    [2/2]
G4 [7/7]    w8  = (n7 − v0) & F ;  w8' = ((n7 + v0) & F) XOR F   [2+3]
            w9  = IV7 (register) ;  w9' = (n7 − F) & F             [0+2]
G6 [9/9]    w12 = (D1 − v2) & F ;  w12' = ((D1 + v2) & F) XOR F  [2+3]
            w13 = (0 − D1) & F  ;  w13' = (D1 − F) & F            [2+2]
```

Executed in the listed order, with each message word stored as soon as it is
computed, at most 12 words are live at once (`F`, `v0`, `v2`, `D1`, `n7`,
`IV7` carried forward, plus the current column's operands and two rotate
temporaries), within the 16-register model; each IV word is loaded once.

The emitted messages equal the certificate pair. An independent emulation of
this exact instruction stream on 256-bit integers (with the stated masks and
elisions, asserting every rotate input is a clean 32-bit word) reproduces the
Section 4 bytes and tallies 13, 15, 14, 17, 7, 9 (primary) and
15, 19, 17, 20, 7, 9 (full mask), for every row of Section 6.3.

### 5.1 Why `H = 2` and the digest compare stay in charged time

collision-frontier-v5 lists **"collision checking"** under
`total_time_includes`, and its computation model says BLAKE3 **must charge all
chunk/parent/root compressions**. A 64-byte message is one root compression,
so the program's own check of both messages costs **two** units. The theorem
guarantees the check passes, which removes failed-trial amplification; it does
not price a named charged category at zero. This package therefore does **not**
use, and does not file a companion for, any omit-verify reading (`H = 0`,
claims at 0 / 0.1) of the same lemmas and witness.

### 5.2 Why placement stays in charged time

`code` under `memory_includes` puts code bytes in the memory report; it does
not remove program/table placement work from time (`"preprocessing"` is in
`total_time_includes`). We charge 1 op per program instruction and 2 ops per
constant-table word. Memory-only accounting of the code/table image is not
used.

### 5.3 Certificate = witness, not advice

The program computes the pair from `IV` alone; it never reads the
certificate. The certificate is the program's fixed public output, supplied so
the organizer verifier (`verifier/certificates.py` against
`verifier/blake3.py`, rounds = 1) can check it mechanically.
`nonuniform_advice_log2_bytes = 0`. No instance word (`w0..w15`, `D1`, `β1`,
…) is stored as a table constant: the table holds only `IV[0..7]` and `F`.

### 5.4 Deterministic closed form

Every instruction is a fixed modular identity from Lemmas 1–5; there is no
loop, branch on data (other than the charged, always-passing verification
branches), random coin, search, sort, or table lookup. Success probability is
exactly 1 for the fixed public target.

## 6. Cost accounting under collision-frontier-v5

One blake3-r1 compression = 1 unit; every other listed 256-bit RAM primitive
= `1/C`, `C = 222`. Narrow arithmetic follows the organizer normalization
(`scripts/reference_operation_costs.py`, `docs/RESCORING.md`): each narrow
add/sub is followed by `AND F`; each narrow rotation is `SHL, SHR, OR, AND`
(4 primitives). **No native 32-bit rotate is assumed** ("shift or rotation" is
not read as a 1-op narrow ROT).

Two exact-mod-`2^32` optimizations define the primary stream:

- **Chained masked sum.** `(p − q − r) AND F` as `SUB, SUB, AND` (3).
- **Rotation AND elision.** A rotation whose result (possibly after an XOR with
  a clean word) feeds only masked add/sub omits its own trailing `AND` (3).
  Every rotation *input* is a clean masked word (asserted in emulation).

### 6.1 Primary envelope

| Activity | Count | Charge |
| --- | ---: | ---: |
| Load `IV[0..7]`, `F` | 9 LD | 9 |
| Column / diagonal ALU (Section 5) | 75 | 75 |
| Message stores (12 shared + 8 differing) | 20 ST | 20 |
| Verification non-COMP (`V`) | 37 | 37 |
| **Program length `P`** | | **141** |
| Program placement (1 × `P`) | | 141 |
| Table placement (2 × 9) | | 18 |
| **`W` (all non-compression primitives)** | | **300** |
| Verification compressions | 2 COMP | **2 units** |

`T = 2 + 300/222 = 3.351`, `log2 T = 1.745`.

### 6.2 Claim ceiling

`time_log2 = 1.85` ⇔ `T ≤ 2^1.85 = 3.6050` ⇔ (with `H = 2`)
`W ≤ (2^1.85 − 2)·222 = 356.31`.

### 6.3 Full stress lattice (all charged claim rows)

Each skeptic refusal is applied independently and jointly; every row is a
costing of the same instruction stream and certificates. Refusing chaining
adds 4 ALU (G2 ×2, G1, G3); refusing elision adds 8 ALU (two rotates per
column); 32 ST stores both 16-word blocks with no shared buffer. Placement
grows with each added instruction.

| Chain | Elide | ST | ALU | P | W | T | log2 T | ≤ 356? |
| :---: | :---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: |
| yes | yes | 20 | 75 | 141 | 300 | 3.351 | 1.745 | yes |
| no | yes | 20 | 79 | 145 | 308 | 3.387 | 1.760 | yes |
| yes | no | 20 | 83 | 149 | 316 | 3.423 | 1.775 | yes |
| yes | yes | 32 | 75 | 153 | 324 | 3.459 | 1.791 | yes |
| no | no | 20 | 87 | 153 | 324 | 3.459 | 1.791 | yes |
| no | yes | 32 | 79 | 157 | 332 | 3.496 | 1.806 | yes |
| yes | no | 32 | 83 | 161 | 340 | 3.532 | 1.820 | yes |
| **no** | **no** | **32** | **87** | **165** | **348** | **3.568** | **1.835** | **yes** |

Maximum `W = 348 ≤ 356.31`: claim **1.85** holds on every row, margin 8 ops.
The scalar is not an as-run reading of the primary stream: the primary row
alone would fit 1.75, but rows with 32 ST exceed the 1.8 ceiling (329.05), so
1.8 is **not** claimed.

**Convention sensitivity.** If a reviewer additionally loads the target
parameters `11` and `64` from the table instead of using immediates
(`LD = 11`), the harshest row is `W = 2·(11+87+32+37) + 22 = 356 ≤ 356.31`;
1.85 still holds. (The organizer reference count itself prices constant
operands such as the `0xFFFFFFFF` mask as immediates; we load `F` anyway.)
Readings that additionally itemize the internals of a verification
compression on top of its unit are excluded by the rescoring notes as
double counting.

### 6.4 Shaves deliberately not taken

| Reading | Effect | Why rejected |
| --- | --- | --- |
| Omit verification (`H = 0`) / certificate as free check | T < 1 | `"collision checking"` ∈ `total_time_includes` |
| Memory-only code/table image (no placement) | −159 | placement is preprocessing work |
| Native narrow ROT = 1 primitive | ≈ −32 | reference: "no native 32/64-bit rotate is assumed" |
| `F` as immediate | −4 | keep wide mask as a loaded constant |
| Packed 256-bit digest compare | ≈ −56 | keep peer-comparable 8 × 32-bit compare |
| Skip storing zero words (BSS) | −8 | zeroing stays on-ledger |
| Bake `w0..w7` or `D1` into the table | large | instance words as table = advice |

Peak memory is under `2^16` bytes; there is no birthday table.

Claim fields:

- `time_log2 = 1.85`: `T ≤ 2^1.85 ≈ 3.605` (`H = 2` plus `W ≤ 356` ops at
  `1/222`; primary `W = 300`, harshest lattice row `W = 348`).
- `memory_log2_bytes = 16`; `preprocessing_log2 = 0` (setup and placement are
  already inside `T`); `nonuniform_advice_log2_bytes = 0`;
  `success_probability = 1`.

## 7. Evidence and interpretation

- Mathematical support: Lemmas 1–5 and the Theorem are exact identities; no
  random-oracle, independence, or differential heuristic is used.
- Mechanical witness: `blake3-r1-complement-pair`, checked by the organizer
  verifier with rounds = 1.
- No experiment manifest: success probability 1 is proved, not estimated.
- Scope: one round leaves the diagonal message words attacker-controlled after
  the columns force `v8 = v10 = 0` and `v5 = v7 = 0`. With two or more rounds
  the permutation reintroduces every word; no claim is made for `blake3-r2`
  or free-start collisions.
- Background (not used as a black box): Aumasson, Guo, Knellwolf, Matusiewicz,
  Meier, "Differential and Invertibility Properties of BLAKE", FSE 2010 /
  IACR ePrint 2010/043, on invertibility of BLAKE's G.
- History of this package line: organizer birthday baseline 149; earlier
  filings of the same diagonal-complement idea at 4, 2 (`W ≤ 394`, then 326)
  and 1.9 (primary `W ≤ 310`, harshest stress `W = 366`). This package keeps
  `H = 2`, placement, narrow 8-word compare, loaded `F`, and the same stress
  lattice, and lowers the harshest row from 366 to 348 by re-parameterizing
  the columns (`B = 0` on G1/G3, zero-`a1` G0). `baseline_improved =
  blake3-r1-nominal-v2` names the organizer nominal display reference; it is
  not an established attack and does not itself assert an improvement.
- Not claimed: `time_log2 ≤ 1.8` (needs harshest `W ≤ 329`; gap 19 ops);
  any omit-verify, memory-only, or native-ROT reading.

`submission_state = ready` means the package is prepared for submission with
CLI attribution flags. It does not assert a qualifying review, a score,
human acceptance, or promotion.
