# A deterministic O(1)-work ordinary collision for 1-round BLAKE3 (blake3-r1-prefix-v1) — corrected, panel-hardened

Closed-form constructor with a machine-verified witness pair. Claimed
`time_log2 = 1.60` target-compressions, `success_probability = 1`,
heuristics: none, nonuniform advice: zero bytes.

This package supersedes refuted ticket `ca1bca4`. The panel was right on all
counts and its arithmetic is adopted wholesale: (1) the old section-3 listing
decomposed ROR12 as `(x<<12)|(x>>20)` — that is ROL12 — so the *listed
program* no longer constructed the certified pair; (2) 256-bit→32-bit lane
semantics (mask steps after add/sub on a mod-2^256 machine, lane unpack for
message loading) were uncharged; (3) the stated digest-equality comparison was
not in the primary ledger; (4) declared preprocessing ops sat outside the
charged total. All four are fixed here, and the corrected straight-line
program is **executed byte-exactly** by `experiments/builder.py`, declared as
organizer-executed evidence (`experiments/manifest.json`,
`python-message-pairs-v1`, event `full-collision`) — asserted against the
certificate files themselves — before submission.

## 1. Exact target semantics

Target `blake3-r1-prefix-v1`; reference `verifier/blake3.py:blake3(data, 1)`
(reached through the organizer dispatcher `verifier.hash_functions.digest(data,
"blake3", 1)` — data first). Both witness messages are exactly 64 bytes, so
the complete hash is exactly **one compression**:

- one chunk (64 ≤ 1024 bytes), chunk counter `0`, one block with true
  `block_len = 64` (the block is full, so the 16 little-endian message words
  are the message),
- `flags = CHUNK_START | CHUNK_END | ROOT = 1 | 2 | 8 = 11`,
- initial state `v[0..7] = IV[0..7]`, `v[8..11] = IV[0..3]`,
  `v[12..15] = (counter_lo, counter_hi, block_len, flags) = (0, 0, 64, 11)`,
- rounds = 1 means exactly loop iteration 0: eight `G` calls on the
  **un-permuted** schedule, four columns then four diagonals
  `G(0,5,10,15;m8,m9) G(1,6,11,12;m10,m11) G(2,7,8,13;m12,m13) G(3,4,9,14;m14,m15)`;
  the end-of-round message permutation is inert (no round 1 consumes it),
- `G(a,b,c,d,x,y)` exactly as in the verifier:
  `a1 = A+B+x; d1 = ROR16(D^a1); c1 = C+d1; b1 = ROR12(B^c1);
  a2 = a1+b1+y; d2 = ROR8(d1^a2); c2 = c1+d2; b2 = ROR7(b1^c2)`;
  `RORk(u) = (u >> k) | (u << (32-k))` — **right** rotation — all additions
  modulo 2^32,
- root digest = the first eight feed-forward words `o[i] = v[i] ^ v[i+8]`,
  `i = 0..7`, packed little-endian.

Machine model (`collision-frontier-v5` + the paired-lanes-v1 cost lane's
reading, adopted): a 256-bit-word RAM. ADD/SUB are modulo 2^256, so every
32-bit lane add/sub is followed by an AND-mask (2 charged ops); bitwise
XOR/OR on lane-clean 32-bit lanes cannot carry across lanes (1 op);
lane-wise 32-bit rotations are SHL+SHR+OR+AND (4 ops); CMP and conditional
branch are charged ops; reading lane `k>0` of a 256-bit register costs
SHR+AND (2 ops), lane 0 costs AND (1 op). One target compression = 1 unit;
every other primitive = 1/222 (v5 `reference_operation_costs["blake3-r1"]`).
Memory reported, not scored. All arithmetic below in Z/2^32; `F = 0xFFFFFFFF`.

## 2. Two G-decoupling lemmas and the collision theorem

**Lemma 1 (c1 = 0, a2 = 0 inversion).** For diagonal `G(a,b,c,d,x,y)` with
post-column inputs `(A,B,C,D)`, choose

    x = ((D ^ ROR16(−C)) − A − B)         (mod 2^32)
    a1 = A + B + x = D ^ ROR16(−C)
    y  = (−a1 − ROR12(B))                 (mod 2^32)

