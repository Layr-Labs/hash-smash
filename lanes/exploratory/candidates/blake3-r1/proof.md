# A deterministic O(1)-work ordinary collision for 1-round BLAKE3 (blake3-r1-prefix-v1) — final hardened package

Closed-form constructor, machine-verified witness pair, and an
organizer-declared experiment that **encodes, decodes, and executes the
claimed straight-line listing itself**. Claimed `time_log2 = 1.60`
target-compressions (ledger: 1.5139 primary, 1.5871 worst legitimate
sensitivity row), `success_probability = 1`, heuristics: none, nonuniform
advice: 0 bytes, `memory_log2_bytes = 13` with 32-byte-wide registers
priced at the declared machine word size.

Lineage: `ca1bca4` refuted on four cost/constructor findings (all adopted);
`97dbc8d` refuted solely on F-MEMORY-WORD-WIDTH (4 B/register vs the
declared 256-bit machine) with score_arithmetic UPHELD and cryptanalysis
unanimously clean; the floor-accounting twin `8fc264b` refuted the floor
convention itself (the panel charged both verification compressions:
H = 2 is track policy). This single ticket fixes the memory pricing at
32 B/word, unifies the packing representation at the true 256-bit word
(64-byte message = 2 machine words), states one constants convention
everywhere, and makes the declared experiment execute the exact
fixed-constant listing.

## 1. Machine model and exact target semantics (stated once)

**Machine.** 256-bit-word RAM (v5 `computation_model`). 48 registers
R0..R47, each 256 bits = 8 lanes of 32 bits. Memory is an array of 256-bit
words. Instructions are fixed-width **16 bytes**: `opcode u8 | rA u8 |
rB u8 | rD u8 | imm i64 | pad u32`. Primitives, each one charged
word-op at 1/222 (one full target compression = 1): `LD` (immediate load),
`ADD`/`SUB` (mod 2^256 — hence every 32-bit lane value is re-masked with
`AND m32` after every add/sub step, mask-per-step, the strictest reading),
`AND` (reg & imm), `XOR`, `OR`, `SHL`, `SHR` (mod 2^256), `CMP`, `BR`,
`ST`. Lane-wise 32-bit `RORk(u) = (u >> k) | (u << (32−k))` within a lane
= `SHL + SHR + OR + AND` = 4 ops; XOR/OR on lane-clean 32-bit lanes cannot
carry across lanes (1 op). Reading lane `k>0` of a 256-bit register costs
`SHR + AND` (2 ops); lane 0 costs `AND` (1 op). Registers are 32 bytes
each by the machine's own word width — priced, not assumed.

**Target.** `blake3-r1-prefix-v1`; reference
`verifier/blake3.py:blake3(data, 1)` via the organizer dispatcher
`verifier.hash_functions.digest(data, "blake3", 1)` (data first). Both
witnesses are exactly 64 bytes, so the complete hash is exactly **one
compression**: one chunk, counter 0, one full block (`block_len = 64`, so
the 16 LE32 message words are the message), `flags = CHUNK_START |
CHUNK_END | ROOT = 11`, state `v[0..7] = IV`, `v[8..11] = IV[0..3]`,
`v[12..15] = (0, 0, 64, 11)`. Rounds = 1 is loop iteration 0 exactly: the
four column G's then the four diagonal G's `G(0,5,10,15;m8,m9)
G(1,6,11,12;m10,m11) G(2,7,8,13;m12,m13) G(3,4,9,14;m14,m15)` on the
un-permuted schedule; the end-of-round permutation is inert. `G(a,b,c,d,x,y)`:
`a1 = A+B+x; d1 = ROR16(D^a1); c1 = C+d1; b1 = ROR12(B^c1); a2 = a1+b1+y;
d2 = ROR8(d1^a2); c2 = c1+d2; b2 = ROR7(b1^c2)`, adds mod 2^32, ROR right.
Root digest = first eight feed-forward words `o[i] = v[i] ^ v[i+8]` packed
LE. Full 7-round BLAKE3 is not claimed broken.

