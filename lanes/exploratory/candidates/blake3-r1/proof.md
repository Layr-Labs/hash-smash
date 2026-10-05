# Deterministic collision for 1-round BLAKE3: uniform Lemma-5 columns run 4-wide in one 256-bit word, plus a y-flip on both diagonals

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is reported
separately as a resource bound.

This exploratory package targets `blake3-r1-prefix-v1`. It gives a classical,
deterministic algorithm. It succeeds with probability 1, its total charged time
is at most `2^1.77` target-compression units, and its peak memory is at most
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
| Primary program (Section 5) | 63 | 18 | 9 | 272 | 3.225 | 1.689 |
| Harshest stress (32 ST, LD 11, flip by SUB 1 + AND) | 64 | 32 | 11 | **310** | 3.396 | **1.764** |
| Claim-1.77 ceiling `(2^1.77 − 2)·222` | | | | 313.14 | 3.411 | 1.77 |
| Previous package (y-LSB, scalar), harshest | 79 | 32 | 9 | 332 | 3.496 | 1.806 |

We claim **1.77**. That value is sized to the **maximum** of the full stress
lattice in Section 6.3, not to the primary program: `310 ≤ 313.14`. All rows
charge both verification compressions and all placement. No row uses a native
rotate of any width, chained (unmasked) arithmetic, rotation-AND elision,
packed IV loads, packed message stores, or packed digest compare.

**What is new.**
1. *Algebra.* All four column `G` calls use the **same** identity (Lemma 5,
   `(C*,D*) = (0,−b)`). Each column therefore outputs `B = C = 0` and `D = −b`.
   The diagonals then see `b = c = 0` and `d ∈ {−IV7, −IV5}`. Their `M` words are
   `x = d − a` and `y = −d`. Here `y` is a loaded IV word (`IV7` or `IV5`), so it
   needs no instruction. `M'` changes only the two diagonal `y` words to `~d`
   (Lemma 6′). Lemma 6′ makes each flipped diagonal output all-`F` for **any**
   `d`, so it needs no parity condition.
2. *Implementation.* Because the four columns share one formula, they run
   together as one program on 256-bit words. Each 256-bit word holds four 64-bit
   lanes: a 32-bit value plus a 32-bit guard gap. The column stage costs 23 ALU
   operations in total. The old scalar program spent 71 ALU (harshest) on its
   four separately specialised columns. Lane packing, lane masks and unpacking
   are all charged (Section 5, Section 6).

Reading chain: Lemmas 1, 5, 6′ (BLAKE3 algebra) → Theorem → instance →
lane Lemmas S1–S3 (word-RAM arithmetic) → charged program → cost lattice.
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
the two small-constant forms of the flip used in Section 5, step 6:
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
HALT. **No rotate instruction of any width is used.**

### 5.1 Lane layout and lane lemmas (word-RAM arithmetic, exact)

A *vector* is a 256-bit word with four 64-bit lanes. Lane `i` holds a 32-bit
value at bits `[64i, 64i+32)`; bits `[64i+32, 64i+64)` form its *gap*. A vector is
*clean* when every gap is zero. Constants built in the program:
`M = Σ F·2^{64i}` is the lane mask and `Gd = M << 32` sets every gap to all ones.

**Lemma S1 (lane subtraction).** Let `X, Y` be clean with lanes `x_i, y_i`. Then
`((X OR Gd) − Y) AND M` is clean with lanes `(x_i − y_i) mod 2^32`. The same holds
for `(Gd − Y) AND M`, whose lanes are `(−y_i) mod 2^32`.
*Proof.* `X OR Gd = Σ (x_i + 2^64 − 2^32)·2^{64i}`, and every lane term is
`≥ 2^32 > y_i`. So `X OR Gd − Y = Σ (x_i + 2^64 − 2^32 − y_i)·2^{64i}`, with every
lane term in `[0, 2^64)`. No borrow crosses a lane boundary, and nothing wraps
mod `2^256`. The low 32 bits of lane `i` are `x_i − y_i mod 2^32`, and AND `M`
clears the gaps. For `Gd − Y` set `x_i = 0`.

