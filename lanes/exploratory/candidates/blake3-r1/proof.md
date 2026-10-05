# Deterministic collision for 1-round BLAKE3: uniform Lemma-5 columns in 2-wide SWAR plus y-flip (insurance schedule)

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is reported
separately as a resource bound.

This exploratory package targets `blake3-r1-prefix-v1`. It gives a classical,
deterministic algorithm. It succeeds with probability 1, its total charged time
is at most `2^1.81` target-compression units, and its peak memory is at most
`2^16` bytes. The construction uses only public IV constants and exact modular
identities of the BLAKE3 `G` function. The heuristic list is empty.

**Parallel-AR / insurance role.** Algebra and messages are bit-identical to the
4-way SWAR package awaiting review as `94e5361` @1.77 (harshest `W = 310`).
This package charges only a **2-lane** word-RAM schedule (harshest `W = 332`)
so the resource claim survives if reviewers reject 4-wide packing but accept
2-wide packing. It does **not** cancel or replace `94e5361`.

## 0. Ledger at a glance (for reviewers)

```
T  = H + W / C,      H = 2 verification compressions,   C = 222 (blake3-r1)
P  = LD + ALU + ST + V
W  = 2·(LD + ALU + ST + V) + 2·LD
V  = 37           (digest EQ 32 + distinctness 4 + HALT 1)
LD = 9            (IV[0..7] and F; stress also LD = 11 with 11 and 64 loaded)
```

| Row | ALU | ST | LD | W | T | log2 T |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Primary 2-way program | 74 | 18 | 9 | 294 | 3.324 | 1.733 |
| Harshest stress (ST 32, LD 11, sub1) | 75 | 32 | 11 | **332** | 3.495 | **1.806** |
| Claim-1.81 ceiling `(2^1.81 − 2)·222` | | | | 334.43 | 3.506 | 1.81 |
| Same algebra, 4-way (`94e5361`) | 64 | 32 | 11 | 310 | 3.396 | 1.764 |
| Same algebra, serial | 87 | 32 | 11 | 356 | 3.604 | 1.849 |
| Prior scalar y-LSB (`fdc25b2`) | 79 | 32 | 9 | 332 | 3.496 | 1.806 |

We claim **1.81**, sized to lattice max `332 ≤ 334.43`. Claim **1.80** is not
made (`330/332 > 329.05`). Claim **1.77** is not made on this schedule.

**Construction summary.**
1. *Algebra.* All four columns use Lemma 5 `(C*,D*)=(0,−b)` so `B=C=0`, `D=−b`.
   Diagonals see `b=c=0`, `d∈{−IV7,−IV5}`; `M` uses `x=d−a`, `y=−d`; `M'`
   replaces only `w9,w13` by `~d` (Lemma 6′). Feed-forward pairs cancel.
2. *2-way schedule.* Pair `(G0,G1)` (`d=0`) and pair `(G2,G3)` (`d=(64,11)`)
   each run as two 64-bit lanes (32-bit value + 32-bit guard) in one 256-bit
   word; shared `M=F|(F<<64)`, `Gd=M<<32`; scalar diagonals with limb-mod
   `x`-words. No native rotate, no chaining, no rotation-AND elision.

Certificate `blake3-r1-swar-lemma5-pair` witnesses the Section 4 instance.

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



## 5. Algorithm (charged 2-way program)

Straight-line program on the 256-bit word RAM of `collision-frontier-v5`.
Primitives used: word `ADD`/`SUB` (mod `2^256`), `AND`/`OR`/`XOR`, `SHL`/`SHR`.
No rotate of any width. Every column `ADD`/`SUB` is lane-masked before further
arithmetic. Narrow rotations expand to `SHL+SHR+OR+AND`.

### 5.1 Lane layout (2-wide)

Each active vector holds **two** 64-bit lanes: bits `[0,32)` and `[64,96)` carry
values; bits `[32,64)` and `[96,128)` are guard gaps. Mask
`M = F | (F << 64)` and guard `Gd = M << 32`. Lane lemmas S1–S3 of the sibling
4-way package apply verbatim with lane count 2 (borrow still lands in an
all-ones gap; `vadd`/`vrotl` stay gap-clean after `AND M`).

