# SHA3-256 prefix rounds 0-5: distinguished-point generic collision search

Selected lane: exploratory. Target: `sha3-256-r6-prefix-v1`.
Cost model: `collision-frontier-v5`, with reference operation cost
C = 1626 for `sha3-256-r6`. One six-round sponge permutation costs 1 unit.
Every other primitive RAM word operation costs 1/1626 units.

Claim: a classical randomized algorithm with the following properties.

* It outputs two distinct 32-byte messages with equal six-round SHA3-256
  digests, on all 256 output bits.
* Its total charged time is at most 2^128.01392 units in every run. The JSON
  rounds this up to `time_log2: 128.014`.
* Its success probability is at least 0.39. This rests on one declared
  heuristic, H-RF: the step map behaves like a random function
  (Sections 6 and 9).
* Its memory is at most 2^112 bytes. It uses no advice, and its
  preprocessing is below one unit.

This is the generic birthday attack. It uses the parallel collision search
of van Oorschot and Wiener with distinguished points, run on one processor
(P. C. van Oorschot and M. J. Wiener, "Parallel Collision Search with
Cryptanalytic Applications", Journal of Cryptology 12(1):1-28, 1999).
The method is the authors'. The parameters, the program, the
probability bounds and the cost accounting below are our own derivation.
Every argument the review needs is written out in this file.

No cryptanalytic advance is claimed. The scalar sits just above the
organizer's nominal 128 because every instruction is charged. The required
`baseline_improved` identifier `sha3-256-r6-nominal-v2` names that nominal
reference only. We do not claim to improve on any established attack.

## 1. Exact target, message map and step function

Let N = 2^256. For a 256-bit word x, let msg(x) = LE32(x). LE32 writes x as
exactly 32 little-endian bytes, including leading zero bytes.
msg is injective, and every msg(x) is a legal message of bit length
256 < 2^64.

The target sponge has a 1600-bit state, rate 1088 bits (136 bytes), capacity
512 bits, an all-zero initial state and a 256-bit output. Padding uses the
SHA3 domain suffix 01 and then pad10*1, with delimited suffix byte 0x06.
A 32-byte message m therefore pads to exactly one 136-byte block:

    m || 06 || (00 repeated 102 times) || 80

There is one absorption and one permutation call. No squeeze permutation
follows, because 32 output bytes are fewer than the 136-byte rate.
There is no feed-forward.

Write the state as 25 lanes A[0..24], with lane index x+5y. Each lane is
64 bits in little-endian byte order. XORing the padded block into the zero
state gives this input state:

    A[0..3] = the four 64-bit lanes of x  (A[j] = bits 64j..64j+63 of x)
    A[4]    = 0x0000000000000006           (byte 32 of the block)
    A[16]   = 0x8000000000000000           (byte 135 of the block)
    all other lanes, A[5..15] and A[17..24], equal 0

PERM6 applies Keccak-f[1600] rounds 0 through 5. This is the prefix
convention, not Keccak-p's last-round convention. In each round all
subscripts are mod 5 and all lane arithmetic is on 64 bits. Each stage
reads the result of the previous stage.

    C[x] = A[x,0] ^ A[x,1] ^ A[x,2] ^ A[x,3] ^ A[x,4]
    D[x] = C[x-1] ^ rot64(C[x+1], 1)
    B[y, 2x+3y] = rot64(A[x,y] ^ D[x], rho[x+5y])
    A[x,y] = B[x,y] ^ ((NOT B[x+1,y]) AND B[x+2,y])
    A[0,0] = A[0,0] ^ RC[round]

Here rot64(v, k) rotates a 64-bit lane left by k bit positions, from bit
i to bit i+k mod 64, and NOT complements the 64 lane bits.
The rho offsets, in x+5y order, are 0,1,62,28,27, 36,44,6,55,20,
3,10,43,25,39, 41,45,15,21,8, 18,2,61,56,14. The six round constants,
in order, are 0x0000000000000001, 0x0000000000008082,
0x800000000000808A, 0x8000000080008000, 0x000000000000808B and
0x0000000080000001.

The digest is the first 32 squeeze bytes. These are lanes A[0..3] in
little-endian order. Define the step map f on 256-bit words by

    f(x) = A[0] + 2^64 A[1] + 2^128 A[2] + 2^192 A[3]   (after PERM6)

so that LE32(f(x)) is exactly the target digest of msg(x).
Whenever x != x' and f(x) = f(x'), the messages msg(x) and msg(x') are
distinct and have equal full 256-bit target digests. That is an ordinary
collision for the selected target. Messages are 32 bytes.
The digest-to-message map msg is injective, so a chain of f-evaluations is
a chain of complete target hash evaluations.

Check performed by us, not by the organizer: the C program of Appendix A,
run in its `test` mode, prints f on four pseudo-random 32-byte inputs. All
four outputs agree with the repository reference
`verifier/keccak.py:sha3_256(m, rounds=6)`. A separate reimplementation of
f written from this section alone agreed with that reference on 200
inputs (197 random ones plus the all-zero, one and all-ones inputs). These are sanity
tests only; the proof does not depend on them.

## 2. Machine model and charging conventions

The model is a classical probabilistic 256-bit word RAM with a constant
number of 256-bit registers (fewer than 64 are used) and the primitives of
`collision-frontier-v5`. Each primitive costs 1/1626 units:

* 256-bit load and store, including a store of an immediate constant;
* addition and subtraction mod 2^256;
* AND, OR, XOR and NOT;
* shift or rotation (the program below only ever shifts by constant
  amounts);
* comparison;
* conditional branch;
* RAND, one fresh independent uniform 256-bit word.

We also apply the following conservative conventions.

* An unconditional jump is charged as one branch.
* A register-to-register move, and writing an immediate constant into a
  register, are each charged as one operation.
* A comparison and the branch that uses it are two operations.
* The permutation state lives in 25 dedicated registers R0..R24, with
  lane A[j] in the low 64 bits of Rj and the upper bits zero. PERM6 is the
  selected target permutation applied to R0..R24 and costs 1 unit; we
  charge 1 extra operation for issuing it, and never also charge its
  internal operations. This matches how C is defined. docs/RESCORING.md
  states that the reference count "counts additions, logical operations,
  shifts and masks on data words" and that "memory traffic and
  serialization are excluded from this reference normalization". C is
  therefore the price of a permutation on register-resident lanes. Because
  the state is never in memory, no lane load or store occurs around a
  PERM6 call. Every write of a lane register (the constant padding and
  capacity lanes, and the message lanes when a chain starts) is charged
  below as an operation.
* Every memory access the attack makes (the trie, the records, the output
  messages) is charged as a load or store.
* Instruction fetch is not a primitive of this model and is not charged.
  The program has fewer than 1024 instructions, and we count its storage
  in memory (Section 8).
* The algorithm never reads memory it has not written. Its correctness
  therefore does not depend on initial memory contents, and no free
  zero-fill is assumed.

## 3. Parameters

    distinguished point (DP): an f-output z whose low 32 bits are 0
    DP probability     theta = 2^-32 for a uniform output
    maximum chain      L     = 2^40 = 16 * 2^36 evaluations
    evaluation budget  K0    = 65162 * 2^112 = 0.994293212890625 * 2^128
    record cap         Dcap  = 2^98

All of these are constants in the program. All counters and addresses fit
in one 256-bit word. M64 = 2^64 - 1 and M32 = 2^32 - 1 are held in
registers that the setup writes.

## 4. Algorithm

Registers: R0..R24 hold the permutation state. g counts the evaluations in
completed chains, r counts stored records, free is the next unused trie
address, cnt counts the remaining blocks of the current chain, s is the
current chain's start, and t is scratch. ROOT is a two-word trie node in
the fixed memory area. The fixed area starts at a nonzero address, so no
node address is 0.

Setup: write 0 to ROOT[0] and ROOT[1]. Write M64 and M32. Set free to the
first address after the fixed area, and set g = 0 and r = 0. This is at
most 16 operations.

CHAIN (start a new chain). Costs 11 operations.

    if g >= K0: halt with failure                 (compare, branch: 2)
    s = RAND                                      (1)
    R0 = s AND M64                                (1)
    t = s >> 64; R1 = t AND M64                   (2)
    t = s >> 128; R2 = t AND M64                  (2)
    R3 = s >> 192                                 (1)
    cnt = 2^36                                    (1)
    jump BLOCK                                    (1)

The start s is a uniform 256-bit word, and R0..R3 now hold its four lanes.

BLOCK (sixteen evaluations of f, unrolled). For k = 1, ..., 16 the block
contains one copy of the following straight-line code, laid out in
sequence so that copy k falls through to copy k+1:

    R4 = 6; R5..R15 = 0; R16 = 2^63; R17..R24 = 0 (21 immediate writes)
    PERM6(R0..R24)                                (1 unit + 1 op)
    t = R0 AND M32                                (1)
    if t == 0: goto DP_k                          (compare, branch: 2)

After copy 16:

    cnt = cnt - 1                                 (1)
    if cnt != 0: goto BLOCK                       (compare, branch: 2)
    (fall through) ABANDON: g = g + L; goto CHAIN (2, counted per chain)

    DP_k (k = 1..16): off = k; goto DPFOUND       (2, counted per chain)

PERM6 leaves the output lanes in R0..R3. These are exactly the input lanes
of the next message msg(f(x)), so the next copy only rewrites R4..R24. The
input of every evaluation is therefore exactly the padded block of
Section 1. Every evaluation is followed by its own DP test, so a chain
stops at its first DP output, exactly as in a non-unrolled loop. The block
counter only limits the chain: a chain that has found no DP after
16 * 2^36 = L evaluations is abandoned and stores nothing. So the chain
semantics are exactly: iterate f from s, stop at the first DP output, and
abandon after L evaluations without a DP.

Per evaluation this costs 1 unit plus 25 operations, and the 3
block-control operations are executed once per completed block of 16
evaluations. A chain of length len executes at most floor(len/16) block
controls. The main loop therefore costs at most 25 + 3/16 = 403/16
operations per evaluation, in addition to the unit.

DPFOUND. When copy k of block j finds a DP, cnt = 2^36 - (j - 1) and the
chain has made len = 16(j - 1) + k evaluations. The chain's evaluations
are s = x_0, x_1 = f(x_0), ..., x_len = f(x_{len-1}) = z, and z is the
first DP output in the chain.

    t = 2^36; t = t - cnt; t = t << 4; len = t + off   (4)
    g = g + len                                        (1)
    key = R0 OR (R1 << 64) OR (R2 << 128) OR (R3 << 192)
                                          (3 shifts, 3 ORs: 6)
    node = ROOT; i = 224                               (2)
    LEVEL:                                  (at most 17 per level)
        b = key >> 255                                 (1)
        key = key << 1                                 (1)
        p = node + b                                   (1)
        c = load [p]                                   (1)
        if c == 0: goto ALLOC                          (2)
        created = 0; goto JOIN                         (2)
      ALLOC:
        c = free                                       (1)
        store [c] = 0                                  (1)
        t = c + 1; store [t] = 0                       (2)
        free = free + 2                                (1)
        store [p] = c                                  (1)
        created = 1                                    (1)
        (fall through to JOIN)
      JOIN:
        node = c                                       (1)
        i = i - 1                                      (1)
        if i != 0: goto LEVEL                          (2)
    if created == 1: goto NEWKEY                       (2)
    s' = load [node]; t = node + 1; len' = load [t]    (3)
    goto RELOCATE                                      (1)
  NEWKEY:
    store [node] = s; t = node + 1; store [t] = len    (3)
    r = r + 1                                          (1)
    if r == Dcap: halt with failure                    (2)
    goto CHAIN                                         (1)

The DP z has its low 32 bits equal to 0, so key = z carries all of z in
its 224 high bits. Each level takes the current top bit of key with a
constant shift by 255 and then discards it with a constant left shift by 1
(mod 2^256). After 224 levels the descent has used exactly the 224 high
bits of z, from the most significant down. So two DPs reach the same leaf
exactly when they are equal.

This is a binary trie of depth 224. Each node has two words. A value 0
means an empty child; allocated addresses are never 0. Only completed
insertions create nodes, and an insertion always descends the full 224
levels. So the final level creates a node exactly when the key is new. If
the key is old, the leaf holds the record (s', len') of the earlier chain
that ended at the same DP z. Every address offset (c + 1, node + 1) is
computed by its own charged addition.

Operation count of DPFOUND, including the entry stub DP_k:

* entry stub 2, len and g 5, key 6, initialisation 2: 15 in total;
* each level: 6 common operations (two shifts, the add, the load, the
  compare and the branch), then either 2 (else path) or 7 (allocation
  path: c = free, two stores, one add, free = free + 2, store [p] = c,
  created = 1), then 4 at JOIN. That is at most 6 + 7 + 4 = 17;
* exit: at most 2 + 7 = 9 (NEWKEY path) or 2 + 4 = 6 (RELOCATE path).

So one DPFOUND costs at most 15 + 224*17 + 9 = 3832 operations. A chain
executes CHAIN (11) and then either ABANDON (2) or DPFOUND (at most 3832),
so every chain costs at most 3843 < 2^12 operations outside its
evaluations and block controls. We charge 2^13 = 8192 per chain.

RELOCATE((s, len), (s', len')). Name the longer chain (s1, l1) and the
other (s2, l2), with l1 >= l2.

    a = s1; repeat (l1 - l2) times: a = f(a)
    b = s2
    repeat at most l2 times:
        if a == b: halt with failure        (one start lies on the other chain)
        fa = f(a); fb = f(b)
        if fa == fb: goto OUTPUT(a, b)
        a = fa; b = fb
    halt with failure

Each f here writes R0..R3 from a 256-bit register (6 operations, as in
CHAIN), writes R4..R24 (21), issues PERM6 (1 unit + 1) and assembles the
256-bit output from R0..R3 (6, as in DPFOUND): 34 operations. With loop
control, moves and comparisons this is at most 64 operations per
evaluation. RELOCATE makes at most (l1 - l2) + 2*l2 <= 2L evaluations.
We charge 3L evaluations at (1 + 64/C) units each.

OUTPUT(a, b): recompute f(a) and f(b) from freshly written input states
(2 units). Check that a != b and that all 256 output bits are equal. Then
write the two 32-byte messages msg(a) and msg(b) to memory. If the check
fails, halt with failure. This costs at most 2 units plus 200 operations.

There is exactly one run, with no restart and no amplification. The
algorithm halts at its first RELOCATE, whether that RELOCATE succeeds or
fails.

## 5. Every output is a valid collision (unconditional)

OUTPUT is reached only with a != b and f(a) = f(b), and it verifies both by
recomputing them. By Section 1, msg(a) != msg(b) are then two legal
messages with equal full 256-bit six-round SHA3-256 digests. This holds
for every run and needs no heuristic.

## 6. Success probability

### 6.1 The heuristic

H-RF (declared in claim.json): when the algorithm evaluates f at a point x
it has not evaluated before, f(x) is uniform on {0,1}^256 and independent of
the algorithm's coins and of all values it has observed so far.

This is the standard random-mapping premise behind the analysis of
van Oorschot and Wiener. H-RF is used only in this section. Every resource
bound in Sections 4, 7 and 8 is a worst-case bound that holds without it.

### 6.2 Definitions

Number the evaluations in the main loop (CHAIN/BLOCK) 1, 2, 3, ..., and let
p_j be the input of evaluation j. Let V_j be the set of all inputs p_1..p_j
and all outputs f(p_1)..f(p_{j-1}). Every chain start is an input.
Evaluation j makes contact if f(p_j) is in V_j. Let tau be the index of the
first contact.

A start is fresh if it is not in the current V when it is drawn. Before tau
every input is unevaluated: a non-start input is the previous output, which
is not in V, and a start is fresh unless event B1 below occurs.

### 6.3 Lemma 1: contact happens early

With B1 as defined in Section 6.4,

    Pr(no contact among evaluations 1..K0, and B1 does not occur)
        <= exp(-K0(K0+1)/(2N)).

Proof. Let A_j be the event that evaluation j makes no contact and that
any start drawn just before it is fresh. Condition on any history in
which A_1, ..., A_{j-1} hold and the start (if any) is fresh. Then p_j is
unevaluated, and by H-RF f(p_j) is uniform. V_j contains the j distinct inputs
p_1..p_j, so Pr(f(p_j) not in V_j | history) <= 1 - j/N. The chain rule
bounds Pr(A_1 and ... and A_K0) by prod_{j=1..K0} (1 - j/N). Applying 1-u <= e^-u
gives the bound. The main loop starts a new chain while g < K0, so
evaluations 1..K0 all happen unless the run halts first. A halt before K0
evaluations without contact happens only through event B4 below.

### 6.4 Bad events and their probabilities

Let S be the number of chains started before tau and within the first K0
evaluations. Each start after the first follows either a DP output, which is
a fresh uniform value with probability theta of being a DP, or an
abandonment, which needs L evaluations. Hence

    E[S] <= 1 + K0*theta + K0/L = 2^96 (0.994293212890625 + 2^-8 + 2^-96)
         < 0.99818 * 2^96.

When a start is drawn within the first K0 evaluations, |V| <= 2*K0 =
1.98858642578125 * 2^128 < 1.98859 * 2^128.

* B1: some start drawn before tau lies in V. By the two bounds above,
  Pr(B1) <= E[S] * 2K0 / N < 0.99818 * 1.98859 * 2^-32
  = 1.98498 * 2^-32 < 4.63e-10   (2^-32 = 2.3283064e-10).
* B2: the first contact lands on a start, or on an input of the current
  chain. A fixed point is the case where it lands on p_j itself.
  At evaluation j at most S + L such points exist, so
  Pr(B2) <= K0 * (E[S] + L) / N
  < 0.994294 * (0.99818 + 2^-56) * 2^-32 = 0.99248 * 2^-32 < 2.32e-10.
* B3: some chain started before tau has L/2 consecutive non-DP outputs
  among its fresh outputs. Each output is a DP independently with
  probability theta, so
  Pr(B3) <= E[S] * (1-theta)^(L/2) <= E[S] * exp(-theta*L/2)
  = E[S] * exp(-128) < 2^96 * 2^-184.6 < 2^-88.
  If B3 does not occur, no chain is abandoned before tau. Every chain
  completed before tau has length at most L/2, and the current chain has
  made at most L/2 evaluations up to contact.
* B4: Dcap = 2^98 records are reached before the first duplicate DP is
  detected. Before tau, chains share no points, so all stored DPs are
  distinct. The records are then the DPs among at most K0 fresh outputs.
  Their count is dominated by X ~ Binomial(K0, theta), with mean
  mu = K0*theta < 2^96. The Chernoff bound
  Pr(X >= a) <= e^-mu (e*mu/a)^a with a = 2^98 - 1 >= 4*mu gives
  Pr(B4) <= (e/4)^a < 2^-(2^97).

In total, eps = Pr(B1 or B2 or B3 or B4) < 4.63e-10 + 2.32e-10 + 2^-88
+ 2^-(2^97) < 7.0e-10. (Exact evaluation of the four bounds at 80 decimal
digits gives 4.6216e-10, 2.3108e-10, 2.0e-27 and a negligible B4 term.)

### 6.5 Lemma 2: first contact leads to success

Suppose contact happens at some tau <= K0 and none of B1-B4 occurs. Then
the algorithm outputs a collision.

Proof. Let the current chain have start s_c, and let the contact be its
a-th evaluation: f(x_{a-1}) = v. B2 does not occur, so v is neither a start
nor a point of the current chain. B3 does not occur, so no earlier chain was
abandoned. Hence v is a non-start point c'_b (b >= 1) of an earlier completed
chain c' = (s', l'), and c'_b = f(c'_{b-1}).

Before contact every input is unevaluated, so x_{a-1} != c'_{b-1}. This pair
is already a collision of f. Because f is deterministic, the current chain
then follows c'_{b+1}, ..., c'_{l'} = z'. Chain c' stopped at its first DP,
so z' is the first DP the current chain meets, and the chain has length
l_c = a + l' - b. Without B3, a <= L/2 and l' <= L/2, so l_c < L, and the
chain is not abandoned. DPFOUND then finds the key of z' already present.
Before contact all chains are disjoint and, without B4, the run has not
halted, so the stored leaf is (s', l').

The current chain's points x_0..x_{a-1} are disjoint from the points of
c'. Here x_0 = s_c is a fresh start (no B1). Each x_i with 1 <= i <= a-1 is
an output made before the first contact, so it was not in V when it was
produced. Every point of c' was already in V at that time.

RELOCATE aligns the two chains so that each is the same number of
evaluations, min(l_c, l'), away from z'. If a >= b, it advances the current
chain by a - b steps to x_{a-b}, and the walks are (x_{a-b+k}, c'_k).
If a < b, it advances c' by b - a steps, and the walks are (x_k, c'_{b-a+k}).
In both cases, for steps before the walks reach x_a = v = c'_b, one walk
is at a point x_i with i < a and the other at a point of c'. By
disjointness these differ, so the a == b test does not fire. At the next
step both walks reach v. The previous pair (x_{a-1}, c'_{b-1}) is
distinct and has equal images, so RELOCATE reaches OUTPUT with a != b, and
OUTPUT's check succeeds.

This is the first duplicate the run meets. Before contact all DPs are
distinct, and no other chain completes between the contact and this
DPFOUND.

### 6.6 Result

Combining Lemmas 1 and 2:

    Pr(success) >= 1 - exp(-K0(K0+1)/(2N)) - eps.

With K0 = 65162 * 2^112:
K0^2 / (2N) = 65162^2 / 2^33 = 4246086244 / 8589934592 = 0.4943094966,
and K0(K0+1)/(2N) exceeds this by less than 2^-128.
Also -ln(0.61) = 0.4942963218. The difference is
d = 1.3175e-5 > 0, so
exp(-K0(K0+1)/(2N)) <= 0.61 * e^-d <= 0.61 * (1 - d + d^2/2) < 0.61 - 8.03e-6.
Therefore

    Pr(success) > 0.39 + 8.03e-6 - 7.0e-10 > 0.39 + 8.0e-6.

(At 80 digits, 1 - exp(-K0(K0+1)/(2N)) - eps = 0.3900080358.)

The margin above 0.39 is deliberately small. K0 = 65162 * 2^112 is the
smallest multiple of 2^112 for which this bound reaches 0.39. Under H-RF
the bound is exact arithmetic, not an estimate, so the size of the margin
does not affect its validity. A larger margin would cost time: for
example K0 = 65300 * 2^112 gives a bound of about 0.3913 and
log2 T of about 128.0170 instead of 128.0139. The effect of a possible
departure from H-RF is quantified in Section 9 (Sensitivity).

The JSON reports `success_probability: 0.39`. This is the probability that
this fixed algorithm succeeds over its own coins under H-RF. It is not a
statement of confidence in the heuristic or in any review.

## 7. Total charged time (worst case for every run)

| Phase | Bound on count | Charge per item (units) |
| --- | ---: | ---: |
| Main-loop evaluations (BLOCK) | at most K0 - 1 + L | 1 + 403/(16*1626) = 1 + 403/26016 |
| Per-chain work outside evaluations (CHAIN, DPFOUND, ABANDON) | at most 2^98 + 2^88 + 1 chains | 2^13/1626 |
| RELOCATE evaluations (at most one RELOCATE) | at most 3L | 1 + 64/1626 |
| OUTPUT recomputation and emission, setup | 1 | 2 + 216/1626 |

Why these counts are worst-case bounds:

* A chain starts only while g < K0. Here g counts every evaluation of the
  earlier chains, and a chain makes at most L evaluations, so the main loop
  makes at most K0 - 1 + L evaluations.
* The block-control operations are at most 3/16 per evaluation
  (Section 4), so 403/16 operations per main-loop evaluation is an upper
  bound for every chain, including abandoned chains and chains that stop
  inside a block.
* At most Dcap chains store a record, because the run halts when r = Dcap.
  An abandoned chain uses exactly L evaluations, so at most
  (K0 - 1 + L)/L < 2^88 + 1 chains are abandoned. The last chain may end at
  a duplicate DP.
* The run halts at its first RELOCATE.

Every failed trial, abandoned chain, trie operation, comparison and
verification is included above. Summing:

    T <= (K0 - 1 + L)(1 + 403/26016) + (2^98+2^88+1) 2^13/1626
         + 3*2^40 (1 + 64/1626) + 2 + 216/1626.

The second term is below 2^100.34, the third below 2^41.7, and the last
below 3. Relative to K0 (1 + 403/26016), which is about 2^128.0139, their
sum is below 2^-27.67. Also K0 - 1 + L < K0 (1 + 2^-87.99). Hence

    T <= K0 (26419/26016) (1 + 2^-87.99 + 2^-27.67) <= K0 (26419/26016) (1 + 2^-27.6),

and, using ln(1+u) <= u,

    log2 T <= log2 K0 + log2(26419/26016) + 2^-27.6/ln 2
            = (128 - 0.0082567357) + 0.0221766969 + 0.0000000071
            = 128.0139199683...

where log2(65162/65536) = -0.0082567357 and log2(26419/26016) =
0.0221766969 (each rounded at the tenth decimal). The claimed scalar is
`time_log2: 128.014`, rounded up from 128.01392.

The 0.0222 bits above log2 K0 = 127.9917 come from the 403/16 = 25.1875
non-permutation operations per evaluation:

* 21 immediate register writes reset the constant padding and capacity
  lanes R4..R24 (PERM6 overwrites them, so they cannot be skipped);
* 1 operation issues the PERM6 call;
* 3 operations test for a DP (AND, compare, branch);
* 3/16 operations update and test the block counter.

In the 256-bit RAM, 32-byte messages let each output be the next input
without format conversion: the output lanes are already in R0..R3.

The run is never repeated, and no work happens outside the program. In
particular there is no stored collision, no search for favorable
parameters or coins, and no precomputation.

## 8. Memory, preprocessing, advice and data

Peak memory:

* Each new key allocates at most 224 trie nodes of 2 words. The leaf node
  holds (s, len).
* With at most Dcap = 2^98 keys this is at most
  2^98 * 448 words * 32 bytes = 2^98 * 14336 bytes < 2^111.81 bytes.
* The register file (fewer than 64 registers of 32 bytes, including the
  25 state registers), ROOT, the output buffer and the program code (fewer
  than 1024 instructions of at most 4 words each) fit in a fixed area
  under 2^17 bytes.
* No messages other than the current ones are retained. There is no
  sorting table, and no randomness is kept beyond the stored starts.

M <= 2^111.81 + 2^17 < 2^112 bytes, which is reported as
`memory_log2_bytes: 112`. Memory does not affect the scalar.

Preprocessing is the 16-operation setup, below 1 unit, and is already
included in T. It is reported as `preprocessing_log2: 0`, meaning at most
2^0 units.

Nonuniform advice is zero bytes. The schema cannot encode log2(0), so
`nonuniform_advice_log2_bytes: 0` is a conservative upper bound of one
byte. The program and its constants are uniform, and their memory is
counted above.

`data_log2` is omitted because it is optional legacy metadata. All
messages are generated internally, and every complete-message hash
evaluation is a PERM6 call that is already charged in T.

## 9. Evidence for H-RF (our own reduced-output experiments)

These are our own measurements. The organizer has not executed them, and
no experiment manifest is declared, so the judge cannot rerun them here.
They are supporting evidence only: no number below enters the probability
bound in Section 6, which is derived analytically from H-RF. The complete
source of the program is reproduced in Appendix A, and every row below
gives the exact arguments, so each row can be regenerated bit-exactly
(the program is deterministic given its arguments). All rows except the
three n = 48 rows were regenerated a second time from the same source and
arguments, and reproduced exactly.

What the program runs. It runs the Section 4 algorithm with the following
differences:

* the step map is f_n on n-bit words: f_n(x) is the low n bits of lane
  A[0] after PERM6 applied to the padded block of msg(x), where the n-bit
  x is the 32-byte message with zero high bytes. This is the real
  six-round target permutation and padding, restricted to n bits of input
  and output. The six-round map is the same fixed, unkeyed map in every
  trial; only the algorithm's coins differ between trials;
* starts are uniform n-bit words (from a seeded splitmix64 generator), not
  256-bit words;
* a hash map replaces the trie, and there is no record cap Dcap;
* after alignment, RELOCATE tests a == b once rather than before every
  step; for a deterministic f the outcome is the same;
* the parameters are scaled as K0 = ceil(0.9944 * 2^(n/2)), DP probability
  theta_n = 2^-t and L = 2^(t+5) = 32/theta_n. (At full size
  L = 2^8/theta, so abandonment is rarer there.)

"Success" means the run output a verified collision of f_n within the
budget. "Contact <= K0" (measured only for n <= 40, where the program
keeps the set of all visited points) means that within the first K0
evaluations some output, or some start, was already a visited point. It
therefore also counts a start landing on a visited point, which Section 6
classes as event B1 rather than contact. The predicted value is the
Lemma 1 lower bound 1 - exp(-K0(K0+1)/2^(n+1)).

The control replaces the six rounds by the full 24-round Keccak-f[1600]
and keys the map per trial with a random lane A[5]; it is otherwise the
same program.

Program arguments are: n, t, trials, threads, track-visited flag,
c = 0.9944, log2 L, seed, rounds. All rows used c = 0.9944 and L = 2^(t+5).
The per-thread generators are seeded from the seed and the thread index,
so a row is reproduced only with the same seed and thread count.

All runs made with this program, in the order they were made:

| run | n | t | rounds | trials | threads | seed | contact <= K0 | success | predicted |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 24 | 4 | 6 (target) | 2000 | 14 | 7 | 852 (0.4260) | 751 (0.3755) | 0.3903 |
| 2 | 24 | 4 | 24 (control) | 2000 | 14 | 7 | 843 (0.4215) | 756 (0.3780) | 0.3903 |
| 3 | 32 | 8 | 6 (target) | 20000 | 14 | 11 | 7774 (0.3887) | 7759 (0.3880) | 0.3901 |
| 4 | 32 | 8 | 24 (control) | 20000 | 14 | 12 | 7917 (0.3958) | 7852 (0.3926) | 0.3901 |
| 5 | 40 | 10 | 6 (target) | 5000 | 14 | 21 | 2025 (0.4050) | 2025 (0.4050) | 0.3901 |
| 6 | 40 | 10 | 24 (control) | 5000 | 14 | 22 | 1983 (0.3966) | 1976 (0.3952) | 0.3901 |
| 7 | 48 | 12 | 6 (target), batch 1 | 1000 | 14 | 31 | not measured | 372 (0.3720) | 0.3901 |
| 8 | 48 | 12 | 24 (control) | 1000 | 14 | 32 | not measured | 386 (0.3860) | 0.3901 |
| 9 | 32 | 8 | 6 (target), re-run | 20000 | 12 | 777 | 7822 (0.3911) | 7775 (0.3887) | 0.3901 |
| 10 | 32 | 8 | 24 (control), re-run | 20000 | 12 | 778 | 7865 (0.3932) | 7788 (0.3894) | 0.3901 |
| 11 | 48 | 12 | 6 (target), batch 2 | 2000 | 14 | 33 | not measured | 793 (0.3965) | 0.3901 |

Pooled six-round values: n = 32 (runs 3 and 9), 15534/40000 = 0.3884;
n = 48 (runs 7 and 11), 1165/3000 = 0.3883.

Stopping and selection. Runs 1-2 were a small smoke test. Runs 3-8 were
launched together with fixed sizes before any of them had been seen.
Runs 9-10 were an independent re-run of the n = 32 pair with fresh seeds,
made during internal review. Run 11 was made after run 7 had been
observed, to reduce the standard error at n = 48. We report both n = 48
batches and their pooled value. No run made with this program is
omitted, and none was discarded.

Statistics. The binomial standard error of a single proportion near 0.39
is about 0.0109 for 2000 trials, 0.0034 for 20000, 0.0069 for 5000,
0.0089 for 3000 and 0.0154 for 1000. Against the prediction, the six-round
success rates have z-scores -1.36 (run 1), -0.62 (run 3), +2.16 (run 5),
-1.17 (run 7), -0.39 (run 9), +0.59 (run 11) and -0.20 (n = 48 pooled).
The largest deviation (run 5, +0.0149) lies above the prediction, which is
the favourable direction. Against its 24-round control, using the
standard error of the difference sqrt(p1 q1/n1 + p2 q2/n2), each
six-round success rate is within 1.01 standard errors: z = -0.16 (n = 24),
-0.95 (runs 3 vs 4), -0.13 (runs 9 vs 10), +1.00 (n = 40), -0.65
(run 7 vs 8), +0.56 (run 11 vs 8) and +0.13 (n = 48 pooled vs 8). For
the six-round target at these sizes we found no departure from
random-mapping behaviour.

At these small sizes, success falls below contact, and at n = 24 both
success rates (target and control alike) fall below the prediction.
Starts landing on earlier chains (event B1) and the abandonment cap are
non-negligible when theta*sqrt(N) is only 2^8 to 2^12. The program
counted these start collisions per run (97 and 89 trials at n = 24,
fewer than 0.4% of trials at n = 32 and n = 40). At full size these events
fall into eps < 7e-10 (Section 6.4).

Scope and limits of this evidence:

* It tests output widths of 24 to 48 bits, not 256.
* It tests only the restricted input sets of n-bit messages.
* It cannot rule out a structural property that appears only at full width.

We know of no published property of six-round Keccak-f[1600] that predicts
fewer collisions for f than for a random function. For a single fixed
function, a collision rate along pseudo-random walks clearly below the
random-function rate would itself be a strong distinguisher. The
reduced-round Keccak distinguishers we are aware of, such as zero-sum and
cube-type distinguishers, need structured, chosen input sets. A
pseudo-random walk does not choose such sets.

Sensitivity: H-RF affects only the success probability. Near K0, the
random-function contact probability 1 - exp(-c^2/2), with c = K0/2^128,
rises at rate c*exp(-c^2/2), about 0.6065 per unit of c. Suppose the true
contact probability at K0 fell short by a small delta. Restoring 0.39
would then need K0 larger by a factor of about 1 + delta/(c^2 exp(-c^2/2))
= 1 + 1.66*delta, which adds about 2.4*delta bits to the scalar. The cost
and memory bounds would not change.

## 10. Literature status and limitations

To our knowledge, no classical ordinary-collision attack below the birthday
bound is published for six-round SHA3-256. J. Guo, G. Liu, L. Song and
Y. Tu, "Exploring SAT for Cryptanalysis: (Quantum) Collision Attacks
against 6-Round SHA-3" (ASIACRYPT 2022; IACR ePrint 2022/184), give
six-round SHA3-256 collision attacks only in the quantum setting, which
this track excludes. This package is therefore the generic attack with
exact accounting. It makes no novelty claim.

The certificate manifest is empty. No collision for this target is
claimed, and none is computable at this scale.
No experiment manifest is declared, and nothing in this package needs to
be executed by the organizer.

This package is a draft. Qualification and scoring require organizer
review of the exact package. Exploratory qualification
(`plausible_not_refuted`) is neither a mathematical proof nor human
acceptance.

## Appendix A. Source of the reduced-output experiment program

This is the exact C source that produced every row of the Section 9 table
(SHA-256 of the file: 273e5fc67dcb82b0fa4c3d4da1c2b19468401a222b93f8df1be7bc26178d32ee).
It is reproduced verbatim, so its first comment still says it is not part
of the candidate package; it is included here only as evidence. It needs a
C compiler with pthreads and the math library (for example
`cc -O2 vow.c -o vow -lm -lpthread`). `./vow test` prints the four f
cross-check vectors of Section 1 (input, then digest, as hex bytes).

```c
// Reduced-output simulation of the distinguished-point collision search
// on the 6-round SHA3-256 prefix target. Not part of the candidate package.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <pthread.h>

static const uint64_t RC[24] = {
 0x0000000000000001ULL,0x0000000000008082ULL,0x800000000000808AULL,0x8000000080008000ULL,
 0x000000000000808BULL,0x0000000080000001ULL,0x8000000080008081ULL,0x8000000000008009ULL,
 0x000000000000008AULL,0x0000000000000088ULL,0x0000000080008009ULL,0x000000008000000AULL,
 0x000000008000808BULL,0x800000000000008BULL,0x8000000000008089ULL,0x8000000000008003ULL,
 0x8000000000008002ULL,0x8000000000000080ULL,0x000000000000800AULL,0x800000008000000AULL,
 0x8000000080008081ULL,0x8000000000008080ULL,0x0000000080000001ULL,0x8000000080008008ULL};
static int ROUNDS=6; static __thread uint64_t KEYLANE=0;
static const int RHO[25] = {0,1,62,28,27,36,44,6,55,20,3,10,43,25,39,
  41,45,15,21,8,18,2,61,56,14};
static inline uint64_t rol(uint64_t v, int a){ return a? (v<<a)|(v>>(64-a)) : v; }

static void perm6(uint64_t *A){
  uint64_t C[5], D[5], B[25];
  for(int r=0;r<ROUNDS;r++){
    for(int x=0;x<5;x++) C[x]=A[x]^A[x+5]^A[x+10]^A[x+15]^A[x+20];
    for(int x=0;x<5;x++) D[x]=C[(x+4)%5]^rol(C[(x+1)%5],1);
    for(int y=0;y<5;y++) for(int x=0;x<5;x++){
      int i=x+5*y; B[y+5*((2*x+3*y)%5)] = rol(A[i]^D[x], RHO[i]); }
    for(int y=0;y<5;y++) for(int x=0;x<5;x++)
      A[x+5*y] = B[x+5*y] ^ ((~B[(x+1)%5+5*y]) & B[(x+2)%5+5*y]);
    A[0]^=RC[r];
  }
}

// f(x): message = LE32(x) (32 bytes), single padded block, return state lanes 0..3
static inline void f_full(const uint64_t in[4], uint64_t out[4]){
  uint64_t S[25]; memset(S,0,sizeof S);
  S[0]=in[0];S[1]=in[1];S[2]=in[2];S[3]=in[3];S[4]=0x06;S[16]=0x8000000000000000ULL;
  perm6(S); out[0]=S[0];out[1]=S[1];out[2]=S[2];out[3]=S[3];
}
// truncated n-bit map on n-bit inputs (zero-extended to 32 bytes)
static int NB; static uint64_t NMASK;
static inline uint64_t fn(uint64_t x){
  uint64_t S[25]; memset(S,0,sizeof S); S[0]=x; S[5]=KEYLANE; S[4]=0x06; S[16]=0x8000000000000000ULL;
  perm6(S); return S[0]&NMASK;
}

static inline uint64_t splitmix(uint64_t *s){ uint64_t z=(*s+=0x9E3779B97F4A7C15ULL);
  z=(z^(z>>30))*0xBF58476D1CE4E5B9ULL; z=(z^(z>>27))*0x94D049BB133111EBULL; return z^(z>>31);}

// open-addressing hash map keyed by 64-bit value (value+1 stored to reserve 0)
typedef struct { uint64_t *k; uint64_t *v1; uint64_t *v2; uint64_t mask; } map_t;
static void map_init(map_t *m, int bits){ size_t n=(size_t)1<<bits; m->mask=n-1;
  m->k=calloc(n,8); m->v1=malloc(n*8); m->v2=malloc(n*8);}
static void map_clear(map_t *m){ memset(m->k,0,(m->mask+1)*8); }
static inline uint64_t hh(uint64_t k){ k^=k>>33; k*=0xff51afd7ed558ccdULL; k^=k>>33; return k; }
static int map_get(map_t *m, uint64_t key, uint64_t *a, uint64_t *b){
  uint64_t i=hh(key)&m->mask; while(m->k[i]){ if(m->k[i]==key+1){*a=m->v1[i];*b=m->v2[i];return 1;} i=(i+1)&m->mask;} return 0;}
static void map_put(map_t *m, uint64_t key, uint64_t a, uint64_t b){
  uint64_t i=hh(key)&m->mask; while(m->k[i]){ if(m->k[i]==key+1) break; i=(i+1)&m->mask;} m->k[i]=key+1;m->v1[i]=a;m->v2[i]=b;}
static int set_add(map_t *m, uint64_t key){ // returns 1 if already present
  uint64_t i=hh(key)&m->mask; while(m->k[i]){ if(m->k[i]==key+1) return 1; i=(i+1)&m->mask;} m->k[i]=key+1; return 0;}

static int T_BITS; static uint64_t K0, LMAX; static int TRACK;
typedef struct { int id, trials; uint64_t seed; long succ, contact_le_k0, rh, abandoned_total, fail_budget;
  double evals_sum; double tau_sum; long tau_cnt; long hist[64]; } job_t;

// returns 1 on success
static int run_trial(uint64_t *rng, map_t *dp, map_t *vis, job_t *J){
  map_clear(dp); if(TRACK) map_clear(vis);
  if(ROUNDS!=6) KEYLANE=splitmix(rng);
  uint64_t g=0; uint64_t evals=0; uint64_t tau=0; int contact=0;
  uint64_t dpmask=((uint64_t)1<<T_BITS)-1;
  while(g<K0){
    uint64_t s=splitmix(rng)&NMASK, x=s; uint64_t len=0;
    if(TRACK && !contact){ if(set_add(vis,x)){contact=1;tau=evals;} }
    int isdp=0;
    while(len<LMAX){
      uint64_t y=fn(x); len++; evals++;
      if(TRACK && !contact){ if(set_add(vis,y)){contact=1;tau=evals;} }
      if((y&dpmask)==0){ isdp=1; x=y; break;} x=y;
    }
    g+=len;
    if(!isdp){ J->abandoned_total++; continue; }
    uint64_t s2,l2;
    if(map_get(dp,x,&s2,&l2)){
      // relocate
      uint64_t a=s, b=s2, la=len, lb=l2;
      while(la>lb){ a=fn(a); la--; evals++; }
      while(lb>la){ b=fn(b); lb--; evals++; }
      if(a==b){ J->rh++; goto done_fail; }
      for(;;){ uint64_t fa=fn(a), fb=fn(b); evals+=2;
        if(fa==fb){ // a!=b guaranteed here
          // verify
          if(a!=b && fn(a)==fn(b)){ evals+=2; J->succ++; J->evals_sum+=evals;
            if(TRACK){ if(contact && tau<=K0) J->contact_le_k0++; if(contact){J->tau_sum+=tau;J->tau_cnt++;} }
            return 1; }
          goto done_fail; }
        a=fa;b=fb; }
    }
    map_put(dp,x,s,len);
  }
  J->fail_budget++;
done_fail:
  J->evals_sum+=evals;
  if(TRACK){ if(contact && tau<=K0) J->contact_le_k0++; if(contact){J->tau_sum+=tau;J->tau_cnt++;} }
  return 0;
}

static void *worker(void *arg){ job_t *J=arg; uint64_t rng=J->seed;
  map_t dp, vis; int expdp=(int)ceil(log2((double)K0/(double)((uint64_t)1<<T_BITS)))+3; if(expdp<8)expdp=8;
  map_init(&dp,expdp); if(TRACK) map_init(&vis,(int)ceil(log2((double)K0))+3);
  for(int t=0;t<J->trials;t++) run_trial(&rng,&dp,TRACK?&vis:&dp,J); return 0; }

int main(int argc,char**argv){
  if(argc>1 && !strcmp(argv[1],"test")){
    // print f on fixed inputs for cross-check against the organizer reference
    uint64_t seed=12345; for(int i=0;i<4;i++){ uint64_t in[4],out[4]; for(int j=0;j<4;j++) in[j]=splitmix(&seed);
      f_full(in,out); for(int j=0;j<4;j++){ for(int b=0;b<8;b++) printf("%02x",(unsigned)((in[j]>>(8*b))&0xff)); } printf(" ");
      for(int j=0;j<4;j++){ for(int b=0;b<8;b++) printf("%02x",(unsigned)((out[j]>>(8*b))&0xff)); } printf("\n"); }
    return 0; }
  ROUNDS=atoi(argv[9]);
  NB=atoi(argv[1]); T_BITS=atoi(argv[2]); int trials=atoi(argv[3]); int threads=atoi(argv[4]); TRACK=atoi(argv[5]);
  double c=atof(argv[6]); int lexp=atoi(argv[7]); uint64_t seed0=strtoull(argv[8],0,0);
  NMASK=(NB==64)?~0ULL:(((uint64_t)1<<NB)-1);
  K0=(uint64_t)ceil(c*pow(2.0,NB/2.0)); LMAX=(uint64_t)1<<lexp;
  pthread_t th[64]; job_t J[64]; memset(J,0,sizeof J);
  for(int i=0;i<threads;i++){ J[i].id=i; J[i].trials=trials/threads+(i<trials%threads); J[i].seed=seed0*1000003ULL+i*0x1234567ULL+1; pthread_create(&th[i],0,worker,&J[i]); }
  long succ=0,cle=0,rh=0,ab=0,fb=0,tc=0; double es=0,ts=0;
  for(int i=0;i<threads;i++){ pthread_join(th[i],0); succ+=J[i].succ; cle+=J[i].contact_le_k0; rh+=J[i].rh; ab+=J[i].abandoned_total; fb+=J[i].fail_budget; es+=J[i].evals_sum; ts+=J[i].tau_sum; tc+=J[i].tau_cnt; }
  double pred=1-exp(-(double)K0*(K0+1)/(2*pow(2.0,NB)));
  printf("rounds=%d n=%d t=%d L=2^%d K0=%llu trials=%d success=%ld (%.4f) pred_lower=%.4f contact<=K0=%ld (%.4f) RH=%ld abandoned=%ld budget_fail=%ld mean_evals/K0=%.4f mean_tau/sqrtN=%.4f\n",
    ROUNDS,NB,T_BITS,lexp,(unsigned long long)K0,trials,succ,(double)succ/trials,pred,cle,(double)cle/trials,rh,ab,fb,es/trials/K0, tc? ts/tc/pow(2.0,NB/2.0):0);
  return 0;
}
```
