# Deterministic y-LSB dual-flip collision for 1-round BLAKE3 (B-vanishing columns)

The scalar below is `time_log2` under `collision-frontier-v5`. Memory remains
a separately reported resource bound.

This exploratory package targets `blake3-r1-prefix-v1`. It gives a classical
deterministic algorithm with success probability 1, total charged time at most
`2^1.83` target-compression units, and peak memory at most `2^16` bytes. The
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
| Primary program (Section 5) | 67 | 18 | 131 | 280 | 3.261 | 1.706 |
| Harshest stress (full mask, full rotates, 32 ST) | 79 | 32 | 157 | **332** | 3.496 | **1.806** |
| Claim-1.83 ceiling `(2^1.83 − 2)·222` | | | | 345.29 | 3.555 | 1.83 |

The claimed scalar **1.83** is sized to the **maximum** of the full stress
lattice (Section 6.3), not to the primary stream: `332 ≤ 345` (margin 13 ops).
With `LD = 11` (also loading `11` and `64`), harshest `W = 340 ≤ 345.29`.
Both verification compressions and all placement are inside `T`.

**Skeptic-review card.** Ledger `W = 2(LD+ALU+ST+V)+2LD` with `LD=9`, `V=37`,
`H=2`, `C=222`. Primary `ALU=67`, `ST=18` ⇒ `W=280`. Full
`{chain, elide, ST∈{18,32}}` lattice max `ALU=79`, `ST=32` ⇒ `W=332`.
Claim `1.83` covers that max. Certificate is a witness, not advice.
Omit-verify, memory-only placement, and native 1-op narrow ROT are rejected.

**Qualitatively new family.** Prior packages used the diagonal *complement*
(`g` vs `~g`). This package keeps B-vanishing columns and `g = 0` on both
diagonals, then obtains `M'` from `M` by flipping the LSB of the two diagonal
`y` words (`w9` and `w13`). When those diagonals' `d`-inputs are odd (true for
BLAKE3's IV under B-vanishing), each flipped `G` emits the all-`F` state, and
the four feed-forward pairs written by G4/G6 cancel: `F XOR F = 0 XOR 0`.
Messages differ in only two words; construction never builds a second diagonal
closed form.

Reading chain: Lemmas 1–6 → Theorem → instance → charged program → cost lattice.
Certificate `blake3-r1-complement-pair` witnesses the Section 4 instance.

## 1. Exact complete hash

Each message is exactly 64 bytes. One chunk, one full block, no parent, one
compression with `CHUNK_START | CHUNK_END | ROOT = 11`, block length 64,
counter 0. Unkeyed BLAKE3-256 with 1 prefix round.

Decode `m` into sixteen LE 32-bit words `w[0..15]`. IV:

```
6a09e667 bb67ae85 3c6ef372 a54ff53a
510e527f 9b05688c 1f83d9ab 5be0cd19.
```

`v[0..7]=IV`, `v[8..11]=IV[0..3]`, `v[12..15]=(0,0,64,11)`. Additions mod
`2^32`. `G(a,b,c,d,x,y)`:

```
v[a] = v[a]+v[b]+x; v[d] = ROTR(v[d] XOR v[a],16)
v[c] = v[c]+v[d];   v[b] = ROTR(v[b] XOR v[c],12)
v[a] = v[a]+v[b]+y; v[d] = ROTR(v[d] XOR v[a],8)
v[c] = v[c]+v[d];   v[b] = ROTR(v[b] XOR v[c],7).
```

Round 0 schedule `s = w`:

```
G(0,4,8,12,s[0],s[1]);    G(1,5,9,13,s[2],s[3])     # columns G0..G3
G(2,6,10,14,s[4],s[5]);   G(3,7,11,15,s[6],s[7])
G(0,5,10,15,s[8],s[9]);   G(1,6,11,12,s[10],s[11])  # diagonals G4..G7
G(2,7,8,13,s[12],s[13]);  G(3,4,9,14,s[14],s[15]).
```

Digest `o[i] = v[i] XOR v[i+8]`. Matches `verifier/blake3.py:blake3(m,1)`.

## 2. Exact identities for one G call

```
a1 = a+b+x;  d1 = ROTR(d XOR a1,16);  c1 = c+d1;  b1 = ROTR(b XOR c1,12);
A  = a1+b1+y; D = ROTR(d1 XOR A,8);   C  = c1+D;  B  = ROTR(b1 XOR C,7).
```

**Lemma 1 (choose `C`, `D`).** For any inputs and targets `(C*,D*)`:
`c1 = C*−D*`, `d1 = c1−c`, `a1 = d XOR ROTL(d1,16)`, `x = a1−a−b`,
`b1 = ROTR(b XOR c1,12)`, `A = ROTL(D*,8) XOR d1`, `y = A−a1−b1`,
`B = ROTR(b1 XOR C*,7)` give `G(a,b,c,d;x,y) = (A,B,C*,D*)`.