**Limb-mod (diagonal `x`).** For any 256-bit words `a,b`,
`(a − b) mod 2^32 = (a_lo − b_lo) mod 2^32`. Therefore
`AND(SUB(nIV, A), F)` equals `AND(SUB(nIV, AND(A,F)), F)` when `nIV` is a clean
32-bit value. The program uses the shorter form and keeps the output `AND F`.
This is not rotation-AND elision and not chaining.

### 5.2 Program

| phase | ops | ALU |
| --- | --- | ---: |
| setup | `M = F|(F<<64)`, `Gd = M<<32` | 3 |
| pair1 `(G0,G1)` | pack Av,Bv (4); Lemma-5 body with `a1=vrotl(d1,16)` (22); unpack X,Y (4) | 30 |
| pair2 `(G2,G3)` | pack Av,Bv,Dv (6); Lemma-5 body (23); unpack (4) | 33 |
| diagonals | `nIV7=SHR(N2,64)`, `nIV5=SHR(N1,64)`, `w8=AND(SUB(nIV7,A1),F)`, `w12=AND(SUB(nIV5,A2),F)`, `w9p=XOR(w9,1)`, `w13p=XOR(w13,7)` | 8 |
| **total (xor7)** | | **74** |
| sub1 flip variant | `w13p = AND(SUB(w13,1),F)` instead of `XOR 7` | **75** |

Lane order inside each pair is `(lo,hi) = (G0,G1)` and `(G2,G3)`. Message words
are the same 16-word instance as Section 4 / the 4-way package.

### 5.3 Why `H = 2`, placement, and narrow EQ stay charged

Both compressions, program placement (1 op/instruction), constant-table
placement (2 ops/word), 8×32-bit digest EQ, and message-distinctness are
charged exactly as in the sibling package. `V = 37`. No omit-verify.

### 5.4 Why 2-wide lane-parallel arithmetic is in-model

`cost-models/collision-frontier-v5.json` gives a 256-bit word RAM with word
`ADD`/`SUB`/`AND`/`OR`/`XOR`/`NOT` and shift or rotation. Using two value
lanes separated by guard gaps is ordinary word-RAM programming; every mask,
pack, unpack, and guard is line-itemed above. We do **not** claim 4-wide
amortisation in this package. Serial same algebra is `W = 356` (below).

### 5.5 Certificate = witness, not advice

Certificate `blake3-r1-swar-lemma5-pair` (`swar-a.bin` / `swar-b.bin`) is an
organizer-checked collision witness for the Section 4 instance. It is not
nonuniform advice and does not replace charged collision checking.

## 6. Cost

### 6.1 Primary program

`ALU = 74`, `ST = 18`, `LD = 9`, `V = 37` ⇒ `P = 138` ⇒ `W = 2·138 + 18 = 294`
(`T = 2 + 294/222 ≈ 3.324`, `log2 ≈ 1.733`).

### 6.2 Claim ceiling

`(2^1.81 − 2)·222 ≈ 334.43`. Need harshest `W ≤ 334.43`.

### 6.3 Full stress lattice

Axes: `ST ∈ {18,32}`, `LD ∈ {9,11}`, flip ∈ {xor7, sub1}.

| ST | LD | flip | ALU | P | W | T | log2 T | ≤ 334.43? |
| ---: | ---: | :---: | ---: | ---: | ---: | ---: | ---: | :---: |
| 18 | 9 | xor7 | 74 | 138 | 294 | 3.324 | 1.733 | yes |
| 18 | 11 | xor7 | 74 | 140 | 302 | 3.360 | 1.749 | yes |
| 18 | 9 | sub1 | 75 | 139 | 296 | 3.333 | 1.737 | yes |
| 18 | 11 | sub1 | 75 | 141 | 304 | 3.369 | 1.752 | yes |
| 32 | 9 | xor7 | 74 | 152 | 322 | 3.450 | 1.787 | yes |
| 32 | 11 | xor7 | 74 | 154 | 330 | 3.486 | 1.802 | yes |
| 32 | 9 | sub1 | 75 | 153 | 324 | 3.459 | 1.791 | yes |
| **32** | **11** | **sub1** | **75** | **155** | **332** | **3.495** | **1.806** | **yes** |

Maximum `W = 332 ≤ 334.43` (margin ≈ 2.43). Claim **1.80** fails:
ceiling ≈ 329.05, and LD-11 rows are 330 and 332.

### 6.4 Comparison table (same algebra)

