# A deterministic O(1)-work ordinary collision for 1-round BLAKE3 (blake3-r1-prefix-v1) — rev4, derivation-charged package

Closed-form constructor whose constants are **constructed by the program
itself**, machine-verified witness pair, and an organizer-declared
experiment that **encodes, decodes, and executes the claimed
straight-line listing itself**. Claimed `time_log2 = 1.7487`
target-compressions — the review panel's own prescribed bound from
ticket `271553a`, `log2(2 + (190+112)/222) = 1.748616`, rounded UP —
with primary ledger `log2(2 + 298/222) = 1.7409`, `success_probability = 1`,
heuristics: none, `preprocessing_log2 = 0` **because no preprocessing
phase exists** (the derivation is charged inside the program), 0 bytes
nonuniform advice, `memory_log2_bytes = 13`.

## 0. What changed in rev4, and why (lineage)

`ca1bca4` refuted on four cost/constructor findings (all adopted);
`97dbc8d` refuted solely on F-MEMORY-WORD-WIDTH (4 B/register vs the
declared 256-bit machine), score_arithmetic UPHELD; the floor-accounting
twin `8fc264b` refuted the floor convention itself (H = 2 is track
policy); `2553709` died at intake (the experiment sandbox mounts only
`program.py`; fixed by embedding witness bytes as program constants);
`65794fd` refuted on F-OMITTED-CONSTANT-CONSTRUCTION; `271553a` was
refuted by exactly one fatal finding, **F-COST-PRECOMPUTED-CONSTANTS**,
carrying three fatal obligations — `time_bound`,
`data_preprocessing_advice`, `score_arithmetic` — and the panel wrote
the fix itself: *"the fixed constructor starts from eight precomputed
post-column state words. Loading those values is not their
construction… including the disclosed omitted derivation changes the
exponent from the submitted 1.60 upper bound to at least
log2(2+302/222)=1.7486"* and *"the retained eight 32-bit values also
constitute 32 bytes of target-specific precomputed data unless derived
within the charged algorithm."*

