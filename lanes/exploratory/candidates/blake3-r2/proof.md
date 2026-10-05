# Grouped partial-evaluation birthday search (tightened ledger)

The scalar below is `time_log2` under `collision-frontier-v5` with `C = 430`.
Memory is a separately reported resource bound.

This exploratory package targets `blake3-r2-prefix-v1`. It proposes a classical
randomized birthday search with algorithmic success probability at least 0.39
under heuristic H1, total charged time at most `2^127.417` units, and peak
memory at most `2^146` bytes. These are analytical upper bounds on charged
computation, not measured wall-clock costs. The claimed scalar is **127.417**.

## Provenance and relation to 127.524

- Awaiting-review `8e870aed` claims **127.524** with the **same algorithm** and
  an inner body of **260** Word ops plus **14** spare (309 ops/msg).
- This package keeps the algorithm, probability argument, memory bound, and
  organizer-faithful **30**-op full G count. It tightens only:
  1. omit redundant feed-forward `& MASK` (8 ops → FF total 8 instead of 16);
  2. drop the **14**-op spare that was an explicit conservatism envelope.
- Resulting per-message ops: `252 + 14 + 21 = 287` → **127.417**.
- Public awaiting-review note near **127.481** used an inner body of **247**.
  That figure undercounts organizer `_g` (30 ops) as 29 on several segments.
  This write-up does **not** adopt 247; it uses independently metered 252/260.

## 1. Target and message layout

Unkeyed BLAKE3-256 with exactly 2 compression rounds. Each message is 64 bytes:
one chunk, one root compression, counter 0, block length 64, flags
`CHUNK_START|CHUNK_END|ROOT = 11`. Digest lanes are `o[i] = v[i] XOR v[i+8]`
after two rounds. Reference: `verifier/blake3.py`.

Messages are organised as `N = 2^128 = 2^96` groups × `2^32` values of `m15`,
with `m0..m14` fixed per group from fresh coins.

## 2. Why `m15` amortises

Round-1 G-schedule uses `(m0,m1),...,(m14,m15)` in order, so `m15` is only the
**y** input of the last diagonal `G(3,4,9,14,m14,m15)`. After
`PERM = (2,6,3,10,7,0,4,13,1,11,12,5,9,14,15,8)`, round 2 uses original `m15`
only as the **x** input of the last diagonal. After round 1 only
`v3,v4,v9,v14` depend on `m15`. Each round-2 column G receives exactly one of
those lanes (roles b,c,d,a). Diagonals and feed-forward are fully recomputed.

Bit-exact check: thousands of random `(prefix, m15)` evaluations of the partial
body matched `blake3(message, 2)`.

## 3. Algorithm

1. For each of `2^96` groups: draw uniform `m0..m14`, run group setup, then for
   `m15 = 0..2^32-1` run the inner body, pack key `K`, and probe/insert a
   Briggs-Torczon sparse set on the top 140 bits of `K`.
2. On a key match: rebuild both messages and re-verify with two full reference
   compressions (2 units). Accept iff messages differ and all 256 bits agree.

## 4. Word-op cost model

Counting matches `scripts/reference_operation_costs.py`. Organizer `_g` = 30.
A white-box whole 2-round compression is ~496 ops (> C), so raw Word-op full
compressions are not cheaper than one unit. Savings come only from skipping
identical work.

### 4.1 Setup (once/group): 236 ops → negligible after `/C` across `2^96` groups.

### 4.2 Inner body: **252** ops

| segment | ops |
| --- | ---: |
| finish R1 last G (`y=m15`) | 15 |
| column 0 full G | 30 |
| column 1 (reuse `a1,d1`) | 22 |
| column 2 (reuse `a1'`) | 27 |
| column 3 full G | 30 |
| four diagonal G | 120 |
| eight digest xors (**no** trailing `& MASK`) | 8 |
| **total** | **252** |

**Why FF `& MASK` is omitted.** Every G write applies `& MASK`
(`verifier/blake3.py:_g`). After round 2, all `v[i]` lie in `[0,2^32)`, so
`o[i]=v[i] XOR v[i+8]` already lies in `[0,2^32)` without a further mask.
Values match the masked computation bit-exactly.

**Fallback:** if a reviewer requires explicit FF masks, inner = 260, and with
no spare: `260+14+21=295` → **127.457**.

### 4.3 Per-message overhead: 35 ops

- Pack eight lanes into a 256-bit table key: **14**
- Sparse-set probe/insert: **21**
- **No spare.** Loop control uses unroll `U=256` (`3/256` ops/msg, absorbed).

**Fallback:** restoring the 14-op spare on the masked inner returns
`260+14+21+14=309` → **127.524** (`8e870aed`).

### 4.4 Total

    ops_msg = 287
    T < 2^128 · 287/430
    287/430 ≈ 0.6674418605
    log2(287/430) ≈ -0.583286
    T < 2^{127.41672} < 2^{127.417}.

Claim `time_log2 = 127.417`.

Reload-all fallback (27 extra loads/msg): `287+27=314` → **127.546**.

## 5. Success probability

`F1`: `Pr[no collision] < exp(-1/2+2^{-128}) < 0.606531`.
`F2`: displacement miss `≤ N·2^{-140}=2^{-12}<0.000244`.
`F3`: identical prefixes `< 2^{-287}`.
Under H1: success `> 0.3932`. Claim **0.39**.

## 6. Heuristic H1-grouped-digests (score-critical)

See `claim.json`. Organizer experiments at matched scales `N_t^2/2^w=1` for
`w∈{16,20,24}` plus a single-group stress layout support truncated collision
statistics; extrapolation to 256 bits remains a modeling hypothesis.

## 7. Experiments

| id | layout | mask bits | N_t^2/2^w |
| --- | --- | ---: | ---: |
| `b3r2-grouped-spread` | 32×32 | 20 | 1 |
| `b3r2-grouped-spread-16` | 16×16 | 16 | 1 |
| `b3r2-grouped-spread-24` | 64×64 | 24 | 1 |
| `b3r2-single-group` | 1×1024 | 20 | 1 |

Digests from the partial evaluator only; organizer re-verifies mask events.

## 8. Memory / preprocessing / advice

Peak `< 2^{146}` bytes (sparse universe `2^{140}`). `preprocessing_log2=0`.
Advice 0. Memory unscored under v5.

## 9. Comparison

| package | time_log2 | notes |
| --- | ---: | --- |
| Organizer sort | 140 | |
| `18ad754c` | 128.11 | multi-trail VOW |
| `8e870aed` | 127.524 | same algo; spare + masked FF |
| Public ~127.481 | 127.481 | untrusted; 247-op inner not adopted |
| **This package** | **127.417** | 287 ops; honest 30-op G |

## 10. Evidence summary

Algorithm §§1–3; cost §4; probability §5; H1 §6; experiments §7.
Certificates: empty valid manifest. `submission_state=ready`.
`baseline_improved=blake3-r2-nominal-v2` is metadata, not an improvement claim
over a qualified baseline.