**Lemma S2 (lane addition).** For clean `X, Y`, `(X + Y) AND M` is clean with
lanes `(x_i + y_i) mod 2^32`. Each lane sum is `< 2^33 < 2^64`, so there is no
inter-lane carry.

**Lemma S3 (lane rotation).** For clean `X` and `0 < k < 32`,
`(SHL(X,k) OR SHR(X,32−k)) AND M` is clean with lanes `ROTL32(x_i, k)`.
*Proof.* `SHL` moves bit `j` of lane `i` to `64i+j+k < 64i+64`, so the bit stays
in lane `i`. The highest position is `192+31+k < 256`, so nothing is lost.
`SHR` sends bits `j ≥ 32−k` to `64i + j − 32 + k ∈ [64i, 64i+k)`. It sends bits
`j < 32−k` into the gap of lane `i−1` (bits `≥ 64(i−1)+32+k`), and for lane 0 off
the bottom. After OR, the low 32 bits of lane `i` are
`(x_i·2^k mod 2^32) | (x_i >> (32−k)) = ROTL32(x_i,k)`. All stray bits are in
gaps, and AND `M` removes them.

**Extraction.** For a clean vector, the four lane values are `V AND F`,
`SHR(V,64) AND F`, `SHR(V,128) AND F` and `SHR(V,192)`. That is 6 instructions,
each yielding a clean 32-bit word.

### 5.2 Program

Lane order is `(lane0, lane1, lane2, lane3) = (G3, G0, G1, G2)`. This order puts
G3's `D` directly below G0's `A`, and G1's `D` directly below G2's `A`. One
`SHL 64` then aligns the diagonal inputs.

```
0. LD IV0..IV7, F                                                   [9 LD]
1. setup     t  = F OR SHL(F,64);  M = t OR SHL(t,128)              [4]
             Gd = SHL(M,32)                                         [1]
             Av = IV3 | IV0<<64 | IV1<<128 | IV2<<192               [6]  (a = c lanes)
             Bv = IV7 | IV4<<64 | IV5<<128 | IV6<<192               [6]  (b lanes)
             Dv = 11 OR SHL(64,192)                                 [2]  (d lanes 11,0,0,64)
2. columns   d1 = ((Bv OR Gd) − Av) AND M            (S1)  b − c    [3]
   Lemma 5   a1 = Dv XOR ROTL(d1,16)                 (S3)           [5]
   4 lanes   S  = (Av + Bv) AND M                    (S2)  a + b    [2]
             X  = ((a1 OR Gd) − S) AND M             (S1)  x words  [3]
             N  = (Gd − Bv) AND M                    (S1)  D = −b   [2]
             A  = ROTL(N,8) XOR d1                   (S3)  A outputs[5]
             Y  = ((A OR Gd) − a1) AND M             (S1)  y words  [3]
3. unpack    (w6,w0,w2,w4) = lanes(X);  (w7,w1,w3,w5) = lanes(Y)    [6+6]
4. diagonals Xd  = ((SHL(N,64) OR Gd) − A) AND M      lane1 = −IV7 − A0,
                                                      lane3 = −IV5 − A2   [4]
             w8  = SHR(Xd,64) AND F;  w12 = SHR(Xd,192)             [2+1]
             w9  = IV7 (register);    w13 = IV5 (register)          [0]
5. M'-words  w9'  = IV7 XOR 1        (= IV7 − 1)                    [1]
             w13' = IV5 XOR 7        (= IV5 − 1)                    [1]
             stress row: w13' = (IV5 − 1) AND F                     [2]
6. ST        14 shared words + 2 + 2 differing words (shared buffer)    [ST = 18]
             stress row: both 16-word messages stored separately    [ST = 32]
7. verify    two blake3-r1 compressions (H = 2 units);
             8×32-bit digest EQ (16 LD + 8 XOR + 7 OR + BNZ);
             distinctness on word 9 (2 LD + XOR + BNZ); HALT         [V = 37]
```

