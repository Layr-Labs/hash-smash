# Deterministic collision for 1-round BLAKE3: uniform Lemma-5 columns in 2-wide top-lane SWAR plus y-flip (insurance schedule)

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is reported
separately as a resource bound.

This exploratory package targets `blake3-r1-prefix-v1`. It gives a classical,
deterministic algorithm. It succeeds with probability 1, its total charged time
is at most `2^1.79` target-compression units, and its peak memory is at most
`2^16` bytes. The construction uses only public IV constants and exact modular
identities of the BLAKE3 `G` function. The heuristic list is empty.

**Parallel-AR / insurance role.** Algebra and messages are bit-identical to the
4-way top-lane package awaiting review as `4a200f9` @1.76 (harshest `W = 304`)
and to the earlier 2-way insurance `1f80563` @1.81 (harshest `W = 332`). This
package charges a **2-lane top-of-word** schedule (harshest `W = 322`) so the
resource claim survives if reviewers reject 4-wide packing but accept 2-wide
packing, and it materially beats `1f80563` by the same top-lane dead-mask
saving used in `4a200f9`. It does **not** cancel or replace `4a200f9`,
`1f80563`, or `94e5361`.

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
| Primary 2-way top-lane program | 69 | 18 | 9 | 284 | 3.279 | 1.713 |
| Harshest stress (ST 32, LD 11, sub1) | 70 | 32 | 11 | **322** | 3.450 | **1.7868** |
| Claim-1.79 ceiling `(2^1.79 − 2)·222` | | | | 323.71 | 3.458 | 1.79 |
| Prior 2-way insurance (`1f80563`) | 75 | 32 | 11 | 332 | 3.495 | 1.806 |
| Same algebra, 4-way top-lane (`4a200f9`) | 61 | 32 | 11 | 304 | 3.369 | 1.7525 |
| Same algebra, serial top-field | 84 | 32 | 11 | 350 | 3.577 | 1.839 |
| Prior scalar y-LSB (`fdc25b2`) | 79 | 32 | 9 | 332 | 3.496 | 1.806 |

We claim **1.79**, sized to lattice max `322 ≤ 323.71` (margin ≈ 1.71). Claim
**1.78** is not made (`322 > 318.40`). Claim **1.76** is not made on this
schedule.

**What changed vs `1f80563` @1.81.** Lane offsets move from `(0,64)` to
`(0,224)`: the high lane is the top 32 bits of the word. By Lemmas S4/S5
(same statements as in `4a200f9`), `SHR(V,224)` is always a clean 32-bit word
and `extract(V AND M) = extract(V)` for every `V`, so the vector `AND M` on
extract-only `X`/`Y` is dead code (−2 per pair: one on `X`, one on `Y`), and the
top-field diagonal `w12` needs no `AND F` (−1). ALU 75 → 70, harshest W 332 → 322.

**Construction summary.**
1. *Algebra.* All four columns use Lemma 5 `(C*,D*)=(0,−b)` so `B=C=0`, `D=−b`.
   Diagonals see `b=c=0`, `d∈{−IV7,−IV5}`; `M` uses `x=d−a`, `y=−d`; `M'`
   replaces only `w9,w13` by `~d` (Lemma 6′). Feed-forward pairs cancel.
2. *2-way top-lane schedule.* Pair `(G0 low, G1 top)` (`d=0`) and pair
   `(G3 low, G2 top)` (`d=(11,64)`) each run as two lanes at offsets
   `(0,224)`; shared `M=F|(F<<224)`, `Gd=SHL(M,32)`. Raw `X`/`Y` extracted by
   `AND F` / `SHR 224`. Diagonals: limb-mod low `w8` and guarded top `w12`.
   No native rotate, no chaining, no rotation-AND elision.

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
the two small-constant forms of the flip:
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

so `o0 = o2 = o5 = o7 = 0`, as predicted. Certificate `blake3-r1-swar-lemma5-pair`
stores these exact bytes (same witness as `4a200f9` / `1f80563` / `94e5361`).

## 5. Algorithm (charged 2-way top-lane program)

Straight-line program on the 256-bit word RAM of `collision-frontier-v5`.
Primitives used: word `ADD`/`SUB` (mod `2^256`), `AND`/`OR`/`XOR`, `SHL`/`SHR`.
No rotate of any width. Every column `ADD`/`SUB` that feeds further arithmetic
or a rotation is lane-masked. Narrow rotations expand to `SHL+SHR+OR+AND`.

### 5.1 Lane layout (2-wide top-lane)

Lanes sit at bit offsets `(0, 224)`:

- Lane 0: value `[0,32)`, guard gap `[32,64)` filled by `Gd`.
- Lane 1: value `[224,256)` — the **top 32 bits** of the word. No gap, no guard.