Then `D ^ a1 = ROR16(−C)` so `d1 = ROR16(D^a1) = −C` (ROR16 involution),
`c1 = C + d1 = 0`, `b1 = ROR12(B ^ 0) = ROR12(B)`, and `a2 = a1 + b1 + y = 0`.
Both rotations are RIGHT rotates; the earlier ticket's listing wrongly
expanded ROR12 leftward, breaking exactly this chain (its recomputed `a2`
values were `0x6d6b43e3` / `0x1c918cc5` ≠ 0; corrected values are zero,
asserted numerically in `experiments/builder.py`).

**Lemma 2 (four-way complement flip).** Keep `x`; replace `y` by `y − 1`.
Values through `b1` are unchanged; then

    a2' = a2 − 1 = F = a2 ^ F
    d2' = ROR8(d1 ^ a2') = ROR8(d1) ^ F = d2 ^ F   (RORk commutes with xor)
    c2' = c1 + d2' = 0 + d2' = c2 ^ F              (uses c1 = 0)
    b2' = ROR7(b1 ^ c2') = ROR7(b1 ^ c2 ^ F) = b2 ^ F

so decrementing `y` complements **all four** outputs of that diagonal.

**Theorem (diagonal-pair cancellation at the feed-forward).** The four
diagonals write disjoint slot sets `{0,5,10,15}`, `{1,6,11,12}`,
`{2,7,8,13}`, `{3,4,9,14}`, and no diagonal reads another's slots: each
diagonal's output depends only on the column phase and its own two message
words. The digest pairing `o[i] = v[i]^v[i+8]` pairs slots of `G(0,5,10,15)`
against slots of `G(2,7,8,13)` exactly (`0↔8`, `10↔2`, `5↔13`, `15↔7`), so
`o0,o2,o5,o7` consume one word from each; `o1,o3,o4,o6` consume neither.
Apply Lemma 1 to both diagonals (`m8,m9` and `m12,m13`), and define `M2` from
`M1` by `m9 → m9−1`, `m13 → m13−1`. Slots `{0,2,5,7,8,10,13,15}` all
complement, every other state word is bit-identical, and each affected digest
word sees `(F^u)^(F^v) = u^v`. Hence `H(M1) = H(M2)` with probability 1 for
**every** choice of `m0..m7, m10, m11, m14, m15`: zero conditions, zero
trials. ∎ The construction evaluates zero target compressions.

## 3. Corrected straight-line program (78 construction ops, mask-charged)

Zero-column instance (`m0..m7 = m10 = m11 = m14 = m15 = 0`); its eight needed
post-column words are compile-time constants, re-derived from
`verifier/blake3.py` (column phase on zero words), not assumed:

    v0=eb2778d5 v2=c8e43216 v5=5896cda4 v7=05d223ed
    v8=70c46342 v10=edd208cd v13=ba0940f8 v15=f67a3c87

`SUB` below is 2 ops (op + AND-mask), `ROR` 4 ops (SHL+SHR+OR+AND),
`XOR`/`LD`/`ST` 1 op, `PACK` (pair into a 256-bit register) 2 ops (SHL+OR):