## 2. Lemmas and theorem

**Lemma 1 (c1 = 0, a2 = 0 inversion).** For diagonal `G(a,b,c,d,x,y)` with
inputs `(A,B,C,D)`, set

    x = ((D ^ ROR16(−C)) − A − B)  (mod 2^32),  a1 = A+B+x = D ^ ROR16(−C)
    y = (−a1 − ROR12(B))          (mod 2^32)

Then `d1 = ROR16(D^a1) = ROR16(ROR16(−C)) = −C` (involution), `c1 = 0`,
`b1 = ROR12(B)`, `a2 = 0`. (The refuted listing expanded ROR12 leftward as
ROL12 and its `a2` ≠ 0; corrected values are zero and are *asserted on the
executed register state* by `experiments/fixed.py` every trial.)

**Lemma 2 (four-way complement flip).** Keep `x`; replace `y` by `y−1`.
Then `a2' = a2 − 1 = F`; `d2' = ROR8(d1 ^ F) = d2 ^ F` (rotation permutes
bits, `F` is all-ones); `c2' = c1 + d2' = 0 + d2' = c2 ^ F` (uses `c1 = 0`);
`b2' = ROR7(b1 ^ c2') = b2 ^ F`. All four outputs complement.

**Theorem.** The diagonals write disjoint slot sets `{0,5,10,15}`,
`{1,6,11,12}`, `{2,7,8,13}`, `{3,4,9,14}` and read only column-phase slots,
so each output depends only on the column phase and its own message words.
The feed-forward pairing `o[i] = v[i]^v[i+8]` pairs `G(0,5,10,15)` against
`G(2,7,8,13)` exactly (`0↔8, 10↔2, 5↔13, 15↔7`); `o1,o3,o4,o6` touch
neither. Apply Lemma 1 on both diagonals; flip both `y` words (`m9−1`,
`m13−1`). Slots `{0,2,5,7,8,10,13,15}` all complement; every affected
digest word becomes `(F^u)^(F^v) = u^v`; all others unchanged. `H(M1) =
H(M2)` with probability 1 for every `m0..m7, m10, m11, m14, m15`. Zero
conditions, zero trials, zero evaluated compressions. ∎

## 3. The claimed program: 78 instructions, encoded and executed