ALU per phase: setup 19, columns 23, unpack 12, diagonals + flips 9. Total
**ALU = 63** (64 with the SUB-1 flip). Every arithmetic result is lane-masked
(or, for scalars, AND `F`) before it feeds any further arithmetic. Every rotation
keeps its final AND. Every stored word is a clean 32-bit value in its own cell.

The Appendix A listing (`ledger_emulator.py`) executes exactly this program on Python
integers mod `2^256`. It counts one unit per primitive and asserts every stored
word is in `[0, 2^32)`. It checks the collision with `verifier/blake3.py` and
prints every lattice row. Its output is reproduced in Section 6.3.

### 5.3 Why `H = 2`, placement, and narrow EQ stay charged

`total_time_includes` lists collision checking, and BLAKE3 must charge all root
compressions: two messages give two units. `docs/FRONTIER_LANES.md` says that
preprocessing, failed trials, verification, advice and **code storage** count in
the resource ledger. `docs/RESCORING.md` keeps memory accesses charged. We use
the same 1 op/instruction program placement and 2 ops/table-word table placement
as the honest peer package `d60b306`. Digest equality is compared as eight
32-bit words.

### 5.4 Why lane-parallel arithmetic is in-model

The cost model is a "classical probabilistic 256-bit word RAM". Its primitives
are 256-bit add/subtract mod `2^256`, AND/OR/XOR/NOT, and shift. Lemmas S1–S3
use only those primitives on 256-bit words, and each instruction is charged
once. No new primitive, native narrow rotate, or lookup table is introduced.
Lane masks, guards and IV packing are built from `F` and the loaded IV words at
full charge. The reference cost `C = 222` normalizes the scalar reference
compression. How the attack program uses the machine word is the attacker's
choice, and every instruction of that choice is in `W`.

### 5.5 Certificate = witness, not advice

The organizer's re-hash of the certificate does not replace the program's own
`H = 2` check. The certificate is not nonuniform advice: the program regenerates
the pair from IV constants.

## 6. Cost

### 6.1 Primary program

| Item | Ops | Notes |
| --- | ---: | --- |
| LD | 9 | IV[0..7], F |
| ALU | 63 | Section 5.2 |
| ST | 18 | 14 shared + 4 differing |
| V | 37 | EQ + distinct + HALT |
| **P** | **127** | |
| Program placement | 127 | 1 op / instruction |
| Table placement | 18 | 2 × 9 words |
| **W** | **272** | |
| Verification compressions | **2 units** | |

`T = 2 + 272/222 = 3.225`, `log2 T = 1.689`.

### 6.2 Claim ceiling

`time_log2 = 1.77` ⇔ `T ≤ 2^1.77 ≈ 3.4105` ⇔ `W ≤ (2^1.77 − 2)·222 = 313.14`.

### 6.3 Full stress lattice

Stress axes:
- `ST ∈ {18, 32}`: 32 means no shared buffer, with every word of both messages
  stored.
- `LD ∈ {9, 11}`: 11 also table-loads the constants `11` and `64`.
- Flip of `w13'`: `XOR 7` or masked `SUB 1`.

The two axes of the previous package, *chaining* and *rotation-AND elision*,
change nothing here. The program never chains and never elides, so refusing
either costs 0.

| ST | LD | flip | ALU | P | W | T | log2 T | ≤ 313.14? |
| ---: | ---: | :---: | ---: | ---: | ---: | ---: | ---: | :---: |
| 18 | 9 | xor7 | 63 | 127 | 272 | 3.2252 | 1.6894 | yes |
| 18 | 11 | xor7 | 63 | 129 | 280 | 3.2613 | 1.7054 | yes |
| 18 | 9 | sub1 | 64 | 128 | 274 | 3.2342 | 1.6934 | yes |
| 18 | 11 | sub1 | 64 | 130 | 282 | 3.2703 | 1.7094 | yes |
| 32 | 9 | xor7 | 63 | 141 | 300 | 3.3514 | 1.7447 | yes |
| 32 | 11 | xor7 | 63 | 143 | 308 | 3.3874 | 1.7602 | yes |
| 32 | 9 | sub1 | 64 | 142 | 302 | 3.3604 | 1.7486 | yes |
| **32** | **11** | **sub1** | **64** | **144** | **310** | **3.3964** | **1.7640** | **yes** |

