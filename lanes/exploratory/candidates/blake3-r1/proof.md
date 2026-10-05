# Deterministic collision for 1-round BLAKE3: uniform Lemma-5 columns run 4-wide in one 256-bit word with a top-of-word lane, plus a y-flip on both diagonals

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is reported
separately as a resource bound.

This exploratory package targets `blake3-r1-prefix-v1`. It gives a classical,
deterministic algorithm. It succeeds with probability 1, its total charged time
is at most `2^1.76` target-compression units, and its peak memory is at most
`2^16` bytes. The construction uses only public IV constants and exact modular
identities of the BLAKE3 `G` function. The heuristic list is empty.

## 0. Ledger at a glance (for reviewers)

```
T  = H + W / C,      H = 2 verification compressions,   C = 222 (blake3-r1)
P  = LD + ALU + ST + V            (straight-line program length, instructions)
W  = P            (execute every instruction once)
   + P            (program placement: 1 op per instruction)
   + 2·LD         (constant-table placement: 2 ops per table word)
   = 2·(LD + ALU + ST + V) + 2·LD
V  = 37           (digest EQ 32 + distinctness 4 + HALT 1)
LD = 9            (IV[0..7] and F = 0xFFFFFFFF, each a separate narrow table word)
```

| Row | ALU | ST | LD | W | T | log2 T |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Primary program (Section 5) | 60 | 18 | 9 | 266 | 3.198 | 1.677 |
| Harshest stress (32 ST, LD 11, flip by SUB 1 + AND) | 61 | 32 | 11 | **304** | 3.369 | **1.7525** |
| Claim-1.76 ceiling `(2^1.76 − 2)·222` | | | | 307.91 | 3.387 | 1.76 |
| Previous package (same algebra, uniform 64-bit lanes), harshest | 64 | 32 | 11 | 310 | 3.396 | 1.764 |
| Older package (y-LSB, scalar), harshest | 79 | 32 | 9 | 332 | 3.496 | 1.806 |

We claim **1.76**. That value is sized to the **maximum** of the full stress
lattice in Section 6.3, not to the primary program: `304 ≤ 307.91` (margin 3.91).
All rows charge both verification compressions and all placement. No row uses a
native rotate of any width (narrow or 256-bit), chained (unmasked) arithmetic,
rotation-AND elision, packed IV loads, pre-packed lane vectors in the table,
packed message stores, or packed digest compare. Claim **1.75** is not made: its
ceiling is `≈302.72` and the harshest row is `304` (§6.5).

**What is new relative to the 1.77 package (same algebra, same messages).**
The four column lanes now sit at bit offsets `(0, 64, 160, 224)` instead of
`(0, 64, 128, 192)`. Lane 3 therefore occupies the **top 32 bits of the
256-bit word**. Two exact word-RAM facts follow (Lemmas S4, S5):

1. Arithmetic mod `2^256` already reduces the top lane mod `2^32`: it needs no
   guard, no gap and no carry/borrow containment.
2. `SHR(V, 224)` is a clean 32-bit word for **every** 256-bit `V`.

Consequently the three vectors that are only ever *unpacked* (the column
`x`-vector `X`, the column `y`-vector `Y`, and the diagonal `x`-vector `Xd`)
no longer need a vector `AND M` before extraction: for lanes 0–2 the
extraction's own `AND F` is the lane mask, and for lane 3 the word boundary is.
For every input, `extract(V AND M) = extract(V)` bit for bit, so that `AND M`
is dead code (Lemma S5). That is **−3 ALU** on every lattice row, `W 310 → 304`.
Every vector that feeds further arithmetic is still `AND M`-clean, every
rotation keeps its final AND, and every stored word is a clean 32-bit value.

**Algebra (unchanged from the 1.77 package).**
All four column `G` calls use the **same** identity (Lemma 5,
`(C*,D*) = (0,−b)`). Each column therefore outputs `B = C = 0` and `D = −b`.
The diagonals then see `b = c = 0` and `d ∈ {−IV7, −IV5}`. Their `M` words are
`x = d − a` and `y = −d` (`= IV7`, `IV5`, loaded words). `M'` changes only the
two diagonal `y` words to `~d` (Lemma 6′), which makes each flipped diagonal
output all-`F` for **any** `d`.

**Graceful degradation (same messages).** If a reviewer rejects 4-wide
packing: 2-way top-lane schedule harshest `W = 322` (fits 1.79); serial
top-field schedule harshest `W = 350` (fits 1.84). Both are better than the
previous fallbacks (332 / 356) and both are emulated (§6.6, §6.8).

Reading chain: Lemmas 1, 5, 6′ (BLAKE3 algebra) → Theorem → instance →
lane Lemmas S0–S5 (word-RAM arithmetic) → charged program → cost lattice.
Certificate `blake3-r1-swar-lemma5-pair` is a witness of the Section 4 instance.

## 1. Exact complete hash

Each message is exactly 64 bytes: one chunk, one full block, no parent. There is
one compression, with flags `CHUNK_START | CHUNK_END | ROOT = 11`, block length 64
and counter 0. The hash is unkeyed BLAKE3-256 with 1 prefix round.

Decode `m` into sixteen little-endian 32-bit words `w[0..15]`. The IV is:

```
6a09e667 bb67ae85 3c6ef372 a54ff53a
510e527f 9b05688c 1f83d9ab 5be0cd19.
```

`v[0..7]=IV`, `v[8..11]=IV[0..3]`, `v[12..15]=(0,0,64,11)`. Additions are mod
`2^32`. `G(a,b,c,d,x,y)`:

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

The digest is `o[i] = v[i] XOR v[i+8]`, `i = 0..7`. This matches
`verifier/blake3.py:blake3(m,1)`.

## 2. Exact identities for one G call

```
a1 = a+b+x;  d1 = ROTR(d XOR a1,16);  c1 = c+d1;  b1 = ROTR(b XOR c1,12);
A  = a1+b1+y; D = ROTR(d1 XOR A,8);   C  = c1+D;  B  = ROTR(b1 XOR C,7).
```

**Lemma 1 (choose `C`, `D`).** Fix any inputs and any targets `(C*,D*)`. Set
`c1 = C*−D*`, `d1 = c1−c`, `a1 = d XOR ROTL(d1,16)`, `x = a1−a−b`,
`b1 = ROTR(b XOR c1,12)`, `A = ROTL(D*,8) XOR d1`, `y = A−a1−b1`,
`B = ROTR(b1 XOR C*,7)`. Then `G(a,b,c,d;x,y) = (A,B,C*,D*)`.
*Proof.* Substitute each line into the next; every step inverts one line of `G`.

**Lemma 5 (`B = C = 0`; any `a,b,c,d`).** Lemma 1 with `(C*,D*) = (0,−b)` gives
`c1 = b`, `b1 = ROTR(0,12) = 0`, `B = ROTR(0 XOR 0,7) = 0`. Explicitly:

```
d1 = b − c,   a1 = d XOR ROTL(d1,16),   x = a1 − a − b,
D  = −b,      A  = ROTL(D,8) XOR d1,    y = A − a1,
G(a,b,c,d; x,y) = (A, 0, 0, −b).
```

This is the unique `(x,y)` with `B = C = 0`. `B = 0` forces `b1 = C = 0`, hence
`c1 = b` and `D = C − c1 = −b`.

