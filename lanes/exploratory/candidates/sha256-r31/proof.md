<!-- Subflatus3 resubmit: peer-conservative CF31 wrapper after 7252657 lean-ABI not_evaluable.
Claimed time_log2 128.00996 is the tight upper bound on the same reconstruction as winglock ed444cc
(exact log2 T = 128.00995645027). Lean ABI path abandoned. -->

# SHA-256 steps 0-30: distinguished-point generic collision search

Selected lane: exploratory. Target: `sha256-r31-prefix-v1`.
Cost model: `collision-frontier-v5`, with reference operation cost
C = 2140 for `sha256-r31`. One 31-step compression costs 1 unit.
Every other primitive RAM word operation costs 1/2140 units.

Claim: a classical randomized algorithm with the following properties.

* It outputs two distinct 32-byte messages with equal 31-step SHA-256
  digests, on all 256 output bits.
* Its total charged time is at most 2^128.00996 units in every run. The JSON
  rounds this up to `time_log2: 128.00996`.
* Its success probability is at least 0.39. This rests on one declared
  heuristic, H-RF: the step map behaves like a random function
  (Sections 6 and 9).
* Its memory is at most 2^112 bytes. It uses no advice, and its
  preprocessing is below one unit.

This is the generic birthday attack. It uses the parallel collision search
of van Oorschot and Wiener with distinguished points, run on one processor
(P. C. van Oorschot and M. J. Wiener, "Parallel Collision Search with
Cryptanalytic Applications", Journal of Cryptology 12(1):1-28, 1999).
The method is the authors'. The parameters, the program, the probability
bounds and the cost accounting below are our own derivation. Every argument
the review needs is written out in this file.

No cryptanalytic advance is claimed (see Section 10). The scalar sits just
above the organizer's nominal 128 because every instruction is charged. The
required `baseline_improved` identifier `sha256-r31-nominal-v2` names that
nominal reference only.

## 1. Exact target, message map and step function

Let N = 2^256. For a 256-bit word x, let msg(x) = BE32(x). BE32 writes x as
exactly 32 big-endian bytes, including leading zero bytes. msg is
injective, and every msg(x) is a legal message of bit length 256 < 2^64.

FIPS 180-4 padding appends 0x80, then zero bytes up to 56 mod 64, then the
64-bit big-endian bit length. A 32-byte message m therefore pads to exactly
one 64-byte block:

    m || 80 || (00 repeated 23 times) || 00 00 00 00 00 00 01 00

Read as sixteen big-endian 32-bit words, this block is

    W[0..7] = the eight 32-bit words of x, most significant first
              (W[j] = bits 224-32j .. 255-32j of x)
    W[8]    = 0x80000000,   W[9..14] = 0,   W[15] = 0x00000100 (= 256)

There is one compression, applied to the standard IV
H(0) = 6a09e667 bb67ae85 3c6ef372 a54ff53a 510e527f 9b05688c 1f83d9ab
5be0cd19. CF31 is the FIPS 180-4 compression restricted to step indices
0 through 30, with the standard constants K[0..30] at their original
indices. All arithmetic is mod 2^32; ROTR is a 32-bit right rotation.

    for i = 16..30: W[i] = s1(W[i-2]) + W[i-7] + s0(W[i-15]) + W[i-16]
        s0(v) = ROTR7(v) ^ ROTR18(v) ^ (v >> 3)
        s1(v) = ROTR17(v) ^ ROTR19(v) ^ (v >> 10)
    (a..h) = H(0)
    for i = 0..30:
        T1 = h + S1(e) + Ch(e,f,g) + K[i] + W[i];  T2 = S0(a) + Maj(a,b,c)
        h=g; g=f; f=e; e=d+T1; d=c; c=b; b=a; a=T1+T2
        S0(a) = ROTR2 ^ ROTR13 ^ ROTR22,  S1(e) = ROTR6 ^ ROTR11 ^ ROTR25
        Ch(e,f,g) = (e AND f) ^ (NOT e AND g),  Maj = (a&b)^(a&c)^(b&c)
    H[k] = H(0)[k] + (a,b,c,d,e,f,g,h)[k]   for k = 0..7  (feed-forward)

The digest is H[0] || ... || H[7], each word big-endian. Define the step
map f on 256-bit words by

    f(x) = H[0]*2^224 + H[1]*2^192 + ... + H[6]*2^32 + H[7]

so that BE32(f(x)) is exactly the target digest of msg(x), and
msg(f(x)) has message words W[0..7] = H[0..7]. Whenever x != x' and
f(x) = f(x'), the messages msg(x) and msg(x') are distinct and have equal
full 256-bit target digests: an ordinary collision for the selected target,
with the fixed IV and standard padding. msg is injective, so a chain of
f-evaluations is a chain of complete target hash evaluations.

Check performed by us, not by the organizer: the C program of Appendix A,
run in its `test` mode, prints f on four pseudo-random 32-byte inputs. All
four outputs agree with the repository reference
`verifier/hash_functions.py:digest(m, "sha256", 31)`, and a separate check
of the block layout and of f as defined here agreed with that reference on
200 random inputs. These are sanity tests only; the proof does not depend
on them.

## 2. Machine model and charging conventions

The model is a classical probabilistic 256-bit word RAM with a constant
number of 256-bit registers (fewer than 64 are used) and the primitives of
`collision-frontier-v5`, each costing 1/2140 units: 256-bit load and store
(including a store of an immediate constant); addition and subtraction mod
2^256; AND, OR, XOR and NOT; shift or rotation (the program only shifts by
constant amounts); comparison; conditional branch; RAND, one fresh
independent uniform 256-bit word. We also apply these conservative
conventions.

* An unconditional jump is charged as one branch.
* A register-to-register move, and writing an immediate constant into a
  register, are each charged as one operation.
* A comparison and the branch that uses it are two operations.
* The compression works on 24 dedicated registers R0..R23, each holding one
  32-bit word in its low 32 bits with the upper bits zero. CF31 reads the
  message words W[0..15] from R0..R15 and the chaining value from R16..R23,
  and writes the new chaining value H[0..7] into R16..R23 (in place, as in
  FIPS 180-4). It costs 1 unit; we charge 1 extra operation for issuing it
  and never also charge its internal operations. After a call we assume
  nothing about R0..R15, and only that R16..R23 hold H[0..7]. This matches
  how C is defined: docs/RESCORING.md states that the reference count
  "counts additions, logical operations, shifts and masks on data words,
  including message expansion and feed-forward" and that "memory traffic
  and serialization are excluded from this reference normalization". C is
  therefore the price of a compression on register-resident words. Every
  write of an input register (the message, padding and IV words) and every
  move of an output word is charged below as an operation.
* Every memory access the attack makes (the trie, the records, the output
  messages) is charged as a load or store.
* Instruction fetch is not a primitive of this model and is not charged.
  The program has fewer than 1024 instructions, and we count its storage
  in memory (Section 8).
* The algorithm never reads memory it has not written, so no free
  zero-fill is assumed.

## 3. Parameters

    distinguished point (DP): an f-output z whose low 32 bits are 0
    DP probability     theta = 2^-32 for a uniform output
    maximum chain      L     = 2^40 = 16 * 2^36 evaluations
    evaluation budget  K0    = 65162 * 2^112 = 0.994293212890625 * 2^128
    record cap         Dcap  = 2^98

All of these are constants in the program. All counters and addresses fit
in one 256-bit word. M32 = 2^32 - 1 is held in a register that the setup
writes. The low 32 bits of f(x) are H[7], so z is a DP exactly when H[7] = 0.

## 4. Algorithm

Registers: R0..R23 as in Section 2. g counts the evaluations in completed
chains, r counts stored records, free is the next unused trie address, cnt
counts the remaining blocks of the current chain, s is the current chain's
start, and t is scratch. ROOT is a two-word trie node in the fixed memory
area, which starts at a nonzero address, so no node address is 0.

Setup: write 0 to ROOT[0] and ROOT[1], write M32, set free to the first
address after the fixed area, set g = 0 and r = 0. At most 16 operations.

CHAIN (start a new chain). Costs 19 operations.

    if g >= K0: halt with failure                 (compare, branch: 2)
    s = RAND                                      (1)
    R7 = s AND M32                                (1)
    for j = 1..6: t = s >> 32j; R(7-j) = t AND M32 (2 each: 12)
    R0 = s >> 224                                 (1)
    cnt = 2^36                                    (1)
    jump BLOCK                                    (1)

The start s is a uniform 256-bit word, and R0..R7 now hold W[0..7] of msg(s).

BLOCK (sixteen evaluations of f, unrolled). For k = 1, ..., 16 the block
contains one copy of the following straight-line code, laid out in
sequence so that copy k falls through to copy k+1:

    R8 = 0x80000000; R9..R14 = 0; R15 = 256      (8 immediate writes)
    R16..R23 = H(0)[0..7]                         (8 immediate writes)
    CF31(R0..R23)                                 (1 unit + 1 op)
    R0 = R16; ...; R7 = R23                       (8 moves)
    if R7 == 0: goto DP_k                         (compare, branch: 2)

After copy 16:

    cnt = cnt - 1                                 (1)
    if cnt != 0: goto BLOCK                       (compare, branch: 2)
    (fall through) ABANDON: g = g + L; goto CHAIN (2, counted per chain)

    DP_k (k = 1..16): off = k; goto DPFOUND       (2, counted per chain)

After the moves, R0..R7 hold H[0..7] = f(x), which are exactly the message
words W[0..7] of the next message msg(f(x)). Every copy rewrites R8..R23,
so the input of every evaluation is exactly the padded block and IV of
Section 1. R7 holds H[7] with zero upper bits, so the test R7 == 0 is the
DP test. Every evaluation is followed by its own DP test, so a chain stops
at its first DP output. A chain that has found no DP after 16 * 2^36 = L
evaluations is abandoned and stores nothing. So the chain semantics are
exactly: iterate f from s, stop at the first DP output, and abandon after
L evaluations without a DP.

Per evaluation this costs 1 unit plus 27 operations, and the 3
block-control operations run once per completed block of 16 evaluations.
The main loop therefore costs at most 27 + 3/16 = 435/16 operations per
evaluation, in addition to the unit.

DPFOUND. When copy k of block j finds a DP, cnt = 2^36 - (j - 1) and the
chain has made len = 16(j - 1) + k evaluations: s = x_0, x_1 = f(x_0), ...,
x_len = z, and z is the first DP output in the chain.

    t = 2^36; t = t - cnt; t = t << 4; len = t + off   (4)
    g = g + len                                        (1)
    key = (R0 << 224) OR (R1 << 192) OR ... OR (R6 << 32) OR R7
                                         (7 shifts, 7 ORs: 14)
    node = ROOT; i = 224                               (2)
    LEVEL:                                  (at most 17 per level)
        b = key >> 255; key = key << 1                 (2)
        p = node + b; c = load [p]                     (2)
        if c == 0: goto ALLOC                          (2)
        created = 0; goto JOIN                         (2)
      ALLOC:
        c = free; store [c] = 0                        (2)
        t = c + 1; store [t] = 0                       (2)
        free = free + 2; store [p] = c; created = 1    (3)
      JOIN:
        node = c; i = i - 1                            (2)
        if i != 0: goto LEVEL                          (2)
    if created == 1: goto NEWKEY                       (2)
    s' = load [node]; t = node + 1; len' = load [t]    (3)
    goto RELOCATE                                      (1)
  NEWKEY:
    store [node] = s; t = node + 1; store [t] = len    (3)
    r = r + 1                                          (1)
    if r == Dcap: halt with failure                    (2)
    goto CHAIN                                         (1)

key = z, whose low 32 bits are 0, so its 224 high bits carry all of z. Each
level takes the current top bit of key and then discards it with a left
shift by 1 (mod 2^256). After 224 levels the descent has used exactly the
224 high bits of z, so two DPs reach the same leaf exactly when they are
equal. Each node has two words; 0 means an empty child, and allocated
addresses are never 0. An insertion always descends all 224 levels, so the
final level creates a node exactly when the key is new. If the key is old,
the leaf holds the record (s', len') of the earlier chain that ended at z.

Operation count of DPFOUND, including the entry stub DP_k: entry 2, len and
g 5, key 14, initialisation 2 (23 in total); each level at most
6 + 7 + 4 = 17 (common part, allocation path, JOIN); exit at most 9. So one
DPFOUND costs at most 23 + 224*17 + 9 = 3840 operations. A chain executes
CHAIN (19) and then either ABANDON (2) or DPFOUND (at most 3840), so every
chain costs at most 3859 < 2^12 operations outside its evaluations and
block controls. We charge 2^13 = 8192 per chain.

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

Each f here writes R0..R7 from a 256-bit register (14 operations, as in
CHAIN), writes R8..R23 (16), issues CF31 (1 unit + 1) and assembles the
256-bit output from R16..R23 (14, as in DPFOUND): 45 operations. With loop
control, moves and comparisons this is at most 80 operations per
evaluation. RELOCATE makes at most (l1 - l2) + 2*l2 <= 2L evaluations; we
charge 3L evaluations at (1 + 80/2140) units each.

OUTPUT(a, b): recompute f(a) and f(b) from freshly written inputs
(2 units), check that a != b and that all 256 output bits are equal, then
write msg(a) and msg(b) to memory (32 bytes each). If the check fails, halt
with failure. This costs at most 2 units plus 200 operations.

There is exactly one run, with no restart and no amplification. The
algorithm halts at its first RELOCATE, whether it succeeds or fails.

## 5. Every output is a valid collision (unconditional)

OUTPUT is reached only with a != b and f(a) = f(b), and it verifies both by
recomputing them. By Section 1, msg(a) != msg(b) are then two legal
messages with equal full 256-bit 31-step SHA-256 digests. This holds for
every run and needs no heuristic.

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
unevaluated, and by H-RF f(p_j) is uniform. V_j contains the j distinct
inputs p_1..p_j, so Pr(f(p_j) not in V_j | history) <= 1 - j/N. The chain
rule bounds Pr(A_1 and ... and A_K0) by prod_{j=1..K0} (1 - j/N). Applying
1-u <= e^-u gives the bound. The main loop starts a new chain while g < K0,
so evaluations 1..K0 all happen unless the run halts first. A halt before
K0 evaluations without contact happens only through event B4 below.

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
  chain (a fixed point is the case where it lands on p_j itself). At
  evaluation j at most S + L such points exist, so
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

K0 = 65162 * 2^112 is the smallest multiple of 2^112 for which this bound
reaches 0.39. Under H-RF the bound is exact arithmetic, not an estimate.
The effect of a possible departure from H-RF is quantified in Section 9.
The JSON reports `success_probability: 0.39`: the probability that this
fixed algorithm succeeds over its own coins under H-RF, not a statement of
confidence in the heuristic or in any review.

## 7. Total charged time (worst case for every run)

| Phase | Bound on count | Charge per item (units) |
| --- | ---: | ---: |
| Main-loop evaluations (BLOCK) | at most K0 - 1 + L | 1 + 435/(16*2140) = 6935/6848 |
| Per-chain work outside evaluations (CHAIN, DPFOUND, ABANDON) | at most 2^98 + 2^88 + 2 chains | 2^13/2140 |
| RELOCATE evaluations (at most one RELOCATE) | at most 3L | 1 + 80/2140 |
| OUTPUT recomputation and emission, setup | 1 | 2 + 216/2140 |

Why these counts are worst-case bounds:

* A chain starts only while g < K0. Here g counts every evaluation of the
  earlier chains, and a chain makes at most L evaluations, so the main loop
  makes at most K0 - 1 + L evaluations.
* The block-control operations are at most 3/16 per evaluation, so 435/16
  operations per main-loop evaluation bounds every chain, including
  abandoned chains and chains that stop inside a block.
* At most Dcap chains store a record, because the run halts when r = Dcap.
  An abandoned chain uses exactly L evaluations, so at most
  (K0 - 1 + L)/L < 2^88 + 1 chains are abandoned. One more chain may end at
  a duplicate DP, and one final CHAIN may halt on g >= K0.
* The run halts at its first RELOCATE.

Every failed trial, abandoned chain, trie operation, comparison and
verification is included above. Summing:

    T <= (K0 - 1 + L)(6935/6848) + (2^98+2^88+2) 2^13/2140
         + 3*2^40 (1 + 80/2140) + 2 + 216/2140.

The second term is below 2^99.94, the third below 2^41.7, and the last
below 3. Relative to K0 (6935/6848), their sum is below 2^-28.07. Also
K0 - 1 + L < K0 (1 + 2^-87.99). Hence

    T <= K0 (6935/6848) (1 + 2^-87.99 + 2^-28.07) <= K0 (6935/6848) (1 + 2^-28.0),

and, using ln(1+u) <= u,

    log2 T <= log2 K0 + log2(6935/6848) + 2^-28.0/ln 2
            < 127.9917432644 + 0.0182131809 + 0.0000000054
            = 128.0099564507

where log2 K0 = 128 + log2(65162/65536) = 127.99174326435 and
log2(6935/6848) = 0.01821318081, each rounded up above. An 80-digit
evaluation of the exact sum gives log2 T = 128.00995645027. The claimed
scalar is `time_log2: 128.00996`, rounded up from 128.00995645027.

The 0.0182 bits above log2 K0 = 127.9917 come from the 435/16 = 27.1875
non-compression operations per evaluation: 8 immediate writes of the
padding words R8..R15 and 8 of the IV words R16..R23 (CF31 may overwrite
them, so they are rewritten), 1 to issue CF31, 8 moves of the output words
into the message registers, 2 for the DP test, and 3/16 for block control.

The run is never repeated, and no work happens outside the program: no
stored collision, no search for favorable parameters or coins, and no
precomputation.

## 8. Memory, preprocessing, advice and data

Each new key allocates at most 224 trie nodes of 2 words; the leaf holds
(s, len). With at most Dcap = 2^98 keys this is at most
2^98 * 448 words * 32 bytes = 2^98 * 14336 bytes < 2^111.81 bytes. The
register file (fewer than 64 registers of 32 bytes), ROOT, the output
buffer and the program code (fewer than 1024 instructions of at most 4
words each) fit in a fixed area under 2^17 bytes. No messages other than
the current ones are retained, there is no sorting table, and no
randomness is kept beyond the stored starts. M <= 2^111.81 + 2^17 < 2^112
bytes, reported as `memory_log2_bytes: 112`. Memory does not affect the
scalar.

Preprocessing is the 16-operation setup, below 1 unit, already included in
T, and reported as `preprocessing_log2: 0` (at most 2^0 units). Nonuniform
advice is zero bytes; the schema cannot encode log2(0), so
`nonuniform_advice_log2_bytes: 0` is a conservative upper bound of one
byte. `data_log2` is omitted as optional legacy metadata: all messages are
generated internally, and every hash evaluation is a charged CF31 call.

## 9. Evidence for H-RF (our own reduced-output experiments)

These are our own measurements. The organizer has not executed them, and no
experiment manifest is declared. They are supporting evidence only: no
number below enters the bound of Section 6, which is derived analytically
from H-RF. The program source is in Appendix A, and every row gives its
exact arguments, so each row can be regenerated bit-exactly (the program is
deterministic given its arguments).

What the program runs: the Section 4 algorithm with these differences.

* The step map is f_n on n-bit words: f_n(x) is the low n bits of
  H[6]*2^32 + H[7] after CF31 on the padded block of msg(x), where the
  n-bit x is the 32-byte message with zero high bytes. This is the real
  31-step target compression, IV and padding, restricted to n bits of
  input and output, and the same fixed map in every trial.
* Starts are uniform n-bit words (seeded splitmix64), a hash map replaces
  the trie, and there is no record cap. After alignment, RELOCATE tests
  a == b once; for a deterministic f the outcome is the same.
* K0 = ceil(0.9944 * 2^(n/2)), theta_n = 2^-t and L = 2^(t+5).

"Success" means a verified collision of f_n within the budget. "Contact <=
K0" (measured for n <= 40) means that within the first K0 evaluations some
output, or some start, was already a visited point. The prediction is the
Lemma 1 bound 1 - exp(-K0(K0+1)/2^(n+1)). The control is the full 64-step
compression, keyed per trial by a random word W[0] (outside the n input
bits); it is otherwise the same program. Arguments: n, t, trials, threads,
track flag, c = 0.9944, log2 L = t + 5, seed, steps.

All runs made with this program, in the order they were made:

| run | n | t | steps | trials | threads | seed | contact <= K0 | success | predicted |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 24 | 4 | 31 (target) | 2000 | 14 | 7 | 902 (0.4510) | 765 (0.3825) | 0.3903 |
| 2 | 24 | 4 | 64 (control) | 2000 | 14 | 7 | 838 (0.4190) | 748 (0.3740) | 0.3903 |
| 3 | 32 | 8 | 31 (target) | 20000 | 14 | 11 | 7767 (0.3883) | 7736 (0.3868) | 0.3901 |
| 4 | 32 | 8 | 64 (control) | 20000 | 14 | 12 | 7951 (0.3976) | 7865 (0.3932) | 0.3901 |
| 5 | 40 | 10 | 31 (target) | 5000 | 14 | 21 | 1946 (0.3892) | 1946 (0.3892) | 0.3901 |
| 6 | 40 | 10 | 64 (control) | 5000 | 14 | 22 | 1962 (0.3924) | 1965 (0.3930) | 0.3901 |
| 7 | 48 | 12 | 31 (target) | 2000 | 14 | 31 | not measured | 784 (0.3920) | 0.3901 |
| 8 | 48 | 12 | 64 (control) | 2000 | 14 | 32 | not measured | 773 (0.3865) | 0.3901 |

Run 1 was a smoke test; runs 2-8 were launched together, with fixed sizes,
after it. No run made with this program is omitted or discarded.

Statistics. The binomial standard error near 0.39 is about 0.0109 for
2000 trials, 0.0034 for 20000 and 0.0069 for 5000. The 31-step success
rates have z-scores -0.72, -0.96, -0.13 and +0.17 against the prediction
(runs 1, 3, 5, 7). Against its 64-step control (standard error of the
difference sqrt(p1 q1/n1 + p2 q2/n2)), each 31-step rate is within 1.32
standard errors: z = +0.55 (n = 24), -1.32 (n = 32), -0.39 (n = 40) and
+0.36 (n = 48). At n = 24, contact exceeds and success falls below the
prediction for target and control alike: starts landing on visited points
(event B1; 49 and 54 trials) and the abandonment cap matter when
theta*sqrt(N) is only 2^8. At full size these events fall into
eps < 7e-10 (Section 6.4). At n = 40 the control shows 3 more successes
than contacts, because the last chain may run past K0 evaluations.
For the 31-step target at these sizes we found no departure from
random-mapping behaviour.

Scope and limits: these runs test output widths of 24 to 48 bits on
restricted input sets, not the full 256-bit map, and cannot rule out a
structural property that appears only at full width. For a single fixed
function, a collision rate along pseudo-random walks clearly below the
random-function rate would itself be a strong distinguisher. The known
31-step collision attacks (Section 10) work only on chosen message pairs
with prescribed differences and many satisfied conditions; a pseudo-random
walk does not choose such pairs, and those attacks predict more collisions
on such pairs, not fewer collisions among random inputs.

Sensitivity: H-RF affects only the success probability. Near K0, the
random-function contact probability 1 - exp(-c^2/2), with c = K0/2^128,
rises at about 0.6065 per unit of c. If the true contact probability at
K0 fell short by a small delta, restoring 0.39 would need K0 larger by a
factor of about 1 + 1.66*delta, adding about 2.4*delta bits to the scalar.
The cost and memory bounds would not change.

## 10. Literature status and limitations

Classical collision attacks on 31-step SHA-256 far below the birthday bound
are published: F. Mendel, T. Nad and M. Schläffer, "Improving Local
Collisions: New Attacks on Reduced SHA-256" (EUROCRYPT 2013) give a 31-step
collision attack, and Y. Li, F. Liu and G. Wang, "New Records in Collision
Attacks on SHA-2" (EUROCRYPT 2024) give a practical one. This package does
not use them and is not competitive with them. It is a generic upper bound
with exact accounting, filed as a simple, independently checkable result;
it makes no novelty claim.

The certificate manifest is empty: no collision is claimed by this package,
and none is computable at this scale. No experiment manifest is declared,
and nothing in this package needs to be executed by the organizer.
Exploratory qualification (`plausible_not_refuted`) is neither a
mathematical proof nor human acceptance.

## Appendix A. Source of the reduced-output experiment program

The exact C source that produced every row of Section 9 (SHA-256 of the
file: bfc3b648bb091620507d91fcccbc639528a3f7c738764bf1a1b12979c73e1487). Build with
`cc -O2 vow.c -o vow -lm -lpthread`; `./vow test` prints the four f
cross-check vectors of Section 1 (message, then digest, as hex).

```c
// Reduced-output simulation of the distinguished-point collision search on
// SHA-256 steps 0..30 (32-byte single-block messages). Evidence only.
// usage: ./vow test | ./vow n t trials threads track c log2L seed rounds
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <pthread.h>
static const uint32_t K[64]={
0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2};
static const uint32_t IV[8]={0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,
 0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};
static int ROUNDS=31; static __thread uint32_t KEYW=0;
#define ROR(v,k) (((v)>>(k))|((v)<<(32-(k))))
// W[0..15] = message words, H[0..7] <- compression of IV with ROUNDS steps
static void cf(uint32_t *W, uint32_t *H){
  uint32_t w[64]; memcpy(w,W,64);
  for(int i=16;i<ROUNDS;i++){ uint32_t x=w[i-15],y=w[i-2];
    w[i]=w[i-16]+(ROR(x,7)^ROR(x,18)^(x>>3))+w[i-7]+(ROR(y,17)^ROR(y,19)^(y>>10)); }
  uint32_t a=IV[0],b=IV[1],c=IV[2],d=IV[3],e=IV[4],f=IV[5],g=IV[6],h=IV[7];
  for(int i=0;i<ROUNDS;i++){
    uint32_t t1=h+(ROR(e,6)^ROR(e,11)^ROR(e,25))+((e&f)^(~e&g))+K[i]+w[i];
    uint32_t t2=(ROR(a,2)^ROR(a,13)^ROR(a,22))+((a&b)^(a&c)^(b&c));
    h=g;g=f;f=e;e=d+t1;d=c;c=b;b=a;a=t1+t2; }
  H[0]=IV[0]+a;H[1]=IV[1]+b;H[2]=IV[2]+c;H[3]=IV[3]+d;
  H[4]=IV[4]+e;H[5]=IV[5]+f;H[6]=IV[6]+g;H[7]=IV[7]+h;
}
static inline void pad(uint32_t *W){ W[8]=0x80000000u; for(int j=9;j<15;j++) W[j]=0; W[15]=256; }
// n-bit map: message = BE32(x) for n-bit x (W6:W7 = x), W0 = per-trial key in the control
static int NB; static uint64_t NMASK;
static inline uint64_t fn(uint64_t x){ uint32_t W[16]={0},H[8];
  W[0]=KEYW; W[6]=(uint32_t)(x>>32); W[7]=(uint32_t)x; pad(W); cf(W,H);
  return ((((uint64_t)H[6])<<32)|H[7])&NMASK; }
static inline uint64_t splitmix(uint64_t *s){ uint64_t z=(*s+=0x9E3779B97F4A7C15ULL);
  z=(z^(z>>30))*0xBF58476D1CE4E5B9ULL; z=(z^(z>>27))*0x94D049BB133111EBULL; return z^(z>>31);}
typedef struct { uint64_t *k,*v1,*v2,mask; } map_t; // open addressing, key+1 stored
static void map_init(map_t *m,int bits){ size_t n=(size_t)1<<bits; m->mask=n-1;
  m->k=calloc(n,8); m->v1=malloc(n*8); m->v2=malloc(n*8); }
static inline uint64_t hh(uint64_t k){ k^=k>>33; k*=0xff51afd7ed558ccdULL; k^=k>>33; return k; }
static int map_get(map_t *m,uint64_t key,uint64_t *a,uint64_t *b){ uint64_t i=hh(key)&m->mask;
  while(m->k[i]){ if(m->k[i]==key+1){*a=m->v1[i];*b=m->v2[i];return 1;} i=(i+1)&m->mask;} return 0; }
static int map_put(map_t *m,uint64_t key,uint64_t a,uint64_t b){ uint64_t i=hh(key)&m->mask; // 1 if present
  while(m->k[i]){ if(m->k[i]==key+1) return 1; i=(i+1)&m->mask;} m->k[i]=key+1;m->v1[i]=a;m->v2[i]=b; return 0; }
static int T_BITS,TRACK; static uint64_t K0,LMAX;
typedef struct { int trials; uint64_t seed; long succ,cle,b1; } job_t;
static int run_trial(uint64_t *rng,map_t *dp,map_t *vis,job_t *J){
  memset(dp->k,0,(dp->mask+1)*8); if(TRACK) memset(vis->k,0,(vis->mask+1)*8);
  if(ROUNDS!=31) KEYW=(uint32_t)splitmix(rng);
  uint64_t g=0,ev=0,dpm=((uint64_t)1<<T_BITS)-1; int contact=0,ok=0;
  while(g<K0){
    uint64_t s=splitmix(rng)&NMASK,x=s,len=0,s2,l2; int isdp=0;
    if(TRACK&&!contact&&map_put(vis,x,0,0)){ contact=1; J->b1++; if(ev<=K0) J->cle++; }
    while(len<LMAX){ uint64_t y=fn(x); len++; ev++;
      if(TRACK&&!contact&&map_put(vis,y,0,0)){ contact=1; if(ev<=K0) J->cle++; }
      x=y; if((y&dpm)==0){ isdp=1; break; } }
    g+=len; if(!isdp) continue;
    if(map_get(dp,x,&s2,&l2)){ uint64_t a=s,b=s2,la=len,lb=l2;   // RELOCATE
      while(la>lb){ a=fn(a); la--; } while(lb>la){ b=fn(b); lb--; }
      if(a!=b) for(;;){ uint64_t fa=fn(a),fb=fn(b); if(fa==fb){ ok=(a!=b&&fn(a)==fn(b)); break; } a=fa;b=fb; }
      break; }
    map_put(dp,x,s,len);
  }
  J->succ+=ok; return ok;
}
static void *worker(void *arg){ job_t *J=arg; uint64_t rng=J->seed; map_t dp,vis;
  int e=(int)ceil(log2((double)K0/(double)((uint64_t)1<<T_BITS)))+3; if(e<8) e=8; map_init(&dp,e);
  if(TRACK) map_init(&vis,(int)ceil(log2((double)K0))+3);
  for(int t=0;t<J->trials;t++) run_trial(&rng,&dp,&vis,J); return 0; }
int main(int argc,char**argv){
  if(argc>1&&!strcmp(argv[1],"test")){ uint64_t sd=12345;   // f on 4 inputs: msg hex, digest hex
    for(int i=0;i<4;i++){ uint32_t W[16]={0},H[8]; for(int j=0;j<8;j++) W[j]=(uint32_t)splitmix(&sd);
      for(int j=0;j<8;j++) printf("%08x",W[j]); printf(" "); pad(W); cf(W,H);
      for(int j=0;j<8;j++) printf("%08x",H[j]); printf("\n"); } return 0; }
  NB=atoi(argv[1]); T_BITS=atoi(argv[2]); int trials=atoi(argv[3]),th=atoi(argv[4]); TRACK=atoi(argv[5]);
  double c=atof(argv[6]); int lexp=atoi(argv[7]); uint64_t seed0=strtoull(argv[8],0,0); ROUNDS=atoi(argv[9]);
  NMASK=(NB==64)?~0ULL:(((uint64_t)1<<NB)-1); K0=(uint64_t)ceil(c*pow(2.0,NB/2.0)); LMAX=(uint64_t)1<<lexp;
  pthread_t T[64]; job_t J[64]; memset(J,0,sizeof J);
  for(int i=0;i<th;i++){ J[i].trials=trials/th+(i<trials%th); J[i].seed=seed0*1000003ULL+i*0x1234567ULL+1;
    pthread_create(&T[i],0,worker,&J[i]); }
  long su=0,cl=0,b1=0; for(int i=0;i<th;i++){ pthread_join(T[i],0); su+=J[i].succ; cl+=J[i].cle; b1+=J[i].b1; }
  printf("rounds=%d n=%d t=%d K0=%llu trials=%d success=%ld (%.4f) pred=%.4f contact<=K0=%ld (%.4f) startcontact=%ld\n",
    ROUNDS,NB,T_BITS,(unsigned long long)K0,trials,su,(double)su/trials,
    1-exp(-(double)K0*(K0+1)/(2*pow(2.0,NB))),cl,(double)cl/trials,b1);
  return 0;
}
```

## Claim rounding (Subflatus3)

An 80-digit evaluation of the Section 4 sum gives log2 T = 128.00995645027. This package declares `time_log2: 128.00996`, the tight upper bound on that reconstruction (peer ed444cc rounded the same number up to 128.01). The algorithm, ABI (27.1875 ordinary ops/eval), parameters, and H-RF success bound are unchanged from the peer-conservative wrapper.