The maximum is `W = 310 ≤ 313.14`, a margin of 3.14 ops. We do not claim 1.76:
its ceiling is 307.91, and the two LD-11 rows (`308`, `310`) exceed it. We do not
claim 1.75 either (ceiling 302.72).

### 6.4 Shaves deliberately not taken

| Reading | Effect | Why not used |
| --- | ---: | --- |
| Omit verification (`H = 0`) | T < 1 | collision checking ∈ total_time_includes |
| Memory-only code/table image | large | code storage is in the ledger |
| Native narrow ROT = 1 | ≈ −24 | reference forbids native narrow rotate |
| Native 256-bit ROT (alternate lane order + `ROT 128`) | −2 W | listed primitive, but not needed; kept out for a uniform no-rotate program |
| Fuse the lane mask of `Xd` into extraction | −2 W | conservative: every vector result masked |
| Chained guarded subtraction (reuse unmasked gaps) | −2…−6 W | is chaining; refused |
| IV as one packed 256-bit table word | ≈ −28 W | keep 8 narrow IV words (peer parity) |
| Packed 256-bit message stores / digest EQ | large | keep narrow 32-bit stores and compare |
| BSS / skip storing zero words | −8 W | zeroing stays on-ledger |
| `F` as immediate | −4 W | keep the wide mask loaded |

Peak memory is under `2^16` bytes, and there is no birthday table.

Claim fields: `time_log2 = 1.77`, `memory_log2_bytes = 16`,
`preprocessing_log2 = 0`, `nonuniform_advice_log2_bytes = 0`,
`success_probability = 1`.

## 7. Evidence and interpretation

- Lemmas 1, 5, 6′, S1–S3 and the Theorem are exact. No differential heuristic is
  used for the existence claim.
- Certificate `blake3-r1-swar-lemma5-pair` is checked by the organizer verifier
  at rounds = 1. `python3 scripts/local_tracks.py check blake3-r1-exploratory`
  reports `mechanically_valid` with `certificates_verified = 1`.
- The Appendix A emulator reproduces the instance, the per-phase operation counts
  (setup 19, columns 23, unpack 12, diagonals 9/10) and every lattice row.
- Scope: 1 prefix round only. The diagonal cancellation needs the B/C-vanishing
  column state, and it does not transfer to two or more rounds without a new
  argument.
- Background: Aumasson et al., FSE 2010 / ePrint 2010/043 (G invertibility).
  It is not used as a black box; Lemma 1 is proved inline.

## 8. Skeptic FAQ

**Q. Ledger arithmetic?**
`W = 2(LD+ALU+ST+V)+2LD` with `V=37`, `H=2` and `C=222`.
- Primary: `LD=9`, `ALU=63`, `ST=18` give `P=127` and `W=272`.
- Harshest: `LD=11`, `ALU=64`, `ST=32` give `P=144` and `W=2·144+22=310`.
- Ceiling for 1.77: `313.14`, so the margin is 3.14.

**Q. Isn't four-lane arithmetic a "native narrow rotate" in disguise?**
No. Each lane rotation is the explicit `SHL + SHR + OR + AND` on the 256-bit
word, 4 charged instructions (Lemma S3). The saving comes from doing four
columns' rotations in those same 4 instructions. The cost is charged packing
(12), masks (5) and unpacking (12).

