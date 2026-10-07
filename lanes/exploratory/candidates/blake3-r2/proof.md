# Grouped m15 birthday — lane-parallel (SWAR) digest evaluator (126.218, ROT_COST=3)

Claimed `time_log2` under `collision-frontier-v5` (`C=430`): **126.218**.

This document is self-contained: the search, table procedure, verification,
cost ledger and success-probability argument are all written out below.
Grouped birthday over `2^96` groups × all `m15`; Briggs–Torczon sparse set on the
top 140 bits of `K_full` (§2.5); `prefixes[g]` reconstruction and equal-`K_full`
VERIFY with two reference compressions, `V_max=8` (§2.6); no expectations in
`T` (§3). The per-message digest evaluator is lane-parallel (SWAR, §2.2–§2.4),
with feed-forward and pack fused into an 8-op programme (Lemma F) and every
256-bit rotation charged **3** ops. Body **101**, BT **24**, total **125** ops/msg.

## Lineage / failure-pattern hardening

| prior | defect | status here |
| --- | --- | --- |
| `c1454726` | F-COST-VERIFY-OMITTED | compressions only on equal `K_full`; `V_max=8` (§2.6) |
| `4dd74401` | F-COST-INDEX-COMPARE-TAIL | worst-case compare inside BT-24 (§2.5); no expectations in `T` |
| `c36797d2` | H-COST-SPARSE-21 | explicit Briggs–Torczon, `H-COST-BT-SPARSE` @24 (not 21) |
| `7212ec23` | EVAL-F1/F2 | `prefixes[g]` (§2.1) + ≤512 Word/group (§2.3) |
| `c1a7e1b9` | F-COST-PARTIAL-COUNT-EVIDENCE | Word meter `b3r2-swar-meter` (§2.7) |
| `ef428b33` | SWAR 126.241, failed at experiment intake (likely wall-clock) | −2 body ops at the same ROT_COST=3 |
| `0a368cf8` | not_evaluable: BT / VERIFY / F1–F4 not self-contained | §2.1, §2.5, §2.6, §4, §5.2 written out in full |

## 1. Target
Unkeyed BLAKE3-256, 2 rounds, one 64-byte root block, flags 11, counter 0,
length 64. Ordinary full-digest collision of distinct messages
(`verifier/blake3.py`).

## 2. Algorithm

`N=2^128` messages as `G=2^96` groups × all `m15∈[0,2^32)`.

### 2.1 Persistent state and record layout
- `n ∈ {0,…,N}` live BT count; initially `0` (one store at run start).
- `sparse[0..2^140)` — array of 256-bit words, **never cleared**.
- `dense[0..N)`, `keys[0..N)`, `recs[0..N)` — parallel arrays of 256-bit words.
- `prefixes[0..G)` — entry `prefixes[g]` is **two** 256-bit words packing the
  fifteen 32-bit words `m0..m14` (480 bits) of group `g`. Written once at group
  setup; read only by VERIFY.

Membership: `idx` is live iff `s=sparse[idx]`, `s<n` and `dense[s]=idx`
(Briggs–Torczon). Record for live slot `s`: `dense[s]=idx` (140-bit index,
zero-padded), `keys[s]=K_full` (256 bits), `recs[s]=(g∥m15)` (96-bit group id in
the high bits, 32-bit `m15` in the low bits; one 256-bit word).

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
whole slots. ∎ Checked on every metered message (§2.7).