**Lemma 6′ (y-flip to `~d` on a zero diagonal; any `d`).** Take `b = c = 0`,
`x = d − a`, `y = −d`. Then `a1 = d`, `d1 = c1 = b1 = 0`, `A = 0`, `D = C = B = 0`,
so `G = (0,0,0,0)`. Replace `y` by `y' = ~d = −d − 1` and keep `x`. The first half
is unchanged, and `A' = d + ~d = 0xFFFFFFFF = F`. So `D' = ROTR(0 XOR F,8) = F`,
`C' = 0 + F = F` and `B' = ROTR(0 XOR F,7) = F`. Hence `G = (F,F,F,F)`.
(When `d` is odd, `~d = (−d) XOR 1`. That is the earlier y-LSB lemma. Lemma 6′
removes the parity condition.)

All lemmas are identities on `(Z/2^32Z)^4`.

## 3. Collision theorem

**Theorem.** Choose `(w[2j], w[2j+1])` for each column `Gj` (`j = 0..3`) by
Lemma 5. Each column's inputs are `(a,b,c,d) = (IVj, IV(j+4), IVj, v[12+j])`
with `v[12..15] = (0,0,64,11)`. After the column step:

```
v4 = v5 = v6 = v7 = 0     (B outputs)      v8 = v9 = v10 = v11 = 0   (C outputs)
v12..v15 = (−IV4, −IV5, −IV6, −IV7)        v0..v3 = column A outputs A0..A3
```

Set `w10 = w11 = w14 = w15 = 0`. Define

```
w8  = −IV7 − A0 ,   w9  = IV7          (G4: a = A0, b = v5 = 0, c = v10 = 0, d = v15 = −IV7)
w12 = −IV5 − A2 ,   w13 = IV5          (G6: a = A2, b = v7 = 0, c = v8  = 0, d = v13 = −IV5)
```

Let `M` use these words. Let `M'` equal `M` except `w9' = ~(−IV7) = IV7 − 1` and
`w13' = ~(−IV5) = IV5 − 1`. Then `M ≠ M'` and `blake3_r1(M) = blake3_r1(M')`.

*Proof.* Columns: Lemma 5 in each column gives the listed state for both `M` and
`M'`, because the column words are shared. G4 has `x = d − a`, `y = −d`. By
Lemma 6′ it outputs `(0,0,0,0)` into lanes `(0,5,10,15)` under `M` and
`(F,F,F,F)` under `M'`. G6 is the same on lanes `(2,7,8,13)`. G5 reads
`(1,6,11,12)` and G7 reads `(3,4,9,14)`. Neither set meets `{0,5,10,15,2,7,8,13}`.
Their message words are shared. So G5 and G7 compute identical values under `M`
and `M'` (the four diagonals touch disjoint lanes, so their order is
irrelevant). The final states differ exactly on the eight G4/G6 lanes. The
affected digest words are

```
o0 = v0 XOR v8,  o2 = v2 XOR v10,  o5 = v5 XOR v13,  o7 = v7 XOR v15,
```

and each pairs one G4 lane with one G6 lane. Each word is `0 XOR 0 = 0` under `M`
and `F XOR F = 0` under `M'`. The other four digest words read only lanes that
are equal under `M` and `M'`. Distinctness: `w9' = IV7 − 1 ≠ IV7`. ∎

No IV parity fact is needed. The only IV-specific identities in the program are
the two small-constant forms of the flip used in Section 5.2, step 5:
`IV7 − 1 = IV7 XOR 1` (`IV7` odd) and `IV5 − 1 = IV5 XOR 7` (`IV5 ≡ 0xc mod 16`).
The stress lattice also has a row that computes both flips by masked subtraction.

## 4. Concrete instance

```
M  = 1eae00b1b20691aa8cc89a63c6ee026b3716478a85d0f8b848f4aed6e079c2d1
     3145758d19cde05b00000000000000009be3c7c58c68059b0000000000000000
M' = 1eae00b1b20691aa8cc89a63c6ee026b3716478a85d0f8b848f4aed6e079c2d1
     3145758d18cde05b00000000000000009be3c7c58b68059b0000000000000000
```

`M'` differs from `M` only in words 9 and 13: `IV7 → IV7−1` and `IV5 → IV5−1`.
Both messages have the blake3-r1 digest

```
0000000033fbbe7300000000dd3cea93ad1e92c800000000f91286d500000000
```

so `o0 = o2 = o5 = o7 = 0`, as predicted. An independent scalar re-run of `G`
confirms these values after the columns: `v4..v11 = 0`, `v13 = −IV5`,
`v15 = −IV7`. It also confirms G4/G6 outputs `0` under `M` and `F` under `M'`.
Certificate `blake3-r1-swar-lemma5-pair` stores these exact bytes.

## 5. Algorithm (charged program)

The program runs on the 256-bit word RAM of collision-frontier-v5. It is
deterministic and straight-line, with no coins, no search and no restarts.
Primitives used: 256-bit LD/ST, ADD/SUB mod `2^256`, AND/OR/XOR, SHL/SHR, BNZ,
HALT. **No rotate instruction of any width is used.** `SHL` discards bits
shifted past bit 255 and `SHR` discards bits shifted below bit 0 (ordinary
word-RAM shift semantics; arithmetic is mod `2^256`).

### 5.1 Lane layout and lane lemmas (word-RAM arithmetic, exact)

A *vector* is a 256-bit word with four 32-bit **value fields** at bit offsets

```
o = (o0, o1, o2, o3) = (0, 64, 160, 224).
```

Lane `i` holds a 32-bit value at bits `[o_i, o_i + 32)`. The bits between value
fields are *gaps*: lane 0's gap is `[32, 64)` (32 bits), lane 1's gap is
`[96, 160)` (64 bits), lane 2's gap is `[192, 224)` (32 bits). **Lane 3 has no
gap: its value field is the top 32 bits of the word.** A vector is *clean*
when every gap bit is zero. Constants built in the program:

```
M  = F·(2^0 + 2^64 + 2^160 + 2^224)        lane mask (value fields)
Gd = SHL(M, 32) = F·(2^32 + 2^96 + 2^192)  guards (the lane-3 copy of F is
                                            shifted out of the word)
```

Lane order is `(lane0, lane1, lane2, lane3) = (G3, G0, G1, G2)`.

**Lemma S1 (guarded lane subtraction).** Let `X, Y` be clean with lanes
`x_i, y_i`. Let `R = (X OR Gd) − Y mod 2^256`. Partition the word into regions
`[0,64)`, `[64,160)`, `[160,224)`, `[224,256)`. In each of the three lower
regions, `X OR Gd` holds `x_i + F·2^{32}` (relative to `o_i`; for lane 1 the
bits `[128,160)` are 0), and `Y` holds `y_i < 2^32`. Hence the region
difference is `x_i − y_i + F·2^32 ≥ 2^64 − 2^33 > 0`: no borrow leaves any of
the three lower regions, and the low 32 bits of the region are
`(x_i − y_i) mod 2^32`. No borrow enters the top region, so its 32 bits are
`(x_3 − y_3) mod 2^32` (any borrow out of bit 255 is discarded by mod `2^256`).
`R AND M` is therefore clean with lanes `(x_i − y_i) mod 2^32`. The same holds
for `(Gd − Y) AND M`, whose lanes are `(−y_i) mod 2^32` (set `x_i = 0`).

**Lemma S2 (lane addition).** For clean `X, Y`, `(X + Y) AND M` is clean with
lanes `(x_i + y_i) mod 2^32`. Each lower-lane sum is `< 2^33`, so its carry stays
in bit `o_i + 32` of its own gap. The top lane's carry leaves the word and is
discarded mod `2^256`.

