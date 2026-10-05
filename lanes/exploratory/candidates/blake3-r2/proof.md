# Grouped m15 birthday — lane-parallel (SWAR) digest evaluator (126.241)

Claimed `time_log2` under `collision-frontier-v5` (`C=430`): **126.241**.

Same search as the 127.432 lineage (grouped birthday, 2^96 groups × all m15,
Briggs–Torczon sparse set on top-140 bits, `prefixes[g]` reconstruction,
equal-`K_full` VERIFY with two reference compressions, `V_max=8`, no
expectations in `T`). **Only the per-message digest evaluator changes**: the
scalar 252+14 = 266-op partial evaluator + pack is replaced by a 103-op
lane-parallel evaluator that uses the 256-bit word width the cost model already
charges for.

## Lineage / failure-pattern hardening (all retained)

| prior | defect | status here |
| --- | --- | --- |
| `c1454726` | F-COST-VERIFY-OMITTED | compressions only on equal `K_full`; `V_max=8` |
| `4dd74401` | F-COST-INDEX-COMPARE-TAIL | worst-case compare inside BT-24; no expectations in `T` |
| `c36797d2` | H-COST-SPARSE-21 | explicit BT, `H-COST-BT-SPARSE` @24 (not 21) |
| `7212ec23` | EVAL-F1/F2 | `prefixes[g]` + ≤512 Word/group |
| `c1a7e1b9` | F-COST-PARTIAL-COUNT-EVIDENCE | answered by Word meter `b3r2-swar-meter` (count + bit-exactness) |

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

### 2.4 Per-message step (inside 256-way unroll) — 103 + 24 Word ops
```
A  = Qm & M4                         # 1   (= A+B'+Y1d, slot3 carries m15)
D' = ror4(D'^A, 8); C' = (C'+D')&M4; B' = ror4(B'^C', 7)   # 12
(A,B,C,D) = undiag(A,B',C',D')       # 9   (3 rotations × 3)
(A,B,C,D) = G4(A,B,C,D, X2, Y2)      # 30  R2 columns
(A,B',C',D') = diag(A,B,C,D)         # 9
(A,B',C',D') = G4(A,B',C',D', X3m, Y3)  # 30  R2 diagonals (slot3 x = m15)
H0 = A  ^ rot(C',128)                # 4   h0..h3
H1 = B' ^ rot(D',128)                # 4   slot j = h_{4+(j+1)%4}
K_full = H0 | (H1 << 32)             # 2   fixed bit-permutation of digest
Qm  += 2^192 ; X3m += 2^192          # 2   slot-3 m15 counters
BT_probe_insert(K_full)              # 24  127.432 §2.4 unchanged, incl. (g∥m15)+=1
```
`Qm` slot 3 stays < 2^35 for all m15 < 2^32; higher overflow is dropped mod
2^256 (top slot). Body total: 1+12+9+30+9+30+4+4+2+2 = **103**.
`idx = top140(K_full)` is formed inside the BT address margin, as before.

### 2.5 BT and VERIFY
Unchanged from 127.432 §2.4–§2.5 (24-op envelope with counter; VERIFY rebuilds
both messages from `prefixes`/`recs`, ≤16 compressions, ≤640 Word ops).

### 2.6 Meter evidence (`b3r2-swar-meter`)
`experiments/swar_meter.py` runs the exact §2.4 body under a Word class that
counts every 256-bit op (rotations charged 3), checks the digest bit-for-bit
against an inlined reference identical to `verifier/blake3.py`, and checks
`K_full == perm(digest)`. Local self-test (40 trials, 33,401 messages):
meter_ok 33401/33401, ref_ok 33401/33401, k_ok 33401/33401; masked detections
20/40 (0.50, consistent with 0.393 at this sample size). An independent
frontier meter (`../meters/bet_meters.py`, staging workspace) reproduces the live 252 body and gets
103 (rot=3) / 87 (rot=1) over 1,152 messages including m15 ∈ {0, 2^32−1}.

## 3. Unconditional time ledger
| component | ops/msg |
| --- | ---: |
| SWAR body (§2.4) | **103** |
| BT + K compare + (g∥m15) counter | 24 |
| **Per-message dominant** | **127** |
| outer unroll control | 3/256 |

    T ≤ 2^128·(127+3/256)/430 + 16 + 2 + 2^96·512/430
      < 2^126.24063  <  2^126.241.

Claim **126.241**. No expectations in the inequality.

## 4. Success probability
Identical to 127.432 §4 (F1 < 0.606531, F2 ≤ 2^-12 with earliest-completing
pair, F3 < 2^-287, F4 negligible with V_max=8). `K_full` is a fixed bijective
bit-permutation of the digest, so equal-K ⇔ equal digest and, under H1,
`top140(K_full)` is uniform. Success > 0.3932; claim 0.39.

## 5. Heuristics
`H1-grouped-digests` (unchanged), `H-COST-BT-SPARSE` (unchanged 24),
`H-COST-SWAR-EVAL` (new; deterministic 103-op count, Lemma S + meter).

## 6. Memory
Unchanged: peak < 2^146 bytes.

## 7. Fallback ladder (each still far below 127.432)
| variant | ops | time_log2 |
| --- | ---: | ---: |
| this package (rot=3) | 127 | 126.241 |
| BT envelope 28 | 131 | 126.286 |
| + scalar 14-op pack instead of 2-op perm pack | 139 | 126.371 |
| rotation credited as 1-op primitive (next undercut) | 111 | 126.047 |

## 8. Refused
21-op sparse; pack=0; BT<24; public 247; expectations in `T`; skipping VERIFY;
omitting `prefixes[g]`.