**Q. Is this the y-LSB package with different accounting?**
No. The column algebra is different. The old package used four specialised
column lemmas (4a, 1, 4b, 5) with `D`-values `−IV0, 0, β1−IV1, −IV7`; here every
column uses Lemma 5. The diagonal flip is different: `~d` (any parity) instead
of `XOR 1` (odd `d` only). The message pair is different (digest above). And the
program is different: the uniform column formula is what makes lane-parallel
execution possible. On the old scalar ledger, uniform Lemma 5 alone costs slightly
more than before (about 84 vs 79 harshest ALU). The gain comes from algebra and implementation together.

**Q. Any lattice shopping?**
No. 1.77 covers every row of the `ST × LD × flip` lattice, including the row that
uses none of the small-constant XOR flips. The previous chaining and elision
axes are 0-effect here because the program uses neither.

**Q. `XOR 1` / `XOR 7` immediates?**
They are small public constants, like the shift counts, `11` and `64`. The
stress lattice also prices the masked-`SUB 1` form (+1 ALU), and the claim
covers it.

**Q. H = 2? Placement? Cert = advice? Omit-verify?**
- `H = 2`: yes.
- Placement: yes, program at 1 op/instruction and table at 2 ops/word.
- Certificate: it is a witness, not advice.
- There is no omit-verify companion, memory-only image, alias EQ, or BSS skip.

---

> Ledger: `W=2(LD+ALU+ST+V)+2LD`. Primary `LD=9`, `ALU=63`, `ST=18` ⇒ `W=272`.
> Harshest (32 stores, LD 11, masked-SUB flip, no chaining, no elision, no
> native rotate) `ALU=64` ⇒ `W=310 ≤ 313.14` ⇒ `time_log2 = 1.77`.

## Appendix A. Ledger emulator (reviewer-run; not executed by intake)

