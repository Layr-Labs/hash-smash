# BLAKE3 one-round explicit ordinary collisions: a deterministic zero-digest pair

## 0. Statement

Target `blake3-r1-prefix-v1`: unkeyed BLAKE3-256 with `rounds = 1`, messages
of exactly 64 bytes (one root chunk block: `CHUNK_START | CHUNK_END | ROOT` =
flags 11, block length 64, counter 0). We exhibit two explicit 64-byte
messages `M` and `M'` with `blake3(M, 1) = blake3(M', 1) = 0^256`, produced by
a deterministic straight-line program. Primary ledger on the selected
256-bit-word machine: **323 charged word operations** = 203 data-path ops
(151 instructions) + 112 packing ops + 8 packed 256-bit stores, against the
organizer reference `C = 222` (`scripts/reference_operation_costs.py`,
`blake3-r1 = 222`). `log2(323/222) = 0.541`; we claim the conservatively
rounded bound `time_log2 = 0.55`. No randomness, no trials, no compression
evaluation, no collision check, no restart, no precomputed pair, no advice
string: `success_probability = 1`, `preprocessing = 0`. The constructor
itself is attached as the organizer-executed experiment program
`experiments/builder.py` (Section 8), so the ledger numbers below are read
from its organizer-run output, not merely asserted.

## 1. Anatomy of the single compression

`verifier/blake3.py` builds `v = cv[0..7] || IV[0..3] || [c_lo, c_hi, len,
flags]`. For our target `cv = IV`, `v[8..11] = IV[0..3]`, `v[12] = v[13] = 0`,
`v[14] = 64`, `v[15] = 11`. One round applies eight `G` functions:

- columns `Gc_k = G(k, k+4, k+8, k+12; m[2k], m[2k+1])`, `k = 0..3`;
- diagonals `Gd_0 = G(0,5,10,15; m[8], m[9])`, `Gd_1 = G(1,6,11,12; m[10],
  m[11])`, `Gd_2 = G(2,7,8,13; m[12], m[13])`, `Gd_3 = G(3,4,9,14; m[14],
  m[15])`,

where `G(a,b,c,d; x,y)` is (`MASK = 0xFFFFFFFF`, all adds masked):

```
a1 = (a + b + x)        d1 = ror16(d ^ a1)   c1 = (c + d1)   b1 = ror12(b ^ c1)
A  = (a1 + b1 + y)      D  = ror8(d1 ^ A)    C = (c1 + D)    B = ror7(b1 ^ C)
```

The output digest words are `o_i = v[i] ^ v[i+8]`, `i = 0..7`. Two facts drive
everything:

1. The four diagonal `G` functions overwrite **all** 16 state words. Column
   outputs matter only as diagonal inputs.
2. Each message pair `(x, y)` enters exactly one `G`, only through
   `a1 = a + b + x` and `A = a1 + b1 + y`.

Hence: if every diagonal output `(A, B, C, D)` is chosen so that each pair
`v[i], v[i+8]` XORs to zero, the digest is `0^256`; and the message words are
whatever the solved `G` instances require. This reduces "find a collision" to
eight independent one-`G` inversions with the digest conditions transferred
onto `G` outputs.

## 2. Lemma 1 (diagonal solver: target the (C, D) outputs)

Given inputs `a, b, c, d` and design targets `(Ct, Dt)`, set

```
c1 = Ct - Dt                    d1 = c1 - c
a1 = d ^ rol16(d1)              x  = a1 - a - b
b1 = ror12(b ^ c1)              A  = rol8(Dt) ^ d1
y  = A - a1 - b1                B  = ror7(b1 ^ Ct)
```

(Every sum/difference is masked to 32 bits; `rol_n` = rotate left.)

**Proof.** Substitute into the `G` equations. `C = c1 + D` with
`D = ror8(d1 ^ A) = ror8(d1 ^ rol8(Dt) ^ d1) = Dt`, so `C = c1 + Dt - Dt = Ct`
because `c1 = Ct - Dt`. `d1 = ror16(d ^ a1)`: `d ^ a1 = rol16(d1)` by
construction, so `ror16` returns `d1`. `a1 = a + b + x` holds since
`x = a1 - a - b`. `b1, B` are read off directly, and `A = a1 + b1 + y` holds
since `y = A - a1 - b1`. `QED`. The solver realizes any `(C, D)` pair with
free `(A, B)` determined by it; `(x, y)` are the two message words.

## 3. Lemma 2 (column solver: target the (B, C) outputs)

Given inputs `a, b, c, d` and design targets `(Bt, Ct)`, set