Shared mask `M = F | (F << 224)` and guard `Gd = SHL(M, 32)` (the top copy of
`Gd` leaves the word). 

**Lemma S4 (top lane).** For every 256-bit `V`, `SHR(V,224) ∈ [0,2^32)`. Word
width alone; no cleanliness hypothesis.

**Lemma S5 (dead-mask extract).** Write
`extract(V) = (AND(V,F), SHR(V,224))`. For every 256-bit `V`,
`extract(V AND M) = extract(V)` because both windows lie inside `M`. So a
vector `AND M` before extracting an unpack-only raw guarded difference is dead
code. This is not chaining: the raw word is never an arithmetic operand.

**Limb-mod (low diagonal `x`).** For any 256-bit words `a,b`,
`(a − b) mod 2^32 = (a_{lo} − b_{lo}) mod 2^32`. Therefore
`AND(SUB(N_pair2, A_pair1), F)` needs no pre-mask on the multi-lane operands
when the result is immediately `AND F`. Output mask kept. Not chaining.

**Guarded top diagonal `x`.** `w12 = SHR((N_pair1 OR Gd) − A_pair2, 224)` uses
the lane-0 guard so that no borrow enters the top field (S1 with one lower
lane); S4 makes the `SHR` a clean 32-bit word with no `AND F`.

### 5.2 Program

| phase | ops | ALU (xor7) |
| --- | --- | ---: |
| setup | `M = F\|(F<<224)`, `Gd = M<<32` | 3 |
| pair1 `(G0,G1)` d=0 | pack Av,Bv (4); body with `a1=vrotl(d1,16)` (no Dv XOR); raw X/Y; extract (2+2) | 28 |
| pair2 `(G3,G2)` | pack Av,Bv,Dv (6); full Lemma-5 body; raw X/Y; extract | 31 |
| diagonals | `w8 = AND(SUB(N2,A1),F)` (2); `w12 = SHR((N1\|Gd)−A2, 224)` (3) | 5 |
| flips | `w9p = XOR(IV7,1)`; `w13p = XOR(IV5,7)` | 2 |
| **total (xor7)** | | **69** |
| sub1 flip variant | `w13p = AND(SUB(IV5,1),F)` | **70** |

