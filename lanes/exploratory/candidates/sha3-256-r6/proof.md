# SHA3-256 prefix rounds 0-5: bit-sliced distinguished-point collision walk

Lane: exploratory. Target: `sha3-256-r6-prefix-v1`. Attack class: ordinary
collision. Cost model `collision-frontier-v5`, C = 1626: one six-round sponge
permutation costs 1 unit; every other 256-bit RAM word operation costs 1/1626.

## 0. Claim

* Output: two distinct 32-byte messages whose complete six-round SHA3-256
  digests agree on all 256 bits (Section 6, unconditional).
* Time: at most 2^125.5787186 units in every run (Section 8), under the fixed
  register-bank convention of Section 2 with one placement charged per gate
  result. Claimed `time_log2: 125.58`.
* Success: at least 0.4218060 under one heuristic, H-RF (Sections 7, 11).
  Claimed 0.42 (rounded down; 0.0318 above the 0.39 gate).
* Memory below 2^112 bytes; preprocessing at most 2^8.1485 units, declared
  2^9; advice zero (Section 9).

This is a generic birthday attack: van Oorschot-Wiener parallel collision
search with distinguished points (DPs), with 256 chains carried in the 256
bit positions of each RAM word. The step map is a straight-line Boolean
circuit on bit planes whose digest planes become the next input planes, so no
transpose or sort is on the per-evaluation path. No cryptanalytic advance on
SHA3 is claimed. `baseline_improved` names the nominal reference only.

## 1. Target and step map

N = 2^256. For a 256-bit word x, msg(x) = LE32(x) (32 little-endian bytes);
msg is injective. A 32-byte message pads to one 136-byte block
`m || 06 || 00^102 || 80` (SHA3 suffix 01, pad10*1). The state is 25 lanes
A[0..24], index x+5y, 64 bits each, all-zero IV. After absorbing:
A[0..3] = the four lanes of x, A[4] = 0x06, A[16] = 2^63, all others 0.

PERM6 applies Keccak-f[1600] rounds 0..5 (prefix convention). Per round,
indices mod 5, lane arithmetic on 64 bits:

    C[x] = A[x,0]^A[x,1]^A[x,2]^A[x,3]^A[x,4]
    D[x] = C[x-1] ^ rot64(C[x+1], 1)
    B[y, 2x+3y] = rot64(A[x,y] ^ D[x], rho[x+5y])
    A[x,y] = B[x,y] ^ ((NOT B[x+1,y]) AND B[x+2,y])
    A[0,0] ^= RC[round]