```
b1 = rol7(Bt) ^ Ct              c1 = b ^ rol12(b1)
d1 = c1 - c                     D  = Ct - c1
a1 = d ^ rol16(d1)              x  = a1 - a - b
A  = rol8(D) ^ d1               y  = A - a1 - b1
```

**Proof.** `B = ror7(b1 ^ C)`: with `C = c1 + D = c1 + Ct - c1 = Ct` and
`b1 ^ Ct = rol7(Bt)`, `B = Bt`. `d1 = ror16(d ^ a1)` as in Lemma 1;
`c1 = b ^ rol12(b1)` inverts `b1 = ror12(b ^ c1)`; the two subtractions
invert the two masked additions for `x`, `y`. `QED`. Columns are solved for
`(B, C)` because those two outputs are exactly the `b`, `c` inputs of the
diagonal `G` functions (concretely `b_in(Gd_j)` and `c_in(Gd_j)` are column
`B`/`C` outputs), while the columns' `A`, `D` outputs (feeding diagonal `a`,
`d` inputs) stay free.

## 4. Message `M`: the zero point

Solve all four columns for `(B, C) = (0, 0)` (Lemma 2) and then all four
diagonals for `(C, D) = (0, 0)` with `a, b, c, d` equal to the solved column
outputs. Every diagonal output is `(A,B,C,D) = (0,0,0,0)`, so the final state
is `v = 0^512` and `o_i = 0 ^ 0 = 0`: `blake3(M, 1) = 0^256`. The eight
solver instances write all 16 message words; the instance values are exact
closed forms in the IV constants (Section 6 lists the bytes).

## 5. The companion `M'(C0, D0)`: a universal compensation family

Let `(C0, D0)` be **any** pair of 32-bit design constants. Keep every column
target at zero except columns 0 and 3, and keep every diagonal target at zero
except `Gd0` and `Gd2`, which are re-targeted:

- `Gd0'` target `(C, D) = (C0, D0)`.
- `Gd2'` targets `(C, D) = (A0', B0')`, taken **at runtime** from `Gd0'`'s own
  `A`, `B` outputs.
- Column 0 keeps `B = 0`, target `C = K` (compensation constant).
- Column 3 keeps `C = 0`, target `B = L` (compensation constant).

Define the design constants (`K`, `L`) from `(C0, D0)`:

```
c1 = C0 - D0            A0 = rol8(D0) ^ c1            b1 = ror12(c1)
B0 = ror7(b1 ^ C0)      K  = (A0 - B0) - (C0 ^ rol8(B0))
b12 = rol7(D0) ^ A0     L  = rol12(b12) ^ (A0 - B0)
```

**Key observation.** In `Gd0'`, `c_in = v10` (column 2 `C` target = 0) and
`b_in = v5` (column 1 `B` target = 0), so `A0' = rol8(D0) ^ (C0 - D0) = A0`
and `B0' = ror7(ror12(C0 - D0) ^ C0) = B0`: the `Gd0'` outputs `A, B` do not
depend on its `a, d` inputs (which do change, because column 0 was
re-solved). Hence the runtime targets `A0', B0'` equal the closed forms above.

**Theorem.** With `(K, L)` as defined, for every `(C0, D0)`, the program
above emits a message `M'` whose digest is `0^256`.

*Proof.* All eight digest words are 0:

- `o0 = v0' ^ v8' = A0' ^ Ct2' = A0' ^ A0' = 0`: a runtime data-flow identity,
  since `v0'` is `Gd0'`'s A output and `v8'` is `Gd2'`'s C target set to it.
- `o5 = v5' ^ v13' = B0' ^ Dt2' = 0`: same, via `B`.
- `o2 = v2' ^ v10' = A2' ^ C0`: by Lemma 1 on `Gd2'`,
  `A2' = rol8(Dt2') ^ d1_2 = rol8(B0) ^ ((A0 - B0) - K)` because
  `c1_2 = Ct2' - Dt2' = A0 - B0` and `c_in2 = v8` (column phase) `= K`.
  The disclosed `K` gives `(A0 - B0) - K = C0 ^ rol8(B0)`, so
  `A2' = rol8(B0) ^ rol8(B0) ^ C0 = C0` and `o2 = 0`.
- `o7 = v7' ^ v15' = B2' ^ D0`: Lemma 1 gives
  `B2' = ror7(b1_2 ^ Ct2')` with `b1_2 = ror12(b_in2 ^ c1_2)` and
  `b_in2 = v7` (column phase) `= L`. The disclosed `L` yields
  `b1_2 = rol7(D0) ^ A0`, hence `B2' = ror7(rol7(D0) ^ A0 ^ A0) = D0`,
  `o7 = 0`.
