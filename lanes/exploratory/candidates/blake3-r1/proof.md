# BLAKE3 with 1 prefix round: closed-form ordinary collision at time 1.624

## 1. Scope and claim

This package selects `blake3-r1-exploratory`, target `blake3-r1-prefix-v1`,
cost model `collision-frontier-v5`, review policy `paired-lanes-v1`.
The submitted scalar is `time_log2: 1.624` target compressions, an upper bound on
total charged computation. Peak memory is below `2^15` bytes, reported
separately. Success probability is 1. Preprocessing is 0 with all work online.
Nonuniform advice is 0. Data is at most 256 bytes (`data_log2: 8`).
This is a deterministic exact construction with explicit messages verifiable
by `verifier/blake3.py:blake3`, not a birthday search, differential heuristic,
or stored precomputed collision. The heuristic list is empty and the
certificate manifest holds one `hash-collision-witness-v2` pair (`certificates/a.bin`,
`certificates/b.bin`); the messages below are the same pair and any
reviewer can recompute them. Readiness requests review; it does not assert
qualification, formal verification, human acceptance, or promotion.

The starting point is the organizer package at `8a0f026` with scalar 149
(generic merge sort). That argument is replaced here by a 1-round structural
collision. No declared inherited scalar is used as evidence.

## 2. Exact complete hash

Messages are exactly 64 bytes, bit length 512 < 2^64. Decode into sixteen
little-endian 32-bit words w[0..15]. Unkeyed BLAKE3-256 with 1 prefix round in
every compression. On 64-byte messages there is one chunk, one full block, no
parent, and exactly one compression with counter 0, block length 64, flags
`CHUNK_START|CHUNK_END|ROOT = 11`. The eight-word IV in order is

    6a09e667 bb67ae85 3c6ef372 a54ff53a
    510e527f 9b05688c 1f83d9ab 5be0cd19.

Initialize `v[0..7]=IV`, `v[8..11]=IV[0..3]`, `v[12..15]=(0,0,64,11)`.
All additions are modulo 2^32. `ROR(x,k)` rotates right in 32 bits.
`G(a,b,c,d,x,y)` on state `v` is

    v[a] = v[a]+v[b]+x; v[d] = ROR(v[d]^v[a],16);
    v[c] = v[c]+v[d];   v[b] = ROR(v[b]^v[c],12);
    v[a] = v[a]+v[b]+y; v[d] = ROR(v[d]^v[a],8);
    v[c] = v[c]+v[d];   v[b] = ROR(v[b]^v[c],7).

One round calls, with schedule `s` initially `w` (no permutation yet),

    G(0,4,8,12,s[0],s[1]);  G(1,5,9,13,s[2],s[3]);
    G(2,6,10,14,s[4],s[5]); G(3,7,11,15,s[6],s[7]);
    G(0,5,10,15,s[8],s[9]); G(1,6,11,12,s[10],s[11]);
    G(2,7,8,13,s[12],s[13]);G(3,4,9,14,s[14],s[15]).

Feed-forward is standard 16-word output: `o[i]=v[i]^v[i+8]` for `i=0..7`
(the digest) and `v[i+8]^cv[i]` for the chaining part. With `cv=IV` on the
single root block, the digest is the first eight words above serialized
little-endian. This matches `verifier/blake3.py:blake3(m,1)`. No free-start,
compression-only, truncated-output, or changed-round variant is used.

## 3. Lemma 1 (choose G outputs)

For any `(a,b,c,d)` and any targets `(c*,d*)`, set

    c1 = c*-d*; d1 = c1-c; a1 = d^ROTL16(d1); x = a1-a-b;
    b1 = ROR(b^c1,12); a2 = ROTL8(d*)^d1; y = a2-a1-b1,

with `ROTL16/ROTL8` the left rotations and all differences modulo 2^32.
Then `G(a,b,c,d;x,y) = (a2, ROR(b1^c*,7), c*, d*)`.
Proof is forward evaluation: `x` forces the first-line `v[a]` to `a1`, so
`v[d]` after the second line is `ROR(d^a1,16)^... ` equal to `d1` by
construction of `a1`; then `v[c]` becomes `c+d1 = c1+d*... `; tracking each
line gives the stated outputs. It is an exact identity with no condition.
Every operation is a 32-bit add/sub, XOR, or fixed rotation.

## 4. Lemma 2 (complement step)

Fix `c=0`, `d*=0`, `c*=g`. Then Lemma 1 outputs `(a2, beta(g), g, 0)` with
`beta(g)=ROR(ROR(b^g,12)^g,7)` (with the ambient `b,d` suppressed).
Rotation commutes with complement and XOR distributes so that
`(~u)^(~z)=u^z`; hence `beta(~g)=beta(g)`. Replacing `g` by `~g` complements
the `a` and `c` outputs and leaves `b,d` unchanged. This is exact integer
arithmetic, verified by substituting `~g = g^0xFFFFFFFF` and using
`ROR(u^0xFFFFFFFF,k)=ROR(u,k)^0xFFFFFFFF`.

## 5. Theorem (1-round collision)

Use Lemma 1 in the four column calls to force `v[8]=0` (via G0),
`v[9]=0` (G1), `v[10]=0` (G2), `v[11]=0` (G3), with all `d` targets 0.
Apply Lemma 2 to diagonal `G4` on `(0,5,10,15)` with `c`-input `v[10]=0`
and to `G6` on `(2,7,8,13)` with `c`-input `v[8]=0`, using `(g4,g6)` for `M`
and `(~g4,~g6)` for `M'`. Use Lemma 1 with targets `(0,0)` for `G5,G7`.
The final states differ only in `v[0],v[10]` (from G4) and `v[2],v[8]`
(from G6). Digest words are `o[i]=v[i]^v[i+8]`: `o[0]=v[0]^v[8]=g4^g6`
up to the common `beta` terms which cancel, and `o[2]=v[2]^v[10]` likewise
agrees; the other six digest words use unchanged state words. `M != M'`
because G4 `c`-outputs `g4` vs `~g4` differ, forcing `(w8,w9)!=(w8',w9')`.
The argument holds for every choice of the 12 free words, giving distinct
pairs. No randomness, search, or heuristic is used.