**Lemma S3 (lane rotation).** For clean `X` and `0 < k < 32`,
`(SHL(X,k) OR SHR(X,32−k)) AND M` is clean with lanes `ROTL32(x_i, k)`.
*Proof.* `SHL` moves bit `j` of lane `i` to `o_i + j + k`. For lanes 0–2 this is
inside the value field or the lane's own gap (every gap has `≥ 32 > k` bits).
For lane 3, positions `≥ 256` are discarded, which are exactly the bits that
wrap in a 32-bit rotate; the remaining bits are `x_3·2^k mod 2^32` in place.
`SHR` sends bit `j ≥ 32−k` of lane `i` to `o_i + j − 32 + k ∈ [o_i, o_i + k)`.
It sends bits `j < 32−k` to `[o_i − 32 + k, o_i)`, which is inside lane
`i−1`'s gap: `[32+k, 64)`, `[128+k, 160)`, `[192+k, 224)` for `i = 1, 2, 3`;
lane 0's low bits leave the word. After OR, the value field of lane `i` is
`(x_i·2^k mod 2^32) | (x_i >> (32−k)) = ROTL32(x_i,k)`. All stray bits are in
gaps, and AND `M` removes them.

**Lemma S0 (cleanliness invariant).** (i) Table IV words and `F` are clean
scalars (`≤ F`). (ii) Packing four clean scalars into the value fields with
`SHL` by `o_i` and `OR` yields a clean vector. (iii) `AND M` yields a clean
vector. (iv) Lemmas S1–S3 outputs are clean; `XOR` of clean vectors is clean.
By induction every vector that feeds arithmetic or a rotation in Section 5.2
(`Av, Bv, Dv, d1, a1, S, N, A`) is clean. The emulator asserts this on the
instance.

**Lemma S4 (top lane).** For every 256-bit word `V`, `SHR(V, 224) ∈ [0, 2^32)`.
ADD/SUB/SHL mod `2^256` act on bits `[224, 256)` exactly as 32-bit arithmetic,
given that no carry/borrow enters from below (guaranteed by S1/S2 for lanes
0–2). So the top lane needs neither a guard nor a gap nor an output mask
before `SHR 224`.

**Lemma S5 (extraction of a guarded difference).** Let `R = (X OR Gd) − Y`
with `X, Y` clean (S1, no output mask). Then

```
AND(R, F)             = (x0 − y0) mod 2^32
AND(SHR(R, 64), F)    = (x1 − y1) mod 2^32
AND(SHR(R, 160), F)   = (x2 − y2) mod 2^32
SHR(R, 224)           = (x3 − y3) mod 2^32     (S4)
```

Moreover, for **every** 256-bit `V` and `o ∈ {0, 64, 160}`,
`AND(SHR(AND(V,M), o), F) = AND(SHR(V, o), F)` (the window `[o, o+32)` lies
inside `M`), and `SHR(AND(V,M), 224) = SHR(V, 224)` (`M ⊇ [224, 256)`). So a
vector `AND M` placed in front of this extraction changes no stored bit for
any input: it is dead code. The program therefore extracts `X`, `Y` and `Xd`
directly from the raw guarded differences. This is **not** chaining: a raw
difference is never an operand of ADD/SUB/XOR or of a rotation; it is only
shifted and AND-masked into a 32-bit scalar (or read as the top 32 bits),
exactly the six extraction primitives that the 1.77 package already charged.

**Why the 1.77 layout could not do this.** With offsets `(0,64,128,192)` the top
lane had a 32-bit gap `[224,256)` above it. A raw guarded difference has
`F` or `F−1` in that gap, so `SHR(R,192)` is not a 32-bit word and needs either
`AND M` on the vector or `AND F` on the extract: the sound saving was 0
(probed in the 1.77 package, `w12 = 0xfffffffec5c7e39b`). Moving lane 3 to the
top of the word removes that gap; the saving becomes 1 per extracted vector.

**Extraction cost.** Four lanes cost `1 + 2 + 2 + 1 = 6` primitives:
`AND F`, `SHR 64 + AND F`, `SHR 160 + AND F`, `SHR 224`.

### 5.2 Program

Lane order `(G3, G0, G1, G2)` at offsets `(0, 64, 160, 224)`. This puts G3's
`D` 64 bits below G0's `A` and G1's `D` 64 bits below G2's `A`, so one `SHL 64`
aligns both diagonal inputs.

```
0. LD IV0..IV7, F                                                   [9 LD]
1. setup     t  = F OR SHL(F,64);  M = t OR SHL(t,160)              [4]
             Gd = SHL(M,32)                                         [1]
             Av = IV3 | IV0<<64 | IV1<<160 | IV2<<224               [6]  (a = c lanes)
             Bv = IV7 | IV4<<64 | IV5<<160 | IV6<<224               [6]  (b lanes)
             Dv = 11 OR SHL(64,224)                                 [2]  (d lanes 11,0,0,64)
2. columns   d1 = ((Bv OR Gd) − Av) AND M            (S1)  b − c    [3]
   Lemma 5   a1 = Dv XOR ROTL(d1,16)                 (S3)           [5]
   4 lanes   S  = (Av + Bv) AND M                    (S2)  a + b    [2]
             Xr = (a1 OR Gd) − S                     (S1 raw) x     [2]
             N  = (Gd − Bv) AND M                    (S1)  D = −b   [2]
             A  = ROTL(N,8) XOR d1                   (S3)  A outputs[5]
             Yr = (A OR Gd) − a1                     (S1 raw) y     [2]
3. unpack    (w6,w0,w2,w4) = extract(Xr); (w7,w1,w3,w5) = extract(Yr) (S5) [6+6]
4. diagonals Xdr = (SHL(N,64) OR Gd) − A     lane1 = −IV7 − A0, lane3 = −IV5 − A2  [3]
             w8  = SHR(Xdr,64) AND F;   w12 = SHR(Xdr,224)          [2+1]
             w9  = IV7 (register);      w13 = IV5 (register)        [0]
5. M'-words  w9'  = IV7 XOR 1        (= IV7 − 1)                    [1]
             w13' = IV5 XOR 7        (= IV5 − 1)                    [1]
             stress row: w13' = (IV5 − 1) AND F                     [2]
6. ST        14 shared words + 2 + 2 differing words (shared buffer)    [ST = 18]
             stress row: both 16-word messages stored separately    [ST = 32]
7. verify    two blake3-r1 compressions (H = 2 units);
             8×32-bit digest EQ (16 LD + 8 XOR + 7 OR + BNZ);
             distinctness on word 9 (2 LD + XOR + BNZ); HALT         [V = 37]
```

ALU per phase: setup 19, columns 21, unpack 12, diagonals 6, flips 2 (3 with
the SUB-1 flip). Total **ALU = 60** (61 with the SUB-1 flip).

