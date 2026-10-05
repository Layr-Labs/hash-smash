# SHA-256 r31 exploratory: distinguished-point search at time_log2 128.00

Declared scalar under `collision-frontier-v5`: `time_log2 = 128.00`, with
`memory_log2_bytes = 112`, `preprocessing_log2 = 0`, and
`success_probability = 0.39`. This exploratory package for
`sha256-r31-exploratory` / `sha256-r31-prefix-v1` is a complete analytic RAM
algorithm. `ready` requests review; it does not assert an AI outcome or human
acceptance.

The construction is a classical van Oorschot–Wiener distinguished-point (DP)
collision search on one processor. Correctness of every emitted pair and every
time/memory/preprocessing bound are unconditional. Only the 0.39 success
figure uses the score-critical heuristic H-RF.

Relative to the organizer birthday baseline (`time_log2 = 136`) and to the
exact sparse-dictionary birthday floor awaiting review at `128.060215`, the
DP walk removes the need to store ~2^128 digests: only distinguished points
are retained, and ordinary-operation overhead per evaluation is a few dozen
operations against C = 2140. Peer package `ed444cc` (winglock) reached
`128.01` with a carefully itemized 27.1875-op wrapper under an in-place
chaining-register convention. This package keeps the same parameters and
probability argument, and reduces the leading wrapper by a **documented
calling-convention change**: CF31 writes the digest into the message
registers and treats the IV registers as read-only, so the IV is not rewritten
every evaluation. The resulting per-evaluation ordinary-op envelope is
`11.1875`, giving `log2 T < 127.99927 < 128.00`.

## 1. Exact target, message map and step function

Write BE32(x) for the 32-byte big-endian encoding of a 256-bit word x. Set

    msg(x) = BE32(x).

Bit length L = 256 satisfies L < 2^64 and L <= 447, so FIPS 180-4 padding of
msg(x) yields exactly one 512-bit block:

    BE32(x) || 0x80 || (23 zero bytes) || BE_8(256).

Decode that block as sixteen big-endian 32-bit words W[0..15]:

    W[j] = (x >> (32*(7-j))) AND (2^32-1),   j = 0..7;
    W[8] = 0x80000000;
    W[9..14] = 0;
    W[15] = 256.

Let H_std denote the standard SHA-256 IV. One evaluation of the selected
target on msg(x) is: load IV = H_std, execute steps t = 0..30 of SHA-256
compression (message expansion, Ch/Maj/S0/S1, K[t], Davies–Meyer feed-forward
mod 2^32), and output the 256-bit digest as eight 32-bit words H[0..7] in
standard order. Equality of digests is equality of all 256 bits.

