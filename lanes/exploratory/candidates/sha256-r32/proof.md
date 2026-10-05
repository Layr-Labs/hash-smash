# SHA-256 steps 0-31: distinguished-point generic collision search

Selected lane: exploratory. Target: `sha256-r32-prefix-v1`. Cost model: `collision-frontier-v5`,
with reference operation cost C = 2224 for `sha256-r32`. One 32-step SHA-256 compression costs 1
unit. Every other primitive RAM word operation costs 1/2224 units.

Claim: a classical randomized algorithm with the following properties.

* It outputs two distinct 32-byte messages whose complete 32-step SHA-256 digests (fixed IV,
  standard padding, feed-forward) agree on all 256 bits.
* Its total charged time is at most 2^128.00928 units in every run. The JSON rounds this up to
  `time_log2: 128.01`.
* Its success probability is at least 0.39. This rests on one declared heuristic, H-RF: the step map
  behaves like a random function (Sections 6 and 9).
* Its memory is at most 2^112 bytes. It uses no advice, and its preprocessing is below one unit.

This is the generic birthday attack: the distinguished-point collision search of P. C. van Oorschot
and M. J. Wiener ("Parallel Collision Search with Cryptanalytic Applications", J. Cryptology
12(1):1-28, 1999), run on one processor. The parameters, program, probability bounds and cost
accounting are our own and fully written out here. No cryptanalytic advance is claimed;
`sha256-r32-nominal-v2` names the organizer's nominal reference only.

## 1. Exact target, message map and step function

Let N = 2^256. For a 256-bit word x, let msg(x) = BE32(x): x written as exactly 32 bytes, most
significant byte first, including leading zero bytes. msg is injective, and every msg(x) is a legal
message of bit length 256 < 2^64.

FIPS 180-4 padding appends 0x80, zero bytes to 56 mod 64, and the 64-bit big-endian bit length
256 = 0x100. A 32-byte message m therefore pads to exactly one 64-byte block

    m || 80 || (00 repeated 23 times) || 00 00 00 00 00 00 01 00

whose sixteen big-endian 32-bit words are W[0..7] = the words of x (W[i] = bits 32(7-i)..32(7-i)+31
of x, so W[0] is the most significant), W[8] = 0x80000000, W[9..14] = 0 and W[15] = 0x00000100. The
hash is one compression from the fixed IV (6a09e667, bb67ae85, 3c6ef372, a54ff53a, 510e527f,
9b05688c, 1f83d9ab, 5be0cd19).

COMP32(S, W) is the selected compression. Words have 32 bits; additions are mod 2^32; R_n is right
rotation within 32 bits and >> is logical shift. For t = 16..31:

    sigma0(x) = R_7(x) ^ R_18(x) ^ (x >> 3);   sigma1(x) = R_17(x) ^ R_19(x) ^ (x >> 10)
    W[t] = W[t-16] + sigma0(W[t-15]) + W[t-7] + sigma1(W[t-2])

With Sigma0(x) = R_2(x)^R_13(x)^R_22(x), Sigma1(x) = R_6(x)^R_11(x)^R_25(x), Ch(x,y,z) =
(x&y)^(~x&z) and Maj(x,y,z) = (x&y)^(x&z)^(y&z), set (a,...,h) = S and for t = 0..31 (old values on
the right):

    T1 = h + Sigma1(e) + Ch(e,f,g) + K[t] + W[t];   T2 = Sigma0(a) + Maj(a,b,c)
    (a,b,c,d,e,f,g,h) = (T1+T2, a, b, c, d+T1, e, f, g)

and return S + (a,...,h) componentwise (feed-forward). K[0..31] are the standard FIPS 180-4
constants at their original indices, 428a2f98 ... 14292967 (listed in Appendix A). The digest is the
eight output words H0..H7, big-endian, in order. Define the step map f on 256-bit words by

    f(x) = H0*2^224 + H1*2^192 + ... + H6*2^32 + H7   (H = COMP32(IV, block of msg(x)))