**Diagonal step in detail (Lemma S1/S5 applied to a shifted minuend).**
`SHL(N,64)` moves N's lane 0 (`−IV7`) to bits `[64,96)`, N's lane 1 (`−IV4`)
to `[128,160)` (inside lane 1's gap), N's lane 2 (`−IV5`) to `[224,256)`, and
drops N's lane 3. Its bits `[0,64)` and `[160,224)` are 0 (N is clean). After
`OR Gd`: region `[0,64)` is `F·2^32 ≥ A_lane0`, so no borrow enters bit 64;
region `[64,160)` is `−IV7 + F·2^32 + (−IV4)·2^64`, which exceeds `A0 ≤ F` by
more than `2^63`, so its low 32 bits are `(−IV7 − A0) mod 2^32` and no borrow
leaves it; region `[160,224)` is `F·2^32` relative to bit 160, again no borrow;
the top field is `(−IV5 − A2) mod 2^32`. So `w8 = −IV7 − A0` and
`w12 = −IV5 − A2` exactly, as the Theorem requires. Lanes 0 and 2 of `Xdr` are
not used.

#### Explicit line-item costing (every mask / guard / pack / unpack)

| Phase | Ops | Charge | Notes |
| --- | ---: | ---: | --- |
| Lane mask `M` | 4 | SHL×2 + OR×2 | `t = F\|SHL(F,64)`; `M = t\|SHL(t,160)`. |
| Guard `Gd` | 1 | SHL | `Gd = SHL(M,32)`; the top copy leaves the word. |
| Pack `Av` | 6 | SHL×3 + OR×3 | Four narrow IV words (`≤ F`); no pre-AND. |
| Pack `Bv` | 6 | SHL×3 + OR×3 | Same. |
| Pack `Dv` | 2 | SHL + OR | Immediates `11`, `64` (table-loaded under LD = 11). |
| `d1` (masked S1) | 3 | OR + SUB + AND `M` | feeds a rotation and XOR → must be clean. |
| `S` (S2) | 2 | ADD + AND `M` | feeds SUB as subtrahend → masked (no chaining). |
| `N` (masked S1) | 2 | SUB + AND `M` | feeds a rotation and the diagonal minuend. |
| `vrotl` ×2 | 4 each | SHL + SHR + OR + AND `M` | Lemma S3; **no** rotate opcode; final AND kept. |
| XOR into `a1`, `A` | 1 each | XOR | |
| `Xr`, `Yr` (raw S1) | 2 each | OR + SUB | extract-only (S5); vector `AND M` would be dead code. |
| Unpack `Xr`, `Yr` | 6 each | AND, SHR+AND, SHR+AND, SHR | S5; lane 3 by S4. |
| `Xdr` align + sub | 3 | SHL + OR + SUB | extract-only (S5). |
| Extract `w8`, `w12` | 3 | SHR + AND `F` + SHR | `w12` is the top 32 bits (S4). |
| Flips | 2 / 3 | XOR+XOR / XOR+SUB+AND | xor7 / sub1 rows. |
| **Total** | **60 / 61** | | Matches Appendix A counts. |

Difference from the 1.77 program: exactly the three vector `AND M`
instructions on `X`, `Y`, `Xd` are gone (63 → 60, 64 → 61). Everything else
(constants, packing, column formula, rotations, flips, stores, verification)
is the same instruction for instruction, apart from the shift amounts 160/224
replacing 128/192.

#### Harsher readings that were priced and refused

| Skeptic add-on | ΔALU | Why refused |
| --- | ---: | --- |
| `AND M` on `Xr`, `Yr`, `Xdr` before extraction | +3 | Dead code for **every** input (S5): no stored bit changes. With it the program is the 1.77 program (W 310). |
| `AND F` on the three top-lane extracts | +3 | `SHR(V,224) < 2^32` for every 256-bit `V` (S4): word width, not a cleanliness argument. |
| Gap above lane 3 "for symmetry" | +3 | Changes nothing in the model; the top 32 bits of a word are an ordinary field. |
| Rebuild `Gd` before every guarded SUB | +5 | `Gd` is a live register constant. |
| Re-clean (`AND M`) before each `OR Gd` | +4 | Inputs already clean by S0. |
| Linear 7-op `M` instead of tree-4 | +3 | Worse schedule, not a model rule. |
| AND `F` on each IV before pack | +8 | IV words already `≤ F`. |
| Simulate borrow with two SUBs per lane-sub | +5 | Lemma S1: one 256-bit SUB is exact. |

No **honest** extra survives: ALU stays 60/61 and the harshest row stays
`W = 304 ≤ 307.91`.

The Appendix A listing (`ledger_emulator.py`) executes exactly this program on
Python integers mod `2^256`. It counts one unit per primitive, asserts that
every vector feeding arithmetic is clean and that every stored word is in
`[0, 2^32)`, checks the collision with `verifier/blake3.py`, checks that the
message pair is bit-identical to Section 4, and prints every lattice row.

### 5.3 Why `H = 2`, placement, and narrow EQ stay charged

Even though the collision is proved by exact lemmas (deterministic, probability 1):

1. **Collision checking is named.** `cost-models/collision-frontier-v5.json`
   lists `"collision checking"` under `total_time_includes`. A proved
   construction that never compares digests still omits a charged category if
   it asks the organizer verifier to supply that check for free.
2. **BLAKE3 compressions.** The same model's `computation_model` requires that
   BLAKE3 charge all chunk/parent/root compressions. Each 64-byte message is one
   root compression; two messages give **H = 2** when verification hashes both.
3. **Determinism does not zero the check.** That verification always takes the
   success branch (by theorem) zeroes failed-trial amplification; it does not
   make the two compressions or the compare cost 0.
4. **Placement is attack work.** `docs/FRONTIER_LANES.md`: preprocessing, failed
   trials, verification, advice and **code storage** count in the resource
   ledger. `docs/RESCORING.md`: all actual attack work, including memory
   accesses, remains charged. We charge 1 op per instruction for program
   placement and 2 ops per table word for constant-table placement.
5. **Narrow digest EQ.** Equality is eight narrow 32-bit words (`V = 37` with
   distinctness and HALT). Packed 256-bit EQ is deliberately not used.

### 5.4 Why lane-parallel arithmetic is in-model (not native-ROT shopping)

The cost model is a classical probabilistic **256-bit word RAM**. Its listed
primitives (`collision-frontier-v5.json`) are 256-bit load/store, add/subtract
mod `2^256`, AND/OR/XOR/NOT, **shift or rotation**, comparison, branch, and
random word.

**What the reference forbids.** `scripts/reference_operation_costs.py` and
`docs/RESCORING.md` say that **narrow** (32/64-bit) rotations keep their
explicit shifts, ORs and masks in the 256-bit RAM model; no native 32/64-bit
rotate is assumed. Lemma S3 does exactly that: each lane rotation is charged as
`SHL + SHR + OR + AND` (4 primitives), and the final AND is never elided.

**What this program does.** It uses only ADD/SUB/AND/OR/XOR/SHL/SHR. It uses
**no rotate instruction of any width**, including no 256-bit `ROT`. The
lane-parallel saving is that four columns share one instruction stream because
they share one formula (Lemma 5). Packing (12), masks (5) and unpacking (12)
are charged in full. The top-lane placement uses nothing beyond the published
semantics of `SHL`/`SHR`/`ADD`/`SUB` on a 256-bit word: bits above 255 are
discarded.

**Guard gaps are not a cheat.** Lemma S1 needs the all-ones guard so that a
256-bit SUB cannot borrow across a lane boundary. Every ADD/SUB result that
feeds further arithmetic is AND-masked with `M` first. The three raw
differences `Xr`, `Yr`, `Xdr` feed **only** the extraction (S5), where each
stored word is `AND F`-masked or is the top 32 bits of the word.

**Reference cost `C = 222`.** It normalizes the scalar reference compression
under the same expanded-narrow-ROT counting. How the attack program uses the
machine word is the attacker's choice; every instruction of that choice is in
`W`.

**"Isn't 4-lane packing outside the calibrated model?"** No.
`collision-frontier-v5` defines a 256-bit word RAM whose primitives are
word-wide ADD/SUB/AND/OR/XOR/NOT/SHL/SHR. The reference script expands *narrow*
rotates inside the trusted BLAKE3 core so that `C = 222` matches that same
discipline; it does not rewrite the attack machine into a 32-bit-only ALU, and
it does not forbid placing four independent 32-bit values in one word.

### 5.5 Certificate = witness, not advice

Certificate `blake3-r1-swar-lemma5-pair` stores the Section 4 byte strings so the
organizer can re-hash them under `blake3(m, 1)`. That check is evidence that the
fixed pair collides; it is **not** a step of the submitted RAM program and does
not replace the program's own `H = 2` compressions plus EQ/distinctness. The
certificate is not nonuniform advice: the program regenerates the pair from
public IV constants with no search and no stored collision as input. Advice
bytes are reported as 0. The message pair is bit-identical to the 1.77
package; only the program that produces it changed.

## 6. Cost

### 6.1 Primary program

| Item | Ops | Notes |
| --- | ---: | --- |
| LD | 9 | IV[0..7], F |
| ALU | 60 | Section 5.2 |
| ST | 18 | 14 shared + 4 differing |
| V | 37 | EQ + distinct + HALT |
| **P** | **124** | |
| Program placement | 124 | 1 op / instruction |
| Table placement | 18 | 2 × 9 words |
| **W** | **266** | |
| Verification compressions | **2 units** | |

`T = 2 + 266/222 = 3.198`, `log2 T = 1.677`.

### 6.2 Claim ceiling

`time_log2 = 1.76` ⇔ `T ≤ 2^1.76 ≈ 3.3870` ⇔ `W ≤ (2^1.76 − 2)·222 = 307.91`.

### 6.3 Full stress lattice

Stress axes:
- `ST ∈ {18, 32}`: 32 means no shared buffer, with every word of both messages
  stored.
- `LD ∈ {9, 11}`: 11 also table-loads the constants `11` and `64`.
- Flip of `w13'`: `XOR 7` or masked `SUB 1`.

The program never chains and never elides a rotation AND, so those two axes of
older packages change nothing.

| ST | LD | flip | ALU | P | W | T | log2 T | ≤ 307.91? |
| ---: | ---: | :---: | ---: | ---: | ---: | ---: | ---: | :---: |
| 18 | 9 | xor7 | 60 | 124 | 266 | 3.1982 | 1.6773 | yes |
| 18 | 11 | xor7 | 60 | 126 | 274 | 3.2342 | 1.6934 | yes |
| 18 | 9 | sub1 | 61 | 125 | 268 | 3.2072 | 1.6813 | yes |
| 18 | 11 | sub1 | 61 | 127 | 276 | 3.2432 | 1.6974 | yes |
| 32 | 9 | xor7 | 60 | 138 | 294 | 3.3243 | 1.7331 | yes |
| 32 | 11 | xor7 | 60 | 140 | 302 | 3.3604 | 1.7486 | yes |
| 32 | 9 | sub1 | 61 | 139 | 296 | 3.3333 | 1.7370 | yes |
| **32** | **11** | **sub1** | **61** | **141** | **304** | **3.3694** | **1.7525** | **yes** |

The maximum is `W = 304 ≤ 307.91`, a margin of 3.91 ops. We do not claim 1.75:
its ceiling is 302.72 and the harshest row (`304`) exceeds it.

### 6.4 Shaves deliberately not taken

| Reading | Effect | Why not used |
| --- | ---: | --- |
| Omit verification (`H = 0`) | T < 1 | collision checking ∈ total_time_includes |
| Memory-only code/table image | large | code storage is in the ledger |
| Native narrow ROT = 1 | ≈ −24 | reference forbids native 32/64-bit rotate |
| Native 256-bit word `ROT` | ≈ 0 | listed word primitive, but unused; program is uniform no-rotate |
| Unmasked `S = Av + Bv` fed to the `X` subtraction | −1 ALU | is chaining (ADD result enters SUB unmasked); refused |
| "Guard absorbs carry": `Xr = ((a1 + N) OR Gd) − Av` | −1 ALU (harshest W 302, would fit 1.75) | exact (the sum's carry bit lies under `Gd`), but the ADD result is not AND-masked before further use; refused as mask elision |
| Chained guarded subtraction `((a1 OR Gd) − Av) − Bv` | −1 ALU | is chaining; refused |
| Drop the `AND F` in the sub1 flip (`IV5 ≥ 1`) | −1 ALU on sub1 rows | the stress row exists to avoid IV-specific shortcuts; refused |
| IV as one packed 256-bit table word / pre-packed lane vectors in the table | large | keep 8 narrow IV words + `F`; layout-baked table vectors are table shopping |
| Packed 256-bit message stores / digest EQ | large | keep narrow 32-bit stores and compare |
| BSS / skip storing zero words | −8 W | zeroing stays on-ledger |
| `F` as immediate | −4 W | keep the wide mask loaded |
| Drop the `LD = 11` stress axis | −8 W on LD-11 rows | lattice shopping; claim covers the full lattice |
| Drop the `ST = 32` stress axis (register-resident messages) | −28 W | load/store peers charge 32 stores; lattice shopping |

Peak memory is under `2^16` bytes, and there is no birthday table.

Claim fields: `time_log2 = 1.76`, `memory_log2_bytes = 16`,
`preprocessing_log2 = 0`, `nonuniform_advice_log2_bytes = 0`,
`success_probability = 1`.

### 6.5 Why claim 1.75 is not made

Claim 1.75 requires every stress row to satisfy `W ≤ (2^1.75 − 2)·222 ≈ 302.72`.
Only the harshest row (`ST 32, LD 11, sub1`, `W = 304`) exceeds it; it would
need one more honest ALU. The only −1 candidates found are the chaining /
mask-elision shaves in §6.4, which this package refuses. Native word `ROT`
(lane realignment by `ROT`) does not reduce the count: the diagonal alignment
is already one `SHL`. Claim **1.75 is not made**; claim **1.76** stands on
`W = 304 ≤ 307.91`.

### 6.6 Serial fallback (same algebra, no SWAR)

Cost the **same** Theorem / Lemma-5 / Lemma-6′ instance as four independent
scalar columns, under full locks (H = 2, placement, expanded narrow ROT, no
chaining in the low-limb sense, no elision, narrow EQ, `ST 32`, `LD 11`, sub1).

- *Low-limb scalars* (each value in bits `[0,32)`, every ADD/SUB AND-masked
  with `F`, each ROTL = SHL+SHR+OR+AND): 87 ALU, harshest **W = 356** (the
  1.77 package's serial row).
- *Top-field scalars* (each value `x` held as `x·2^224`, i.e. in the top 32
  bits of the word): by Lemma S4 every ADD/SUB result is already an exact
  clean 32-bit field — there is no bit outside the field to mask, so nothing
  is chained or elided. Rotations keep their final `AND (F<<224)`. Charged
  conversions: `F<<224` (1), eight IV words and `11`, `64` moved up by
  `SHL 224` (10), eight column message words moved down by `SHR 224` (8).
  Columns 58, diagonals `SHR(D − A, 224)` 2×2 = 4, flips 2/3: **83 / 84 ALU**, harshest
  `W = 2·84 + 182 = 350` (fits 1.84, ceiling 350.78).

### 6.7 ST = 32 floor (no register-only shave)

Dropping the `ST = 32` stress axis to shared-buffer `ST = 18` would cut `W` by
28. It is not taken: honest load/store peers charge `ST = 32` for both
messages on their skeptic ledgers; `docs/RESCORING.md` keeps memory accesses
on the ledger; sixteen registers cannot hold two 16-word messages end-to-end;
and organizer text never licenses free stores. The lattice keeps `ST = 32`.

### 6.8 Two-way fallback (same algebra, no 4-wide requirement)

If a reviewer accepts lane packing in principle but rejects **four** lanes in
one word, the same instance runs as two 2-lane pairs with lanes at offsets
`(0, 224)`: lane 0 has a 32-bit guard, lane 1 is the top field (S4). Shared
`M = F | F<<224`, `Gd = SHL(M,32)` (3 ALU). Pair `(G0 low, G1 top)` has `d = 0`
(no XOR into `a1`), pair `(G3 low, G2 top)` has `d = (11, 64)`. `X`/`Y` are
raw guarded differences extracted by `AND F` and `SHR 224` (S5). Diagonals:
`w8 = (N_pair2 − A_pair1) AND F` (low limbs: `−IV7 − A0`; the low 32 bits of a
256-bit difference depend only on the low 32 bits of the operands) and
`w12 = SHR((N_pair1 OR Gd) − A_pair2, 224)` (top limbs, guarded: `−IV5 − A2`).

| phase | ALU (xor7) |
| --- | ---: |
| setup `M`,`Gd` | 3 |
| pair `(G0,G1)` d=0 | 28 |
| pair `(G3,G2)` | 31 |
| diagonals | 5 |
| flips | 2 (sub1: 3) |
| **total** | **69** (sub1: **70**) |

Harshest `W = 2·70 + 182 = 322 ≤ 323.71` (fits 1.79). The previous 2-way
schedule was 332 (1.81).

**Degradation ladder (harshest W, same messages).**

| Schedule | ALU (sub1) | harshest W | fits |
| --- | ---: | ---: | --- |
| 4-way top-lane (this claim) | 61 | **304** | 1.76 |
| 2-way top-lane | 70 | 322 | 1.79 |
| serial top-field | 84 | 350 | 1.84 |
| serial low-limb | 87 | 356 | 1.85 |

This package claims 1.76 and therefore depends on defended 4-wide packing;
§6.6/§6.8 show that the algebra still beats the older scalar construction
(1.83) under the weaker 2-way assumption.

## 7. Evidence and interpretation

- Lemmas 1, 5, 6′, S0–S5 and the Theorem are exact. No differential heuristic is
  used for the existence claim.
- Certificate `blake3-r1-swar-lemma5-pair` is checked by the organizer verifier
  at rounds = 1. `python3 scripts/local_tracks.py check blake3-r1-exploratory`
  reports `mechanically_valid` with `certificates_verified = 1`.
- The Appendix A emulator reproduces the instance (bit-identical to Section 4),
  the per-phase operation counts (setup 19, columns 21, unpack 12, diagonals
  6, flips 2/3) and every lattice row. Appendix B reproduces the 2-way and
  serial fallbacks on the same messages.
- Informal sanity check (not evidence for the claim, which rests on S1–S5): the
  lane program was compared with scalar Lemma 5 on 2·10^5 random lane inputs,
  including all-0/all-F edge cases, with no mismatch.
- Scope: 1 prefix round only. The diagonal cancellation needs the B/C-vanishing
  column state, and it does not transfer to two or more rounds without a new
  argument.
- Background: Aumasson et al., FSE 2010 / ePrint 2010/043 (G invertibility).
  It is not used as a black box; Lemma 1 is proved inline.

## 8. Skeptic FAQ

**Q. Ledger arithmetic? Why `W = 304 ≤ 307.91`?**
`W = 2(LD+ALU+ST+V)+2LD` with `V=37`, `H=2` and `C=222`.
- Primary: `LD=9`, `ALU=60`, `ST=18` give `P=124` and `W=266`
  (`T = 2 + 266/222 = 3.198`, `log2 ≈ 1.677`).
- Harshest: `LD=11`, `ALU=61`, `ST=32` give `P=141` and
  `W = 2·141 + 22 = 304` (`T ≈ 3.369`, `log2 ≈ 1.7525`).
- Ceiling for 1.76: `≈ 307.91`. Margin 3.91. Ceiling for 1.75 is `≈ 302.72`;
  not claimed.

**Q. What exactly changed from the 1.77 package?**
Only the lane offsets (`160/224` instead of `128/192`) and, as a consequence,
the removal of three vector `AND M` instructions that became dead code. Same
algebra, same messages, same certificate, same constants, same stress lattice.

**Q. Isn't dropping `AND M` on `X`, `Y`, `Xd` the "fused-unmasked extraction"
that the previous package refused?**
No. The refused form stored a word that was not a clean 32-bit value
(`SHR` of a gapped top lane). Here every stored word is either `AND F` of a
shifted vector or the top 32 bits of the word, and Lemma S5 shows that the
removed `AND M` changes no stored bit for **any** 256-bit input. The previous
package priced the sound form at 0 saving only because its top lane had a gap
above it; with the top lane at bit 224 the sound form saves 1 per vector.

**Q. Is a lane with no gap and no guard legitimate?**
Yes. The model's ADD/SUB are mod `2^256` and its shifts discard bits leaving
the word. For the top 32 bits that *is* 32-bit modular arithmetic, provided no
carry or borrow enters from below, which the guards of lanes 0–2 guarantee
(S1, S2). Rotation of the top lane: `SHL` discards exactly the bits that a
32-bit rotate wraps, and `SHR` returns them to the bottom of the field (S3).

**Q. Isn't four-lane arithmetic a "native narrow rotate" in disguise?**
No. Each lane rotation is the explicit `SHL + SHR + OR + AND` on the 256-bit
word — four charged instructions (Lemma S3), with the AND kept. The saving is
that four columns share one instruction stream because they share one formula.

**Q. Why are guard gaps needed? Isn't that chaining?**
Gaps make Lemma S1's 256-bit SUB lane-exact. Every ADD/SUB result that feeds
another ADD/SUB/XOR or a rotation is AND-masked first. Chaining would reuse an
unmasked sum/difference as an arithmetic operand; that is refused (§6.4). The
raw differences `Xr`, `Yr`, `Xdr` are only extracted.

**Q. Any lattice shopping?**
No. 1.76 covers every row of the `ST × LD × flip` lattice, including the row
that uses none of the small-constant XOR flips and the row that table-loads
`11` and `64`.

**Q. `XOR 1` / `XOR 7` immediates?**
Small public constants, like the shift counts. The stress lattice also prices
the masked-`SUB 1` form (+1 ALU), and the claim covers it.

**Q. H = 2? Placement? Cert = advice? Omit-verify?**
- `H = 2`: yes — both root compressions (§5.3).
- Placement: yes — program 1 op/instruction, table 2 ops/word.
- Certificate: witness only; the program still charges `H = 2` + EQ (§5.5).
- No omit-verify companion, memory-only image, alias EQ, BSS skip, packed IV,
  pre-packed table vectors, packed stores, or packed digest compare.

**Q. Could a skeptic insist on scalar-only arithmetic or on 2-wide packing?**
Forbidding more than 32 useful bits per word would reject the published word
width itself. Separately, the same algebra costs harshest `W = 350`
(serial top-field) or `322` (2-way), §6.6/§6.8; the 1.76 resource claim
depends on 4-wide packing, which is defended as ordinary word-RAM use.

---

> Ledger: `W=2(LD+ALU+ST+V)+2LD`. Primary `LD=9`, `ALU=60`, `ST=18` ⇒ `W=266`.
> Harshest (32 stores, LD 11, masked-SUB flip, no chaining, no elision, no
> native rotate of any width) `ALU=61` ⇒ `W=304 ≤ 307.91` ⇒ `time_log2 = 1.76`.
> Claim 1.75 is not made (`302.72 < 304`; §6.5).

## Appendix A. Ledger emulator (reviewer-run; not executed by intake)

```python
#!/usr/bin/env python3
"""Reviewer-side ledger emulator (proof.md Section 5). Save as
ledger_emulator.py at the repository root and run `python3 ledger_emulator.py`.
Top-lane SWAR Lemma-5 emulator (round 2).
Lane offsets (0,64,160,224) = columns (G3,G0,G1,G2). Lane 3 occupies the top
32 bits of the 256-bit word: no gap, no guard; ADD/SUB/SHL mod 2^256 already
reduce it mod 2^32 and SHR(V,224) is a clean 32-bit word for ANY V.
Outputs X, Y, Xd are never fed to arithmetic: they are extracted directly
(AND F on lanes 0..2, SHR 224 on lane 3), so their AND M is not needed.
Every vector that feeds arithmetic is still AND M clean (no chaining).
"""
import math, struct, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verifier.blake3 import blake3, IV

W256 = (1 << 256) - 1
F = 0xFFFFFFFF
COUNT = {}; _phase = ['']; TRACE = []
def _op(name, r):
    COUNT[_phase[0]] = COUNT.get(_phase[0], 0) + 1; TRACE.append((_phase[0], name)); return r
def ADD(a, b): return _op('ADD', (a + b) & W256)
def SUB(a, b): return _op('SUB', (a - b) & W256)
def AND(a, b): return _op('AND', a & b)
def OR(a, b):  return _op('OR', a | b)
def XOR(a, b): return _op('XOR', a ^ b)
def SHL(a, k): return _op('SHL', (a << k) & W256)
def SHR(a, k): return _op('SHR', a >> k)
OFF = (0, 64, 160, 224)
def lanes_of(V): return [(V >> o) & F for o in OFF]
def clean(V):
    return V == sum(((V >> o) & F) << o for o in OFF)

def program(flip='xor7', ld11=False):
    COUNT.clear(); TRACE.clear()
    _phase[0] = 'setup'
    t = OR(F, SHL(F, 64)); M = OR(t, SHL(t, 160))           # 4  M = F@0,64,160,224
    Gd = SHL(M, 32)                                         # 1  guards [32,64),[96,128),[192,224)
    pack = lambda w0, w1, w2, w3: OR(OR(OR(w0, SHL(w1, 64)), SHL(w2, 160)), SHL(w3, 224))
    Av = pack(IV[3], IV[0], IV[1], IV[2])                   # 6
    Bv = pack(IV[7], IV[4], IV[5], IV[6])                   # 6
    Dv = OR(11, SHL(64, 224))                               # 2  d = (11,0,0,64)
    vsub = lambda x, y: AND(SUB(OR(x, Gd), y), M)           # 3
    vadd = lambda x, y: AND(ADD(x, y), M)                   # 2
    vrotl = lambda x, k: AND(OR(SHL(x, k), SHR(x, 32 - k)), M)  # 4
    _phase[0] = 'columns'
    d1 = vsub(Bv, Av)                    # 3 clean
    a1 = XOR(Dv, vrotl(d1, 16))          # 5 clean
    S = vadd(Av, Bv)                     # 2 clean
    Xr = SUB(OR(a1, Gd), S)              # 2 raw (extract-only)
    N = AND(SUB(Gd, Bv), M)              # 2 clean
    A = XOR(vrotl(N, 8), d1)             # 5 clean
    Yr = SUB(OR(A, Gd), a1)              # 2 raw (extract-only)
    for v in (d1, a1, S, N, A): assert clean(v)
    _phase[0] = 'unpack'
    ext = lambda V: [AND(V, F), AND(SHR(V, 64), F), AND(SHR(V, 160), F), SHR(V, 224)]  # 6
    w6, w0, w2, w4 = ext(Xr)
    w7, w1, w3, w5 = ext(Yr)
    _phase[0] = 'diagonals'
    Xdr = SUB(OR(SHL(N, 64), Gd), A)     # 3 raw: lane1 = -IV7-A_G0, lane3 = -IV5-A_G2
    w8 = AND(SHR(Xdr, 64), F)            # 2
    w12 = SHR(Xdr, 224)                  # 1 (top 32 bits)
    w9, w13 = IV[7], IV[5]
    w9p = XOR(w9, 1)                     # 1
    w13p = XOR(w13, 7) if flip == 'xor7' else AND(SUB(w13, 1), F)
    assert w9p == (IV[7] - 1) & F and w13p == (IV[5] - 1) & F
    words = [w0, w1, w2, w3, w4, w5, w6, w7, w8, w9, 0, 0, w12, w13, 0, 0]
    assert all(0 <= w <= F for w in words)
    m = struct.pack('<16I', *words)
    words[9], words[13] = w9p, w13p
    mp = struct.pack('<16I', *words)
    return m, mp, dict(COUNT)

if __name__ == '__main__':
    C, V = 222, 37
    REF = bytes.fromhex('1eae00b1b20691aa8cc89a63c6ee026b3716478a85d0f8b848f4aed6e079c2d1'
                        '3145758d19cde05b00000000000000009be3c7c58c68059b0000000000000000')
    print('ceilings', {k: round((2 ** k - 2) * C, 2) for k in (1.74, 1.75, 1.76, 1.77)})
    for flip in ('xor7', 'sub1'):
        m, mp, cnt = program(flip)
        alu = sum(cnt.values())
        ok = m != mp and blake3(m, 1) == blake3(mp, 1)
        print(f'flip={flip}: ALU={alu} {cnt} collision={ok} same_M_as_1.77={m == REF}')
        for ST in (18, 32):
            for LD in (9, 11):
                P = LD + alu + ST + V; Wt = 2 * P + 2 * LD; T = 2 + Wt / C
                print(f'  ST={ST} LD={LD} P={P} W={Wt} T={T:.4f} log2T={math.log2(T):.4f} <=1.76:{Wt <= (2**1.76-2)*C} <=1.75:{Wt <= (2**1.75-2)*C}')
    m, mp, _ = program('xor7')
    print('M  =', m.hex()); print("M' =", mp.hex()); print('digest', blake3(m, 1).hex())
```

Output:

```
ceilings {1.74: 297.56, 1.75: 302.72, 1.76: 307.91, 1.77: 313.14}
flip=xor7: ALU=60 {'setup': 19, 'columns': 21, 'unpack': 12, 'diagonals': 8} collision=True same_M_as_1.77=True
  ST=18 LD=9 P=124 W=266 T=3.1982 log2T=1.6773 <=1.76:True <=1.75:True
  ST=18 LD=11 P=126 W=274 T=3.2342 log2T=1.6934 <=1.76:True <=1.75:True
  ST=32 LD=9 P=138 W=294 T=3.3243 log2T=1.7331 <=1.76:True <=1.75:True
  ST=32 LD=11 P=140 W=302 T=3.3604 log2T=1.7486 <=1.76:True <=1.75:True
flip=sub1: ALU=61 {'setup': 19, 'columns': 21, 'unpack': 12, 'diagonals': 9} collision=True same_M_as_1.77=True
  ST=18 LD=9 P=125 W=268 T=3.2072 log2T=1.6813 <=1.76:True <=1.75:True
  ST=18 LD=11 P=127 W=276 T=3.2432 log2T=1.6974 <=1.76:True <=1.75:True
  ST=32 LD=9 P=139 W=296 T=3.3333 log2T=1.7370 <=1.76:True <=1.75:True
  ST=32 LD=11 P=141 W=304 T=3.3694 log2T=1.7525 <=1.76:True <=1.75:False
M  = 1eae00b1b20691aa8cc89a63c6ee026b3716478a85d0f8b848f4aed6e079c2d13145758d19cde05b00000000000000009be3c7c58c68059b0000000000000000
M' = 1eae00b1b20691aa8cc89a63c6ee026b3716478a85d0f8b848f4aed6e079c2d13145758d18cde05b00000000000000009be3c7c58b68059b0000000000000000
digest 0000000033fbbe7300000000dd3cea93ad1e92c800000000f91286d500000000
```

## Appendix B. Fallback emulator (reviewer-run; not executed by intake)

```python
#!/usr/bin/env python3
"""Reviewer-side fallback emulator (proof.md 6.6/6.8). Save as
fallback_emulator.py at the repository root and run it.
Degradation schedules for the same Lemma-5 / Lemma-6' instance (round 2).
two_way(): 2 lanes at offsets (0,224); lane 1 = top 32 bits (no guard, no gap).
serial():  scalar 'top-field' representation x*2^224: ADD/SUB mod 2^256 are
           exactly mod 2^32 on the field and every intermediate word is clean.
Both reproduce the 1.77/1.76 message pair."""
import math, struct, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verifier.blake3 import blake3, IV
W256 = (1 << 256) - 1; F = 0xFFFFFFFF; T = 224
COUNT = {}; _phase = ['']
def _op(r):
    COUNT[_phase[0]] = COUNT.get(_phase[0], 0) + 1; return r
def ADD(a, b): return _op((a + b) & W256)
def SUB(a, b): return _op((a - b) & W256)
def AND(a, b): return _op(a & b)
def OR(a, b):  return _op(a | b)
def XOR(a, b): return _op(a ^ b)
def SHL(a, k): return _op((a << k) & W256)
def SHR(a, k): return _op(a >> k)
REF = bytes.fromhex('1eae00b1b20691aa8cc89a63c6ee026b3716478a85d0f8b848f4aed6e079c2d1'
                    '3145758d19cde05b00000000000000009be3c7c58c68059b0000000000000000')

def finish(words, flip):
    w9p = XOR(IV[7], 1)
    w13p = XOR(IV[5], 7) if flip == 'xor7' else AND(SUB(IV[5], 1), F)
    assert all(0 <= w <= F for w in words)
    m = struct.pack('<16I', *words); words = list(words); words[9], words[13] = w9p, w13p
    return m, struct.pack('<16I', *words)

def two_way(flip='xor7'):
    COUNT.clear(); _phase[0] = 'setup'
    M = OR(F, SHL(F, T)); Gd = SHL(M, 32)                       # 3
    pack2 = lambda lo, hi: OR(lo, SHL(hi, T))                   # 2
    vsub = lambda x, y: AND(SUB(OR(x, Gd), y), M)
    vadd = lambda x, y: AND(ADD(x, y), M)
    vrotl = lambda x, k: AND(OR(SHL(x, k), SHR(x, 32 - k)), M)
    ext = lambda V: (AND(V, F), SHR(V, T))                      # 2
    def pair(a_lo, a_hi, b_lo, b_hi, Dv=None):
        Av = pack2(a_lo, a_hi); Bv = pack2(b_lo, b_hi)
        d1 = vsub(Bv, Av)
        a1 = vrotl(d1, 16) if Dv is None else XOR(Dv, vrotl(d1, 16))
        S = vadd(Av, Bv)
        Xr = SUB(OR(a1, Gd), S)
        N = AND(SUB(Gd, Bv), M)
        A = XOR(vrotl(N, 8), d1)
        Yr = SUB(OR(A, Gd), a1)
        return ext(Xr), ext(Yr), N, A
    _phase[0] = 'pair1'   # (G0 low, G1 top), d = 0
    (w0, w2), (w1, w3), N1, A1 = pair(IV[0], IV[1], IV[4], IV[5])
    _phase[0] = 'pair2'   # (G3 low, G2 top), d = (11, 64)
    Dv = pack2(11, 64)
    (w6, w4), (w7, w5), N2, A2 = pair(IV[3], IV[2], IV[7], IV[6], Dv)
    _phase[0] = 'diagonals'
    w8 = AND(SUB(N2, A1), F)               # 2 low limbs: -IV7 - A_G0
    w12 = SHR(SUB(OR(N1, Gd), A2), T)      # 3 top limbs: -IV5 - A_G2 (guarded)
    _phase[0] = 'flips'
    words = [w0, w1, w2, w3, w4, w5, w6, w7, w8, IV[7], 0, 0, w12, IV[5], 0, 0]
    return finish(words, flip)

def serial(flip='xor7'):
    COUNT.clear(); _phase[0] = 'setup'
    Mt = SHL(F, T)                                              # 1 field mask
    up = lambda w: SHL(w, T)
    rotl = lambda x, k: AND(OR(SHL(x, k), SHR(x, 32 - k)), Mt)  # 4
    ivt = [up(IV[j]) for j in range(8)]                         # 8
    dt = [None, None, up(64), up(11)]                           # 2
    _phase[0] = 'columns'
    out = {}
    for j in range(4):
        a = c = ivt[j]; b = ivt[j + 4]
        d1 = SUB(b, c)
        a1 = rotl(d1, 16) if dt[j] is None else XOR(dt[j], rotl(d1, 16))
        x = SUB(SUB(a1, a), b)
        D = SUB(0, b)
        A = XOR(rotl(D, 8), d1)
        y = SUB(A, a1)
        out[j] = (x, y, D, A)
    _phase[0] = 'extract'
    words = [0] * 16
    for j in range(4):
        words[2 * j] = SHR(out[j][0], T); words[2 * j + 1] = SHR(out[j][1], T)
    _phase[0] = 'diagonals'
    words[8] = SHR(SUB(out[3][2], out[0][3]), T)   # -IV7 - A0
    words[12] = SHR(SUB(out[1][2], out[2][3]), T)  # -IV5 - A2
    words[9], words[13] = IV[7], IV[5]
    _phase[0] = 'flips'
    return finish(words, flip)

if __name__ == '__main__':
    C, V = 222, 37
    for name, fn in (('2-way', two_way), ('serial', serial)):
        for flip in ('xor7', 'sub1'):
            m, mp = fn(flip); alu = sum(COUNT.values())
            ok = m != mp and blake3(m, 1) == blake3(mp, 1)
            Wh = 2 * (11 + alu + 32 + V) + 22
            print(f'{name} {flip}: ALU={alu} {dict(COUNT)} collision={ok} sameM={m == REF} '
                  f'W(ST32,LD11)={Wh} log2T={math.log2(2 + Wh / C):.4f}')
```

Output:

```
2-way xor7: ALU=69 {'setup': 3, 'pair1': 28, 'pair2': 31, 'diagonals': 5, 'flips': 2} collision=True sameM=True W(ST32,LD11)=320 log2T=1.7830
2-way sub1: ALU=70 {'setup': 3, 'pair1': 28, 'pair2': 31, 'diagonals': 5, 'flips': 3} collision=True sameM=True W(ST32,LD11)=322 log2T=1.7868
serial xor7: ALU=83 {'setup': 11, 'columns': 58, 'extract': 8, 'diagonals': 4, 'flips': 2} collision=True sameM=True W(ST32,LD11)=348 log2T=1.8349
serial sub1: ALU=84 {'setup': 11, 'columns': 58, 'extract': 8, 'diagonals': 4, 'flips': 3} collision=True sameM=True W(ST32,LD11)=350 log2T=1.8386
```