**Lemma 2 (complement step; any `b`, `d`).** Take `c = 0`, `D* = 0`,
`C* = g`. Outputs `(g, β_b(g), g, 0)` with
`β_b(g) = ROTR(ROTR(b XOR g,12) XOR g, 7)`. Then `β_b(~g) = β_b(g)`.

**Lemma 3 (both complement messages).** Under Lemma 2 with `g = 0` and
`g = F`: `s = a+b`, `t = d + ROTR(b,12)`,
`x = d−s`, `y = −t`, `x' = ~(d+s)`, `y' = t+1`.

**Corollary 3b (`b = 0`).** `x = d−a`, `x' = (d+a) XOR F`, `y = −d`,
`y' = d+1`. If `d = −k` for loaded `k`, then `y = k` needs no instruction.

**Lemma 4 (zero-`a1` column, `d = 0`).** `x = −(a+b)` ⇒ `a1 = d1 = 0`,
`c1 = c`, `b1 = β := ROTR(b XOR c,12)`. For any `D*`, `A = ROTL(D*,8)`,
`y = A−β`. Specializations: **4a** (`C = 0`): `D* = −c`. **4b** (`B = 0`):
`D* = β−c`.

**Lemma 5 (`B`-vanishing column, any `d`).** `(C*,D*) = (0, −b)` ⇒
`c1 = b`, `b1 = 0`, `B = 0`, `D* = −b`.

**Lemma 6 (y-LSB flip on a zero diagonal).** Take `b = c = 0` and the
`g = 0` message words of Corollary 3b: `x = d−a`, `y = −d`. Then
`G(a,0,0,d; x,y) = (0,0,0,0)`. Replacing `y` by `y XOR 1` and keeping `x`
gives, with `A = d + (y XOR 1)`:

- if `d` is even: `(1, ROTR(1,15), ROTR(1,8), ROTR(1,8))`;
- if `d` is odd: `(F, F, F, F)`.

Proof. First half still yields `a1 = d`, `d1 = b1 = c1 = 0`. Then
`A = d + ((−d) XOR 1)`. Since `d + (−d) = 0`, `A = ((−d) XOR 1) − (−d)`,
which is `+1` when `−d` is even and `−1 ≡ F` when `−d` is odd. Parity of
`−d` equals parity of `d`. The odd case gives `A = F`, hence
`D = ROTR(F,8) = F`, `C = F`, `B = ROTR(F,7) = F`.

All lemmas are identities on `(Z/2^32Z)^4`.

## 3. Collision theorem (y-LSB dual flip)

**Theorem.** Build columns as in the B-vanishing complement packages
(Lemmas 4a, 1, 4b, 5):

- G0 Lemma 4a: `v8 = 0`, `v0 = ROTL(−IV0, 8)`, `v12 = −IV0`.
- G2 Lemma 1 `(C*,D*) = (0,0)`: `v10 = 0`, `v2 = −IV2`, `v14 = 0`.
- G1 Lemma 4b: `v5 = 0`, `v13 = D1 := β1 − IV1`, `β1 = ROTR(IV5 XOR IV1, 12)`.
- G3 Lemma 5: `v7 = 0`, `v11 = 0`, `v15 = −IV7`.

Set `(w10,w11,w14,w15) = (0,0,0,0)` and take diagonal `g = 0` words:

```
w8  = −IV7 − v0 ,   w9  = IV7
w12 = D1 − v2   ,   w13 = −D1
```

Let `M` use these words and `M'` use the same words except
`w9' = w9 XOR 1`, `w13' = w13 XOR 1` (so `w8' = w8`, `w12' = w12`).

For BLAKE3's IV, both `v15 = −IV7` and `v13 = D1` are odd. By Lemma 6 each of
G4 and G6 on `M` outputs `(0,0,0,0)`, while on `M'` each outputs `(F,F,F,F)`.
G5 and G7 see identical inputs for `M` and `M'` (zero message words; lanes
they read are not among `{0,5,10,15}` or `{2,7,8,13}` before they run, and
G4/G6 write exactly those sets). Final states therefore differ only in
`{v0,v5,v10,v15,v2,v7,v8,v13}`, each flipped `0 ↔ F`. The digest pairs are

```
o0 = v0 XOR v8 ,  o2 = v2 XOR v10 ,  o5 = v5 XOR v13 ,  o7 = v7 XOR v15
```

and each is `0 XOR 0` on `M` and `F XOR F` on `M'`. The other four digest
words use only lanes identical for `M` and `M'`. Hence the digests agree.