```
# ---- LD: 10 constants (each = 1 charged 256-bit load) ------------------
L01 LD K_V0  = eb2778d5   L02 LD K_V5  = 5896cda4   L03 LD K_V10 = edd208cd
L04 LD K_V15 = f67a3c87   L05 LD K_V2  = c8e43216   L06 LD K_V7  = 05d223ed
L07 LD K_V8  = 70c46342   L08 LD K_V13 = ba0940f8   L09 LD K_ZERO = 0
L10 LD K_ONE = 1                                                     [10 ops]
# ---- INIT: address regs, counters, branch slots ------------------------
10 control/register init ops — the panel's F-COST-PREPROCESSING work, now
inside the charged ledger, not declared outside it                      [10 ops]
# ---- diagonal G(0,5,10,15): solve (m8,m9) with c1=0, a2=0 -------------
d1 = SUB K_ZERO,K_V10; AND      # -C = 122df733                         [2]
r  = SHR d1,16; SHL d1,16; OR; AND          # ROR16 = f733122d          [4]
a1 = XOR K_V15, r                           # 01492eaa                  [1]
x  = SUB a1,K_V0; AND; SUB x,K_V5; AND      # a1-A-B = m8 = bd8ae831    [4]
b1 = SHR K_V5,12; SHL K_V5,20; OR; AND      # ROR12(B) = da45896c   <<CORRECTED
                                            #   old listing (B<<12)|(B>>20)
                                            #   = 0x6cda4589 = ROL12(B)     [4]
y  = SUB K_ZERO,a1; AND; SUB y,b1; AND      # -a1-b1 = m9 = 247147ea    [4]
                                                                 # subtotal [19]
# ---- diagonal G(2,7,8,13): solve (m12,m13), same shape ----------------
d1b = SUB K_ZERO,K_V8; AND (2); rb = ROR16(d1b) (4); a1b = XOR K_V13,rb (1);
x = SUB a1b,K_V2 (2), m12 = SUB x,K_V7 (2);
b1b = SHR K_V7,12; SHL K_V7,20; OR; AND (4) = 3ed05d22  <<CORRECTED
                                            #   old 0x223ed05d = ROL12
m13 = SUB K_ZERO,a1b (2); SUB ,b1b (2)... see builder listing      [19]
# ---- Lemma-2 flips ------------------------------------------------------
m9p  = SUB m9,K_ONE; AND                    # 247147e9                  [2]
m13p = SUB m13,K_ONE; AND                   # 9a77d31a                  [2]
# ---- PACK: pair words into 256-bit registers (SHL+OR each) -------------
q1 = m8 | m9<<32;  q2 = m12 | m13<<32;  q3 = m8 | m9p<<32;  q4 = m12 | m13p<<32
                                                                    [8 ops]
# ---- ST: 256-bit stores; both per-message zero-word stores charged -----
S01 ST M1[0..3]=0    S02 ST M1[4..7]=0    S03 ST M1[8..11]=q1   S04 ST M1[12..15]=q2
S05 ST M2[0..3]=0    S06 ST M2[4..7]=0    S07 ST M2[8..11]=q3   S08 ST M2[12..15]=q4
                                                                    [8 ops]
```

**Construction total: 10 LD + 10 INIT + 19 + 19 + 4 + 8 + 8 = 78 ops.**
`experiments/builder.py` is the executable rendering of this listing: the
ROR expansions above are the ones it runs (ROR12 = `>>12 | <<20`), the
solved-word hex values are its outputs, and the organizer's own experiment
harness (§4.5) executes it per trial and recomputes both digests.

## 4. Charged post-construction work (F-COST-32BIT-SEMANTICS + F-COST-COMPARISON)

Verification charges **both** full compressions (H = 2, the convention of
6109275) *and* the lane work the compressions and the acceptance test need
on the mask-charged machine:

- **Message lane unpack: 56 ops.** Each compression loads 16 message words
  from its 64-byte buffer; each message = 4 packed 256-bit words; unpacking
  one packed word = AND (lane 0) + 3×(SHR+AND) = 7 ops; 4×7 = 28 per
  message, 56 for both. All 16 lanes are charged, including the twelve zero
  lanes; no exemption.
- **Acceptance comparisons: 52 ops.** Digest equality: 8 XOR + 7 OR-fold +
  1 CMP + 1 BR = 17. Message distinctness (profile precondition):
  16 XOR + 15 OR-fold + 1 CMP + 1 BR = 33. Loop control/accumulator: 2.

**Primary ledger: T = 2 + (78 + 56 + 52)/222 = 2 + 186/222 = 2.837838
compressions, log2 T = 1.504792. Claimed: 1.60** — the claim tolerates
W ≤ 229.0 ops versus the primary 186 and the worst legitimate ladder variant
219. Every operation the panel named is inside the number; the margin is
recomputed from the ledger itself, not inherited from the refuted ticket.

Sensitivity ladder (same mask-charged semantics; §4.5 + note reprint the
numbers with execution evidence):

| reading                                                          | W   | T      | log2 T |
|---|---|---|---|
| **primary: packed stores, mask-charged construction+unpack+cmp**  | 186 | 2.8378 | **1.5048** |
| narrow 32-bit stores instead of PACK+ST (−16 +32)                 | 202 | 2.9099 | 1.5410 |
| digest comparison also charged inside the verifier replay (+17)   | 203 | 2.9144 | 1.5432 |
| both of the above (legitimate worst)                              | 219 | 2.9865 | 1.5784 |
| (disclosed; triple-counted comparison, not a single accounting)   | 236 | 3.0631 | 1.6150 |

The claim 1.60 upper-bounds every legitimate reading including narrow stores
and replayed comparison. The last row breaks it only if the same digest
comparison is charged a third time — disclosed here rather than argued away.

## 4.5 Organizer-executed evidence (declared experiment)