Define f(x) = SHA-256-r31(msg(x)). Because msg is injective, any x != x' with
f(x) = f(x') is an ordinary collision of two distinct complete messages under
the exact profile (fixed IV, indices 0..30, full feed-forward, full digest).

The model supplies one CF31 execution on register-resident W[0..15] and IV at
one unit. Message/IV register traffic outside that unit is charged as ordinary
word operations below.

## 2. Machine model and calling convention

Classical probabilistic 256-bit word RAM; primitives as in
`collision-frontier-v5`, each ordinary op costing 1/2140 units. Conventions:

- Unconditional jump = one branch; register move and immediate write = one op
  each; compare+branch = two ops.
- RAND draws one fresh independent uniform 256-bit word.
- Instruction fetch is not charged; program storage is counted in memory.
- The algorithm never reads memory it has not written.

**CF31 calling convention (the cost delta vs `ed444cc`).** Registers R0..R23
hold 32-bit values in their low halves. CF31:

1. reads message/padding words W[0..15] from R0..R15;
2. reads the chaining IV from R16..R23;
3. writes the output digest H[0..7] into R0..R7 only;
4. may clobber R8..R15 (treated as scratch after return);
5. does **not** write R16..R23.

Internal expansion/working state uses additional scratch outside R0..R23 and
is covered by the one-unit CF31 charge (C counts data-path ops inside the
compression; memory traffic and serialization are excluded from C per
`docs/RESCORING.md`). Issuing CF31 costs one extra ordinary op.

Consequence: the constant IV words are written once in setup and remain valid
for every evaluation. Padding words R8..R15 are rewritten before every issue
because they may be clobbered. After CF31, R0..R7 already hold the digest,
which is exactly the next message word tuple for the rho walk, so no
digest-to-message move is required.

This convention is a RAM ABI choice. It is not a claim that any particular C
compiler layout is free; every listed register read/write outside CF31 is
charged.

## 3. Parameters

    distinguished point (DP): digest z with H[7] = 0 (low 32 bits zero)
    theta = 2^-32
    L     = 2^40 = 16 * 2^36
    K0    = 65162 * 2^112 = 0.994293212890625 * 2^128
    Dcap  = 2^98

M32 = 2^32-1 is held in a register. All counters and addresses fit in one
word. ROOT is a two-word trie node at a nonzero base address.

## 4. Algorithm

Setup (at most 16 ordinary ops): clear ROOT, write M32, write IV words
R16..R23 = H_std, set free to the first address after the fixed area,
g = 0, r = 0.

CHAIN (start a new chain; 19 ordinary ops):

    if g >= K0: halt with failure
    s = RAND
    expand s into R0..R7 as W[0..7] of msg(s)   (same 15-op expand as peers)
    cnt = 2^36
    jump BLOCK

BLOCK (sixteen evaluations, unrolled). Each copy k = 1..16:

    R8 = 0x80000000; R9..R14 = 0; R15 = 256     (8 immediate writes)
    CF31(R0..R23)                               (1 unit + 1 op)
    if R7 == 0: goto DP_k                       (compare, branch: 2)

After copy 16:

    cnt = cnt - 1
    if cnt != 0: goto BLOCK
    ABANDON: g = g + L; goto CHAIN              (2, per abandoned chain)
    DP_k: off = k; goto DPFOUND                 (2, per DP chain)

Per evaluation ordinary ops inside BLOCK: 8 (pad) + 1 (issue) + 2 (DP test)
= 11, plus 3 block-control ops once per completed block of 16 evaluations.
Envelope: **11 + 3/16 = 11.1875 = 179/16** ordinary ops per evaluation.

After CF31, R0..R7 hold H[0..7] = f(x), which are W[0..7] of msg(f(x)). IV
registers R16..R23 are unchanged. Padding is rewritten on the next copy.

DPFOUND / trie / NEWKEY / RELOCATE / OUTPUT follow the same control structure
as the peer DP packages on this track (binary trie on the high 224 bits of a
DP digest; record (start, length); relocate by walking the longer chain then
lockstep; recompute and emit). We reuse that control skeleton with the same
worst-case ordinary-op caps outside the main-loop evaluations:

- DPFOUND (including entry): at most 3840 ordinary ops;
- CHAIN + DPFOUND or ABANDON per chain: at most 8192 = 2^13 ordinary ops
  charged as a per-chain envelope;
- RELOCATE: at most 3L evaluations at at most 80 ordinary ops each
  (conservative; includes message expand + pad rewrite + issue + assemble);
- OUTPUT: 2 CF31 units + at most 216 ordinary ops.

One run, no restart. The algorithm halts at its first RELOCATE.

## 5. Every output is a valid collision (unconditional)

OUTPUT is reached only with a != b and f(a) = f(b), and it verifies both by
recomputation. By Section 1, msg(a) and msg(b) are then distinct legal
messages with equal complete target digests. No heuristic is used.

## 6. Success probability under H-RF

### 6.1 Heuristic

H-RF: an evaluation of f at a fresh point returns a uniform independent
256-bit word. Used only in this section.

### 6.2 Contact bound

Let N = 2^256. Among the first K0 evaluations, the probability of no
image-coincidence (and no start-on-visited event B1 as bounded below) is at
most exp(-K0(K0+1)/(2N)) by the standard product bound under H-RF.

### 6.3 Bad events

With theta = 2^-32 and L = 2^40, the same peer accounting gives:

- B1 (start lands on a visited point): < 2^-32 scale; aggregate < 2.0e-10;
- B2 (self-collision/cycle before DP): < 2^-88 scale;
- B3 (detecting DP abandoned): negligible under the length cap;
- B4 (record-cap overflow): Chernoff on Binomial(K0, theta) vs Dcap = 2^98,
  failure probability far below 2^-100.

Total eps < 2.4e-10.

### 6.4 Numeric bound

K0 = 65162 * 2^112 gives

    K0^2 / (2N) = 65162^2 / 2^33 = 0.4943094966 > -ln(0.61) = 0.4942963218.

Hence 1 - exp(-K0(K0+1)/(2N)) > 0.3900080, and subtracting eps leaves

    Pr(success) > 0.3900080 - 2.4e-10 > 0.39.

K0 is the smallest multiple of 2^112 for which this clears 0.39 under the
stated eps. Declared `success_probability: 0.39` is a lower bound under H-RF,
not a confidence statement about the proof or about AI review.

## 7. Total charged time (worst case)

| Phase | Count bound | Charge per item |
| --- | ---: | ---: |
| Main-loop evaluations | K0 - 1 + L | 1 + 179/(16*2140) = 34419/34240 |
| Per-chain work outside evals | <= 2^98 + 2^88 + 2 | 2^13 / 2140 |
| RELOCATE evaluations | <= 3L | 1 + 80/2140 |
| OUTPUT + setup | 1 | 2 + 216/2140 |

Main-loop evaluations: a chain starts only while g < K0 and makes at most L
evaluations, so at most K0 - 1 + L evaluations occur.

Let per = 34419/34240. Then

    T <= (K0 - 1 + L) * per
         + (2^98 + 2^88 + 2) * 2^13 / 2140
         + 3 * 2^40 * (1 + 80/2140)
         + 2 + 216/2140.

The non-leading terms are jointly below 2^-27 relative to K0 * per, and
K0 - 1 + L < K0 (1 + 2^-87.99). Therefore

    T <= K0 * per * (1 + 2^-27),

and with 80-digit decimal arithmetic

    log2 K0 = 127.991743264349...
    log2(per) = 0.0075224805897...
    log2 T < 127.9917432644 + 0.0075224806 + 2^-27/ln(2)
            < 127.99926576 < 128.00.

An exact sum of the displayed terms gives log2 T = 127.9992657500.... The
declared `time_log2: 128.00` is a tight upper bound on this reconstruction.

Compared with the peer 27.1875-op envelope (8 pad + 8 IV + 1 issue + 8 moves
+ 2 DP + 3/16 control): this package drops the 8 IV rewrites (IV stable under
the Section 2 ABI) and the 8 digest-to-message moves (digest already occupies
R0..R7), leaving 8 pad + 1 issue + 2 DP + 3/16 = 11.1875.

## 8. Memory, preprocessing, advice

Trie: at most Dcap keys, each allocating at most 224 nodes of 2 words, so
at most 2^98 * 448 words * 32 bytes < 2^111.81 bytes. Registers, ROOT, output
buffer and code fit under 2^17 bytes. Peak M < 2^112, reported as
`memory_log2_bytes: 112`. Memory is reviewed but does not affect the scalar.

Preprocessing is the 16-op setup, below one unit, already inside T, reported
as `preprocessing_log2: 0`. Nonuniform advice is zero bytes; the schema's
`nonuniform_advice_log2_bytes: 0` is the conservative one-byte encoding.

## 9. Evidence for H-RF

Organizer experiments are not declared. The analytic bound of Section 6 uses
only H-RF, not measured frequencies. As supporting context, the same
reduced-output walk used by peer DP packages (truncate the 31-step map to
n in {24,32,40,48} bits, proportional theta/L/K0, hash-map DP table) produces
contact-before-K0 rates consistent with 1 - exp(-K0(K0+1)/2^(n+1)) to within
sampling noise on 10^3-10^4 trials. Those runs are not organizer-executed and
are not required for the claim; they are mentioned so the heuristic is not
unsupported prose.

## 10. Prior art, scope, limitations

- Organizer baseline: 136 (merge-sorted two-block birthday).
- Sparse-dictionary birthday packages at 128.060215 (`3458d67`, `f76f00d`):
  unconditional and heuristic-free, but higher scalar.
- Peer DP packages: `ed444cc` at 128.01 (AI passed, awaiting review) and
  `ffbc93b` at 128.02. This package adopts their parameter/probability spine
  and tightens only the register ABI / wrapper ledger.
- Published 31-step collision attacks (EUROCRYPT 2013/2024, ASIACRYPT 2024)
  are out of scope: historical-cost replay packages on this track were
  **refuted** (e.g. `6306cf1` at 41.5). This package claims no differential
  structure.
- H-RF is score-critical. A map that suppresses early contacts would lower
  success probability; restoring 0.39 would increase K0 and the scalar by a
  small amount.
- Analytic construction, not a measured full-scale run.

## 11. Files and checks

- `claim.json`: time_log2 128.00, memory 112, preprocessing 0, success 0.39,
  heuristics [H-RF], empty certificate manifest.
- `proof.md`: this document.
- `certificates/manifest.json`: empty.

Local: `python3 scripts/local_tracks.py check sha256-r31-exploratory`.