**Distinctness.** `w9' = w9 XOR 1 ≠ w9`.

**Why this beats the complement family on the same columns.** The complement
package builds eight diagonal words (`w8,w8',w9,w9',w12,w12',w13,w13'`) with
Corollary 3b (16 ALU harshest on G4+G6, 8 differing stores). Here only four
diagonal words are computed for `M` and two XOR-with-1 produce `M'`
(8 ALU harshest on G4+G6; messages differ in two words; primary `ST = 18`).
Same columns, same `H = 2` locks, fewer diagonal ops and fewer stores.

## 4. Concrete instance

```
M  = 1ac7e7441ae995b4efe892a979a1c5c9b4f69bb08050501c48f4aed6e079c2d1
     529905ae19cde05b0000000000000000194b99e159a8d55a0000000000000000
M' = 1ac7e7441ae995b4efe892a979a1c5c9b4f69bb08050501c48f4aed6e079c2d1
     529905ae18cde05b0000000000000000194b99e158a8d55a0000000000000000
```

(`M'` differs from `M` only in the LSBs of words 9 and 13.) Both have
blake3-r1 digest

```
00000000fd12b1a600000000efa6e4d069871b2b00000000a13b329e00000000
```

so `o0 = o2 = o5 = o7 = 0` as predicted. Certificate
`blake3-r1-complement-pair` stores these exact bytes.

## 5. Algorithm (charged program)

Deterministic straight-line program on the 16-register 256-bit word RAM of
collision-frontier-v5; no coins, no search, no restarts.

1. Load `IV[0..7]` and `F` (9 LD). Immediates: shift counts, flags `11`,
   block length `64`, and the bit-mask `1` used only as `XOR 1` on already
   computed `y` words (small public constant; alternative `ADD F` also works
   when the word is odd and yields the same LSB flip).
2. Columns exactly as the B-vanishing package (59 ALU primary / 71 harshest
   on G0–G3 — unchanged).
3. Diagonals for `M` only, then two `XOR 1` (8 ALU primary / 8 harshest on
   G4–G6 including the flips).
4. Store 14 shared words once and the 2+2 differing `y` words (`ST = 18`).
5. **Verification.** Two blake3-r1 compressions, 8×32-bit digest EQ
   (16 LD + 8 XOR + 7 OR + BNZ), distinctness on word 9 (2 LD + XOR + BNZ),
   HALT. `V = 37`. Success branch always taken; failure still charged.

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
G4 [3/3]    w8  = (n7 − v0) & F                    [2]
            w9  = IV7 (register) ;  w9' = w9 XOR 1 [0+1]
G6 [5/5]    w12 = (D1 − v2) & F                    [2]
            w13 = (0 − D1) & F  ;  w13' = w13 XOR 1 [2+1]
