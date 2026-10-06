# SHA3-256 r6: incremental grouped search with a projected 144-bit key

## 0. Submission status and provenance

This package proposes time_log2124.648, conditional success0.39 and
memory_log2_bytes207 for exploratory review. New experiments await organizer
isolation. Static index, operation and register accounting and the confirmation
calling convention are documented below; no execution of a complete RAM
instruction stream or full-scale search is claimed. Ready status means ready
for independent review, not qualification, proof or human acceptance.

The direct starting point is winglock's unpromoted bfc8c418-1ad7-4982-89af-
70a22f13a638, commit 6a250bf4c5084458a63c8fe2dd76dbb5538f5ca3, screened
124.680. The grouped family and sparse-set idea originate with jaazinn
(0a5b7ae8), bit-plane evaluator and transpose with may93182 (11c46f4d), lane
complementing with tekkac (b001199a, following the Keccak team), and the
last-round diagonal dependency with ercumentyildirim (c7fa1a56/4c969300).
Exact charging precedents are zeeshan8281 (cbf7998d), tekkac (f58275ef), and
mitchuski (02d6a703). All materially reused unpromoted contributors must be
credited on any future submission. None has reviewed this derivative.
Sections 2-4 retain the source's definitions and mathematical lemmas; their
full-key transpose is a reference identity, specialized in Section 5.
Source local measurements and claimed simulator runs are not reproduced
here and are not presented as this draft's evidence.

Our changes: retain only digest bits 112..255, specialize the known-zero
transpose, omit unused last-round inputs and corresponding round-5 stores,
verify every projected match against both complete digests, and bound the
number of confirmations. These changes preserve the fixed target and family
but require a new success heuristic. They are not a cosmetic score change.

## 1. Target and machine

The target is the complete SHA3-256 sponge with zero IV, rate 1088, capacity
512, delimited suffix 0x06, pad10*1, prefix rounds 0..5, and all 256 output
bits. Every message has 64 bytes and needs one permutation. Lane index is
L=x+5y; lane words and the digest integer use little-endian encoding.
For a message digest integer D, the stored key is

    K = D AND (((1 << 144) - 1) << 112).

Only lookup is projected; every output must be two distinct messages with
equal full digests. Source KEYMASK affects only lane 0, so it vanishes under
this projection. No decoded complemented bits remain in K.

The stated machine is a classical 256-bit word RAM with 64 registers. Each
load, store, arithmetic/Boolean operation, shift, comparison, branch,
immediate move and random word is charged once at 1/1626 units. A complete
six-round permutation costs one unit. Literal operands and fixed addresses
are instruction fields; dynamic address arithmetic is charged. The register
budget and direct-immediate convention are explicit interpretations of v5,
not organizer-verified facts. The bound is not claimed for a memory-to-memory
ALU model or for free memory traffic. Every processor's work is included.
## 2. Messages, groups, batches and processing order

For group g the algorithm draws two fresh uniform 256-bit words R0, R1. Their
little-endian bytes form a uniform 64-byte prefix P_g, which is stored. For
z in {0,1}^32:

    m(g, z) = P_g with LE32(z) XORed into bytes 0..3 and into bytes 40..43,

so z is XORed into the low 32 bits of lane 0 (x=0, y=0) and of lane 5
(x=0, y=1). Write g = 256*beta + p, batch beta < 2^88, slot p < 256. Batch
beta runs t = 0, 1, ..., 2^32 - 1 with z = gray(t) = t XOR (t >> 1). At each t
it evaluates the 256 messages m(256*beta + p, gray(t)) and offers them to the
table in processing order q = 0..255, slot

    p = decode_slot(q) = 64*floor(q/64) + 8*(q mod 8) + (floor(q/8) mod 8).

Batches run in order beta = 0, 1, .... Message (beta, t, q) gets the
**message number** n = beta*2^40 + t*2^8 + q, which is also the count of
messages processed before it. Every message is evaluated exactly once, and
N = 2^128.

**Bit mapping.** Word P(L, b) holds in bit position p the bit b of lane L of
message m(256*beta + p, z). Row p of input matrix w (w = 0, 1) is R_w of slot
p; after the transpose (Lemma 5), row k of matrix w is plane
P(4w + floor(k/64), k mod 64). Padding planes are constants: P(8,1) = P(8,2)
= P(16,63) = all-ones; all other planes of lanes 8..24 are 0.