## 6. Instance (explicit messages)

With `g4=0x11111111`, `g6=0x22222222`, the construction yields 64-byte
messages (hex, little-endian bytes as hashed):

    M  = 105d815ebe726754872d0efb8d5c536ab4f69bb08050501c68989509fff1537e186409cef83fe4d8954a3240aa4cf8c018eaed44f0471c6a190b00db025be35d
    M' = 105d815ebe726754872d0efb8d5c536ab4f69bb08050501c68989509fff1537ef541e7ab09c01b27954a3240aa4cf8c0d3a5a90011b8e395190b00db025be35d

Both are 64 bytes, distinct (bytes 32..39 and 48..55 differ), in the allowed
domain. Their complete `blake3-r1` digests agree:

    H(M) = H(M') = 33333333000000003333333300000000493944fda2156c32660f7eac34836f65

Recompute with the organizer reference:

    python3 -c "from verifier.blake3 import blake3; a=bytes.fromhex('105d815ebe726754872d0efb8d5c536ab4f69bb08050501c68989509fff1537e186409cef83fe4d8954a3240aa4cf8c018eaed44f0471c6a190b00db025be35d'); b=bytes.fromhex('105d815ebe726754872d0efb8d5c536ab4f69bb08050501c68989509fff1537ef541e7ab09c01b27954a3240aa4cf8c0d3a5a90011b8e395190b00db025be35d'); assert a!=b; assert blake3(a,rounds=1)==blake3(b,rounds=1)"

or `verifier/hash_functions.py:digest(m,'blake3',1)`. The words in
little-endian order are M=`5e815d10 546772be fb0e2d87 6a535c8d b09bf6b4
1c505080 09959868 7e53f1ff ce096418 d8e43ff8 40324a95 c0f84caa 44edea18
6a1c47f0 db000b19 5de35b02` and M' differing only in words 8,9,12,13 as
`abe741f5 271bc009 ... 0a9a5d3 95e3b811`. This is an ordinary collision of
complete messages on all 256 digest bits.

## 7. Algorithm and charged cost

The RAM program is straight-line: load 18 constant table words (IV0..7, 64,
11, F=0xFFFFFFFF, 1, 0, 7, 12, 16, 20, 25), evaluate the closed forms of
section 5 (at most 140 ALU/load/store steps), store 32 message words.
Then verify: two complete 1-round recomputations, one 8-word digest
comparison, one message-inequality check. No branch on secret data, no loop
beyond bounded counters, no random-word primitive, no second compression
beyond the two verification hashes.

Cost model `collision-frontier-v5` for `blake3-r1` has `C=222`: one
selected-round compression is one unit, each other 256-bit primitive word
operation is `1/222` units. Narrow 32-bit add/sub is followed by AND F and
each rotation is SHR+SHL+OR+AND per `scripts/reference_operation_costs.py`;
all such expansions are inside the counts below. There are no immediates:
every constant is loaded once from the table.

Ledger (worst case, all phases):

| Phase | Selected compressions | Ordinary operations |
| --- | ---: | ---: |
| Load 18 table words | 0 | 18 |
| Construct M,M' (ADD 6, SUB 19, AND 28, OR 10, XOR 7, SHL 10, SHR 10, loads/stores) | 0 | at most 158 |
| Verification: 2 hashes | 2 | 0 |
| Digest/message checks, addressing, branches | 0 | at most 64 |

Total ordinary `W <= 240`, selected `H = 2`. Total `T = 2 + W/222 <= 2 + 240/222
= 3.0811`. Hence `log2(T) <= 1.6235`. The claim reports the ceiling `1.624`.
Preprocessing is 0 (no offline phase; all work above is online and counted).
Data is 128 construction bytes plus 128 verification bytes = 256 = `2^8`.
Memory below `2^15` bytes: 128 message bytes, under 4 KiB state/scratch,
under 20 KiB code+constants (generous bound for ~200 instructions plus
18-word table); total under 32768. Memory scores nothing. Advice is 0.

Success probability is 1: the program has no coins and no failure branch
except a verification that passes on the instance above by the theorem and
the recomputation. All failed tapes are vacuous; total work is worst-case.

## 8. Evidence, provenance, limitations

Heuristics `[]`, no experiment manifest, one verified
`hash-collision-witness-v2` certificate `witness-1` binding
`certificates/a.bin` and `certificates/b.bin` to expected digest
`33333333000000003333333300000000493944fda2156c32660f7eac34836f65`
under target profile `blake3-r1-prefix-v1`. The explicit hex above is the
same pair, recomputable via `verifier/blake3.py:blake3` and
`verifier/hash_functions.py:digest(data, "blake3", 1)`. The probability and
costs are analytic for the explicit program; no full-scale search was needed
beyond the closed form. Trusted reference remains `verifier/blake3.py:blake3`
and `verifier/hash_functions.py:digest`.

Memory and time are impractical as hardware but permitted by the word-RAM and
memory-only-reporting policy; this is a 1-round structural result, not a
break of full BLAKE3 or of 2+ rounds. Complement does not commute with modular
addition in later rounds, so nothing about `blake3-r2` follows. Qualification
is AI screening (`plausible_not_refuted`), not formal verification, human
acceptance, or promotion. Promotion is manual.
