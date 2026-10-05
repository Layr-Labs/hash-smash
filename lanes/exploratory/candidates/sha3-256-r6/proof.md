# SHA3-256 prefix rounds 0-5: bit-sliced distinguished-point collision walk (register-bank accounting)

Selected lane: exploratory. Target: `sha3-256-r6-prefix-v1`. Attack class:
ordinary collision. Cost model: `collision-frontier-v5`, with reference
operation cost C = 1626 for `sha3-256-r6`. One six-round sponge permutation
costs 1 unit; every other primitive 256-bit RAM word operation costs 1/1626.

## 0. Claim

A classical randomized algorithm with these properties:

* It outputs two distinct 32-byte messages whose complete six-round
  SHA3-256 digests agree on all 256 bits (Section 6, unconditional).
* Total charged time is at most 2^125.5788 units in every run (Section 8),
  under the fixed register-bank convention of the accepted bit-sliced r6
  packages (#148, #170, #178), with one placement charged per gate result.
  The JSON reports `time_log2: 125.58`, which leaves 0.0013 bits of slack.
  This improves on the pending leader (winglock 377eebd, 125.655).
* Success probability is at least 0.4218060 under one declared heuristic,
  H-RF (Sections 7 and 11). The JSON reports 0.42, rounded down; the
  bound clears the 0.39 gate by 0.0318.
* Memory is below 2^111.81 + 2^24 bytes < 2^112 bytes. Preprocessing
  (SETUP + 256 initial SEEDs) is at most 2^8.15 units, declared as 2^9.
  Nonuniform advice is zero.

This is a generic birthday attack: van Oorschot-Wiener parallel collision
search with distinguished points, with 256 chains carried in the 256 bit
positions of each RAM word (bit slicing). The step map is evaluated by a
straight-line Boolean circuit on bit planes, so a chain's digest planes are
the next input planes in place. No transpose, sort or format conversion is
on the per-evaluation path. No cryptanalytic advance on SHA3 is claimed.
The required `baseline_improved` identifier `sha3-256-r6-nominal-v2` names
the organizer's nominal reference only.

Every argument the review needs is in this file. All eight declared
experiments run one program, `experiments/slot_dp_walk.py`, included in the
package (Section 10); its circuit generator is reproduced in Appendix A.

## 1. Exact target, message map and step function

Let N = 2^256. For a 256-bit word x, msg(x) = LE32(x): x written as exactly
32 little-endian bytes, leading zero bytes included. msg is injective, and
every msg(x) is a legal message of bit length 256 < 2^64.

The sponge has a 1600-bit state, rate 1088 bits (136 bytes), capacity 512,
the all-zero initial state and a 256-bit output. Padding is the SHA3
domain suffix 01 followed by pad10*1 (delimited suffix byte 0x06). A
32-byte message m pads to exactly one 136-byte block

    m || 06 || (00 repeated 102 times) || 80

There is one absorption and one permutation. No squeeze permutation
follows, because 32 output bytes are fewer than the rate. No feed-forward.

State lanes A[0..24], index x+5y, 64 bits each, little-endian. XORing the
padded block into the zero state gives:

    A[0..3] = the four 64-bit lanes of x  (A[j] = bits 64j..64j+63 of x)
    A[4]    = 0x0000000000000006           (byte 32 of the block)
    A[16]   = 0x8000000000000000           (byte 135 of the block)
    every other lane = 0

PERM6 applies Keccak-f[1600] rounds 0 through 5 (the prefix convention, not
Keccak-p's last-round convention). In each round, subscripts mod 5, lane
arithmetic on 64 bits, each stage reading the previous stage:

    C[x] = A[x,0] ^ A[x,1] ^ A[x,2] ^ A[x,3] ^ A[x,4]
    D[x] = C[x-1] ^ rot64(C[x+1], 1)
    B[y, 2x+3y] = rot64(A[x,y] ^ D[x], rho[x+5y])
    A[x,y] = B[x,y] ^ ((NOT B[x+1,y]) AND B[x+2,y])
    A[0,0] = A[0,0] ^ RC[round]

rot64(v,k) rotates left by k (bit i to bit i+k mod 64). The rho offsets in
x+5y order are 0,1,62,28,27, 36,44,6,55,20, 3,10,43,25,39, 41,45,15,21,8,
18,2,61,56,14. The round constants, in order, are 0x0000000000000001,
0x0000000000008082, 0x800000000000808A, 0x8000000080008000,
0x000000000000808B, 0x0000000080000001.

The digest is the first 32 squeeze bytes, lanes A[0..3] in little-endian
order. Define

    f(x) = A[0] + 2^64 A[1] + 2^128 A[2] + 2^192 A[3]   (after PERM6)

so LE32(f(x)) is exactly the target digest of msg(x). "Digest bit i" means
bit i of the integer f(x), 0 <= i <= 255; it is bit (i mod 64) of lane
floor(i/64), and lies in digest byte floor(i/8). If x != x' and
f(x) = f(x'), then msg(x) != msg(x') have equal full 256-bit digests: an
ordinary collision of the selected target. This is the same step map as the
earlier r6 distinguished-point package (#28, Section 12).

## 2. Machine model and charging convention

Classical probabilistic 256-bit word RAM with the `collision-frontier-v5`
primitives, each costing 1/1626: 256-bit load and store; addition and
subtraction mod 2^256; AND, OR, XOR, NOT; shift or rotation; comparison;
conditional branch; RAND (one fresh independent uniform 256-bit word).

**Convention used for the claim: the fixed register-bank convention of the
bit-sliced r6 packages #148 (126.995), #170 (126.92) and #178 (126.902).**
#178's proof states it as follows (quoted verbatim): "The program has a
fixed finite register bank of fewer than 2^14 words, independent of n. ...
Registers and their stored values count toward memory. Primitive
instructions read their named register operands as part of the operation;
indirect main-memory loads and stores are charged below." Its round table
"additionally charges a placement for every logical result, beyond its
primitive's normal result write." winglock 377eebd restates the same base
rule. Prior acceptance is reported, not verifiable from this package: in
the review dossiers we downloaded for #148, #170 and #178, each was scored
`plausible_not_refuted` and the cost lane raised no finding against this
convention. A reviewer cannot check that from here, so we also give the
fully memory-charged bound (companion `package_r6`, 126.4) and the Section 8
sensitivity table. We adopt the convention as follows:

* The program holds the circuit's working values in a fixed register bank
  of at most 2050 words (Section 2.1), independent of the message and chain
  counts and below the 2^14 ceiling. The bank allocation is static: it is
  fixed when the program is written, and costs nothing at run time. The
  START and SB slot arrays and the trie are main memory, not bank.
* Each primitive costs one unit and reads its named bank operands as part of
  the operation. A binary gate is one operation.
* We additionally charge **one placement (a bank store) per gate result**,
  as #178's table does, so no result write is free.
* A comparison and the branch that uses it are 2 operations. An
  unconditional jump is one branch. Writing a constant is one operation.
* Only genuinely indirect, data-dependent main memory is charged as a
  separate load or store: the depth-224 trie, the START and SB slot arrays,
  and the per-DP slot extraction. These are per-chain, charged in Section 5.
* A scalar permutation call (RELOCATE and OUTPUT only) costs 1 unit plus 128
  operations for writing its 25 lanes and reading 4 lanes back.
* Instruction fetch is not a primitive and is not charged; the program text
  is counted in memory (Section 9). The algorithm never reads memory it has
  not written.

Scope and honesty of this convention. This is the broad fixed-bank
convention (bank under 2^14 words) that three r6 packages passed, not a
narrow 64-register file. winglock 377eebd additionally narrows to a stated
64-register machine and charges one address-add for every direct load and
store, reaching 320 operations per message. Our six-round step map keeps
all 1600 state planes live across each round, so a genuine 64-register file
would spill the state and reload it: an optimal (Belady) schedule of our
straight-line program needs about 59,000 direct accesses per 256-message
batch, i.e. about 605 charged operations per evaluation under winglock's
per-access rule, which would be about 2^126.64 and would **not** improve on
125.655. We therefore do not claim the narrow 64-register number. The claim
rests on the broad fixed-bank convention, made conservative by charging a
placement per result (Section 8 sensitivity). The reference cost C excludes
memory traffic (`docs/RESCORING.md`), so the bank's internal traffic is not
double-charged against the permutation unit.

A companion package (`package_r6`, time_log2 126.4) states the same
algorithm with every load and store of the core charged memory-to-memory,
for a reviewer who rejects any register-bank convention.

### 2.1 Register-bank allocation and the maximum live word count

The unrolled circuit names 36703 gate results, but these are not 36703
simultaneous words. Each result occupies a bank word only from the gate
that defines it to its last use; the bank word is then free. The 256 digest
results stay live to the end of the batch (they are the next input planes);
the 256 input planes are live from the start of the batch to their last use
in round 0. For a straight-line program, linear-scan (interval) allocation
assigns each result the lowest free bank word at its definition and frees it
after its last use. The bank size it needs is exactly the maximum number of
values simultaneously live.

We computed that maximum from the generator (Appendix A) by an exact
liveness scan over the generation order: a value is live on [define, last
use], digest results to the batch end, input planes from the start. The
maximum live count is 2048 words if a result may take the word of an operand
that dies at the same gate, and 2049 under strict intervals; one more word
holds the materialised-NOT temporary. **The bank therefore needs at most
2050 words.** Measured per-round maxima under strict intervals: round 0
1730, rounds 1-4 2049 each, round 5 1601. Roughly, a round holds one full
1600-plane state plus the parity, theta-D and chi working values it still
needs; the measured figures, not that sketch, are the bound. So the bank is
at most 2050 < 2^14 words, independent of the message and chain counts.
This reconciles the fixed bank with the circuit's 36703 result names: the
names are reused, and at most 2050 words are resident at once.

The 256 digest results are copied into the input-plane words P[0..255] at
the end of each batch, so the next batch reads its inputs from fixed words.
We charge those 256 copies (one operation each) in Section 3.6.

The placement charge of Section 2 is one bank store per gate result. Under
the allocation above, that store writes the result into its assigned
(reused) bank word, and every operand read is a named bank read within the
2050-word bank, charged as part of its gate. The per-evaluation charge of
Section 3.6 is therefore one operation plus one store per result, plus the
256 digest copies, which the allocation realises; no reload is needed,
because a straight-line schedule in generation order reads each value from
its still-live bank word. The 2050-word maximum is the only fact Section 8
needs from this section.

## 3. The bit-sliced step circuit

### 3.1 Planes

A batch evaluates f on 256 inputs x_0..x_255 at once. For each input bit
i (0..255) one RAM word P[i] holds bit i of x_j at bit position j. P[i] is
bit (i mod 64) of lane floor(i/64) for all 256 slots: the "plane" of that
state bit. A Boolean gate on planes applies that gate to all 256 slots
independently. Every other input lane bit is a public constant (0, except
lane 4 bits 1 and 2 and lane 16 bit 63, which are 1). No plane exists for
constants.

### 3.2 Compile rules (applied once, when the program is written)

A circuit signal is either a public constant bit, or a stored plane word s
together with a public flag phi in {0,1}; its true value is s XOR
(phi ? all-ones : 0).

* XOR of a signal with a constant flips the flag. No instruction.
* NOT flips the flag. No instruction.
* XOR of two stored signals: one XOR instruction; flags add mod 2.
* AND with constant 1 is the identity, AND with constant 0 is constant 0.
* AND of two stored signals with flags (0,0): one AND, flag 0.
  Flags (1,1): one OR, flag 1, since (NOT a) AND (NOT b) = NOT (a OR b).
  Mixed flags: materialise one NOT and one AND, flag 0.
* rho and pi only rename which plane is referenced; z-rotation of a lane
  becomes a fixed index permutation of its 64 planes. No instruction.
* iota XORs public constants into lane 0: flag flips only.

These rules are exact Boolean identities, applied identically to every slot
and every input, so the instruction sequence is data-independent. At the
end, each of the 256 digest signals with flag 1 is fixed by one NOT.

### 3.3 First-round folding and last-round projection

Round 0 starts with lanes 0..3 variable and lanes 4 and 16 constant, so:
column parities need no XOR instruction (each column has at most one
variable lane); D needs 192 XORs (D1 = C0^C2, D2 = C1^C3, D4 = C3^C0 are
variable-variable; D0 and D3 involve a constant column); theta application
needs 256 XORs (lanes 0..3), all other lanes only take a flag from D. The
round-0 folding is the same lever as #178's padding-specialised first round.

Round 5 only needs digest lanes 0..3. Chi for row y = 0 reads B[x,0] for
x = 0..4, and rho/pi maps source lane (x,y) to row 0 exactly when x = y, so
only source lanes 0, 6, 12, 18, 24 are theta-applied and only 4 chi lanes
are computed (the last-round projection of #170). Every omitted value has no
path to a digest bit.

### 3.4 Exact instruction counts per batch of 256 evaluations

| Round | XOR | AND+OR | of which AND-with-NOT |
|---|---:|---:|---|
| 0 | 2048 (0 + 192 + 256 + 1600 chi) | 1600 | |
| 1-4, each | 4800 (1280 + 320 + 1600 + 1600 chi) | 1600 | |
| 5 | 2176 (1280 + 320 + 320 + 256 chi) | 256 | |
| Total | 23424 | 8256 (6643 AND, 1613 OR) | 5023 |

The XOR and AND+OR totals follow from the table by hand. The split into
6643 AND, 1613 OR and 5023 materialised NOTs comes from applying the
Section 3.2 rules mechanically. That compile is the function
`compile_circuit` in `experiments/slot_dp_walk.py`, and every organizer
trial reports these four numbers as observations. It also gives 129 digest
planes with flag 1, which need a fix-up NOT each.

The claimed bound uses this exact compiled count. That count is
data-independent and is reproduced by every organizer trial. Under the
register-bank convention (Section 2), the per-evaluation charge is one
operation plus one placement per gate result, i.e. 2*36703 plus fix-ups,
digest copies and control, which is 289.05 (Section 3.6). The claimed 125.58
absorbs up to 290.26 operations per evaluation (Section 8), so the charged
290 fits. The sensitivity table in
Section 8 shows how the charge moves under gates-only accounting and under
winglock's stricter narrow 64-register per-access rule.

### 3.5 Memory layout, in-place feedback and correctness

Circuit results live in bank words assigned by the static linear-scan
allocation of Section 2.1 (at most 2050 words). At the end of each batch the
256 digest values are copied into the fixed input-plane words P[0..255]
(256 charged copies, Section 3.6). So after a batch, P[i] holds digest bit i
of f(x_j) in slot j. These planes are exactly the input planes of the next
evaluation x_j <- f(x_j), with no transpose.

Correctness: by induction over the six rounds, each slot's bits follow the
scalar round equations of Section 1 exactly. This holds because every
compile rule is a Boolean identity and the constant lanes are the padding
of Section 1. Appendix A gives the generator source and this argument in
full. The organizer-executed experiments of Section 10 give finite checks
on the real target: absolute 14-bit and 18-bit collisions returned by the
walk and contact runs, and a 12-bit cross-check; none of them is a full
256-bit equivalence test.

### 3.6 Charged cost of one batch (register-bank convention)

Each of the 36703 gates costs one operation and, by the Section 2
convention, one placement for its result: 2 each. The 129 final fix-up NOTs
cost 2 each. The DP test and batch control are charged as named-bank
operations. Indirect memory (the trie and slot arrays) is per-chain and
appears in Section 5, not here.

| Item | Operations per batch |
|---|---:|
| 36703 gates (23424 XOR, 6643 AND, 1613 OR, 5023 NOT) at 1 each | 36703 |
| one placement per gate result, at 1 each | 36703 |
| 129 digest fix-up NOTs at 2 each (op + placement) | 258 |
| DP test: OR of 32 planes, NOT, AND with ACTIVE, compare, branch | 72 |
| Batch control: b = b+1, sweep test (compare, branch), jump back | 4 |
| Copy of the 256 digest values into P[0..255] | 256 |
| **Total** | **73996** |

That is 289.05 operations per evaluation. **We charge c = 290 operations
per slot-evaluation, i.e. 74240 per batch**, whether or not every slot is
active. The memory-to-memory variant of this table (every operand a load,
every result a store) is 516.43 per evaluation; it is the basis of the
companion `package_r6` claim at 126.4 and the last row of the Section 8
sensitivity table.

## 4. Parameters, distinguished points and the trie key

    DP bits         digest bits 224..255 (lane 3 bits 32..63; digest bytes 28..31)
    DP              an output z with all 32 DP bits equal to 0
    theta           2^-32 for a uniform output
    key bits        digest bits 0..223, exactly the 224 non-DP bits
    Lab             2^40      abandonment threshold (chain length)
    sweep period    2^38      batches between abandonment sweeps
    L               2^40 + 2^38   hard bound on any chain's length
    Lrun            2^39      run length used in the bad event B3
    K0              68600 * 2^112   (evaluation budget for new chains)
    B0              K0/256 = 68600 * 2^104 batches (reseeding stops at b = B0)
    Dcap            2^98      record cap

The DP test of one batch is w = NOT(P[224] OR ... OR P[255]) AND ACTIVE:
bit j of w is 1 exactly when slot j is active and its output has all 32 DP
bits zero.

The trie key of a DP in slot j is

    key = OR over i = 0..223 of ( ((P[i] >> j) AND 1) << (i + 32) )

so key = z * 2^32 mod 2^256. Key bits 32..255 are exactly digest bits
0..223 of z, and key bits 0..31 are zero. The trie descends from key bit 255
(digest bit 223) down to key bit 32 (digest bit 0): 224 levels, consuming
exactly the 224 non-DP bits and no DP bit. Two DPs reach the same leaf iff
their bits 0..223 agree. Their bits 224..255 are all zero, so this happens
iff the DPs are equal. No two distinct DPs alias.

## 5. Algorithm

State in RAM: planes P[0..255]; arrays START[0..255] and SB[0..255] (start
word and start batch index of the chain in each slot); ACTIVE (a 256-bit
word, bit j = slot j active); counters b (batches done), r (records), free
(next trie address); ROOT (two-word trie root); eight 256-bit index masks
HI_0..HI_7 (HI_k has bit c set iff bit k of c is 1). The fixed area starts
at a nonzero address, so no node address is 0.

SETUP (at most 600 operations): store 0 to the 256 planes, ROOT and
counters; store HI_0..HI_7 and ACTIVE = all-ones; then SEED(j) for
j = 0..255.

SEED(j) (start a new chain in slot j; m = 2^j is in a register; 1800
operations including the B0 test):

    if b >= B0: goto DEACT(j)                      (2)
    s = RAND                                       (1)
    store START[j] = s; store SB[j] = b            (2 address adds + 2 stores = 4)
    nm = NOT m                                     (1)
    for i = 0..255 (unrolled):                     (7 each, 1792)
        t = s >> i; t = t AND 1; t = t << j
        p = load P[i]; p = p AND nm; p = p OR t; store P[i] = p

DEACT(j): ACTIVE = ACTIVE AND NOT m (load, NOT, AND, store: 4);
if ACTIVE == 0: halt with failure (2).

BATCH: b = b + 1 (b is now the index of this batch). Run the
straight-line circuit of Section 3 on P, in place. Then run the DP test,
giving w (Section 3.6). If w != 0, run DPLOOP. Then batch control: if b
equals the next sweep batch, run SWEEP; jump to BATCH. A chain seeded in
batch b (or in SETUP, with b = 0) has SB = b and makes its first evaluation
in batch b + 1. So after batch b' its length is exactly b' - SB.

DPLOOP processes the set bits of w **in increasing slot order**, one at a
time:

    m = w AND (0 - w)                     lowest set bit            (2)
    j = 0; for k = 7..0: t = load HI_k; t = m AND t;
           if t != 0: j = j + 2^k         index of that bit         (1 + 8*5 = 41)
    w = w XOR m                                                     (1)
    key = 0; for i = 0..223: t = load P[i]; t = t >> j;
           t = t AND 1; t = t << (i+32); key = key OR t             (1 + 224*5 = 1121)
    s = load START[j]; sb = load SB[j]; len = b - sb                (2 adds + 2 loads + 1 = 5)
    DPFOUND(key, s, len)                                            (<= 3818)
    SEED(j)                                                         (<= 1800)
    if w != 0: goto DPLOOP; else goto batch control                 (3)

DPFOUND is the depth-224 binary trie of #28, with two-word nodes and 0 as
the empty pointer. node = ROOT and i = 224 cost 2. Each level costs at most
17 operations:
* b = key >> 255; key = key << 1; p = node + b; c = load [p];
  if c == 0 goto ALLOC (6);
* else path: created = 0, jump (2); or the allocation path: c = free;
  store [c] = 0; t = c+1; store [t] = 0; free = free+2; store [p] = c;
  created = 1 (7);
* JOIN: node = c; i = i-1; if i != 0 goto LEVEL (4).

Exit: if created == 1 (2) then NEWKEY: store [node] = s; t = node+1;
store [t] = len; r = r+1; if r == Dcap halt with failure (6). Otherwise
s' = load [node]; t = node+1; len' = load [t] (3), then RELOCATE((s, len),
(s', len')). Bound: 2 + 224*17 + 2 + 6 = 3818.

Same-batch DPs are therefore handled sequentially: if two slots reach the
same DP in one batch, the lower slot inserts the record and the higher slot
finds it and goes to RELOCATE.

SWEEP (every 2^38 batches, after that batch's DPLOOP): for each active slot
j, load SB[j]; if b - SB[j] >= Lab, the chain is abandoned (no record) and SEED(j) runs.
The sweep costs at most 2^12 operations plus the SEEDs, and each SEED is
charged to its chain. A chain is checked at least once every 2^38 batches,
so every chain has length below Lab + 2^38 = L.

RELOCATE((s1, l1), (s2, l2)), with l1 >= l2 after renaming. Each f here is
one scalar permutation (1 unit) plus at most 192 operations: 128 for lane
writes and reads, plus loop control and compares.

    a = s1; repeat (l1 - l2) times: a = f(a)
    b = s2
    repeat at most l2 times:
        if a == b: halt with failure
        fa = f(a); fb = f(b)
        if fa == fb: goto OUTPUT(a, b)
        a = fa; b = fb
    halt with failure

It makes at most (l1 - l2) + 2 l2 <= 2L evaluations. We charge
3L(1 + 192/C) units, which is below 2^42.07.

OUTPUT(a, b): recompute f(a) and f(b) with the scalar permutation (2
units), check a != b and equality of all 256 output bits, then store the two
32-byte messages. If the check fails, halt with failure. This costs 2 units
plus at most 200 operations.

**Halting.** The run halts at its first RELOCATE, successful or not, at
Dcap records, or when ACTIVE becomes 0 after reseeding has stopped (the
drain). There is one run, with no restart and no amplification.

**Drain.** Once b >= B0, SEED deactivates slots instead of reseeding. Every
chain still in flight ends within fewer than L more batches: at a DP, at an
abandonment sweep, or at the halt. So the number of batches is at most
B0 + L, and the number of slot-evaluations is at most
256(B0 + L) = K0 + 256L.

Per-chain work outside the circuit: one SEED (1800), plus at most one
DPLOOP body excluding SEED (2 + 41 + 1 + 1121 + 5 + 3818 + 3 = 4991), or one
abandonment (at most 16 in the sweep). That is at most 6791 < 2^13 = 8192
operations. **We charge 2^13 per chain.**

Number of chains: 256 initial chains plus one per SEED that does not
deactivate. Such a SEED happens only after a NEWKEY (at most Dcap, because
the run halts at r = Dcap) or an abandonment. Each abandoned chain used at
least Lab = 2^40 slot-evaluations of the at most K0 + 256L < 1.0468 * 2^128,
so there are fewer than 2^89 abandonments. Hence there are at most
2^98 + 2^89 + 257
chains in any run.

## 6. Every output is a valid collision (unconditional)

OUTPUT is reached only with a != b and f(a) = f(b) verified by
recomputation with the scalar permutation. By Section 1, msg(a) != msg(b)
are then legal 32-byte messages with equal complete 256-bit six-round
SHA3-256 digests. No heuristic is used here.

## 7. Success probability with 256 concurrent chains

### 7.1 The heuristic

H-RF: whenever the algorithm evaluates f at a point x it has not evaluated
before, f(x) is uniform on {0,1}^256 and independent of the algorithm's
coins and of every value revealed earlier in the evaluation order below.
H-RF is used only in this section. All resource bounds are worst case for
every run and do not use it.

### 7.2 Evaluation order and definitions

Number the slot-evaluations of the main loop e = 1, 2, ... **batch-major,
slot-minor**: evaluation e = 256(b-1) + j + 1 is slot j in batch b (active
slots only, keeping this order). The inputs of batch b are fixed before
batch b is computed. Revealing its 256 outputs one by one in slot order is
therefore a valid sequential order for H-RF; the simultaneity of the
hardware evaluation is irrelevant to the distribution. Starts drawn by SEED
after batch b come after all of batch b's outputs in this order.

p_e is the input of evaluation e. V_e = {p_1..p_e} together with
{f(p_1)..f(p_{e-1})}. Evaluation e makes contact if f(p_e) is in V_e;
tau is the first contact. This definition includes **same-batch
collisions**: if slot j' < j in the same batch already produced
f(p_e), it is in V_e. A start is fresh if it is not in the current V when
drawn. A fresh output is the output of an evaluation at a point not
evaluated before.

Before tau, every input is unevaluated. A start is fresh unless B1 below
occurs. A non-start input p_e of slot j is f(p_{e'}) for slot j's previous
evaluation e'. It is not among p_1..p_{e'}, because e' made no contact. It
is not among p_{e'+1}..p_{e-1} either. Each of those is a fresh start, or
an output f(p_k) with k < e'; if f(p_k) = f(p_{e'}), evaluation e' would
have made contact.

### 7.3 Bad events (taken over the whole run, including the drain)

Let E_max = K0 + 256L < 1.04676 * 2^128 bound all evaluations. Let S be
the number of starts: 256 + (DPs among fresh outputs) + (abandonments) + 1,
so E[S] < 256 + E_max*theta + 2^89 + 1 < 1.05457 * 2^96. Every V has size at
most 2 E_max < 2.09351 * 2^128.

* B1: some start, when drawn, lies in the current V (this includes two
  equal starts). Pr(B1) <= E[S] * 2E_max / N < 5.1403e-10.
* B2: some fresh output equals a start drawn earlier (any slot, in flight
  or completed), or a point of its own chain (a cycle).
  Pr(B2) <= E_max (E[S] + L) / N < 2.5702e-10.
* B3: some chain makes Lrun = 2^39 consecutive evaluations whose outputs
  are all fresh and none is a DP. There are at most E_max possible first
  evaluations of such a run, and each run has probability at most
  (1 - theta)^(2^39) <= e^-128, so Pr(B3) <= E_max e^-128 < 2^-56.5
  (log2 E_max < 128.066, and e^-128 = 2^-184.66).
* B4: r reaches Dcap = 2^98. Before the first RELOCATE every stored record
  is a distinct DP among fresh outputs (a repeated DP goes to RELOCATE and
  halts). The count is dominated by Binomial(E_max, theta), whose mean mu
  is below 1.0468 * 2^96. The Chernoff bound
  Pr(X >= a) <= e^-mu (e mu / a)^a with a = 2^98 has e mu / a < 0.712, so
  Pr(B4) <= 0.712^(2^98).
* B5 (concurrency): within the 2^40 batches starting at the batch of tau,
  some evaluation at a previously unevaluated point, other than tau itself,
  has its output in V (a second contact). There are at most 256 * 2^40
  such evaluations, each with probability at most 2E_max/N, so
  Pr(B5) <= 2^48 * 2.0935 * 2^-128 < 2^-78.9.

eps = Pr(B1 or B2 or B3 or B4 or B5) < 7.72e-10.

B1 and B2 are stated over the whole run, not only up to tau, and B5 is new.
These are the changes needed for concurrency. After the first contact the
other 255 chains keep running until the halting RELOCATE: their starts must
stay off every other chain, and no second merge may lengthen the path to
the shared DP.

### 7.4 Lemma 1 (contact by K0)

Pr(no contact among evaluations 1..K0, and not B1) <= exp(-K0(K0+1)/(2N)).

Proof. Reseeding continues while b < B0, so all 256 slots are active in the
first B0 batches, and evaluations 1..K0 all occur unless the run halts.
Before a contact, a halt can only come from B4. A RELOCATE needs two equal
DP outputs at distinct evaluations, and the later of the two is a contact.
Condition on any history in which evaluations 1..e-1 made no contact and
the starts so far are fresh. Then p_e is unevaluated, f(p_e) is uniform by
H-RF, and V_e contains the e distinct inputs p_1..p_e. So
Pr(f(p_e) not in V_e | history) <= 1 - e/N. The chain rule and
1 - u <= e^-u give the bound.

### 7.5 Lemma 2 (RELOCATE succeeds unless B1 or B2)

Let chains A = (s1, l1) and B = (s2, l2) end at the same DP z, with
l1 >= l2. Assume s2 is not a point of A. Then RELOCATE(A, B) outputs a
collision.

Proof. A chain that stops at a DP has pairwise distinct points: a repeated
point before the first DP would put the chain on a cycle with no DP, and it
would never stop. Records are exact: s is the stored start and len counts
the evaluations from s to z. After alignment, a and b are both l2 steps
from z. While a != b, step together. The test a == b can first hold only at
the first iteration, which would mean s2 is a point of A. That is excluded.
They reach z together after l2 steps, so there is a first step where
f(a) = f(b) with a != b. RELOCATE outputs that pair, and OUTPUT verifies
it.

If neither B1 nor B2 occurs, no start ever lies on another chain. When a
start is drawn, it is not in V, so it is not a point of any earlier chain.
After it is drawn, a later chain can reach it only through an output equal
to it. A fresh output equal to it is B2. A non-fresh output equals an
earlier output, which is either a fresh output (B2 again) or was itself
produced before the start was drawn (then the start was in V: B1). So the
hypothesis of Lemma 2 holds for every RELOCATE.

### 7.6 Lemma 3 (first contact leads to a successful RELOCATE)

Suppose contact happens at tau <= K0 and none of B1-B5 occurs. Then the
run reaches a RELOCATE, and by Lemma 2 that RELOCATE outputs a collision.

Proof. Let tau be slot j* in batch b*, on chain C, with f(p_tau) = v.
By B2, v is not a start and not a point of C. So v = f(u) for a point u of
another chain C', evaluated at some k < tau, and u != p_tau (before tau all
inputs are distinct, Section 7.2). Then (p_tau, u) is already a collision
of f. Let z' be the first DP on the forward path v, f(v), f(f(v)), ...

Path length. Every point of the path v, f(v), ..., z' is evaluated first
by C'. If C' had completed before tau (case (a) below), it did so with no
contact. If C' is in flight, it is ahead of C on the path, and by B5 none
of its evaluations at unevaluated points in the window has its output in V.
So C' never merges into a third chain before z', and the path from v to z'
consists of fresh outputs of C' alone. By B3, C' makes fewer than 2^39
consecutive fresh non-DP outputs. So the distance d from v to z' is at
most 2^39, and the length of C' at u is below 2^39. C's outputs up to tau
are fresh and all but v are non-DP, so C's length at tau is a <= 2^39.
Hence C reaches z' at length a + d <= 2^40 = Lab, and C' reaches it at
length at most 2^40. Every earlier sweep saw a length below Lab. The DP is
processed in DPLOOP before that batch's sweep. So neither chain is
abandoned, and both reach z' within 2^39 batches of b*, inside the B5
window.

Order of arrival. There are three concurrency cases:
(a) C' had completed before tau. Its record (s', l') for z' is already in
    the trie.
(b) C' is in flight in another slot j', and k lies in an earlier batch
    than b*. C' is then at least one batch ahead of C on the common path,
    so it reaches z' in an earlier batch and inserts it first.
(c) C' is in flight in slot j' < j*, and k lies in batch b* itself (a
    same-batch collision). C and C' then hold the same point in every
    later batch and reach z' in the same batch. DPLOOP processes slots in
    increasing order, so C' (lower slot) inserts z' and C then finds it.
k cannot lie in a later batch, or in batch b* at a higher slot, because k < tau.

The drain does not interfere. After b >= B0, in-flight chains keep running
until their DP or abandonment, and neither C nor C' is abandoned. B4
excludes the record-cap halt. No other RELOCATE can come first. A RELOCATE
needs a repeated DP, so it needs a contact. Before tau there is none. Inside
the window, B5 excludes every further contact at an unevaluated point. So
the only evaluations whose outputs lie in V are C's evaluations along the
path from v, and the only repeated DP is z', reached by C. The RELOCATE is
therefore between C and C', and Lemma 2 applies because B1 and B2 hold for
the whole run. So the run outputs a collision.

### 7.7 Result

Pr(success) >= 1 - exp(-K0(K0+1)/(2N)) - eps.

K0^2/(2N) = 68600^2 / 2^33 = 4705960000 / 8589934592 = 0.5478458479...,
and K0(K0+1)/(2N) exceeds it by less than 2^-128.
1 - exp(-0.5478458479) = 0.4218060124. Subtracting eps < 7.8e-10 gives

    Pr(success) >= 0.4218060116 > 0.42.

The JSON reports `success_probability: 0.42`, rounded **down** from the
bound. The bound clears the 0.39 gate by 0.0318, so no rounding near the
gate is involved. K0 was chosen as large as the claimed 125.58 allows while
keeping this margin (Section 8). It is the probability of this fixed
algorithm over its own coins under H-RF, not a confidence in H-RF.

## 8. Total charged time (worst case for every run)

| Phase | Count bound | Charge (units) | log2 of product |
|---|---|---|---:|
| Bit-sliced batches (gates + placements, fix-ups, digest copies, DP test, control) | at most B0 + L batches = (K0 + 256L)/256 | 256 * 290 / 1626 per batch | 125.578719 |
| Per-chain work (SEED, DPLOOP incl. trie, abandonment) | at most 2^98 + 2^89 + 257 chains | 2^13 / 1626 per chain | 100.3357 |
| RELOCATE | at most 3L scalar f, L = 2^40 + 2^38 | 1 + 192/1626 each | 42.068 |
| OUTPUT, setup, RELOCATE control | 1 | 3 | 1.585 |
| SWEEP scans (no-abandon case, including the drain) | at most (B0 + L)/2^38 + 1 sweeps of 2^12 ops | 2^12 / 1626 per sweep | 83.40 |

    T <= (K0 + 256L) * 290/1626 + (2^98 + 2^89 + 257) * 2^13/1626
         + 3L * (1 + 192/1626) + ((B0 + L)/2^38 + 1) * 2^12/1626 + 3

The SWEEP term is ((68600 * 2^104 + L)/2^38 + 1) * 2^12 / 1626 = 2^83.40,
included for completeness; it is 2^-42.2 relative to term 1.

Term 1: log2 K0 = 128.0659210, log2(290/1626) = -2.4872025, and
K0 + 256L < K0 (1 + 2^-79.7). Term 1 = 2^125.5787185.
The other terms (per-chain, RELOCATE, SWEEP, OUTPUT) add a relative
2^-25.2, i.e. 3.6e-8 bits; the SWEEP term alone is 2^-42.2 relative.

    log2 T <= 125.5787186 < 125.58.

The claimed `time_log2: 125.58` leaves a factor 2^0.0013 = 1.0009. That
absorbs up to c = 290.26 operations per evaluation, against the 290
charged and 289.05 itemised in Section 3.6. K0 = 68600 * 2^112 was chosen to
raise the success bound while keeping T under 125.58 (the largest admissible
multiple is 68660 * 2^112). This improves on the pending leader (winglock
377eebd, 125.655) by 0.075 bits under a convention winglock's own note
states, and that three r6 packages used (Section 2). Every failed and abandoned
chain, every trie step, every load and store of the core, the drain, the DP
tests, RELOCATE and the final verification are included. There is no
precomputation beyond SETUP and the initial seeding (Section 9), no stored
collision, no search over parameters or coins, and no repetition.

Sensitivity (same algorithm, only the per-evaluation charge c varies):

| Convention for the same circuit | c | log2 T |
|---|---:|---:|
| fixed bank, gates only, no placement (less conservative; not claimed) | 144 | 124.57 |
| **fixed bank (at most 2050 words), one placement per gate result (#178-style, claimed)** | **290** | **125.58** |
| winglock 377eebd published charge, for comparison | 320 | 125.72 |
| genuine 64-register file, Belady schedule, +1 per direct access (winglock's stricter rule; our state spills) | 605 | 126.64 |
| memory-to-memory, every operand a load and every result a store (the companion `package_r6` basis; 516.43 itemised, 518 charged) | 518 | 126.42 |

Only the bolded row is claimed. The gates-only row (124.57) is the
convention our earlier dossier used; we do not claim it, because it charges
no placement. The 605 row shows that under winglock's stricter narrow
64-register rule our six-round circuit does not improve on 125.655, which
is why the claim uses the broad fixed-bank convention. The other rows locate
the lever and bound the claim. Complement tracking (Section 3.2) matters:
without it the gate count rises from 36703 to about 39963 per batch, giving
about (2*39963 + 334)/256 = 313.5 operations per evaluation and 2^125.69,
which would not support the claim (it would not beat 125.655 either).
Complement tracking is part of the compiled program the organizer executes
(Appendix A), so the claimed row stands.

## 9. Memory, preprocessing, advice

* Trie: each new key allocates at most 224 nodes of 2 words. With at most
  Dcap = 2^98 keys: 2^98 * 448 * 32 bytes = 2^111.8074 bytes.
* Register bank: at most 2050 words (Section 2.1). Main memory outside the
  bank: the 256-word slot arrays START and SB, ACTIVE and the eight index
  masks. Together fewer than 2^12 words, each 32 bytes. Program text: the unrolled circuit is about 37k
  straight-line instructions plus the loops, below 8 MB at 4 words per
  instruction. The fixed area is below 2^24 bytes.
* No messages are retained beyond chain starts. No sort table. No
  transposes.

M <= 2^111.8074 + 2^24 < 2^112 bytes: `memory_log2_bytes: 112`.

Preprocessing. The only work before the first batch is SETUP: zeroing the
fixed area and the 256 planes, writing the eight index masks and ACTIVE,
and the 256 initial SEED calls. SETUP is at most 600 operations and each
initial SEED is at most 1800 operations, so preprocessing is at most
600 + 256*1800 = 461400 word operations = 461400/1626 = 283.76 target
compressions, whose log2 is 8.1485. We declare `preprocessing_log2: 9`, an
honest ceiling (2^9 = 512 units). This same work is also inside the
per-chain time term of Section 8 (the 256 initial chains are 256 of the at
most 2^98 + 2^89 + 257 chains, each charged 2^13), so it is charged once in
T and separately bounded here; there is no omitted work and no contradiction
between the two declarations. Advice is zero bytes, reported as 0 (at most
one byte). `data_log2` is omitted.

## 10. Organizer-executed experiments

All experiments use one standard-library program,
`experiments/slot_dp_walk.py`, included in this package, branching on the
experiment id. To avoid shipping a second file, the program builds the
circuit's Python source in-process from the Section 3.2 rules and runs it
with `exec(compile(...))`; that generated code reads no input and does no
I/O, and only maps 256 plane integers to 256 plane integers. Digests come
only from the compiled circuit `compile_circuit` (Appendix A). RELOCATE's
scalar f is a separate 25-lane implementation of Section 1. The organizer
recomputes every returned pair with its own reference implementation and
checks the declared event. Nothing the program prints is trusted.

The manifest declares eight experiments in three families.

**`bitslice-fullwidth-equivalence`** (12-bit mask). 256 uniformly seeded
full-width inputs, one bit-sliced batch, and a returned pair whose
bit-sliced digests agree on digest bits 0-2 of each digest lane. This is a
mechanical cross-check touching all four output lanes. It is not a full
256-bit equivalence test, and an XOR mask cannot detect an error identical
on both returned messages.

**`slot-dp-walk-n14`** (14-bit mask). The complete Section 5 algorithm at
reduced width n = 14: step x <- (bit-sliced digest planes 0..13 of
LE32(x)); 256 slots; DP = digest bit 13 zero (theta = 1/2), keyed on bits
0..12; abandonment at 16; reseeding stops after 256 evaluations, then the
drain; same-batch DPs in slot order; halt at the first RELOCATE. Returned
pairs are absolute 14-bit collisions of the real target.

**`contact-n18-k00, k02, k04, k06, k08, k10`** (18-bit masks). The contact
process behind Lemma 1, at reduced width: N = 2^18, exactly K = 512
evaluations (two batches; the loop stops at exactly K), 256 distinct
uniform starts, 256 slots in batch-major, slot-minor order; K^2/2N = 0.5
(the full attack's K0^2/2N is 0.5478). Set k fixes an 18-bit input window
(message bits (7k + 11i) mod 256) and an 18-bit output window (digest bits
k + 12i); the six output windows are disjoint. The six k were fixed before
any run. A trial returns the first-contact collision pair (an absolute
18-bit collision), or null if the first contact lands on a start or no
contact occurs within K.

Random-function prediction for this exact harness. Before the first
contact, the known set at evaluation e holds the 256 starts and e - 1
earlier outputs, all distinct. Under a random function the output is
uniform, so

    P(success) = sum_{e=1..K} [ prod_{i<e} (1 - (255 + i)/N) ] (e - 1)/N
               = 0.28850          (N = 2^18, K = 512),

with P(no contact within K) = 0.36785 and P(first contact on a start) =
0.34366. A Monte Carlo of the identical loop with a lazily sampled true
random function gave 1750/6000 = 0.2917 (+0.5 sd), which agrees.

Results in our run of the organizer executor with the public seed. We ran
`experiments/runner.py` with its own Docker command (pinned image
`python:3.12.12-slim-bookworm`, no network, read-only, 1 CPU, 128 MiB,
20 s), the public seed `hashsmash-public-seed-v1`, 256 trials per
experiment, and the organizer's target-config fingerprint 8bc09b76... (see
the note below). Each experiment ran twice with byte-identical output, in
2.9 to 4.0 s of container wall time per execution (a second gate run with the
stock tool measured 3.1 to 5.5 s), against the 20 s limit. The trusted organizer
report governs; a holdout nonce changes every count.

| experiment | successes / 256 | invalid pairs |
|---|---:|---:|
| bitslice-fullwidth-equivalence | 256 | 0 |
| slot-dp-walk-n14 | 127 | 0 |
| contact-n18-k00 | 79 | 0 |
| contact-n18-k02 | 77 | 0 |
| contact-n18-k04 | 66 | 0 |
| contact-n18-k06 | 69 | 0 |
| contact-n18-k08 | 76 | 0 |
| contact-n18-k10 | 71 | 0 |

The six contact runs total 438/1536 = 0.2852 against the prediction
0.28850 (0.3 binomial standard deviations low; descriptive only).

Every six-round contact run we made, all program versions, in order. A
version marked * stopped the loop only at batch boundaries, so its real K
(2304) exceeded its stated K (2106); its prediction below uses the real K.
"Windows fp" runs used a seed fingerprint that the organizer does not use.

| run | successes / trials | frequency | RF prediction | z |
|---|---:|---:|---:|---:|
| n=24, K=4352, 2 windows, local seeds | 205/512 | 0.4004 | 0.4137 | -0.6 |
| n=22, K=2304*, 3 windows, local seeds | 305/768 | 0.3971 | 0.4297 | -1.8 |
| n=22, K=2304*, 12 windows, local seeds | 1337/3072 | 0.4352 | 0.4297 | +0.6 |
| n=22, K=2304*, 6 windows, Docker, Windows fp | 634/1536 | 0.4128 | 0.4297 | -1.3 |
| n=20, K=1024, 6 windows, Docker, Windows fp | 480/1536 | 0.3125 | 0.3363 | -2.0 |
| n=19, K=768, 6 windows, Docker, organizer fp | 483/1536 | 0.3145 | 0.3410 | -2.2 |
| n=19, K=768, 6 windows, Docker, Windows fp | 523/1536 | 0.3405 | 0.3410 | -0.0 |
| n=19, K=768, 6 windows, local seeds | 2142/6144 | 0.3486 | 0.3410 | +1.3 |
| n=18, K=512, 6 windows, Docker, organizer fp (above) | 438/1536 | 0.2852 | 0.2885 | -0.3 |
| n=18, K=512, 6 windows, local seeds | 1699/6144 | 0.2765 | 0.2885 | -2.1 |
| n=18, K=512, 6 windows, Docker, Windows fp | 408/1536 | 0.2656 | 0.2885 | -2.0 |
| subtotal, the runs above | 8654/25856 | 0.3347 | 8840 expected | -2.45 |
| n=18, K=512, 12 windows (6 declared, 6 undeclared odd k), fresh seeds, internal gate seat, seed not recorded | 14169/49152 | 0.2883 | 0.2885 | -0.1 |
| n=18, K=512, 12 windows (6 declared, 6 undeclared odd k), fresh seeds, base seed 20261005 | 14189/49152 | 0.2887 | 0.2885 | +0.1 |
| **all six-round runs** | **37012/124160** | | **37201 expected** | **-1.17** |

The last two rows were run after the subtotal's shortfall was noticed, as
a confirmatory check: each uses 4096 trials on each of the six declared
windows and on six undeclared windows (odd k = 1..11, disjoint from the
declared ones), with the package's own `contact_trial` and compiled
circuit. The second of them can be regenerated exactly from its recorded
base seed (trial seed = base + 1000003 k + i for window k, trial i). Per
window, base seed 20261005, successes were 1208, 1168, 1209, 1145, 1200,
1192, 1183, 1196, 1160, 1202, 1192, 1134 for k = 0..11.

One further local n=22 run was made whose output was not captured; it is
not in the table. Controls on the identical harness (exact K, same
windows, same order), current version only: full 24-round SHA3-256 in
place of the six-round map gave 2065/6000 = 0.3442 at n = 19 (+0.5 sd) and
1771/6000 = 0.2952 at n = 18 (+1.1 sd); the true random function gave
0.3448 (n = 19) and 0.2917 (n = 18). An earlier "24-round control 0.368"
was not run on the identical harness and is withdrawn.

Reading. The six-round frequencies are consistent with the
random-function prediction. Run by run they lie within about 2.2 standard
deviations of it; the organizer-seed run of the final version is at -0.3 sd;
the two large fresh-seed runs (98,304 trials) are at -0.1 and +0.1 sd; and
the identical harness with 24-round SHA3-256 or a true random function also
matches. The earlier subtotal shortfall (2.1%, -2.45 sd over 25,856 trials)
does not persist: over all 124,160 six-round trials, successes are 0.51%
below expectation (-1.17 sd). These are descriptive comparisons: the runner
records `probability_inference: none`, runs share structure (same windows
across seeds, several program versions), and we derive no bound from them.
The Section 7 bound is analytic under H-RF and uses none of these numbers.

How a shortfall would carry to full width. The harness success frequency is
not the contact probability: success requires that the first contact land
on an earlier output, in competition with first contacts on a start (34%)
and with no contact within K (37%). The natural carry-over model is a lower
per-evaluation contact rate lambda (lambda = 1 under H-RF), applied to both
outputs and starts in the exact formula above, and at full width to the
contact bound, which becomes 1 - exp(-lambda K0^2/2N). Mapping each harness
shortfall to its lambda and then to the full width at K0 = 68600 * 2^112:

| harness success shortfall | lambda | full-width success bound |
|---|---:|---:|
| 0.51% (all runs, observed) | 0.990 | 0.4185 |
| 1.22% (all runs, one-sided 95% upper end) | 0.975 | 0.4139 |
| 2.11% (earlier subtotal, observed) | 0.958 | 0.4083 |
| 3.52% (earlier subtotal, one-sided 95% upper end) | 0.931 | 0.3996 |
| 5.10% | 0.902 | 0.3900 (the 0.39 gate is used up) |

Even the worst row taken from the data, the earlier subtotal's 95% upper end,
leaves the bound above 0.39. The gate would be used up only by a harness
shortfall of 5.10%, a contact-rate deficit of 9.8% (lambda = 0.902).

Note on seeds and versions. The runner derives every trial seed from the
public seed and the target-config fingerprint. A Windows (CRLF) checkout of
the repository gives a different fingerprint (79ed66e1...) from the LF
checkout the organizer uses (8bc09b76...). An earlier walk count of 172
against the organizer's 177 came from that fingerprint difference, not
from the Python version: the sandbox always runs Python 3.12.12. The table
of organizer-seed results above uses the organizer's fingerprint.

What these experiments establish. On the real target: absolute 14-bit and
18-bit collisions returned through the bit-sliced circuit, the in-place
digest feedback, the DP plane test, slot extraction on the non-DP planes,
sequential same-batch processing, the drain and RELOCATE; and a
predicted-versus-observed comparison of the contact process that Lemma 1
models.

What they do not establish. No full 256-bit circuit-equivalence certificate
(that rests on the deterministic argument of Section 3.5 and Appendix A),
no full-scale cost, and no full-width success probability. The reduced
frequencies are not estimates of the full-width 0.41.

## 11. Heuristics (complete list)

**H-RF (score-critical, only for success probability).** The statement is
in Section 7.1.
* Scope: the fixed six-round prefix SHA3-256 on 32-byte messages LE32(x).
  These have 4 variable input lanes and 21 constant lanes. It is iterated
  along chains from uniform 256-bit starts, over at most E_max < 1.0468 * 2^128
  evaluations.
* Role: it lower-bounds Pr(contact by K0) in Lemma 1 and the bad events in
  Section 7.3. It is not used for correctness (Section 6), time, memory or
  preprocessing.
* Evidence: the standard van Oorschot-Wiener premise, judged plausible for
  the same map in #28. #28 supported it with its own reduced-n runs
  (n = 24 to 48, not organizer-executed) comparing measured success and
  contact frequencies with the Lemma 1 prediction, and a 24-round keyed
  control. Ours adds organizer-executed runs: the six `contact-n18`
  experiments run the Lemma 1 contact process on the real map and return
  organizer-recomputed absolute 18-bit collisions, compared with the exact
  random-function prediction for that harness (0.28850). In our run of the
  organizer executor with the public seed the pooled frequency was 0.2852
  (-0.3 sd). Two fresh-seed runs of 49,152 trials each over 12 windows gave
  0.2883 and 0.2887 (-0.1 and +0.1 sd; one has its seed recorded). Over all
  124,160 six-round trials (every program version, Section 10) successes
  are 0.51% below expectation (-1.17 sd), and the identical harness with
  24-round SHA3-256 or a true random function matches the prediction. This
  is consistent with the random-function prediction; it is descriptive
  reduced-width evidence, not a full-width proof and not a statistical test.
* Extrapolation: from the n = 18 contact runs (and the earlier n = 19 to 24
  runs of Section 10) and the n = 14 walk on the real map, and the general
  behaviour of six-round Keccak, to the full 256-bit map. Under the
  contact-rate carry-over model of Section 10, the observed 0.51% harness
  shortfall would give a full-width success bound of 0.4185, and its
  one-sided 95% upper end (1.22%) 0.4139; the 0.39 gate is used up only at a
  5.10% harness shortfall (lambda = 0.902).
* Sensitivity: the H-RF contact bound is 0.4218060 and the success bound is
  0.4218060 - 7.8e-10. Success stays at least 0.39 for any contact-rate
  multiplier lambda >= 0.902, i.e. a contact-probability shortfall up to
  0.0318, with no change to the algorithm or the claim. Near K0 the bound
  rises by about 0.439 per bit of K0. The time slack under 125.58 is 0.0013
  bits. The claim is for the fixed K0 above.
* Limitations: H-RF is false as a literal statement about a fixed
  deterministic function. Six-round SHA3-256 has known differential
  structure. The best published classical results we found reach real
  collisions at 5 rounds (Guo, Liao, Liu, Liu, Qiao, Song, J. Cryptology
  2020) and a 6-bit near-collision at 6 rounds (Tu, Song, Wu, Guo, Weng,
  Xing, ePrint 2026/2107, abstract only). Guo, Liu, Song, Tu (ASIACRYPT
  2022) report that their classical 6-round SHA3-256 collision approach
  does not reach below the birthday bound. Those results use chosen
  differences, which an iterated random walk does not produce. No result
  showing that six-round SHA3-256, restricted to this input set, iterates
  measurably unlike a random mapping was found in this survey. The survey
  covered those papers, the keccak.team third-party cryptanalysis list,
  and 2024-2026 searches. Absence of evidence is not a proof.

**Not assumed.** There is no heuristic about memory, cost or circuit
correctness: the circuit is exact and the costs are worst-case. There is
no independence between rounds, no differential trail, and no PRNG-quality
premise for the full attack: RAND is the model's primitive. The experiment
frequencies enter only as descriptive predicted-versus-observed
comparisons (Section 10); no interval, test or bound is derived from them,
so no assumption about the independence of experiment trials is needed.

## 12. Prior work and credit

* P. C. van Oorschot and M. J. Wiener, "Parallel Collision Search with
  Cryptanalytic Applications", J. Cryptology 12(1):1-28, 1999: the
  distinguished-point method.
* #28 (winglock), sha3-256-r6 at 128.014: the distinguished-point walk on
  this exact step map. We reuse its trie (DPFOUND), record cap, chain bound
  and the sequential form of its success lemmas, which Sections 7.4-7.6
  rewrite for 256 concurrent chains.
* #148 (may93182), sha3-256-r6 at 126.995: 256-message bit-sliced
  evaluation of the six-round permutation in the 256-bit RAM.
* #170 (ercumentyildirim), sha3-256-r6 at 126.92: the final-round
  projection to the four digest lanes (Section 3.3).
* #178 (zeeshan8281), sha3-256-r6 at 126.902: the
  padding-specialised first-round constant folding (Section 3.3), and the
  equivalence-experiment format we follow.

These four r6 packages are unpromoted, in-review work. Their authors are
credited as coauthors of the reused ideas. Our addition is the combination:
the bit-sliced core inside a distinguished-point walk, with slots as
chains, in-place feedback, the slot-DP machinery, its concurrency proof,
and a fully memory-charged cost bound. No earlier r6 package combining
bit slicing with distinguished points was found in this survey (open r6
PRs through #180).

## 13. Limitations

* This is a generic birthday-bound attack. It is far from practical and is
  not a structural break of SHA3. It gains a constant factor over the
  bit-sliced birthday-and-sort packages by removing the transposes and the
  sort. It costs one random-function heuristic, which those packages avoid.
* The margin above 0.39 is 0.0318 under H-RF (Section 11, sensitivity).
* The claim depends on the fixed register-bank convention of Section 2,
  the convention #148, #170 and #178 used; their prior acceptance is
  reported (Section 2), not verifiable from this package. Under a
  genuine narrow 64-register file with winglock 377eebd's per-access rule,
  our six-round circuit spills the 1600-plane state and does not beat
  125.655 (Section 8, the 605 row). The companion `package_r6` makes the
  fully memory-charged claim at 126.4, with no register-bank assumption.
* The experiments are reduced-width. The walk and the six n = 18 contact
  runs return organizer-recomputed absolute collisions (14 and 18 bits). The
  contact frequencies are consistent with the random-function prediction
  (all 124,160 trials: -0.51%, -1.17 sd); under the Section 10 carry-over
  model even the one-sided 95% upper end of the shortfall leaves the success
  bound at 0.4139, and the gate is used up only at a 5.10% harness
  shortfall. They do not establish full-256-bit circuit
  equivalence (which rests on the Section 3.5 / Appendix A induction) or
  full-scale success probability.
* Preprocessing is declared at 2^9 (SETUP + 256 initial SEEDs, 2^8.1485
  actual); it is also inside the total time term, so it is bounded twice and
  omitted nowhere.


## Appendix A. The circuit generator (exact source)

The compiled bit-sliced circuit of Section 3 is produced by the following
`compile_circuit` function, the exact source included in
`experiments/slot_dp_walk.py`. It applies the Section 3.2 rules as a
straight-line program over symbolic plane signals, folds the padding
constants of Section 1, treats rho/pi as index renaming, projects the last
round to the four digest lanes, and emits one Python line per gate. The
result is deterministic and data-independent; the organizer experiments run
this exact code. Reading it establishes, with the induction of Section 3.5,
that each of the 256 slots computes the complete six-round digest.

```python
class Compiler:
    """Symbolic compile of the proof.md Section 3 circuit into straight-line code.

    A signal is ("c", bit) for a public constant plane or ("v", name, flag) where the
    stored plane word is the true plane XOR (flag ? all-ones : 0). XOR with a constant
    and NOT only flip the flag (no instruction). AND of two plain operands is AND;
    of two flagged operands is OR with the flag set (De Morgan); a mixed pair
    materialises one NOT and then an AND.
    """

    def __init__(self):
        self.lines = []
        self.n = 0
        self.ops = {"xor": 0, "and": 0, "or": 0, "not": 0}

    def tmp(self):
        self.n += 1
        return "t%d" % self.n

    def xor(self, a, b):
        if a[0] == "c" and b[0] == "c":
            return ("c", a[1] ^ b[1])
        if a[0] == "c":
            a, b = b, a
        if b[0] == "c":
            return ("v", a[1], a[2] ^ b[1])
        t = self.tmp()
        self.lines.append("%s=%s^%s" % (t, a[1], b[1]))
        self.ops["xor"] += 1
        return ("v", t, a[2] ^ b[2])

    def neg(self, a):
        return ("c", 1 - a[1]) if a[0] == "c" else ("v", a[1], a[2] ^ 1)

    def band(self, a, b):
        if a[0] == "c" and b[0] == "c":
            return ("c", a[1] & b[1])
        if a[0] == "c":
            a, b = b, a
        if b[0] == "c":
            return a if b[1] else ("c", 0)
        t = self.tmp()
        if a[2] == 0 and b[2] == 0:
            self.lines.append("%s=%s&%s" % (t, a[1], b[1]))
            self.ops["and"] += 1
            return ("v", t, 0)
        if a[2] == 1 and b[2] == 1:
            self.lines.append("%s=%s|%s" % (t, a[1], b[1]))
            self.ops["or"] += 1
            return ("v", t, 1)
        if a[2] == 1:
            a, b = b, a
        self.lines.append("%s=%s&(%s^M)" % (t, a[1], b[1]))
        self.ops["not"] += 1
        self.ops["and"] += 1
        return ("v", t, 0)


def compile_circuit():
    cp = Compiler()
    st = [[("c", 0)] * 64 for _ in range(25)]
    for lane in range(4):
        for z in range(64):
            st[lane][z] = ("v", "P[%d]" % (64 * lane + z), 0)
    st[4] = [("c", (0x06 >> z) & 1) for z in range(64)]
    st[16] = [("c", ((1 << 63) >> z) & 1) for z in range(64)]
    for r in range(ROUNDS):
        last = r == ROUNDS - 1
        col = [[None] * 64 for _ in range(5)]
        for x in range(5):
            for z in range(64):
                acc = st[x][z]
                for y in range(1, 5):
                    acc = cp.xor(acc, st[x + 5 * y][z])
                col[x][z] = acc
        dd = [[cp.xor(col[(x - 1) % 5][z], col[(x + 1) % 5][(z - 1) % 64]) for z in range(64)]
              for x in range(5)]
        bb = [None] * 25
        for idx in (range(25) if not last else (0, 6, 12, 18, 24)):
            x, y = idx % 5, idx // 5
            th = [cp.xor(st[idx][z], dd[x][z]) for z in range(64)]
            off = RHO[idx]
            bb[y + 5 * ((2 * x + 3 * y) % 5)] = [th[(z - off) % 64] for z in range(64)]
        out = [None] * 25
        for idx in (range(25) if not last else range(4)):
            x, y = idx % 5, idx // 5
            b1, b2 = bb[(x + 1) % 5 + 5 * y], bb[(x + 2) % 5 + 5 * y]
            out[idx] = [cp.xor(bb[idx][z], cp.band(cp.neg(b1[z]), b2[z])) for z in range(64)]
        out[0] = [cp.xor(out[0][z], ("c", (RC[r] >> z) & 1)) for z in range(64)]
        st = out
    res = []
    fixups = 0
    for lane in range(4):
        for z in range(64):
            s = st[lane][z]
            if s[0] == "c":
                res.append("M" if s[1] else "0")
            elif s[2]:
                res.append("(%s^M)" % s[1])
                fixups += 1
            else:
                res.append(s[1])
    src = "def F(P):\n " + "\n ".join(cp.lines) + "\n return [" + ",".join(res) + "]\n"
    env = {"M": M}
    exec(compile(src, "<bitsliced-sha3-r6>", "exec"), env)
    return env["F"], cp.ops, fixups
```

Correctness argument (deterministic). The initial signals are the message
planes of lanes 0-3 (variable) and the padding constants of lanes 4 and 16
(Section 1); all other lanes are the constant 0. Each round applies theta,
rho, pi, chi and iota to the signals exactly as in Section 1: `xor`
implements theta and iota (XOR with a constant or another plane), the
`rho/pi` renaming is the index permutation `B[...] = th[(z-off) mod 64]`,
and `band`/`neg` implement chi's `B ^ ((NOT B1) AND B2)`. Every rule is a
Boolean identity on the true plane value (the stored word XOR its flag), so
by induction over the six rounds each output signal's true value is the
corresponding digest bit of every slot. The last round computes only the
four digest lanes (Section 3.3). The emitted program therefore computes
f(x) for all 256 slots, independent of the inputs.