```python
#!/usr/bin/env python3
"""Reviewer-side ledger emulator for the SWAR Lemma-5 / y-flip package (proof.md Section 5).

Executes the exact straight-line program of proof.md on Python integers reduced
mod 2^256, counting one unit per primitive word-RAM operation (ADD/SUB mod 2^256,
AND/OR/XOR, SHL/SHR).  No native rotate of any width is used; every narrow
rotation is SHL+SHR+OR+AND.  No chaining: every ADD/SUB result is lane-masked
before it feeds any further arithmetic.  No rotation-AND elision.

Usage: save as ledger_emulator.py at the repository root and run
    python3 ledger_emulator.py
"""
import math, struct, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verifier.blake3 import blake3, IV   # organizer reference, rounds=1 below

W256 = (1 << 256) - 1
F = 0xFFFFFFFF
TRACE = []
COUNT = {}
_phase = ['']

def _op(name, r):
    COUNT[_phase[0]] = COUNT.get(_phase[0], 0) + 1
    TRACE.append((_phase[0], name))
    return r

def ADD(a, b): return _op('ADD', (a + b) & W256)
def SUB(a, b): return _op('SUB', (a - b) & W256)
def AND(a, b): return _op('AND', a & b)
def OR(a, b):  return _op('OR', a | b)
def XOR(a, b): return _op('XOR', a ^ b)
def SHL(a, k): return _op('SHL', (a << k) & W256)
def SHR(a, k): return _op('SHR', a >> k)

def program(flip='xor7'):
    COUNT.clear(); TRACE.clear()
    # lanes 0..3 (64 bits each, value in low 32 bits, 32-bit gap) = columns G3, G0, G1, G2
    _phase[0] = 'setup'
    t = OR(F, SHL(F, 64)); M = OR(t, SHL(t, 128))          # 4: lane mask
    Gd = SHL(M, 32)                                        # 1: all-ones gap guards
    pack = lambda w0, w1, w2, w3: OR(OR(OR(w0, SHL(w1, 64)), SHL(w2, 128)), SHL(w3, 192))
    Av = pack(IV[3], IV[0], IV[1], IV[2])                  # 6: a = c inputs
    Bv = pack(IV[7], IV[4], IV[5], IV[6])                  # 6: b inputs
    Dv = OR(11, SHL(64, 192))                              # 2: d inputs (11,0,0,64)
    vsub = lambda x, y: AND(SUB(OR(x, Gd), y), M)          # 3: lane-wise (x-y) mod 2^32
    vadd = lambda x, y: AND(ADD(x, y), M)                  # 2: lane-wise (x+y) mod 2^32
    vrotl = lambda x, k: AND(OR(SHL(x, k), SHR(x, 32 - k)), M)   # 4: lane-wise ROTL32
    _phase[0] = 'columns'          # Lemma 5 in all four lanes: (C*,D*) = (0,-b)
    d1 = vsub(Bv, Av)              # 3  d1 = c1 - c = b - a
    a1 = XOR(Dv, vrotl(d1, 16))    # 5  a1 = d ^ ROTL(d1,16)
    S = vadd(Av, Bv)               # 2  a + b
    X = vsub(a1, S)                # 3  x = a1 - a - b
    N = AND(SUB(Gd, Bv), M)        # 2  D = -b
    A = XOR(vrotl(N, 8), d1)       # 5  A = ROTL(D,8) ^ d1
    Y = vsub(A, a1)                # 3  y = A - a1   (b1 = 0)
    _phase[0] = 'unpack'
    lanes = lambda V: [AND(V, F), AND(SHR(V, 64), F), AND(SHR(V, 128), F), SHR(V, 192)]
    w6, w0, w2, w4 = lanes(X)      # 6
    w7, w1, w3, w5 = lanes(Y)      # 6
    _phase[0] = 'diagonals'
    Xd = vsub(SHL(N, 64), A)       # 4  lane1 = -IV7 - A_G0, lane3 = -IV5 - A_G2
    w8 = AND(SHR(Xd, 64), F)       # 2
    w12 = SHR(Xd, 192)             # 1
    w9, w13 = IV[7], IV[5]         # registers (y = -d with d = -IV7, -IV5)
    w9p = XOR(w9, 1)               # 1  = ~d4 = IV7 - 1 (IV7 odd)
    if flip == 'xor7':
        w13p = XOR(w13, 7)         # 1  = ~d6 = IV5 - 1 (IV5 = ...c, so -1 = xor 7)
    else:
        w13p = AND(SUB(w13, 1), F) # 2  same value via masked subtraction
    assert w9p == (IV[7] - 1) & F and w13p == (IV[5] - 1) & F
    words = [w0, w1, w2, w3, w4, w5, w6, w7, w8, w9, 0, 0, w12, w13, 0, 0]
    assert all(0 <= w <= F for w in words)
    m = struct.pack('<16I', *words)
    words[9], words[13] = w9p, w13p
    mp = struct.pack('<16I', *words)
    return m, mp, dict(COUNT)

if __name__ == '__main__':
    C, V = 222, 37
    print('ceilings W(k) = (2^k - 2) * 222:',
          {k: round((2 ** k - 2) * C, 2) for k in (1.75, 1.76, 1.77, 1.78, 1.8, 1.83)})
    for flip in ('xor7', 'sub1'):
        m, mp, cnt = program(flip)
        alu = sum(cnt.values())
        ok = m != mp and blake3(m, 1) == blake3(mp, 1)
        print(f'\nflip={flip}: ALU={alu} {cnt} collision={ok}')
        for ST in (18, 32):
            for LD in (9, 11):
                P = LD + alu + ST + V
                Wt = 2 * P + 2 * LD
                T = 2 + Wt / C
                print(f'  ST={ST:2d} LD={LD:2d}  P={P}  W={Wt}  T={T:.4f}  log2T={math.log2(T):.4f}'
                      f'  <=1.77:{Wt <= (2**1.77-2)*C}')
    m, mp, _ = program('xor7')
    print('\nM  =', m.hex()); print("M' =", mp.hex())
    print('digest =', blake3(m, 1).hex())
    print('differing words:', [i for i in range(16) if m[4*i:4*i+4] != mp[4*i:4*i+4]])
```