## 3. Dependency analysis (exact)

Every step map except chi is GF(2)-linear on the 1600-bit state. Fix a group
and view each state as a function of z. A2 denotes the state after round 1
and the theta of round 2, which is the input of round-2 rho/pi.

**Lemma 1 (round-1 theta is invariant).** Lanes 0 and 5 lie in column x = 0
and carry the same difference z. Every column parity C[x] = XOR_y A[x+5y] is
therefore independent of z, and so is D[x] = C[x-1] XOR rot(C[x+1], 1). Hence
theta(A(z)) = theta(A(0)) XOR (z in lanes 0 and 5).

**Lemma 2 (A2 is affine in z).** Rho/pi sends lane 0 to position 0 (row 0,
rotation 0) and lane 5 to position 16 (row 3, x = 1, rotation 36). Chi acts
on each row separately as A'[x] = B[x] XOR (NOT B[x+1] AND B[x+2]). Rows 0 and
3 each contain exactly one varying input, so no AND multiplies two varying
inputs. With c a group constant, v -> (NOT v) AND c and v -> (NOT c) AND v are
affine in v. The round-1 output is therefore affine in z, and iota and round-2
theta are affine. So A2(z) = A2(0) XOR sum_j z_j L_j exactly, with fixed
vectors L_j (depending on the group). This is plain algebra.

