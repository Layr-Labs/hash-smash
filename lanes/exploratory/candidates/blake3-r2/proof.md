# Grouped m15 birthday — lane-parallel (SWAR) digest evaluator (126.218, ROT_COST=3)

Claimed `time_log2` under `collision-frontier-v5` (`C=430`): **126.218**.

Same search as the 127.432 / ef428b33 lineage (grouped birthday, 2^96 groups ×
all m15, Briggs–Torczon sparse set on top-140 bits, `prefixes[g]` reconstruction,
equal-`K_full` VERIFY with two reference compressions, `V_max=8`, no
expectations in `T`). **Only the per-message digest evaluator changes** relative
to ef428b33 @126.241: the separate feed-forward + pack (10 ops) is fused into an
8-op programme that computes the same `K_full` bit-permutation. ROT_COST stays
**3**. Body 103 → **101**.

## Lineage / failure-pattern hardening (all retained)

| prior | defect | status here |
| --- | --- | --- |
| `c1454726` | F-COST-VERIFY-OMITTED | compressions only on equal `K_full`; `V_max=8` |
| `4dd74401` | F-COST-INDEX-COMPARE-TAIL | worst-case compare inside BT-24; no expectations in `T` |
| `c36797d2` | H-COST-SPARSE-21 | explicit BT, `H-COST-BT-SPARSE` @24 (not 21) |
| `7212ec23` | EVAL-F1/F2 | `prefixes[g]` + ≤512 Word/group |
| `c1a7e1b9` | F-COST-PARTIAL-COUNT-EVIDENCE | answered by Word meter `b3r2-swar-meter` (count + bit-exactness) |
| `ef428b33` | (SWAR 126.241, failed at experiment intake, likely timeout) | this package undercuts by −2 body ops at same ROT_COST=3 |

## 1. Target
Unkeyed BLAKE3-256, 2 rounds, one 64-byte root block, flags 11, counter 0,
length 64. Ordinary full-digest collision of distinct messages
(`verifier/blake3.py`).

## 2. Algorithm

### 2.1 Persistent state
As 127.432 §2.1: `n`, never-cleared `sparse[0..2^140)` of 256-bit words,
`dense/keys/recs[0..2^128)`, `prefixes[0..2^96)` (two words per group).

### 2.2 Representation (SWAR)
A 256-bit word holds four 64-bit slots; slot j = bits [64j, 64j+64). A lane
value lives in the low 32 bits of its slot; the high 32 bits are **zero** in
every *clean* word. Constant `M4 = Σ_j (2^32−1)·2^{64j}` is register-resident.
State words (column form): `A=(v0..v3) B=(v4..v7) C=(v8..v11) D=(v12..v15)`.

`ror4(t,n) = ((t>>n) | (t<<(32−n))) & M4` — 4 ops, rotates all four lanes.

`G4(A,B,C,D,X,Y)` (30 ops; same 8-line shape as organizer `_g`):
```
A=(A+B+X)&M4   D=ror4(D^A,16)   C=(C+D)&M4   B=ror4(B^C,12)
A=(A+B+Y)&M4   D=ror4(D^A,8)    C=(C+D)&M4   B=ror4(B^C,7)
```
Diagonal form: `B'=rot(B,64) C'=rot(C,128) D'=rot(D,192)` (right-rotation of a
256-bit word by 64k bits), so slot j holds the j-th diagonal G
`(j, 4+(j+1)%4, 8+(j+2)%4, 12+(j+3)%4)` — exactly organizer G4..G7.
**Each 256-bit rotation is charged 3 ops** (`(x>>k)|(x<<(256−k))`), not the
1-op "rotation" primitive the cost model lists.

**Lemma S (carry isolation).** If A,B,C,D,X,Y are clean, every G4 line yields
the organizer lane values in every slot and a clean word. *Proof.* Sums of ≤3
clean slots are < 2^34 < 2^64, so no carry crosses a slot boundary; `&M4`
restores clean. For clean t, `t>>n` puts lane bits [n,32) at [0,32−n) and the
slot's zero high bits at [32−n,32); the next slot's low n bits land in
[64−n,64) (high half). `t<<(32−n)` puts lane bits [0,n) at [32−n,32); bits
landing in the high half or shifted in from the previous slot's (zero) high
bits [32+n,64) are cleared by `&M4`; slot 3 overflow beyond bit 256 is
discarded mod 2^256. Hence the low 32 bits of each slot equal
`ror32(lane,n)`. XOR of clean words is clean. Slot rotations by 64k permute
whole slots. ∎ Checked on every metered message (§2.6).

### 2.3 Group setup (once per group, ≤512 Word ops)
Identical to ef428b33 / draft_swar_126.241 §2.3:
1. Draw `m0..m14` (≤20 ops); store `prefixes[g]` (2 stores).
2. Build slot words from message words (≤48 ops): R1 `X1,Y1`, R1-diag `X1d`,
   `Y1d_base=(m9,m11,m13,0)`, R2 `X2=(p0,p2,p4,p6)`, `Y2=(p1,p3,p5,p7)`,
   `X3_base=(p8,p10,p12,0)`, `Y3=(p9,p11,p13,p15)` where `p=m∘PERMUTATION`
   (`p14 = m15` is the varying word).
3. R1 column G4 (30), diagonalize (9), first half of R1 diagonal G4 (15) —
   all independent of m15 (m15 is the y-input of R1 diagonal slot 3).
4. `Q = A + B' + Y1d_base` (2, unmasked: slots < 2^34). Counter registers
   `Qm ← Q`, `X3m ← X3_base` (m15 = 0 in slot 3), `(g∥m15) ← g∥0`.
Metered setup ≈ 56 + 48 + 20 + 2 + 2 ≈ 128 ≤ 512.