rho (x+5y order): 0,1,62,28,27, 36,44,6,55,20, 3,10,43,25,39, 41,45,15,21,8,
18,2,61,56,14. RC: 0x1, 0x8082, 0x800000000000808A, 0x8000000080008000,
0x808B, 0x80000001. The digest is lanes A[0..3] little-endian. Define
f(x) = A[0] + 2^64 A[1] + 2^128 A[2] + 2^192 A[3] after PERM6, so LE32(f(x))
is the digest of msg(x). "Digest bit i" is bit i of f(x) (byte i/8). If
x != x' and f(x) = f(x'), then msg(x), msg(x') are an ordinary collision.

## 2. Machine model and register-bank convention

Primitives (each 1/1626): 256-bit load, store; add/sub mod 2^256; AND, OR,
XOR, NOT; shift/rotate; compare; conditional branch; RAND (fresh uniform
256-bit word). A compare plus its branch is 2; a jump is 1; writing a
constant is 1. Instruction fetch is not charged; program text counts as
memory. The algorithm never reads memory it has not written. A scalar
permutation call (RELOCATE and OUTPUT only) costs 1 unit plus at most 192
operations for lane writes, reads and control.

**Convention.** The fixed register-bank convention of #148 (126.995), #170
(126.92) and #178 (126.902). #178's proof states, verbatim: "The program has
a fixed finite register bank of fewer than 2^14 words, independent of n. ...
Registers and their stored values count toward memory. Primitive
instructions read their named register operands as part of the operation;
indirect main-memory loads and stores are charged below." Its round table
"additionally charges a placement for every logical result, beyond its
primitive's normal result write." In the review dossiers we downloaded, each
of the three was scored `plausible_not_refuted` with no cost-lane finding
against this convention; that acceptance is reported, not verifiable here.
We adopt it as follows:

* The circuit's working values live in a fixed bank of at most 2050 words
  (Lemma 2.1), independent of message and chain counts. The allocation is
  static (fixed when the program is written; no run-time cost).
* Each gate is one operation reading its named bank operands, plus **one
  placement (bank store) per gate result**.
* The START and SB slot arrays and the trie are main memory: every access to
  them is a charged load or store (Section 5).

Under winglock 377eebd's stricter narrow 64-register file with +1 per direct
access, our 1600-plane state would spill: an optimal (Belady) schedule of our
program needs about 59,000 direct accesses per 256-evaluation batch, about
605 operations per evaluation, giving 2^126.64. We do not claim that model.

**Lemma 2.1 (bank size).** Each gate result is live from its definition to
its last use; the 256 digest results to the end of the batch; the 256 input
planes from the batch start to their last use in round 0. For straight-line
code, linear-scan allocation (lowest free word at definition, freed after
last use) needs exactly the maximum number of simultaneously live values. An
exact liveness scan of the generated program (Appendix A) gives 2048 if a
result may take the word of an operand dying at the same gate and 2049 under
strict intervals, plus one word for the materialised-NOT temporary: at most
**2050 words**. Per-round strict maxima: round 0: 1730; rounds 1-4: 2049;
round 5: 1601. The 36703 result names are reused; at most 2050 are resident.
At the end of each batch the 256 digest values are copied into fixed
input-plane words P[0..255] (256 charged copies, Section 3).

## 3. The bit-sliced step circuit

A batch evaluates f on 256 inputs; word P[i] holds bit i of x_j at bit j.
Constant lanes have no plane. A signal is a public constant bit or a stored
plane word s with a public flag phi (true value s XOR phi*all-ones). Rules,
applied once when the program is written:

* XOR with a constant, and NOT, flip the flag (no instruction). rho/pi are
  index renaming; iota is flag flips (no instruction).
* XOR of two stored signals: one XOR, flags added mod 2.
* AND: with constant 1 the identity, with 0 constant 0; flags (0,0): one AND;
  (1,1): one OR with flag 1 (De Morgan); mixed: one NOT plus one AND.
* At the end, each digest signal with flag 1 gets one fix-up NOT.

Round 0: column parities need no XOR (each column has at most one variable
lane); D needs 192 XORs; theta needs 256 XORs (lanes 0..3). This is #178's
padding folding. Round 5 computes only digest lanes 0..3, whose chi row reads
only source lanes 0, 6, 12, 18, 24 (#170's projection).

| Round | XOR | AND+OR |
|---|---:|---:|
| 0 | 2048 (0 + 192 + 256 + 1600 chi) | 1600 |
| 1-4, each | 4800 (1280 + 320 + 1600 + 1600 chi) | 1600 |
| 5 | 2176 (1280 + 320 + 320 + 256 chi) | 256 |
| Total | 23424 | 8256 = 6643 AND + 1613 OR |

Applying the rules mechanically also gives 5023 materialised NOTs and 129
fix-up planes (36703 gates in all); every organizer trial reports these
counts as observations of the compiled program.

**Correctness.** Every rule is a Boolean identity on true plane values, and
the constant lanes are exactly the padding of Section 1. By induction over
the six rounds each slot computes f exactly, independently of the inputs
(Appendix A). The experiments of Section 10 are finite checks only.

**Charge per batch of 256 evaluations:**

| Item | Operations |
|---|---:|
| 36703 gates | 36703 |
| one placement per gate result | 36703 |
| 129 fix-up NOTs, op + placement | 258 |
| 256 digest copies into P[0..255] | 256 |
| DP test (OR of 32 planes, NOT, AND with ACTIVE, compare, branch) | 72 |
| batch control (b = b+1, sweep test, jump) | 4 |
| **Total** | **73996** |

That is 289.05 per evaluation. **We charge c = 290 per slot-evaluation**
(74240 per batch), whether or not every slot is active. Without complement
tracking the gate count would be about 39963 per batch, giving 313.5 per
evaluation and 2^125.69 (not supported); the tracking is part of the compiled
program.

## 4. Parameters, distinguished points, trie key

    DP bits   digest bits 224..255 (lane 3 bits 32..63); DP: all 32 are zero
    theta     2^-32
    key       digest bits 0..223 (the non-DP bits)
    Lab       2^40       abandonment threshold (chain length)
    sweep     every 2^38 batches
    L         2^40 + 2^38  hard bound on chain length
    Lrun      2^39       run length in event B3
    K0        68600 * 2^112  evaluation budget for new chains
    B0        K0/256 = 68600 * 2^104 batches (reseeding stops at b = B0)
    Dcap      2^98       record cap

The DP test is w = NOT(P[224] OR ... OR P[255]) AND ACTIVE. The trie key of a
DP in slot j is key = OR_{i<224} (((P[i] >> j) AND 1) << (i + 32)) = z*2^32
mod 2^256. The trie descends 224 levels from key bit 255 (digest bit 223) to
key bit 32 (digest bit 0), consuming exactly the non-DP bits. Two DPs share a
leaf iff their bits 0..223 agree; their bits 224..255 are zero, so iff they are
equal. No two distinct DPs alias.

## 5. Algorithm

State: planes P[0..255]; main-memory arrays START[0..255], SB[0..255] (start
word and start batch per slot); ACTIVE (bit j = slot j active); counters b, r,
free; trie ROOT; index masks HI_0..HI_7 (bit c of HI_k is bit k of c).

SETUP (at most 600 ops): zero planes, ROOT, counters; write HI_k and ACTIVE =
all-ones; then SEED(j) for j = 0..255.

SEED(j) (1800 ops): if b >= B0 goto DEACT(j) (2); s = RAND (1); store START[j]
= s and SB[j] = b (4, with address adds); nm = NOT 2^j (1); for i = 0..255:
t = ((s >> i) AND 1) << j; P[i] = (P[i] AND nm) OR t, with load and store
(7 each, 1792). DEACT(j): ACTIVE = ACTIVE AND NOT 2^j (4); if ACTIVE = 0 halt
with failure (2).

BATCH: b = b+1; run the circuit on P; copy digests to P; DP test gives w; if
w != 0 run DPLOOP; if b is a sweep batch run SWEEP; repeat. A chain seeded in
batch b (SETUP: b = 0) has SB = b and length b' - SB after batch b'.

DPLOOP (set bits of w in **increasing slot order**): m = w AND (0 - w) (2);
j from m by 8 tests against HI_k (41); w = w XOR m (1); key extraction
(1 + 224*5 = 1121); s = load START[j], len = b - load SB[j] (5);
DPFOUND(key, s, len) (at most 3818); SEED(j) (at most 1800); loop (3).

DPFOUND: the depth-224 binary trie of #28, two-word nodes, 0 = empty. Per
level at most 17 ops (b = key >> 255; key <<= 1; p = node + b; c = load [p];
test; allocate c with 2 stores and link, or not; node = c; count down).
Exit: new key, store (s, len) at the leaf, r = r+1, halt with failure at
r = Dcap; else load (s', len') and call RELOCATE((s, len), (s', len')).
Bound: 2 + 224*17 + 2 + 6 = 3818. Two slots reaching one DP in the same
batch are handled in slot order: the lower inserts, the higher relocates.

SWEEP (every 2^38 batches, after DPLOOP; at most 2^12 ops plus SEEDs): an
active slot with b - SB[j] >= Lab is abandoned (no record) and reseeded.
Every chain therefore has length below Lab + 2^38 = L.

RELOCATE((s1, l1), (s2, l2)), l1 >= l2, scalar f: advance s1 by l1 - l2;
then step both while a != b, returning the first pair with f(a) = f(b) and
a != b; halt with failure if a == b. At most 2L evaluations; charged
3L(1 + 192/C). OUTPUT(a, b): recompute f(a), f(b) (2 units), check a != b and
equality, store the messages (at most 200 ops). The run halts at its first
RELOCATE, at Dcap, or when ACTIVE = 0 after reseeding stops. No restart.

**Counts.** Reseeding stops at b = B0; every in-flight chain then ends within
fewer than L batches, so there are at most B0 + L batches and at most
256(B0 + L) = K0 + 256L slot-evaluations. Per chain outside the circuit: one
SEED (1800) plus at most one DPLOOP body (2+41+1+1121+5+3818+3 = 4991) or one
abandonment: at most 6791 < 2^13, **charged 2^13**. Chains: 256 initial plus
one per non-deactivating SEED, which follows a NEWKEY (at most Dcap) or an
abandonment (each uses >= 2^40 of the < 1.0468*2^128 evaluations, so fewer
than 2^89): at most 2^98 + 2^89 + 257.

## 6. Every output is a collision (unconditional)

OUTPUT is reached only with a != b and f(a) = f(b), both recomputed; by
Section 1 msg(a) != msg(b) collide on all 256 digest bits.

## 7. Success probability with 256 concurrent chains

**H-RF.** Whenever the algorithm evaluates f at a point not evaluated before,
f(x) is uniform on {0,1}^256 and independent of the coins and of every value
revealed earlier in the order below. Used only in this section.

**Order.** Evaluations are numbered batch-major, slot-minor: e = 256(b-1)+j+1.
Batch b's inputs are fixed before it is computed, so revealing its outputs in
slot order is a valid sequential order; SEED's starts come after the batch's
outputs. p_e is the input of evaluation e; V_e = {p_1..p_e} with
{f(p_1)..f(p_{e-1})}; e makes **contact** if f(p_e) is in V_e; tau is the
first contact. Contact includes same-batch collisions. A fresh output is the
output at a previously unevaluated point. Before tau all inputs are distinct
(a non-start input of slot j is f(p_e') for its previous evaluation e', not
among p_1..p_e' since e' made no contact, and not a later input, which is a
fresh start or an output f(p_k), k < e', else e' would have made contact).

**Bad events (over the whole run, including the drain).** E_max = K0 + 256L <
1.04676*2^128. Starts S <= 256 + (DPs among fresh outputs) + (abandonments)
+ 1, so E[S] < 1.05457*2^96; every V has size below 2E_max < 2.09351*2^128.

* B1: a start, when drawn, lies in V. Pr <= E[S]*2E_max/N < 5.1403e-10.
* B2: a fresh output equals an earlier start or a point of its own chain.
  Pr <= E_max(E[S] + L)/N < 2.5702e-10.
* B3: some chain makes Lrun = 2^39 consecutive fresh non-DP outputs.
  Pr <= E_max e^-128 < 2^-56.5.
* B4: r reaches Dcap. Records are distinct DPs among fresh outputs,
  dominated by Binomial(E_max, theta) with mean mu < 1.0468*2^96; Chernoff
  with a = 2^98 (e mu/a < 0.712) gives Pr <= 0.712^(2^98).
* B5 (concurrency): within 2^40 batches of tau's batch, some evaluation at an
  unevaluated point other than tau has output in V. Pr <= 2^48 * 2.0935 *
  2^-128 < 2^-78.9.

eps = Pr(B1 or ... or B5) < 7.72e-10.

**Lemma 1 (contact by K0).** Pr(no contact among evaluations 1..K0 and not
B1) <= exp(-K0(K0+1)/(2N)). All slots are active for the first B0 batches,
so evaluations 1..K0 occur unless the run halts; before a contact only B4 can
halt it (a RELOCATE needs a repeated DP, hence a contact). Given no contact
so far and fresh starts, p_e is unevaluated, f(p_e) is uniform, and V_e holds
e distinct inputs, so Pr(no contact at e) <= 1 - e/N; apply 1-u <= e^-u.

**Lemma 2 (RELOCATE).** If chains A = (s1, l1) and B = (s2, l2) end at the
same DP with l1 >= l2 and s2 is not a point of A, RELOCATE outputs a
collision. A chain ending at a DP has distinct points; records are exact;
after alignment both walks are l2 steps from the DP; a == b can only hold at
the first step (excluded), so they first meet at some step with distinct
predecessors. Without B1 and B2 no start ever lies on another chain: a start
is not in V when drawn, and a later output equal to it is a fresh output (B2)
or equals an earlier output produced before it was drawn (B1).

**Lemma 3 (first contact succeeds).** If contact occurs at tau <= K0 and
none of B1-B5 occurs, the run outputs a collision. Let tau be slot j* of batch
b* on chain C, with f(p_tau) = v. By B2, v = f(u) for a point u != p_tau of
another chain C', evaluated at k < tau. Let z' be the first DP on the path
from v. C' evaluates every point of that path first; by B5 none of those
evaluations lands in V, so the path is fresh outputs of C' and, by B3, its
length d <= 2^39; C's length at tau is a <= 2^39. So C reaches z' at length
a + d <= Lab, processed in DPLOOP before that batch's sweep, and C' within
length 2^40: neither is abandoned. Cases: (a) C' completed before tau: its
record exists. (b) C' in flight with k in an earlier batch: it is a batch
ahead and inserts z' first. (c) C' in slot j' < j* with k in batch b*: both
reach z' in the same batch and the lower slot inserts first. The drain does
not stop in-flight chains; B4 excludes the cap. By B5 no other repeated DP
arises in the window, so the first RELOCATE is between C and C', and Lemma 2
applies.

**Result.** Pr(success) >= 1 - exp(-K0(K0+1)/(2N)) - eps. K0^2/(2N) =
68600^2/2^33 = 4705960000/8589934592 = 0.5478458479 (the +1 adds < 2^-128).
1 - exp(-0.5478458479) = 0.4218060124; minus eps < 7.8e-10 gives

    Pr(success) >= 0.4218060116,

claimed as 0.42 (rounded down). This is the algorithm's probability over its
own coins under H-RF, not a confidence in H-RF.

## 8. Total charged time (worst case, every run)

| Phase | Count | Units each | log2 of product |
|---|---|---|---:|
| Batches | <= B0 + L = (K0 + 256L)/256 | 256*290/1626 | 125.578719 |
| Per-chain work | <= 2^98 + 2^89 + 257 | 2^13/1626 | 100.3357 |
| RELOCATE | <= 3L scalar f | 1 + 192/1626 | 42.068 |
| SWEEP scans | <= (B0 + L)/2^38 + 1 | 2^12/1626 | 83.40 |
| OUTPUT, setup | 1 | 3 | 1.585 |

    T <= (K0 + 256L)*290/1626 + (2^98 + 2^89 + 257)*2^13/1626
         + 3L(1 + 192/1626) + ((B0 + L)/2^38 + 1)*2^12/1626 + 3

log2 K0 = 128.0659210, log2(290/1626) = -2.4872025, K0 + 256L < K0(1 +
2^-79.7): term 1 = 2^125.5787185. The other terms add a relative 2^-25.2
(3.6e-8 bits). **log2 T <= 125.5787186 < 125.58.** The slack is 0.0013 bits,
absorbing c <= 290.26 against the 290 charged (289.05 itemised). K0 = 68600 *
2^112 keeps T under 125.58; the largest admissible multiple is 68660 * 2^112.
Every failed and abandoned chain, trie step, bank read and placement, digest
copy, DP test, sweep, RELOCATE and final verification is included. There is
no other precomputation, no stored collision, no parameter search and no
repetition.

Sensitivity (only c varies):

| Convention for the same circuit | c | log2 T |
|---|---:|---:|
| fixed bank, gates only, no placement (not claimed) | 144 | 124.57 |
| **fixed bank, one placement per result (claimed)** | **290** | **125.58** |
| winglock 377eebd published charge, for comparison | 320 | 125.72 |
| narrow 64-register file, Belady schedule, +1 per direct access | 605 | 126.64 |
| memory-to-memory, every operand loaded, every result stored | 518 | 126.42 |

## 9. Memory, preprocessing, advice

Trie: at most Dcap = 2^98 keys, each at most 224 two-word nodes: 2^98 * 448 *
32 bytes = 2^111.8074. Bank (at most 2050 words), START, SB, ACTIVE, masks
(under 2^12 words) and the program text (about 37k straight-line
instructions, under 8 MB): under 2^24 bytes. M <= 2^111.8074 + 2^24 < 2^112:
`memory_log2_bytes: 112`. No messages are retained beyond chain starts.

Preprocessing is SETUP plus the 256 initial SEEDs: at most 600 + 256*1800 =
461400 operations = 283.76 units = 2^8.1485, declared `preprocessing_log2: 9`.
The same work is inside the per-chain time term, so it is charged once in T
and bounded separately here. Advice: zero bytes (reported 0).

## 10. Experiments and H-RF evidence

One standard-library program, `experiments/slot_dp_walk.py`, serves three
declared experiments. To avoid shipping a second file it builds the
circuit's Python source in-process (Appendix A) and runs it with
`exec(compile(...))`; that generated code reads no input and does no I/O.
RELOCATE's scalar f is a separate 25-lane implementation of Section 1. The
organizer recomputes every returned pair; nothing the program prints is
trusted.

* **`bitslice-fullwidth-equivalence`** (12-bit mask): 256 seeded full-width
  inputs, one bit-sliced batch, a pair whose bit-sliced digests agree on
  bits 0-2 of each digest lane. A cheap cross-check, not an equivalence test
  (an XOR mask cannot see an error common to both messages).
* **`slot-dp-walk-n14`** (14-bit mask): the full Section 5 algorithm at n = 14
  (step x <- digest planes 0..13; 256 slots; DP = bit 13 zero, keyed on bits
  0..12; abandonment at 16; reseeding stops after 256 evaluations, then
  drain; same-batch DPs in slot order; halt at first RELOCATE). Returned
  pairs are absolute 14-bit collisions of the real target.
* **`contact-n18-k00`** (18-bit mask): the Lemma 1 contact process at
  reduced width: N = 2^18, exactly K = 512 evaluations, 256 distinct starts,
  256 slots, batch-major slot-minor order; input window message bits
  11i mod 256, output window digest bits 12i (i < 18). A trial returns the
  first-contact collision pair, or null if the first contact lands on a start
  or no contact occurs within K.

**Random-function prediction for the contact harness.** Before the first
contact the known set at evaluation e holds 256 starts and e-1 outputs, so

    P(success) = sum_{e=1..K} [prod_{i<e} (1 - (255+i)/N)] (e-1)/N = 0.28850

(N = 2^18, K = 512), with P(first contact on a start) = 0.34366 and P(none) =
0.36785. A Monte Carlo of the identical loop with a true random function gave
1750/6000 = 0.2917.

**Docker run.** `experiments/runner.py` with its own Docker command (pinned
`python:3.12.12-slim-bookworm`, no network, read-only, 1 CPU, 128 MiB, 20 s),
public seed, 256 trials each, two byte-identical executions of 3.8-4.4 s:
equivalence 256/256; walk 133/256; contact 74/256 (prediction 73.9). No
invalid pair. Seeds derive from the public seed and the target-config
fingerprint; this run used a Windows checkout's fingerprint, and the
organizer's fingerprint or a holdout nonce gives different counts.

**All six-round contact runs we made** (every program version; one earlier
version stopped only at batch boundaries and its prediction uses its real K):

| runs | successes / trials | expected | z |
|---|---:|---:|---:|
| 11 earlier runs, n = 18 to 24 (6-12 windows each) | 8654/25856 | 8840 | -2.45 |
| fresh seeds, 12 windows, n = 18 (seed not recorded) | 14169/49152 | 14180 | -0.1 |
| fresh seeds, 12 windows, n = 18, base seed 20261005 | 14189/49152 | 14180 | +0.1 |
| **all** | **37012/124160** | **37201** | **-1.17** |

The two fresh-seed runs were made after the earlier subtotal came out low,
as a confirmatory check, on the six windows k = 0, 2, .., 10 and six further
windows (odd k; window k uses input bits (7k + 11i) mod 256 and output bits
k + 12i). On the identical harness, full 24-round SHA3-256 gave 0.2952 and a
true random function 0.2917, both matching 0.28850.

**Reading.** The six-round frequencies are consistent with the
random-function prediction: all 124,160 trials are 0.51% below expectation
(-1.17 sd). These are descriptive comparisons; the runner records
`probability_inference: none`, and no bound is derived from them.

**Carry-over to full width.** The harness success frequency is not the
contact probability: success needs the first contact to land on an earlier
output, against starts (34%) and no contact (37%). We model a deviation as a
contact-rate multiplier lambda on the per-evaluation contact probability (to
outputs and starts in the formula above; at full width the contact bound
becomes 1 - exp(-lambda K0^2/2N)). At K0 = 68600 * 2^112:

| harness success shortfall | lambda | full-width success bound |
|---|---:|---:|
| 0.51% (all runs) | 0.990 | 0.4185 |
| 1.22% (all runs, one-sided 95% upper end) | 0.975 | 0.4139 |
| 3.52% (earlier subtotal, one-sided 95% upper end) | 0.931 | 0.3996 |
| 5.10% | 0.902 | 0.3900 (gate used up) |

## 11. Heuristics (complete list)

**H-RF** (score-critical; success probability only). Statement: Section 7.
Scope: six-round prefix SHA3-256 on 32-byte messages (4 variable, 21 constant
lanes), iterated from uniform 256-bit starts in 256 concurrent slots, over at
most E_max < 1.0468*2^128 evaluations. Role: Lemma 1 and the bad events; not
used for correctness, time, memory or preprocessing. Evidence: the standard
van Oorschot-Wiener premise, judged plausible for this map in #28, which
supported it with its own reduced-n contact runs and a 24-round control; ours
adds an organizer-executed contact experiment and the 124,160-trial
comparison of Section 10, consistent with the prediction. Extrapolation: from
n = 18 (and n = 19-24) contact runs and the n = 14 walk to the full map.
Sensitivity: success stays at least 0.39 for lambda >= 0.902 (a harness
shortfall up to 5.10%); dPr/dlog2 K0 is about 0.439. Limitations: H-RF is
false as a literal statement about a fixed function; six-round SHA3-256 has
differential structure (real 5-round collisions, Guo-Liao-Liu-Liu-Qiao-Song,
J. Cryptology 2020; a 6-bit 6-round near-collision, ePrint 2026/2107, abstract
only; Guo-Liu-Song-Tu, ASIACRYPT 2022, find no classical 6-round SHA3-256
collision below the birthday bound). Those use chosen differences, which a
random walk does not produce. No result showing that this iterated map
departs measurably from a random mapping was found in this survey.

**Not assumed.** No heuristic about cost, memory or circuit correctness (all
exact and worst-case); no differential trail; no PRNG premise for the attack
(RAND is a primitive); no inference from experiment statistics.

## 12. Prior work and credit

* van Oorschot and Wiener, "Parallel Collision Search with Cryptanalytic
  Applications", J. Cryptology 12(1):1-28, 1999.
* #28 (winglock, 128.014): the DP walk on this step map, its trie, record cap,
  chain bound and sequential lemmas, rewritten here for 256 chains.
* #148 (may93182, 126.995): 256-message bit slicing in the 256-bit RAM.
* #170 (ercumentyildirim, 126.92): the four-lane last-round projection.
* #178 (zeeshan8281, 126.902): first-round padding folding, the bank
  convention wording, and the equivalence-experiment format.

These are unpromoted in-review packages; their authors are credited as
coauthors of the reused ideas. Ours is the combination: the bit-sliced core
inside a DP walk with slots as chains, the slot-DP machinery and its
concurrency proof. No earlier r6 package combining bit slicing with DPs was
found in our survey (open r6 PRs through #180).

## 13. Limitations

* Generic, far from practical; a constant-factor gain over bit-sliced
  birthday-and-sort packages from removing transposes and sorting, at the
  cost of one random-function heuristic.
* The claim rests on the fixed register-bank convention of #148/#170/#178
  (here at most 2050 words), whose acceptance is reported, not verifiable
  here; under a narrow 64-register file it is 2^126.64. A companion package
  charges every core load and store (126.4).
* The success margin above 0.39 is 0.0318 under H-RF; the reduced-width
  evidence is consistent with H-RF but is not a full-width proof.
* The experiments are finite and reduced-width; full-width circuit
  correctness rests on Section 3 and Appendix A.

## Appendix A. The circuit generator

`compile_circuit` in `experiments/slot_dp_walk.py` (shipped, and shown in full
in the organizer report) emits the Section 3 circuit as one straight-line
Python function F(P) -> 256 digest planes. Its logic, exactly:

    signal := ("c", bit) | ("v", name, flag)
    xor(a,b):  both const -> const; one const -> flip flag of the other;
               else emit t = a ^ b, flag = fa ^ fb
    neg(a):    flip const bit or flag
    band(a,b): both const -> const; one const -> other if 1 else const 0;
               flags (0,0) emit t = a & b, flag 0
               flags (1,1) emit t = a | b, flag 1
               mixed      emit t = a & (b ^ M)  [b the flagged one], flag 0
    state: lanes 0..3 = input planes P[64*lane + z]; lane 4 = const 0x06 bits;
           lane 16 = const bit 63; all other lanes const 0
    per round r = 0..5 (last = r == 5):
      C[x][z] = xor over y of st[x+5y][z]
      D[x][z] = xor(C[x-1][z], C[x+1][z-1])
      for idx in (all 25, or 0,6,12,18,24 if last):
        th[z] = xor(st[idx][z], D[idx%5][z])
        B[y + 5((2x+3y)%5)][z] = th[(z - rho[idx]) % 64]
      for idx in (all 25, or 0..3 if last):
        out[idx][z] = xor(B[idx][z], band(neg(B[x+1,y][z]), B[x+2,y][z]))
      out[0][z] = xor(out[0][z], const(RC[r] bit z))
    digest plane 64*lane + z: stored word, XOR M if its flag is 1

Each emitted line is one gate; the emitted counts are those of Section 3.
Because every branch is a Boolean identity on true values, the emitted
program computes f for every slot.
