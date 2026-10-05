# SHA3-256 prefix rounds 0–5: unconditional 32-bit radix (visible spare, 128.25)

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is a
separately reported resource bound and does not affect the score.

Selected lane: exploratory. Target: `sha3-256-r6-prefix-v1`.
This finite classical algorithm has total charged time at most 2^128.25,
peak memory at most 2^136 bytes, and success probability at least 0.39.
The proposed scalar is **128.25**. It is a generic analytic construction
with infeasible resource use, not a claimed cryptanalytic advance.
`baseline_improved: sha3-256-r6-nominal-v2` is the required nominal reference
identifier only; nominal display 128 is not an established attack.

**Provenance.** Zero-spare itemization at 128.24 (gen64/pp28/scan16) was
**refuted** under paired review. Awaiting-review `5cbeddb` at **128.26** uses
gen72/pp30/scan20. This package sits between them: **visible spare** above the
itemized floor (generate **68**, per-pass **29** = 28+1, scan **18**) while
improving on 128.26. Empty heuristics. Does not alter awaiting-review tickets.

## 1. Exact complete hash and legal messages

Let `Q = ceil(9943 * 2^128 / 10000)` and `N = 2^256`. Numerically
`Q = 338342757429489101165234520331412045824`
(`2^127.99175 < Q < 2^127.99176`). Messages are all 64-byte strings
`LE32(u)||LE32(v)` (`|D|=2^512`).

SHA3-256 sponge: rate 1088, capacity 512, all-zero IV, suffix `0x06` + pad10*1,
prefix rounds 0..5, full 256-bit digest. One absorption; no squeeze permutation.

H(u,v): zero 25 lanes; load u,v into A[0..3], A[4..7]; set A[8]=0x06,
A[16]=0x8000000000000000; apply six Keccak-f rounds with standard rho and RC[0..5]
as in FIPS 202 / organizer `verifier/keccak.py`; return
`d = A[0]|(A[1]<<64)|(A[2]<<128)|(A[3]<<192)`. One selected permutation costs 1
unit; other word ops cost 1/1626.

## 2. Algorithm

Two arrays Src, Dst of Q three-word records `(digest,u,v)`; Cnt/Pos of length
`2^32`.

**Generate:** no bulk zero of Src/Dst (every Src slot overwritten; first scatter
fills Dst). For i=0..Q-1 draw u_i,v_i, store (H(u_i,v_i), u_i, v_i).

**LSD 32-bit radix:** for k=0..7, counting-sort by `(d>>(32*k)) AND (2^32-1)`,
swap bases. Eight passes cover 256 bits.

**Scan:** adjacent equal digests with distinct messages → recompute H, emit.

## 3. Unconditional success

Schur/averaging: uniform digests maximize Pr(all distinct). With stated Q,
`Q(Q-1)/(2N)=0.494316245 > -ln(0.61)`, so `Pr(E)>0.390012`. Message repeats
`Pr(R)<2^{-256}`. Hence `Pr(success)>0.39`. Heuristics empty.

## 4. Cost (C=1626) — visible spare

**H wrapper:** ≤56 ordinary ops (25 clears + extracts + pad + pack + bookkeeping).

**Generate:** 2 rand + 56 wrapper + 3 stores + loop with spare → **68**
(itemized minimum toward 64; **+4 spare**).

**Radix per record per pass:** hist 8 + scatter 20 = 28 itemized; **+1 spare → 29**.

**Scan per adjacent pair:** **18** (above a tight 16 itemization; **+2 spare**).

**Tables:** 8 × 4 × 2^32 ≤ 2^37. **Fixed load:** 2^30. No Src/Dst bulk zero.

| Phase | Perms | Ordinary ops |
| --- | ---: | ---: |
| Fixed load | 0 | 2^30 |
| Generate | Q | 68 Q |
| 8 × 29/record | 0 | 232 Q |
| Table O(1) | 0 | 2^37 |
| Scan | 0 | 18 Q |
| Verify | ≤2 | 2^14 |

    W ≤ (68+232+18)Q + 2^30 + 2^37 + 2^14 = 318 Q + 138512711680
    T ≤ Q + 2 + 318Q/1626 + 138512711680/1626
      = Q(1944/1626) + … = Q(972/813) + …
      < 1.1970 · Q + 2^27
      < 2^128.2495

Exact Q: `T < 2^128.24946`. Claim **128.25** (`2^128.24946 < 2^128.25`).

Spare summary versus refuted zero-spare 128.24 (Wcoef 304): this Wcoef **318**
(+14). Versus awaiting 128.26 (Wcoef 332): this is tighter (−14) while keeping
explicit positive spare on every hot path.

Preprocessing: fixed load only; `preprocessing_log2: 30`.

## 5. Memory

`M ≤ 192Q + 2^38 + 2^24 < 2^136`. Fields as in claim.json.

## 6. Limitations

Analytic infeasible birthday bound; not a structural 6-round break. Spare is
intentional after 128.24 refutation. No certificates/experiments. DP/H-RF work
is separate research and not claimed here.

## 7. Provenance

Between refuted 128.24 and awaiting-review 128.26 spare profile. Fresh review
required. Does not modify `5cbeddb` or `25f61e1`.