```

Primary column+diagonal ALU `13+15+14+17+3+5 = 67`. Harshest (no chain, no
rotate AND elision) `15+19+17+20+3+5 = 79`. Shared-buffer stores: 14 shared +
4 differ = 18. Emulation on 256-bit integers reproduces Section 4 and these
tallies on every lattice row.

### 5.1 Why `H = 2` and digest compare stay charged

`total_time_includes` lists collision checking; BLAKE3 must charge all root
compressions. Two messages ⇒ two units. The theorem removes failed-trial
amplification only. No omit-verify reading is filed.

### 5.2 Why placement stays charged

`code` under `memory_includes` is a memory metric, not a license to drop
program/table placement from time. Charge 1 op/instruction and 2 ops/table word.

### 5.3 Certificate = witness, not advice

Organizer re-hash of the certificate is not a substitute for the program's
own `H = 2` check. The certificate is not nonuniform advice.

### 5.4 Narrow rotations expanded

Each narrow rotate is `SHL + SHR + OR` and, unless elided into a later masked
consumer, `AND F`. No native 32-bit ROT is assumed
(`scripts/reference_operation_costs.py`).

## 6. Cost

### 6.1 Primary stream

| Item | Ops | Notes |
| --- | ---: | --- |
| LD | 9 | IV[0..7], F |
| ALU | 67 | Section 5 |
| ST | 18 | 14 shared + 4 differ |
| V | 37 | EQ + distinct + HALT |
| **P** | **131** | |
| Program placement | | 131 |
| Table placement (2 × 9) | | 18 |
| **W** | | **280** |
| Verification compressions | | **2 units** |

`T = 2 + 280/222 = 3.261`, `log2 T = 1.706`.

### 6.2 Claim ceiling

`time_log2 = 1.83` ⇔ `T ≤ 2^1.83 ≈ 3.555` ⇔ `W ≤ (2^1.83 − 2)·222 = 345.29`.

### 6.3 Full stress lattice

Refusing chaining adds 4 ALU; refusing rotate AND elision adds 8 ALU; 32 ST
stores both blocks with no shared buffer.

| Chain | Elide | ST | ALU | P | W | T | log2 T | ≤ 345? |
| :---: | :---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: |
| yes | yes | 18 | 67 | 131 | 280 | 3.261 | 1.706 | yes |
| no | yes | 18 | 71 | 135 | 288 | 3.297 | 1.722 | yes |
| yes | no | 18 | 75 | 139 | 296 | 3.333 | 1.737 | yes |
| yes | yes | 32 | 67 | 145 | 308 | 3.387 | 1.760 | yes |
| no | no | 18 | 79 | 143 | 304 | 3.369 | 1.753 | yes |
| no | yes | 32 | 71 | 149 | 316 | 3.423 | 1.775 | yes |
| yes | no | 32 | 75 | 153 | 324 | 3.459 | 1.791 | yes |
| **no** | **no** | **32** | **79** | **157** | **332** | **3.496** | **1.806** | **yes** |

Maximum `W = 332 ≤ 345.29` (margin 13). With `LD = 11`, harshest
`W = 340 ≤ 345.29`. Claim **1.8** is not made (`332 > 329.05`). Claim
**1.82** is not made under `LD = 11` (`340 > 339.84`).

### 6.4 Shaves deliberately not taken

| Reading | Effect | Why rejected |
| --- | --- | --- |
| Omit verification (`H = 0`) | T < 1 | collision checking ∈ total_time_includes |
| Memory-only code/table image | large | placement is preprocessing |
| Native narrow ROT = 1 | ≈ −32 | reference forbids native rotate |
| `F` as immediate | −4 | keep wide mask loaded |
| Packed 256-bit digest compare | ≈ −56 | keep 8 × 32-bit compare |
| Skip storing zero words (BSS) | −8 | zeroing stays on-ledger |
| Theorem-alias digest EQ | −64 | still charge full 8-word EQ |
| Bake column words into the table | large | would be advice |

Peak memory under `2^16` bytes; no birthday table.

Claim fields: `time_log2 = 1.83`, `memory_log2_bytes = 16`,
`preprocessing_log2 = 0`, `nonuniform_advice_log2_bytes = 0`,
`success_probability = 1`.

## 7. Evidence and interpretation

- Lemmas 1–6 and the Theorem are exact; no differential heuristic is used for
  the existence claim (the y-LSB idea was found by probing B-vanishing digests,
  then proved).
- Certificate `blake3-r1-complement-pair` checked by the organizer verifier at
  rounds = 1.
- Scope: 1-round only; oddness of `−IV7` and `D1` is an IV fact used explicitly.
- Background: Aumasson et al., FSE 2010 / ePrint 2010/043 (G invertibility),
  not used as a black box.

## 8. Skeptic FAQ

**Q. Ledger formula?**
`W = 2(LD+ALU+ST+V)+2LD` with `LD=9`. Primary `ALU=67`, `ST=18` ⇒ `W=280`.
Harshest `ALU=79`, `ST=32` ⇒ `W=332 ≤ 345.29`.

**Q. Why 1.83 not 1.85 / 1.8?**
Prior complement family harshest `W = 348` needed `1.85`. This family cuts
diagonal construction and differs in two words ⇒ `W = 332`, which clears
`1.83` including `LD = 11` (`340 ≤ 345`) but not `1.8` (`332 > 329`).

**Q. Is this just the complement pair with a different accounting?**
No. `M'` is not the Corollary-3b complement message. Words 8 and 12 are
*shared*; only the LSBs of words 9 and 13 flip. The state difference is
all-`F` on G4/G6 outputs via Lemma 6, not Lemma 2's `g` vs `~g` with
unchanged `B,D`.

**Q. Why is `XOR 1` allowed as an immediate?**
Same small-constant carve-out already used for shift counts, `0`, `11`, and
`64`. The bit `1` is a one-bit public mask. Loading it from the table instead
(`LD = 10`) still leaves harshest `W = 336 ≤ 345`.

**Q. H = 2? Placement? Cert = advice?**
Yes / yes / no — unchanged CoS posture from the 1.85 filing.

**Q. Mechanical check?**
`blake3(M,1) == blake3(M',1)`, `M != M'`, emulator tallies match Section 6.3.

---

> Ledger: `W=2(LD+ALU+ST+V)+2LD` with `LD=9`. Primary `ALU=67`, `ST=18` ⇒
> `W=280`. Harshest (no chained mask, no rotation AND elision, 32
> non-shared stores) `ALU=79`, `ST=32` ⇒ `W=332 ≤ 345.29`.