- `o1 = v1' ^ v9' = A1' ^ 0`: `Gd1'` has targets `(0,0)` and inputs
  `b = c = 0`, so `d1_1 = c1_1 - c_in1 = (0 - 0) - 0 = 0` and
  `A1' = rol8(0) ^ 0 = 0`.
- `o3 = v3' ^ v11' = A3' ^ 0 = 0`: identically, `Gd3'` inputs `b = c = 0`
  (`b_in3 = v4 =` column 0 `B` target `= 0`, `c_in3 = v9 =` column 1 `C`
  output `= 0`).
- `o4 = v4' ^ v12' = B3' ^ 0 = 0` and `o6 = v6' ^ v14' = B1' ^ 0 = 0`: both
  `b1` terms reduce to `ror12(0 ^ 0) = 0` and both `C` targets are 0.

`M' != M` because word `w0'` differs: in `M`, `w0 = a1 - IV0 - IV4` with
`a1 = 0`; in `M'`, `a1' = ror16(d1')` with `d1' = c1' - IV0`,
`c1' = IV4 ^ rol12(K)`; `K = 0xFE0000FD != 0`, and the solved pairs differ in
11 of 16 words for the submitted instance. `QED`.

Determinism: every value is a closed-form function of public constants
(`IV`, 64, 11, `C0 = D0 = 1`, and the two disclosed design constants
`K = 0xFE0000FD`, `L = 0xFE180100`); the program contains no branch, no
comparison, no random word, and it never evaluates the compression function.
Nothing is searched: `(C0, D0) = (1, 1)` is an arbitrary published choice —
the theorem holds for all `2^64` points, so no selection cost can attach.

## 6. Concrete instance (submitted certificate)

Design constants: `C0 = D0 = 1`; `c1 = 0`; `A0 = 0x00000100`; `b1 = 0`;
`B0 = 0x02000000`; `K = 0xFE0000FD`; `L = 0xFE180100`.

```
M  = 1eae00b1b20691aa8cc89a63c6ee026b3716478a85d0f8b848f4aed6e079c2d1
     3145758d19cde05b1edfe6897f520e519be3c7c58c68059bdaf5d936abd9831f
M' = 11ae20eca0114c738cc89a63c6ee026b3716478a85d0f8b849ec6e471840b561
     93c89393d93ee753fba4f387a28c01539be2aec70d67069b22b7262aabd9831f
```

`M != M'` in 11 of 16 words. Common digest:
`0000000000000000000000000000000000000000000000000000000000000000`.