Zero-column instance; the eight post-column constants are IV-derived public
values **embedded as LD immediates** (their entire runtime existence = the
10 LD ops below; their entire storage = their 16-byte instructions inside
the charged code bound — see §5/§6; one convention, no exceptions elsewhere
in this package). Executable encoding with opcode table, register file, and
assertions: `experiments/fixed.py`; instruction map (each line's op count
is asserted by the program's own length check):

```
LD     10   K_V0=eb2778d5 K_V5=5896cda4 K_V10=edd208cd K_V15=f67a3c87
            K_V2=c8e43216 K_V7=05d223ed K_V8=70c46342 K_V13=ba0940f8
            K_ZERO=0 K_ONE=1
INIT     10   AND R,R,0 x10 (mask-to-zero of the ten accumulator regs)
DIAG-A  19   d1a=SUB K_ZERO,K_V10; AND; ROR16: SHL,SHR,OR,AND; a1a=XOR K_V15;
             x=SUB,K_V0; AND; m8=SUB,K_V5; AND;      # m8 = bd8ae831
             b1a=ROR12(K_V5): SHL20,SHR12,OR,AND;    # = da45896c (ROR12, not
             tc=SUB K_ZERO,a1a; AND; m9=SUB,tc-b1a; AND  # 0x6cda4589=ROL12)
                                                       # m9 = 247147ea
DIAG-B  19   same shape on (K_V8,K_V13,K_V2,K_V7):   # m12=580179c0
                                                       # m13=9a77d31b
FLIPS    4   m9'=SUB m9,K_ONE; AND (=247147e9); m13'=SUB; AND (=9a77d31a)
PACK    12   qa = m8|m9<<32 (SHL,OR); qb = m12|m13<<32 (SHL,OR);
             w1a = qa | qb<<128 (SHL,OR)              # M1 word 1: lanes 8..15
             qap = m8|m9'<<32 (SHL,OR); qbp = m12|m13'<<32 (SHL,OR);
             w1b = qap | qbp<<128 (SHL,OR)            # M2 word 1
ST       4   ST mem[1]<=w1a, mem[0]<=0 (M1); ST mem[3]<=w1b, mem[2]<=0 (M2)
                                    TOTAL            78 instructions = 1248 B
```

A message is **two true 256-bit machine words** `[word0 = 0][word1 =
lanes 8..15]`; the PACK/ST ledger and the unpack ledger below use exactly
this representation — no 4-word "256-bit" groups anywhere (closes
F-COST-PACKING-GRANULARITY). `experiments/fixed.py` builds this program,
encodes it (`<BBBBQI`, 16 B/instruction), **decodes the bytes and executes
the decoded instruction stream** on the model, asserts
`a1a+b1a+m9 ≡ 0` and `a1b+b1b+m13 ≡ 0 (mod 2^32)` on the executed register
state, and asserts the assembled messages equal
`certificates/message-a.bin` / `message-b.bin` byte-for-byte. The organizer
harness executes that file per trial and recomputes both digests
(`event: full-collision`), and double-executes for reproducibility — so the
cheap fixed-constant path itself, not a column-recomputing restatement, is
under organizer execution (closes F-EVAL-BUILDER-COST-MISMATCH /
F-EXECUTED-PROGRAM-MISMATCH). A second declared experiment
(`family-generalization-v1`, `experiments/builder.py`) re-derives the
column phase per random seed and evidences the "every column choice" clause;
it is explicitly labelled supplementary, not the claimed cheap path.

## 4. Ledger (everything charged; one convention)

    construction (executed listing)                              W  =  78
    message lane unpack (both messages -> message words)            =  60
       each 256-bit word -> 8 lanes: AND(lane0) + 7x(SHR+AND) = 15
       2 words x 15 = 30 per message; x 2 messages = 60
       (panel's own corrected number; adopted)
    acceptance comparisons                                        =  52
       digest EQ: 8 XOR + 7 OR + 1 CMP + 1 BR = 17
       distinctness: 16 XOR + 15 OR + 1 CMP + 1 BR = 33
       loop control/accumulator: 2
    verification compressions (H = 2, track policy per the 8fc264b
      refutation: "those compressions add two target-compression units")   = 2.0

    T = 2 + 190/222 = 2.855856 target-compressions
    log2 T = 1.513923        (claimed scalar 1.60, log2 units per v5
                              score = log2(total charged time))

Sensitivity ladder — same itemized ops, every op priced exactly once per
row; the margin check: 1.60 tolerates W ≤ 2^1.60 − 2 = 228.979 ops:

| reading                                                    | W   | T      | log2 T   |
|---|---|---|---|
| **primary (packed 256-bit words, mask-per-step)**           | 190 | 2.8559 | **1.5139** |
| narrow 32-bit stores (PACK 12 + ST 4 → 32 narrow, +16)      | 206 | 2.9279 | 1.5499   |
| digest comparison also charged in verifier replay (+17)     | 207 | 2.9324 | 1.5521   |
| both stacked — legitimate worst                             | 223 | 3.0045 | **1.5871** |
| (disclosed; same comparison charged a third time, +50)      | 240 | 3.0811 | 1.6234   |

The claim upper-bounds every legitimate single accounting (223 < 228.979).
The last row exceeds by 0.023 only if the digest comparison is charged a
third time — disclosed, not a legitimate reading. Constants: no ladder row
charges a "derivation phase" because none exists (§3/§6: LD immediates);
the historical +112 in-program-re-derivation variant (log2 1.7486) is a
convention this package rejects **everywhere and consistently** — that
inconsistency is what F-PREPROCESSING-CLASSIFICATION flagged; there is now
exactly one constants story in this document.

## 5. Memory bound (F-MEMORY-WORD-WIDTH closed)

Priced at the declared machine word width — **registers = 32 bytes each**:

    code      190 instructions x 16 B  = 3040 B   (78-instruction listing
                                                    = 1248 B executed by the
                                                    declared experiment;
                                                    + 112 unpack/comparison
                                                    checking instructions)
    registers 48 x 32 B                = 1536 B   (R0..R47, 256-bit each)
    message buffers: 2 x 64 B          =  128 B
    digests    2 x 32 B                =   64 B
    program counter / flags / stack     =   64 B
    -----------------------------------
    peak total                         = 4832 B ≤ 8192 = 2^13

`memory_log2_bytes = 13`. (The panel's own recomputation of the old ledger
was 4512 B > 4096 B = the exact 97dbc8d fatal; at 32 B/register the honest
number is 4832 B, comfortably inside 2^13.) Memory is a reported metric —
no scalar contribution. The instruction encoding is concrete (fixed-width
`opcode u8 | rA u8 | rB u8 | rD u8 | imm i64 | pad u32`), the complete
encoding is machine-generated by `experiments/fixed.py`
(`encode(build_program())`, 1248 bytes asserted), closing
F-MEMORY-ENCODING-EVIDENCE for the executed portion.

## 6. Resource fields

- `time_log2 = 1.60`: §4; worst legitimate row 1.5871.
- `memory_log2_bytes = 13`: §5, 32-byte registers, concrete encoding.
- `preprocessing_log2 = 0`: **zero preprocessing**: the program is one
  straight-line listing executed by the verifier path itself; the LD
  immediates' entire preprocessing IS their 10 LD instructions (charged in
  the 78) and their code bytes (charged in §5). Nothing is hoisted outside
  the ledger; nothing is derived at runtime; constants are IV-derived
  public values (the same convention AArnott's 6109275 used — cited).
- `nonuniform_advice_log2_bytes = 0`: uniform program; 0 bytes stored
  advice (the certificate files are review witnesses, not inputs — the
  program emits them).
- `success_probability = 1`: deterministic identity (§2); zero trials.

## 7. Witness pair and verification

`certificates/message-a.bin`, `certificates/message-b.bin` (64 raw bytes
each) — the §3 program's exact output — and expected digest

    M1 = 0000000000000000000000000000000000000000000000000000000000000000
         31e88abdea4771240000000000000000c07901581bd3779a0000000000000000
    M2 = 0000000000000000000000000000000000000000000000000000000000000000
         31e88abde94771240000000000000000c07901581ad3779a0000000000000000
    H  = 9c3b8fbe64d9445bf72d12335ca2283f497c0ecbd5945d89020d61c63a93124e

Re-verified with organizer code this run: `digest(M1,"blake3",1) =
digest(M2,"blake3",1) = H`; 7-round BLAKE3 separates them
(`dafe7fd2…` vs `0f341cca…`); post-round-0 state diff is exactly the all-F
pattern on `{0,2,5,7,8,10,13,15}` (the Lemma-2 signature). The panel's own
lane_cryptanalysis on 97dbc8d recorded the mechanism as sound and its
checker as "a trusted certificate and 256 organizer-recomputed executions
corroborate the exact construction". Scope: context-bound to
`(counter=0, block_len=64, flags=11)`, 64-byte single chunk; tested
non-transferable to a 2-chunk tree; no full-BLAKE3 claim.

## 8. Credit

Family prior art, all pending at submission: winglock 754f0f2/d60b306
(two-ticket strategy — we ran and retired ours on the panel's H=2 ruling),
jvr0x 93f45e2 (organizer-executed builder discipline — now executed on the
*exact listing*), jungjipdo af4c65b (family instance), AArnott 6109275
(H=2 convention and constant-table convention — both adopted; the panel
confirmed H = 2 as track policy when refuting our floor twin). Mathematics
independently re-derived and machine-verified in this package.