### 2.4 Per-message step (inside 256-way unroll) — 101 + 24 Word ops
```
A  = Qm & M4                         # 1   (= A+B'+Y1d, slot3 carries m15)
D' = ror4(D'^A, 8); C' = (C'+D')&M4; B' = ror4(B'^C', 7)   # 12
(A,B,C,D) = undiag(A,B',C',D')       # 9   (3 rotations × 3)
(A,B,C,D) = G4(A,B,C,D, X2, Y2)      # 30  R2 columns
(A,B',C',D') = diag(A,B,C,D)         # 9
(A,B',C',D') = G4(A,B',C',D', X3m, Y3)  # 30  R2 diagonals (slot3 x = m15)
AB = A | (B' << 32)                  # 2
CD = C' | (D' << 32)                 # 2
CD = rot(CD, 128)                    # 3
K_full = AB ^ CD                     # 1   fused FF+pack (= 8)
Qm  += 2^192 ; X3m += 2^192          # 2   slot-3 m15 counters
BT_probe_insert(K_full)              # 24  127.432 §2.4 unchanged, incl. (g∥m15)+=1
```
`Qm` slot 3 stays < 2^35 for all m15 < 2^32; higher overflow is dropped mod
2^256 (top slot). Body total: 1+12+9+30+9+30+8+2 = **101**.

**Lemma F (FF+pack fusion).** After R2 diagonal G4, A,B',C',D' are clean
(Lemma S). Let `H0 = A ^ rot(C',128)` and `H1 = B' ^ rot(D',128)` as in
ef428b33, and `K = H0 | (H1<<32)`. Then
`K = (A|(B'<<32)) ^ rot(C'|(D'<<32), 128)`.
*Proof.* Cleanliness ⇒ within each 64-bit slot the low 32 bits of A (resp. C')
and the low 32 bits of B' (resp. D') shifted by 32 do not overlap, so
`|` and the distributed `^` agree with separate XOR-then-OR. Also
`rot(C'|(D'<<32), 128) = rot(C',128) | (rot(D',128)<<32)` because `<<32` is
intra-slot and `rot(·,128)` permutes whole slots. Expanding the right-hand
side recovers `H0 | (H1<<32)`. ∎ Same fixed bit-permutation of the digest;
equal-K ⇔ equal digest; top140 uniform under H1.

### 2.5 BT and VERIFY
Unchanged from 127.432 §2.4–§2.5 (24-op envelope with counter; VERIFY rebuilds
both messages from `prefixes`/`recs`, ≤16 compressions, ≤640 Word ops).

### 2.6 Meter evidence (`b3r2-swar-meter`)
`experiments/swar_meter.py` Word-meters the exact §2.4 body once per trial
(rotations charged ROT_COST=3), then evaluates every birthday digest with a
plain-int twin. A reference sample — the Word-metered message, the first 8
messages of group 0, and both messages of any returned pair — is checked
bit-for-bit against an inlined reference identical to `verifier/blake3.py`,
with `K_full == perm(digest)`. (Checking every message was dropped to fit the
organizer's 20s per-run Docker timeout; the host independently recomputes the
digests of every returned pair, so detections are not trusted from the
program.) Flat numeric observations only (10 keys).

Birthday consistency experiments run at two matched scales, N_t=2^10 / 20-bit
(`b3r2-grouped-spread`) and N_t=2^8 / 16-bit (`b3r2-grouped-spread-16`), plus
a single-group N_t=2^8 / 16-bit structured stress (`b3r2-single-group`). The
earlier 2^12 / 24-bit scale was dropped for wall-clock. These are consistency
checks for H1 only, never full-scale evidence.

Host self-test 2026-10-07 (256 trials each, organizer flags `-B -s -P`):
meter_ok 256/256, ref_fail 0, k_fail 0 over 2248 reference checks,
body_ops=101; all runs replay byte-identically.

## 3. Unconditional time ledger
| component | ops/msg |
| --- | ---: |
| SWAR body (§2.4) | **101** |
| BT + K compare + (g∥m15) counter | 24 |
| **Per-message dominant** | **125** |
| outer unroll control | 3/256 |

    T ≤ 2^128·(125+3/256)/430 + 16 + 2 + 2^96·512/430
      < 2^126.21773  <  2^126.218.

Claim **126.218**. No expectations in the inequality.

## 4. Success probability
Identical to 127.432 §4 (F1 < 0.606531, F2 ≤ 2^-12 with earliest-completing
pair, F3 < 2^-287, F4 negligible with V_max=8). `K_full` is a fixed bijective
bit-permutation of the digest, so equal-K ⇔ equal digest and, under H1,
`top140(K_full)` is uniform. Success > 0.3932; claim 0.39.

## 5. Heuristics
`H1-grouped-digests` (unchanged), `H-COST-BT-SPARSE` (unchanged 24),
`H-COST-SWAR-EVAL` (101-op count at ROT_COST=3, Lemma S + Lemma F + meter).

## 6. Memory
Unchanged: peak < 2^146 bytes.

## 7. Fallback ladder (each still far below 127.432)
| variant | ops | time_log2 |
| --- | ---: | ---: |
| this package (rot=3, fused FF+pack) | 125 | 126.218 |
| BT envelope 28 | 129 | 126.264 |
| parent ef428b33 without fusion (rot=3) | 127 | 126.241 |
| scalar flat-obs fail-fallback | 290 | 127.432 |

## 8. Refused
21-op sparse; pack=0; BT<24; public 247; expectations in `T`; skipping VERIFY;
omitting `prefixes[g]`; delayed-reduction / mask-before-rotate (competitor
lever — not used here); ROT_COST=1 (CoS HOLD).
