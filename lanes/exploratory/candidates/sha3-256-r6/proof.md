# sha3-256-r6: bitsliced grouped birthday search on 128-byte linear-structure prefixes, time_log2 = 124.07261

## 0. Summary and credit

A generic birthday search over full 256-bit digests. No cryptanalytic
weakness of SHA3 is claimed. This package (our internal label bs11)
revises our df0136bc (bs9, 124.096), which revised our 7e40f784 (bs7,
124.263). It keeps df0136bc's message family, key, table, candidate path,
H1 (restated for this N; Section 7), declared experiments, K = 10 and Gray order (the experiment script
is byte-identical, so bs7's organizer
runs and our pre-registered runs apply as they are) and includes the
text revisions of bs10, an unsubmitted revision of df0136bc (complete run
list, 2^100-unit development charge, disclosures). What is new is a
cheaper counted program, a batch count fixed by the success bound, and a
five-decimal claim; see "Changes from df0136bc" at the end of this
section:

- **memo2: complement classes and stored chi terms (Lemma 14').** bs9's
  block memo reloads a round-3 chi output when its three input words have
  the same view expressions as at an earlier position of the block. memo2
  also (i) reloads it when the expressions differ only by the all-ones
  term of input X, complementing it (chi output X is a XOR (NOT b AND c),
  affine in a), and (ii) stores the nonlinear term NOT b AND c, keyed by
  the expressions of inputs X+1 and X+2, so that a later first occurrence
  with the same pair computes the output as a XOR the stored term. Fewer
  outputs are computed in full, so fewer view words must be maintained
  (358,840 instead of df0136bc's 626,300): this removes a large part
  of the high steps' view work and part of the low steps' round 3.
- **Block-unrolled control (Section 5.2).** The 2^K - 1 low steps of a
  block always run the same bodies in the same order, so each block
  pattern's low bodies are laid out as one straight-line chain. Only the
  high step of a block dispatches (a chain of bit tests on the block
  counter); a low step runs no control operation.
- **Unchanged view count and order (Lemmas 12-13).** K = 10 (1,023 views)
  and ORDER are df0136bc's; `ordergen.py` is byte-identical.
- **Exact batch count.** Every (leaf, view state) pair that occurs has its
  own straight-line body (2,069 bodies, all compiled and run
  by the self-test). The time bound charges the **exact** number of
  operations of one batch, T = 117,398,575,636,479, i.e. T / 2^32 =
  **27,333.986** operations per z-step of 256 messages (df0136bc:
  27,743.222). This is a count of a deterministic schedule, not an
  estimate.
- **Batch count from the success bound (Sections 7-8).** The run uses
  NB = 307,990,341,830,783,024,002,353,940 batches, the smallest
  number whose success bound under H1 (Section 7) is at least 0.3905; df0136bc used 255 * 2^80
  batches (bound 0.39106). The rule is fixed and computed by `cert.py`
  (no run informs it). The claimed success probability stays 0.39.
- **Five-decimal claim.** The integer certificate is evaluated at 10^-5:
  the claim is the smallest c / 10^5 with A^(10^5) < 2^c K'^(10^5)
  (rounded up). The five-decimal format follows GordoAR's 5dac3f95 and
  dcdd90ec (the latter re-claims our df0136bc at 124.09527).
- **Shipped and checked.** The counted program is in Appendix A. The
  self-test regenerates all 2,069 bodies, prints T, checks the
  control layout, runs every body once on the counted 64-register
  simulator from a random state against `verifier/keccak.py`
  (529,664 keys), checks the maintained A2, O2P and view words
  against a rebuild, runs 3 x 40 consecutive steps across block
  boundaries (one run from the first step of a block with no memo
  prefill), the candidate and halting paths and the counted setup
  programs. A battery (Section 10.1) adds six seeds, a run of 2,088
  consecutive steps through whole blocks of both patterns and their
  boundaries, static audits and mutations of the new memo stores,
  complement flags and term polarities. Every constant the count depends
  on is the output of shipped deterministic code, except bs7's start
  planes (Section 10.1); all target-specific search and development is
  charged (Section 8).

| quantity | value |
| --- | --- |
| messages N | NB * 2^40 = 2^127.993016 (NB = 307,990,341,830,783,024,002,353,940 batches x 256 groups x 2^32 values of z) |
| ops per batch T (2^32 z-steps x 256 messages), exact | 117,398,575,636,479 (every executed primitive) |
| ops per z-step, T / 2^32 | 27,333.986 (bodies: t = 0 31,491; low leaves 26,415..30,882; high leaves 301,235..376,557) |
| ops per message charged | 106.7734 (T / 2^40) + batch setup < 2^-17 |
| candidate verifications | at most VCAP = floor(N^2/2^141) + floor(N^2/2^148) + 2^91 + 2^61, each 3 units + at most 150 ops |
| total T_run | 2^124.072606093 (Section 8; exact integer certificate) |
| claimed time_log2 | **124.07261** |
| success probability | >= 0.3905 under H1 (model value 0.3905000); claimed 0.39 |
| memory | < 2^145.01 bytes; claimed 146 |

**Credit.**

- **Co-authors.**
  - **5kyguy** (6e715d9a, 124.270): the 128-byte family with z in lanes 4
    and 14 and its constraints (L5 = L15, L8 = 0, L12), which this package
    adopts unchanged (Sections 2-3); the per-branch-site candidate copies
    ending in a charged direct jump back (Section 5.4); the
    program-generation allowance (2^50 in 6e715d9a; Section 8 charges
    2^100 units); and the example of shipping
    the counted generator and simulator with the package. Their polarity,
    allocation and schedule are not used: ours are generated by our
    compiler. Earlier, 78676cf6 independently and concurrently specialised
    delta swaps for zero rows; nothing from it is used.
  - **Th0rgal** (4867f093): the linear-structure prefix on this track,
    which makes round 1 linear in z and round 2 incrementally AND-free.
    Earlier (76ccfa1c): our table builds on T2, their sparse set at address
    0, and our compiler subsumes T3.
  - **jaazinn** (0a5b7ae8): grouped partial evaluation, the Briggs-Torczon
    sparse set, the failure analysis with H1 and the scaled-experiment
    design.
  - **may93182** (11c46f4d): the 256-way bit-plane Keccak and the
    delta-swap transpose.
- **Credited.**
  - **GordoAR** (5dac3f95, dcdd90ec): the five-decimal claim (the integer
    certificate evaluated at 10^-5, Section 8); earlier (e715ab73,
    df2619d4) the integer-certificate format. dcdd90ec re-claims our
    df0136bc at 124.09527; nothing else from their packages is used.
  - Jian Guo, Meicheng Liu and Ling Song, "Linear Structures: Applications
    to Cryptanalysis of Round-Reduced Keccak", ASIACRYPT 2016: linear
    structures.
  - tekkac (b001199a): lane-complement chi on this track, after the Keccak
    team.
  - ercumentyildirim (c7fa1a56; r5: 4c969300): the last-round early abort,
    which the kept planes extend.
  - zeeshan8281 (cbf7998d): the 255/256 message budget (df0136bc's batch
    count; this package derives its batch count from the success bound).
  - zeeshan8281 and tekkac (f58275ef): exact per-message charging.
  - mitchuski (02d6a703): the every-load-and-store-charged reading.
- **Not used.** Nothing from newjordan's b54bb98c is used.
- **Ours.** Read-only flips with storage polarity, patches merged into
  round 3, Lemmas 7 and 9-14' (including the materialised Gray views, the
  block memo, memo2, the Gray order, the block-unrolled control and the
  exact batch count), the start-plane search, the 16-row transpose
  layout, pair ids, the kept planes with verify and continue, the
  tagged-id table, the counted program, the experiment protocol, the batch
  count rule and any errors.

None of them has reviewed this package.

**Changes from df0136bc (bs9).**
- *Program (new T).* memo2 (Lemma 14'); block-unrolled control (Section
  5.2); the batch setup stores only the maintained view words (Section
  5.1). K = 10, ORDER, the start planes, the family, the key, the table
  and the candidate path are unchanged. T / 2^32 falls from 27,743.222 to
  27,333.986.
- *Batch count.* NB = 307,990,341,830,783,024,002,353,940 (Section 7), fixed by the success bound
  0.3905, instead of 255 * 2^80; VCAP and H1 are restated for this N.
- *Claim format.* Five decimals, rounded up (GordoAR's format).
- *From bs10 (unsubmitted text revision of df0136bc).* Section 10.3
  lists every run of the experiment script up to bs10's run-list freeze
  (2026-10-07T21:46Z), including one public-seed replay made after
  df0136bc's freeze and a later `--local` review run; Lemma 12 and Section
  10.1 disclose the cost-model runs behind K and the generator seed;
  Section 8 charges all target-specific search and development with a
  2^100-unit term instead of 2^50; smaller corrections (verification work
  156 operations per z-step, seed key counts, self-test memory guidance,
  the Appendix B nonce labels). This package also corrects the `ir.py`
  header comment (cmpeq compares two registers), which bs10 corrected only
  in its text.
- *Development of this revision (development choices, all charged by the
  2^100-unit term of Section 8; none reads a digest).* Prototype builds
  compared memo2 store thresholds 0, 1 and 2 (1 kept) and a variant that
  complements on every reduced-class reload (rejected: it cost 141
  operations per low body more), and sampled K = 10, 11 and 12 with memo2
  (exact static counts of 30 to 240 low bodies and the first high
  bodies); for K = 11 and 12 they also scored extensions of ORDER with the
  shipped cost model, and for K = 12 a partial build was made (Section
  10.1). Other prototype static counts compared kept-plane variants (any
  one unkept plane added, any one kept plane removed; not adopted: KEEP is
  bs7's, fixed in the frozen script), a grouped-id candidate path with a
  units cap and a last-writer-first candidate order (not adopted), start
  planes (2, 39, 34) (not adopted), and ledgers that chose the 0.0005
  allowance (the K = 12 development files used 0.3901; the target was raised to 0.3905 before the K = 10 build; no trial informed either) and the five-decimal format. Prototypes import the experiment
  script's geometry as a module, as `ref.py` does; an import runs no
  trial. All prototype files and outputs are hashed in Section 10.1. We keep K = 10 and ORDER: the projections favour K = 12 (about
  -0.020 in time_log2) but its self-test would compile and run 8,211
  bodies, four times this one's, and we prefer a self-test a reviewer can
  rerun in well under an hour. Sensitivity of the development choices
  (prototype projections, not exact counts): store thresholds 2 and 0
  would cost about +0.0010 and +0.0060 in time_log2 at K = 10.

## 1. Target, machine and charging conventions

- **Target.** `sha3-256-r6-prefix-v1`: the complete SHA3-256 sponge (rate
  1088, capacity 512, suffix 0x06, pad10*1, zero IV) with Keccak rounds
  0..5 and all 256 output bits, as in `verifier/keccak.py:sha3_256(msg, 6)`.
  Messages are exactly 128 bytes, so one 136-byte block. Lane k (k < 16) is
  bytes 8k..8k+7, read little-endian. Lane 16 = PAD16 = 0x8000000000000006
  (the 0x06 suffix and the final pad bit) and lanes 17..24 are 0. Lane
  index L = x + 5y. Rounds are numbered 1..6.
- **Digest and key.** The digest is lanes 0..3 after round 6, and K* =
  int.from_bytes(digest, "little"). The program stores the **key**
  K = key_of_digest(K*):
  - digest bit (x, b), with x < 4 and b in KEEP, moves to key bit
    ROWOF(x, b) = 4k + x, where b = KEEP[k];
  - the result is XORed with a public constant KEYMASK;
  - key bits 140..255 are 0.

  K is a fixed function of 140 digest bits, so **equal keys are only a
  candidate**.
- **Cost model.** `collision-frontier-v5`, C = 1626. One permutation costs 1
  unit. Any other 256-bit word primitive costs 1/1626.
- **Machine.** A 256-bit word RAM with **64 registers**. This is our stated
  assumption, and the program uses all 64. An operation on register
  operands is one primitive, not a memory access. 64 registers of 256 bits
  are 2 KiB, a 32-entry 512-bit SIMD register file. This reading does not
  cover a register bank of thousands of words; we claim no bound under such
  a reading, nor under a memory-to-memory reading.
- **Charging (claimed).** Every executed primitive of the v5 list costs 1:
  - every load and store, direct or register-addressed;
  - XOR, AND, OR, NOT, shift or rotation, add, compare, conditional branch,
    immediate move and random word.

  A constant address or an immediate is a field of the instruction that
  executes. A candidate verification evaluates three messages with the
  reference six-round function, 1 unit each (Section 5.4). Section 9
  prices address additions, immediates and shift amounts separately.

## 2. Messages, groups, batches and processing order

This is 5kyguy's 128-byte family (6e715d9a). For group g the algorithm
draws three fresh uniform 256-bit words, i.e. 768 bits, and splits them into
the twelve free lanes L0, L1, L2, L3, L4, L6, L7, L9, L10, L11, L13, L14.
With

    C4 = L4 XOR L9 XOR L14,   C1 = L1 XOR L6 XOR L11 XOR PAD16,

the **structured prefix** P_g sets

    L5 = L15 = C4 XOR rotl64(C1, 1),   L8 = 0,
    L12 = NOT rotl64(C4, 1) XOR L2 XOR L7.

The map from the 768 free bits to P_g is injective, so P_g is uniform over a
set S of 2^768 prefixes. P_g is stored. For z in {0,1}^32:

    m(g, z) = P_g with LE32(z) XORed into bytes 32..35 and into bytes 112..115.

So z is XORed into the low 32 bits of lane 4 (x=4, y=0) and of lane 14
(x=4, y=2). Both are free lanes and the same value enters both, so C4, C1
and the dependent lanes are unchanged: for every z the map P -> m(P, z) is
a permutation of S.

- **Batches.** Write g = 256*beta + p, with batch beta < NB and slot
  p < 256 (NB = 307,990,341,830,783,024,002,353,940 < 2^88 batches,
  Section 7). Batch beta runs t = 0, 1, ..., 2^32 - 1 with
  z(t) = zperm(gray(t)), gray(t) = t XOR (t >> 1), where zperm moves bit j
  of its argument to bit ORDER[j] (Lemma 12; ORDER is the fixed permutation
  of Appendix A, `selftest.py`). t -> z(t) is a bijection onto {0,1}^32.
- **Processing order.** At each t the batch evaluates the 256 messages
  m(256*beta + p, z(t)). It offers them to the table in the order
  q = 0..255, slot p = decode_slot(q) = 16*(q mod 16) + floor(q/16).
- **Pair id.** The messages with processing indices q = 2k and q = 2k + 1
  of batch beta at step t, k < 128, form a pair with id
  n = beta*2^39 + t*2^7 + k, which is also the count of pairs processed
  before it. Every message is evaluated once.

**Bit mapping.** Word P(L, b) holds, in bit position p, bit b of lane L of
m(256*beta + p, z). Padding planes are constants: P(16,1) = P(16,2) =
P(16,63) = all-ones, P(8, b) = 0, and all planes of lanes 17..24 are 0.

## 3. Dependency analysis (exact)

Every step map except chi is GF(2)-linear. A2 denotes the state after round
1 and the theta of round 2. Theta: C[x] = XOR_y L(x+5y),
D[x] = C[x-1] XOR rotl(C[x+1], 1). Chi: out[X] = b[X] XOR (NOT b[X+1] AND
b[X+2]).

**Lemma 1 (round-1 theta is invariant; two constant lanes).** Lanes 4 and 14
lie in column 4 and carry the same z, so every column parity, and so every
D word of round 1, is independent of z. Moreover:
- D0 = C4 XOR rotl(C1, 1), where the column-1 parity C1 = L1 XOR L6 XOR
  L11 XOR PAD16 includes lane 16 (lane 21 is 0). Since L5 = L15 =
  C4 XOR rotl(C1, 1) = D0, lanes 5 and 15 are **0 after theta**.
- C2 = L2 XOR L7 XOR L12 = NOT rotl(C4, 1) (lanes 17 and 22 are 0), so
  D3 = C2 XOR rotl(C4, 1) = all-ones. Lane 8 (L8 = 0) and lane 23 (0) are
  therefore **all-ones after theta**.

**Lemma 2 (round 1 is linear in z; linear structure).** Rho/pi sends lane 4
(rotation 27) to row Y = 3, X = 0, plane j+27, and lane 14 (rotation 39) to
row Y = 4, X = 2, plane j+39, for z-bit j. A varying chi input b[X] enters
out[X-1] through NOT b[X] AND b[X+1] and out[X-2] through NOT b[X-1] AND
b[X]. Both terms are constant when b[X+1] = 0 and b[X-1] = all-ones on the
varying plane:
- Row 3, X = 0: b[1] comes from lane 5 (rotation 36), 0 by Lemma 1, and
  b[4] from lane 23 (rotation 56), all-ones by Lemma 1.
- Row 4, X = 2: b[3] comes from lane 15 (rotation 41), 0, and b[1] from
  lane 8 (rotation 55), all-ones.

So z changes exactly two round-1 outputs, bit j+27 of lane 15 and bit j+39
of lane 22, each by z_j itself. Hence A2(z) = A2(0) XOR sum_j z_j E_j
exactly, where E_j is a fixed vector that does not depend on the group.

**Lemma 3 (22-word support, all-ones).** Round-2 theta spreads the two
flipped bits over 4 D columns. In bitsliced form z_j is the same in all 256
groups, so E_j is all-ones (W) on exactly these 22 words and 0 elsewhere
(planes mod 64):
- bit j+27 of lane 15 and bit j+39 of lane 22 (the chi outputs);
- D1 at plane j+27: lanes 1, 6, 11, 16, 21;
- D4 at plane j+28: lanes 4, 9, 14, 19, 24;
- D3 at plane j+39: lanes 3, 8, 13, 18, 23;
- D1 at plane j+40: lanes 1, 6, 11, 16, 21.

These sets are disjoint, so there are 22 words. With the Gray order of
Lemma 12, A2(z(t)) = A2(z(t-1)) XOR E_{ORDER[ctz(t)]}. The counted simulator, the self-test of
Appendix A and every organizer trial check this support against a
from-scratch evaluation (Section 10).

## 4. Bitsliced Keccak, encodings, transpose and compiler (exact)

**Lemma 4 (bitsliced round).** On planes the round is bitwise:
- theta: C[x][b] = XOR_y P(x+5y, b), D[x][b] = C[x-1][b] XOR C[x+1][b-1],
  and A'(L, b) = P(L, b) XOR D[x][b];
- rho/pi: B(X, Y, b) = A'(L, b - RHO[L]), with (x, y) = pisrc(X, Y);
- chi and iota: as in the scalar round.

Bit position p therefore runs the scalar round on message p. A lane
rotation in a round only changes which address is read. The only executed
rotations are 256-bit word rotations in the transpose (Lemma 9).

**Lemma 5 (delta swap).** For d in {1, ..., 128} let M_d have bit c set iff
c AND d = 0. A swap of rows a = R[i] and b = R[i+d] (i AND d = 0) exchanges
entries (i, c+d) and (i+d, c) for c AND d = 0. Stage d applies it to all 128
such row pairs and swaps bit log2(d) of the row index with the same bit of
the column index. The 8 stages act on different index bits, so they
commute. All 8, in any order, transpose the 256 x 256 matrix.

**Lemma 6 (AND-free incremental round 2).**
- **What is maintained.** O2P is the round-2 output (chi, iota) with
  round-3 theta applied, in the encoding Q3 of Lemma 8. (Here A2 and O2P
  are kept at the base point of Lemma 13, and only steps with Gray bit
  j >= K apply this lemma, to the base and to every maintained view.)
- **Chi difference.** For a row with old inputs a and input change c, the
  exact output difference is

      dout[k] = c_k ^ c_{k+2} ^ a_{k+1} c_{k+2} ^ c_{k+1} a_{k+2} ^ c_{k+1} c_{k+2}.

  By Lemma 3 every c is 0 or W, so every product is either 0, W or a single
  A2 word. Each dout is an XOR of at most two A2 words and possibly W, with
  no AND. The 22 flipped words lie in 22 distinct round-2 chi rows.
- **Theta and the patch.** dC[x][b] = XOR_Y dout(x, Y, b), dD[x][b] =
  dC[x-1][b] XOR dC[x+1][b-1], and O2P(x+5Y, b) ^= dout(x, Y, b) XOR
  dD[x][b]. Symbolically, for each z-bit j, 499 O2P words get a fixed patch
  expression: an XOR of at most 4 terms, each an A2 word (44 distinct
  words per leaf) or W. 128 of them are W alone. A term that is itself
  flipped by this step is read after its flip, with W toggled.
- **Read-only flips.** Only the 975 A2 words that some leaf's expression
  reads are maintained. Leaf j flips the words of its support that lie in
  this set (3-10 words; load, NOT, store). Other A2 words are never read.
- **Storage polarity.** A2 word i is stored as A2[i] XOR pi_i W, for a fixed
  set pi of 359 words chosen by a deterministic local search to minimise
  the complemented expressions. Each stored term toggles W in its
  expression. The value is unchanged.
- **Merged into round 3.** Round 3 loads each patched O2P word once,
  XORs the expression, stores it back and uses the new value directly.
  When the expression is W alone, new = NOT old, so both polarities are in
  registers for the chi gate plans of Lemma 8. Distinct non-trivial
  expressions are formed once and reused (a small scratch cache).
- **Exactness.** Theta is linear and every encoding is an XOR with a
  constant, so the patched O2P equals the encoded, theta'd round-2 output of
  the new A2.
- **Cost.** In bs7 1,737..1,764 operations per leaf. Here only the high
  steps (ctz(t) >= K) do this work, for the base and every maintained
  view (Lemma 13; Section 5.2 ledger).

**Lemma 7 (theta at the store, rotating start plane).** A round processes
planes b = s, s+1, ..., s+63 (mod 64) for a fixed start plane s.
- Plane b's 25 chi outputs are in registers, so its parities C'[x][b] are
  complete before any store.
- For b != s, D'[x][b] = C'[x-1][b] XOR C'[x+1][b-1] is available, because
  plane b-1 was processed just before. Each output word is stored with D'
  already added.
- Plane s is stored raw. After plane s+63, the 5 fix words fix[x] =
  D'[x][s] = C'[x-1][s] XOR C'[x+1][s-1] are known.
- The next round XORs fix[x] into each loaded word whose source plane is s.

The stored state plus the fix is exactly the theta'd state, for every
choice of s. The start planes of rounds 3, 4, 5 are **(10, 61, 34)**. They
were chosen for this family by a coordinate search: for each round, all 64
values of its start plane were compiled for all 32 leaves with the other
two fixed, and the value with the smallest worst leaf was kept (two passes;
bs6's (2, 39, 34) gives 31,189 in bs7's program). The search changes only the program,
never a computed value. This package keeps bs7's planes; they were not
searched again for the new program.

**Lemma 8 (lane-complement encoding; as in bs4).**
- Each stored lane L has a compile-time polarity pi_L: the stored word is
  the true word XOR pi_L * (all-ones).
- Per chi row the program uses the cheapest exact gate plan for the given
  input and output polarities: NOT b AND c equals s_b AND s_c, or NOT(s_b OR
  s_c), with at most one shared complemented copy and the iota bit folded
  in. The plan comes from an exhaustive search over the 32 complemented-copy
  sets. Where a complemented input is already in a register (Lemma 6), it
  costs nothing.
- The patterns are P34 (output of rounds 2, 3, 4) and P5 (output of round
  5). Rounds 3-5 read Q3 = fpol(P34), and the last round reads fpol(P5).
- Every chi row of rounds 3-5 costs at most 1 NOT. The last round takes,
  per plane, the digest polarities that need no NOT; moved to key rows,
  these fixed bits form KEYMASK (33 of the 140 bits set).

**Lemma 9 (kept planes, key rows and the rotating-frame transpose; bs4's
swaps in a 16-row layout).**

    KEEP = (0, 1, 2, 3, 4, 9, 10, 11, 16, 17, 18, 22, 23, 24, 25, 29, 30, 31,
            32, 37, 38, 39, 40, 44, 45, 46, 47, 51, 52, 53, 54, 58, 59, 60, 61)

- **Key rows.** Plane KEEP[k] gets slot k, and digest bit (x, b) becomes key
  row 4k + x. Rows 0..139 hold the kept bits and rows 140..255 are
  constant zero.
- **Blocks.** Block g holds rows 16g..16g+15 (4 kept planes). Blocks 0-7
  are full, block 8 holds slots 32-34, and blocks 9-15 are empty.
- **Frames.** Row r is held in a **frame** OFF[r]: physical bit q holds
  logical bit (q + OFF[r]) mod 256. A stage-d swap of rows a = R[i] and
  b = R[i+d] keeps the row of even index parity (popcount) in frame 0 and
  moves the other.
  - If b stays in frame 0, then u = rot(a, OFF[a] - d) puts logical bit c+d
    of a at physical position c. Then t = (u XOR b) AND M_d; b ^= t;
    a = u XOR t; OFF[a] = d. These are 5 operations, and they exchange
    exactly the entries of Lemma 5.
  - The case where a stays in frame 0 is symmetric, with NOT M_d and
    OFF[b] = -d.
- **Zero rows.** A statically zero row needs no rotation and is substituted
  into the formulas: zero mover 2 operations, zero stayer 3, both zero
  nothing. The zero pattern is known at compile time.
- **Phase 1.** As soon as a block's 4 kept planes exist, the last round
  computes that block's 16 rows in registers and applies stages 1, 2, 4, 8
  in the cheapest static order: 1,410 operations in all.
- **Phase 2.** For each gi = 0..15 the program takes the 16 rows
  16i + gi, loads rows i <= 8 only, and applies stages 16, 32, 64, 128:
  1,880 in all.
- **Frame fix.** One rotation per row left outside frame 0, 128 in all.

The transpose costs 3,418 ALU operations (1,410 + 1,880 + 128). Its memory
traffic is counted in Section 5.2 (96 stores and 96 loads of ROWS between
the phases, and 20 loads of the delta-swap masks). Last round + phase 1 =
1,896 operations (1,408 gates, 110 loads, 96 stores, 282 rotations);
phase 2 + frame fix + the 1,408-op table = 3,524. By Lemma 5, row 16i + gi
is then the key of slot 16i + gi = decode_slot(16gi + i).

**Lemma 10 (dependency cone with start planes).** The last round on plane b
reads the 5 diagonal lanes at source plane (b - RHO[L]) mod 64. Round 5
must therefore store only these 175 words. None lies on round 5's start
plane 34, so no round-5 fix word is needed. For a round with start plane s
whose input lacks D on plane s_in, needed outputs propagate backwards:
- a needed stored word (L, b) with b != s needs its chi output, C[x-1][b]
  and C[x+1][b-1];
- a needed fix column x needs C[x-1][s] and C[x+1][s-1];
- a parity needs its 5 chi outputs;
- a chi output needs its 3 row inputs, plus the fix wherever the source
  plane is s_in.

Round 5 computes 1,161 chi outputs and 229 parities and reads 1,363 words
with all 5 fix columns. Round 4 needs all 320 parities and reads all 1,600
words. Every computed word is given by the same formula from the same
inputs as in the full round, and no omitted word is ever read.

**Lemma 11 (straight-line compiler).** The code of one body (one leaf and
view state, Section 5.2) is a single straight line, compiled in four steps:
1. It is put in SSA form.
2. Loads are store-to-load forwarded. A direct load whose word was written
   or loaded earlier in the block takes the value from the register that
   still holds it, chosen by an exact max-weight selection under the
   62-register budget. All addresses are instruction constants, so aliasing
   is decided exactly. A store to a scratch word of the step is dropped when
   no later load reads it. Scratch words are never read outside the step.
3. Registers are allocated by interval colouring. This is exact for
   straight-line code: the register count is the maximum number of
   simultaneously live values.
4. The result runs on the counted simulator.

No step changes a computed value. Every leaf uses at most 62 registers,
plus the persistent s and c, so 64 in all. The compiler is `ir.py` of
Appendix A.

**Lemma 12 (Gray order).** ORDER is a permutation of {0, ..., 31} and
zperm(x) = sum over the set bits j of x of 2^ORDER[j]. Since gray and zperm
are bijections of {0,1}^32, a batch evaluates every z exactly once, and
z(t) XOR z(t-1) = 2^ORDER[ctz(t)]. So step t flips the support
E_{ORDER[ctz t]} of Lemma 3. ORDER = [25, 8, 21, 10, 28, 15, 30, 17, 4, 12, 19, 27, 6, 26, 1, 14, 13, 24, 7, 18, 3, 31, 9, 5, 20, 11, 16, 22, 23, 2, 0, 29].
It is the output of `ordergen.py` (Appendix A):
`python3 ordergen.py 10 12 600` prints it (about 30 minutes, one
process). We made this call as `ordergen.search(10, 12, 600)` under
Python 3.9.6, through a logging wrapper whose callback only records each
proposal and does not touch the random generator; the lowest-cost order
visited is at proposal 68 of 600, and a reviewer's run of the shipped
file with 70 proposals printed the same ORDER. The generator anneals
which z-bits are the K low Gray bits, and in which order, under a static
cost model of the work of Lemma 13 and of a row-level version of Lemma 14
(`random.Random(12)`, 600 proposals, the lowest-cost order visited), then
orders the other bits by increasing overlap with the maintained views. It
reads only the static patch geometry, never a digest. Any permutation
gives a correct program with the same message set; ORDER changes only T,
which the self-test counts exactly.

*How K and the seed were chosen (cost only).* Before this call we ran
earlier versions of the same static cost model (same objective, different
search code) for K = 3..11: `comb.py` with seeds 1-5, and a pruned variant
with seeds 11 and 12 for K = 9..11. At K = 10 the pruned variant gave a
lower model cost with seed 12 than with seed 11, so seed 12 was used. An
unsubmitted intermediate build used the order of that earlier K = 10, seed
12 run, whose proposal count we had not recorded; it is replaced by this
reproducible one and is not used. One attempt of the call above with an
earlier, memory-heavier version of `ordergen.py` was stopped after 67
proposals. K = 10 itself was fixed by the exact counts T of builds with K
= 3, 9 and 10 (Section 10.1). None of these runs reads a digest; all are
charged in Section 8.

*This revision.* bs11 keeps K = 10 and this ORDER; `ordergen.py` is
byte-identical to df0136bc's. Its development (memo2, Lemma 14') also
compiled sample bodies at K = 10, 11 and 12 and scored extensions of
ORDER by one and two low bits with the same cost model (a development
version of `ordergen.py` with an `extend` function, not shipped because
its output is not used; the run is listed in Section 10.1). These choices
read no digest and are charged in Section 8.

**Lemma 13 (materialised Gray views; exact).** Fix K = 10. Write gray(t)
= h + s with s = gray(t) mod 2^K (the **view state**) and h the high part;
the **base point** of t is zperm(h). For a state s let O2P_s(h) be O2P at
the point zperm(h + s) (O2P_0 is the base).
- (i) *A fixed difference.* For every s there are a fixed set VS[s] of O2P
  words and, for each w in VS[s], a fixed set VD[s][w] of A2 word indices
  and possibly W, such that for every h and every group, O2P_s(h)[w] =
  O2P_0(h)[w] XOR (XOR of A2(zperm(h)) over VD[s][w]), and
  O2P_s(h)[w] = O2P_0(h)[w] for w not in VS[s]. Proof: by Lemmas 3 and 6,
  flipping the low Gray bit i at any point x XORs into O2P the fixed patch
  expression of z-bit ORDER[i] evaluated with A2(x); A2(x) differs from
  the base A2 by W exactly on the supports of the low bits set in x
  (Lemma 3), which toggles W once per expression term in such a support.
  Raising the bits of s one at a time from 0 composes these expressions
  (symbolically, as sets of terms); storage polarity toggles W once per
  stored term. VS[s] is the set of words with a non-empty composition.
  The sizes are 499..1,533 words over the 1,023 states.
- (ii) *Storage.* The program keeps A2 at the base (polarity pi), O2P_0 in
  the array O2P, and O2P_s[w] at V[2048 s + w] for w in VN[s] (Lemma 14'
  (v)), a subset of VS[s] of 358,840 words in all (df0136bc: 626,300).
- (iii) *Low steps.* If ctz(t) < K, only s changes and h does not, so no
  stored word changes: the body does no round-2 work and round 3 reads w
  from V[2048 s + w] when w is in VS[s], else from O2P.
- (iv) *High steps.* If j = ctz(t) >= K, h changes by Gray bit j and the
  state after the step is s = 2^(K-1) (j = K) or 0. The body flips the read
  A2 support words of z-bit ORDER[j] (Lemma 6), and for every view s'
  (base included) and every word w that Lemma 6 patches for this bit and
  that is maintained in view s', it XORs into the stored word the same A2
  terms as the base patch with W toggled once per term that lies in the
  support of a low bit set in s'. That is Lemma 6's patch evaluated at the
  point zperm(h_old + s'), since A2 there differs from the base by those
  supports. Words not patched for this bit change in no view, and words
  outside VS[s'] equal the base. The patches of the view that round 3
  reads are merged into the round-3 loads (as in bs7); the others are
  plain load, XOR (or NOT), store.

By induction over t, every maintained word is exact at every step; words
of VS[s] outside VN[s] are never written (not even by the setup) and never
read.

**Lemma 14 (block memo of round-3 chi outputs; exact; df0136bc).** A
**block** is the 2^K steps t = 2^K m + r, r = 0..2^K - 1. Within a block h
is constant (the bits of gray(t) at positions >= K depend only on m), and
the view state at position r is seq_p(r) = gray(r) XOR p 2^(K-1) with p =
m mod 2. The step at r = 0 is the block's high step (ctz(t) >= K) or t =
0. Each body knows its (p, r): leaf j >= K has r = 0 and p = 1 iff j = K,
and a leaf j < K with state s has the unique r with ctz(r) = j and
seq_p(r) = s.
- Raw chi output X of round-3 row (Y, b) (before theta of round 4, in the
  encoding of Lemma 8) is a fixed function of the row's input words X,
  X+1, X+2 (mod 5) only. Its **class** in state s is the triple of the
  expressions VD[s][w] of these three words (empty for s = 0 or w not in
  VS[s]). Equal classes in one block mean equal input values (Lemma 13
  (i)), hence equal outputs.
- At position r an output whose class occurred at an earlier position of
  the block is loaded from R3C (word 5 ((64 Y + b) 2^K + class) + X, class
  numbers < 2^K in order of first occurrence); otherwise it is computed
  (the row's gate plan restricted to the outputs it computes, reading only
  their inputs), and stored to that word if its class occurs again later
  in the block. Everything after the chi outputs (parities, D, stores) is
  unchanged.

**Lemma 14' (memo2: complement classes and stored chi terms; exact;
new).** Same blocks and positions. For input word X of a row write its
expression in state s as e_X(s) = e'_X(s) XOR f_X(s) W, with W not in
e'_X(s) and the flag f_X(s) in {0, 1}.
- (i) *Reduced classes.* The **reduced class** of output X at position r
  is (e'_X, e_(X+1), e_(X+2)) at seq_p(r). If it equals the reduced class
  at an earlier position r0, then (Lemma 13 (i)) inputs X+1 and X+2 are
  equal at r and r0 and input X differs by (f_X(r) XOR f_X(r0)) W. Chi
  output X is a XOR (NOT b AND c), affine in a with coefficient 1, so
  out(r) = out(r0) XOR (f_X(r) XOR f_X(r0)) W in every encoding. Such an
  output is loaded (from the R3C word of the reduced class's first full
  class) and complemented with one NOT when the flags differ. If at least
  3 positions of the block carry the other flag, the first of them also
  stores its (complemented) value under its own full class and the later
  ones load that word without a NOT.
- (ii) *Stored terms.* The term NOT b AND c of output X depends only on
  inputs X+1 and X+2, so positions with equal **term classes**
  (e_(X+1), e_(X+2)) have equal terms. Consider the first occurrences of
  reduced classes at positions r >= 1. If the term class of such an output
  occurred at an earlier such first occurrence r1 >= 1, the output is
  computed as out = a XOR t, with t the term stored by the body at r1 in
  the polarity of that body's gate (Lemma 8: the AND form gives the term,
  the OR form its complement, and the form is a fixed function of the
  row's polarities and of which outputs the body at r1 computes, so the
  reading body knows it), plus one NOT when the input and output
  polarities require it. The body at r1 stores t to R3T (word
  5 ((64 Y + b) 2^K + term class) + X) when at least M2THR = 1 later first
  occurrence uses its term class.
- (iii) *What is stored.* An output is stored to R3C (at its full class)
  when its reduced class occurs again later in the block, as in Lemma 14;
  the complement-class and term stores are those of (i) and (ii). All
  rules are fixed by the static geometry (`gen.Geometry.m2rows`).
- (iv) *Exactness.* The positions of a block run in order, and every R3C
  or R3T word a body loads was stored at an earlier position of the same
  block, so every load reads the exact value of this block; words from
  earlier blocks are never read before being rewritten. The self-test's
  and the battery's runs from the first step of a block with no memo
  prefill check this (a never-written word cannot be read without a fault).
- (v) *Maintained words.* VN[s] is the set of words of VS[s] read by an
  output computed at a position of state s in either block pattern (all
  three inputs of an output computed in full, input X of an output computed
  from a stored term); only these view words are set up and maintained
  (Lemma 13 (ii)): 358,840 words at K = 10 (df0136bc: 626,300).

## 5. The algorithm and its counted program

### 5.1 Run and batch setup

**Once per run.**
- c = RAND AND (2^256 - 2^128), i.e. c = TAG*2^128 with TAG its uniform
  high 128 bits.
- CNT = 0.
- The z tables ZT[x] = zperm(x) and ZT[2^16 + x] = zperm(x << 16) for
  x < 2^16 (used only on the candidate path): ZT[0] = ZT[2^16] = 0 and
  ZT[x] = ZT[x AND (x - 1)] XOR 2^ORDER[ctz x] (and the same with
  ORDER[16 + ctz x]), 3 operations per entry, 393,213 operations
  (counted; Section 10.1). We charge 2^19 operations per run.

At the start of batch beta, c = TAG*2^128 + beta*2^39 (2^32 steps of 128
pair ids each carry it over).

**Once per batch** (counted straight-line programs, 2,383,931 operations
in all, 62 registers; `setup_gen.py`):
- draw 768 random words (3 per group) and build the 256 structured
  prefixes (Section 2); store their four words at PREF + 1024*beta + 4p + w,
  with 1024*beta = (c AND (2^128 - 1)) >> 29 read from c, and transpose
  them;
- store the padding planes;
- compute round 1 and A2 (stored with polarity pi), and O2P (z = 0, the base
  of t = 0);
- store the maintained view words: V[2048 s + w] = O2P[w] XOR (XOR of the
  stored A2 words of VD[s][w]) [XOR W] for every s >= 1 and w in VN[s]
  (Lemma 13 (i) at h = 0; df0136bc stored all of VS[s]);
- store the delta-swap masks and set s = 0.

The setup program's prefixes (all constraints of Section 2), A2, O2P,
maintained view words and masks were compared with an independent
reference (Section 10.1). With batch-loop control this is < 2^23
operations per batch, i.e. < 2^-17 per message, which Section 8 charges.

### 5.2 Per z-step program (fully unrolled; block-unrolled control; exact batch count)

There are two persistent registers: s (the block counter, not the view
state s of Lemma 13: the steps t = 2^K m + r, r < 2^K, form block m, and
s = m during block m) and
c = TAG*2^128 + n, n the current pair id. The program is laid out as
straight-line code with direct jumps and conditional branches only (no
indirect jump):

    T0:       the t = 0 body (z = 0); falls through into CHAIN_0
    CHAIN_p:  (p = 0, 1) the 2^K - 1 low bodies of block pattern p, in position
              order r = 1, ..., 2^K - 1 (the body of (leaf ctz r, state seq_p(r)),
              Lemma 14), one after the other; then jump TOP          (1 operation)
    TOP:      s = s + 1; then bit tests v = s AND 2^i ; branch to H_(K+i) if v != 0
              for i = 0, 1, ..., 31 - K (2 operations each); if all fail
              (s = 2^(32-K)) the batch ends                  (1 + 2(32 - K) operations, once)
    H_j:      (j = K, ..., 31) the high body of leaf j; then jump CHAIN_p,
              p = 1 iff j = K                                        (1 operation)

The steps of block m >= 1 are TOP (s becomes m; the tests stop at the
lowest set bit of m, so j = K + ctz(m) = ctz(2^K m)), the high body
H_j, and the chain of pattern p = m mod 2. Block 0 is T0 and CHAIN_0.
TOP's test value v lives in a body register (0..61), which is free
between bodies, so s and c stay the only persistent registers.
Hence a low step (ctz(t) < K) runs **no control operation**; a high step
with ctz(t) = j runs 1 + 2(j - K + 1) operations before its body and one
jump after it; the last body of each chain (r = 2^K - 1: leaf 0 in state
2^(K-1) for p = 0, and in state 0 for p = 1) is followed by one jump. The
self-test walks this layout for batches of 2^(K+1), 2^(K+2) and 2^(K+5)
steps (`machine.layout_trace`) and checks that it executes exactly the
bodies (ctz t, gray(t) mod 2^K) in step order with the counted number of
control operations.

Each body: for j >= K, A2 flips and the base and view patches (Lemma 13
(iv)) merged into round 3; for j < K nothing before round 3. Then R3
(start 10; Lemma 14/14' memo loads and stores), R4 (cone, start 61), R5
(cone, start 34) with the last-round blocks and phase 1 interleaved as
soon as their round-5 planes exist (16-row blocks), phase 2, the frame fix
and 256 table steps (5.3). The exact count of one batch is

    T = body_0 + sum_{j < K} sum_{s in states(j)} 2^(31-K) (body(j, s) + jump(j, s))
        + sum_{j >= K} 2^(31-j) (1 + 2(j - K + 1) + body(j) + 1) + 1 + 2(32 - K)
      = 117,398,575,636,479,

where states(j) are the 2^(K-j) states in which leaf j runs (each low body
runs once in every block of its pattern, 2^(31-K) times per batch) and
jump(j, s) = 1 for the two chain ends, else 0. The self-test computes T
from the compiled bodies (Appendix A.1), and the simulator's measured
count of every step equals control + body + jump. Control costs
29,360,123 operations per batch in all (0.0068 per z-step;
df0136bc: 24.0 per z-step).

**Ledger (simulator count).** Body sizes: t = 0: 31,491; leaves j < K
(2,046 bodies): 26,415..30,882 (they differ only by the
memo pattern of their block position); leaves j >= K (22 bodies, one per
leaf): 301,235..376,557, dominated by the view patches. Per z-step
on average:

| block | ops | gates | loads | stores | ROT/ADD/CMP/branch |
| --- | ---: | ---: | ---: | ---: | ---: |
| round 2 and view patches (high steps only) | 279.79 | 93.26 | 93.32 | 93.21 | 0.00 |
| round 3 (memo loads and stores included) | 7,004.18 | 3,473.32 | 1,746.67 | 1,784.19 | 0.00 |
| round 4 (cone) | 9,366.00 | 6,488.00 | 1,559.00 | 1,319.00 | 0.00 |
| round 5 (cone) | 5,264.00 | 3,851.00 | 1,314.00 | 99.00 | 0.00 |
| last round, 35 planes | 379.00 | 280.00 | 99.00 | 0.00 | 0.00 |
| transpose phase 1 | 1,517.00 | 1,128.00 | 11.00 | 96.00 | 282.00 |
| transpose phase 2 + frame fix | 2,116.00 | 1,504.00 | 108.00 | 0.00 | 504.00 |
| 256 table steps | 1,408.00 | 256.00 | 256.00 | 256.00 | 640.00 |
| control (TOP: add, bit tests; end of batch) | 0.0049 | 0.0020 | 0 | 0 | 0.0029 |
| jumps (after high bodies and chain ends) | 0.0020 | 0 | 0 | 0 | 0.0020 |
| **total = T / 2^32** | **27,333.99** | 17,073.58 | 5,187.00 | 3,647.40 | 1,426.00 |

Gates are XOR/AND/OR/NOT after store-to-load forwarding (the control's
AND with a constant mask is counted as a gate). Round 3 includes
1,431.60 R3C loads, 185.73 R3C stores, 98.71 R3T loads and
44.46 R3T stores per z-step on average.

### 5.3 Tagged-id table (bs4's table with pair ids)

S has 2^140 words at address 0 and is never initialised. All other arrays
lie in [2^140, 2^140 + 2^99) (Section 11). The key K < 2^140 is the
address. Per message q of a z-step (hot path; 5 operations for even q, 6
for odd q, 1,408 per z-step):

    w = LOAD [K] ; x = w XOR c ; f = (x < 2^128) ; if f goto CAND_q
    STORE [K] = c ; (odd q only) c = c + 1

- **Hot path.** x < 2^128 iff the high half of S[K] equals TAG. A written
  slot always holds TAG*2^128 + (pair id of the last message with key K),
  so every lookup of a written slot is a **genuine candidate**: an earlier
  message with an equal 140-bit key, which is a member of the stored pair
  (Section 5.4).
- **Garbage candidates.** A never-written slot is a candidate only if its
  initial high half equals TAG. TAG is uniform and drawn after the initial
  memory is fixed, so each lookup is a garbage candidate with probability
  at most 2^-128, whatever the initial memory.
- **Overwrite rule.** After the step, S[K] = TAG*2^128 + n, as in a
  Briggs-Torczon set whose stored index is the pair id of the message. Only
  the last message with each key is remembered (up to its pair partner).

### 5.4 Candidates: verify and continue, halting, cap

- **Calling convention** (5kyguy's, from 6e715d9a). Each of the 2,069 x 256
  branch sites has its own out-of-line copy CAND_q of the candidate block.
  It knows statically the member bit m = q mod 2 of the current message and
  its return point, and ends with a direct jump back to the site's STORE (1
  counted branch). The copies are code, not run time (Section 11).
- **Rebuild.** CAND_q saves 14 registers and takes i = w AND (2^128 - 1)
  (stored pair id) and n = c AND (2^128 - 1) (current pair id). It decodes
  a pair id to beta = id >> 39, t = (id >> 7) mod 2^32, k = id mod 128 and
  z = gray(t). Member m (q = 2k + m) sits in slot p = decode_slot(q) =
  32(k mod 8) + floor(k/8) + 16m, and its four prefix words are at
  PREF + 4(256*beta + p) = PREF + 1024*beta + 128(k mod 8) + 4 floor(k/8)
  + 64m, the address taking beta modulo 2^88 (every real beta is smaller).
  The decode costs 13 operations per id; loading one message and XORing
  LE32(z) into bits 0..31 of word 1 and bits 128..159 of word 3 (lanes 4
  and 14) costs 10 more (11 for m = 1). A garbage id rebuilds some
  128-byte string.
- **Verify.** It evaluates the current message (member m of n) and then
  each member of pair i, in turn, with the reference function (3 units in
  all). After each stored member it compares the 256-bit digests with the
  current one (1 compare, 1 branch) and, if they are equal, the four
  message words (1 compare and 1 branch each, leaving at the first
  difference).
- **Halt.** If a stored member has the current digest and is a different
  message, it outputs the pair and halts.
- **Continue.** Otherwise it loads CNT, adds 1 and stores it. It aborts the
  run with failure if CNT >= VCAP. It then restores the registers and
  jumps back.
- **Costs** (simulator, and by the count above):
  - continue: 111 operations above the hot path (112 for odd q) when no
    digest matches, and 119 / 120 when a stored member is the current
    message itself (equal digests, same message; this happens when
    q = 2k + 1 meets the slot that 2k wrote, or in a replay). All include
    the jump back and (since df0136bc) the 7 operations per decoded id that
    map gray(t) to z through ZT (2 table loads);
  - halt: measured 80 operations after the branch;
  - abort (CNT reaches VCAP): a prefix of the continue path.

  Continue and halt each add at most 3 units.
- **Around each reference call.** The simulator's `hash4` takes the four
  message words in registers and returns the 256-bit digest as 1 unit with
  no word operations. Forming the padded 1600-bit input explicitly (7
  stores of state words: the four message words, the word holding
  0x8000000000000006 in lane 16, zeros; 2 immediate moves) and reading the
  digest (1 load) is at most 10 operations per evaluation, 30 per
  candidate. We charge **150** operations per candidate (120 + 30); the
  five-decimal claim holds up to 152 (Section 8).

The cap is an instruction immediate:

    VCAP = floor(N^2 / 2^141) + floor(N^2 / 2^148) + 2^91 + 2^61.

The term floor(N^2/2^148) = E/128 is a margin for H1 (Section 7).

## 6. Correctness (unconditional)

- **Evaluator exactness.** Lemmas 1-3, 6, 12 and 13 keep every read A2 word
  of the base, all of the base O2P and every maintained view word exact at
  every t, and Lemmas 14 and 14' make every memo load exact. Lemmas 4, 7, 8, 10 and 11 make every needed word
  of rounds 3-5 exact in its encoding. Lemma 9 makes the key of slot p
  equal key_of_digest(K*) of message p. Section 10 checks this bit for bit.
- **Outputs.** The run outputs only two distinct 128-byte strings whose
  256-bit digests were equal under two reference evaluations, which is a
  full collision. A key match or a garbage word never produces output by
  itself.

## 7. Success probability

The run halts at the first verified collision. The failure events are:

- **F3:** two groups produce the same message. m(g, z) = m(g', z') needs the
  ten free lanes other than 4 and 14 to be equal and L4 XOR L4' =
  L14 XOR L14' in a set of 2^32 values, an event of probability at most
  2^32/2^768 per pair of groups. There are fewer than 2^191 pairs, so
  Pr[F3] < 2^-545 (no heuristic).
- **F1:** no two of the N messages have equal digests.
- **F2:** for some colliding pair (a, b), a processed before b, some message
  c between them has a's key and a different digest.
- **F4:** the number of continued candidates reaches VCAP.

**If none of F1-F4 occurs, the run succeeds.** Take a colliding pair
(a, b).
1. When a is processed, it either halts with a collision or sets
   S[K] = TAG*2^128 + (pair id of a).
2. Each later message c before b with that key: by not-F2, c has a's
   digest. The slot holds the pair id of the last earlier message d with
   a's key (a itself or later), hence (not-F2) d has a's digest. c's
   candidate rebuilds both members of d's pair, so d among them; d was
   processed before c, so d is a different index and (not-F3) a different
   message. Unless an earlier member already gave a verified collision,
   comparing d with c finds equal digests of distinct messages, and the
   run succeeds. (A member equal to c itself, the case q = 2k + 1 after
   2k, is skipped as the same message.)
3. Otherwise, at b's lookup the slot holds the pair id of such a message d,
   and the candidate finds the collision in the same way.
4. Without F4 the run is not aborted before then.

So Pr[fail] <= Pr[F1] + Pr[F2] + Pr[F3] + Pr[F4].

**Heuristic H1 (declared; identical text in claim.json).** (a) For the
failure events F1, F2 and the genuine-candidate part of F4 (proof Section
7), the N = NB*2^40 digests (NB = 307,990,341,830,783,024,002,353,940
batches, Section 7) of the grouped message set {m(g, z)}
(independent prefixes P_g, each uniform over the 2^768 structured 128-byte
prefixes of Section 2, all z in {0,1}^32, processed in any fixed order
chosen independently of the digests, in particular the order of Section 2:
batch by batch, t = 0..2^32-1 with z = zperm(gray(t)), slots p = decode_slot(q) =
16*(q mod 16) + floor(q/16) for q = 0..255) behave like N independent
uniform 256-bit values, i.e. Pr[F1] <= exp(-N(N-1)/2^257), Pr[F2] <= N^3/6
* 2^-396 and, since the 140-bit key is a fixed function of 140 digest bits,
the number Y1 of message pairs with equal keys has E[Y1] <= N^2/2^141 and
Var[Y1] <= E[Y1]. (b) Run-selection premise of the evidence: the
organizer-executed configuration (four layouts, 18-bit masks, N_t = 2^9,
256 trials per experiment, per-trial seed derivation by the runner) is
unchanged from our public packages 949c283b and 5e73af65; the message
family is fixed externally (5kyguy, 6e715d9a; their organizer trials of it
were not used to choose anything here); the only parameters chosen for
this package (storage polarity pi, start planes 10, 61, 34, prefix seed
label s3r6-ls128-v1, and, new since bs7, the view count K = 10, the Gray
order ORDER, the output of the shipped generator ordergen.py with seed
12, the memo2 rules and threshold, and the batch count NB, fixed by the
success-bound rule of cert.py) were set by cost objectives or fixed
rules, before or without any of our trials, never from a digest or
masked-collision statistic; and our own runs of the
experiment script were specified and hashed before our first trial of this
family and are all reported in proof Section 10.3, together with every
later run by us or by agents working for us up to the run-list freeze of
this revision (reviewer runs and exact replays included), none selected,
repeated or dropped according to its outcome.

With N = NB * 2^40, NB = 307,990,341,830,783,024,002,353,940 (the smallest batch
count whose bound below is at least 0.3905; `cert.py` checks NB and
NB - 1):

- **F1.** Under H1, Pr[F1] <= exp(-N(N-1)/2^257) < 0.609459897.
- **F2.** Under H1, Pr[F2] <= N^3/6 * 2^-396 < 4.0104 * 10^-5 (< 2^-14.6).
- **F3.** Pr[F3] < 2^-545.
- **F4.** Continued candidates are Y1 + Y2.
  - A genuine one is the lookup of a message b at a slot last written by
    an earlier message d with K(d) = K(b). Each message makes one lookup,
    so distinct genuine candidates give distinct pairs (d, b) with equal
    keys, and they number at most Y1. Pair ids change only what is
    rebuilt, not this count. With E = floor(N^2/2^141) < 2^115 and
    E' = floor(N^2/2^148) > 2^107.98, Chebyshev gives
    Pr[Y1 >= E + E' + 2^91] <= E/E'^2 < 2^-100.
  - **Sensitivity.** F4 is the most sensitive use of H1: by
    Cauchy-Schwarz any non-uniformity of the 140-bit key can only raise
    E[Y1]. The cap tolerates a relative excess of 2^-7 (0.78%) over
    N^2/2^141, plus 2^91 pairs. The scaled experiments resolve the
    masked-pair mean to about 0.6% (pooled ratio to the uniform model
    1.0022 +- 0.0061 over the 53,248 pre-registered trials of Section
    10.3; 1.000 over all 58,368 sampled trials), so this margin is not certified
    by them. Within-group pairs would need an
    average key-collision probability above about 2^-51, or above about
    2^-19 for the pairs of one z-difference, to matter.
  - Garbage ones, Y2, satisfy E[Y2] <= N * 2^-128 < 1 for any initial
    memory (Section 5.3; no heuristic), so Markov gives Pr[Y2 >= 2^61] <=
    2^-61.

  Hence Pr[F4] <= 2^-100 + 2^-61.
- **Total.** Success >= 1 - Pr[F1] - Pr[F2] - Pr[F3] - Pr[F4] >= 0.3905
  (model value 0.3905000; the exact sum, computed by `cert.py` with
  60-digit decimals, exceeds 0.3905 by 3.7e-29, so the rounded-up
  figures above give only > 0.390499). We claim 0.39, which leaves an
  allowance of 0.0005 (df0136bc: 0.00106 with 255 * 2^80 batches). The allowance is
  not a statistical margin: under H1 the bound holds as stated, and the
  experiments of Section 10 resolve the success frequency only to about
  +-0.008 per layout, which neither allowance could cover.

The scaled analogue of Y1 is the per-trial `masked_pairs` count. Its
variance/mean ratio is about 1 (Section 10.3).

**Rigorous partial support (jaazinn's argument, adapted).** For every z,
P -> m(P, z) permutes S (Section 2), so each m(g, z) is uniform over S. For
groups g != g' the messages m(g, z) and m(g', z') are independent and
identically distributed, so by Cauchy-Schwarz they collide with probability
>= 2^-256. Within-group pairs are a 2^-96 fraction, so the expected number
of colliding pairs is at least (1 - 2^-96) * N(N-1)/2^257. H1 is needed for
the second-moment behaviour behind Pr[F1], for F2 and for Y1.

**What does not change the message set.** Bitslicing, batching, the
incremental round 2, the views, the block memo and memo2, the Gray order,
the block-unrolled control, the cone,
the start planes, the compiler, the 140-bit key, the encodings, the
transpose layout and the pair ids fix only how and in which order digests
are computed and how candidates are rebuilt. The Gray order permutes the
2^32 values of z within each batch (Lemma 12); F1-F4 and Y1 are statements
about the set of N messages and their pairs, not about the order.
That order is a function of (beta, t, q), never of digests. The 128-byte
family does change the message set relative to bs5 and bs6, and the batch
count NB fixes its size N. H1 is stated for this set, and the experiments
of Section 10 use it.

## 8. Time bound

The main loop executes exactly T = 117,398,575,636,479 operations per batch of 2^40
messages (Section 5.2), i.e. T / 2^40 = 106.7734 per message. This covers
the round-2, view and memo work, rounds 3-6, the transpose, every table
load, store, compare and branch, and all control and jumps. Per batch the
setup programs and batch-loop control take < 2^23 operations
(2,383,931 counted). On top come at most VCAP continued candidates
(3 units + 150 operations each), one halting candidate (3 units + 150), the
per-run initialisation (ZT and c, < 2^19 operations), 1 unit of
unassigned slack (the "+ 1" below) and a term of 2^100
units that charges generating the program and all target-specific search
and development by anyone. So, in every run (no restarts), with NB =
307,990,341,830,783,024,002,353,940 batches,

    T_run <= NB (T + 2^23)/1626 + 2^19/1626 + VCAP (3 + 150/1626) + (3 + 150/1626) + 1 + 2^100
          < 2^124.07261            (log2 of the right-hand side: 124.072606093).

**Integer certificate.** With K' = 2^28 * 1626,

    A = T_run K' = (NB T + NB 2^23 + 2^19) 2^28 + VCAP (3*1626 + 150) 2^28
        + (3*1626 + 150) 2^28 + K' + 2^100 K'

is an integer, and A^100000 < 2^12407261 * K'^100000 holds exactly (and
fails for 2^12407260). The claimed time_log2 is therefore
**124.07261**, rounded up at the fifth decimal (the format of GordoAR's
5dac3f95 and dcdd90ec; at three decimals the same certificate gives
124.073). `cert.py` (Appendix A) computes NB, checks its rule and
prints the claim.

- **Slack.** The claim would still hold with T / 2^32 up to
  27,334.060, or with up to 152 operations per candidate. The
  count T is a deterministic function of the shipped code, so a rerun of
  the self-test reproduces it exactly.
- **Expected verification work.** Under H1 it is about 2^116.6 units,
  about 156 operations per z-step on average (150 operations
  charged per candidate).
- **Generation and development are charged.** preprocessing_log2 = 0
  because nothing is left outside T_run: setup is per batch, and the
  2^100-unit term charges generating the program once (`ordergen.py`,
  `choose_polarity`, compiling 2,069 bodies) and all
  target-specific search and development for this target by anyone: every
  search, sweep and annealing run that chose a constant (start planes,
  polarity, K, the generator seed, ORDER and the scored extensions of
  it, the memo2 rules and threshold, the discarded candidates), every compilation,
  self-test, experiment, prototype and review run of bs1-bs11, and the
  earlier work on this target that we build on. Any computation
  physically performed for it is far below 2^100 * 1626 word primitives.
  (For our own part, every run by us or by agents working for us ran on
  one 15-core machine between 2026-09-27 and 2026-10-10: fewer than 15 x
  14 x 86,400 x 4.5 * 10^9 x 10 < 2^60 machine instructions. Even
  counting 2^20 v5 word primitives per instruction, enough to emulate
  multiplies, divides, floating-point and vector instructions, that is
  below 2^80 primitives, i.e. below 2^70 units. This remark is not needed
  for the bound.) The term is about 2^-24 of T_run; the five-decimal claim
  is unchanged for any additional development below 2^105.6 units
  (exact check with `cert.py`'s A). 5kyguy's 6e715d9a charges 2^50 units
  for program generation; we use a larger term so that the charge does not
  rest on our account of our own machine time.

## 9. Sensitivity of the bound to conventions

Same program and exact batch count, the candidate term included, NB
batches unless stated; time_log2 rounded up at the fifth decimal.

| reading | ops/z-step (T / 2^32) | ops/message | time_log2 |
| --- | ---: | ---: | ---: |
| every executed primitive once, 64 registers (claimed) | 27,333.99 | 106.77 | 124.072606 -> 124.07261 |
| + one address addition per direct load/store, + one MOVI per ALU immediate | 36,040.39 | 140.78 | 124.46953 |
| as above, + one op per shift or rotation amount | 36,826.39 | 143.85 | 124.50052 |
| batch count 255 * 2^80 (df0136bc's; success bound 0.39106) | 27,333.99 | 106.77 | 124.07396 |
| logic gates only (reference; needs far more than 64 registers) | 17,073.58 | 66.69 | 123.39864 |
| df0136bc's program (bs9; K = 10, no memo2, per-step dispatch), this NB | 27,743.22 | 108.37 | 124.09393 |

We do not adopt a fixed-bank reading. Under our 64-register reading every
direct load and store is charged. The second and third rows also charge
the immediates of the control (the add of s and the bit-test masks); they
keep the candidate term at 150 operations (pricing the candidate path's
own address additions and immediates in the same way adds about 0.0001).

## 10. Evidence

### 10.1 Counted simulator and shipped program (participant evidence)

- **Shipped.** Appendix A contains the generator (`gen.py`), the compiler
  and simulator core (`ir.py`), the run harness with batch setup at
  reference level, control, the views and memo state and the candidate
  path (`machine.py`), the counted setup generator (`setup_gen.py`), the
  self-test (`selftest.py`), the certificate (`cert.py`), the Gray-order
  generator (`ordergen.py`) and two short adapters (`ref.py`,
  `vkeccak.py`). The reference geometry (rho, gate plans, polarities, kept
  planes, transpose orders, start planes, cones) is imported from the
  shipped experiment script.
- **Every load-bearing constant is produced by shipped code.** ORDER:
  `ordergen.py` (Lemma 12: `python3 ordergen.py 10 12 600`, df0136bc's
  order, unchanged; the self-test does not rerun it). Storage polarity pi:
  `gen.choose_polarity` (deterministic; the self-test asserts it equals
  the script's `PI`). The memo2 actions and the maintained words:
  `gen.Geometry.m2rows` and `needed2` (deterministic given the threshold
  M2THR = 1, which the prototype comparison of Section 0 chose by static
  counts). Gate plans, kept planes, transpose stage orders, cones:
  deterministic functions of the shipped experiment script. The batch
  count NB: `cert.py` (the rule of Section 7).
  K = 10: df0136bc's (fixed by the exact counts T of builds with K = 3, 9
  and 10), kept here although memo2 samples project K = 11 and 12 to be
  cheaper (Section 0, Lemma 12). The start planes (10, 61, 34) are bs7's: the
  coordinate search of Lemma 7 (each plane over all 64 values with the
  other two fixed, objective the worst compiled leaf, two passes from
  (2, 39, 34)) run on bs7's shipped compiler (7e40f784, Appendix A); the
  loop driving it is not shipped, and the planes were not searched again
  for this program. A reviewer's static counts on df0136bc's generator
  found (2, 39, 34) 2 to 4 operations cheaper per body there (about 0.0002
  in time_log2); our prototype of this program found about the same (3
  operations per z-step), so the planes are kept and cost at most about
  that. Any triple gives a correct program whose cost the self-test
  counts exactly; the triple is part of the algorithm's description, like
  every other constant here (read as advice it would be 18 bits, 3 bytes),
  so the claim declares no nonuniform advice. Each
  search is charged (Section 8), and none reads a digest.
- **Self-test** (`python3 selftest.py REPO_ROOT`; 15 minutes with
  NPROC = 6 on our machine, at most 1.4 GiB per process; Appendix A.1). It
  rebuilds the geometry, checks the control layout, rebuilds all
  2,069 bodies and prints T = 117,398,575,636,479 and the body hash
  `4c07e7ba...`. Each body is compiled, its 256 table steps are
  checked statically, and it is run once on the simulator from a random
  state (low bodies at their block position, with the memo words (R3C and
  R3T) of the block's earlier positions prefilled from a reference), against
  `verifier/keccak.py`: 529,664 keys, measured = control + static +
  jump on every body, and A2 (read words), O2P and the maintained view
  words (the current state and 12 random states, all states on every 61st
  body) equal to a rebuild from the prefixes. Then 3 runs of 40
  consecutive steps (crossing block boundaries and high steps; the second
  starts at the first step of a block with no memo prefill, so each memo
  load there reads a word the program itself wrote) with the same checks
  after every step; two replayed z-steps (512 genuine candidates, exact
  rebuilds, continue costs 111..120) and the halting path
  (80); and the counted setup (2,383,931 operations, equal to a
  reference incl. all maintained view words) and ZT (393,213).
- **The simulator.** The program runs on a counted 256-bit word-RAM
  simulator with an explicit 64-register file (high-water check, at most
  62 per body plus s and c) and a counter per primitive. Its `hash4`
  instruction (1 unit) is `verifier/keccak.py:sha3_256(m, 6)`.
- **Hostile memory.** Before every z-step all scratch words of the step and
  all 62 non-persistent registers are overwritten with random junk. A read
  outside the cone, or of a word not yet written in the step, would corrupt
  a key. The memo words R3C and R3T and the views are persistent and are
  written only by the program (for a run started inside a block, the views
  come from a reference rebuild and the memo words of the block's earlier
  positions from the base O2P and the view expressions). A read of a
  never-written memo or view word faults. Never-written table words are
  set, by body, to all-ones, random, zero, or adversarial (high half =
  TAG).
- **Mutations** (`mut10.py`, our driver, not shipped; bodies from the
  compile pass below): each mutation was caught (key mismatch
  against the verifier, a read of a never-written word, or the
  maintained-state check):
  - M1 drop view store (leaf 11, view 433, word 275)
  - M1 drop view store (leaf 11, view 892, word 1308)
  - M2 R3C memo load from a wrong slot (body (2, 974), position 372)
  - M2T R3T term load from a wrong slot (body (2, 974), position 372)
  - M4 view load from the base (body (2, 974), position 372)
  - M2 R3C memo load from a wrong slot (body (2, 194), position 892)
  - M2T R3T term load from a wrong slot (body (2, 194), position 892)
  - M4 view load from the base (body (2, 194), position 892)
  - M2 R3C memo load from a wrong slot (body (1, 85), position 102)
  - M2T R3T term load from a wrong slot (body (1, 85), position 102)
  - M4 view load from the base (body (1, 85), position 102)
  - M3 drop R3C store (pattern 0, row (0, 0), X 0, position 1, reloaded at 2)
  - M3 drop R3C store (pattern 1, row (0, 1), X 0, position 1, reloaded at 2)
  - M6 drop R3T term store (pattern 0, row (0, 49), X 1, position 1, used at 2)
  - M6 drop R3T term store (pattern 1, row (0, 11), X 0, position 1, used at 2)
  - M9 drop complement-class store (pattern 0, row (0, 1), X 2, position 1, reloaded at 30)
  - M9 drop complement-class store (pattern 1, row (0, 61), X 0, position 1, reloaded at 30)
  - M7a complement added to an exact R3C reload (body (7, 960), position 640)
  - M7b complement dropped from a complemented R3C reload (body (0, 771), position 509)
  - M8 term polarity flipped after an R3T load (body (5, 944), position 288)
  - M5 body of state 252 run in state 204 (leaf 3)
  - M5 body of state 796 run in state 500 (leaf 3)
- **Battery on this program** (`verify10.py`, our driver, not shipped;
  every check it makes is one of the self-test's; bodies compiled once by
  the pass below, whose body hash equals the self-test's, and loaded with
  their per-body hashes checked). Seeds 2026, 4711, 31337, 5150, 7 and 99 (the last two run after the others, in the same way): each runs 96 z-steps from the first (high) step of a block with no memo prefill, then 40 steps crossing a block boundary from inside a block (the new block starts with the previous block's memo words in memory; batch index near the maximum NB - 1), seed 2026 also the t = 0 body and the first 24 steps of a batch: 840 steps and 215,040 keys. One run of 2,088 consecutive steps from a block start (no prefill) through two whole blocks, one of each pattern, and 40 steps into the third (534,528 keys; every low body at its block position, three high steps). In all 749,568 keys, 0 mismatches against `verifier/keccak.py`; on every step measured = control + static + jump; A2, O2P and the maintained view words equal to a rebuild every 8 steps (every 32 in the long run) and all views at the end of each run; every data address in [2^140, 2^140 + 2^99) and every table address below 2^140.
- **Static scan** (the pass below): the t = 0 and low bodies store nothing
  to A2, O2P or the views, and in the 22 high bodies each of the
  2,338,858 such stores depends only on loads of A2, O2P and
  views through XOR and NOT (an affine map over GF(2), the same in every
  bit position).
- **Runs of the counted program for this revision** (SHA-256 of the
  output files; none runs the experiment script, none reads a digest
  statistic):
  - development check of the generator and control code at K = 4 (`S8CFG`, the whole self-test at K = 4 with the K = 12 development order, 59 bodies, 15,104 keys; a development version of the Appendix A code): `dev/st_k4.log` 245758f20af4d3b83ed72b1e400b2a96b82a5c7bd5f3b735426617472516e53d
  - K = 12 development (not used): resource measurement (5 bodies compiled and run through the self-test's per-body check): `dev/measure12.log` d7dee51b983adcaac8a279c69acd3a501251415d6460c29797055532415372a2
  - K = 12 development (not used): pre-test of the self-test's sequential end stage (control layout, steps from a block start without prefill and across a boundary, candidate replays, halt, counted setup, ZT): `dev/endtest12.log` ef2a797ff75f53495472b0e61de7c9add919c871f982f0bff07050f3d376701b
  - K = 12 development (not used): `ordergen.py extend 12` with a development version of `ordergen.py` (the scored extension of ORDER by bits 13 and 26; 809 s): `ordergen_extend12.out` 03471f937ad9d7e253f1e3203935cd1137adaf2a236feebbd225279f68538639
  - K = 12 development (not used): a compile pass over the 8,211 K = 12 bodies, stopped after 7,348 bodies (45 min), and a second attempt stopped after one minute; SHA-256 of the sorted list of (body file, SHA-256) of the 7,348 cached bodies: d94f4f765ec86e21b438cb4ae2abe002e21500535ced827e0ce883557e7cc199: `run_pass_run1.log` 061607cc06474f384b3161a97eeca9f1ee7faa9e428e90ff23ca8081176a387f; `run_pass_b.log` 9c77dc7a7bd6b05e15cd3c0de5b1143a42e58cd1d2fc77578db55940b4992d0e
  - compile pass over all 2,069 bodies of this program (exact T, body hash, static table check, static affine scan, opcode ledger; body cache for the battery; run on the Appendix A files before comment-only edits and before EXPECT and `cert.py`'s default T were filled in): `pass10.json` a70e96076a86f7d82b878a46cc121b664c5c3fc51ab977ba5f8735008c52b49a; `pass10.out` ca1abddf18270b79e46d6c30e6f29b00db73e0dc3f46fb103d050c432ea0bf22
  - a first start of the self-test, stopped after 48 s (during compilation) to make two comment-only fixes (the `ir.py` header and a `selftest.py` docstring): `selftest10_stopped.log` 3099799b3653bbfa5ad82bf893e6b4de49915bab52f78b40c56ee0344dd376e6
  - the shipped self-test on the final Appendix A files (Appendix A.1): `selftest10.log` 8f0aa26a2a5d5ea638c0b419800a9d9cd77690d56b23e6026f30ca816174b5b9
  - battery (`verify10.py` 2dbd981054de9486; it imports the generator from the Appendix A files, then differing from them only in those two comments): `ver10/seed_2026.json` d87fed670290ea971441cb234761c08040b2466ab99683e3fe68640ee5872ca0; `ver10/seed_4711.json` 37d6e7fc3d784b2ad04b8d997a9dfa75b9eaf40dfd1c649eb0ed9e8b1bc180c9; `ver10/seed_31337.json` baa3d3d7b9fa9c6efc86cdcd591b53c075181835f00b436b71334daae19dfaa4; `ver10/seed_5150.json` feb94dff3456344213bd036f28b7d465355207514f1da8876ecfd7ce1d1ef613; `ver10/seed_7.json` 4a420771e69f4edccb4d36cefd148b4e0389c7d5ed2c84e1d4e28be18f993d34; `ver10/seed_99.json` da377684546ddeafbaf0caeb9e8e35d5f601cc94f7706a35e12ff4a488ce2b56; `ver10/long_777.json` b259cc854b4282444df2850c9b95593b991a08357c03eda3ec233144b85847ef
  - mutations (`mut10.py` e727dde3598ed9f7; same import as the battery): `mut10.log` 1e81990bedb3ba75fab046003cb91c284c10cd5c5af6835a507a2509ef4ba36f
  - `cert.py T`: `cert10.out` 0c06245ee8f385a4d461bd8e6986f68e1c41171d13c3b7c5bd01eb5ebda1332e
- **Prototype runs** (development, charged in Section 8; static counts and
  bit-exact simulator checks of earlier versions of the memo2 generator;
  outputs hashed):
  - memo2 bit-exact runs on the counted simulator (K = 4, 5, 6, 10; thresholds 1 and 2; from block starts with no prefill): `t_k4_m2.jsonl` 8b8ab27c124f0acbb9ca48e55528f3bfe30cd83fb5ecebac09f0d403e65ca418; `t_k4b_thr1.jsonl` 60a6cb381f83604b9ee195841934626a0f97117c3e0db8fcc0b0376627bbebe5; `t_k4b_thr2.jsonl` 1478f6e5db9681fbe20b501f1e5f94c4fbc56751f8b19804761ae4954a514f58; `t_k5b_thr1.jsonl` 6f3596dc79a6d468bcc54125029360cffb3a45af497046c170cdbc05ab999631; `t_k6_m2.jsonl` c13353ad8474779dda59733bac593f7975632d1dc0e50782d4eb25b1bf509c98; `t_k10_m2.jsonl` 7e626ecc82aa7e2bdfce7e3efe6482976cd1e64ad10fc82eb1438d619f98b55f
  - paired static counts memo2 off/on (K = 10 thresholds 0, 1, 2; K = 11; K = 12), and the first, rejected memo2 variant: `st2_k10_t0.jsonl` 04aa6dc7105b42dbb65b618c0aaf6710e188ac8f9720ff069265995d1fbcd297; `st2_k10_t1.jsonl` 5b3b4f036f7c31aae4882c2fdbf41fa0315ebf0eb4a22b6b1078292e4d7d8a4f; `st2_k10_t2.jsonl` b436bc004476ed5e999936177d1d4fe1213b59bb9b5a9bffc4d1aacb965439c6; `st2_k11.jsonl` c7a4d4b1193c401b879d958824de3205c44dd3ba87b8a10f31ec50c21fe87308; `st2_k12.jsonl` 33081e65d28ef89bce82161176d94cae1d14824debfd4bf2e26783cd7a437893; `st_k4.jsonl` 113b18b67575d2473734ceeaee829dfe5a6dbabdb3b61dbbf3a5e2dd30ac9ba5; `st_k10.jsonl` 50a93c68d6bb6a83b0acfd65b16a11d3dd54b9ad5f33e8b9bdf477b4bb405029; `st_k10_t0.jsonl` 7d07649da05855dafc5ed49025c987496161de81f55b2c82711b112cb0bfca6a; `st_k10_t2.jsonl` 9aa30a2f6ff1617eef026e73acde4b5aa183a81d9ea05887aa3b236f26d630cb; `st_k10_t3.jsonl` 231bae61f973b066fb70d99c30adebb794f4b792d21d62cff33719005599c551
  - samples of df0136bc's generator at K = 10, 11, 12 (static counts, some bodies run on the simulator): `s10.jsonl` 14f6e6bbddc102104255e3041214b405ce78cbd5abe34a646a473a8b86c03cef; `s11.jsonl` 114bb53964236ba6bee9a5c3909b73dc8e5e3f494425cee7c6a3f42ba92b90de; `s12.jsonl` 3f2e09e77a5845965febdb4fde8336ef7118482a7617695b9d41c7ca9830d7de
  - Gray-order model scores for the K = 11 and K = 12 extension: `k11_model.jsonl` 4fdf2f2e07b975cab12be37e28f19bad4fbfccc04d01045d7ffde6db8e9905a6; `k12_model.jsonl` 552898f19aa06c3ec7da5a7d4502580ebe1172cbd966f678e68b0d849d8f2266
  - memo statistics and kept-plane variants (not adopted): `memo_an10.out` 70f74476d0186f467312b16c0137df51c758e1f6099443bf5670592b1cd049b3; `memo2_an10.out` 6fb4708a2de8f16c656e6fa9cd84b102460f57999fd8e9257c71134572550b4b; `kv_single.jsonl` 875dc8333d802c36f53e4015246e9c386ef9f7fd2da3ed3b9875036ac771deca; `kv_rm1.jsonl` 7a7396131086019d5f823413e6ff3027f606a5054840f0fe2ba10a5bae154833
  - every file of the prototype folder (97 files: the scripts and every saved output and log of the runs above and of their smaller trial runs, including the kept-plane variants `kv.py`, `kv2.py`, `cone.py`, the candidate-path prototypes `lastwriter.py`, `project.py`, the allowance and claim-format ledgers `ntight.py`, `final_proj.py`, `proj2.py`, and the control prototype `ctl_proto.py`, whose console outputs were not saved): SHA-256 of the sorted list of (file, SHA-256): e05fa43efec58d877b8f4ff2f507cba8cee0c424c1fa213d4d6ce682353c9a09
- **bs7's audits** (bs7's mutations of the parts unchanged here: rounds
  4-6, the transpose, the table, the candidate path) were run on bs7's
  program; Section 10.1 of bs7. df0136bc's mutations of the views and the
  bs9 memo (Section 10.1 of df0136bc) apply to the unchanged parts.

### 10.2 Declared experiments (organizer-executed, `python-message-pairs-v1`)

All four experiments run `experiments/s3r6_bitslice_birthday.py`, unchanged
from bs7 (same bytes, same SHA-256). It mirrors bs7's counted program; this
package changes only how the program stores O2P (views, Lemma 13), reuses round-3
chi outputs and chi terms (Lemmas 14 and 14'), lays out its control (Section 5.2),
in which order a batch enumerates z (Lemma 12) and how many batches run (NB),
none of which changes a key or the definition of a message:
- structured 128-byte prefixes (Section 2) derived from the organizer seed
  with SHA-256 (label `s3r6-ls128-v1`), z in lanes 4 and 14;
- per-batch A2 (polarity pi) and O2P, and Gray updates that flip the read
  support words and XOR the fixed patch expressions into the 499 O2P words;
- lane-complement rounds 3-5 with theta at the store and the start planes
  (10, 61, 34) stored raw and fixed on read;
- rounds 4 and 5 computed in full, after which every word and fix column
  outside the Lemma 10 cone (1,363 and 175 words) is replaced by an
  unrelated constant;
- the last round on the 35 kept planes at key rows 4k + x in the KEYMASK
  encoding;
- the rotating-frame zero-row transpose in the 16-row layout (asserted at
  3,418 operations) and the processing order decode_slot(q).

The manifest's scope text is bs7's and is kept byte-identical so that its
hash and every listed run stay valid. Its "counted program's order" and
"proof.md Sections 4-5" refer to bs7's program (7e40f784): the evaluator
enumerates z = gray(t) (high-z: gray(t) << 25) and does not use this
program's views, memos, control or ORDER. The message set and every key are the
same in any order (Lemma 12; Section 7), and the self-test checks this
program's keys against `verifier/keccak.py` directly.

Every digest bit used for matching comes from this evaluator. The script
maps the digest mask to key rows and refuses a mask bit outside the kept
planes. It uses only the per-trial seeds of the request, so an organizer
holdout nonce changes every trial.

**Self-checks** (any failure aborts the run):
- the whole 140-bit key of each trial's first 4 messages, and of its first
  message at each step t = 2^i, against an independent direct sponge;
- for every z-bit used, A2(e_j) XOR A2(0), computed from scratch, is
  all-ones exactly on the 22 support words;
- the maintained A2 (read words) and O2P against a rebuild from the
  prefixes after the batch;
- at every step, the zero key rows, and the transpose against the full
  6-op transpose;
- every key of the batch through the tagged-id table with pair ids, with
  adversarial never-written words (1/16 carry the run's TAG, so the
  verify-and-continue path must be taken). Every table word must name a
  pair containing a message whose key is its address.

Sabotage (in memory, the script unchanged): dropping one patched word,
corrupting one patch constant, or storing message numbers instead of pair
ids in the table makes the run fail; dropping any one of the 8 flip words
of z-bits 0..4 that a patch of a used z-bit reads also fails (spread
layout; run S2, added after S, Section 10.3). Dropping a flip word that no
used z-bit reads changes no key and is not detected, as expected.

**Scale.** N_t = 2^9 and an 18-bit mask give N_t^2/2^18 = 1, close to
N^2/2^256 = 0.9904 (the manifest's "the same ratio" was written for
255 * 2^80 batches, (255/256)^2 = 0.9922). The uniform-model success
probability is 0.393074 (100.6 +- 7.8 per 256 trials). Layouts:
- `k6r6-ls128-full-width`: 256 groups x 2;
- `k6r6-ls128-spread`: 16 x 32;
- `k6r6-ls128-single-group`: 1 x 512;
- `k6r6-ls128-high-z`: 4 x 128 with z = gray(t) << 25.

The layouts and masks are bs4's (949c283b), unchanged; they were fixed for
a different message family, before this family existed in our work.

### 10.3 Run selection (H1(b)) and participant runs (participant runs are untrusted)

**What a reviewer can check without trusting us.**
1. The organizer-executed configuration (the four layouts, the four 18-bit
   masks, N_t = 2^9, 256 trials, per-trial seeds derived by the runner) is
   the one of our public packages 949c283b and 5e73af65 (and 64ee9000),
   unchanged. Only the message family and the evaluator changed.
2. The family is 5kyguy's (6e715d9a), fixed outside this package. Their
   organizer trials of it were not used to choose anything here.
3. The only parameters chosen for this package are the storage polarity
   pi (deterministic cost rule `choose_polarity` in Appendix A `gen.py`),
   the start planes (10, 61, 34) (objective: worst compiled leaf of bs7),
   the prefix seed label `s3r6-ls128-v1` (fixed in the frozen script), and,
   new since bs7, K = 10 (objective: the exact count T of earlier builds),
   ORDER (output of the shipped `ordergen.py`, a static operation-count
   model), the memo2 rules and threshold (static operation counts) and the
   batch count NB (the fixed success-bound rule of `cert.py`, with the
   target 0.3905 chosen by us from cost ledgers, without any trial). No
   objective
   reads a digest bit or a masked-collision statistic. **No run of the
   experiment script was made to build or choose anything in this
   package.** The list below is every run of the script by us or by agents
   working for us up to bs10's run-list freeze, 2026-10-07T21:46Z:
   bs7's runs, bs7's review committee runs, the runs of the reviewers of
   an unsubmitted intermediate revision (2026-10-07, 17:38-17:45Z), and
   one replay by the pre-submission reviewers of df0136bc (20:56Z) and the
   `--local` runs Q0 and Q by a review after its submission (21:03-21:04Z). This
   revision (bs11) made no run of the script: our run records from that
   freeze to this revision's run-list freeze (2026-10-08T16:25Z) show
   none by us or by agents working for us (the runs of Section 10.1
   execute the counted program only; it and our prototypes import the
   script's geometry as a module, as `ref.py` does, which runs no
   trial). Runs after this freeze will be listed in later revisions.
4. The organizer's public-seed run of this package (no nonce) should show:
   - `manifest_sha256` =
     `6955f6aedaf54f53f722075f1c499e19900957d8a5c593c3915f26af67cb6fbe`
     (canonical manifest; the file bytes hash to
     `6fb0a610bb703bc1f6f0f2812e432417adecda9793500905847b10ccb85ce9e1`);
   - `sources[0].sha256` =
     `c5d0dd9b4300ec29eff8aced9e0873c5aab3cc0f9298918e8b448162c17d5edb`;
   - `full_report_sha256` =
     `d160f2ea8ffc5f9cdbeceb560805422e5930a0e008e9cd5b0d2b2eb58d05fa44`;
   - successes 91 / 99 / 105 / 105 (full-width / spread / single-group /
     high-z),

   which is our R1 below. For bs6 (64ee9000) the same local replay gave
   exactly the organizer's report hash
   `83e80e0ecce7637c8239a54f80f24303757b845f6233d68fc8548ec5a635584f`
   (run 37598515389), so our runner replays reproduce the organizer's
   executor on the public seed (that run had no holdout nonce; nonce runs
   use the same runner code). R1's intervals are therefore
   intervals on counts that the organizer report establishes.
5. A fresh organizer holdout nonce (`HASHSMASH_EXPERIMENT_HOLDOUT_NONCE`)
   tests the script without any change to it.

**Our protocol.** Before our first trial of this family we froze the script
and the manifest (hashes above) and recorded a pre-registration
(Appendix B, verbatim; SHA-256
`931e662ae5f21abafca60fe829dd769ec1df36f82a6188138fdbb4c9a09ead54`,
created 2026-10-07T09:50:01Z) listing the runs, the seed labels, the
analysis and the commitment that nothing is changed, repeated or dropped
after a result. Before it, only exactness checks without trials were run
(evalcheck a and b, 59,840 + 16,320 = 76,160 keys; Appendix B). The
nonces of R2-R4 were drawn with
`secrets.token_hex(16)` after the pre-registration hash was recorded. Runs
used the repository's `experiments/runner.py` (Docker replaced by a local
`python3 -I` subprocess) or the script's `--local` mode. The self-tests of
Appendix A import the script's geometry but run no trial.

**Every run of the script**, in time order (2026-10-07, UTC):
- R1 (09:50): runner, public seed `hashsmash-public-seed-v1`, no nonce,
  Python 3.9;
- R2-R4 (09:51-09:53): the same with participant nonces (ours, drawn after
  the pre-registration hash was recorded; not organizer holdout nonces)
  `bd46009ebe3e0b094c616228743f412c`, `24ddca750d9cab391425191615a7a8c5`,
  `817e871f5368158322f2f79815bd8c96`;
- R5 (09:54-09:56): `--local`, 48 chunks x 256 trials per layout (labels
  `v7stat-<layout>-c<k>`);
- S (09:56): pre-registered sabotage run (16 trials per case; only caught /
  not caught is used);
- S2 (09:57): **added after S, not pre-registered.** S had dropped a flip
  word that no used z-bit reads, which changes no key; S2 drops each of the
  8 flip words that a used z-bit reads (all caught). Only caught / not
  caught is used, no statistic;
- **after the build, by our review committee (not in the pre-registered
  analysis):** two public-seed replays on Python 3.12.14 (about 10:15 and
  10:16:51), each reproducing R1's report hash exactly (not new samples),
  and C2 (10:17:57), a participant-nonce run with nonce
  `bc71146c783d88db95d1c7ec012fc7f8` drawn at 10:17:39 (report
  `7274c95bd11e489eba8e089faa081514d172f5d89f7e5a3113d57465d6b55f26`);
- **after the build, by the reviewers of an unsubmitted intermediate
  revision of this package (not pre-registered; same script and manifest,
  runner with Docker replaced by a local subprocess; times are completion
  times):** V0 (17:38:46), a public-seed replay reproducing R1's report
  hash `d160f2ea...` exactly (not a new sample); V1-V3 (17:40:43,
  17:41:20, 17:41:58), participant nonces
  `9e9e7e8227618bbd715e250f52498c51`, `1837e091bff62f7f9af0d61183bcaa1b`,
  `1202ae306ce92dad543be11ccf1e5495` (reports below); and replays that are not new
  samples: the public-seed single-group request executed directly through
  the script (17:45:10; output byte-identical to R1's) and seven R5
  `--local` chunks (reported by the reviewers as identical to R5's);
- **after df0136bc's files were frozen (20:51Z) and before its submission
  (20:57:14Z), by its pre-submission reviewers (not pre-registered; not
  listed in df0136bc):** J0 (20:56:26-20:56:47Z), a runner replay of the
  public seed with no nonce (Docker replaced by a local subprocess,
  Python 3.9.6), report
  `d160f2ea8ffc5f9cdbeceb560805422e5930a0e008e9cd5b0d2b2eb58d05fa44`
  = R1 exactly, 91 / 99 / 105 / 105 (not a new sample);
- **after df0136bc's submission, by a review of the submitted package
  made for us (not pre-registered; `--local` mode, Python 3.9.6; outputs
  as printed in that reviewer's session record, not kept as files):**
  Q0 (21:03:45Z) `--local k6r6-ls128-full-width 32 rev-bs9-q3`: 12 / 32,
  masked pairs 15 (squares 21); its 32 seeds are those of the first 32
  trials of Q's full-width run, so it is not an independent sample. Q
  (21:03:51-21:04:03Z) `--local LAYOUT 256 rev-bs9-q3` for the four
  layouts: 112 / 108 / 103 / 95 of 256, masked pairs 148 / 137 / 133 / 128
  (squares 236 / 203 / 195 / 210). An earlier attempt wrapped in
  `timeout` did not start (command not found).

Full report hashes of the runner runs:
- R1 and J0 `d160f2ea8ffc5f9cdbeceb560805422e5930a0e008e9cd5b0d2b2eb58d05fa44`;
- R2 `9ea9962edf31d43056178427a23ff323c18727ab828e38100ca86cb72308e333`;
- R3 `b19d86098f628a9140d5b216537b2ed80168cf961bc966cc861efb506f01a13d`;
- R4 `9030dd7df63d7869cb71c72a2b13bb5cdec9a13dc24693e15c4731789533f0a3`;
- C2 `7274c95bd11e489eba8e089faa081514d172f5d89f7e5a3113d57465d6b55f26`;
- V1 `0cabb1102c7113621d7cceaad76b5b0153f300473c2e13092615bc8ec927ecd3`;
- V2 `39b6850ef8475593646c6547f6f23d549e60caf60806581a3f79b0f68a9203e8`;
- V3 `0d404654f7f57913288844e7c2ef77a0049e98ddbd852405bb66a1d858d25ee1`.

Our run records (every report and log of our build and review
directories, and the session records of the agents working for us,
scanned again at the freeze, 2026-10-07T21:46Z) show no other run of the
script by us or by agents working for us.

**Replays.** The two public-seed replays after the build, V0, the
single-group request, the seven R5 chunks and J0 repeat R1 or R5
byte-identically to check reproducibility, and Q's first 32 full-width
trials use Q0's seeds. Literally they depart from
Appendix B's wording "no run is repeated"; they are disclosed here.
None is a new sample and none could select an outcome: each reproduced
an output already listed, and no sampled run (R1-R4, R5, C2, V1-V3, Q) was
repeated with a different outcome or dropped.

Each runner run executed every experiment twice with byte-identical output.
No self-check failed and no full collision occurred. Peak resident memory
was at most 109 MiB (single-group: 101 MiB under Python 3.9, 107-109 MiB
under 3.12.14, macOS `ru_maxrss`); bs6's script, with the same table
logic, measured 108.7 MiB the same way and completed in the organizer's
128 MiB container. The slowest execution took 3.5 s unloaded (8.8 s on a
heavily loaded machine).

**Results** (successes / 256 unless stated; uniform model 0.393074):

| layout | R1 public | R2 | R3 | R4 | R5 local (/12,288) | C2 (post) | pooled R1-R5 (/13,312), z | pooled R1-R5 + C2 (/13,568), z | masked pairs R1-R5: ratio, var/mean |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| full-width | 91 | 113 | 105 | 96 | 4,845 | 93 | 5,250, +0.31 | 5,343, +0.17 | 0.998, 0.989 |
| spread | 99 | 102 | 107 | 107 | 4,861 | 86 | 5,276, +0.77 | 5,362, +0.51 | 1.019, 1.003 |
| single-group | 105 | 100 | 101 | 104 | 4,804 | 96 | 5,214, -0.33 | 5,310, -0.41 | 0.989, 0.989 |
| high-z | 105 | 101 | 92 | 104 | 4,849 | 105 | 5,251, +0.33 | 5,356, +0.40 | 1.003, 0.995 |

**Intervals and multiple testing.** p-values are exact two-sided binomial
(twice the smaller tail).
- Pre-registered analysis (R1-R5; 24 comparisons, 4 layouts x 5 runs + 4
  pooled): exact Clopper-Pearson intervals at the Bonferroni level
  1 - 0.05/24 contain 0.393074 in all 24; smallest p-value 0.130 (R2
  full-width).
- Runs R1-R5 and C2 (28 comparisons, 4 x 6 + 4 pooled): intervals at
  1 - 0.05/28 contain 0.393074 in all 28; smallest p-value 0.069 (C2
  spread), above the Bonferroni threshold 0.0018 and above 0.05
  unadjusted. Pooled 95% intervals: full-width [0.3856, 0.4021], spread
  [0.3870, 0.4035], single-group [0.3831, 0.3996], high-z [0.3865,
  0.4030].
- Masked pairs: 1.0022 +- 0.0061 times the uniform value 0.4990 over the
  53,248 pre-registered trials (variance/mean 0.994), 1.0010 over the
  54,272 trials of R1-R5 and C2.
- With the reviewers' runs (all sampled runs: R1-R5, C2, V1-V3; 40
  comparisons, 4 x 9 + 4 pooled): the Clopper-Pearson intervals at
  1 - 0.05/40 contain 0.393074 in all 40; smallest p-value still 0.069
  (C2 spread). V1-V3 gave 105 / 100 / 86 / 95, 106 / 94 / 107 / 90 and
  98 / 95 / 86 / 104 (full-width / spread / single-group / high-z).
  Pooled over 14,336 trials per layout: 5,652 / 5,651 / 5,589 / 5,645, z =
  +0.29 / +0.27 / -0.79 / +0.17 (p = 0.78 / 0.79 / 0.44 / 0.87); masked
  pairs 0.998 times uniform over those 57,344 trials.
- With the post-submission reviewer run Q (all sampled runs: R1-R5, C2,
  V1-V3, Q; 44 comparisons, 4 x 10 + 4 pooled): the Clopper-Pearson
  intervals at 1 - 0.05/44 contain 0.393074 in all 44; smallest p-value
  still 0.069 (C2 spread; also V1 and V3 single-group). Q alone: p =
  0.165 / 0.379 / 0.807 / 0.514, masked pairs 1.069 times uniform over its
  1,024 trials (z about +1.5). Pooled over 14,592 trials per layout:
  5,764 / 5,759 / 5,692 / 5,740, z = +0.48 / +0.39 / -0.74 / +0.07 (p =
  0.64 / 0.70 / 0.46 / 0.95); masked pairs 1.000 times uniform over all
  58,368 sampled trials.

The intervals assume independent trials: trials of one runner request
share batches but not bit positions (Section 10.2), and their seeds are
distinct SHA-256 outputs.

**What this does and does not show.** At this scale a deviation of the
success probability by more than about 0.015 (pooled, per layout) would
likely have been visible; a deviation at the 0.0005 allowance of Section
7, or a 0.78% excess of key pairs at full scale, would not.

## 11. Memory

| array | 32-byte words | bytes |
| --- | --- | --- |
| S (tagged ids, at 0) | 2^140 | 2^145 |
| PREF (at 2^140 + 2^30; 4 words per group; reads from garbage ids stay below 2^140 + 2^30 + 2^98) | < 2^99 written | < 2^104 |
| views V (at 2^140 + 2^27; 2048 words per state, 358,840 maintained) | < 2^21 | < 2^26 |
| memo R3C (at 2^140 + 2^26; 5 words per row and output class) | < 2^21 | < 2^26 |
| memo R3T (at 2^140 + 2^29; 5 words per row and term class) | < 2^21 | < 2^26 |
| A2, O2P, ZT, patch cache, masks, state buffers, ROWS, CNT, save area (at 2^140 + k*2^20, k < 30) | < 2^18 | < 2^23 |
| code (2,069 bodies, setup, 256 candidate copies per body of < 200 instructions) | < 2^31 instructions | < 2^36 |

The whole data address span is below 2^140 + 2^99 words, so total
memory, address span included, is < 2^145.01 bytes; we claim 146.
Memory is reported only.

## 12. Limitations

- **H1 is a heuristic.** It extends the grouped structure from the tested
  scale (N_t = 2^9, 18-bit masks) to N = NB * 2^40 and the 256-bit
  digest. F2 and Y1 cannot be scaled down faithfully and are bounded only
  under H1. The 0.0005 allowance between the model value and the claimed
  0.39 is not statistically certified (neither was df0136bc's 0.00106).
- **Run selection.** H1(b) rests partly on facts a reviewer can check
  (unchanged organizer configuration, the externally fixed family,
  cost-only parameter choices in Appendix A, the R1 report hash that the
  organizer's own public-seed run should reproduce) and partly on our
  statement about our own runs, whose timing a reviewer cannot check
  (Appendix B); df0136bc's run list missed one exact replay made after
  its freeze, which Section 10.3 lists with a later local-mode review run.
  A holdout-nonce rerun by the organizer is the independent check.
- **Stronger within-group structure.** Round 1 is linear in z, with fixed
  group-independent differences (Lemmas 2-3). Five nonlinear chi layers
  follow. Within a group the digest has degree at most 32 in z; with 32 z
  bits, this gives no zero-sum on any affine subspace of z. Within-group
  pairs are a 2^-96 fraction of all pairs.
- **Source of the gain.** The gain comes from operation-level pricing. All
  executed work, including all memory traffic and every candidate
  verification, is charged.
- **Register assumption.** The 64-register machine is an assumption, and
  the program uses all 64. Section 9 gives stricter readings, all at most
  124.50052.
- **Candidate cap.** F4 is the most sensitive use of H1 (Section 7): the
  cap tolerates a relative excess of 2^-7 of E[Y1] over N^2/2^141, which
  the experiments do not certify.
- **Rounding slack.** At five decimals the slack is small: T / 2^32 may
  grow to 27,334.060 (Section 8). T is exact and reproducible.
- **Exact average, not a worst step.** The claim charges the exact operation
  count of every batch (a deterministic schedule). Single steps differ
  widely: the 2^-K fraction of high steps costs up to 376,557
  operations, the low steps 26,415..30,882.
- **Program size.** 2,069 straight-line bodies (generated, not
  hand-written); the self-test needs about 15 minutes with 6
  processes and at most 1.4 GiB of memory per process.
- **Self-test.** Appendix A is participant code; it is reproducible from
  the package but is not an organizer artifact. The experiment script is
  bs7's; its runs up to this revision's run-list freeze, including our
  reviewers' runs, are in Section 10.3.
- **Scope.** No sub-birthday attack, collision certificate or full-scale
  run is claimed.

## 13. Credit

- **Co-authors**, in the sense of Section 0:
  - **5kyguy** (6e715d9a: the 128-byte family with z in lanes 4 and 14,
    the per-branch-site candidate copies with a charged direct jump back,
    the program-generation allowance (2^50 in 6e715d9a), and shipping the counted
    program; 78676cf6: concurrent zero-row delta swaps, not used);
  - **Th0rgal** (4867f093: the linear-structure prefix on this track;
    76ccfa1c: the table builds on T2, T3 subsumed by Lemma 11);
  - **jaazinn** (0a5b7ae8);
  - **may93182** (11c46f4d).
- **Credited:**
  - GordoAR (5dac3f95 and dcdd90ec: the five-decimal claim; e715ab73 and
    df2619d4: the integer-certificate format of Section 8; nothing else
    used);
  - Guo, Liu and Song (ASIACRYPT 2016), linear structures;
  - tekkac (b001199a, f58275ef);
  - ercumentyildirim (c7fa1a56, 4c969300);
  - zeeshan8281 (cbf7998d, including the 255/256 budget of df0136bc);
  - mitchuski (02d6a703).

Errors are ours.

## Appendix A. The counted program (source)

These files are the counted program of Sections 4-5 and 10.1, exactly as
run by the self-test of A.1 (the compile pass, battery and mutations of
Section 10.1 ran on them before two comment-only edits and before
`selftest.py`'s EXPECT and `cert.py`'s default T were filled in, as listed
there). Python 3 standard library only; `ref.py`, `vkeccak.py` and
`ordergen.py` are byte-identical to df0136bc's, the other six differ.
Each block below is one file; its SHA-256 is in the marker line. Sizes
and roles:

- `ref.py` (197 bytes): adapter: the reference geometry is the shipped experiment script.
- `vkeccak.py` (132 bytes): adapter: the reference hash is the challenge verifier.
- `ir.py` (14361 bytes): builder, straight-line compiler (forwarding, interval colouring) and the counted simulator.
- `gen.py` (40629 bytes): generator of the bodies (patches, polarity, views, block memo and memo2, rounds 3-6, cones, transpose, table steps).
- `setup_gen.py` (9314 bytes): counted per-batch setup programs (prefixes, A2, O2P, maintained view words).
- `machine.py` (26888 bytes): memory layout, run harness, block-unrolled control, memo prefill, z tables, candidate path, reference checks.
- `selftest.py` (20010 bytes): self-test entry point (exact batch count T, control layout).
- `cert.py` (3326 bytes): the batch-count rule and the integer certificate of Section 8.
- `ordergen.py` (4706 bytes): the deterministic generator of the Gray order ORDER (Lemma 12; df0136bc's file, unchanged; not run by the self-test).

Together 119563 bytes. The experiment script `experiments/s3r6_bitslice_birthday.py`
(SHA-256 `c5d0dd9b4300ec29eff8aced9e0873c5aab3cc0f9298918e8b448162c17d5edb`, unchanged from bs7)
is the tenth file: `ref.py` imports its geometry, and `selftest.py`
asserts that the generator's storage polarity equals its `PI`.

### A.0 Extraction and self-test

From the repository root, with Python 3 (about 15 minutes with 6
processes on our machine; `selftest.py`'s docstring gives a conservative
25-40 minutes and ~3 GiB per process; set NPROC to change; at most 1.4 GiB of memory per process, so
choose NPROC to fit the available memory, e.g. at most a quarter of it in
GiB; the self-test reads `verifier/keccak.py` from the given root):

```sh
mkdir -p /tmp/s3prog && python3 - <<'EOF'
import hashlib, re
C = "lanes/exploratory/candidates/sha3-256-r6/"
t = open(C + "proof.md").read()
n = 0
for name, sha, body in re.findall(r"<!-- file: (\S+) sha256=(\w+) -->\n```python\n(.*?)```\n", t, re.S):
    assert hashlib.sha256(body.encode()).hexdigest() == sha, name
    open("/tmp/s3prog/" + name, "w").write(body)
    n += 1
assert n == 9
src = open(C + "experiments/s3r6_bitslice_birthday.py", "rb").read()
open("/tmp/s3prog/s3r6_bitslice_birthday.py", "wb").write(src)
EOF
NPROC=6 python3 /tmp/s3prog/selftest.py .
python3 /tmp/s3prog/cert.py 117398575636479
```

### A.1 Self-test output of our run

```text
geometry: 22-word supports, 499 patched words, 975 read words, flips 3..10, |pi| = 359; Gray order [25, 8, 21, 10, 28, 15, 30, 17, 4, 12, 19, 27, 6, 26, 1, 14, 13, 24, 7, 18, 3, 31, 9, 5, 20, 11, 16, 22, 23, 2, 0, 29]; K = 10, 1023 views of 499..1533 words, 358840 maintained view words (memo2) (16s)
control: block-unrolled layout executes the bodies (ctz t, gray(t) mod 2^K) in step order for batches of 2^11, 2^12, 2^15 steps; control count = formula; per batch 29360123 control ops
static body counts: t0 31491; leaf 0: 26415..30882 (1024 bodies); leaf 1: 26439..30629 (512 bodies); leaf 2: 26459..30324 (256 bodies); leaf 3: 26564..30563 (128 bodies); leaf 4: 26626..30589 (64 bodies); leaf 5: 26785..30202 (32 bodies); leaf 6: 27235..30551 (16 bodies); leaf 7: 27636..30147 (8 bodies); leaf 8: 28657..30045 (4 bodies); leaf 9: 30085..30085 (2 bodies); leaf 10: 301235; leaf 11: 341912; leaf 12: 316912; leaf 13: 334260; leaf 14: 326501; leaf 15: 343685; leaf 16: 330330; leaf 17: 351330; leaf 18: 350106; leaf 19: 342237; leaf 20: 355329; leaf 21: 350498; leaf 22: 368916; leaf 23: 369565; leaf 24: 352729; leaf 25: 372915; leaf 26: 345512; leaf 27: 371753; leaf 28: 376557; leaf 29: 360847; leaf 30: 369675; leaf 31: 371063
EXACT ops per batch T = 117398575636479; T / 2^32 = 27333.985929 ops per z-step; 2069 bodies, sha256 4c07e7bad4fcc77d9282c88f89f3e64f99af9b8cf88c54678403db8b66a4efc5 (732s)
each body: static table check (256 exact hot paths); run once on the counted simulator from a random state: 529664 keys equal key_of_digest(sha3_256(m, 6)); measured == control + static + jump; A2/O2P/views equal a rebuild (732s)
simulator: 120 consecutive steps from 3 starts (one a block start, no memo prefill), keys exact and A2/O2P/views equal a rebuild after each (899s)
candidates: replayed z-steps gave 2 x 256 genuine candidates with exact rebuilds; continue costs [111, 112, 119, 120] ops, (3 units each), forced halt 80 ops
batch setup: 2383931 ops, 62 registers, equal to the reference incl. the maintained words of the 1023 views (913s)
run setup: z tables ZT, 393213 ops, equal to zperm
{"T": 117398575636479, "ops_per_z_step": 27333.985929488903, "t0": 31491, "bodies": 2069, "bodies_sha256": "4c07e7bad4fcc77d9282c88f89f3e64f99af9b8cf88c54678403db8b66a4efc5", "cand_ops_max": 120, "halt_ops": 80, "setup_ops": 2383931, "zt_ops": 393213}
      913.16 real      4411.72 user        34.01 sys
          1457471488  maximum resident set size
                   0  average shared memory size
                   0  average unshared data size
                   0  average unshared stack size
             2479245  page reclaims
                 120  page faults
                   0  swaps
                   0  block input operations
                   0  block output operations
                   0  messages sent
                   0  messages received
                   0  signals received
                3507  voluntary context switches
             5892728  involuntary context switches
       5114883986400  instructions retired
        873875480101  cycles elapsed
          1361102192  peak memory footprint
exit 0
```

The final JSON line is the machine-readable result: `T` is the exact
operation count of one batch charged in Section 8, and `bodies_sha256`
identifies the compiled bodies. A rerun prints the same output up to
the timings in parentheses. `cert.py 117398575636479` printed:

```text
NB = 307990341830783024002353940 batches (0.99517047 * 2^88), N = NB * 2^40 = 2^127.993016; success bound under H1 0.3905000000
T 117398575636479 ops/z-step 27333.985929 claim 124.07261 log2 total 124.072606
slack: T / 2^32 up to 27334.0604 ops/z-step, or up to 152 operations per candidate
```

### A.2 Source files

<!-- file: ref.py sha256=8a643599f0b7da540be2e9ebf0a6bb99c3756df36d6e74f633aef6ccfdb1432c -->
```python
"""The counted program's reference geometry is the shipped experiment script."""
import s3r6_bitslice_birthday as _e
globals().update({k: v for k, v in vars(_e).items() if not k.startswith('__')})
```

<!-- file: vkeccak.py sha256=6a875cdc5231175db1c9947a28bcce949d111ec7428c296258318c8712364318 -->
```python
"""The reference hash: the challenge verifier (REPO_ROOT/verifier/keccak.py)."""
from verifier.keccak import sha3_256  # noqa: F401
```

<!-- file: ir.py sha256=2e857241f66a93045cb566b7147bba5474a34b7f7f9acc7cafde47f376039cd0 -->
```python
"""SSA IR, straight-line compiler (store-to-load forwarding under a register
budget, scratch dead-store elimination, interval-colouring register
allocation) and a counted 256-bit word-RAM simulator with 64 registers.

Instruction tuple: (op, dst, a, b, imm)
  ld   dst <- MEM[imm]            imm = (array, index): constant address
  st   MEM[imm] <- a
  ldr  dst <- MEM[a]              register-addressed (table)
  str  MEM[a] <- b
  xor/and/or dst <- a op b ; not dst <- ~a
  rot  dst <- rotl256(a, imm)
  andi dst <- a & imm ; cmplt dst <- (a < imm) ; cmpeq dst <- (a == b)
  add  dst <- a + imm (mod 2^256)
  br   if a: candidate path (out of line), then fall through
Persistent registers 'S' (block counter) and 'C' (table word) live in physical
registers 62 and 63; all other values get registers 0..61.
"""
import heapq

W = (1 << 256) - 1
NREG = 62
PERSIST = ('S', 'C')
SCRATCH = {'ROWIN', 'TR', 'C1S', 'D1', 'O1', 'C2', 'A2P', 'CSS', 'FIXS', 'B3', 'B4', 'B5', 'FIX3', 'FIX4', 'FIX5', 'CS3', 'CS4', 'CS5', 'DL', 'ROWS', 'LR'}


class Bld:
    def __init__(self):
        self.ins = []
        self.tags = []
        self.tag = None
        self.n = 0

    def emit(self, op, a=None, b=None, imm=None, dst=True):
        d = None
        if dst:
            d = self.n
            self.n += 1
        self.ins.append((op, d, a, b, imm))
        self.tags.append(self.tag)
        return d

    def ld(self, arr, i):
        return self.emit('ld', imm=(arr, i))

    def st(self, arr, i, v):
        self.emit('st', a=v, imm=(arr, i), dst=False)

    def xor(self, a, b):
        return self.emit('xor', a, b)

    def and_(self, a, b):
        return self.emit('and', a, b)

    def or_(self, a, b):
        return self.emit('or', a, b)

    def not_(self, a):
        return self.emit('not', a)

    def rot(self, a, k):
        k %= 256
        assert k
        return self.emit('rot', a, imm=k)


def _uses(ins):
    op, d, a, b, imm = ins
    u = []
    if a is not None:
        u.append(a)
    if b is not None:
        u.append(b)
    return u


class SegTree:
    """range add, range max over [0, n)."""

    def __init__(self, vals):
        n = 1
        while n < len(vals):
            n *= 2
        self.n = n
        self.mx = [0] * (2 * n)
        self.lz = [0] * (2 * n)
        for i, v in enumerate(vals):
            self.mx[n + i] = v
        for i in range(n - 1, 0, -1):
            self.mx[i] = max(self.mx[2 * i], self.mx[2 * i + 1])

    def add(self, l, r, v, node=1, nl=0, nr=None):
        if nr is None:
            nr = self.n
        if r <= nl or nr <= l or l >= r:
            return
        if l <= nl and nr <= r:
            self.mx[node] += v
            self.lz[node] += v
            return
        m = (nl + nr) // 2
        self.add(l, r, v, 2 * node, nl, m)
        self.add(l, r, v, 2 * node + 1, m, nr)
        self.mx[node] = max(self.mx[2 * node], self.mx[2 * node + 1]) + self.lz[node]

    def query(self, l, r, node=1, nl=0, nr=None):
        if nr is None:
            nr = self.n
        if r <= nl or nr <= l or l >= r:
            return -10 ** 9
        if l <= nl and nr <= r:
            return self.mx[node]
        m = (nl + nr) // 2
        return max(self.query(l, r, 2 * node, nl, m), self.query(l, r, 2 * node + 1, m, nr)) + self.lz[node]


def compile_block(ins, tags=None, nreg=NREG, forward=True):
    """Forward loads, drop dead scratch stores, allocate registers.
    Returns (physical instruction list, high-water register count)."""
    ins = list(ins)
    n = len(ins)
    parent = {}

    def find(v):
        while v in parent and parent[v] != v:
            nxt = parent[v]
            if nxt in parent and parent[nxt] != nxt:
                parent[v] = parent[nxt]
            v = nxt
        return v
    # memval candidates (fixed by program order)
    cand = []           # (p, prev value)
    last = {}
    for p, (op, d, a, b, imm) in enumerate(ins):
        if op == 'ld':
            if imm in last:
                cand.append((p, last[imm]))
            last[imm] = d
        elif op == 'st':
            last[imm] = a
    alive = [True] * n
    forwarded = set()

    def intervals():
        dpos, end = {}, {}
        for p in range(n):
            if not alive[p]:
                continue
            op, d, a, b, imm = ins[p]
            for u in _uses(ins[p]):
                if u in PERSIST:
                    continue
                r = find(u)
                if end.get(r, -1) < p:
                    end[r] = p
            if d is not None and d not in PERSIST and find(d) == d:
                dpos[d] = p
        iv = {}
        for v, p in dpos.items():
            iv[v] = [p, max(end.get(v, p + 1), p + 1)]
        return iv

    # store groups: loads between a store and the next store to the same address
    grp = {}
    cur = {}
    for p, (op, d, a_, b_, imm) in enumerate(ins):
        if op == 'st':
            cur[imm] = p
        elif op == 'ld' and imm in cur:
            grp.setdefault(cur[imm], []).append(p)
    gsize = {}
    for sp, lds in grp.items():
        for p in lds:
            gsize[p] = len(lds) if ins[sp][4][0] in SCRATCH else 0
    while forward:
        changed = False
        # 1. free forwards (the previous value is still live at the load)
        iv = intervals()
        for p, pv in cand:
            if p in forwarded:
                continue
            r = find(pv)
            l = ins[p][1]
            if iv[r][1] > p:
                iv[r][1] = max(iv[r][1], iv[l][1])
                parent[l] = r
                del iv[l]
                alive[p] = False
                forwarded.add(p)
                changed = True
        # 2. max-weight forwards under the register budget (min-cost flow)
        iv = intervals()
        diff = [0] * (n + 1)
        for s_, e_ in iv.values():
            diff[s_] += 1
            diff[e_] -= 1
        pres, c = [], 0
        for p in range(n):
            c += diff[p]
            pres.append(c)
        if max(pres) > nreg:
            raise RuntimeError("baseline pressure %d exceeds the budget" % max(pres))
        items = []
        for p, pv in cand:
            if p in forwarded:
                continue
            r = find(pv)
            ev = iv[r][1]
            w = 1000 + (1000 // gsize[p] if gsize.get(p) else 0)
            items.append((ev, p, w, pv))
        sel = select_intervals(items, pres, n, nreg)
        for ev, p, w, pv in sel:
            r = find(pv)
            l = ins[p][1]
            parent[l] = r
            alive[p] = False
            forwarded.add(p)
            changed = True
        # 3. dead scratch stores
        nextld = {}
        for p in range(n - 1, -1, -1):
            op, d, a_, b_, imm = ins[p]
            if op == 'ld' and alive[p]:
                nextld[imm] = True
            elif op == 'st':
                if alive[p] and imm[0] in SCRATCH and not nextld.get(imm, False):
                    alive[p] = False
                    changed = True
                nextld[imm] = False
        if not changed:
            break
    # rewrite
    out = []
    otags = []
    for p in range(n):
        if not alive[p]:
            continue
        op, d, a, b, imm = ins[p]
        a2 = a if a in PERSIST or a is None else find(a)
        b2 = b if b in PERSIST or b is None else find(b)
        out.append((op, d, a2, b2, imm))
        otags.append(tags[p] if tags else None)
    # check: every scratch load is preceded by a live store in the block
    written = set()
    for op, d, a, b, imm in out:
        if op == 'st':
            written.add(imm)
        elif op == 'ld' and imm[0] in SCRATCH and imm not in written:
            raise RuntimeError("scratch load before store: %r" % (imm,))
    code, hw = allocate(out, nreg)
    return code, hw, otags


def select_intervals(items, pres, n, nreg):
    """Max-weight subset of intervals [a, b) (items (a, b, w, key)) such that
    pres[x] + #chosen covering x <= nreg everywhere (exact, min-cost flow)."""
    items = [it for it in items if it[0] < it[1]]
    if not items:
        return []
    coords = sorted({0, n} | {it[0] for it in items} | {it[1] for it in items})
    idx = {c: i for i, c in enumerate(coords)}
    m = len(coords)
    INF = float('inf')
    to, cap, cost, adj = [], [], [], [[] for _ in range(m)]

    def add(u, v, c, w):
        adj[u].append(len(to)); to.append(v); cap.append(c); cost.append(w)
        adj[v].append(len(to)); to.append(u); cap.append(0); cost.append(-w)
    M = 10 ** 9
    for i in range(m - 1):
        bm = max(pres[coords[i]:coords[i + 1]])
        add(i, i + 1, bm, -M)
        add(i, i + 1, nreg - bm, 0)
    ie = []
    for it in items:
        ie.append(len(to))
        add(idx[it[0]], idx[it[1]], 1, -it[2])
    # potentials: DAG shortest paths (all original edges go forward)
    pot = [INF] * m
    pot[0] = 0
    for u in range(m):
        if pot[u] == INF:
            continue
        for e in adj[u]:
            if cap[e] > 0 and pot[u] + cost[e] < pot[to[e]]:
                pot[to[e]] = pot[u] + cost[e]
    flow = 0
    while flow < nreg:
        dist = [INF] * m
        prev = [-1] * m
        dist[0] = 0
        h = [(0, 0)]
        while h:
            d, u = heapq.heappop(h)
            if d > dist[u]:
                continue
            pu = pot[u]
            for e in adj[u]:
                if cap[e] > 0:
                    v = to[e]
                    nd = d + cost[e] + pu - pot[v]
                    if nd < dist[v]:
                        dist[v] = nd
                        prev[v] = e
                        heapq.heappush(h, (nd, v))
        if dist[m - 1] == INF:
            break
        for v in range(m):
            if dist[v] < INF:
                pot[v] += dist[v]
        f = nreg - flow
        v = m - 1
        while v != 0:
            e = prev[v]
            f = min(f, cap[e])
            v = to[e ^ 1]
        v = m - 1
        while v != 0:
            e = prev[v]
            cap[e] -= f
            cap[e ^ 1] += f
            v = to[e ^ 1]
        flow += f
    return [it for it, e in zip(items, ie) if cap[e] == 0]


def allocate(ins, nreg):
    n = len(ins)
    dpos, end = {}, {}
    for p, x in enumerate(ins):
        for u in _uses(x):
            if u in PERSIST:
                continue
            end[u] = p
        d = x[1]
        if d is not None and d not in PERSIST:
            if d in dpos:
                raise RuntimeError("SSA violated")
            dpos[d] = p
    starts = sorted((p, v) for v, p in dpos.items())
    free = list(range(nreg))[::-1]
    import heapq as hq
    act = []
    reg = {}
    hw = 0
    for p, v in starts:
        e = max(end.get(v, p + 1), p + 1)
        while act and act[0][0] <= p:
            _, r = hq.heappop(act)
            free.append(r)
        if not free:
            raise RuntimeError("register budget exceeded at %d" % p)
        r = free.pop()
        reg[v] = r
        hq.heappush(act, (e, r))
        hw = max(hw, len(act))
    phys = {'S': 62, 'C': 63}

    def R(v):
        if v is None:
            return None
        if v in phys:
            return phys[v]
        return reg[v]
    out = [(op, R(d), R(a), R(b), imm) for op, d, a, b, imm in ins]
    return out, hw


class Machine:
    """Counted simulator: 64 registers of 256 bits, word memory (dict)."""

    def __init__(self, layout):
        self.reg = [None] * 64
        self.mem = {}
        self.layout = layout      # array name -> base address
        self.count = 0
        self.hist = {}
        self.cand_hook = None
        self.units = 0

    def mem_get(self, a):
        if a not in self.mem:
            import random
            self.mem[a] = random.Random(a).getrandbits(256)
        return self.mem[a]

    def addr(self, imm):
        return self.layout[imm[0]] + imm[1]

    def run(self, code):
        reg, mem = self.reg, self.mem
        cnt = 0
        hist = self.hist
        for op, d, a, b, imm in code:
            cnt += 1
            hist[op] = hist.get(op, 0) + 1
            if op == 'ld':
                reg[d] = mem[self.addr(imm)]
            elif op == 'st':
                mem[self.addr(imm)] = reg[a]
            elif op == 'xor':
                reg[d] = reg[a] ^ reg[b]
            elif op == 'and':
                reg[d] = reg[a] & reg[b]
            elif op == 'or':
                reg[d] = reg[a] | reg[b]
            elif op == 'not':
                reg[d] = reg[a] ^ W
            elif op == 'rot':
                x = reg[a]
                reg[d] = ((x << imm) | (x >> (256 - imm))) & W
            elif op == 'ldr':
                reg[d] = self.load_table(reg[a]) if imm is None else self.mem_get(reg[a])
            elif op == 'str':
                if imm == 'mem':
                    mem[reg[a]] = reg[b]
                else:
                    self.store_table(reg[a], reg[b])
            elif op == 'cmplt':
                reg[d] = 1 if reg[a] < imm else 0
            elif op == 'add':
                reg[d] = (reg[a] + imm) & W
            elif op == 'br':
                if reg[a]:
                    self.count += cnt
                    cnt = 0
                    self.cand_hook(self, b, imm)
            elif op == 'shr':
                reg[d] = reg[a] >> imm
            elif op == 'shl':
                reg[d] = (reg[a] << imm) & W
            elif op == 'andi':
                reg[d] = reg[a] & imm
            elif op == 'addr':
                reg[d] = (reg[a] + reg[b]) & W
            elif op == 'cmpeq':
                reg[d] = 1 if reg[a] == reg[b] else 0
            elif op == 'rand':
                reg[d] = self.rng.getrandbits(256)
            elif op == 'xori':
                reg[d] = reg[a] ^ imm
            elif op == 'hash':
                cnt -= 1
                self.units += 1
                reg[d] = self.hashfn(reg[a], reg[b])
            elif op == 'hash4':
                cnt -= 1
                self.units += 1
                reg[d] = self.hashfn(*[reg[r] for r in imm])
            elif op == 'ldi':
                reg[d] = self.mem_get(self.layout[imm[0]] + imm[1])
            else:
                raise RuntimeError(op)
        self.count += cnt

    def load_table(self, k):
        return self.table_get(k)

    def store_table(self, k, v):
        self.table_put(k, v)
```

<!-- file: gen.py sha256=b8ab5bd48184e70093ca6970ffc9ab7b4980af4d79d073c0333a4204922c9455 -->
```python
"""Generator of the per-z-step straight-line program (one leaf per Gray column j).

Message set (linear structures, Guo-Liu-Song 2016; the 128-byte family with
z in lanes 4 and 14 is 5kyguy's, 6e715d9a): z is XORed into the low 32 bits
of lanes 4 and 14 (col = (4, 14)).  Each z-bit j then flips a fixed 22-word
set of A2 (round-1 output + round-2 theta), every word by all-ones, for every
group (proof Lemmas 1-3).  The reference geometry (rho, chi gate plans,
polarities, kept planes, transpose orders, start planes, cones) is imported
from the shipped experiment script through ref.py.

bs9: materialised Gray views (proof Lemma 13).  A2 and O2P are kept at the
"base" point (the low K bits of z replaced by 0; K = 10 in this package), and
for every s in 1..2^K - 1 the array Vs holds O2P at the point with low bits s, on the words VS[s]
where it can differ from the base.  A step whose Gray bit j < K changes only
the low bits: its body does no round-2 work and reads view s (s = the low
bits after the step).  A step with j >= K flips the A2 support of bit j and
patches the base and every maintained view word (merged into the round-3
reads where round 3 reads them).

bs11: memo2 (proof Lemma 14'; opts['memo2']; K = 10 as in bs9).  Within a block, raw
round-3 chi output X is also reloaded when its reduced class (the view
expressions of inputs X, X+1, X+2 with the all-ones term of input X removed)
occurred earlier, complemented when the all-ones flags differ; and the
nonlinear term NOT b AND c (in the polarity of the gate that computes it) is
stored keyed by the pair of expressions of inputs X+1, X+2, so that a later
first occurrence of the same pair computes out = a XOR term (Geometry.m2rows;
the maintained view words are Geometry.needed2).  The bodies are laid out in
chains with block-unrolled control (machine.control).
"""
import ref
from ref import (RHO, DIAG, KEEP, ROWOF, RC, W, solve_row, _rowq, P34, P5, Q3, _bsrc,
                 round_needs, STARTS, LASTPLAN, BLOCKS, KEYROWS, P1ORDER, P2ORDER, _par)
from ir import Bld

WT = -1     # the all-ones term in a patch expression
M2THR = 1   # memo2: store a nonlinear term when at least this many later first occurrences reuse it
_RC2 = {}


def solve_row_free(q, p, iota, outs, free):
    """As ref.solve_row, but complemented copies of inputs in `free` cost 0
    (their complement is already in a register).  Same exact gate plans."""
    key = (q, p, iota, tuple(outs), frozenset(free))
    if key in _RC2:
        return _RC2[key]
    import itertools
    qb = [(q >> k) & 1 for k in range(5)]
    pb_ = [(p >> k) & 1 for k in range(5)]
    best = None
    for Sm in range(32):
        S = [k for k in range(5) if (Sm >> k) & 1]
        cost = len([k for k in S if k not in free])
        plan = {}
        for X in outs:
            ib = iota if X == 0 else 0
            bo = None
            for ca, cb, cc in itertools.product((0, 1), repeat=3):
                if (ca and X not in S) or (cb and (X + 1) % 5 not in S) or (cc and (X + 2) % 5 not in S):
                    continue
                pa = qb[X] ^ ca
                pbb = qb[(X + 1) % 5] ^ cb
                pcc = qb[(X + 2) % 5] ^ cc
                if (pbb, pcc) == (1, 0):
                    gate, pT = "and", 0
                elif (pbb, pcc) == (0, 1):
                    gate, pT = "or", 1
                else:
                    continue
                on = int(pa ^ pT ^ ib != pb_[X])
                if bo is None or on < bo[0]:
                    bo = (on, (ca, cb, cc, gate, on))
            if bo is None:
                cost = 99
                break
            cost += bo[0]
            plan[X] = bo[1]
        if best is None or cost < best[0]:
            best = (cost, S, plan)
    _RC2[key] = best
    return best


def dst_of(L, b):
    """A2 word (L, b) -> round-2 chi position (X, Y, plane)."""
    x, y = L % 5, L // 5
    return y, (2 * x + 3 * y) % 5, (b + RHO[L]) % 64


def r1_flips(col, j):
    """Round-1 output bits flipped by z-bit j (structured prefix): the two
    z-carrying positions after rho/pi (their chi neighbours are constants)."""
    out = set()
    for L in (tuple(col) if isinstance(col, tuple) else (col, col + 5)):
        X, Y, p = dst_of(L, j)
        out.add((X + 5 * Y, p))
    return out


def a2_support(col, j):
    S = set(r1_flips(col, j))
    dC = {}
    for L, b in r1_flips(col, j):
        dC[(L % 5, b)] = dC.get((L % 5, b), 0) ^ 1
    for (x, b), v in dC.items():
        if v:
            for xx, bb in (((x + 1) % 5, b), ((x - 1) % 5, (b + 1) % 64)):
                for y in range(5):
                    S ^= {(xx + 5 * y, bb)}
    return S


def src_word(X, Y, bp):
    L, bs = _bsrc(X, Y, bp)
    return 64 * L + bs


def patch_exprs(col, j, flipfix=True):
    """O2P word index -> frozenset of terms (A2 word indices, WT); plus A2 flip
    set and A2 read set."""
    S = a2_support(col, j)
    flips = {64 * L + b for L, b in S}
    rows = {}
    for L, b in S:
        X, Y, p = dst_of(L, b)
        rows.setdefault((Y, p), set()).add(X)
    dout = {}
    reads = set()
    for (Y, p), Xs in rows.items():
        c = [1 if X in Xs else 0 for X in range(5)]
        for k in range(5):
            k1, k2 = (k + 1) % 5, (k + 2) % 5
            e = set()
            if c[k] ^ c[k2] ^ (c[k1] & c[k2]):
                e ^= {WT}
            if c[k2]:
                e ^= {src_word(k1, Y, p)}
            if c[k1]:
                e ^= {src_word(k2, Y, p)}
            reads |= {t for t in e if t != WT}
            if e:
                dout[(k, Y, p)] = frozenset(e)
    dC = {}
    for (x, Y, b), v in dout.items():
        dC[(x, b)] = dC.get((x, b), frozenset()) ^ v
    patch = {}
    for (x, Y, b), v in dout.items():
        patch[64 * (x + 5 * Y) + b] = v
    for (x, b), v in dC.items():
        if not v:
            continue
        for xx, bb in (((x + 1) % 5, b), ((x - 1) % 5, (b + 1) % 64)):
            for Y in range(5):
                w = 64 * (xx + 5 * Y) + bb
                patch[w] = patch.get(w, frozenset()) ^ v
    patch = {w: v for w, v in patch.items() if v}
    # the formulas use OLD A2 values; the program reads A2 after this leaf's
    # flips, so an old flipped word is (new word) XOR all-ones (flipfix=False:
    # the raw formula in old values)
    fixed = {}
    for w, v in patch.items():
        v = set(v)
        for t in list(v):
            if flipfix and t != WT and t in flips:
                v ^= {WT}
        fixed[w] = frozenset(v)
    patch = {w: v for w, v in fixed.items() if v}
    return patch, flips, reads


def _wcost(leaves, pi):
    worst = tot = 0
    for pe in leaves:
        ex = set()
        for e in pe.values():
            t = set(e)
            w = WT in t
            t.discard(WT)
            if not t:
                continue
            for a in t:
                if a in pi:
                    w = not w
            ex.add((frozenset(t), w))
        c = sum(1 for t, w in ex if w)
        worst = max(worst, c)
        tot += c
    return worst, tot


def choose_polarity(leaves):
    """A2 storage polarity pi (set of words stored complemented), chosen by
    deterministic local search to minimise complemented patch expressions."""
    words = sorted({t for pe in leaves for e in pe.values() for t in e if t != WT})
    pi = set()
    best = _wcost(leaves, pi)
    while True:
        improved = False
        for a in words:
            pi ^= {a}
            c = _wcost(leaves, pi)
            if c < best:
                best, improved = c, True
            else:
                pi ^= {a}
        if not improved:
            return frozenset(pi)


class Geometry:
    def __init__(self, col, prune_flips=True, polar=True, K=3, order=None):
        """order[j] = the z-bit flipped by Gray bit j (z = sum of 2^order[j] over the set
        bits j of gray(t)); leaf j patches z-bit order[j]."""
        self.col = col
        self.order = list(order) if order is not None else list(range(32))
        assert sorted(self.order) == list(range(32))
        self.P = [patch_exprs(col, self.order[j]) for j in range(32)]
        allreads = set().union(*[p[2] for p in self.P])
        self.flips = [sorted(p[1] & allreads) if prune_flips else sorted(p[1]) for p in self.P]
        self.pi = choose_polarity([p[0] for p in self.P]) if polar else frozenset()
        # A2 word a is stored as a ^ (a in pi) * all-ones: toggle WT per stored term
        newP = []
        for pe, fl, rd in self.P:
            q = {}
            for w, e in pe.items():
                e = set(e)
                for t in list(e):
                    if t != WT and t in self.pi:
                        e ^= {WT}
                q[w] = frozenset(e)
            newP.append(({w: e for w, e in q.items() if e}, fl, rd))
        self.P = newP
        # views (Lemma 13): VD[s][w] = terms (stored-A2 words at the base, WT) whose
        # XOR is O2P(low bits s) ^ O2P(base) at word w; VS[s] = its word set
        self.K = K
        self.sup = [frozenset(64 * L + b for L, b in a2_support(col, self.order[i])) for i in range(32)]
        raw = [patch_exprs(col, self.order[i], flipfix=False)[0] for i in range(K)]
        self.VD, self.VS = {}, {}
        itn = {}                            # equal expressions share one frozenset (memory only)

        def I(e):
            e = frozenset(e)
            return itn.setdefault(e, e)
        rawd = {0: {}}                      # O2P(low bits sv) ^ O2P(base), in plain A2 terms
        for sv in range(1, 1 << K):
            i = sv.bit_length() - 1         # raise the top bit last: path 0 -> sv ^ 2^i -> sv
            prev = sv ^ (1 << i)
            acc = dict(rawd[prev])
            for w, e in raw[i].items():
                e = set(e)                  # derivative along bit i at the point prev
                for t in list(e):
                    if t != WT:
                        for i2 in range(i):
                            if (prev >> i2) & 1 and t in self.sup[i2]:
                                e ^= {WT}
                acc[w] = I(set(acc.get(w, frozenset())) ^ e)
            acc = {w: e for w, e in acc.items() if e}
            rawd[sv] = acc
            d = {}
            for w, e in acc.items():
                e = set(e)
                for t in list(e):
                    if t != WT and t in self.pi:
                        e ^= {WT}
                if e:
                    d[w] = I(e)
            self.VD[sv] = d
            self.VS[sv] = frozenset(d)
        del rawd

    def needed(self):
        """VN[s]: words of view s that some body reads (an input word of a round-3 chi
        output that is computed, not taken from the block memo, at a position of
        state s in either block pattern).  Only these are maintained (Lemma 14)."""
        if not hasattr(self, '_vn'):
            vn = {sv: set() for sv in self.VS}
            for p in (0, 1):
                seq = block_seq(p, self.K)
                for Y in range(5):
                    for b in range(64):
                        ws = self.row_words(Y, b)
                        for X in range(5):
                            cls = [self.out_class(Y, b, X, sv) for sv in seq]
                            w3 = {ws[X], ws[(X + 1) % 5], ws[(X + 2) % 5]}
                            for r, sv in enumerate(seq):
                                if sv and cls.index(cls[r]) == r:
                                    vn[sv] |= w3 & self.VS[sv]
            self._vn = {sv: frozenset(v) for sv, v in vn.items()}
        return self._vn

    def m2rows(self, p, Y, b):
        """memo2 (Lemma 14'): actions of round-3 row (Y, b) in block pattern p, a list over X
        of lists over the positions r of the block:
          ('load', c, neg, c2st)  reload R3C class c (complemented if neg); c2st: also store
                                  the result under its own class c2st (or None);
          ('pair', d, r1, st)     out = input a XOR the nonlinear term stored (R3T class d)
                                  at the earlier position r1 >= 1; st: store out (class) or None;
          ('comp', st, d)         compute the output; st: store it (class) or None; d: also
                                  store its nonlinear term under R3T class d (or None).
        Classes: full = the triple of view expressions of the inputs X, X+1, X+2; reduced =
        the same with the all-ones term of input X removed (equal reduced classes give equal
        or complementary outputs); term class = the pair of expressions of inputs X+1, X+2
        (equal term classes give equal nonlinear terms NOT b AND c)."""
        if not hasattr(self, '_m2'):
            self._m2, self._m2a = {}, {}
        key = (p, Y, b)
        if key in self._m2:
            return self._m2[key]
        A = self._m2a                       # equal action tuples share one object (memory only)
        K = self.K
        N = 1 << K
        seq = block_seq(p, K)
        ws = self.row_words(Y, b)
        E = frozenset()
        ex = [[self.VD[s].get(w, E) if s else E for w in ws] for s in seq]
        thr = getattr(self, 'm2thr', M2THR)
        res = []
        for X in range(5):
            i1, i2 = (X + 1) % 5, (X + 2) % 5
            c3n, fl, c2, e3 = [], [], [], []
            id3, id2, ide = {}, {}, {}
            for r in range(N):
                e = ex[r]
                c3n.append(id3.setdefault((e[X] - {WT}, e[i1], e[i2]), len(id3)))
                fl.append(WT in e[X])
                c2.append(id2.setdefault((e[i1], e[i2]), len(id2)))
                e3.append(ide.setdefault((e[X], e[i1], e[i2]), len(ide)))
            occ = {}
            for r in range(N):
                occ.setdefault(c3n[r], []).append(r)
            ts, nuse = {}, {}
            for r in range(1, N):
                if occ[c3n[r]][0] == r:
                    if c2[r] not in ts:
                        ts[c2[r]] = r
                    else:
                        nuse[c2[r]] = nuse.get(c2[r], 0) + 1
            on = {c for c, n in nuse.items() if thr and n >= thr}
            acts = [None] * N
            for k, rs in occ.items():
                F = fl[rs[0]]
                aF = e3[rs[0]]
                other = [r for r in rs if fl[r] != F]
                stF = len(rs) > 1
                stN = len(other) >= 3
                for r in rs:
                    if r == rs[0]:
                        if r >= 1 and c2[r] in on and ts[c2[r]] < r:
                            a = ('pair', c2[r], ts[c2[r]], aF if stF else None)
                        else:
                            a = ('comp', aF if stF else None,
                                 c2[r] if (r >= 1 and c2[r] in on and ts[c2[r]] == r) else None)
                    elif fl[r] == F:
                        a = ('load', aF, False, None)
                    elif stN and r != other[0]:
                        a = ('load', e3[r], False, None)
                    else:
                        a = ('load', aF, True, e3[r] if (stN and r == other[0]) else None)
                    acts[r] = A.setdefault(a, a)
            res.append(acts)
        self._m2[key] = res
        return res

    def needed2(self):
        if not hasattr(self, '_vn2'):
            vn = {sv: set() for sv in self.VS}
            for p in (0, 1):
                seq = block_seq(p, self.K)
                for Y in range(5):
                    for b in range(64):
                        ws = self.row_words(Y, b)
                        acts = self.m2rows(p, Y, b)
                        for X in range(5):
                            for r, sv in enumerate(seq):
                                a = acts[X][r]
                                if not sv:
                                    continue
                                if a[0] == 'comp':
                                    vn[sv] |= {ws[X], ws[(X + 1) % 5], ws[(X + 2) % 5]} & self.VS[sv]
                                elif a[0] == 'pair':
                                    vn[sv] |= {ws[X]} & self.VS[sv]
            self._vn2 = {sv: frozenset(v) for sv, v in vn.items()}
        return self._vn2

    def row_words(self, Y, b):
        return [64 * _bsrc(X, Y, b)[0] + _bsrc(X, Y, b)[1] for X in range(5)]

    def out_class(self, Y, b, X, sv):
        """Class of the raw chi output X of round-3 row (Y, b) in view state sv: the
        view expressions of its three input words X, X+1, X+2 (mod 5).  Equal
        classes in two states of one block mean equal inputs, so equal outputs."""
        if not hasattr(self, '_oc'):
            self._oc = {}
        if (Y, b) not in self._oc:
            ws = self.row_words(Y, b)
            res = []
            for X2 in range(5):        # (not X: the argument X is used below)
                w3 = (ws[X2], ws[(X2 + 1) % 5], ws[(X2 + 2) % 5])
                ks = [tuple(self.VD[s2].get(w, frozenset()) if s2 else frozenset() for w in w3)
                      for s2 in range(1 << self.K)]
                idx = {}
                res.append([idx.setdefault(k2, len(idx)) for k2 in ks])
            self._oc[(Y, b)] = res
        return self._oc[(Y, b)][X][sv]

    def vpatch(self, j, sv, w):
        """Patch of word w of view sv in leaf j >= K: leaf j's base expression
        (stored-A2 terms read after the flips of bit j) with the all-ones term
        toggled once per term in the A2 support of each low bit set in sv."""
        e = set(self.P[j][0][w])
        for t in list(e):
            if t != WT:
                for i in range(self.K):
                    if (sv >> i) & 1 and t in self.sup[i]:
                        e ^= {WT}
        return frozenset(e)


# ---------------- cones ------------------------------------------------------
ALLW = frozenset((L, b) for L in range(25) for b in range(64))
ALLP = frozenset((x, b) for x in range(5) for b in range(64))
NEED5 = frozenset((L, (b - RHO[L]) % 64) for L in DIAG for b in KEEP)
_CONES = {}


def cones(starts):
    if starts not in _CONES:
        fix5 = frozenset(L % 5 for L, b in NEED5 if b == starts[2])
        chi5, par5, need4, fix4 = round_needs(NEED5, fix5, starts[2], starts[1])
        chi4, par4, need3, fix3 = round_needs(need4, fix4, starts[1], starts[0])
        assert need3 == ALLW
        _CONES[starts] = dict(FIX5=fix5, CHI5=chi5, PAR5=par5, NEED4=need4, FIX4=fix4, CHI4=chi4,
                              PAR4=par4, NEED3=need3, FIX3=fix3)
    return _CONES[starts]


def gen_round(B, getin, fixin, fp_in, qin, pout, rc, s, outarr, chi_need, par_need, st_need,
              fix_need, csarr, fixarr, after_plane=None, rowmemo=None):
    """rowmemo(Y, b) -> {X: None, ('load', a) or ('store', a)}: block memo of the
    raw chi output X of row (Y, b) (array R3C, word a; Lemma 14)."""
    Cprev = {}
    for k in range(64):
        b = (s + k) % 64
        outs = {}
        for Y in range(5):
            Xs = [X for X in range(5) if (X + 5 * Y, b) in chi_need]
            if not Xs:
                continue
            qrow, prow = _rowq(qin, Y), (pout >> (5 * Y)) & 31
            io = (rc >> b) & 1 if Y == 0 else 0
            rm = rowmemo(Y, b) if rowmemo else {}
            for X in Xs:
                if rm.get(X) and rm[X][0] == 'load':
                    outs[(X, Y)] = B.ld('R3C', rm[X][1])
                    if len(rm[X]) > 2 and rm[X][2]:
                        outs[(X, Y)] = B.not_(outs[(X, Y)])
                    if len(rm[X]) > 3 and rm[X][3] is not None:
                        B.st('R3C', rm[X][3], outs[(X, Y)])
            pairX = [X for X in Xs if rm.get(X) and rm[X][0] == 'pair']
            Xs = [X for X in Xs if not (rm.get(X) and rm[X][0] in ('load', 'pair'))]
            if not Xs and not pairX:
                continue
            need_in = sorted({(X + t) % 5 for X in Xs for t in (0, 1, 2)} | set(pairX))
            vin = {}
            comp = {}
            for X in need_in:
                L, bs = _bsrc(X, Y, b)
                v = getin(L, bs)
                if isinstance(v, tuple):          # (value, its complement)
                    v, comp[X] = v
                if fixin is not None and bs == fp_in:
                    v = B.xor(v, fixin(L % 5))
                    comp.pop(X, None)
                vin[X] = v
            if not Xs:
                plan = {}
            elif comp:
                _, _, plan = solve_row_free(qrow, prow, io, Xs, set(comp))
            else:
                _, _, plan = solve_row(qrow, prow, io, Xs)

            def g(X, c):
                if not c:
                    return vin[X]
                if X not in comp:
                    comp[X] = B.not_(vin[X])
                return comp[X]
            for X in Xs:
                ca, cb, cc, gate, on = plan[X]
                a_, b_, c_ = g(X, ca), g((X + 1) % 5, cb), g((X + 2) % 5, cc)
                t = B.or_(b_, c_) if gate == "or" else B.and_(b_, c_)
                if rm.get(X) and rm[X][0] == 'comp' and rm[X][2] is not None:
                    taddr, tgate = rm[X][2]
                    assert tgate == gate, (Y, b, X, tgate, gate)
                    B.st('R3T', taddr, t)
                o = B.xor(a_, t)
                if on:
                    o = B.not_(o)
                outs[(X, Y)] = o
            qb_ = [(qrow >> k) & 1 for k in range(5)]
            pb_ = [(prow >> k) & 1 for k in range(5)]
            for X in pairX:
                _, taddr, pT, _ = rm[X]
                t = B.ld('R3T', taddr)
                ib = io if X == 0 else 0
                on = int(qb_[X] ^ pT ^ ib != pb_[X])
                if on and X in comp:
                    a_, on = comp[X], 0
                else:
                    a_ = vin[X]
                o = B.xor(a_, t)
                if on:
                    o = B.not_(o)
                outs[(X, Y)] = o
            for X in Xs + pairX:
                if rm.get(X) and rm[X][0] == 'store':
                    B.st('R3C', rm[X][1], outs[(X, Y)])
                elif rm.get(X) and rm[X][0] in ('comp', 'pair') and rm[X][1 if rm[X][0] == 'comp' else 3] is not None:
                    B.st('R3C', rm[X][1 if rm[X][0] == 'comp' else 3], outs[(X, Y)])
        C = {}
        for x in range(5):
            if (x, b) in par_need:
                c = outs[(x, 0)]
                for Y in range(1, 5):
                    c = B.xor(c, outs[(x, Y)])
                C[x] = c
                if b == s and ((x + 1) % 5) in fix_need:
                    B.st(csarr, x, c)
        D = {}
        for Y in range(5):
            for x in range(5):
                L = x + 5 * Y
                if (L, b) not in st_need:
                    continue
                if b == s:
                    B.st(outarr, 64 * L + b, outs[(x, Y)])
                else:
                    if x not in D:
                        D[x] = B.xor(C[(x - 1) % 5], Cprev[(x + 1) % 5])
                    B.st(outarr, 64 * L + b, B.xor(outs[(x, Y)], D[x]))
        Cprev = C
        if after_plane:
            after_plane(b)
    for x in sorted(fix_need):
        c1 = B.ld(csarr, (x - 1) % 5)
        B.st(fixarr, x, B.xor(c1, Cprev[(x + 1) % 5]))


MASKIDX = {}


def mask(B, d, neg):
    return B.ld('MASK', d + (256 if neg else 0))


class Transposer:
    def __init__(self, B):
        self.B = B
        self.R = {}
        self.Z = {r: r not in KEYROWS for r in range(256)}
        self.OFF = [0] * 256

    def swap(self, ia, ib, d):
        B, R, Z, OFF = self.B, self.R, self.Z, self.OFF
        za, zb = Z[ia], Z[ib]
        if za and zb:
            return
        if _par(ib) == 0:              # b even: a moves
            m = mask(B, d, False)
            if za:
                t = B.and_(R[ib], m)
                R[ib] = B.xor(R[ib], t)
                R[ia] = t
            else:
                u = B.rot(R[ia], OFF[ia] - d)
                if zb:
                    t = B.and_(u, m)
                    R[ib] = t
                    R[ia] = B.xor(u, t)
                else:
                    t = B.and_(B.xor(u, R[ib]), m)
                    R[ib] = B.xor(R[ib], t)
                    R[ia] = B.xor(u, t)
            OFF[ia] = d % 256
        else:                          # a even: b moves
            m = mask(B, d, True)
            if zb:
                t = B.and_(R[ia], m)
                R[ia] = B.xor(R[ia], t)
                R[ib] = t
            else:
                v = B.rot(R[ib], OFF[ib] + d)
                if za:
                    t = B.and_(v, m)
                    R[ia] = t
                    R[ib] = B.xor(v, t)
                else:
                    t = B.and_(B.xor(R[ia], v), m)
                    R[ia] = B.xor(R[ia], t)
                    R[ib] = B.xor(v, t)
            OFF[ib] = (-d) % 256
        Z[ia] = Z[ib] = False


def slot_planes(g, w1=32):
    return [KEEP[k] for k in range(len(KEEP)) if k // (w1 // 4) == g]


_LAYOUTS = {}


def tlayout(w1):
    """Transpose layout (v6): phase 1 on blocks of w1 consecutive rows (stages
    1..w1/2), phase 2 on the 256/w1 rows w1*i + gi (stages w1..128).  w1 = 32 is
    bs5's layout (identical BLOCKS/P1ORDER/P2ORDER); w1 = 16 is the 16-row
    variant.  Processing index q -> slot w1*(q mod nb) + floor(q/nb), nb = 256/w1."""
    if w1 not in _LAYOUTS:
        nb = 256 // w1
        k = w1.bit_length() - 1
        bits1 = tuple(1 << i for i in range(k))
        bits2 = tuple(1 << i for i in range(k, 8))
        blocks = sorted({r // w1 for r in KEYROWS})
        p1 = {g: ref._best_order({w1 * g + q: (w1 * g + q) not in KEYROWS for q in range(w1)},
                                 [w1 * g + q for q in range(w1)], bits1) for g in blocks}
        p2 = {gi: ref._best_order({w1 * i + gi: i not in blocks for i in range(nb)},
                                  [w1 * i + gi for i in range(nb)], bits2) for gi in range(w1)}
        _LAYOUTS[w1] = dict(w1=w1, nb=nb, blocks=blocks, p1=p1, p2=p2,
                            slot=[w1 * (q % nb) + q // nb for q in range(256)])
    return _LAYOUTS[w1]


assert tlayout(16)['blocks'] == list(BLOCKS) and tlayout(16)['p1'] == P1ORDER and tlayout(16)['p2'] == P2ORDER


VSTRIDE = 2048     # view sv of word w is V[VSTRIDE * sv + w]


def vaddr(sv, w):
    return ('O2P', w) if sv == 0 else ('V', VSTRIDE * sv + w)


def px_map(geo, j):
    """Patch-term sets whose value E view_preblock leaves in PX[i] for the body."""
    K = geo.K
    sc = 1 << (j - 1) if j - 1 < K else 0
    pe = geo.P[j][0]
    ts = set()
    for w in pe:
        if any(sv != sc and w in geo.VS[sv] for sv in range(1, 1 << K)):
            t = tuple(sorted(x for x in pe[w] if x != WT))
            if len(t) >= 2:
                ts.add(t)
    return {t: i for i, t in enumerate(sorted(ts))}


def view_preblock(geo, j):
    """Leaf j >= K, first part (physical registers 0..3, no allocation): the A2
    flips of bit j, then every view that the round-3 reads do not use (all
    sv != 0 and != the current state) gets its patch: per patched word w the
    patch value E (XOR of stored-A2 terms; its complement once if some view
    needs it) is formed in r0 (r1), then per view ld r2 ; xor/not r2 ; st r2."""
    K = geo.K
    sc = 1 << (j - 1) if j - 1 < K else 0
    code = []
    for w in geo.flips[j]:
        code += [('ld', 2, None, None, ('A2', w)), ('not', 2, 2, None, None), ('st', None, 2, None, ('A2', w))]
    pe = geo.P[j][0]
    groups = {}                     # words with equal patch terms share one E (and ~E)
    for w in sorted(pe):
        vs = [sv for sv in range(1, 1 << K) if sv != sc and w in geo.VS[sv]]
        if vs:
            groups.setdefault(tuple(sorted(t for t in pe[w] if t != WT)), []).append((w, vs))
    pxm = px_map(geo, j)
    for ts, items in sorted(groups.items()):
        need_c = False
        if ts:
            code.append(('ld', 0, None, None, ('A2', ts[0])))
            for t in ts[1:]:
                code += [('ld', 3, None, None, ('A2', t)), ('xor', 0, 0, 3, None)]
            if ts in pxm:                   # hand E to the body (it patches the base view too)
                code.append(('st', None, 0, None, ('PX', pxm[ts])))
            need_c = any(WT in geo.vpatch(j, sv, w) for w, vs in items for sv in vs)
            if need_c:
                code.append(('not', 1, 0, None, None))
        for w, vs in items:
            for sv in vs:
                e = geo.vpatch(j, sv, w)
                if not e:
                    continue
                ad = vaddr(sv, w)
                code.append(('ld', 2, None, None, ad))
                if not ts:
                    code.append(('not', 2, 2, None, None))
                else:
                    code.append(('xor', 2, 2, 1 if WT in e else 0, None))
                code.append(('st', None, 2, None, ad))
    return code


def leaf_views(j, K=3):
    """Low-K-bit states s (z after the step) in which leaf j can run: z_i = 0
    for i < j - 1, z_{j-1} = 1, z_i (j <= i < K) free."""
    if j is None:
        return [0]
    if j >= K:
        return [1 << (j - 1) if j - 1 < K else 0]
    base = 1 << (j - 1) if j else 0
    return sorted(base | (f << j) for f in range(1 << (K - j)))


def block_seq(p, K=3):
    """View states of the 2^K steps of a block (t = 2^K m + r, p = m mod 2):
    gray(r) XOR p * 2^(K-1); r = 0 is the high step (or t = 0)."""
    return [(r ^ (r >> 1)) ^ (p << (K - 1)) for r in range(1 << K)]


def block_pos(j, sv, K=3):
    """(p, r) of a body: t = 0 -> (0, 0); leaf j >= K -> (1 if j == K else 0, 0);
    leaf j < K in state sv -> the unique r with ctz(r) = j and block_seq(p)[r] = sv."""
    if j is None:
        return 0, 0
    if j >= K:
        return (1 if j == K else 0), 0
    hits = [(p, r) for p in (0, 1) for r in range(1, 1 << K)       # block_seq(p, K)[r], inlined
            if (r & -r).bit_length() - 1 == j and (r ^ (r >> 1)) ^ (p << (K - 1)) == sv]
    assert len(hits) == 1, (j, sv, hits)
    return hits[0]


def memo_addr(Y, b, X, c, K):
    """R3C word of output X of round-3 row (Y, b), output class c < 2^K."""
    return 5 * ((64 * Y + b) * (1 << K) + c) + X


def build_leaf(geo, j, opts=None):
    """Straight-line body of leaf j in view state opts['sv'] (None: the t = 0
    body, view 0, without round 2)."""
    opts = opts or {}
    starts = tuple(opts.get('starts', STARTS))
    TL = tlayout(opts.get('w1', 32))
    w1, nb, BLK = TL['w1'], TL['nb'], TL['blocks']
    pair = opts.get('pair', False)
    cn = cones(starts)
    B = Bld()
    # ---- incremental round 2 (j >= K: A2 flips; base and view patches merged
    # into the round-3 reads; j < K: none)
    K = geo.K
    sc = opts.get('sv', 0) if j is not None else 0
    assert sc in leaf_views(j, K)
    patch = {}
    if j is not None and j >= K:
        B.tag = "r2"
        pe, _, _ = geo.P[j]
        patch = pe                      # (split mode: the A2 flips are in view_preblock)
        if opts.get('merge', True):
            for w in geo.flips[j]:
                B.st('A2', w, B.not_(B.ld('A2', w)))
    cache = {}

    pxm = px_map(geo, j) if j is not None and j >= K and not opts.get('merge', True) else {}

    def getexpr(e):
        if len(e) == 1 and WT not in e:
            return B.ld('A2', next(iter(e)))
        if e in cache:
            return B.ld('DL', cache[e])
        tse = tuple(sorted(x for x in e if x != WT))
        if tse in pxm:                          # E left in PX by view_preblock
            v = B.ld('PX', pxm[tse])
            if WT in e:
                v = B.not_(v)
            cache[e] = len(cache)
            B.st('DL', cache[e], v)
            return v
        cmode = opts.get('cache', 'all')
        r = set(e)
        v = None
        while r:
            best, gain = None, 1
            for f in cache:
                gn = len(r) - len(r ^ f)
                if gn > gain:
                    best, gain = f, gn
            if best is not None:
                piece = B.ld('DL', cache[best])
                r ^= best
                v = piece if v is None else B.xor(v, piece)
                continue
            ts = sorted(t for t in r if t != WT)
            if ts:
                t = ts[0]
                piece = B.ld('A2', t)
                r.discard(t)
                v = piece if v is None else B.xor(v, piece)
            else:
                r.discard(WT)
                v = B.not_(v)
        if cmode == 'all' or (cmode == 'multi' and len(e - {WT}) >= 2):
            cache[e] = len(cache)
            B.st('DL', cache[e], v)
        return v

    def getin3(L, bs):
        w = 64 * L + bs
        rv = sc if (sc and w in geo.VS[sc]) else 0       # view read by round 3
        if w not in patch:
            return B.ld(*vaddr(rv, w))
        tg = B.tag
        B.tag = "r2"
        out = None
        VN = geo.needed2() if opts.get('memo2') else geo.needed()
        svs = ([0] + [x for x in range(1, 1 << K) if w in VN[x] or (x == rv and w in geo.VS[x])]
               if opts.get('merge', True) else sorted({0, rv}))
        for sv in svs:                          # merged: all views; split: base and current
            e = patch[w] if sv == 0 else geo.vpatch(j, sv, w)
            if not e:
                if sv == rv:
                    out = B.ld(*vaddr(sv, w))
                continue
            old = B.ld(*vaddr(sv, w))
            if e == frozenset([WT]):
                new = B.not_(old)
                val = (new, old) if opts.get('freecomp', True) else new
            else:
                new = val = B.xor(old, getexpr(e))
            B.st(*vaddr(sv, w), new)
            if sv == rv:
                out = val
        B.tag = tg
        return out
    # ---- round 3 (full), start plane STARTS[0]; block memo of raw chi outputs (Lemma 14)
    p_, r_ = block_pos(j, sc, K)
    seq = block_seq(p_, K)

    def rowmemo(Y, b):
        if not opts.get('memo', True):
            return {}
        if opts.get('memo2'):
            acts = geo.m2rows(p_, Y, b)
            res = {}
            for X in range(5):
                a = acts[X][r_]
                if a[0] == 'load':
                    res[X] = ('load', memo_addr(Y, b, X, a[1], K), a[2],
                              None if a[3] is None else memo_addr(Y, b, X, a[3], K))
                elif a[0] == 'pair':
                    _, c2, r1, st = a
                    # gate form of the term stored at position r1 (a low body: plain solve_row)
                    comp1 = [X2 for X2 in range(5) if acts[X2][r1][0] == 'comp']
                    _, _, plan1 = solve_row(_rowq(Q3, Y), (P34 >> (5 * Y)) & 31,
                                            (RC[2] >> b) & 1 if Y == 0 else 0, comp1)
                    pT = 1 if plan1[X][3] == 'or' else 0
                    res[X] = ('pair', memo_addr(Y, b, X, c2, K), pT,
                              None if st is None else memo_addr(Y, b, X, st, K))
                else:
                    _, st, tc = a
                    tinfo = None
                    if tc is not None:
                        comp0 = [X2 for X2 in range(5) if acts[X2][r_][0] == 'comp']
                        _, _, plan0 = solve_row(_rowq(Q3, Y), (P34 >> (5 * Y)) & 31,
                                                (RC[2] >> b) & 1 if Y == 0 else 0, comp0)
                        tinfo = (memo_addr(Y, b, X, tc, K), plan0[X][3])
                    res[X] = ('comp', None if st is None else memo_addr(Y, b, X, st, K), tinfo)
            return res
        act = {}
        for X in range(5):
            cls = [geo.out_class(Y, b, X, sv) for sv in seq]
            c = cls[r_]
            first, last = cls.index(c), max(i for i, x in enumerate(cls) if x == c)
            a = memo_addr(Y, b, X, c, K)
            act[X] = ('load', a) if first < r_ else (('store', a) if last > r_ else None)
        return act
    B.tag = "r3"
    gen_round(B, getin3, None, None, Q3, P34, RC[2], starts[0], 'B3', ALLW, ALLP, cn['NEED3'],
              cn['FIX3'], 'CS3', 'FIX3', rowmemo=rowmemo)
    # ---- round 4 (cone)
    B.tag = "r4"
    gen_round(B, lambda L, bs: B.ld('B3', 64 * L + bs), lambda x: B.ld('FIX3', x), starts[0], Q3, P34,
              RC[3], starts[1], 'B4', cn['CHI4'], cn['PAR4'], cn['NEED4'], cn['FIX4'], 'CS4', 'FIX4')
    # ---- round 5 (cone) with the last round and phase 1 interleaved
    T = Transposer(B)
    produced = set()
    lastdone = set()
    blockdone = set()
    kslot = {b: k for k, b in enumerate(KEEP)}

    def last_plane(kb):
        B.tag = "last"
        (_, _, plan), _ = LASTPLAN[kb]
        Bv = []
        for X in range(5):
            L = DIAG[X]
            bs = (kb - RHO[L]) % 64
            v = B.ld('B5', 64 * L + bs)
            if bs == starts[2]:
                v = B.xor(v, B.ld('FIX5', L % 5))
            Bv.append(v)
        comp = {}

        def g(X, c):
            if not c:
                return Bv[X]
            if X not in comp:
                comp[X] = B.not_(Bv[X])
            return comp[X]
        for x in range(4):
            ca, cb, cc, gate, on = plan[x]
            a_, u, v = g(x, ca), g((x + 1) % 5, cb), g((x + 2) % 5, cc)
            t = B.or_(u, v) if gate == "or" else B.and_(u, v)
            o = B.xor(a_, t)
            if on:
                o = B.not_(o)
            r = ROWOF[(x, kb)]
            if opts.get('lr_scratch', True):
                B.st('LR', r, o)
            else:
                T.R[r] = o

    def phase1(gb):
        B.tag = "p1"
        rows = [w1 * gb + q for q in range(w1)]
        if opts.get('lr_scratch', True):
            for r in rows:
                if r in KEYROWS:
                    T.R[r] = B.ld('LR', r)
        for d in TL['p1'][gb]:
            for q in range(w1):
                r = w1 * gb + q
                if not r & d:
                    T.swap(r, r + d, d)
        for r in rows:
            if not T.Z[r]:
                B.st('ROWS', r, T.R[r])

    fixready = [False]

    def ready(kb):
        bss = [(kb - RHO[L]) % 64 for L in DIAG]
        return all(x in produced for x in bss) and (fixready[0] or starts[2] not in bss)

    def after5(b):
        if b is not None:
            produced.add(b)
        if opts.get('lastmode') == 'block':
            for gb in BLK:
                if gb in blockdone:
                    continue
                if all(ready(kb) for kb in slot_planes(gb, w1)):
                    tg = B.tag
                    for kb in slot_planes(gb, w1):
                        lastdone.add(kb)
                        last_plane(kb)
                    blockdone.add(gb)
                    phase1(gb)
                    B.tag = tg
            return
        for kb in KEEP:
            if kb in lastdone:
                continue
            if ready(kb):
                tg = B.tag
                lastdone.add(kb)
                last_plane(kb)
                B.tag = tg
        for gb in BLK:
            if gb in blockdone:
                continue
            if all(p in lastdone for p in slot_planes(gb, w1)):
                tg = B.tag
                blockdone.add(gb)
                phase1(gb)
                B.tag = tg
    B.tag = "r5"
    gen_round(B, lambda L, bs: B.ld('B4', 64 * L + bs), lambda x: B.ld('FIX4', x), starts[1], Q3, P5,
              RC[4], starts[2], 'B5', cn['CHI5'], cn['PAR5'], NEED5, cn['FIX5'], 'CS5', 'FIX5',
              after_plane=after5)
    fixready[0] = True
    B.tag = "r5"
    after5(None)
    assert blockdone == set(BLK)
    # ---- phase 2, frame fix, table
    for gi in range(w1):
        B.tag = "p2"
        for i in range(nb):
            r = w1 * i + gi
            if not T.Z[r]:
                T.R[r] = B.ld('ROWS', r)
        for d in TL['p2'][gi]:
            for i in range(nb):
                r = w1 * i + gi
                if not r & d:
                    T.swap(r, r + d, d)
        for i in range(nb):
            r = w1 * i + gi
            if T.OFF[r]:
                T.R[r] = B.rot(T.R[r], T.OFF[r])
                T.OFF[r] = 0
        B.tag = "table"
        for i in range(nb):
            q = nb * gi + i
            assert TL['slot'][q] == w1 * i + gi
            K = T.R[w1 * i + gi]
            w = B.emit('ldr', a=K)
            x = B.emit('xor', a=w, b='C')
            f = B.emit('cmplt', a=x, imm=1 << 128)
            # br imm: pair-member bit of this site (pair ids: the out-of-line
            # candidate clone of this site knows statically which member it is)
            B.emit('br', a=f, b=w, imm=(q & 1) if pair else None, dst=False)
            B.emit('str', a=K, b='C', dst=False)
            if not pair or q & 1:
                B.ins.append(('add', 'C', 'C', None, 1))
                B.tags.append("table")
    return B
```

<!-- file: setup_gen.py sha256=709805516f1bd54907f29f3460cc8b123d3b7beb8ba1dad5b1470c7809a3565c -->
```python
"""Counted per-batch setup (z = 0): 256 structured 128-byte prefixes from
768 random words (3 per prefix), PREF rows, bitsliced transpose, round 1 + round-2 theta (A2, stored
with polarity pi), O2P (round 2 + round-3 theta, encoding Q3), masks, and
(bs9) the 2^K - 1 views Vs = O2P at z = zperm(s) on the words geo.VS[s]
(bs11: on the maintained words geo.needed2()[s] only).
Straight-line IR compiled by ir.compile_block and run on ir.Machine."""
import ref
import gen
from ir import Bld, W

M64 = (1 << 64) - 1
M128 = (1 << 128) - 1
ref_PAD16 = 0x8000000000000006   # lane 16 of a 128-byte message


class SB(Bld):
    """Builder with constant folding for the words 0 and all-ones."""

    def c_xor(self, a, b):
        if a == 0:
            return b
        if b == 0:
            return a
        if a == 'W':
            return self.c_not(b)
        if b == 'W':
            return self.c_not(a)
        return self.xor(a, b)

    def c_not(self, a):
        if a == 0:
            return 'W'
        if a == 'W':
            return 0
        return self.not_(a)

    def c_and(self, a, b):
        if a == 0 or b == 0:
            return 0
        if a == 'W':
            return b
        if b == 'W':
            return a
        return self.and_(a, b)

    def un(self, op, a, imm):
        return self.emit(op, a, imm=imm)

    def mat(self, v):
        """materialise a folded constant (only 0 / W can occur)"""
        if v == 0:
            return self.zero
        if v == 'W':
            return self.ones
        return v


PREFBASE = None
IDSHIFT = 30     # set by machine.set_opts; 4-word prefixes use IDSHIFT - 1 = 29


def build_setup(col, pi, prefbase, geo=None):
    global PREFBASE
    PREFBASE = prefbase
    B = SB()
    B.tag = "setup"
    r0 = B.emit('rand')
    B.zero = B.xor(r0, r0)
    B.ones = B.not_(B.zero)
    for d in (1, 2, 4, 8, 16, 32, 64, 128):
        B.st('MASK', d, B.un('andi', B.ones, ref.MASKD[d]))
        B.st('MASK', 256 + d, B.un('andi', B.ones, W ^ ref.MASKD[d]))
    # 1. structured prefixes, row form, stored at PREF + 1024 beta + 4p + w
    #    (register-addressed; beta read from C = TAG*2^128 + beta*2^39 at t = 0)
    #    and at ROWIN (direct, for the transpose)
    nw = 4 if isinstance(col, tuple) else 2
    ids = IDSHIFT - 1 if nw == 4 else IDSHIFT        # 4 words per prefix: 1024*beta = (C mod 2^128) >> 29
    pb = B.un('add', B.un('shr', B.un('andi', 'C', M128), ids), PREFBASE)

    def rotl(c, k):
        return B.un('andi', B.or_(B.un('shl', c, k), B.un('shr', c, 64 - k)), M64)
    for p in range(256):
        if nw == 4:       # v7 family (5kyguy 6e715d9a): 3 random words = the 12 free lanes
            r0, r1, r2 = B.emit('rand'), B.emit('rand'), B.emit('rand')
            # r0 = lanes 0..3 (word 0 as drawn); r1 = lanes 4, 9, 6, 7; r2 = lanes 14, 13, 10, 11
            L4 = B.un('andi', r1, M64)
            L9 = B.un('andi', B.un('shr', r1, 64), M64)
            L14 = B.un('andi', r2, M64)
            L1 = B.un('andi', B.un('shr', r0, 64), M64)
            L2 = B.un('andi', B.un('shr', r0, 128), M64)
            L6 = B.un('andi', B.un('shr', r1, 128), M64)
            L7 = B.un('shr', r1, 192)
            L11 = B.un('shr', r2, 192)
            C4 = B.xor(B.xor(L4, L9), L14)
            C1 = B.un('xori', B.xor(B.xor(L1, L6), L11), ref_PAD16)
            L5 = B.xor(C4, rotl(C1, 1))                  # = L15
            L12 = B.xor(B.xor(B.un('xori', rotl(C4, 1), M64), L2), L7)
            w0 = r0
            w1 = B.or_(B.un('andi', r1, M64 | (M128 << 128)), B.un('shl', L5, 64))
            w2 = B.or_(B.un('andi', r2, M128 << 128), B.un('shl', L9, 64))
            w3 = B.or_(B.or_(L12, B.un('andi', r2, M64 << 64)), B.or_(B.un('shl', L14, 128), B.un('shl', L5, 192)))
            words = (w0, w1, w2, w3)
        else:
            raise ValueError('only the 128-byte family (4, 14) is shipped')
        for w, val in enumerate(words):
            B.emit('str', a=B.un('add', pb, nw * p + w), b=val, imm='mem', dst=False)
            B.st('ROWIN', nw * p + w, val)
    # 2. transpose rows -> planes (ref.transpose semantics), w = 0 .. nw-1
    S = {}
    for w in range(nw):
        for g in range(8):            # stages 1..16 inside blocks of 32 rows
            R = {q: B.ld('ROWIN', nw * (32 * g + q) + w) for q in range(32)}
            for d in (1, 2, 4, 8, 16):
                m = B.ld('MASK', d)
                for q in range(32):
                    if not q & d:
                        a, b = R[q], R[q + d]
                        t = B.and_(B.xor(B.un('shr', a, d), b), m)
                        R[q] = B.xor(a, B.un('shl', t, d))
                        R[q + d] = B.xor(b, t)
            for q in range(32):
                B.st('TR', 256 * w + 32 * g + q, R[q])
        for gi in range(32):          # stages 32, 64, 128 on rows 32 i + gi
            R = {i: B.ld('TR', 256 * w + 32 * i + gi) for i in range(8)}
            for d in (32, 64, 128):
                m = B.ld('MASK', d)
                for i in range(8):
                    r_ = 32 * i + gi
                    if not r_ & d:
                        a, b = R[i], R[i + d // 32]
                        t = B.and_(B.xor(B.un('shr', a, d), b), m)
                        R[i] = B.xor(a, B.un('shl', t, d))
                        R[i + d // 32] = B.xor(b, t)
            for i in range(8):
                B.st('TR', 256 * w + 32 * i + gi, R[i])
    # state planes: message lanes from TR, padding planes constant, others 0
    nl = 4 * nw
    zero_lanes = {8} if nw == 4 else ({0, 7} if col == 1 else {4, 6})
    padp = ((16, 1), (16, 2), (16, 63)) if nw == 4 else ((8, 1), (8, 2), (16, 63))

    def plane(L, b):
        if L < nl:
            if L in zero_lanes:
                return 0          # structurally zero lane (no z here: z = 0)
            return ('TR', 64 * L + b)
        if (L, b) in padp:
            return 'W'
        return 0

    def getS(L, b):
        v = plane(L, b)
        return B.ld(*v) if isinstance(v, tuple) else v
    # 3. round 1 (plain) and round-2 theta -> A2 (plain values in A2P scratch)
    C = {}
    for x in range(5):
        for b in range(64):
            v = 0
            for y in range(5):
                v = B.c_xor(v, getS(x + 5 * y, b))
            if v in (0, 'W'):
                C[(x, b)] = v
            else:
                B.st('C1S', 64 * x + b, v)
                C[(x, b)] = None

    def getC(x, b):
        v = C[(x, b)]
        return v if v is not None else B.ld('C1S', 64 * x + b)
    Dc = {}
    for x in range(5):
        for b in range(64):
            v = B.c_xor(getC((x - 1) % 5, b), getC((x + 1) % 5, (b - 1) % 64))
            if v in (0, 'W'):
                Dc[(x, b)] = v
            else:
                B.st('D1', 64 * x + b, v)
                Dc[(x, b)] = None

    def getD1(x, b):
        v = Dc[(x, b)]
        return v if v is not None else B.ld('D1', 64 * x + b)
    out = {}
    C2 = {}
    for Y in range(5):
        for bp in range(64):
            Bv = []
            for X in range(5):
                L, bs = ref._bsrc(X, Y, bp)
                Bv.append(B.c_xor(getS(L, bs), getD1(L % 5, bs)))
            for X in range(5):
                o = B.c_xor(Bv[X], B.c_and(B.c_not(Bv[(X + 1) % 5]), Bv[(X + 2) % 5]))
                if Y == 0 and X == 0 and (ref.RC[0] >> bp) & 1:
                    o = B.c_not(o)
                B.st('O1', 64 * (X + 5 * Y) + bp, B.mat(o))
    for x in range(5):
        for b in range(64):
            v = B.ld('O1', 64 * x + b)
            for y in range(1, 5):
                v = B.xor(v, B.ld('O1', 64 * (x + 5 * y) + b))
            B.st('C2', 64 * x + b, v)
    for x in range(5):
        for b in range(64):
            d = B.xor(B.ld('C2', 64 * ((x - 1) % 5) + b), B.ld('C2', 64 * ((x + 1) % 5) + (b - 1) % 64))
            for y in range(5):
                L = x + 5 * y
                a2 = B.xor(B.ld('O1', 64 * L + b), d)
                B.st('A2P', 64 * L + b, a2)
                B.st('A2', 64 * L + b, B.not_(a2) if 64 * L + b in pi else a2)
    # 4. O2P = encoded round 2 + round-3 theta (start plane 0, then fix plane 0)
    gen.gen_round(B, lambda L, bs: B.ld('A2P', 64 * L + bs), None, None, 0, ref.P34, ref.RC[1], 0, 'O2P',
                  gen.ALLW, gen.ALLP, gen.ALLW, frozenset(range(5)), 'CSS', 'FIXS')
    for L in range(25):
        B.st('O2P', 64 * L, B.xor(B.ld('O2P', 64 * L), B.ld('FIXS', L % 5)))
    return B


def setup_views_code(geo):
    """bs9, after build_setup: the 2^K - 1 views at the batch start (z = zperm(sv),
    low bits sv): V[2048 sv + w] = O2P[w] ^ (XOR of the stored A2 words of
    VD[sv][w]) [^ all-ones]; physical registers 0, 1 (straight line, counted).
    bs11: only the maintained words w in VN[sv] (gen.Geometry.needed2)."""
    code = []
    VN = geo.needed2()
    for sv in sorted(geo.VD):
        for w, e in sorted((w, e) for w, e in geo.VD[sv].items() if w in VN[sv]):
            code.append(('ld', 0, None, None, ('O2P', w)))
            for t in sorted(x for x in e if x != gen.WT):
                code += [('ld', 1, None, None, ('A2', t)), ('xor', 0, 0, 1, None)]
            if gen.WT in e:
                code.append(('not', 0, 0, None, None))
            code.append(('st', None, 0, None, ('V', gen.VSTRIDE * sv + w)))
    return code
```

<!-- file: machine.py sha256=4aa2c26310e142db67125d73276880633fdca870900eb92f3667c50ef0671ad2 -->
```python
"""Batch setup (reference level), memory layout, control, candidate path and
the counted run of z-steps on ir.Machine.  Every key is checked against
verifier/keccak.py sha3_256(m, 6) (copied as vkeccak.py)."""
import random
import ref
import gen
import ir
from vkeccak import sha3_256

M64 = (1 << 64) - 1
W = ir.W
M128 = (1 << 128) - 1

# ---- v6 options (set from the build pickle): w1 = transpose layout, pair = pair ids
OPTS = {}


ORDER = list(range(32))     # bs9: Gray bit j flips z-bit ORDER[j]


def set_opts(opts):
    OPTS.clear()
    OPTS.update(opts or {})
    ORDER[:] = OPTS.get('order', list(range(32)))
    assert sorted(ORDER) == list(range(32))
    global KV
    KV = OPTS.get('K', 3)
    import setup_gen
    setup_gen.IDSHIFT = 30 if OPTS.get('pair') else 31


def PAIR():
    return bool(OPTS.get('pair'))


def QB():
    """Low bits of the message number holding the in-step index (q, or the pair k = q >> 1)."""
    return 7 if PAIR() else 8


def slot_of(q):
    return gen.tlayout(OPTS.get('w1', 32))['slot'][q]


def id_of(beta, t, q):
    return (beta << (32 + QB())) + (t << QB()) + ((q >> 1) if PAIR() else q)


def members(n):
    """Message number -> list of (beta, t, q) it names."""
    beta, t, k = n >> (32 + QB()), (n >> QB()) & 0xFFFFFFFF, n & ((1 << QB()) - 1)
    return [(beta, t, 2 * k), (beta, t, 2 * k + 1)] if PAIR() else [(beta, t, k)]


def rotl64(v, r):
    r %= 64
    return ((v << r) | (v >> (64 - r))) & M64 if r else v


PAD16 = 0x8000000000000006     # lane 16 of a 128-byte message (0x06 suffix, final 0x80 bit)
FREE7 = (0, 1, 2, 3, 4, 6, 7, 9, 10, 11, 13, 14)   # v7 family: the 12 free lanes


def is128(col):
    return isinstance(col, tuple)


def NW(col):
    """256-bit words per message: 4 (128-byte family, z in lanes 4/14) or 2."""
    return 4 if is128(col) else 2


def structured_prefix(rng, col):
    """Round 1 linear in z (Guo-Liu-Song linear structure).  The 128-byte
    family col = (4, 14) of 5kyguy's 6e715d9a: 16
    lanes, 768 uniform bits in the 12 FREE7 lanes; with C4 = L4^L9^L14 and
    C1 = L1^L6^L11^PAD16: L5 = L15 = C4 ^ rotl(C1, 1), L8 = 0,
    L12 = ~rotl(C4, 1) ^ L2 ^ L7."""
    if is128(col):
        assert col == (4, 14)
        L = [0] * 16
        for k in FREE7:
            L[k] = rng.getrandbits(64)
        c4 = L[4] ^ L[9] ^ L[14]
        c1 = L[1] ^ L[6] ^ L[11] ^ PAD16
        L[5] = L[15] = c4 ^ rotl64(c1, 1)
        L[8] = 0
        L[12] = M64 ^ rotl64(c4, 1) ^ L[2] ^ L[7]
        return L
    raise ValueError("only the 128-byte family (4, 14) is shipped")


def message(lanes, z, col):
    L = list(lanes)
    for c in (col if is128(col) else (col, col + 5)):
        L[c] ^= z
    return b"".join(x.to_bytes(8, "little") for x in L)


def gray(t):
    return t ^ (t >> 1)


def zperm(g):
    """Gray-space word g -> z: bit j of g moves to z-bit ORDER[j]."""
    z = 0
    for j in range(32):
        if (g >> j) & 1:
            z |= 1 << ORDER[j]
    return z


def zof(t):
    """z of step t: the 2^32 steps of a batch enumerate every 32-bit z once."""
    return zperm(gray(t))


def zt_word(i):
    """Run-setup table ZT (2 x 2^16 words): ZT[x] = zperm(x), ZT[2^16 + x] = zperm(x << 16)."""
    return zperm(i) if i < 1 << 16 else zperm((i - (1 << 16)) << 16)


def a2_of(prefixes, z, col):
    msgs = [message(p, z, col) for p in prefixes]
    S = [0] * 1600
    nw = NW(col)
    for w in range(nw):
        rows = [int.from_bytes(m[32 * w:32 * w + 32], "little") for m in msgs]
        S[256 * w:256 * w + 256] = ref.transpose(rows, ref.SETUP_ORDER)
    S[64 * 4 * nw + 1] = W                  # 0x06 suffix right after the message
    S[64 * 4 * nw + 2] = W
    S[64 * 16 + 63] = W                     # final pad bit (lane 16, bit 63)
    D1 = ref.d_words(S)
    out, D2 = ref.round_pass(S, D1, ref.RC[0])
    return [out[i] ^ D2[ref.DCOL[i]] for i in range(1600)]


ARR = ['ROWIN', 'TR', 'C1S', 'D1', 'O1', 'C2', 'A2P', 'CSS', 'FIXS', 'O2P', 'A2', 'MASK', 'B3', 'B4', 'B5', 'FIX3', 'FIX4', 'FIX5', 'CS3', 'CS4', 'CS5', 'DL', 'ROWS',
       'LR', 'SAVE', 'CNT', 'ZT', 'PX']
# F3: everything outside the table lies in [2^140, 2^140 + 2^99) words
LAYOUT = {a: (1 << 140) + (k << 20) for k, a in enumerate(ARR)}
LAYOUT['R3C'] = (1 << 140) + (1 << 26)     # bs9 block memo, 5 * 320 * 2^K words (< 2^26 for K <= 15)
LAYOUT['V'] = (1 << 140) + (1 << 27)       # bs9 views, V[2048 sv + w] (< 2^27 for K <= 16)
LAYOUT['R3T'] = (1 << 140) + (1 << 29)     # bs11 memo2 nonlinear-term memo, 5 * 320 * 2^K words
LAYOUT['PREF'] = (1 << 140) + (1 << 30)
assert max(v for a, v in LAYOUT.items() if a != 'PREF') + (1 << 20) <= LAYOUT['PREF']
SCRATCH_SIZES = {'B3': 1600, 'B4': 1600, 'B5': 1600, 'FIX3': 5, 'FIX4': 5, 'FIX5': 5, 'CS3': 5, 'CS4': 5,
                 'CS5': 5, 'DL': 4096, 'ROWS': 256, 'LR': 256, 'PX': 1024}
KV = 3          # low Gray bits with materialised views (gen.Geometry K)


class Run:
    """One batch of 256 groups; runs z-steps with the compiled leaves."""

    def __init__(self, leaves, col, seed, beta, t0, garbage="ones", tag=None, hashfn=None, pi=frozenset(),
                 views=None, geo=None):
        self.leaves, self.col = leaves, col
        self.rng = random.Random(seed)
        rng = self.rng
        self.prefixes = [structured_prefix(rng, col) for _ in range(256)]
        self.beta = beta
        self.t = t0
        m = ir.Machine(LAYOUT)
        self.m = m
        g0 = gray(t0)
        z0 = zperm(g0)
        A2 = a2_of(self.prefixes, z0, col)
        # support check: every z-bit flips exactly the predicted words, by all-ones
        for j in range(32):
            if (t0 * 7 + j) % 8 == 0 or j < 2:
                A2j = a2_of(self.prefixes, z0 ^ (1 << j), col)
                sup = {64 * L + b for L, b in gen.a2_support(col, j)}
                for i in range(1600):
                    want = W if i in sup else 0
                    if A2j[i] ^ A2[i] != want:
                        raise RuntimeError("linear-structure support violated")
        # bs9: A2 and O2P at the base point (low KV bits of z cleared), views Vs
        # = O2P at low bits s on the words views[s]
        gb = g0 & ~((1 << KV) - 1)
        A2 = a2_of(self.prefixes, zperm(gb), col)
        O2P = ref.build_o2p(A2)
        for i in range(1600):
            m.mem[LAYOUT['A2'] + i] = A2[i] ^ (W if i in pi else 0)
            m.mem[LAYOUT['O2P'] + i] = O2P[i]
        for sv, ws in (views or {}).items():
            Os = ref.build_o2p(a2_of(self.prefixes, zperm(gb | sv), col))
            for i in ws:
                m.mem[LAYOUT['V'] + gen.VSTRIDE * sv + i] = Os[i]
        for i in range(1 << 17):
            m.mem[LAYOUT['ZT'] + i] = zt_word(i)
        # bs9 block memo R3C: a run started inside a block gets the raw round-3 row
        # outputs that the block's earlier steps would have stored
        self.O2Pb = O2P
        if geo is not None and t0 > 0:
            self.fill_memo(geo, t0)
        for d in (1, 2, 4, 8, 16, 32, 64, 128):
            m.mem[LAYOUT['MASK'] + d] = ref.MASKD[d]
            m.mem[LAYOUT['MASK'] + 256 + d] = W ^ ref.MASKD[d]
        nw = NW(col)
        for p, L in enumerate(self.prefixes):
            pm = message(L, 0, col)
            for w in range(nw):
                m.mem[LAYOUT['PREF'] + nw * (256 * beta + p) + w] = int.from_bytes(pm[32 * w:32 * w + 32], "little")
        m.mem[LAYOUT['CNT']] = 0
        self.tag = tag if tag is not None else rng.getrandbits(128)
        self.table = {}
        self.garbage = garbage
        self.garbage_cands = 0
        self.genuine_cands = 0
        self.cand_ops = []
        self.hashfn = hashfn or (lambda msg: sha3_256(msg, 6))
        m.hashfn = lambda *ws: int.from_bytes(self.hashfn(b"".join(w.to_bytes(32, "little") for w in ws)), "little")
        m.table_get = self.tget
        m.table_put = self.tput
        m.cand_hook = self.candidate
        m.reg[62] = t0 >> KV                # bs11: s counts blocks (block of step t0)
        m.reg[63] = (self.tag << 128) + id_of(beta, t0 + (1 if t0 else 0), 0)
        self.written = []
        self.expect_cands = 0

    def fill_memo(self, geo, t0):
        """bs9 block memo R3C for a run whose next step is t0 + 1: the raw round-3
        chi outputs that the earlier steps of its block would have stored (each
        output class with a first occurrence before the next position), computed from
        the base O2P and the view expressions (Lemma 13)."""
        m = self.m
        r_next = (t0 + 1) % (1 << KV)
        if not r_next:
            return
        tb = t0 + 1 - r_next
        seq = gen.block_seq((tb >> KV) & 1, KV)
        A2s = [m.mem[LAYOUT['A2'] + i] for i in range(1600)]
        O2P = self.O2Pb

        def word_at(sv, w):            # O2P at low bits sv: base ^ view expression
            v = O2P[w]
            for x in (geo.VD[sv].get(w, ()) if sv else ()):
                v ^= W if x == gen.WT else A2s[x]
            return v
        if OPTS.get('memo2'):
            return self.fill_memo2(geo, (tb >> KV) & 1, seq, r_next, word_at)
        for Y in range(5):
            for b in range(64):
                ws = geo.row_words(Y, b)
                for X in range(5):
                    done = set()
                    p, am, pb, bm, pc, cm, g, om = ref.PLAN3[64 * (X + 5 * Y) + b]
                    assert ref.SRC[p] == ws[X] and ref.SRC[pb] == ws[(X + 1) % 5]
                    for r in range(r_next):
                        c = geo.out_class(Y, b, X, seq[r])
                        if c in done:
                            continue
                        done.add(c)
                        ins = [word_at(seq[r], w) for w in ws]
                        u, v = ins[(X + 1) % 5] ^ bm, ins[(X + 2) % 5] ^ cm
                        m.mem[LAYOUT['R3C'] + gen.memo_addr(Y, b, X, c, KV)] = (
                            ins[X] ^ am ^ ((u | v) if g else (u & v)) ^ om)

    def fill_memo2(self, geo, p, seq, r_next, word_at):
        """bs11 memo2 (Lemma 14'): every R3C word (full or complement class) and R3T term
        that the positions r < r_next of the block store, computed from the base O2P and
        the view expressions at position r: an output by the reference plan, a term
        NOT b AND c in the polarity of the gate (AND: as is; OR: complemented) that the
        storing body's plan uses."""
        m = self.m
        for Y in range(5):
            qr = ref._rowq(ref.Q3, Y)
            for b in range(64):
                ws = geo.row_words(Y, b)
                ins_at = {}
                for r, X, kind, cls, gate in memo2_events(geo, p, Y, b):
                    if r >= r_next:
                        break
                    if r not in ins_at:
                        ins_at[r] = [word_at(seq[r], w) for w in ws]
                    ins = ins_at[r]
                    if kind == 'out':
                        _, am, _, bm, _, cm, g, om = ref.PLAN3[64 * (X + 5 * Y) + b]
                        u, v = ins[(X + 1) % 5] ^ bm, ins[(X + 2) % 5] ^ cm
                        m.mem[LAYOUT['R3C'] + gen.memo_addr(Y, b, X, cls, KV)] = (
                            ins[X] ^ am ^ ((u | v) if g else (u & v)) ^ om)
                    else:
                        tbv = ins[(X + 1) % 5] ^ (W if (qr >> ((X + 1) % 5)) & 1 else 0)
                        tcv = ins[(X + 2) % 5] ^ (W if (qr >> ((X + 2) % 5)) & 1 else 0)
                        m.mem[LAYOUT['R3T'] + gen.memo_addr(Y, b, X, cls, KV)] = (
                            ((tbv ^ W) & tcv) ^ (W if gate == 'or' else 0))

    def clone_at(self, t0, seed, leaves, geo, garbage=None, beta=None):
        """A copy of this run (same batch prefixes and maintained state, which must be
        that of t0's block: same high z bits) positioned so that the next step is
        t0 + 1, with a fresh table, fresh scratch randomness and the block memo."""
        import copy
        r = copy.copy(self)
        m = ir.Machine(LAYOUT)
        m.mem = dict(self.m.mem)
        m.reg = list(self.m.reg)
        r.m = m
        r.leaves = leaves
        r.rng = random.Random(seed)
        r.t = t0
        if beta is not None:
            r.beta = beta
        if garbage is not None:
            r.garbage = garbage
        r.table, r.written, r.cand_ops = {}, [], []
        r.garbage_cands = r.genuine_cands = r.expect_cands = 0
        r.started = True
        m.hashfn = self.m.hashfn
        m.table_get, m.table_put, m.cand_hook = r.tget, r.tput, r.candidate
        m.reg[62] = t0 >> KV
        m.reg[63] = (r.tag << 128) + id_of(r.beta, t0 + 1, 0)
        assert gray(t0) >> KV == gray(self.t) >> KV or (gray(t0) & ~((1 << KV) - 1)) == (gray(self.t) & ~((1 << KV) - 1))
        r.fill_memo(geo, t0)
        return r

    # ---- table memory (never initialised; adversarial contents)
    def tget(self, K):
        v = self._tget(K)
        if v >> 128 == self.tag:
            self.expect_cands += 1                 # this lookup must take the candidate path
        return v

    def _tget(self, K):
        if not 0 <= K < 1 << 140:
            raise RuntimeError("key is not a 140-bit address")
        if K in self.table:
            return self.table[K]
        g = self.garbage
        r = random.Random(K * 1000003 + 17)
        if g == "ones":
            return W
        if g == "zero":
            return 0
        if g == "random":
            return r.getrandbits(256)
        # adversarial: high half = TAG, low half random or an out-of-range id
        lo = r.getrandbits(128) if r.random() < 0.5 else (r.getrandbits(48) << 40) | r.getrandbits(40)
        return (self.tag << 128) | lo

    def tput(self, K, v):
        self.table[K] = v
        self.written.append((K, v))

    # ---- candidate path (out of line), counted instruction by instruction
    def candidate(self, m, rw, mem_bit=None):
        assert PAIR() and is128(self.col)
        return self.candidate_pair4(m, rw, mem_bit)


    def candidate_pair4(self, m, rw, mb):
        """v7 (128-byte family): as candidate_pair, messages are 4 words.  Save
        14 registers; r0 = stored pair id, r1 = current pair id (then the
        current digest), r2 address, r3 z, r4 temp, r5..r8 the current
        message, r9..r12 a stored member, r13 its digest / compare flag.
        Rebuild the current message (member mb) and both stored members, 3
        units; halt only on equal digests of distinct messages; else count,
        cap check, restore, jump back."""
        c0 = m.count
        u0 = m.units
        idw = m.reg[rw] & M128
        idc = m.reg[63] & M128
        NS = 14
        seg = [('st', None, k, None, ('SAVE', k)) for k in range(NS)]
        seg += [('andi', 0, rw, None, M128), ('andi', 1, 63, None, M128)]
        seg += rebuild_addr_pair4(1, 2, 3, 4) + load_msg4(2, mb, (5, 6, 7, 8), 3, 4)
        seg += [('hash4', 1, None, None, (5, 6, 7, 8))]
        seg += rebuild_addr_pair4(0, 2, 3, 4)
        m.run(seg)
        cur = tuple(m.reg[5:9])
        q = len(self.written)                           # true in-step index of the current message
        if mb != (q & 1) or members(idc)[q & 1][2] != q:
            raise RuntimeError("branch-site member bit / current pair id wrong")
        self.check_msg(cur, idc, mb)
        for k in (0, 1):
            m.run(load_msg4(2, k, (9, 10, 11, 12), 3, 4) + [('hash4', 13, None, None, (9, 10, 11, 12)),
                                                              ('cmpeq', 13, 13, 1, None)])
            m.count += 1                                # branch on equal digests
            st = tuple(m.reg[9:13])
            self.check_msg(st, idw, k)
            if m.reg[13]:
                same = True
                for i in range(4):                      # word i equal? (branch out on the first difference)
                    m.run([('cmpeq', 13, 9 + i, 5 + i, None)])
                    m.count += 1
                    if not m.reg[13]:
                        same = False
                        break
                if not same:
                    self.halted = ((st, cur), m.count - c0)
                    raise Halt()
                self.cand_same = getattr(self, 'cand_same', 0) + 1
        m.run([('ld', 4, None, None, ('CNT', 0)), ('add', 4, 4, None, 1), ('st', None, 4, None, ('CNT', 0)),
               ('cmplt', 4, 4, None, VCAP)])
        m.count += 1                                    # branch: abort if CNT >= VCAP
        if not m.reg[4]:
            raise RuntimeError("candidate cap reached")
        m.run([('ld', k, None, None, ('SAVE', k)) for k in range(NS)])
        m.count += 1                                    # jump back to this site's insert
        self.cand_ops.append(m.count - c0)
        assert m.units - u0 == 3

    def check_msg(self, words, n, k):
        """A rebuilt message whose id names a message of this batch must be exact."""
        beta, t, q = members(n)[k]
        if beta != self.beta:
            return
        want = message(self.prefixes[slot_of(q)], zof(t), self.col)
        got = b"".join(w.to_bytes(32, "little") for w in words)
        if got != want:
            raise RuntimeError("id decode / message rebuild wrong")
        self.rebuilt_ok = getattr(self, 'rebuilt_ok', 0) + 1


    def control(self):
        """bs11 block-unrolled control (proof Section 5.2).  Layout: T0 (the t = 0 body)
        falls through into CHAIN_0; CHAIN_p (p = 0, 1) is the straight-line sequence of the
        2^KV - 1 low bodies of block pattern p in position order r = 1 .. 2^KV - 1 (body
        (ctz r, gray(r) XOR p 2^(KV-1))), ending with a jump to TOP; TOP: s = s + 1 (s counts
        blocks), then bit tests v = s AND 2^i ; branch if v != 0 (2 ops each) for i = 0, 1, ...
        up to the lowest set bit of s, branching to H_j, j = KV + ctz(s); H_j: the high body of
        leaf j, then a jump to CHAIN_p (p = 1 iff j = KV).  At s = 2^(32-KV) all 32 - KV tests
        fail and TOP falls through to the end of the batch.  A low step runs no control
        operation; a high step runs 1 + 2 (j - KV + 1) before its body; the jumps (1 op each)
        follow the high bodies and the last body of each chain (loop_ops).  Returns
        (leaf, view state) of step t + 1."""
        t1 = self.t + 1
        r = t1 & ((1 << KV) - 1)
        if r:                                      # next body of the chain: no control op
            return (r & -r).bit_length() - 1, gray(t1) & ((1 << KV) - 1)
        m = self.m
        m.reg[62] = (m.reg[62] + 1) & W            # TOP: add
        s = m.reg[62]
        ops = 1
        i = 0
        while True:
            ops += 2                               # andi + branch on v != 0
            if s & (1 << i):
                break
            i += 1
            if i == 32 - KV:
                raise RuntimeError("s = 2^(32-K): end of batch")
        j = KV + i
        if s != t1 >> KV:
            raise RuntimeError("block counter s differs from the block of the step")
        assert ops == ctl_ops(j)
        m.reg[0] = None                            # temporary
        m.count += ops
        return j, gray(t1) & ((1 << KV) - 1)

    def step(self):
        """One z-step; returns (leaf, ops) and checks every key."""
        m = self.m
        c0 = m.count
        for a, n in SCRATCH_SIZES.items():
            for i in range(n):
                m.mem[LAYOUT[a] + i] = self.rng.getrandbits(256)
        for k in range(62):
            m.reg[k] = self.rng.getrandbits(256)
        if self.t == 0 and m.reg[62] == 0 and not getattr(self, 'started', False):
            leaf = None
            code = self.leaves[None]
        else:
            leaf, sv = self.control()
            self.t += 1
            if leaf != (self.t & -self.t).bit_length() - 1:
                raise RuntimeError("control tree chose the wrong leaf")
            code = self.leaves[(leaf, sv)]
            leaf = (leaf, sv)
        self.started = True
        self.written = []
        nc = len(self.cand_ops)
        e0 = self.expect_cands
        self.run_code(code)
        if len(self.cand_ops) - nc != self.expect_cands - e0:
            raise RuntimeError("candidate path count differs from TAG-high lookups")
        m.count += loop_ops(leaf)                  # jump to the chain / to TOP, if any
        ops = m.count - c0 - sum(self.cand_ops[nc:])
        self.check_step()
        return leaf, ops

    def run_code(self, code):
        self.m.run(code)

    def check_step(self):
        t = self.t
        z = zof(t)
        if len(self.written) != 256:
            raise RuntimeError("expected 256 inserts")
        for q, (K, v) in enumerate(self.written):
            n = id_of(self.beta, t, q)
            if v != (self.tag << 128) + n:
                raise RuntimeError("table word is not TAG*2^128 + n")
            p = slot_of(q)
            msg = message(self.prefixes[p], z, self.col)
            want = ref.key_of_digest(int.from_bytes(sha3_256(msg, 6), "little"))
            if K != want:
                raise RuntimeError("key mismatch: t=%d q=%d" % (t, q))
        self.keys_checked = getattr(self, 'keys_checked', 0) + 256


def memo2_events(geo, p, Y, b):
    """The memo stores of round-3 row (Y, b) over a block of pattern p, sorted by position:
    (r, X, 'out', class, None) for an R3C store and (r, X, 'term', term class, gate) for an
    R3T store, read off gen.Geometry.m2rows; gate = the gate of the storing body's plan
    (gen.solve_row over the outputs it computes, as in gen.build_leaf)."""
    if not hasattr(geo, '_m2ev'):
        geo._m2ev = {}
    key = (p, Y, b)
    if key not in geo._m2ev:
        acts = geo.m2rows(p, Y, b)
        io = (ref.RC[2] >> b) & 1 if Y == 0 else 0
        ev = []
        for r in range(1 << KV):
            comp0 = [X2 for X2 in range(5) if acts[X2][r][0] == 'comp']
            plan0 = None
            for X in range(5):
                a = acts[X][r]
                if a[0] == 'comp':
                    if a[1] is not None:
                        ev.append((r, X, 'out', a[1], None))
                    if a[2] is not None:
                        if plan0 is None:
                            _, _, plan0 = gen.solve_row(ref._rowq(ref.Q3, Y), (ref.P34 >> (5 * Y)) & 31, io, comp0)
                        ev.append((r, X, 'term', a[2], plan0[X][3]))
                elif a[0] == 'pair':
                    if a[3] is not None:
                        ev.append((r, X, 'out', a[3], None))
                elif a[3] is not None:
                    ev.append((r, X, 'out', a[3], None))
        geo._m2ev[key] = ev
    return geo._m2ev[key]


class Halt(Exception):
    pass


def ctl_ops(j):
    """bs11 control before a body of leaf j: 0 for j < KV (bodies follow each other in their
    chain); for j >= KV the TOP code: s = s + 1 and 2 (j - KV + 1) bit-test ops."""
    return 0 if j < KV else 1 + 2 * (j - KV + 1)


def loop_ops(k):
    """Jumps after body k (1 op): after every high body (to its chain) and after the last
    body of each chain (r = 2^KV - 1: leaf 0 in state 2^(KV-1) (p = 0) or 0 (p = 1), to
    TOP); none after T0 (it falls through into CHAIN_0) or any other low body."""
    if k is None:
        return 0
    j, sv = k
    if j >= KV:
        return 1
    return 1 if j == 0 and sv in (0, 1 << (KV - 1)) else 0


def end_ops():
    """TOP at s = 2^(32-KV), once per batch: the add and 32 - KV failing bit tests."""
    return 1 + 2 * (32 - KV)


def layout_trace(nb):
    """Walk the bs11 program layout (T0, CHAIN_p, TOP, H_j) for a batch of 2^nb steps
    (nb > KV, TOP testing nb - KV bits) and count its control operations; returns the list
    of bodies in execution order and the count.  The self-test compares it with
    (ctz t, gray(t) mod 2^KV) for t = 0 .. 2^nb - 1 and with ctl_ops / loop_ops / end_ops."""
    bs = {p: gen.block_seq(p, KV) for p in (0, 1)}
    chain = {p: [((r & -r).bit_length() - 1, bs[p][r]) for r in range(1, 1 << KV)] for p in (0, 1)}
    seq = [None] + chain[0]
    ops = 1                                        # CHAIN_0 -> TOP
    s = 0
    while True:
        s += 1
        ops += 1                                   # TOP: add
        hit = None
        for i in range(nb - KV):
            ops += 2                               # andi + branch
            if s & (1 << i):
                hit = KV + i
                break
        if hit is None:
            return seq, ops                        # fell through: end of batch
        seq.append((hit, (1 << (hit - 1)) if hit - 1 < KV else 0))
        ops += 1                                   # H_j -> CHAIN_p
        seq += chain[1 if hit == KV else 0]
        ops += 1                                   # CHAIN_p -> TOP


NB = 307990341830783024002353940   # bs11: batches per run (cert.py: the smallest count with success bound >= 0.3905)
N = NB << 40
VCAP = N * N // (1 << 141) + N * N // (1 << 148) + (1 << 91) + (1 << 61)



def rebuild_addr_pair4(idr, ar, zr, tr):
    """v7: pair id (beta*2^39 + t*2^7 + k; slot(2k) = 32*(k mod 8) + floor(k/8),
    slot(2k+1) = slot(2k) + 16) in idr -> ar = PREF + 4*(256*(beta mod 2^88) +
    slot(2k)), zr = z(t) = zperm(gray(t)) (bs9: two run-setup ZT lookups);
    member 1 is at ar + 64.  beta is masked to 88 bits
    (every real beta < NB < 2^88), so a garbage id stays in
    [PREF, PREF + 2^98).  idr is preserved."""
    assert OPTS.get('w1') == 16
    return [('shr', ar, idr, None, 29), ('andi', ar, ar, None, ((1 << 98) - 1) ^ 1023),   # 1024*beta
            ('andi', tr, idr, None, 7), ('shl', tr, tr, None, 7), ('addr', ar, ar, tr, None),
            ('shr', tr, idr, None, 1), ('andi', tr, tr, None, 60), ('addr', ar, ar, tr, None),
            ('add', ar, ar, None, LAYOUT['PREF']),
            ('shr', zr, idr, None, 7), ('andi', zr, zr, None, 0xFFFFFFFF),          # t
            ('shr', tr, zr, None, 1), ('xor', zr, zr, tr, None),                    # g = gray(t)
            ('andi', tr, zr, None, 0xFFFF), ('add', tr, tr, None, LAYOUT['ZT']),     # bs9: z = ZT[g mod 2^16]
            ('ldr', tr, tr, None, 'mem'), ('shr', zr, zr, None, 16),                 #   ^ ZT[2^16 + (g >> 16)]
            ('add', zr, zr, None, LAYOUT['ZT'] + (1 << 16)), ('ldr', zr, zr, None, 'mem'),
            ('xor', zr, zr, tr, None)]


def load_msg4(ar, mb, wr, zr, tr):
    """v7: the 4 words of pair member mb at ar (+64 for mb = 1; ar advanced)
    into registers wr; z XORed into the low halves of lanes 4 (word 1, bits
    0..31) and 14 (word 3, bits 128..159)."""
    c = [('add', ar, ar, None, 64)] if mb else []
    c += [('ldr', wr[0], ar, None, 'mem'), ('add', tr, ar, None, 1), ('ldr', wr[1], tr, None, 'mem'),
          ('add', tr, tr, None, 1), ('ldr', wr[2], tr, None, 'mem'),
          ('add', tr, tr, None, 1), ('ldr', wr[3], tr, None, 'mem'),
          ('xor', wr[1], wr[1], zr, None), ('shl', tr, zr, None, 128), ('xor', wr[3], wr[3], tr, None)]
    return c
```

<!-- file: selftest.py sha256=cf9d4c4c18805cad574a4b0a42a11f8673dd88ae29660bacca6ac6d689e6e46c -->
```python
"""Self-test of the bs11 counted program (proof.md Appendix A).

    NPROC=6 python3 selftest.py REPO_ROOT   # about 25-40 minutes with 6 processes, ~3 GiB each, stdlib only

REPO_ROOT is a checkout of the challenge repository: the reference hash is
REPO_ROOT/verifier/keccak.py:sha3_256(m, 6) (imported by vkeccak.py).  Run it
in a directory holding the files of Appendix A and the shipped experiment
script experiments/s3r6_bitslice_birthday.py (the program's reference
geometry, imported by ref.py).  The test

 1. rebuilds the message geometry (22-word supports, 499 patched words, 975
    read words, 3..10 flips per leaf, storage polarity, Gray order ORDER, the
    2^K - 1 = 1023 materialised views of Lemma 13 and the maintained words of
    the memo2 block memo, Lemma 14'), and checks the block-unrolled control
    layout (machine.layout_trace: the bodies run in step order, control count
    = formula);
 2. generates and compiles all 2069 straight-line bodies (t = 0 and every
    (leaf j, view state s) pair that occurs), prints every static count and
    the EXACT number of operations of one batch,
        T = body_0 + sum over t = 1 .. 2^32 - 1 of
            (ctl(ctz t) + body(ctz t, view) + jump(body)) + 1 + 2 (32 - K),
    (ctl(j) = 0 for j < K, 1 + 2 (j - K + 1) for j >= K; jump = 1 after a
    high body and after the last body of each chain, else 0; leaf j < K
    occurs in 2^(K-j) view states, 2^(31-K) times each; leaf j >= K occurs
    2^(31-j) times), T / 2^32, asserts T and the body hash equal the values
    of proof Section 8, and a SHA-256 of the compiled bodies;
 3. statically checks that each of the 2069 x 256 table steps is the exact
    hot path of proof Section 5.3 and that no other table access exists;
 4. runs every body on the counted 64-register simulator (hostile scratch
    memory and registers, adversarial never-written table words), compares
    all 256 keys of every step with key_of_digest(sha3_256(m, 6)) for
    z = zperm(gray(t)), asserts measured = control + static + jump, and
    checks the maintained A2, O2P and view words against a rebuild from the
    prefixes; then runs 3 x 40 consecutive steps across view blocks (one
    from the first step of a block with no memo prefill), checking the same
    after every step;
 5. replays z-steps (2 x 256 genuine candidates, rebuilt messages exact),
    forces the halting path, and reports the candidate costs;
 6. runs the counted batch-setup program (including the maintained view
    words) and the counted run-setup table ZT, and compares them with a
    reference.
Any mismatch raises.  The printed T / 2^32 is the ops/z-step that proof
Section 8 charges."""
import hashlib
import json
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
if len(sys.argv) < 2:
    sys.exit(__doc__)
sys.path.insert(1, os.path.abspath(sys.argv[1]))           # verifier/keccak.py

import gen                                                  # noqa: E402
import ir                                                   # noqa: E402
import machine                                              # noqa: E402
import ref                                                  # noqa: E402
import setup_gen                                            # noqa: E402

COL = (4, 14)
K = 10
ORDER = [25, 8, 21, 10, 28, 15, 30, 17, 4, 12, 19, 27, 6, 26, 1, 14, 13, 24, 7, 18, 3, 31, 9, 5, 20, 11, 16, 22, 23, 2, 0, 29]
DEV = bool(os.environ.get("S8CFG"))
if DEV:                                                     # development override (small K)
    K, ORDER = json.loads(os.environ["S8CFG"])
OPTS = {"lastmode": "block", "lr_scratch": False, "w1": 16, "pair": True, "starts": list(ref.STARTS),
        "order": ORDER, "K": K, "memo2": True}
EXPECT = {"T": 117398575636479,                         # proof Section 8
          "sha256": "4c07e7bad4fcc77d9282c88f89f3e64f99af9b8cf88c54678403db8b66a4efc5"}


def body_keys():
    ks = [None]
    for j in range(32):
        ks += [(j, sv) for sv in gen.leaf_views(j, K)]
    return ks


def canon(leaves):
    h = hashlib.sha256()
    for k in body_keys():
        h.update(json.dumps([k, leaves[k]], separators=(",", ":")).encode())
    return h.hexdigest()


_G = {}


def _winit(root, geo=None):
    if root not in sys.path:
        sys.path.insert(1, os.path.abspath(root))
    machine.set_opts(OPTS)
    _G['geo'] = geo or gen.Geometry(COL, K=K, order=ORDER)


def compile_body(geo, k):
    """Body k (t = 0: None; else (leaf j, view state)) as physical code."""
    o = dict(OPTS)
    if k is not None:
        o['sv'] = k[1]
    B = gen.build_leaf(geo, None if k is None else k[0], o)
    code, hw, tags = ir.compile_block(B.ins, B.tags)
    return code, hw


def body_sha(k, code):
    return hashlib.sha256(json.dumps([k, code], separators=(",", ":")).encode()).hexdigest()


def step_for(j, sv, rng):
    """A random step t (>= 1, < 2^32) with ctz(t) = j and view state sv."""
    while True:
        t = (2 * rng.randrange(1 << (31 - j)) + 1) << j if j < 31 else 1 << 31
        if t >= 2 and machine.gray(t) & ((1 << K) - 1) == sv:
            return t


def _base_run(p):
    """Per worker: a run positioned at the start of a block of pattern p (random
    high bits, worker-specific prefixes), cloned for every low body."""
    key = ('base', p)
    if key not in _G:
        rng = random.Random(os.getpid() * 7 + p)
        m_ = 2 * rng.randrange(1 << (31 - K - 1)) + p
        tb = m_ << K
        _G[key] = machine.Run({}, COL, seed=rng.randrange(1 << 30), beta=rng.randrange(1 << 20), t0=tb,
                              garbage="adv", pi=_G['geo'].pi, views=_G['geo'].needed2(), geo=_G['geo'])
    return _G[key]


def _task(arg):
    """Worker: compile body k, check its table steps statically, run it once on
    the counted simulator (keys vs the verifier, measured = control + static
    + jump, maintained A2 / O2P / views vs a rebuild).  A low body (leaf j < K)
    runs at its block position from a clone of a block-start run; a high body
    and the t = 0 body from a fresh run."""
    n, k = arg
    geo = _G['geo']
    code, hw = compile_body(geo, k)
    static_table_check({k: code})
    rng = random.Random(1000 + n)
    garb = ("adv", "random", "ones", "zero")[n % 4]
    if k is not None and k[0] < K:
        p, r = gen.block_pos(k[0], k[1], K)
        base = _base_run(p)
        run = base.clone_at(base.t + r - 1, 100 + n, {k: code}, geo, garbage=garb)
    else:
        t = 0 if k is None else step_for(k[0], k[1], rng)
        run = machine.Run({k: code}, COL, seed=100 + n, beta=n, t0=max(t - 1, 0), garbage=garb,
                          pi=geo.pi, views=geo.needed2(), geo=geo)
    leaf, ops = run.step()
    want = len(code) + machine.loop_ops(k) + (0 if k is None else machine.ctl_ops(k[0]))
    assert leaf == k and ops == want, (k, ops, want)
    assert run.expect_cands == len(run.cand_ops)
    state_check(geo, run, rng, allviews=(n % 61 == 0))
    return len(code), hw, body_sha(k, code), 256, sorted(set(run.cand_ops))


def state_check(geo, r, rng, allviews=False):
    """Maintained A2 (read words), O2P and views (all, or the current one and 12
    random ones; on the maintained words VN[s] of Lemma 14) equal a rebuild
    from the prefixes at the current z."""
    reads = set().union(*[p[2] for p in geo.P])
    g = machine.gray(r.t)
    gb = g & ~((1 << K) - 1)
    A2 = machine.a2_of(r.prefixes, machine.zperm(gb), COL)
    O2P = ref.build_o2p(A2)
    lay = machine.LAYOUT
    assert all(r.m.mem[lay['A2'] + i] == A2[i] ^ (ir.W if i in geo.pi else 0) for i in reads)
    assert all(r.m.mem[lay['O2P'] + i] == O2P[i] for i in range(1600))
    svs = sorted(geo.VS) if allviews else sorted(({g & ((1 << K) - 1)} - {0}) |
                                                 set(rng.sample(sorted(geo.VS), min(12, len(geo.VS)))))
    for sv in svs:
        Os = ref.build_o2p(machine.a2_of(r.prefixes, machine.zperm(gb | sv), COL))
        assert all(r.m.mem[lay['V'] + gen.VSTRIDE * sv + i] == Os[i] for i in geo.needed2()[sv]), sv


def batch_total(count):
    """Exact operations of one batch (2^32 z-steps); count[k] = static body length.  Control
    (block-unrolled, machine.control): ctl_ops before a high body, loop_ops jumps after the
    high bodies and the two chain ends, end_ops once."""
    T = count[None] + machine.loop_ops(None)
    for j in range(32):
        vs = gen.leaf_views(j, K)
        n = (1 << (31 - j)) // len(vs)
        assert n * len(vs) == 1 << (31 - j)
        for sv in vs:
            T += n * (machine.ctl_ops(j) + count[(j, sv)] + machine.loop_ops((j, sv)))
    return T + machine.end_ops()


def layout_check():
    """The block-unrolled layout (machine.layout_trace) executes the bodies (ctz t, gray(t)
    mod 2^K) in step order, its control count equals the formula used by batch_total (for
    batches of 2^nb steps), the chain ends are the bodies loop_ops charges, and every low
    body is at its gen.block_pos."""
    for nb in (K + 1, K + 2, K + 5):
        seq, ops = machine.layout_trace(nb)
        want = [None] + [((t & -t).bit_length() - 1, machine.gray(t) & ((1 << K) - 1)) for t in range(1, 1 << nb)]
        assert seq == want, nb
        f = sum((1 << (nb - 1 - j)) * (machine.ctl_ops(j) + machine.loop_ops((j, (1 << (j - 1)) if j - 1 < K else 0)))
                for j in range(K, nb))
        f += sum(machine.loop_ops(k) for k in seq[1:] if k[0] < K) + 1 + 2 * (nb - K)
        assert ops == f, (nb, ops, f)
    for j in range(K):
        for sv in gen.leaf_views(j, K):
            p, r = gen.block_pos(j, sv, K)
            assert machine.loop_ops((j, sv)) == (1 if r == (1 << K) - 1 else 0), (j, sv)


def static_table_check(leaves):
    """Each table step is ldr w,[K]; xor x,w,C; cmplt f,x,2^128; br f,w,(q mod 2);
    str [K],C; and add C,C,1 after odd q only; no other table access, branch,
    compare or write of the persistent registers 62 (s), 63 (C) exists."""
    for j, code in leaves.items():
        steps, k = 0, 0
        while k < len(code):
            op, d, a, b, imm = code[k]
            if op == 'ldr' and imm is None:
                w, K = d, a
                x, f, br, st = code[k + 1:k + 5]
                assert x[0] == 'xor' and {x[2], x[3]} == {w, 63} and x[1] not in (w, K, 62, 63), (j, k)
                assert f[0] == 'cmplt' and f[2] == x[1] and f[4] == 1 << 128 and f[1] not in (w, K, 62, 63), (j, k)
                assert br[0] == 'br' and br[2] == f[1] and br[3] == w and br[4] == steps & 1, (j, k)
                assert st[0] == 'str' and st[2] == K and st[3] == 63 and st[4] is None, (j, k)
                if steps & 1:
                    assert code[k + 5] == ('add', 63, 63, None, 1), (j, k)
                    k += 6
                else:
                    k += 5
                steps += 1
                continue
            assert op not in ('ldr', 'str', 'br', 'cmplt') and d not in (62, 63), (j, k, code[k])
            k += 1
        assert steps == 256, (j, steps)


def run_setup(pi, seed, geo):
    """Counted batch setup (proof Section 5.1) against the reference: prefix
    constraints, A2 (polarity pi), O2P, all 2^K - 1 views and the delta-swap masks."""
    M64, lay = (1 << 64) - 1, machine.LAYOUT
    B = setup_gen.build_setup(COL, pi, lay['PREF'])
    code, hw, tags = ir.compile_block(B.ins, B.tags)
    code = code + setup_gen.setup_views_code(geo)
    m = ir.Machine(lay)
    m.rng = random.Random(seed)
    beta = seed * 977
    m.reg[63] = (random.Random(seed).getrandbits(128) << 128) + machine.id_of(beta, 0, 0)
    m.run(code)
    pref = []
    for p in range(256):
        b = b"".join(m.mem[lay['PREF'] + 4 * (256 * beta + p) + w].to_bytes(32, 'little') for w in range(4))
        L = [int.from_bytes(b[8 * i:8 * i + 8], 'little') for i in range(16)]
        c4, c1 = L[4] ^ L[9] ^ L[14], L[1] ^ L[6] ^ L[11] ^ machine.PAD16
        assert L[5] == L[15] == c4 ^ machine.rotl64(c1, 1) and L[8] == 0
        assert L[12] == M64 ^ machine.rotl64(c4, 1) ^ L[2] ^ L[7]
        pref.append(L)
    assert len({tuple(L) for L in pref}) == 256
    A2 = machine.a2_of(pref, 0, COL)
    O2P = ref.build_o2p(A2)
    for i in range(1600):
        assert m.mem[lay['A2'] + i] == A2[i] ^ (ir.W if i in pi else 0) and m.mem[lay['O2P'] + i] == O2P[i]
    VN = geo.needed2()
    for sv, ws in geo.VS.items():
        Os = ref.build_o2p(machine.a2_of(pref, machine.zperm(sv), COL))
        assert VN[sv] <= ws
        for i in VN[sv]:
            assert m.mem[lay['V'] + gen.VSTRIDE * sv + i] == Os[i], (sv, i)
        assert all(Os[i] == O2P[i] for i in range(1600) if i not in ws)     # VS[s] is the full difference set
    for d in (1, 2, 4, 8, 16, 32, 64, 128):
        assert m.mem[lay['MASK'] + d] == ref.MASKD[d] and m.mem[lay['MASK'] + 256 + d] == ir.W ^ ref.MASKD[d]
    return len(code), hw, m.count


def run_zt():
    """Counted run setup of the z tables (once per run): ZT[0] = ZT[2^16] = 0,
    ZT[x] = ZT[x AND (x - 1)] XOR 2^ORDER[ctz x], ZT[2^16 + x] likewise with
    ORDER[16 + ctz x]; 3 ops per entry."""
    code = [('xor', 0, 0, 0, None), ('st', None, 0, None, ('ZT', 0)), ('st', None, 0, None, ('ZT', 1 << 16))]
    for hi in (0, 1):
        for x in range(1, 1 << 16):
            lb = (x & -x).bit_length() - 1
            code += [('ld', 1, None, None, ('ZT', (hi << 16) + (x & (x - 1)))),
                     ('xori', 1, 1, None, 1 << machine.ORDER[16 * hi + lb]),
                     ('st', None, 1, None, ('ZT', (hi << 16) + x))]
    m = ir.Machine(machine.LAYOUT)
    m.reg = [random.getrandbits(256) for _ in range(64)]
    m.run(code)
    base = machine.LAYOUT['ZT']
    assert all(m.mem[base + i] == machine.zt_word(i) for i in range(1 << 17))
    return m.count


def main():
    t0 = time.time()
    machine.set_opts(OPTS)
    geo = gen.Geometry(COL, K=K, order=ORDER)
    assert machine.KV == K and machine.ORDER == ORDER
    reads = set().union(*[p[2] for p in geo.P])
    assert all(len(gen.a2_support(COL, j)) == 22 for j in range(32))
    assert {len(p[0]) for p in geo.P} == {499} and len(reads) == 975
    assert (min(map(len, geo.flips)), max(map(len, geo.flips))) == (3, 10)
    assert geo.pi == ref.PI, "storage polarity differs from the experiment's PI"
    VN = geo.needed2()
    print("geometry: 22-word supports, 499 patched words, 975 read words, flips 3..10, |pi| = %d; Gray order %s;"
          " K = %d, %d views of %d..%d words, %d maintained view words (memo2) (%.0fs)" % (
              len(geo.pi), ORDER, K, len(geo.VS), min(map(len, geo.VS.values())), max(map(len, geo.VS.values())),
              sum(map(len, VN.values())), time.time() - t0), flush=True)
    layout_check()
    print("control: block-unrolled layout executes the bodies (ctz t, gray(t) mod 2^K) in step order for batches"
          " of 2^%d, 2^%d, 2^%d steps; control count = formula; per batch %d control ops" % (
              K + 1, K + 2, K + 5, sum((1 << (31 - j)) * (machine.ctl_ops(j) + 1) for j in range(K, 32))
              + (1 << (32 - K)) + machine.end_ops()), flush=True)
    count = {}
    nproc = max(1, min(int(os.environ.get("NPROC", os.cpu_count() or 1)), 16))
    keys = body_keys()
    jobs = list(enumerate(keys))
    hi = [x for x in jobs if x[1] is not None and x[1][0] >= K]      # large bodies: spread them out
    lo = [x for x in jobs if x not in hi]
    gap = max(1, len(lo) // (len(hi) + 1))
    order = []
    for i, x in enumerate(lo):
        if i % gap == 0 and hi:
            order.append(hi.pop(0))
        order.append(x)
    order += hi
    if nproc > 1:
        import multiprocessing as mp
        with mp.get_context("spawn").Pool(nproc, initializer=_winit, initargs=(sys.argv[1],)) as pool:
            out = pool.map(_task, order, chunksize=1)
    else:
        _winit(sys.argv[1], geo)
        out = [_task(x) for x in order]
    byidx = {x[0]: o for x, o in zip(order, out)}
    res = [byidx[i] for i in range(len(keys))]
    shas, nkeys, cands = [], 0, set()
    for k, (n, hw, sha, kc, cs) in zip(keys, res):
        assert hw <= 62, (k, hw)
        count[k] = n
        shas.append([k, sha])
        nkeys += kc
        cands |= set(cs)
    T = batch_total(count)
    digest = hashlib.sha256(json.dumps(shas, separators=(",", ":")).encode()).hexdigest()
    lo = {j: [count[(j, sv)] for sv in gen.leaf_views(j, K)] for j in range(32)}
    print("static body counts: t0 %d; " % count[None] + "; ".join(
        "leaf %d: %d..%d (%d bodies)" % (j, min(v), max(v), len(v)) if len(v) > 1 else "leaf %d: %d" % (j, v[0])
        for j, v in lo.items()))
    print("EXACT ops per batch T = %d; T / 2^32 = %.6f ops per z-step; %d bodies, sha256 %s (%.0fs)"
          % (T, T / 2 ** 32, len(keys), digest, time.time() - t0), flush=True)
    if not DEV:
        assert EXPECT["T"] == T and EXPECT["sha256"] == digest, "differs from the proof"
    print("each body: static table check (256 exact hot paths); run once on the counted simulator from a random"
          " state: %d keys equal key_of_digest(sha3_256(m, 6)); measured == control + static + jump; A2/O2P/views"
          " equal a rebuild (%.0fs)" % (nkeys, time.time() - t0), flush=True)
    rng = random.Random(2026)
    bodies = {}

    def body(k):
        if k not in bodies:
            bodies[k] = compile_body(geo, k)[0]
            assert len(bodies[k]) == count[k]
        return bodies[k]

    class Lazy(dict):
        def __missing__(self, k):
            return body(k)
    leaves = Lazy()

    def mkrun(seed, beta, t0, garbage, hashfn=None):
        return machine.Run(leaves, COL, seed=seed, beta=beta, t0=t0, garbage=garbage, pi=geo.pi, views=geo.needed2(),
                           hashfn=hashfn, geo=geo)
    seq = 0
    for start in (5, (3 << K) - 1, (rng.randrange(1 << 20) << 12) - 21):    # the 2nd: a block from its
        # first (high) step with no memo prefill, so every memo load reads a word the program wrote
        r = mkrun(300 + start % 97, 3, start, "adv")
        for _ in range(40):
            leaf, ops = r.step()
            j, sv = leaf
            assert ops == machine.ctl_ops(j) + count[leaf] + machine.loop_ops(leaf)
            state_check(geo, r, rng)
            seq += 1
    print("simulator: %d consecutive steps from 3 starts (one a block start, no memo prefill), keys exact and"
          " A2/O2P/views equal a rebuild after each (%.0fs)" % (seq, time.time() - t0), flush=True)
    for reset in (True, False):
        r = mkrun(17 + reset, 6, 0, "ones")
        for _ in range(3):
            r.step()
        m = r.m
        r.t -= 1                      # replay step 3 (a low step: no control operation)
        if reset:
            m.reg[63] -= 128          # current pair ids = the stored ones: the equal-message path
        before = len(r.cand_ops)
        leaf = r.control()
        r.written = []
        m.run(leaves[leaf])
        new = r.cand_ops[before:]
        assert len(new) == 256
        cands |= set(new)
    r = mkrun(13, 9, 0, "adv", hashfn=lambda msg: b"\0" * 32)
    try:
        for _ in range(3):
            r.step()
        raise RuntimeError("halt path not taken")
    except machine.Halt:
        halt_ops = r.halted[1]
    print("candidates: replayed z-steps gave 2 x 256 genuine candidates with exact rebuilds; continue costs %s ops,"
          " (3 units each), forced halt %d ops" % (sorted(cands), halt_ops), flush=True)
    n, hw, cnt = run_setup(geo.pi, 5, geo)
    print("batch setup: %d ops, %d registers, equal to the reference incl. the maintained words of the %d views (%.0fs)"
          % (cnt, hw, len(geo.VS), time.time() - t0))
    zt = run_zt()
    print("run setup: z tables ZT, %d ops, equal to zperm" % zt)
    print(json.dumps({"T": T, "ops_per_z_step": T / 2 ** 32, "t0": count[None], "bodies": len(keys),
                      "bodies_sha256": digest, "cand_ops_max": max(cands), "halt_ops": halt_ops,
                      "setup_ops": cnt, "zt_ops": zt}))


if __name__ == "__main__":
    main()
```

<!-- file: cert.py sha256=324e63d4e03cb3664573e43fdd50426f346ad6667a3f849a9c1e90120aca8b0d -->
```python
"""bs11 integer certificate (proof Section 8):  python3 cert.py [T]

Batch count.  NB is fixed by a rule computed here, before and independent of any
run: the smallest number of batches whose success bound of proof Section 7 (under
H1) is at least 0.3905, i.e. 1 - exp(-N(N-1)/2^257) - N^3/6 * 2^-396 - 2^-545
- 2^-100 - 2^-61 >= 0.3905 with N = NB * 2^40 (checked for NB and NB - 1 with
60-digit decimal arithmetic).

Main term: the EXACT operation count T of one batch (2^32 z-steps of 256
messages; printed by selftest.py) times NB.  Per batch at most SB = 2^23
operations of batch setup (the counted setup programs incl. the maintained
view words) and batch-loop control.  Per candidate 3 units + at most 150
operations (measured 111..120 to continue, 80 to halt, + 30 for forming the
padded inputs and reading the digests).  Once per run at most 2^19
operations (z tables 393,213 and c).  One further unit of unassigned
slack.  A 2^100-unit term charges generating the program and all
target-specific search and development by anyone (the program-generation
allowance is 2^50 in 5kyguy's 6e715d9a).  A is the total in units of
2^-28 operations; one unit is K = 2^28 * C operations' worth.  The claim is
the smallest c / 10^5 with A^(10^5) < 2^c * K^(10^5) (rounded up to five
decimals; the five-decimal format follows GordoAR's 5dac3f95)."""
import math
import sys
from decimal import Decimal as D, getcontext
from fractions import Fraction as F
getcontext().prec = 60
C = 1626
NB = 307990341830783024002353940
N = NB << 40
VCAP = N * N // (1 << 141) + N * N // (1 << 148) + (1 << 91) + (1 << 61)
K = (1 << 28) * C
PRE = 1 << 100
RUNOPS = 1 << 19
SB = 1 << 23
T = int(sys.argv[1]) if len(sys.argv) > 1 else 117398575636479          # selftest step 2 (proof Section 8)
CAND, U = 150, 3
DEC = 5


def success_bound(nb):
    n = nb << 40
    return (D(1) - (-(D(n) * D(n - 1) / D(2) ** 257)).exp() - D(n) ** 3 / 6 / D(2) ** 396 - D(2) ** -545
            - D(2) ** -100 - D(2) ** -61)


def A(t, cand=CAND, units=U, vcap=VCAP, sb=SB):
    return ((NB * t + NB * sb + RUNOPS) * (1 << 28) + vcap * (units * C + cand) * (1 << 28)
            + (units * C + cand) * (1 << 28) + K + PRE * K)


def lg(x):
    x = F(x)
    return math.log2(x.numerator) - math.log2(x.denominator)


def claim(a, dec=DEC):
    s = 10 ** dec
    x = lg(F(a, K))
    c = math.floor(x * s) - 2
    ks = K ** s
    while not (a ** s < (1 << c) * ks):
        c += 1
    return c, x


if __name__ == "__main__":
    assert success_bound(NB) >= D("0.3905") > success_bound(NB - 1)
    print("NB = %d batches (%.8f * 2^88), N = NB * 2^40 = 2^%.6f; success bound under H1 %s" % (
        NB, NB / 2 ** 88, math.log2(N), str(success_bound(NB))[:12]))
    if T is None:
        sys.exit("usage: python3 cert.py T")
    a = A(T)
    c, x = claim(a)
    s = 10 ** DEC
    assert a ** s < (1 << c) * K ** s and not a ** s < (1 << (c - 1)) * K ** s
    print("T", T, "ops/z-step %.6f" % (T / 2 ** 32), "claim %.5f" % (c / s), "log2 total %.6f" % x)
    lim = D(2) ** (D(c) / s) * D(K)                   # the claim holds while A < lim (decimal, 60 digits)
    print("slack: T / 2^32 up to %.4f ops/z-step, or up to %d operations per candidate" % (
        (lim - D(A(0))) / D(NB << 28) / D(2) ** 32,
        CAND + int((lim - D(a)) / D(VCAP + 1) / D(1 << 28))))
```

<!-- file: ordergen.py sha256=07bc626cd5713fbffdf71b423e1db492fd49ef2beb89def9447728eeb0504644 -->
```python
"""Gray-order generator (Lemma 12).  Deterministic: python3 ordergen.py [K SEED ITERS]
(we ran 10 12 600) prints the order; it reads only the static patch geometry
of gen.py (patch expressions and A2 supports), never a digest.

Cost model (per z-step, in operations, a proxy for the work of Lemmas 13-14):
  r2   = sum over high Gray bits j >= K of 2^-(j+1) * (1254 + 3 * (number of
         (view, word) pairs that leaf j must patch in the maintained views));
  memo = average saving of a row-level block memo of round-3 chi rows over the
         2^K positions of both block patterns (+11 per reloaded row, -5 per
         row stored for a later reload);
  ctl  = 1 + 2 (K + 1).
The low K bits are searched by simulated annealing (random.Random(SEED), ITERS
proposals, temperature 20 * 0.995^i; the result is the lowest-cost order visited,
the first one on ties); the high bits follow by increasing overlap with the
maintained views.  Same arithmetic as our original search script; this
version finds the first and last occurrence of each class in one pass (the
original rescanned the block), and keeps only the
32 overlap counts per low set, which changes the running time and memory only."""
import gen, ref, random, math, sys
WT = gen.WT
col = (4, 14)
raw = [gen.patch_exprs(col, j, flipfix=False)[0] for j in range(32)]
R = [set(r) for r in raw]
sup = [{64 * L + b for L, b in gen.a2_support(col, j)} for j in range(32)]
ROWS = [[64 * ref._bsrc(X, Y, b)[0] + ref._bsrc(X, Y, b)[1] for X in range(5)] for Y in range(5) for b in range(64)]


def vexpr(low):
    K = len(low)
    VD = {0: {}}
    for sv in range(1, 1 << K):
        acc = {}
        cur = []
        for i in range(K):
            if (sv >> i) & 1:
                for w, e in raw[low[i]].items():
                    e = set(e)
                    for t in list(e):
                        if t != WT:
                            for c in cur:
                                if t in sup[c]:
                                    e ^= {WT}
                    acc[w] = frozenset(set(acc.get(w, frozenset())) ^ e)
                cur.append(low[i])
        VD[sv] = {w: e for w, e in acc.items() if e}
    return VD


def seqs(K):
    return [[(r ^ (r >> 1)) ^ (p << (K - 1)) for r in range(1 << K)] for p in (0, 1)]


cache = {}
EMPTY = frozenset()


def lowstats(low):
    k = tuple(low)
    if k in cache:
        return cache[k]
    K = len(low)
    VD = vexpr(low)
    tot = 0
    need = {s: set() for s in VD if s}
    for seq in seqs(K):
        for ws in ROWS:
            ks = [tuple(VD[s].get(w, EMPTY) for w in ws) for s in seq]
            first, last = {}, {}
            for r, c in enumerate(ks):
                if c not in first:
                    first[c] = r
                last[c] = r
            for r in range(len(seq)):
                c = ks[r]
                if first[c] < r:
                    tot += 11
                else:
                    if last[c] > r:
                        tot -= 5
                    s = seq[r]
                    if s:
                        for w in ws:
                            if w in VD[s]:
                                need[s].add(w)
    memo = tot / (2 * (1 << K))
    ov = [sum(len(R[b] & need[s]) for s in need) for b in range(32)]
    cache[k] = (memo, ov)     # only the 32 overlap counts are kept
    return cache[k]


BASE = 1254


def score(order, K):
    memo, ov = lowstats(order[:K])
    r2 = sum(2.0 ** -(j + 1) * (BASE + 3 * ov[order[j]]) for j in range(K, 32))
    ctl = 1 + 2 * (K + 1)
    return r2 - memo + ctl, r2, memo


def complete(low, ov):
    rest = [b for b in range(32) if b not in low]
    ovs = sorted((ov[b], b) for b in rest)
    return list(low) + [b for _, b in ovs]


def search(K, seed, iters, trace=None):
    rng = random.Random(seed)
    cur = rng.sample(range(32), K)
    cur = complete(cur, lowstats(cur)[1])
    cs = score(cur, K)
    Tt = 20.0
    best = (cs, cur)
    for it in range(iters):
        a = rng.randrange(K)
        b = rng.randrange(32)
        if cur[b] in cur[:K]:
            if trace:
                trace(it + 1, cs, cur)
            continue
        low = list(cur[:K])
        low[a] = cur[b]
        new = complete(low, lowstats(low)[1])
        s = score(new, K)
        if s[0] < cs[0] or rng.random() < math.exp((cs[0] - s[0]) / Tt):
            cur, cs = new, s
        Tt *= 0.995
        if cs[0] < best[0][0]:
            best = (cs, cur)
        if trace:
            trace(it + 1, cs, cur)
    return best


if __name__ == "__main__":
    K, seed, iters = (int(a) for a in sys.argv[1:4])
    cs, cur = search(K, seed, iters)
    print(K, seed, [round(x, 1) for x in cs], cur, flush=True)
```

## Appendix B. Pre-registration of our runs (verbatim)

The file `PREREG.json` exactly as hashed on 2026-10-07 at 09:50:10Z
(SHA-256 `931e662ae5f21abafca60fe829dd769ec1df36f82a6188138fdbb4c9a09ead54`, 2497 bytes), unchanged from bs7. Its `exp7/` paths are
our build directory: `exp7/s3r6_bitslice_birthday.py` is the shipped
`experiments/s3r6_bitslice_birthday.py`, and its `manifest_sha256` is the
hash of the manifest file bytes (Section 10.3). Runs after it are listed
in Section 10.3, including those not planned here (S2, the review
committee runs, the later reviewer runs and the exact replays). "Before any trial of this family" there means our own
trials: 5kyguy's organizer trials of the family (6e715d9a) came earlier
and were not used to choose anything here. No run of the script was made
to build or choose anything in this package.

```json
{
 "created_utc": "2026-10-07T09:50:01+00:00",
 "purpose": "Pre-registration of every experiment run of the v7 (128-byte family) package, fixed before any trial of this family was run. Earlier runs of this script: none. Exactness checks before this file (no trials, no success counts): evalcheck a (59,840 keys) and b (16,320 keys) vs verifier sha3_256(m, 6).",
 "script": "exp7/s3r6_bitslice_birthday.py",
 "script_sha256": "c5d0dd9b4300ec29eff8aced9e0873c5aab3cc0f9298918e8b448162c17d5edb",
 "manifest_sha256": "6fb0a610bb703bc1f6f0f2812e432417adecda9793500905847b10ccb85ce9e1",
 "experiments": [
  {
   "id": "k6r6-ls128-full-width",
   "mask_hex": "1f00000000000000000e0300000000000000c00300000000000000e001000000"
  },
  {
   "id": "k6r6-ls128-spread",
   "mask_hex": "0000c7000000000000000000e01100000000000000f0000000000000e0010000"
  },
  {
   "id": "k6r6-ls128-single-group",
   "mask_hex": "000000000000403c000000000000403c000000000000003c000000000000003c"
  },
  {
   "id": "k6r6-ls128-high-z",
   "mask_hex": "000000e0210000000000000000f0080000000000000078000f00000000000000"
  }
 ],
 "inherited": "Layouts (256x2, 16x32, 1x512, 4x128 with z << 25), the 18-bit masks and N_t = 2^9 are bs4's (949c283b), unchanged; only the message family, prefix label (s3r6-ls128-v1), PI and start planes changed.",
 "runs": [
  "R1: organizer-runner replay (experiments/runner.py, Docker replaced by a local python3 -I subprocess), seed hashsmash-public-seed-v1, holdout_nonce null, 256 trials per experiment.",
  "R2-R4: the same with holdout nonces H1, H2, H3, each secrets.token_hex(16) drawn after this file's SHA-256 is recorded, in that order; recorded in exp7/runlog.jsonl.",
  "R5: local statistics, --local mode, 48 chunks x 256 trials per layout, seed labels v7stat-<layout>-c<k>, k = 0..47.",
  "S: sabotage run of exp7/sabotage.py (16 spread trials per mutation; only caught/not caught is used)."
 ],
 "analysis": "Per run and layout and for the pooled R1-R5 counts: successes, exact two-sided Clopper-Pearson intervals at 95% and at the Bonferroni level 1 - 0.05/24 (24 = 4 layouts x 5 runs + 4 pooled), exact two-sided binomial p-value against the uniform-model value 0.393074 (Bonferroni threshold 0.05/24); masked-pair mean and variance/mean ratio (uniform model: mean 0.499, ratio about 1).",
 "commitments": "No parameter, mask, layout, seed label or trial count is changed after any result; every run is listed (including failed or aborted ones); no run is repeated or dropped."
}
```

The hash record `PREREG.sha256.txt` of the same directory, verbatim (the
nonce lines were appended as each nonce was drawn):

```text
prereg sha256 931e662ae5f21abafca60fe829dd769ec1df36f82a6188138fdbb4c9a09ead54 recorded 2026-10-07T09:50:10Z
R2 nonce bd46009ebe3e0b094c616228743f412c drawn 2026-10-07T09:51:14Z
R3 nonce 24ddca750d9cab391425191615a7a8c5 drawn 2026-10-07T09:51:54Z
R4 nonce 817e871f5368158322f2f79815bd8c96 drawn 2026-10-07T09:52:34Z
```

In the file, "H1, H2, H3" label the nonces of R2-R4; they are not the
heuristic H1, and the file's "holdout nonces" are the participant
nonces of Section 10.3, not organizer holdout nonces. Its commitment "no run is repeated" is discussed under
"Replays" in Section 10.3.