so that BE32(f(x)) is exactly the target digest of msg(x). Whenever x != x' and f(x) = f(x'), msg(x)
and msg(x') are distinct messages with equal full 256-bit target digests: an ordinary collision for
the selected target. Since msg is injective, a chain of f-evaluations is a chain of complete target
hash evaluations.

Sanity check (ours, not needed by the proof): `./vow test` (Appendix A) prints f on four random
32-byte inputs; all four agree with `verifier/hash_functions.py:digest(m, "sha256", 32)`.

## 2. Machine model and charging conventions

The model is a classical probabilistic 256-bit word RAM with a constant number of 256-bit registers
(fewer than 128) and the primitives of `collision-frontier-v5`, each costing 1/2224 units: 256-bit
load and store (including a store of an immediate); addition and subtraction mod 2^256; AND, OR, XOR
and NOT; shift or rotation (the program only shifts by constants); comparison; conditional branch;
RAND, one fresh independent uniform 256-bit word. We also apply these conservative conventions.

* An unconditional jump is charged as one branch. A register-to-register move, and writing an
  immediate constant into a register, are each one operation. A comparison and the branch that uses
  it are two operations.
* The compression operates on dedicated registers: H0..H7 hold the chaining words and W0..W15 the
  block words, each a 32-bit value in the low bits of its register with upper bits zero. The call
  COMP32 replaces H0..H7 by COMP32(H, W), costs 1 unit, and we charge 1 extra operation for issuing
  it. We never also charge its internal operations. It may overwrite W0..W15 (an in-place message
  schedule) and touches no other program register. This matches how C is defined: docs/RESCORING.md
  states that the reference count "counts additions, logical operations, shifts and masks on data
  words, including message expansion and feed-forward", and that "memory traffic and serialization
  are excluded". C is therefore the price of a compression on register-resident words. Because the
  state is never in memory, no load or store occurs around a call. Every write of a call register
  (the IV, the padding words and the message words) is charged below as an operation.
* Every memory access the attack makes (the trie, the records, the output messages) is charged as a
  load or store.
* Instruction fetch is not a primitive of this model and is not charged. The program has fewer than
  1024 instructions, and we count its storage in memory (Section 8).
* The algorithm never reads memory it has not written, so no free zero-fill is assumed.

## 3. Parameters

    distinguished point (DP): an f-output z whose low 32 bits (word H7) are 0
    DP probability     theta = 2^-32 for a uniform output
    maximum chain      L     = 2^40 = 16 * 2^36 evaluations
    evaluation budget  K0    = 65162 * 2^112 = 0.994293212890625 * 2^128
    record cap         Dcap  = 2^98

All are program constants; all counters and addresses fit in one 256-bit word. The setup writes
M32 = 2^32 - 1 into a register.

## 4. Algorithm

Registers: H0..H7 and W0..W15 as in Section 2; g counts the evaluations in completed chains, r
counts stored records, free is the next unused trie address, cnt counts the remaining blocks of the
current chain, s is the current chain's start, t is scratch. ROOT is a two-word trie node in the
fixed memory area, which starts at a nonzero address, so no node address is 0.

Setup: write 0 to ROOT[0] and ROOT[1]; write M32; set free to the first address after the fixed
area; set g = 0 and r = 0. At most 16 operations.

CHAIN (start a new chain). Costs 19 operations.

    if g >= K0: halt with failure                 (compare, branch: 2)
    s = RAND                                      (1)
    W0 = s >> 224                                 (1)
    for i = 1..6: t = s >> (224 - 32i); Wi = t AND M32   (2 each: 12)
    W7 = s AND M32                                (1)
    cnt = 2^36                                    (1)
    jump BLOCK                                    (1)

The start s is a uniform 256-bit word, and W0..W7 now hold the message words of msg(s).

BLOCK (sixteen evaluations of f, unrolled). For k = 1..16 the block contains one copy of the
following straight-line code, copy k falling through to copy k+1:

    H0..H7 = IV words (8 immediate writes)
    W8 = 0x80000000; W9..W14 = 0; W15 = 0x100   (8 immediate writes)
    COMP32(H, W)                                  (1 unit + 1 op)
    W0..W7 = H0..H7                               (8 moves)
    if W7 == 0: goto DP_k                         (compare, branch: 2)

After copy 16:

    cnt = cnt - 1                                 (1)
    if cnt != 0: goto BLOCK                       (compare, branch: 2)
    (fall through) ABANDON: g = g + L; goto CHAIN (2, counted per chain)

    DP_k (k = 1..16): off = k; goto DPFOUND       (2, counted per chain)

After the moves, W0..W7 hold the words of f(x), exactly the message words of msg(f(x)); the next
copy rewrites the IV and padding words, which the call may have overwritten. So every evaluation
hashes exactly the padded block of Section 1 from the fixed IV. Each evaluation has its own DP test,
and a chain with no DP after 16 * 2^36 = L evaluations is abandoned and stores nothing. So a chain
is exactly: iterate f from s, stop at the first DP output, abandon after L evaluations.

Per evaluation this costs 1 unit plus 8 + 8 + 1 + 8 + 2 = 27 operations, and the 3 block-control
operations run once per completed block of 16 evaluations (a chain of length len executes at most
floor(len/16) of them). The main loop therefore costs at most 27 + 3/16 = 435/16 operations per
evaluation, in addition to the unit.

DPFOUND. When copy k of block j finds a DP, cnt = 2^36 - (j - 1) and the chain has made
len = 16(j - 1) + k evaluations x_1 = f(x_0), ..., x_len = z, with x_0 = s; z is its first DP.

    t = 2^36; t = t - cnt; t = t << 4; len = t + off   (4)
    g = g + len                                        (1)
    key = (W0 << 224) OR (W1 << 192) OR ... OR (W6 << 32) OR W7
                                          (7 shifts, 7 ORs: 14)
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

key = z, and z has its low 32 bits equal to 0, so its 224 high bits carry all of z. Each level takes
the current top bit of key (shift by 255) and discards it (left shift by 1 mod 2^256); after 224
levels the descent has used exactly the 224 high bits of z. So two DPs reach the same leaf exactly
when they are equal. This is a binary trie of depth 224 with two-word nodes; 0 means an empty child,
and allocated addresses are never 0. Only completed insertions create nodes and every insertion
descends all 224 levels, so the final level creates a node exactly when the key is new. If the key
is old, the leaf holds the record (s', len') of the earlier chain that ended at the same DP z.

Operation count of DPFOUND, including the entry stub DP_k: entry 2, len and g 5, key 14,
initialisation 2 (23 in total); each level at most 6 common + 7 allocation + 4 at JOIN = 17; exit at
most 2 + 7 = 9. So one DPFOUND costs at most 23 + 224*17 + 9 = 3840 operations. A chain executes
CHAIN (19) and then ABANDON (2) or DPFOUND (at most 3840), so every chain costs at most 3859 < 2^12
operations outside its evaluations and block controls. We charge 2^13 = 8192 per chain.

RELOCATE((s, len), (s', len')). Name the longer chain (s1, l1), the other (s2, l2).

    a = s1; repeat (l1 - l2) times: a = f(a)
    b = s2
    repeat at most l2 times:
        if a == b: halt with failure        (one start lies on the other chain)
        fa = f(a); fb = f(b)
        if fa == fb: goto OUTPUT(a, b)
        a = fa; b = fb
    halt with failure

Each f here writes W0..W7 from a 256-bit register (14 operations, as in CHAIN), writes the IV and
padding words (16), issues COMP32 (1 unit + 1) and assembles the 256-bit output from H0..H7 (14, as
in DPFOUND): 45 operations. With loop control, moves and comparisons this is at most 80 operations
per evaluation. RELOCATE makes at most (l1 - l2) + 2*l2 <= 2L evaluations; we charge 3L evaluations
at (1 + 80/C) units each.

OUTPUT(a, b): recompute f(a) and f(b) from freshly written registers (2 units), check that a != b
and that all 256 output bits are equal, then write the two 32-byte messages msg(a) and msg(b) to
memory. If the check fails, halt with failure. At most 2 units plus 300 operations.

There is exactly one run, with no restart and no amplification. The algorithm halts at its first
RELOCATE, whether that RELOCATE succeeds or fails.

## 5. Every output is a valid collision (unconditional)

OUTPUT is reached only with a != b and f(a) = f(b), verified by recomputation. By Section 1,
msg(a) != msg(b) are then two legal messages with equal full 256-bit 32-step SHA-256 digests. This
holds for every run and needs no heuristic.

## 6. Success probability

### 6.1 The heuristic

H-RF (declared in claim.json): when the algorithm evaluates f at a point x it has not evaluated
before, f(x) is uniform on {0,1}^256 and independent of the algorithm's coins and of all values it
has observed so far.

This is the standard premise of the van Oorschot-Wiener analysis. H-RF is used only in this
section; every resource bound in Sections 4, 7 and 8 holds without it.

### 6.2 Definitions

Number the main-loop (CHAIN/BLOCK) evaluations 1, 2, 3, ..., and let p_j be the input of evaluation
j. Let V_j be the set of all inputs p_1..p_j and all outputs f(p_1)..f(p_{j-1}). Every chain start
is an input. Evaluation j makes contact if f(p_j) is in V_j. Let tau be the index of the first
contact. A start is fresh if it is not in the current V when it is drawn. Before tau every input is
unevaluated: a non-start input is the previous output, which is not in V, and a start is fresh
unless event B1 below occurs.

### 6.3 Lemma 1: contact happens early

With B1 as defined in Section 6.4,

    Pr(no contact among evaluations 1..K0, and B1 does not occur) <= exp(-K0(K0+1)/(2N)).

Proof. Let A_j be the event that evaluation j makes no contact and that any start drawn just before
it is fresh. Condition on any history in which A_1, ..., A_{j-1} hold and the start (if any) is
fresh. Then p_j is unevaluated, and by H-RF f(p_j) is uniform. V_j contains the j distinct inputs
p_1..p_j, so Pr(f(p_j) not in V_j | history) <= 1 - j/N. The chain rule bounds Pr(A_1 and ... and
A_K0) by prod_{j=1..K0} (1 - j/N), and 1-u <= e^-u gives the bound. The main loop starts a new chain
while g < K0, so evaluations 1..K0 all happen unless the run halts first; a halt before K0
evaluations without contact happens only through event B4 below.

### 6.4 Bad events and their probabilities

Let S be the number of chains started before tau and within the first K0 evaluations. Each start
after the first follows either a DP output, which is a fresh uniform value with probability theta of
being a DP, or an abandonment, which needs L evaluations:

    E[S] <= 1 + K0*theta + K0/L = 2^96 (0.994293212890625 (1 + 2^-8) + 2^-96) < 0.99818 * 2^96.

When a start is drawn within the first K0 evaluations, |V| <= 2*K0 < 1.98859 * 2^128.

* B1: some start drawn before tau lies in V. Pr(B1) <= E[S] * 2K0 / N < 0.99818 * 1.98859 * 2^-32 =
  1.98498 * 2^-32 < 4.63e-10.
* B2: the first contact lands on a start, or on an input of the current chain (a fixed point is the
  case p_j itself). At evaluation j at most S + L such points exist, so Pr(B2) <= K0 * (E[S] + L) /
  N < 0.994294 * (0.99818 + 2^-56) * 2^-32 < 2.32e-10.
* B3: some chain started before tau has L/2 consecutive non-DP outputs among its fresh outputs. Each
  is a DP independently with probability theta, so Pr(B3) <= E[S] * (1-theta)^(L/2) <= E[S] *
  exp(-128) < 2^96 * 2^-184.6 < 2^-88. If B3 does not occur, no chain is abandoned before tau, every
  chain completed before tau has length at most L/2, and the current chain has made at most L/2
  evaluations up to contact.
* B4: Dcap = 2^98 records are reached before the first duplicate DP is detected. Before tau, chains
  share no points, so all stored DPs are distinct and are the DPs among at most K0 fresh outputs.
  Their count is dominated by X ~ Binomial(K0, theta) with mean mu = K0*theta < 2^96. The Chernoff
  bound Pr(X >= a) <= e^-mu (e*mu/a)^a with a = 2^98 - 1 >= 4*mu gives Pr(B4) <= (e/4)^a <
  2^-(2^97).

In total eps = Pr(B1 or B2 or B3 or B4) < 7.0e-10. (Exact evaluation at 80 decimal digits gives
4.6216e-10, 2.3108e-10, 2.0e-27 and a negligible B4 term.)

### 6.5 Lemma 2: first contact leads to success

Suppose contact happens at some tau <= K0 and none of B1-B4 occurs. Then the algorithm outputs a
collision.

Proof. Let the current chain have start s_c, and let the contact be its a-th evaluation:
f(x_{a-1}) = v. Without B2, v is neither a start nor a point of the current chain. Without B3, no
earlier chain was abandoned. Hence v is a non-start point c'_b (b >= 1) of an earlier completed
chain c' = (s', l'), and c'_b = f(c'_{b-1}).

Before contact every input is unevaluated, so x_{a-1} != c'_{b-1}: this pair is already a collision
of f. Because f is deterministic, the current chain then follows c'_{b+1}, ..., c'_{l'} = z'. Chain
c' stopped at its first DP, so z' is the first DP the current chain meets, and its length is
l_c = a + l' - b. Without B3, a <= L/2 and l' <= L/2, so l_c < L and the chain is not abandoned. DPFOUND
then finds the key of z' already present. Before contact all chains are disjoint and, without B4,
the run has not halted, so the stored leaf is (s', l').

The current chain's points x_0..x_{a-1} are disjoint from the points of c': x_0 = s_c is a fresh
start (no B1), and each x_i with 1 <= i <= a-1 is an output made before the first contact, so it was
not in V when produced, while every point of c' already was.

RELOCATE aligns the two chains so that each is min(l_c, l') evaluations from z'. If a >= b, it
advances the current chain by a - b steps and the walks are (x_{a-b+k}, c'_k); if a < b, it
advances c' by b - a steps and the walks are (x_k, c'_{b-a+k}). In both cases, before the walks
reach x_a = v = c'_b, one walk is at some x_i with i < a and the other at a point of c'. By disjointness these
differ, so the a == b test does not fire. At the next step both walks reach v. The previous pair
(x_{a-1}, c'_{b-1}) is distinct with equal images, so RELOCATE reaches OUTPUT with a != b and
OUTPUT's check succeeds. This is the first duplicate the run meets: before contact all DPs are
distinct, and no other chain completes between the contact and this DPFOUND.

### 6.6 Result

Combining Lemmas 1 and 2: Pr(success) >= 1 - exp(-K0(K0+1)/(2N)) - eps.

With K0 = 65162 * 2^112: K0^2/(2N) = 65162^2/2^33 = 4246086244/8589934592 = 0.4943094966, and
K0(K0+1)/(2N) exceeds this by less than 2^-128. Also -ln(0.61) = 0.4942963218. The difference is d =
1.3175e-5 > 0, so exp(-K0(K0+1)/(2N)) <= 0.61 * e^-d <= 0.61 * (1 - d + d^2/2) < 0.61 - 8.03e-6.
Therefore

    Pr(success) > 0.39 + 8.03e-6 - 7.0e-10 > 0.39 + 8.0e-6.

(At 80 digits, 1 - exp(-K0(K0+1)/(2N)) - eps = 0.3900080358.)

K0 = 65162 * 2^112 is the smallest multiple of 2^112 for which this bound reaches 0.39 (under H-RF
it is exact arithmetic; K0 = 65300 * 2^112 would give about 0.3913 at log2 T of about 128.0123).
`success_probability: 0.39` is the probability over the algorithm's own coins under H-RF.

## 7. Total charged time (worst case for every run)

| Phase | Bound on count | Charge per item (units) |
| --- | ---: | ---: |
| Main-loop evaluations (BLOCK) | at most K0 - 1 + L | 1 + 435/(16*2224) = 1 + 435/35584 |
| Per-chain work outside evaluations (CHAIN, DPFOUND, ABANDON) | at most 2^98 + 2^88 + 1 chains | 2^13/2224 |
| RELOCATE evaluations (at most one RELOCATE) | at most 3L | 1 + 80/2224 |
| OUTPUT recomputation and emission, setup | 1 | 2 + 316/2224 |

Why these counts are worst-case bounds:

* A chain starts only while g < K0, g counts every evaluation of the earlier chains, and a chain
  makes at most L evaluations: at most K0 - 1 + L main-loop evaluations.
* Block control is at most 3/16 operations per evaluation (Section 4), so 435/16 operations per
  main-loop evaluation bounds every chain, including abandoned chains and chains that stop inside a
  block.
* At most Dcap chains store a record, because the run halts when r = Dcap. An abandoned chain uses
  exactly L evaluations, so fewer than 2^88 + 1 chains are abandoned. The last chain may end at a
  duplicate DP. The run halts at its first RELOCATE.

Every failed trial, abandoned chain, trie operation, comparison and verification is included.
Summing:

    T <= (K0 - 1 + L)(1 + 435/35584) + (2^98+2^88+1) 2^13/2224
         + 3*2^40 (1 + 80/2224) + 2 + 316/2224.

The second term is below 2^99.89, the third below 2^41.7 and the last below 3; relative to K0 (1 +
435/35584) their sum is below 2^-28.12. Also K0 - 1 + L < K0 (1 + 2^-87.99). Hence T <= K0
(36019/35584) (1 + 2^-28), and, using ln(1+u) <= u,

    log2 T <= log2 K0 + log2(36019/35584) + 2^-28/ln 2
            <= (128 - 0.0082567356) + 0.0175294350 + 0.0000000054
             = 128.0092727048,

where log2(65162/65536) = -0.00825673565... and log2(36019/35584) = 0.01752943490... (each rounded
up at the tenth decimal). The claimed scalar is `time_log2: 128.01`, rounded up from 128.00928.

The 0.0175 bits above log2 K0 = 127.9917 are the 27.1875 non-compression operations per
evaluation: 8 IV and 8 padding-word rewrites, 1 call issue, 8 output moves, 2 for the DP test and
3/16 for block control. No work happens outside the program: no stored collision, no search for
favourable parameters or coins, no precomputation.

## 8. Memory, preprocessing, advice and data

Each new key allocates at most 224 trie nodes of 2 words; the leaf node holds (s, len). With at most
Dcap = 2^98 keys this is at most 2^98 * 448 words * 32 bytes = 2^98 * 14336 bytes < 2^111.81 bytes.
The registers (fewer than 128 of 32 bytes), ROOT, the output buffer and the program code (fewer than
1024 instructions of at most 4 words each) fit in a fixed area under 2^17 bytes. No messages other
than the current ones are retained, there is no sorting table, and no randomness is kept beyond the
stored starts. M <= 2^111.81 + 2^17 < 2^112 bytes: `memory_log2_bytes: 112`. Memory does not affect
the scalar.

Preprocessing is the 16-operation setup, below 1 unit and already in T: `preprocessing_log2: 0`.
Advice is zero bytes; the schema cannot encode log2(0), so advice log2 0 is a conservative bound. `data_log2` is omitted as optional legacy metadata; all
messages are generated internally and every hash evaluation is a COMP32 call already charged in T.

## 9. Evidence for H-RF (our own reduced-output experiments)

These are our own measurements. The organizer has not executed them and no experiment manifest is
declared. They are supporting evidence only: no number below enters the bound of Section 6, which is
derived analytically from H-RF. The complete source is in Appendix A and every row gives its exact
arguments; the program is deterministic given its arguments, so each row can be regenerated
bit-exactly.

What the program runs: the Section 4 algorithm with these differences.

* The step map is f_n on n-bit words: f_n(x) is the low n bits of f(x) (words H6, H7), where the
  n-bit x is the 32-byte message with zero high bytes (x in W6, W7). This is the real 32-step target
  compression, IV and padding, restricted to n bits of input and output; it is the same fixed,
  unkeyed map in every trial.
* Starts are uniform n-bit words from a seeded splitmix64 generator; a hash map replaces the trie;
  there is no record cap; after alignment RELOCATE tests a == b once (for a deterministic f the
  outcome is the same).
* K0 = ceil(0.9944 * 2^(n/2)), theta_n = 2^-t and L = 2^(t+5) = 32/theta_n (at full size L =
  2^8/theta, so abandonment is rarer there).

"Success" means a verified collision of f_n within the budget. "Contact <= K0" (measured for n <=
40, where the program keeps the set of visited points) means that within the first K0 main-loop
evaluations some output or some start was already visited; it also counts starts landing on visited
points (event B1 in Section 6). "Start hits" counts runs that ended because one start lay on the
other chain. The prediction is the Lemma 1 bound 1 - exp(-K0(K0+1)/2^(n+1)).

The control replaces the 32 steps by the full 64-step SHA-256 compression and keys the map per trial
with a random word in W0; it is otherwise the same program. Arguments: n, t, trials, threads,
track-visited flag, c = 0.9944, log2 L = t + 5, seed, rounds.

All runs made with this program, in order (14 threads each):

| run | n | t | rounds | trials | seed | contact <= K0 | success | start hits | predicted |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 24 | 4 | 32 (target) | 2000 | 7 | 871 (0.4355) | 755 (0.3775) | 101 | 0.3903 |
| 2 | 24 | 4 | 64 (control) | 2000 | 8 | 808 (0.4040) | 739 (0.3695) | 71 | 0.3903 |
| 3 | 32 | 8 | 32 (target) | 20000 | 11 | 7998 (0.3999) | 7899 (0.3950) | 54 | 0.3901 |
| 4 | 32 | 8 | 64 (control) | 20000 | 12 | 7951 (0.3976) | 7865 (0.3932) | 64 | 0.3901 |
| 5 | 40 | 10 | 32 (target) | 5000 | 21 | 2019 (0.4038) | 1999 (0.3998) | 6 | 0.3901 |
| 6 | 40 | 10 | 64 (control) | 5000 | 22 | 1962 (0.3924) | 1965 (0.3930) | 1 | 0.3901 |
| 7 | 48 | 12 | 32 (target) | 2000 | 31 | not measured | 778 (0.3890) | 0 | 0.3901 |
| 8 | 48 | 12 | 64 (control) | 2000 | 32 | not measured | 773 (0.3865) | 0 | 0.3901 |

For example, run 3 is `./vow 32 8 20000 14 1 0.9944 13 11 32`; controls end in `64`. A second
execution of runs 1-3 reproduced them exactly.

Stopping and selection: all eight runs were fixed in one script (sizes and seeds as shown) before
any result was seen (run 1 was also executed once alone first, with identical output); none is
omitted or discarded.

Statistics. The binomial standard error of a proportion near 0.39 is about 0.0109 for 2000 trials,
0.0034 for 20000 and 0.0069 for 5000. Against the prediction, the 32-step success rates have
z-scores -1.17 (run 1), +1.41 (run 3), +1.41 (run 5) and -0.10 (run 7); the controls have -1.91,
+0.92, +0.42 and -0.33. Against its 64-step control (standard error of the difference sqrt(p1 q1/n1
+ p2 q2/n2)), each target rate is within 0.70 standard errors: z = +0.52 (n = 24), +0.35 (n = 32),
+0.70 (n = 40), +0.16 (n = 48). We found no departure from random-mapping behaviour at these sizes.
At n = 24, success falls below contact for target and control alike: starts landing on earlier
chains (event B1; 101 and 71 trials) and the abandonment cap are non-negligible when theta*sqrt(N)
is only 2^8 to 2^12. At full size these events lie inside eps < 7e-10 (Section 6.4).

Scope and limits: the tests cover output widths of 24 to 48 bits on restricted n-bit input sets, not
256 bits, and cannot rule out a structural property that appears only at full width. We know of no
published property of 32-step SHA-256 that predicts fewer collisions for f than for a random
function; for a single fixed function, a collision rate along pseudo-random walks clearly below the
random-function rate would itself be a strong distinguisher.

Sensitivity: H-RF affects only the success probability. Near K0 the random-function contact
probability 1 - exp(-c^2/2), c = K0/2^128, rises at rate c*exp(-c^2/2), about 0.6065 per unit of c.
If the true contact probability at K0 fell short by a small delta, restoring 0.39 would need K0
larger by a factor of about 1 + 1.66*delta, adding about 2.4*delta bits to the scalar. The cost and
memory bounds would not change.

## 10. Literature status and limitations

Better-than-generic attacks on step-reduced SHA-256 are published (e.g. Li, Liu, Wang, Dong and
Sun, "The First Practical Collision for 31-Step SHA-256", ASIACRYPT 2024), and we file a separate
differential candidate for this target. This package uses none of that work and makes no novelty
claim. The certificate manifest is empty (no collision is computable at this scale), and no
experiment manifest is declared.

## Appendix A. Source of the reduced-output experiment program

The exact C source that produced every row of the Section 9 table (file SHA-256
59804b283facc0dedc28a7e5c337a79a040e8afc298b126b9c3025f087525dd8). Build:
`cc -O2 vow.c -o vow -lm -lpthread`; `./vow test` prints the Section 1 vectors (message, digest).

```c
// Reduced-output simulation of the distinguished-point collision search
// on the 32-step SHA-256 prefix target (single-block 32-byte messages).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <pthread.h>

static const uint32_t K[64] = {
 0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
 0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
 0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
 0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
 0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
 0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
 0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
 0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2};
static const uint32_t IV[8] = {0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,
 0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};
static int ROUNDS=32; static __thread uint32_t KEYWORD=0;
#define ROR(x,n) (((x)>>(n))|((x)<<(32-(n))))

// one compression from the fixed IV on the padded block of the 32-byte
// message m = BE(in[0]) || ... || BE(in[7]); out = digest words H0..H7
static void comp(const uint32_t in[8], uint32_t out[8]){
  uint32_t W[64]; for(int i=0;i<8;i++) W[i]=in[i];
  W[8]=0x80000000u; for(int i=9;i<15;i++) W[i]=0; W[15]=256;
  for(int t=16;t<ROUNDS;t++){ uint32_t a=W[t-15], b=W[t-2];
    W[t]=W[t-16]+(ROR(a,7)^ROR(a,18)^(a>>3))+W[t-7]+(ROR(b,17)^ROR(b,19)^(b>>10)); }
  uint32_t a=IV[0],b=IV[1],c=IV[2],d=IV[3],e=IV[4],f=IV[5],g=IV[6],h=IV[7];
  for(int t=0;t<ROUNDS;t++){
    uint32_t T1=h+(ROR(e,6)^ROR(e,11)^ROR(e,25))+((e&f)^(~e&g))+K[t]+W[t];
    uint32_t T2=(ROR(a,2)^ROR(a,13)^ROR(a,22))+((a&b)^(a&c)^(b&c));
    h=g; g=f; f=e; e=d+T1; d=c; c=b; b=a; a=T1+T2; }
  out[0]=IV[0]+a; out[1]=IV[1]+b; out[2]=IV[2]+c; out[3]=IV[3]+d;
  out[4]=IV[4]+e; out[5]=IV[5]+f; out[6]=IV[6]+g; out[7]=IV[7]+h;
}
// truncated n-bit map on n-bit inputs (x in the low message words W6,W7;
// the control keys W0 per trial)
static int NB; static uint64_t NMASK;
static inline uint64_t fn(uint64_t x){
  uint32_t in[8]={KEYWORD,0,0,0,0,0,(uint32_t)(x>>32),(uint32_t)x}, out[8];
  comp(in,out); return (((uint64_t)out[6]<<32)|out[7])&NMASK;
}

static inline uint64_t splitmix(uint64_t *s){ uint64_t z=(*s+=0x9E3779B97F4A7C15ULL);
  z=(z^(z>>30))*0xBF58476D1CE4E5B9ULL; z=(z^(z>>27))*0x94D049BB133111EBULL; return z^(z>>31);}

// open-addressing hash map keyed by 64-bit value (value+1 stored to reserve 0)
typedef struct { uint64_t *k, *v1, *v2, mask; } map_t;
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

static int T_BITS, TRACK; static uint64_t K0, LMAX;
typedef struct { int trials; uint64_t seed; long succ, contact, rh; } job_t;

static void run_trial(uint64_t *rng, map_t *dp, map_t *vis, job_t *J){
  map_clear(dp); if(TRACK) map_clear(vis);
  if(ROUNDS!=32) KEYWORD=(uint32_t)splitmix(rng);
  uint64_t g=0, dpmask=((uint64_t)1<<T_BITS)-1; int contact=0;
  while(g<K0){
    uint64_t s=splitmix(rng)&NMASK, x=s, len=0; int isdp=0;
    if(TRACK && !contact && g<K0 && set_add(vis,x)) contact=1;
    while(len<LMAX){
      uint64_t y=fn(x); len++;
      if(TRACK && !contact && g+len<=K0 && set_add(vis,y)) contact=1;
      x=y; if((y&dpmask)==0){ isdp=1; break; }
    }
    g+=len;
    if(!isdp) continue;
    uint64_t s2,l2;
    if(map_get(dp,x,&s2,&l2)){              // relocate
      uint64_t a=s, b=s2, la=len, lb=l2;
      while(la>lb){ a=fn(a); la--; }
      while(lb>la){ b=fn(b); lb--; }
      if(a==b){ J->rh++; break; }
      for(;;){ uint64_t fa=fn(a), fb=fn(b);
        if(fa==fb){ if(a!=b && fn(a)==fn(b)) J->succ++; break; }
        a=fa; b=fb; }
      break;
    }
    map_put(dp,x,s,len);
  }
  J->contact+=contact;
}

static void *worker(void *arg){ job_t *J=arg; uint64_t rng=J->seed; map_t dp, vis;
  int e=(int)ceil(log2((double)K0/(double)((uint64_t)1<<T_BITS)))+3; if(e<8) e=8;
  map_init(&dp,e); if(TRACK) map_init(&vis,(int)ceil(log2((double)K0))+3);
  for(int t=0;t<J->trials;t++) run_trial(&rng,&dp,TRACK?&vis:&dp,J); return 0; }

int main(int argc,char**argv){
  if(argc>1 && !strcmp(argv[1],"test")){   // f on fixed inputs: message, digest (hex)
    uint64_t seed=12345; for(int i=0;i<4;i++){ uint32_t in[8],out[8];
      for(int j=0;j<8;j++) in[j]=(uint32_t)splitmix(&seed);
      comp(in,out); for(int j=0;j<8;j++) printf("%08x",in[j]); printf(" ");
      for(int j=0;j<8;j++) printf("%08x",out[j]); printf("\n"); }
    return 0; }
  if(argc<10){ fprintf(stderr,"usage: vow n t trials threads track c log2L seed rounds\n"); return 1; }
  NB=atoi(argv[1]); T_BITS=atoi(argv[2]); int trials=atoi(argv[3]), threads=atoi(argv[4]);
  TRACK=atoi(argv[5]); double c=atof(argv[6]); int lexp=atoi(argv[7]);
  uint64_t seed0=strtoull(argv[8],0,0); ROUNDS=atoi(argv[9]);
  NMASK=(NB==64)?~0ULL:(((uint64_t)1<<NB)-1);
  K0=(uint64_t)ceil(c*pow(2.0,NB/2.0)); LMAX=(uint64_t)1<<lexp;
  pthread_t th[64]; job_t J[64]; memset(J,0,sizeof J);
  for(int i=0;i<threads;i++){ J[i].trials=trials/threads+(i<trials%threads);
    J[i].seed=seed0*1000003ULL+i*0x1234567ULL+1; pthread_create(&th[i],0,worker,&J[i]); }
  long succ=0,con=0,rh=0;
  for(int i=0;i<threads;i++){ pthread_join(th[i],0); succ+=J[i].succ; con+=J[i].contact; rh+=J[i].rh; }
  double pred=1-exp(-(double)K0*(K0+1)/(2*pow(2.0,NB)));
  printf("rounds=%d n=%d t=%d L=2^%d K0=%llu trials=%d success=%ld (%.4f) pred=%.4f contact<=K0=%ld (%.4f) start_hits=%ld\n",
    ROUNDS,NB,T_BITS,lexp,(unsigned long long)K0,trials,succ,(double)succ/trials,pred,con,(double)con/trials,rh);
  return 0;
}
```