| file | bytes | SHA-256 |
|---|---:|---|
| `certificates/msg_a.bin` (M)  | 64 | `fa353d560c33bdbc46669b602dadc533b7227b2f5d7c119797028af874e872d1` |
| `certificates/msg_b.bin` (M') | 64 | `6c66b5cd722d8d9f1455f93fbcd48122190b2286f620041a79eda3372b459716` |

## 7. Cost ledger (unit = 1/222 of one 1-round compression)

Conventions, aligned with `scripts/reference_operation_costs.py` and the
collision-frontier-v5 primitive list on the selected 256-bit-word machine:
masked add/sub costs 2 (arith + mask); `xor`, `or`, `and`, each shift cost 1;
a 32-bit rotation costs 4 (`shl`, `shr`, `or`, `and` — no native rotate);
packing and stores are modeled as disclosed below (the model's load/store
primitive is 256-bit). Every solver-formula step executes, **including steps
whose operands are constants** (rotations of design constants are charged the
full 4, which is conservative versus treating them as immediate operands).
Only provable identities against literal zero (`u + 0`, `u ^ 0`, `u - 0`,
`rot(0)`) are folded away at design time. Common subexpression elimination is
applied across the whole two-message program (shared column re-solves cost
0). All ledger numbers are emitted by the organizer-run constructor program
itself (`experiments/builder.py`, Section 8), not hand-asserted.

Per-`G` data-path measurement of the emitted straight-line program:

| part | ops | what runs |
|---|---:|---|
| `col0..col3` (M)      | 19+19+20+20 = 78 | Lemma-2 solves, targets (0,0) |
| `Gd0..Gd3` (M)        | 4 x 4 = 16 | Lemma-1 solves, targets (0,0) (most steps are zero-identities) |
| `col0'` (M')          | 26 | Lemma-2, target (0, K) |
| `col1', col2'` (M')    | 0 | targets unchanged: CSE, no recompute |
| `col3'` (M')          | 31 | Lemma-2, target (L, 0) |
| `Gd0'` (M')           | 14 | Lemma-1, target (C0, D0) |
| `Gd1'` (M')           | 4  | re-solve: `d` input changed (column 0 `D`) |
| `Gd2'` (M')           | 32 | Lemma-1, runtime target `(A0', B0')`, inputs `L, K` |
| `Gd3'` (M')           | 2  | re-solve: `a` input changed (column 3 `A`) |
| data-path subtotal    | **203** | 151 executed instructions |
| packing               | 112 | two 64-byte messages from solved 32-bit lanes into eight 256-bit words: 2 x 4 words x 7 merges x {shl, or} |
| stores (256-bit)      | 8   | 8 packed words = the two complete messages |
| **charged total**     | **323** | `323/222 = 1.4550` units; `log2 = 0.541` |

Claimed bound: `time_log2 = 0.55` (conservative rounding of 0.541).

**Register residency and traffic.** The emitted program allocates 144
temporary registers; a liveness scan of the emitted order (computed by the
program itself and reported in its organizer-run observations) shows at most
34 values live at any point, so every intermediate is register-resident with
no spill, no intermediate load or store, and no indexing. Packing reads the
solved lane registers and writes the packed words; after packing, only the 8
words are retained. The instruction stream holds all 21 distinct constants as
immediate operands; the algorithm performs no data-table read.

**Memory layout** (`memory_log2_bytes = 13`, i.e. 8 KiB): 271 instructions
(151 + 112 + 8) at a generous 16 B encoding = 4336 B; register file at 34
peak live x 32 B = 1088 B; the two 64-byte messages = 128 B; total
**5552 B < 8192 B**. Code and messages are the only retained state.

**Disclosed alternative readings** (outside the primary ledger; following the
accounting-disclosure style of public ticket 754f0f2 on this track):

| reading | total | log2(·/222) | stated bound |
|---|---:|---:|---|
| claimed: 203 + 112 packing + 8 packed stores | 323/222 = 1.455 | 0.541 | `time_log2 = 0.55` |
| 32-bit-store machine (packing unnecessary) | 235/222 = 1.059 | 0.082 | <= 0.1 |
| data-path only (no packing, no stores) | 203/222 = 0.914 | -0.13 | below one compression |
| + 21 constant loads (no-immediates machine) | 344/222 = 1.550 | 0.631 | <= 0.7 |
| + table preprocessing over-charge (2 x 21) | 365/222 = 1.644 | 0.719 | <= 0.8 |
| + self-check (2 compressions + compare + distinctness) | 2 + 371/222 = 3.676 | 1.88 | <= 1.9 |

Under every reading the cost is a small constant, far below the nominal 128
and far below the incumbent generic bound (149). The construction never needs
a self-check: the pair identity is proved above and recomputed organizer-side
by the certificate; a check could not change the output or the success
probability, so it is not part of the charged algorithm.

## 8. Evidence chain (organizer-executed, no participant code in the judge)

- `experiments/manifest.json` declares one `python-message-pairs-v1`
  experiment whose program is `experiments/builder.py`, the constructor
  itself: pure stdlib, deterministic, isolated by the organizer runner,
  executed twice byte-identically for reproducibility. The organizer
  recomputes the collision predicate over returned pairs with the trusted
  rounds=1 digest; the program returns exactly the two Section 6 certificate
  byte strings on every trial.
- The same program emits, as numeric observations in its organizer-run
  output, every ledger and liveness number of Section 7: data-path ops 203,
  instructions 151, packing ops 112, packed stores 8, charged totals 323
  (packed) and 235 (word stores), allocated registers 144, peak live values
  34, differing words 11, immediate constants 21.
- `certificates/manifest.json` declares one `hash-collision-witness-v2` over
  the two Section 6 files with expected digest `0^64` hex; the organizer
  verifier recomputed both digests at intake (mechanical check:
  `mechanically_valid`, 1 certificate verified).
- Independently, the emitted instruction list was re-executed by a second
  mechanical counter in local review and agreed at 203 data-path ops.

## 9. Scope and limitations

- Straight-line, single-block messages only (64 bytes); the construction
  makes no claim about full 7-round BLAKE3 or multi-block messages.
- The solver inverts one compression end-to-end; it is an explicit
  algebraic inversion, not a differential trail, and applies because one
  round's eight `G` functions decouple as in Section 1. The BLAKE line of
  work on inverting `G` (Aumasson, Guo, Knellwolf, Matusiewicz, Meier, FSE
  2010, ePrint 2010/043) motivates Lemmas 1-2; the pair construction, the
  universal-family theorem, and the cost accounting here are independent.
- The claimed `time_log2 = 0.55` is a conservative rounding of the packed
  reconstruction `log2(323/222) = 0.541` on the selected 256-bit-word
  machine; cheaper machines/readings are disclosed in Section 7 with stated
  bounds, all small constants.
- The observation numbers are reported by the participant program; their
  role is to make the ledger machine-checkable against the source, which the
  organizer stores and the reviewer can read; the collision itself does not
  depend on them (the certificate covers it).