### 2.3 Group setup (once per group, ≤512 Word ops)
1. Draw `m0..m14` (≤20 ops); `STORE prefixes[g][0], prefixes[g][1]` (2 stores).
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
idx = top140(K_full); BT_probe_insert(K_full)   # 24  §2.5, incl. (g∥m15)+=1
on VERIFY(s): run §2.6; on accept halt
```
`Qm` slot 3 stays < 2^35 for all m15 < 2^32; higher overflow is dropped mod
2^256 (top slot). Body total: 1+12+9+30+9+30+8+2 = **101**. The `idx`
shift is charged inside the BT address/edge margin (§2.5).

**Outer control (every 256 unrolled copies):** compare block counter; branch;
increment block counter (**3** ops per 256 messages = **3/256** per message).
After `2^32` messages the group ends (exact trip count).

**Lemma F (FF+pack fusion).** After R2 diagonal G4, A,B',C',D' are clean
(Lemma S). Let `H0 = A ^ rot(C',128)` and `H1 = B' ^ rot(D',128)` (the separate
feed-forward of the 126.241 variant) and `K = H0 | (H1<<32)`. Then
`K = (A|(B'<<32)) ^ rot(C'|(D'<<32), 128)`.
*Proof.* Cleanliness ⇒ within each 64-bit slot the low 32 bits of A (resp. C')
and the low 32 bits of B' (resp. D') shifted by 32 do not overlap, so
`|` and the distributed `^` agree with separate XOR-then-OR. Also
`rot(C'|(D'<<32), 128) = rot(C',128) | (rot(D',128)<<32)` because `<<32` is
intra-slot and `rot(·,128)` permutes whole slots. Expanding the right-hand
side recovers `H0 | (H1<<32)`. ∎ `K_full` is therefore a fixed bijective
bit-permutation of the 256-bit digest: equal `K_full` ⇔ equal digest.

### 2.5 Procedure `BT_probe_insert` (≤24 Word ops, includes counter)
256-bit word RAM. Loads/stores/compares/branches/adds = 1 op each.
Membership is the Briggs–Torczon filter `dense[sparse[idx]]==idx ∧ sparse[idx]<n`.
```
s <- LOAD sparse[idx]                 # 1
if not (s < n): goto INSERT           # 1 cmp + 1 br
d <- LOAD dense[s]                    # 1
if d != idx: goto INSERT              # 1 cmp + 1 br
Ks <- LOAD keys[s]                    # 1
if Ks != K_full: goto AFTER           # 1 cmp + 1 br
return VERIFY(s)                      # 1 br  (counter still updated after VERIFY returns)
INSERT:
STORE sparse[idx] <- n                # 1
STORE dense[n] <- idx                 # 1
STORE keys[n] <- K_full               # 1
STORE recs[n] <- (g ∥ m15)            # 1  (register already live)
n <- n + 1                            # 1
AFTER:
(g ∥ m15) <- (g ∥ m15) + 1            # 1  (always; low 32 bits)
return CONTINUE                       # 1 br
```

Path primitives (including the always-taken counter add, excluding the VERIFY body):

| path | count | breakdown |
| --- | ---: | --- |
| DISCARD (live, unequal `K`) | 10 | 3 loads + 3 cmp + 3 br + 1 counter-add (+ return br shared below) |
| INSERT via empty (`s≥n`) | 10 | load+cmp+br + 4 stores + n-add + counter-add |
| INSERT via stale (`s<n`, `dense≠idx`) | **13** | load+cmp+br + load+cmp+br + 4 stores + n-add + counter-add |
| VERIFY-decide then counter | 10 | same through equal-`K` branch + counter after VERIFY returns CONTINUE |

Worst non-VERIFY path = **13** (INSERT via stale, including counter).
**Address arithmetic:** each array access may need a `base+index` addition; the
INSERT-via-stale path touches at most **six** distinct address computations after
reusing materialized `idx` and `n`. Charge **≤6**.
**Edge / packing margin:** ≤**5** ops covering `idx` extraction, flag
materialization, branch-delay slots, spare compare reorder and return-branch
accounting. Forming `(g∥m15)` is not an extra charge: that register is the live
per-message counter; its `+1` is the explicit counter line above.

**Charged envelope: 13 + 6 + 5 = 24 Word ops**, worst case on every path, with
no expectation over hit frequencies. Compressions occur **only** inside §2.6.
Live entries are never overwritten: INSERT runs only when `idx` is not live.
The SWAR slot counters `Qm`, `X3m` are separate and charged in the 101-op body.

### 2.6 VERIFY(s) — reconstruction via prefix table
`rec = LOAD recs[s]` (**1**); parse `g* = high96(rec)`, `m15* = low32(rec)` (**2**).

Rebuild stored message `M*`: `p0 ← LOAD prefixes[g*][0]`,
`p1 ← LOAD prefixes[g*][1]` (**2**); unpack `m0..m14` into a 16-word buffer and
set word 15 to `m15*` (**≤20**). Rebuild current message `M` the same way from
`prefixes[g]` (registers from this group's setup, or ≤2 reloads) and the current
`m15` (**≤20**). Then:
- If `M == M*` as 64-byte strings, return CONTINUE (not a distinct-message
  collision) — **≤16** word compares.
- Else run **two** reference compressions (`verifier/blake3.py`) and compare
  digests (**1**). If equal, **accept** and return `(M, M*)`.
- Increment the verification counter; if it exceeds `V_max=8`, **fail**.

VERIFY Word ops (non-compression) ≤80 per attempt; ≤8 attempts ⇒ ≤640 Word ops
⇒ ≤640/430 < 2 compression units. Compressions ≤ `2·V_max = 16`.

### 2.7 Meter evidence (`b3r2-swar-meter`)
`experiments/swar_meter.py` Word-meters the exact §2.4 body once per trial
(rotations charged ROT_COST=3), then evaluates every birthday digest with a
plain-int twin. A reference sample — the Word-metered message, the first 8
messages of group 0, and both messages of any returned pair — is checked
bit-for-bit against an inlined reference identical to `verifier/blake3.py`,
with `K_full == perm(digest)`. The host independently recomputes the digests of
every returned pair. Flat numeric observations only (10 keys). Birthday
consistency experiments: N_t=2^10 / 20-bit (`b3r2-grouped-spread`), N_t=2^8 /
16-bit (`b3r2-grouped-spread-16`), single-group N_t=2^8 / 16-bit stress
(`b3r2-single-group`). These are consistency checks for H1 only.
Host self-test 2026-10-07 (256 trials, flags `-B -s -P`): meter_ok 256/256,
ref_fail 0, k_fail 0 over 2248 reference checks, body_ops=101; runs replay
byte-identically.

## 3. Unconditional time ledger
| component | ops/msg | where |
| --- | ---: | --- |
| SWAR body | **101** | §2.4 / `H-COST-SWAR-EVAL` |
| BT + K compare + (g∥m15) counter | **24** | §2.5 / `H-COST-BT-SPARSE` |
| **Per-message dominant** | **125** | |
| Outer unroll control | 3/256 | §2.4 |

Once-per-run / rare: init `n←0` (1 Word); group setup ≤512 Word/group × `2^96`
(§2.3); VERIFY ≤16 compressions and ≤640 Word → `<2` units (§2.6).
Group-setup units `2^96·512/430 < 2^96·1.191 < 2^97`.

    T ≤ 2^128·(125+3/256)/430 + 16 + 2 + 2^96·512/430
      < 2^126.21773  <  2^126.218.

Claim **126.218**. No expectations in the inequality: index-hit compares are
worst-case inside the 24-op BT line.

## 4. Success probability
Under H1 the `N=2^128` digests are independent uniform 256-bit strings, and
`idx = top140(K_full)` is uniform because `K_full` is a fixed bijective
bit-permutation of the digest (Lemma F).

`F1` (no 256-bit collision among the N digests): `Pr ≤ Π_{i<N}(1−i/2^256)
≤ exp(−N(N−1)/2^257) = e^{−1/2+2^{−129}} < 0.606531`.

`F2` (earliest-completing pair displaced). Let `E` be the event that some
colliding pair exists. On `E`, let `(a*,b*)` be the ordered pair with
`pos(a*)<pos(b*)` and `digest(a*)=digest(b*)` minimizing `(pos(b*),pos(a*))`
lexicographically. Outside `F3`, no message before `b*` collides with an earlier
message (a live entry with key `K(a*)` would be an earlier-completing pair), so
when `a*` is probed its `idx` is either free (then `a*` is inserted and, since
live entries are never overwritten, still live with key `K(a*)` when `b*` is
probed, which reaches VERIFY and accepts) or already live with a **different**
key (then `a*` is discarded). `F2` is the latter. Fewer than `N` entries are
live, so under H1 `Pr[F2 | E] ≤ N/2^140 = 2^{−12}`. The conditioning that defines
`(a*,b*)` couples `digest(a*)` with `digest(b*)` but, under H1, does not couple
`idx(a*)` to the keys of unrelated earlier live entries beyond this bound.

`F3` (two groups draw identical prefixes `m0..m14`): at most `2^191` prefix
pairs, each equal with probability `2^{−480}`, so `Pr < 2^{−287}`.

`F4` (`V_max` exhausted before a true verify): VERIFY is entered only on equal
`K_full`, i.e. equal digests. For distinct messages that is a genuine collision
and the first such VERIFY accepts. VERIFY returns CONTINUE only when `M == M*`,
which requires two groups with identical prefixes (within a group `m15` values
are distinct), i.e. `F3`. Outside `F3` at most one VERIFY occurs, so `F4 ⊆ F3`.

Under H1: success `> 1 − 0.606531 − 2^{−12} − 2^{−287} − ε > 0.3932`, where `ε` is
the negligible model gap declared in H1. Claim **0.39**.

## 5. Heuristics
### 5.1 `H1-grouped-digests`
Modeling hypothesis for F1 and the F2 conditioning (§4). The time bound does not
use H1. Experiments are matched-scale consistency checks (`N_t^2/2^w = 1 =
N^2/2^256`) and do not establish full-scale 256-bit iid behaviour.

### 5.2 `H-COST-BT-SPARSE`
The §2.5 procedure, including the always-taken `(g∥m15)` counter update, one
256-bit `K_full` compare and the address/edge margin, fits in ≤**24** charged
primitives per message on the organizer 256-bit word RAM. Evidence: the §2.5
op list and path table (13 path + 6 address + 5 edge). No page-walk model beyond
1-op word addressing; not microbenchmarked. Fallback: a 28-op envelope gives 129
ops/msg → `time_log2 = 126.264`.

### 5.3 `H-COST-SWAR-EVAL`
The §2.4 body computes `K_full` in exactly 101 Word ops at ROT_COST=3. Evidence:
Lemma S, Lemma F, the line-by-line count in §2.4 and the meter in §2.7.
Observation op counts are harness-untrusted; the adjudicated content is the
analytic ledger plus readable meter source.

## 6. Memory
- `sparse`: `2^140` × 32-byte words = `2^145` bytes (never cleared; no zeroing pass).
- `dense/keys/recs`: ≤ `2^128 × 3 × 32 = 2^128·96` bytes.
- `prefixes`: `2^96 × 2 × 32 = 2^102` bytes.
Peak `< 2^146` bytes. Claim `memory_log2_bytes = 146`.

## 7. Fallback ladder
| variant | ops | time_log2 |
| --- | ---: | ---: |
| this package (rot=3, fused FF+pack) | 125 | 126.218 |
| BT envelope 28 | 129 | 126.264 |
| separate FF + pack (rot=3) | 127 | 126.241 |

## 8. Refused
21-op sparse; pack=0; BT<24; public 247; expectations in `T`; skipping VERIFY;
omitting `prefixes[g]`; delayed-reduction / mask-before-rotate; ROT_COST=1.