Lane order: pair1 `(lo,hi) = (G0,G1)`; pair2 `(lo,hi) = (G3,G2)` so the top
lane of pair2 carries G2 (needed for `w12 = −IV5 − A2`) and the low lane of
pair2 carries G3 (needed for `w8 = −IV7 − A0` via `N2`'s low limb `−IV7`).

### 5.3 Why `H = 2`, placement, and narrow EQ stay charged

Both compressions, program placement (1 op/instruction), constant-table
placement (2 ops/word), 8×32-bit digest EQ, and message-distinctness are
charged. `V = 37`. No omit-verify.

### 5.4 Why 2-wide top-lane packing is in-model

`cost-models/collision-frontier-v5.json` gives a 256-bit word RAM with word
`ADD`/`SUB`/`AND`/`OR`/`XOR`/`NOT` and shift or rotation. Two value lanes with
one top-of-word field is ordinary word-RAM programming; every mask, pack,
unpack, and guard is line-itemed above. We do **not** claim 4-wide
amortisation in this package. Serial top-field same algebra is `W = 350`.

### 5.5 Certificate = witness, not advice

Certificate `blake3-r1-swar-lemma5-pair` (`swar-a.bin` / `swar-b.bin`) is an
organizer-checked collision witness for the Section 4 instance. It is not
nonuniform advice and does not replace charged collision checking.

### 5.6 Harsher readings priced and refused

| Skeptic add-on | ΔALU | Why refused |
| --- | ---: | --- |
| `AND M` on raw `X`/`Y` before extract | +2 | Dead code (S5) for every input |
| `AND F` on top-lane extracts | +2 | S4 word-width fact |
| Force gapped high lane (revert to `1f80563`) | +5 | Restores W=332; not a model rule |
| Packed table lane vectors / unmasked `S` | large | refused locks (peer `9a8d44a`) |

## 6. Cost

### 6.1 Primary program

`ALU = 69`, `ST = 18`, `LD = 9`, `V = 37` ⇒ `P = 133` ⇒ `W = 2·133 + 18 = 284`
(`T = 2 + 284/222 ≈ 3.279`, `log2 ≈ 1.713`).

### 6.2 Claim ceiling

`(2^1.79 − 2)·222 ≈ 323.71`. Need harshest `W ≤ 323.71`.

### 6.3 Full stress lattice

Axes: `ST ∈ {18,32}`, `LD ∈ {9,11}`, flip ∈ {xor7, sub1}.

| ST | LD | flip | ALU | P | W | T | log2 T | ≤ 323.71? |
| ---: | ---: | :---: | ---: | ---: | ---: | ---: | ---: | :---: |
| 18 | 9 | xor7 | 69 | 133 | 284 | 3.279 | 1.713 | yes |
| 18 | 11 | xor7 | 69 | 135 | 292 | 3.315 | 1.729 | yes |
| 18 | 9 | sub1 | 70 | 134 | 286 | 3.288 | 1.717 | yes |
| 18 | 11 | sub1 | 70 | 136 | 294 | 3.324 | 1.733 | yes |
| 32 | 9 | xor7 | 69 | 147 | 312 | 3.405 | 1.768 | yes |
| 32 | 11 | xor7 | 69 | 149 | 320 | 3.441 | 1.783 | yes |
| 32 | 9 | sub1 | 70 | 148 | 314 | 3.414 | 1.772 | yes |
| **32** | **11** | **sub1** | **70** | **150** | **322** | **3.450** | **1.7868** | **yes** |

Maximum `W = 322 ≤ 323.71` (margin ≈ 1.71). Claim **1.78** fails:
ceiling ≈ 318.40 < 322.

### 6.4 Comparison table (same algebra)

| Schedule | Harshest ALU | LD | ST | W | Fits claim |
| --- | ---: | ---: | ---: | ---: | --- |
| 4-way top-lane (`4a200f9`) | 61 | 11 | 32 | 304 | 1.76 |
| **2-way top-lane (this package)** | **70** | **11** | **32** | **322** | **1.79** |
| Prior 2-way (`1f80563`) | 75 | 11 | 32 | 332 | 1.81 |
| Serial top-field | 84 | 11 | 32 | 350 | ≈1.84 |
| Scalar y-LSB (`fdc25b2`) | 79 | 9 | 32 | 332 | 1.83 (LD11 → 340) |

### 6.5 Shaves deliberately not taken

Packed-IV, packed-store, packed-EQ, native ROT, chaining, rotation-AND
elision, omit-verify, ST=18-only shopping, unmasked-`S`, guard-absorbs-carry,
and 4-wide amortisation are not used.

### 6.6 Why this is worth a parallel AR ticket

1. Same collision witness as `4a200f9` / `1f80563`, so mechanical validity is unchanged.
2. Resource claim depends only on **2-wide** packing — a strictly weaker SWAR
   assumption than 4-wide.
3. Materially beats `1f80563` @1.81 (`W 332 → 322`, claim 1.81 → 1.79) by the
   top-lane dead-mask identity already defended for the 4-way package.
4. Does not cancel `4a200f9` or `1f80563`; if 4-wide is accepted, 1.76 remains
   sharper. If 4-wide is rejected but 2-wide is accepted, this ticket improves
   on both 1.81 and 1.83.

## 7. Evidence and interpretation

- Lemmas 1, 5, 6′, S4, S5 and the Theorem are exact.
- Certificate verified by organizer intake at rounds = 1.
- Emulator Appendix A reproduces messages, digest, ALU 69/70, and every lattice
  row; serial top-field fallback prints `W = 350`.
- Heuristic list empty; success probability 1; preprocessing 0.

## 8. Skeptic FAQ

**Q. Is this just the 1.76 package with a worse score?**
A. Same algebra/messages; different charged schedule. Claim 1.79 is the honest
2-wide top-lane bound. The 1.76 ticket separately claims 4-wide.

**Q. Isn't dropping `AND M` on `X`/`Y` the fused-unmasked extract that was refused?**
A. No. S5 is a bit-window identity for every 256-bit word; every stored extract
is a clean 32-bit value (S4 for the top lane). The refused form stored a dirty
word. See also `4a200f9` §5.1 / §8.

**Q. Can a skeptic force the masks back?**
A. Only by charging dead code or inventing a symmetry-gap rule. That restores
`1f80563` (`W = 332`) without changing any stored bit (§5.6).

**Q. What if all SWAR is rejected?**
A. Serial top-field same algebra is `W = 350` (~1.84). Scalar y-LSB @1.83
(`fdc25b2`) remains the best SWAR-free package already in AR.

**Q. Why not claim 1.78?**
A. Harshest `W = 322 > 318.40`.

## Appendix A. Ledger emulator (reviewer-run; not executed by intake)

```python
#!/usr/bin/env python3
"""Reviewer-side 2-way top-lane insurance emulator (proof.md Section 5).
Save as ledger_emulator.py at the repository root and run python3 ledger_emulator.py.
Lanes at offsets (0,224): lane 0 has a 32-bit guard; lane 1 is the top 32 bits
(Lemma S4). X/Y extracted from raw guarded diffs (Lemma S5). Same messages as
4a200f9 / 1f80563. Also prints the serial top-field fallback."""
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