`experiments/manifest.json` declares `straightline-self-exec-v1`
(kind `python-message-pairs-v1`, program `experiments/builder.py`, event
`full-collision`). The program reconstructs the constructor from the IV — it
re-runs the four column quarter-rounds per trial and re-solves both
diagonals (so it does not merely echo constants) — asserts the Lemma-1
invariant `a1 + b1 + y ≡ 0 (mod 2^32)` on both diagonals for every trial,
and emits trial 0 as the byte-exact certificate pair46; the organizer
recomputes both digests and double-executes for reproducibility. This
follows the builder discipline that hardened jvr0x's 93f45e2 and closes the
"program constructs the certificate" gap that killed ca1bca4: the executed
program, not a restatement, is the claimed construction.

## 5. Witness pair and machine verification

Raw bytes (`certificates/message-a.bin`, `certificates/message-b.bin`):

    M1 = 0000000000000000000000000000000000000000000000000000000000000000
         31e88abdea4771240000000000000000c07901581bd3779a0000000000000000
    M2 = 0000000000000000000000000000000000000000000000000000000000000000
         31e88abde94771240000000000000000c07901581ad3779a0000000000000000
    H  = 9c3b8fbe64d9445bf72d12335ca2283f497c0ecbd5945d89020d61c63a93124e

LE32 words: `m8=bd8ae831 m9=247147ea m12=580179c0 m13=9a77d31b`, twelve
other words zero; `M2` decrements `m9` and `m13`. These are exactly the §3
program's outputs — the declared experiment (`experiments/builder.py`, §4.5)
executes the constructor per trial, asserts `a1+b1+m9 ≡ 0` and
`a1b+b1b+m13 ≡ 0` (the Lemma-1 invariant the refuted listing violated),
emits trial 0 byte-identical to the certificate files, and the organizer
recomputes digests against the manifest's `expected_digest` via the
organizer verifier.

The refutation itself confirmed the certificate: "the submitted certificate
is a verified ordinary collision for blake3-r1-prefix-v1" — only the
program-matches-certificate claim died. Re-verified this run:
`digest(M1,"blake3",1) = digest(M2,"blake3",1) = H` (true); 7-round BLAKE3
separates the pair (`dafe7fd22fd0118d…aa19bdec` vs
`0f341cca5426e0f0…52659062`) — the attack is 1-round-prefix specific; the
post-round-0 state difference is exactly the all-F pattern on
`{0,2,5,7,8,10,13,15}` — the Lemma-2 signature.

**Scope disclosure (unchanged):** the collision is bound to context
`(counter=0, block_len=64, flags=11)` of a single-chunk 64-byte message;
tested non-transferable to a 2-chunk tree; no full-BLAKE3 claim.

## 6. Resource fields and memory

- `time_log2 = 1.60`: §4 ledger; worst legitimate reading 1.5784 ≤ 1.60.
- `memory_log2_bytes = 12`: code = 186 instruction templates × 16 B =
  2976 B, runtime = 40 register words (160 B) + two 64-B messages + two
  32-B digests (192 B) + 64 B stack ⇒ 3392 B < 4096 B = 2^12. Explicit
  per-instruction encoding closes the panel's F-MEMORY-ENCODING-GAP; memory
  remains a reported metric.
- `preprocessing_log2 = 0`: there is no work outside the ledger — the ten
  INIT ops are inside the 78-op construction count (F-COST-PREPROCESSING
  fix). Program constants are IV-derived public values; a judge who also
  prices in-program re-derivation of the six post-column constants
  (+112 ops) lands at log2(2+298/222) = 1.74 — disclosed, not claimed;
  the primary reading treats compile-time straight-line constants as
  preprocessing ≤ 2^0, the convention 6109275's accepted-style package used.
- `nonuniform_advice_log2_bytes = 0`: uniform program, zero stored advice.
- `success_probability = 1`: deterministic identity (§2), zero trials.

## 7. Credit

Same decoupling family as the pending line on this track — winglock
(754f0f2/d60b306), jvr0x (93f45e2), jungjipdo (af4c65b), AArnott (6109275) —
independently re-derived and machine-verified here. This revision
specifically adopts: AArnott 6109275's H=2 verification-charged convention
(its ledger arithmetic is our primary convention); jvr0x 93f45e2's
organizer-executed-builder discipline (declared per-trial experiment
self-execution); winglock 754f0f2+d60b306's floor/hardened twin
strategy (our floor twin was withdrawn after the panel priced
comparison+unpacking against even the prob-1 replay argument — see the note);
and the packed-vs-narrow store lesson from the sibling-track refutation
(048680f). Co-authorship attached accordingly.