(The panel's dossier prints "1.7486" at 4 decimals; its exact value is
`log2(2 + 302/222) = 1.748616`, and a claim must not round *below* the
work it bounds — so this package claims `1.7487`, whose tolerance
W ≤ 302.04 covers the panel's exact 302-op row.)

This rev4 **derives the eight post-column words within the charged
program** instead of embedding them: the §3 listing runs the four column
quarter-rounds on the all-zero message (112 masked word-ops) before any
diagonal solve reads them. Every remaining LD immediate is a generic
specification constant (IV words, `block_len = 64`, `flags = 11`, zero,
one) or program text; no target-derived value is precomputed anywhere.
`preprocessing_log2 = 0` no longer means "constants are free" — it means
there is **no preprocessing phase at all**: the derivation cost sits
inside the charged time. `nonuniform_advice_log2_bytes = 0` because
nothing target-specific is stored or retained outside the executed
program. `memory_log2_bytes` and `success_probability = 1` are carried
forward unchanged from `271553a`, where both obligations were upheld
(memory even under the panel's own +112-instruction re-price:
4832 + 1792 = 6624 B ≤ 2^13).

## 1. Machine model and exact target semantics (stated once)

**Machine.** 256-bit-word RAM (v5 `computation_model`: "Classical
probabilistic 256-bit word RAM"). 48 registers R0..R47, each 256 bits =
8 lanes of 32 bits. Memory is an array of 256-bit words; **all registers
are 0 at reset**. Instructions are fixed-width **16 bytes**: `opcode u8
| rA u8 | rB u8 | rD u8 | imm i64 | pad u32`. Primitives, each one
charged word-op at 1/222 (one full target compression = 1): `LD`
(immediate load), `ADD`/`SUB` (mod 2^256 — hence every 32-bit lane value
is re-masked with `AND m32` after every add/sub step, mask-per-step, the
strictest reading), `AND` (reg & imm), `XOR`, `OR`, `SHL`, `SHR` (mod
2^256), `CMP`, `BR`, `ST`. Lane-wise 32-bit `RORk(u) = (u >> k) | (u <<
(32−k))` within a lane = `SHL + SHR + OR + AND` = 4 ops; XOR/OR on
lane-clean 32-bit lanes cannot carry across lanes (1 op). Reading lane
`k>0` of a 256-bit register costs `SHR + AND` (2 ops); lane 0 costs
`AND` (1 op). Registers are 32 bytes each by the machine's own word
width — priced, not assumed.

**Target.** `blake3-r1-prefix-v1`; reference
`verifier/blake3.py:blake3(data, 1)` via the organizer dispatcher
`verifier.hash_functions.digest(data, "blake3", 1)` (data first). Both
witnesses are exactly 64 bytes, so the complete hash is exactly **one
compression**: one chunk, counter 0, one full block (`block_len = 64`,
so the 16 LE32 message words are the message), `flags = CHUNK_START |
CHUNK_END | ROOT = 11`, state `v[0..7] = IV`, `v[8..11] = IV[0..3]`,
`v[12..15] = (0, 0, 64, 11)`. Rounds = 1 is loop iteration 0 exactly: the
four column G's then the four diagonal G's `G(0,5,10,15;m8,m9)
G(1,6,11,12;m10,m11) G(2,7,8,13;m12,m13) G(3,4,9,14;m14,m15)` on the
un-permuted schedule; the end-of-round permutation is inert. `G(a,b,c,d,x,y)`:
`a1 = A+B+x; d1 = ROR16(D^a1); c1 = C+d1; b1 = ROR12(B^c1); a2 = a1+b1+y;
d2 = ROR8(d1^a2); c2 = c1+d2; b2 = ROR7(b1^c2)`, adds mod 2^32, ROR right.
Root digest = first eight feed-forward words `o[i] = v[i] ^ v[i+8]` packed
LE. Full 7-round BLAKE3 is not claimed broken.

## 2. Lemmas and theorem (unchanged; upheld by the 271553a panel)

**Lemma 1 (c1 = 0, a2 = 0 inversion).** For diagonal `G(a,b,c,d,x,y)` with
inputs `(A,B,C,D)`, set

    x = ((D ^ ROR16(−C)) − A − B)  (mod 2^32),  a1 = A+B+x = D ^ ROR16(−C)
    y = (−a1 − ROR12(B))          (mod 2^32)

Then `d1 = ROR16(D^a1) = ROR16(ROR16(−C)) = −C` (involution), `c1 = 0`,
`b1 = ROR12(B)`, `a2 = 0`. (`experiments/fixed.py` *asserts*
`a1 + b1 + y ≡ 0 (mod 2^32)` on the executed register state of both
solved diagonals every trial.)

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

## 3. The claimed program: 186 instructions, derivation-charged, encoded and executed

Zero-column instance. The eight post-column words that rev3 embedded as
precomputed LD immediates are now **derived inside the listing** by the
DERIVE block — the four column quarter-rounds evaluated on the all-zero
message, exactly matching the target's round-0 column phase. Nothing
target-specific remains in any immediate. Executable encoding with opcode
table, register file, and assertions: `experiments/fixed.py`; instruction
map (each line's op count is asserted by the program's own length check):

```
LD      16   spec immediates only: IV0..IV7 into v0..v7, IV0..IV3 into
             v8..v11, v14=64 (block_len), v15=11 (flags), K_ZERO, K_ONE
             — zero target-derived values in any immediate
DERIVE 112   four column quarter-rounds on message words 0..7 = 0:
             G(0,4,8,12;0,0) G(1,5,9,13;0,0) G(2,6,10,14;0,0) G(3,7,11,15;0,0)
             each = 28 masked ops: 4x(ADD+AND) + 4x(XOR+SHL+SHR+OR+AND)
             yields the post-column words used below (asserted in-program
             against the rev3-embedded values, then superseded):
             v0=eb2778d5 v5=5896cda4 v10=edd208cd v15=f67a3c87
             v2=c8e43216 v7=05d223ed v8=70c46342 v13=ba0940f8
DIAG-A  19   d1a=SUB K_ZERO,v10; AND; ROR16: SHL,SHR,OR,AND; a1a=XOR v15;
             x=SUB,v0; AND; m8=SUB,v5; AND;      # m8 = bd8ae831
             b1a=ROR12(v5): SHL20,SHR12,OR,AND;  # ROR12, not 0x6cda4589=ROL12
             tc=SUB K_ZERO,a1a; AND; m9=SUB,tc-b1a; AND   # m9 = 247147ea
DIAG-B  19   same shape on (v2,v7,v8,v13):       # m12=580179c0
                                                     # m13=9a77d31b
FLIPS    4   m9'=SUB m9,K_ONE; AND (=247147e9); m13'=SUB; AND (=9a77d31a)
PACK    12   qa = m8|m9<<32 (SHL,OR); qb = m12|m13<<32 (SHL,OR);
             w1a = qa | qb<<128 (SHL,OR)              # M1 word 1: lanes 8..15
             qap = m8|m9'<<32 (SHL,OR); qbp = m12|m13'<<32 (SHL,OR);
             w1b = qap | qbp<<128 (SHL,OR)            # M2 word 1
             (exact: the q-words are bit-disjoint and every other message
             lane is zero — m0..m7 = m10,m11 = m14,m15 = 0 here)
ST       4   ST mem[1]<=w1a, mem[0]<=K_ZERO (M1); ST mem[3]<=w1b,
             mem[2]<=K_ZERO (M2)
                                    TOTAL      186 instructions = 2976 B
```

A message is **two true 256-bit machine words** `[word0 = 0][word1 =
lanes 8..15]`; the PACK/ST ledger and the unpack ledger below use exactly
this representation — no 4-word "256-bit" groups anywhere
(closes F-COST-PACKING-GRANULARITY). Rev3's 10-instruction INIT block is
gone: the model's documented all-registers-zero reset makes
mask-to-zero of dead accumulators unreachable arithmetic (the paranoid
row that keeps them is priced in §4). `experiments/fixed.py` builds this
program, encodes it (`<BBBBQI`, 16 B/instruction), **decodes the bytes
and executes the decoded instruction stream** on the model, asserts the
**DERIVE audit** — all eight in-program-derived words equal the values
rev3 embedded — asserts `a1a+b1a+m9 ≡ 0` and `a1b+b1b+m13 ≡ 0 (mod
2^32)` on the executed register state, and asserts the assembled
messages equal the witness bytes of `certificates/message-a.bin` /
`message-b.bin` byte-for-byte (the witness bytes are embedded in the
program as constants — the organizer sandbox mounts only `program.py`,
see experiments/runner.py — and they are the same bytes §7 prints and
`certificates/manifest.json` hashes). The organizer harness executes that
file per trial and recomputes both digests (`event: full-collision`), and
double-executes for reproducibility — so the derivation-charged path
itself, not a restatement, is under organizer execution (closes
F-EVAL-BUILDER-COST-MISMATCH / F-EXECUTED-PROGRAM-MISMATCH). A second
declared experiment (`family-generalization-v1`, `experiments/builder.py`)
re-derives the column phase per random seed and evidences the "every
column choice" clause; it is explicitly labelled supplementary, not the
claimed path.

## 4. Ledger (everything charged; the derivation is now inside)

    construction (executed listing, §3)                     W  = 186
       LD 16 spec-value immediates (no target-derived value)
       DERIVE 112  four masked column quarter-rounds, zero message
       DIAG 19+19  Lemma-1 solves on both diagonals
       FLIPS 4 | PACK 12 | ST 4
    message lane unpack (both messages -> message words)       =  60
       each 256-bit word -> 8 lanes: AND(lane0) + 7x(SHR+AND) = 15
       2 words x 15 = 30 per message; x 2 messages = 60
       (panel's own corrected number; adopted)
    acceptance comparisons                                    =  52
       digest EQ: 8 XOR + 7 OR + 1 CMP + 1 BR = 17
       distinctness: 16 XOR + 15 OR + 1 CMP + 1 BR = 33
       loop control/accumulator: 2
    verification compressions (H = 2, track policy per the 8fc264b
      refutation: "those compressions add two target-compression units")  = 2.0

    W = 186 + 60 + 52 = 298 word-ops
    T = 2 + 298/222 = 3.342342 target-compressions
    log2 T = 1.740860        (claimed scalar 1.7487 = the panel's own
                              prescribed bound 1.748616 rounded UP, see
                              below; v5 score = log2(total charged time))

**The panel's prescribed figure.** The 271553a `score_arithmetic` fatal
states: *"Including the disclosed omitted derivation changes the exponent
from the submitted 1.60 upper bound to at least
log2(2+302/222)=1.7486."* That 302 = 190 (rev3 ledger, whose 78-op
construction included 10 INIT mask-zeros and 8 target-constant LDs) + 112
(derivation). The 186-op rev4 listing = rev3's 78 − 10 old LDs − 10
reset-redundant INIT mask-zeros + 16 spec-value LDs + 112 DERIVE ops, so
our honest ledger count is W = 302 − 10 − 10 + 16 = 298 < 302 and
1.740860 < 1.748616. We **claim the panel's prescribed bound,
`time_log2 = 1.7487`** — its exact value 1.748616 rounded UP, never
below the work it bounds (claiming 1.7486 would sit 1.6×10⁻⁵ below the
panel's own row — the same rounding direction that carries a
score_arithmetic fatal) — rather than shave 0.0078 off it to 1.7409;
the "at least" is respected: our total charged work never exceeds it.
The tolerance at the claimed value is W ≤ 2^1.7487 − 2 = 302.04, which
covers even the panel-parity 302-op row. The full ledger delta vs the
panel's 302 is disclosed above: the 112 DERIVE ops are charged in full
exactly as the panel prescribes; the only subtractions are the 10
mask-to-zero INIT ops that touch registers never read before being
written under the model's documented zero-reset (unreachable arithmetic
the panel's 302 inherited from the rev3 ledger, not derivation work)
and the 8 superseded constant LDs, which DERIVE now replaces; the 14
new LDs load only specification values.

Sensitivity ladder — same itemized ops, every op priced exactly once per
row the margin check: the claim 1.7487 tolerates W ≤ 2^1.7487 − 2 =
302.04 ops — at or above every row it labels legitimate (the two bold
rows); rows marked (disclosed) sit above it and are argued illegitimate
below, not conceded:

| reading                                                     | W   | T      | log2 T   |
|---|---|---|---|
| **primary (declared 256-bit-word machine)**                  | 298 | 3.3423 | **1.7409** |
| **panel parity count (rev3 ledger + full 112 derivation)**   | 302 | 3.3604 | **1.748616** |
| (disclosed) add back 10 dead INIT mask-zeros                 | 308 | 3.3874 | 1.7602   |
| (disclosed) narrow 32-bit stores in PACK/ST (+16)            | 314 | 3.4144 | 1.7716   |
| (disclosed) digest comparison charged a second time in replay (+17) | 315 | 3.4189 | 1.7735 |
| (disclosed) narrow + replay stacked (+33)                    | 331 | 3.4910 | 1.8036   |
| (disclosed; triple-counted comparison +50)                   | 348 | 3.5676 | 1.8349   |

Rows marked (disclosed) are **not** legitimate single accountings of the
declared machine and are priced for transparency, not conceded: (a) the
INIT row restores mask-to-zero of registers that are never read before
being written — unreachable arithmetic under the declared zero-reset that
the panel never asked to restore; (b) the narrow row re-machines a
machine the model declares in its own words — "256-bit word RAM",
256-bit `LD`/`ST` primitives — into a 32-bit one only for PACK/ST; a
judge who re-machines `LD`/`ST` must re-machine the DERIVE arithmetic
too (×8, W ≈ 1000+, log2 ≈ 2.45), the same reading every accepted
family ticket shares, so priced fully it prices the whole family out and
is not a discriminating legitimate reading; (c) the replay row charges
the digest comparison a second time — once inside our 52, once again in
verifier replay — the same double-count the 271553a panel declined to
accept against the 190-op ledger ("arithmetically internally consistent,
but not arithmetic for total charged work" was about *omission*, not
about charging one comparison twice). The claim upper-bounds every
legitimate single accounting (298 < 302.04, as is the panel-parity row).
Constants: every ladder row now charges the derivation; there is no
longer any row in which the post-column words are free, because no
reading of any model has them free — they are program arithmetic.

## 5. Memory bound (32-byte-register pricing carried forward; upheld)

Priced at the declared machine word width — **registers = 32 bytes each**:

    code      298 instructions x 16 B  = 4768 B   (186-instruction listing
                                                    = 2976 B executed by the
                                                    declared experiment;
                                                    + 112 unpack/comparison
                                                    checking instructions)
    registers 48 x 32 B                = 1536 B   (R0..R47, 256-bit each)
    message buffers: 2 x 64 B          =  128 B
    digests    2 x 32 B                =   64 B
    program counter / flags / stack     =   64 B
    -----------------------------------
    peak total                         = 6560 B ≤ 8192 = 2^13

`memory_log2_bytes = 13`. Even the most paranoid ladder row (W = 348:
5568 B code) totals 7360 B ≤ 8192 B — the panel itself verified in
271553a that adding the 112 derivation instructions keeps the ceiling
("Adding 112 unrolled 16-byte instructions to the submitted 4832-byte
peak gives 6624 bytes, so the submitted 2^13-byte memory ceiling remains
sufficient"). Memory is a reported metric — no scalar contribution. The
instruction encoding is concrete (fixed-width `opcode u8 | rA u8 |
rB u8 | rD u8 | imm i64 | pad u32`), the complete encoding is
machine-generated by `experiments/fixed.py` (`encode(build_program())`,
2976 bytes asserted), closing F-MEMORY-ENCODING-EVIDENCE for the
executed portion.

## 6. Resource fields

- `time_log2 = 1.7487`: §4 — the panel's prescribed bound 1.748616,
  adopted and rounded UP; primary ledger 1.7409, panel-parity row
  1.748616, and the claim tolerates W ≤ 302.04 ≥ both our honestly
  re-counted 298 and the panel's own 302.
- `memory_log2_bytes = 13`: §5, 32-byte registers, concrete encoding,
  headroom under every ladder row.
- `preprocessing_log2 = 0`: **there is no preprocessing phase.** The
  eight post-column words are produced by 112 charged in-program ops
  (the DERIVE block) inside the claimed time — not hoisted out of the
  ledger, not retained across runs, not read as advice. This is the
  panel's `data_preprocessing_advice` closure by construction, not by
  classification.
- `nonuniform_advice_log2_bytes = 0`: uniform program; 0 bytes stored
  advice. Every immediate is a generic specification constant (IV,
  block_len, flags) or 0/1 — target constants supplied by the
  specification are code, per the model's own treatment of every
  accepted family ticket; the certificate files are review witnesses,
  not inputs (the program emits them).
- `success_probability = 1`: deterministic identity (§2); zero trials;
  DERIVE adds no randomness (upheld obligation, carried forward).

## 7. Witness pair and verification

`certificates/message-a.bin`, `certificates/message-b.bin` (64 raw bytes
each) — the §3 program's exact output — and expected digest

    M1 = 0000000000000000000000000000000000000000000000000000000000000000
         31e88abdea4771240000000000000000c07901581bd3779a0000000000000000
    M2 = 0000000000000000000000000000000000000000000000000000000000000000
         31e88abde94771240000000000000000c07901581ad3779a0000000000000000
    H  = 9c3b8fbe64d9445bf72d12335ca2283f497c0ecbd5945d89020d61c63a93124e

The two witness messages differ in exactly two bytes (m9: ea→e9, m13:
1b→1a at the lemma-2 flip positions; on the 128-hex-character rendering,
exactly the 2 t-characters… precisely: 2 differing bytes, 4 differing
hex characters). Re-verified with organizer code this run:
`digest(M1,"blake3",1) = digest(M2,"blake3",1) = H`; 7-round BLAKE3
separates them (`dafe7fd2…` vs `0f341cca…`); post-round-0 state diff is
exactly the all-F pattern on `{0,2,5,7,8,10,13,15}` (the Lemma-2
signature). The 271553a panel's own lanes — lane_cryptanalysis
(collision_correctness, probability_analysis: supported),
lane_evaluability (all six obligations supported), lane_experiments
(relevance/reproducibility/statistics supported, extrapolation
plausible) — were clean and re-verification this run reproduces every
figure; the DERIVE block is deterministic spec arithmetic and cannot
disturb any of them. Scope: context-bound to `(counter=0, block_len=64,
flags=11)`, 64-byte single chunk; tested non-transferable to a 2-chunk
tree; no full-BLAKE3 claim.

## 8. Credit

Family prior art, all pending at submission: winglock 754f0f2/d60b306
(two-ticket strategy — we ran and retired ours on the panel's H=2
ruling), jvr0x 93f45e2 (organizer-executed builder discipline — now
executed on the *exact listing*), jungjipdo af4c65b (family instance),
AArnott 6109275 (H=2 convention — adopted; the panel confirmed H = 2 as
track policy when refuting our floor twin) and Jbenisek (estimator
work). The independent constructions in these families share the
decoupling idea this ticket prices honestly: separate the zero-message
column phase from the solved diagonals. Mathematics independently
re-derived and machine-verified in this package; rev4's accounting is
the 271553a panel's own prescription, executed verbatim.