| Schedule | Harshest ALU | LD | ST | W | Fits claim |
| --- | ---: | ---: | ---: | ---: | --- |
| 4-way SWAR (`94e5361`) | 64 | 11 | 32 | 310 | 1.77 |
| **2-way SWAR (this package)** | **75** | **11** | **32** | **332** | **1.81** |
| Serial scalar Lemma-5 | 87 | 11 | 32 | 356 | ≈1.85 |
| Scalar y-LSB (`fdc25b2`) | 79 | 9 | 32 | 332 | 1.83 (LD11 → 340) |

### 6.5 Shaves deliberately not taken

Packed-IV, packed-store, packed-EQ, native ROT, chaining, rotation-AND
elision, omit-verify, ST=18-only shopping, and 4-wide amortisation are not
used. Limb-mod on diagonal `x` is used and defended in §5.1.

### 6.6 Why this is worth a parallel AR ticket

1. Same collision witness as `94e5361`, so mechanical validity is unchanged.
2. Resource claim depends only on **2-wide** packing — a strictly weaker
   SWAR assumption than 4-wide.
3. Beats promoted/awaiting scalar `fdc25b2` @1.83 under full locks including
   `LD = 11` (`332 ≤ 334.43`, whereas y-LSB's `LD = 11` row is `340 > 334.43`).
4. Does not cancel `94e5361`; if 4-wide is accepted, 1.77 remains the sharper
   claim. If 4-wide is rejected but 2-wide is accepted, this ticket still
   improves on 1.83.

## 7. Evidence and interpretation

- Lemmas 1, 5, 6′, S1–S3 and the Theorem are exact.
- Certificate verified by organizer intake at rounds = 1.
- Emulator Appendix A reproduces messages, digest, and every lattice row.
- Heuristic list empty; success probability 1; preprocessing 0.

## 8. Skeptic FAQ

**Q. Is this just the 1.77 package with a worse score?**
A. Same algebra/messages; different charged schedule. Claim 1.81 is the
honest 2-wide bound. The 1.77 ticket separately claims 4-wide.

**Q. Does limb-mod undercount masks?**
A. Output `AND F` is charged. Pre-mask on `A` is redundant for
`(a−b) mod 2^32` when `nIV` is a clean 32-bit word (§5.1). Emulator asserts
equality against the pre-masked form.

**Q. What if all SWAR is rejected?**
A. Serial same algebra is `W = 356` (needs ~1.85). Scalar y-LSB @1.83 remains
the best SWAR-free package already in AR (`fdc25b2`). This ticket is specifically
2-wide insurance, not serial insurance.

**Q. Why not claim 1.80?**
A. Harshest `W = 332 > 329.05`. LD-11 xor7 is already `330 > 329.05`.

## Appendix A. Ledger emulator (reviewer-run; not executed by intake)

```python
#!/usr/bin/env python3
"""2-way SWAR insurance emulator for blake3-r1 (Lemma-5 / y-flip).

Two 64-bit lanes (32-bit value + 32-bit guard gap) inside the 256-bit word RAM.
Pair1 = (G0,G1) with d=0 (skip XOR into a1). Pair2 = (G2,G3) with d=(64,11).
Diagonals use limb-mod SUB: (a-b) mod 2^32 depends only on low limbs, so the
pre-mask AND F on a multi-lane minuend/subtrahend is omitted when the result
is immediately AND-masked with F. No chaining, no rotation-AND elision, no
native ROT. Same messages as the 4-way package.
"""
import math, struct, sys
from pathlib import Path
sys.path.insert(0, str(Path('.').resolve()))  # run from repository root
from verifier.blake3 import blake3, IV

W256 = (1 << 256) - 1
F = 0xFFFFFFFF
COUNT = {}
_phase = ['']
TRACE = []

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
    _phase[0] = 'setup'
    M = OR(F, SHL(F, 64))                              # 2  two-lane mask
    Gd = SHL(M, 32)                                     # 1  gap guards
    pack2 = lambda lo, hi: OR(lo, SHL(hi, 64))          # 2
    vsub = lambda x, y: AND(SUB(OR(x, Gd), y), M)       # 3
    vadd = lambda x, y: AND(ADD(x, y), M)               # 2
    vrotl = lambda x, k: AND(OR(SHL(x, k), SHR(x, 32 - k)), M)  # 4
    lanes2 = lambda V: (AND(V, F), SHR(V, 64))          # 2 (top clean)

    # pair1: (G0,G1), d=0 — skip XOR into a1
    _phase[0] = 'pair1'
    Av = pack2(IV[0], IV[1])                            # 2
    Bv = pack2(IV[4], IV[5])                            # 2
    d1 = vsub(Bv, Av)                                   # 3
    a1 = vrotl(d1, 16)                                  # 4  (Dv=0)
    S = vadd(Av, Bv)                                    # 2
    X = vsub(a1, S)                                     # 3
    N1 = AND(SUB(Gd, Bv), M)                            # 2  (-IV4,-IV5)
    A1 = XOR(vrotl(N1, 8), d1)                          # 5
    Y = vsub(A1, a1)                                    # 3
    w0, w2 = lanes2(X)                                  # 2
    w1, w3 = lanes2(Y)                                  # 2

    # pair2: (G2,G3), d=(64,11)
    _phase[0] = 'pair2'
    Av = pack2(IV[2], IV[3])                            # 2
    Bv = pack2(IV[6], IV[7])                            # 2
    Dv = pack2(64, 11)                                  # 2
    d1 = vsub(Bv, Av)                                   # 3
    a1 = XOR(Dv, vrotl(d1, 16))                         # 5
    S = vadd(Av, Bv)                                    # 2
    X = vsub(a1, S)                                     # 3
    N2 = AND(SUB(Gd, Bv), M)                            # 2  (-IV6,-IV7)
    A2 = XOR(vrotl(N2, 8), d1)                          # 5
    Y = vsub(A2, a1)                                    # 3
    w4, w6 = lanes2(X)                                  # 2
    w5, w7 = lanes2(Y)                                  # 2

    _phase[0] = 'diagonals'
    # Limb-mod: (a-b) mod 2^32 = (a_lo-b_lo) mod 2^32, so no pre-AND on A1/A2.
    nIV7 = SHR(N2, 64)                                  # 1  top clean = -IV7
    nIV5 = SHR(N1, 64)                                  # 1  = -IV5
    w8 = AND(SUB(nIV7, A1), F)                          # 2  = -IV7 - A0
    w12 = AND(SUB(nIV5, A2), F)                         # 2  = -IV5 - A2
    assert w8 == ((nIV7 - (A1 & F)) & F)
    assert w12 == ((nIV5 - (A2 & F)) & F)
    w9, w13 = IV[7], IV[5]
    w9p = XOR(w9, 1)                                    # 1
    if flip == 'xor7':
        w13p = XOR(w13, 7)                              # 1
    else:
        w13p = AND(SUB(w13, 1), F)                      # 2

    words = [w0, w1, w2, w3, w4, w5, w6, w7, w8, w9, 0, 0, w12, w13, 0, 0]
    words = [w & F for w in words]
    assert all(0 <= w <= F for w in words)
    m = struct.pack('<16I', *words)
    words[9], words[13] = w9p & F, w13p & F
    mp = struct.pack('<16I', *words)
    return m, mp, dict(COUNT)

def lattice_table():
    C, V = 222, 37
    print('ceilings:', {k: round((2**k - 2) * C, 2) for k in (1.77, 1.80, 1.81, 1.82, 1.83)})
    rows = []
    for flip in ('xor7', 'sub1'):
        m, mp, cnt = program(flip)
        alu = sum(cnt.values())
        ok = m != mp and blake3(m, 1) == blake3(mp, 1)
        print(f'\nflip={flip}: ALU={alu} {cnt} collision={ok}')
        print(f'  digest={blake3(m,1).hex()}')
        for ST in (18, 32):
            for LD in (9, 11):
                P = LD + alu + ST + V
                Wt = 2 * P + 2 * LD
                T = 2 + Wt / C
                rows.append((flip, ST, LD, alu, Wt, T))
                print(f'  ST={ST:2d} LD={LD:2d}  P={P}  W={Wt}  T={T:.4f}  log2T={math.log2(T):.4f}'
                      f'  <=1.81:{Wt <= (2**1.81-2)*C}  <=1.80:{Wt <= (2**1.80-2)*C}')
    return rows

if __name__ == '__main__':
    lattice_table()
    m, mp, _ = program('xor7')
    print('\nM  =', m.hex())
    print("M' =", mp.hex())
    print('differing words:', [i for i in range(16) if m[4*i:4*i+4] != mp[4*i:4*i+4]])

```