**Lemma 3 (62-word support).** Let j' = (j + 36) mod 64. The round-1 output
varies only in bit j of lanes 0, 3, 4 and in bit j' of lanes 15, 16, 19. The
changed column parities are C[0] at j and j', C[3] at j, C[4] at j and j', and
C[1] at j'. Since C[c][b] enters D[c+1][b] and D[c-1][b+1], the D words that
can change are (x, b) = (1,j), (4,j+1), (1,j'), (4,j'+1), (4,j), (2,j+1),
(0,j), (3,j+1), (0,j'), (3,j'+1), (2,j'), (0,j'+1) (bits mod 64): 12 pairs,
60 words P(x+5y, b). The directly varying (3,j) and (19,j') make 62. So L_j
vanishes outside the fixed list SUPPORT_j of 62 words, and Gray order gives
A2(gray(t)) = A2(gray(t-1)) XOR L_{ctz(t)}.

## 4. Bitsliced Keccak, encodings and the transpose (exact)

**Lemma 4 (bitsliced round).** Write pisrc(X, Y) = (x, y) with y = X and
x = 3(Y - 3X) mod 5, the inverse of pi. On planes the round is: theta
C[x][b] = XOR_y P(x+5y, b), D[x][b] = C[x-1][b] XOR C[x+1][b-1],
A'(L, b) = P(L, b) XOR D[x][b]; rho/pi B(X, Y, b) = A'(L, (b - RHO[L]) mod 64)
with L = x + 5y, (x, y) = pisrc(X, Y); chi P'(X+5Y, b) = B(X,Y,b) XOR
(NOT B(X+1,Y,b) AND B(X+2,Y,b)); iota complements P'(0, b) for each bit b of
RC. Every operation is bitwise, so in bit position p it is exactly the scalar
round on message p. Rotations only change which address is read.

**Lemma 5 (transpose).** For d in {1, 2, ..., 128} let M_d have bit c set iff
c AND d = 0. A delta swap of rows a = R[i], b = R[i+d] (i AND d = 0) is
`t = a SHR d; t = t XOR b; t = t AND M_d; u = t SHL d; a = a XOR u; b = b XOR t`
(6 operations) and exchanges entries (i, c+d) and (i+d, c) for c AND d = 0.
Stage d applies it to all 128 such row pairs and swaps bit log2(d) of the row
index with the same bit of the column index. The 8 stages act on different
index bits, so they commute, and all 8 in any order transpose the matrix.

**Lemma 6 (incremental round 2).** Let O2P be the round-2 output (chi, iota)
with the round-3 theta applied, stored in the lane-complement encoding Q3 of
Lemma 8. When A2 changes by L_j on SUPPORT_j, rho/pi sends the 62 words to 60
distinct chi rows (58 rows with one changed input, 2 rows with two; the map
(L, b) -> (X, Y, plane) is a bijection, fixed by j). For a row with one
changed input a[X] -> a[X] XOR c, the exact output difference is
dout[X] = c, dout[X-1] = c AND a[X+1], dout[X-2] = (NOT a[X-1]) AND c (indices
mod 5; a[X+1], a[X-1] are unchanged). For a row with two changed inputs the
program loads all 5 old inputs, forms the new ones and computes
dout[k] = (n[k] XOR o[k]) XOR (NOT n[k+1] AND n[k+2]) XOR (NOT o[k+1] AND o[k+2])
for the affected k. Then dC[x][b] = XOR_Y dout(x, Y, b) and
dD[x][b] = dC[x-1][b] XOR dC[x+1][b-1], and O2P(x+5Y, b) ^= dout(x, Y, b) XOR
dD[x][b]. Theta is linear and the encoding is XOR with a constant, so the
patched O2P equals the encoded theta'd round-2 output of the new A2 exactly.
Terms that are structurally zero for this j emit no code. The source claimed 4149 operations for a fused schedule. This draft instead
uses the independently specified three-pass schedule below, charging5136.

**Lemma 7 (theta at the store).** In a round, plane b's 25 chi outputs are
held in registers, so the column parities C'[x][b] of the output are complete
before any store, and D'[x][b] = C'[x-1][b] XOR C'[x+1][b-1] is available for
b >= 1 from the previous plane's parities (kept in 5 registers). Each output
word of plane b >= 1 is stored with D'[x][b] already added. Plane 0 is stored
without it; after plane 63, fix[x] = D'[x][0] = C'[x-1][0] XOR C'[x+1][63]
stays in 5 registers, and the next round XORs fix[x] into each loaded word
whose source plane is 0 (25 words, one per lane). The stored state plus the
fix is exactly the theta'd state, so the next round needs no theta pass.

**Lemma 8 (lane-complement encoding).** Each stored lane L has a compile-time
polarity bit pi_L: the stored word is the true word XOR pi_L * (all-ones).
For one chi row with input polarities and wanted output polarities, NOT b AND
c equals s_b AND s_c when (pi_b, pi_c) = (1, 0), and NOT(s_b OR s_c) when
(0, 1) (the OR result then has polarity 1). For other combinations a
complemented copy of one input is formed (one NOT, shared within the row).
The output polarity is pi_a XOR (gate polarity) XOR (iota bit); if it differs
from the wanted one, one NOT is added. For each (row polarities, wanted
outputs, iota) the program uses the cheapest plan found by exhaustive search
over the 32 complemented-copy sets and both gate choices. Theta on encoded
words: the stored parity is the true parity XOR the parity of polarities, so
the theta'd next-round input has polarity fpol(pout)_L = pout_L XOR pc[x-1]
XOR pc[x+1], pc[x] = XOR_y pout_{x+5y}. The chosen patterns are P34 (output of
rounds 2, 3, 4; lanes 0,4,8,9,13,14,18,20 complemented) and P5 (output of
round 5; lanes 0,4,8,9,13,17,20), so rounds 3 and 4 and round 5 read
polarity Q3 = fpol(P34) and the last round reads fpol(P5). With them, every
chi row of rounds 3, 4 and 5 costs exactly 1 NOT (iota absorbed). In the last
round each plane's 4 digest outputs take whichever polarity costs no NOT; the
resulting fixed bits form KEYMASK (lane 0 complemented except bits 0 and 31;
lanes 1-3 plain; 62 bits set). All gates are exact; no data-dependent choice
is made. A2 is stored unencoded; the incremental updates of Lemma 6 are
differences and preserve the Q3 encoding of O2P.

**Lemma 9 (fused last round and transpose order).** Key row r = 64x + b
(x < 4) is digest-lane x, bit b. For block g = 0..7, the last round computes
the 32 rows with b = 8g + bl (bl < 8), x < 4, in registers (register index
8x + bl), applies the delta-swap stages d = 1, 2, 4 (row bits of bl) and
d = 64, 128 (row bits of x) inside the block, and stores the 32 rows. Phase 2
then loads, for each of the 32 pairs (x, bl), the 8 rows 64x + 8i + bl
(i < 8), applies stages 8, 16, 32 and hands row 64x + 8i + bl straight to the
table. By Lemma 5 all 8 stages are applied exactly once, so row r ends as the
256-bit key of slot r; the offer order is q = 8(8x + bl) + i, i.e. slot
decode_slot(q) of Section 2.

## 5. Projected evaluator and exact specializations

Use the grouped family, order and affine/incremental evaluator in Sections
2-4. The following specializations act only after the round-4 output.

### 5.0 Independent incremental schedule and register bound

The source's 4149-operation fused schedule is not imported as an established
cost. Use the following three-pass schedule with explicit scratch arrays.
All support lists, addresses and row memberships are compile-time constants
for each of 32 duplicated Gray-bit blocks. No runtime dictionaries, support
searches or variable-address list traversals are hidden in this schedule.

For each affected chi row form its output difference dout and store it.
A single changed input costs12 operations: one coefficient load, one old
A2 load, XOR and A2 store (4); two neighbor loads (2); one NOT and two
ANDs (3); three delta stores (3). There are58 such rows, costing696.
Two other rows have two changed inputs each. Load five old inputs and two
coefficients, XOR the two changes and store them (11 per row). For each
affected output x, the linear difference aliases its coefficient if x
changed. If neither nonlinear gate input changed, the nonlinear difference
is zero and costs nothing. Otherwise compute old and new NOT/AND gates and
XOR them (5), adding one XOR for a changed linear term. Store each delta.
The two rows together cost68. Total first pass:764, producing183 deltas.

Second, for each of145 structurally nonzero column-parity locations,
load its dout terms, XOR-reduce them, and store dC. A location with k terms
costs k loads+(k-1) XORs+one store=2k. There are183 terms overall:366.

Third, for each of215 induced dD locations, load its one or two dC terms,
XOR if needed, and retain dD in a register while patching its five state
words. There are290 dC contributions: cost2*290-215=365. Merge the direct
dout difference with dD in the destination register before storing O2P.
The union of affected destinations has1090 words. Charge three operations
(load/XOR/store) for every destination, plus two (dout load/XOR) for each
of183 direct differences:3636. This deliberately overcharges destinations
having only a direct difference; do not rely on that excess for other work.
A branch to the common round-3 block costs one. Thus

    764 + 366 + 365 + 3636 + 1 = 5132; charge5136.

Independent index-only enumeration of all32 j values gives the same counts:
62 input words;58 single-input rows and2 double-input rows;183 dout words;
145 dC locations;215 dD locations;1090 patched state words. This enumeration
is a static geometric calculation, not a run of any participant hash code.
The diagnostic evaluator now follows the three-pass construction and
asserts its support sizes; organizer execution remains pending.

For register allocation, persistent s,n,SB,ONE and the confirmation counter
use5 registers. Incremental rows need at most5 old+5 new+2 coefficient+3
scratch registers, at most20 including persistent state. dC reduction and
dD patching use fewer. For rounds3-5 allocate25 output,5 input,1 complement,
1 gate scratch, two5-word parity buffers,5 plane-zero parities and5 incoming
fix registers, plus5 persistent:57. The outgoing fix can reuse incoming
fix storage once the round completes. LAST uses32 output rows,5 inputs,
5 masks,5 fixes and3 temporaries plus5 persistent=55. Phase2/table uses
fewer. Confirmation spills/restores all64 registers within its separate
allowance. These are explicit allocation upper bounds, not a measured
high-water mark. Full instruction-stream validation remains desirable.

### 5.1 Retained last-round outputs

For output plane b<48, retain chi outputs x=2,3. Their input union is
{B0,B2,B3,B4}: B1 is not loaded. For b>=48 retain x=1,2,3 and all five
inputs. Each retained output uses one AND/OR and one XOR, with no NOT in
the inherited polarity plan. In particular, 112 omitted outputs save 224
operations, and omission of B1 for b=0..47 saves 48 loads.

B1 is rho/pi of lane 6, whose rotation is 44. Its unused source planes are
(b-44) mod 64, namely 20..63 and 0..3. Round 5 still computes every chi
output and column parity, but omits these 48 lane-6 stores. It also omits
the associated theta XOR on the 47 nonzero planes. Plane 0 was already
stored without theta, and the deferred fix XOR at last-round plane b=44 is
now unused. Total round-5/last-fix saving is 48+47+1=96. Keeping all five
D values and fix registers gives a conservative bound; no additional
savings are assumed.

### 5.2 Known-zero transpose

Before transpose, rows 0..111 are zero; rows 112..255 are the retained
bit planes. The same stages 1,2,4,64,128,8,16,32 apply. Each delta swap
with known-zero inputs is specialized at compile time:

- Both zero: emit nothing, both outputs remain known zero.
- Left zero: t=b AND M; a=t SHL d; b=b XOR t (3 operations).
- Right zero: t=(a SHR d) AND M; a=a XOR (t SHL d); b aliases t
  (4 operations, register naming does not execute a move).
- Neither known zero: the ordinary 6-operation swap.

These are substitutions into the exact delta-swap identity, not
probabilistic assumptions about zero values. Destinations that were known
zero are assigned before reading; both-zero rows need no materialization
until they meet a live row. Static register renaming handles aliases.

| stage | both zero | left zero | right zero | neither | operations |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 56 | 0 | 0 | 72 | 432 |
| 2 | 56 | 0 | 0 | 72 | 432 |
| 4 | 56 | 0 | 0 | 72 | 432 |
| 64 | 48 | 16 | 0 | 64 | 432 |
| 128 | 0 | 96 | 0 | 32 | 480 |
| total | | | | | 2208 |

The baseline phase costs 3840, so 1632 operations are saved. All rows are
structurally live afterwards; phase 2 is left unchanged. Per 32-row fused
block this is 240 operations for each of six blocks with 16 live inputs,
and 384 for each of two blocks with 24 live inputs. No extra row buffers
are needed. An allowance of 8 extra instructions per z-step covers one
zero initialization per block if required by the final allocation.

### 5.3 Setup

Batch setup (once per batch of 2^40 messages):

1. Draw 512 random words (RAND); store each to PREF + 512*beta + 2p + w and to
   STATE0 + 256w + p. 2. Transpose both 256 x 256 matrices. 3. Store the 1088
   padding planes. 4. Compute the round-1 D words. 5. Run round 1 (plain
   encoding) and form A2 = STATE1 XOR D for all 1600 words. 6. For j = 0..31:
   complement P(0, j) and P(5, j), rerun round 1 (D words reused, Lemma 1),
   store COEF[j][k] = A2(e_j) XOR A2(0) on SUPPORT_j[k], restore.
7. Build O2P: round 2 from A2 with output polarity P34 and theta at the store
   (Lemma 7), then apply the plane-0 fix in memory. 8. s = 0.

The source specifies483643 operations per batch under the direct-address
convention. This is not imported as an exact charge for our setup.

The setup count just quoted is a source ledger, not a new measurement.
We provision 2^20 operations per batch, including all setup, prefix draws,
initial round-2 construction and batch-loop control. A further 2^20 global
operations cover fixed masks, cap counter, scratch initialization and code
constant preparation. Setup does not use a stored collision or advice.

## 6. Sparse table, confirmation and halting

Use the top 140 bits, h=K SHR 116, with S at word address 2^200 and DK[n]
at word address n. S is never initialized. Before processing message n,
DK[0..n-1] contains the ACTUAL projected key of each preceding message,
including messages that caused a declined projected match. No dummy value
is written. Prefixes are retained at 2^170, and scratch is relocated to
2^180 (the source used 2^240; that layout is not used here).

    h = K SHR 116; a = SB + h; i = LOAD[a]
    if i < n and LOAD[i] == K:
        if confirmations == 2^112: halt with failure
        confirmations += 1
        decode ids i,n; rebuild their messages from retained prefixes
        compute both complete target digests
        if messages are distinct and digests equal: output pair and halt
        STORE[n] = K; n += 1; continue  # retain S[h]'s representative
    else:
        STORE[n] = K; STORE[a] = n; n += 1

The non-match path has the source's at-most-11 operations. The branch into
confirmation occurs only after a successful projected comparison. All extra
work on that path, including the cap check, save/restore, storing the actual
key and incrementing n, is charged to the confirmation allowance below.
The sparse pointer may initially contain any word. If i<n it always denotes
a real preceding message because every DK entry below n has been written.
If its key equals K, even an untouched bucket therefore leads to a genuine
projected pair; garbage cannot manufacture extra confirmations unrelated
to equal projected keys.

A confirmation reconstructs beta=id>>40, t=(id>>8) mod 2^32, q=id mod 256,
p=decode_slot(q), group=256*beta+p, z=gray(t); load both prefix words and
XOR z into the two specified 32-bit positions. Both full target hashes are
then checked. Spilling/restoring all 64 registers costs 128 loads/stores.
Budget 256 primitives for decoding, prefix addressing, message construction,
distinctness and full-digest comparisons; 256 for operand/result marshaling
around the two permutations; 256 for cap, spills' addressing, table update,
return control and output handling. This subtotal is below 1024; charge
4096 operations plus two permutations per attempted confirmation. The
compiled calling convention still needs auditing against this allowance.
No successful truncated match is output without the full check.

### 6.1 Explicit confirmation calling convention

Each unrolled table offer has a fixed continuation label. On MATCH, write all
64 registers to fixed spill slots, and enter the cold block. The message ID n,
key K, prior ID i and confirmation counter have designated spill slots. Check
the counter from its slot; if it is already2^112, halt with failure. Otherwise
increment its spill slot, so a later restore preserves the updated counter.
The fixed return label is an instruction field saved in one scratch slot.
Cold code uses at most32 registers; no original live register is assumed free.

For each ID, form beta,t,q with shifts/masks. Decode p using shifts by6 and3,
masks63/7 and two ORs. Form group=(beta<<8)|p and z=t XOR(t>>1). Prefix address
is PREF+2*group. Two loads recover the prefix; XOR z into word0 and z<<64 into
word1 (bytes40..43 are bytes8..11 of word1). This takes fewer than32 primitives
per ID; charge64 per ID, including temporary moves and the two prefix loads.
Retain both two-word messages in distinct fixed scratch slots.

For each message prepare the25 scalar lanes at fixed addresses: extract its
8 message lanes with shifts/ANDs, set the remaining lanes to zero except suffix
lane8=0x06 and final rate lane16=1<<63. The two selected six-round permutation
calls are each charged1 unit. Assemble the first four output lanes into the
256-bit digest with shifts/ORs. A128-primitive allowance per permutation covers
all input/output loads/stores, constant moves and this packing; the permutation
internals are charged only through the separate unit cost.

Compare both message words and both digests. On failure load n and K from the
spill image, write DK[n]=K and increment the n spill slot. S is unchanged.
Restore64 registers, including updated n and confirmation count, and branch
to the saved label. On success serialize both64-byte messages and halt; no
restore is necessary. The fixed spill and scratch regions are disjoint from
all round state, prefixes and lookup arrays.

| cold block | conservative primitive budget |
| --- | ---: |
| spill64 registers and restore64 | 128 |
| cap test, updated counter slot and return-label bookkeeping | 32 |
| two ID decodes, prefix addressing, loads and message reconstruction | 128 |
| two permutation input/output marshalings | 256 |
| message inequality and full-digest comparison | 32 |
| actual-key store, updated n slot and return branch | 32 |
| successful output serialization | 64 |
| total, excluding the two separately priced permutations | 672 |

Charging4096 rather than672 leaves ample explicit allowance without changing
any hot-path count. All addresses in this block are either fixed instruction
fields or explicitly formed as above. The budget applies to declined and
successful confirmations and includes the terminal cap check. No same-key
collision is accepted without the full digest comparison.

## 7. Correctness and probability

Projection and transpose are exact Boolean specializations; incremental
rounds and polarities remain as in Sections 2-4. Output correctness follows
from the independent full target check and message-distinctness check,
regardless of the probability assumptions. The algorithm is bounded: at
most N=2^128 messages and R=2^112 confirmations, with no restart.

Define four failure events over fresh independent uniform group prefixes:

- Fdup: two different groups contain the same message.
- Fnone: no full digest collision among all N messages.
- Fobstruct: a full-colliding pair and a distinct third message share the
  pair's top-140-bit bucket. The third message can precede or intervene
  between the pair; this deliberately overcounts harmless triples.
- Fcap: more than R equal projected-key pairs among the N messages.

If none occurs, a full colliding pair (a,b), a before b, is not hidden.
At a, a prior projected match would identify a third message in its bucket,
contrary to not-Fobstruct. Thus S points to a after processing a. No other
bucket occupant occurs before b, so b confirms against a. Fcap guarantees
that the cap cannot prevent this confirmation. Each confirmation corresponds
to a distinct index pair (i,n), so the number attempted is at most Q, the
number of equal projected-key pairs. Storing actual DK keys on declined
matches is essential to this argument.

Fdup has an unconditional bound: each of fewer than 2^191 group pairs needs
a prefix XOR in a 2^32-element subspace of 512 bits, giving Pr(Fdup)<2^-289.

For the iid uniform 256-bit COMPARISON MODEL, independently of whether that
model applies to the real fixed hash family:

1. Pr(Fnone) <= exp(-N(N-1)/2^257) < 0.6065307.
2. For each ordered triple (a,b,c), full equality of a,b costs 2^-256
   and matching c's bucket costs 2^-140. Fewer than N^3 triples give
   Pr(Fobstruct)<2^-12. This bound includes preceding blockers, which the
   unmodified full-key source analysis did not need to include.
3. Q is the sum of indicators of equal 144-bit projections. Each has
   expectation 2^-144. Indicators of disjoint pairs are independent;
   overlapping pairs also have product expectation 2^-288, because equality
   of three independent uniform 144-bit strings has that probability.
   Thus mu=E(Q)<2^111, Var(Q)<=mu. Chebyshev gives
   Pr(Q>2^112) <= Var(Q)/(2^112-mu)^2 < 2^-111.

Hproj, the SCORE-CRITICAL HEURISTIC, says that for this fixed grouped family
and deterministic processing order, Pr(Fnone union Fobstruct union Fcap)
is at most the sum of these iid comparison bounds plus 0.003. Source H1
does not imply Hproj: it did not cover this projected representative policy
or confirmation tail. We state the stronger premise explicitly rather than
silently transfer the source's qualification.

Conditional on Hproj,

    Pr(success) > 1 - 0.6065307 - 2^-12 - 2^-111 - 0.003 - 2^-289
                > 0.3902251593749999 > 0.39.

This is conditional algebra, not an experimentally established success
bound. The 0.003 excess allowance and full-run tail remain unresolved.
Cross-group pairs have collision expectation at least 2^-256 by the source's
Cauchy-Schwarz argument, but expectation alone does not prove Hproj.

## 8. Operation ledger and proposed time

| block | source operations | draft operations |
| --- | ---: | ---: |
| Gray control | 16 | 16 |
| incremental round 2 | 4149 | 5136 |
| round 3 | 9895 | 9895 |
| round 4 | 9920 | 9920 |
| round 5 | 7380 | 7285 |
| last round and first five transpose stages | 4938 | 3033 |
| phase 2 and 256 non-match table paths | 5379 | 5379 |
| loop | 2 | 2 |
| zero initialization allowance | 0 | 8 |
| total | 41679 | 40674 |

Round 5 saves 48 stores and 47 XORs. Last round saves 224 chi operations,
48 loads, one deferred-fix XOR and 1632 transpose operations, totaling 1905.
The retained rounds' source formulas are 64*(25+55+20+25)+63*30+5=9895,
then +25 input fix XORs=9920. Round 5 starts at
64*(25+55+20+5)+63*10+25+5=7380. Phase 2 is
3+32*(8+3*4*6)+256*11=5379. The independent incremental count and explicit register allocation are in
Section5.0. No source simulator was run, and no measured instruction count
is claimed. The source fused4149 schedule is replaced, not certified.

There are 2^120 z-steps. The proposed all-runs upper bound is

    T <= (40674*2^120 + 2^108 + 2^20)/1626
         + 2^112*(2 + 4096/1626).

The second numerator term is setup for 2^88 batches at 2^20 operations each.
The final term includes all successful and declined confirmations. Direct
high-precision scalar arithmetic gives log2(T)=124.6457254552517289..., below
the proposed 124.648. The rounding margin is not a substitute for missing
operations. Under a stricter model with extra direct-address arithmetic,
the source 11640 direct accesses per step alone add about 0.37 bits;
this draft must not advertise 124.648 under that convention.

## 9. Memory and advice

DK occupies at most 2^128 words; S has 2^140 words starting at 2^200;
PREF has 2^97 words starting at 2^170. Place scratch, constants and spills
at 2^180, below 2^181, and code below 2^190. These ranges are disjoint.
Even counting the entire word-address span through S, total storage is
less than 2^202 words, hence less than 2^207 bytes. This deliberately
conservative bound is independent of whether holes in the address space
are charged. It requires the explicit scratch relocation stated above.
No source address at 2^240 survives in the proposed schedule. Memory is
reported but unscored. There is no nonuniform advice and no stored collision;
all runtime setup and randomness are included in T.

## 10. Declared finite experiments, not yet run

Four fresh experiment IDs use layouts 256 groups x 2 steps, 16 x 32,
1 x 512, and 4 x 128 with z bits 25..31. The evaluator checks retained
144-bit keys against its full-key path and an independent scalar sponge;
unused lane-6 stores are zeroed to catch unintended reads; all coefficient
support and final incremental-state rebuild assertions remain.
The zero-aware transpose records its structural count, but participant
observations do not independently certify operation cost.

Each finite table uses an 18-bit organizer-checked event inside the retained
projection, a 16-bit key, a 14-bit bucket and a cap of 64 declined matches.
The different masks start at digest bits 112,144,180,230. Sparse slots are
initially represented by arbitrary potential IDs, not guaranteed-invalid
sentinels; every processed key and its real message identity are retained.
On a projected match the evaluator checks the 18-bit event by rehashing.
Only an organizer-verified event pair can count as a finite success.

These are implementation and table-policy analogues. Their bucket and key
collision rates are not a faithful scaling of the full 256/144/140-bit
search. Do not compare their success counts directly with 0.39307 or claim
they measure the 0.003 allowance. The evaluator continues after its first
success to gather diagnostics; production would halt at that first success.
If no success occurs, every match is declined and the cap policy agrees.
The Python evaluator also computes an unprojected reference and extra
assertions; those diagnostics are not claimed as the costed RAM program.

No participant source has been run on the host. New experiments must run
only in the organizer's isolated executor. Previous source measurements
are historical author reports, not new derivative results. Static AST
parsing and index/count arithmetic are the only new local checks so far.

## 11. Heuristic limitations and source review obligations

The public source remains AI-qualified and awaiting manual review, not
human-accepted or promoted. Its obligations include LC-F1/LC-F2 time and
success-budget uncertainty, F-H1-FULLSCALE-GAP, F-EVAL-1 and finite-scale
statistical/extrapolation gaps. This derivative does not discharge them by
citation. The projected-key policy adds a tail premise and must receive
fresh review. Finite masked experiments cannot exclude adverse full-width
structure, correlated group tails or late-time distribution changes.
The word-RAM register convention also remains an interpretation.

## 12. Static audit and evaluation boundary

The independent geometric enumeration covers all32 Gray-bit supports and gives
the same5132 incremental instructions, charged5136. The projected transpose
has the2208 exact primitive count in Section5.2. Sections5.0 and6.1 allocate
the live registers and explicitly cover cold-path preservation. The remaining
phase totals follow the unrolled formulas in Section8; no indexed dictionary
or support construction is a hidden runtime operation. The11-operation worst
non-match table path counts shift, address addition, load, comparison, branch,
key load, comparison, branch, two stores and n increment. The Gray decision
tree costs one increment plus five AND/compare/branch triples. Every lookup
is offered even after a declined projected match.

Local checks consist of AST parsing, static geometry/cost calculations,
mechanical package validation and whitespace review. These are not candidate
execution. A complete instruction-stream interpreter has not been run. The
Python diagnostic evaluator intentionally performs extra reference work and
is not presented as an instruction-priced implementation. Fresh organizer
experiments and AI review must evaluate this changed package. The full-width
heuristic and machine-convention limitations remain disclosed in Section11;
this submission requests exploratory adjudication rather than claiming they
are resolved by finite tests.
