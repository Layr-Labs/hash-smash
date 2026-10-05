# SHA3-256 prefix rounds 0-4: distinguished-point generic collision search
# (word-native 2x envelope; parent 0cd01934 @ 128.13)

Selected lane: exploratory. Target: `sha3-256-r5-prefix-v1`.
Cost model: `collision-frontier-v5`, reference cost C = 1355 for `sha3-256-r5`.
**One five-round sponge permutation costs exactly 1 unit.** Every other
primitive RAM word operation costs 1/1355 units. Fixed-pad absorption,
zero-IV state install, digest extraction and L0 deposit are charged as
ordinary ops — they are **not** folded into the permutation unit (repair of
lane_cost/F-COST-ABI-1 from refuted ticket c9e2bf8f).

Claim:

* Two distinct 32-byte messages with equal five-round SHA3-256 digests.
* Total charged time at most 2^128.03381249 units every run; JSON claims
  time_log2 128.06 (at least 0.02 bits declared headroom).
* Success probability at least 0.39 under single heuristic H-RF (Sections 6 and 9).
* Memory at most 2^112 bytes (reported). Preprocessing below 1 unit.

Search structure matches the prior DP package; only the cost ABI changed.
H-RF wording is unchanged (previously judged PLAUSIBLE with material
reduced-width evidence gaps disclosed in Section 9). GLL differential work
is parked after refute / not_evaluable tickets.

## 1. Exact target, message map and step function

Let N = 2^256. For a 256-bit word x, let msg(x) = LE32(x): x written as
exactly 32 little-endian bytes, including leading zero bytes. msg is
injective, and every msg(x) is a byte string of bit length 256 < 2^64, so it
lies in the profile's message domain.

The target sponge has a 1600-bit state, rate 1088 bits (136 bytes), capacity
512 bits, an all-zero initial state and a 256-bit output. Padding is the
SHA3 domain suffix 01 followed by pad10*1 (delimited suffix byte 0x06).
A 32-byte message m pads to exactly one 136-byte block:

    m || 06 || (00 repeated 102 times) || 80

There is one absorption and one permutation call. No squeeze permutation
follows, because 32 output bytes are fewer than the 136-byte rate. There is
no feed-forward. With lanes A[0..24] (index x+5y, 64-bit little-endian),
XORing the padded block into the zero state gives:

    A[0..3] = the four 64-bit lanes of x  (A[j] = bits 64j..64j+63 of x)
    A[4]    = 0x0000000000000006           (byte 32 of the block)
    A[16]   = 0x8000000000000000           (byte 135 of the block)
    all other lanes, A[5..15] and A[17..24], equal 0

PERM5 applies Keccak-f[1600] rounds 0 through 4 (the profile's prefix
convention, not Keccak-p's last-round convention). Each round, with
subscripts mod 5, 64-bit lane arithmetic, and each stage reading the
previous stage's result:

    C[x] = A[x,0] ^ A[x,1] ^ A[x,2] ^ A[x,3] ^ A[x,4]
    D[x] = C[x-1] ^ rot64(C[x+1], 1)
    B[y, 2x+3y] = rot64(A[x,y] ^ D[x], rho[x+5y])
    A[x,y] = B[x,y] ^ ((NOT B[x+1,y]) AND B[x+2,y])
    A[0,0] = A[0,0] ^ RC[round]

rot64(v, k) rotates left by k (bit i to bit i+k mod 64). The rho offsets,
in x+5y order, are 0,1,62,28,27, 36,44,6,55,20, 3,10,43,25,39,
41,45,15,21,8, 18,2,61,56,14. The five round constants are
0x0000000000000001, 0x0000000000008082, 0x800000000000808A,
0x8000000080008000 and 0x000000000000808B.

The digest is the first 32 squeeze bytes, i.e. lanes A[0..3] in
little-endian order. Define the step map

    f(x) = A[0] + 2^64 A[1] + 2^128 A[2] + 2^192 A[3]   (after PERM5)

so LE32(f(x)) is exactly the target digest of msg(x). Whenever x != x' and
f(x) = f(x'), msg(x) and msg(x') are distinct legal messages with equal full
256-bit digests: an ordinary collision for the selected target. Because msg
is injective, a chain of f-evaluations is a chain of complete target hash
evaluations, each one PERM5 call.

Sanity check (ours; the proof does not depend on it): the Appendix A
program in `test` mode prints f on four pseudo-random inputs; all four
agree with the repository reference `verifier/keccak.py:sha3_256(m, rounds=5)`.

## 2. Machine model and charging conventions

A classical probabilistic 256-bit word RAM with fewer than 64 registers and
the primitives of collision-frontier-v5, each costing 1/1355 units: load,
store (including a store of an immediate), addition and subtraction mod
2^256, AND/OR/XOR/NOT, shift or rotation (only by constants here),
comparison, conditional branch, and RAND (one fresh uniform 256-bit word).

Conservative conventions:

* Comparison + conditional branch = 2 operations. Unconditional jump = 1
  branch. Register move or immediate write = 1 operation.
* Unit boundary (F-COST-ABI-1 fix). The only 1-unit operation is PERM5(A),
  applying Keccak-f[1600] rounds 0..4 to an already-installed 25-lane state
  array A and writing the new state back. It does not include padding,
  IV/zero install, message absorb, digest extraction, or L0 deposit.
* All attack memory traffic (state lanes, trie, records, output) is charged.
* No free zero-fill: each evaluation re-zeros capacity and re-applies pad.

### 2.1 Per-evaluation inventory and 2x envelope

The machine is a **256-bit word RAM** (Section 2). The 1600-bit Keccak state
occupies **7 words** (covering all 25 lanes). Parent ticket `0cd01934`
charged a lane-level inventory (25 zero-stores + 12-op unpack/pack) that
over-counts relative to this word ABI; that was deliberate fat, not required
by the model. This package uses a word-native inventory (still outside the
PERM5 unit — F-COST-ABI-1 discipline unchanged).

Honest inventory when evaluation begins with message word P0:

| Step | Honest ops |
| --- | ---: |
| Zero 7 state words (covers 25 lanes) | 7 |
| Store P0 as rate word 0 (lanes 0..3) | 1 |
| Pad A[4]=6 and A[16]=2^63 (load/modify/store ×2) | 6 |
| Load digest word 0 → P0 | 1 |
| L0 ← P0 masked to 64 bits | 1 |
| DP test L0 < 2^32 (compare+branch) | 2 |
| Per-eval bookkeeping | 2 |
| Body subtotal | 20 |
| Block control amortized /64 | 3/64 |

Charged envelope: **2 × 20 = 40** body ops + **6/64** control =
**40.09375** ordinary ops per evaluation.

    units/eval = 1 + 40.09375/1355.

Still a full 2× inventory multiplier (same discipline as `0cd01934`, applied
to the corrected word inventory). No pad/IV/L0 fusion into PERM5.

## 3. Parameters

    distinguished point (DP): an f-output z whose bits 32..63 are 0
    (equivalently L0 < 2^32 after digest extract, with L0 = lane A[0])
    DP probability     theta = 2^-32 for a uniform lane A[0]
    maximum chain      L     = 2^40 = 64 * 2^34 evaluations
    evaluation budget  K0    = 65162 * 2^112 = 0.994293212890625 * 2^128
    record cap         Dcap  = 2^98

All are program constants; all counters and addresses fit in one word.
Padding constants A[4]=6, A[16]=2^63 and zero capacity are installed
explicitly each evaluation (Section 2.1), not inside PERM5.

## 4. Algorithm

Registers: P0 (message/digest word), L0 (lane A[0] after extract), g, r,
free, cnt, s, t, and RAM state A[0..24]. ROOT is a two-word trie node in a
fixed memory area at a nonzero address.

Setup: ROOT[0]=ROOT[1]=0; free = first address after fixed area; g=r=0
(at most 16 operations).

CHAIN (start a new chain). 6 operations.

    if g >= K0: halt with failure                 (compare, branch: 2)
    s = RAND                                      (1)
    P0 = s                                        (1)
    cnt = 2^34                                    (1)
    jump BLOCK                                    (1)

BLOCK (64 evaluations of f, unrolled). For k = 1..64:

    for w in 0..6: S[w] = 0                       (in 40-op envelope)
    S[0] = P0                                     (rate lanes 0..3; in envelope)
    insert A[4]=6 and A[16]=2^63 into S           (in envelope)
    PERM5(S)                                      (1 unit; permutation ONLY)
    P0 = S[0]; L0 = P0 & (2^64-1)                 (in envelope)
    if L0 < 2^32: goto DP_k                       (in envelope)

After copy 64:

    cnt = cnt - 1                                 (1; in amortized envelope)
    if cnt != 0: goto BLOCK                       (2; in amortized envelope)
    ABANDON: g = g + L; goto CHAIN                (2, per chain)
    DP_k: off = k; goto DPFOUND                   (2, per chain)

Per evaluation: 1 unit + 40.09375 ordinary ops (Section 2.1). The next
message is the previous digest left in P0. Chains stop at the first DP or
after L evaluations (abandon, store nothing).

DPFOUND (unchanged trie logic vs prior DP package). When copy k of block j
finds a DP, len = 64(j-1)+k:

    t = 2^34; t = t - cnt; t = t << 6; len = t + off   (4)
    g = g + len                                        (1)
    t = P0 >> 64                                       (1)
    key = L0 OR (t << 32)                              (2)
    key = key << 32                                    (1)
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

Trie accounting unchanged: one DPFOUND at most 3830 ops; chain outside evals
at most 3836 < 2^12. We charge 2^13 = 8192 ordinary ops per chain (DPFOUND ≤ 3836; ≥2× margin) for CHAIN+DPFOUND+ABANDON.

RELOCATE((s, len), (s', len')). Let (s1, l1) be the longer chain, (s2, l2)
the other.

    a = s1; repeat (l1 - l2) times: a = f(a)
    b = s2
    repeat at most l2 times:
        if a == b: halt with failure
        fa = f(a); fb = f(b)
        if fa == fb: goto OUTPUT(a, b)
        a = fa; b = fb
    halt with failure

Each f uses the same Section 2.1 absorb+PERM5+extract envelope. Charge at
most 3L evaluations at (1 + 40.09375/1355) units each.

OUTPUT(a, b): recompute f(a) and f(b) (2x units/eval), check a != b and
equal digests, write messages; else fail. Charge 2 units + 400 ordinary ops (setup/output padded).

Exactly one run; halt at first RELOCATE.

## 5. Every output is a valid collision (unconditional)

OUTPUT is reached only with a != b and f(a) = f(b), both verified by
recomputation. By Section 1, msg(a) != msg(b) are legal messages with equal
full 256-bit five-round SHA3-256 digests. No heuristic is needed.

## 6. Success probability

### 6.1 The heuristic

H-RF (declared in claim.json): when the algorithm evaluates f at a point x
it has not evaluated before, f(x) is uniform on {0,1}^256 and independent
of the algorithm's coins and of all values observed so far. This is the
standard random-mapping premise of the van Oorschot-Wiener analysis. It is
used only in this section; Sections 4, 5, 7 and 8 hold without it.

### 6.2 Definitions

Number the main-loop evaluations 1, 2, 3, ..., and let p_j be the input of
evaluation j. Let V_j be the set of inputs p_1..p_j and outputs
f(p_1)..f(p_{j-1}); every chain start is an input. Evaluation j makes
contact if f(p_j) is in V_j; tau is the index of the first contact. A start
is fresh if it is not in the current V when drawn. Before tau every input is
unevaluated: a non-start input is the previous output, which is not in V,
and a start is fresh unless event B1 occurs.

### 6.3 Lemma 1: contact happens early

    Pr(no contact among evaluations 1..K0, and B1 does not occur)
        <= exp(-K0(K0+1)/(2N)).

Proof. Let A_j be the event that evaluation j makes no contact and any
start drawn just before it is fresh. Given any history in which
A_1..A_{j-1} hold and the start (if any) is fresh, p_j is unevaluated, so
by H-RF f(p_j) is uniform; V_j contains the j distinct inputs p_1..p_j, so
Pr(f(p_j) not in V_j | history) <= 1 - j/N. The chain rule bounds
Pr(A_1 and ... and A_K0) by prod_{j=1..K0} (1 - j/N) <= exp(-K0(K0+1)/(2N)).
Chains start while g < K0, so evaluations 1..K0 all happen unless the run
halts earlier; without contact that requires event B4.

### 6.4 Bad events

Let S be the number of chains started before tau within the first K0
evaluations. Each start after the first follows a DP output (a fresh
uniform value, DP with probability theta) or an abandonment (L
evaluations), so

    E[S] <= 1 + K0*theta + K0/L = 2^96 (0.994293212890625 (1 + 2^-8) + 2^-96)
         < 0.99818 * 2^96.

While a start is drawn within the first K0 evaluations,
|V| <= 2*K0 < 1.98859 * 2^128.

* B1: some start drawn before tau lies in V.
  Pr(B1) <= E[S] * 2K0/N < 0.99818 * 1.98859 * 2^-32 < 4.63e-10.
* B2: the first contact lands on a start or on an input of the current
  chain (a fixed point is the case p_j itself). At most S + L such points
  exist, so Pr(B2) <= K0 (E[S] + L)/N < 0.994294 (0.99818 + 2^-56) 2^-32
  < 2.32e-10.
* B3: some chain started before tau has L/2 consecutive non-DP fresh
  outputs. Pr(B3) <= E[S] (1-theta)^(L/2) <= E[S] exp(-128) < 2^-88.
  Without B3 no chain is abandoned before tau, every chain completed before
  tau has length at most L/2, and the current chain has made at most L/2
  evaluations up to contact.
* B4: Dcap records are reached before the first duplicate DP. Before tau
  chains share no points, so the stored DPs are distinct DPs among at most
  K0 fresh outputs, dominated by X ~ Binomial(K0, theta) with mean
  mu = K0*theta < 2^96. Chernoff, Pr(X >= a) <= e^-mu (e*mu/a)^a with
  a = 2^98 - 1 >= 4*mu, gives Pr(B4) <= (e/4)^a < 2^-(2^97).

eps = Pr(B1 or B2 or B3 or B4) < 4.63e-10 + 2.32e-10 + 2^-88 + 2^-(2^97)
< 7.0e-10.

### 6.5 Lemma 2: first contact leads to success

If contact happens at tau <= K0 and none of B1-B4 occurs, the algorithm
outputs a collision.

Proof. Let the contact be the a-th evaluation of the current chain:
f(x_{a-1}) = v. Without B2, v is neither a start nor a point of the
current chain; without B3 no earlier chain was abandoned. So v is a
non-start point c'_b (b >= 1) of an earlier completed chain c' = (s', l'),
with c'_b = f(c'_{b-1}). Before contact every input is unevaluated, so
x_{a-1} != c'_{b-1}: this pair already collides. Since f is deterministic,
the current chain then follows c'_{b+1}, ..., c'_{l'} = z', the first DP
it meets, with length l_c = a + l' - b < L (a, l' <= L/2 without B3), so
it is not abandoned. DPFOUND finds z' already present; before contact the
chains are disjoint and, without B4, the run has not halted, so the leaf
holds (s', l').

The points x_0..x_{a-1} are disjoint from c': x_0 is a fresh start (no B1),
and each x_i (1 <= i <= a-1) is an output made before contact, so it was not
in V when produced, while every point of c' already was. RELOCATE aligns
both walks at distance min(l_c, l') from z'. Until they reach
x_a = v = c'_b, one walk is at some x_i with i < a and the other at a point
of c', so by disjointness a == b never fires. At the next step both reach
v from the distinct pair (x_{a-1}, c'_{b-1}), so RELOCATE reaches OUTPUT
with a != b and the check succeeds. This is the first duplicate DP of the
run, since all DPs before contact are distinct and no other chain
completes between the contact and this DPFOUND.

### 6.6 Result

    Pr(success) >= 1 - exp(-K0(K0+1)/(2N)) - eps.

With K0 = 65162 * 2^112: K0^2/(2N) = 65162^2/2^33 = 4246086244/8589934592
= 0.4943094966, and K0(K0+1)/(2N) exceeds this by less than 2^-128.
-ln(0.61) = 0.4942963218, so d = 1.3175e-5 > 0 and
exp(-K0(K0+1)/(2N)) <= 0.61 e^-d <= 0.61 (1 - d + d^2/2) < 0.61 - 8.03e-6.
Therefore

    Pr(success) > 0.39 + 8.03e-6 - 7.0e-10 > 0.39 + 8.0e-6.

(At 80 digits the bound is 0.3900080358.) K0 = 65162 * 2^112 is the
smallest multiple of 2^112 reaching 0.39. Under H-RF this is exact
arithmetic, so the small margin does not affect validity; Section 9 gives
the sensitivity to a departure from H-RF. `success_probability: 0.39` is
the probability over the algorithm's own coins under H-RF, not a statement
of confidence in the heuristic.

## 7. Total charged time (worst case for every run)

| Phase | Bound on count | Charge per item (units) |
| --- | ---: | ---: |
| Main-loop evaluations (BLOCK) | at most K0 - 1 + L | 1 + 40.09375/1355 |
| Per-chain (CHAIN, DPFOUND, ABANDON) | at most 2^98 + 2^88 + 1 | 2^13/1355 |
| RELOCATE evaluations | at most 3L | 1 + 40.09375/1355 |
| OUTPUT and setup | 1 | 2 + 400/1355 |

Worst-case counts unchanged from the DP spine (chains while g < K0; ≤ L
evals/chain; ≤ Dcap stores; ≤ (K0−1+L)/L abandons; one RELOCATE). Summing,

    T ≤ (K0−1+L)(1+40.09375/1355) + (2^98+2^88+1)·2^13/1355
        + 3·2^40·(1+40.09375/1355) + 2 + 400/1355.

Exact evaluation: **log2 T = 128.0338124948**. Claimed
`time_log2: 128.06` (headroom 0.0262 bits ≥ 0.02).

Decomposition: log2 K0 = 127.9917432643; log2(1+40.09375/1355) =
0.0420692225. Versus parent `0cd01934` (lane inventory ×2 → 114.09375
ops/eval, claim 128.13), the win is the **word-native state ABI** matching
the 256-bit RAM model — not a thinner multiplier and not a fused unit.

## 8. Memory, preprocessing, advice and data

Each new key allocates at most 224 two-word trie nodes (the leaf holds
(s, len)). With at most Dcap = 2^98 keys this is at most
2^98 * 448 * 32 = 2^98 * 14336 bytes < 2^111.81 bytes. Registers (fewer
than 64 words), ROOT, the output buffer and the program (fewer than 1024
instructions of at most 4 words) fit in a fixed area under 2^17 bytes. No
other messages are retained and there is no sorting table. So
M <= 2^111.81 + 2^17 < 2^112 bytes: `memory_log2_bytes: 112`.

Preprocessing is the 16-operation setup, below 1 unit and already in T
(`preprocessing_log2: 0`). Nonuniform advice is zero bytes; the schema
cannot encode log2(0), so `nonuniform_advice_log2_bytes: 0` is a
conservative bound of one byte. `data_log2` is omitted (optional legacy
metadata); all messages are generated internally and every hash evaluation
is a PERM5 evaluation charged in T under Section 2.1.

## 9. Evidence for H-RF (our own reduced-output experiments)

These are our own measurements, not organizer-executed (no experiment
manifest is declared). No number below enters the Section 6 bound. The
full source is Appendix A; each row gives its exact arguments and is
deterministic given them.

The program runs the Section 4 algorithm with these differences: the step
map is f_n(x) = low n bits of lane A[0] after PERM5 applied to the padded
block of msg(x), for n-bit x (zero high bytes), i.e. the real five-round
target map restricted to n input and output bits, fixed across trials;
starts are uniform n-bit words from a seeded splitmix64 generator; a hash
map replaces the trie and there is no Dcap; RELOCATE tests a == b once
after alignment (same outcome for a deterministic f); and K0 =
ceil(0.9944 * 2^(n/2)), theta_n = 2^-t, L = 2^(t+5). Success means a
verified collision of f_n within the budget. The predicted value is the
Lemma 1 bound 1 - exp(-K0(K0+1)/2^(n+1)). The control replaces PERM5 by the
full 24-round Keccak-f[1600] and keys the map per trial with a random
lane A[5]; it is otherwise identical.

Arguments are `n t trials threads seed rounds`; all rows used 10 threads.
The full run list was fixed before any run, and these are all runs made
with this program:

| run | n | t | rounds | trials | seed | success | predicted | start on chain |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 24 | 4 | 5 (target) | 2000 | 7 | 745 (0.3725) | 0.3903 | 99 |
| 2 | 24 | 4 | 24 (control) | 2000 | 8 | 759 (0.3795) | 0.3903 | 87 |
| 3 | 32 | 8 | 5 (target) | 20000 | 11 | 7809 (0.3905) | 0.3901 | 54 |
| 4 | 32 | 8 | 24 (control) | 20000 | 12 | 7858 (0.3929) | 0.3901 | 68 |
| 5 | 40 | 10 | 5 (target) | 5000 | 21 | 1912 (0.3824) | 0.3901 | 1 |
| 6 | 40 | 10 | 24 (control) | 5000 | 22 | 1978 (0.3956) | 0.3901 | 8 |
| 7 | 48 | 12 | 5 (target) | 2000 | 31 | 807 (0.4035) | 0.3901 | 1 |
| 8 | 48 | 12 | 24 (control) | 1000 | 32 | 375 (0.3750) | 0.3901 | 0 |

Standard errors of a proportion near 0.39 are 0.0109 (2000 trials),
0.0034 (20000), 0.0069 (5000) and 0.0154 (1000). The five-round success
rates have z-scores -1.63 (n = 24), +0.11 (n = 32), -1.11 (n = 40) and
+1.23 (n = 48) against the prediction. Against the 24-round control (standard
error sqrt(p1 q1/n1 + p2 q2/n2)) they give z = -0.46, -0.50, -1.35 and
+1.51. We found no departure from random-mapping behaviour at these sizes.
At n = 24, target and control alike fall below the prediction because
starts landing on earlier chains (event B1, last column) and the
abandonment cap are not negligible when theta*sqrt(N) is only 2^8; at full
size these events are inside eps < 7e-10 (Section 6.4).

Scope and limits: the runs test output widths of 24 to 48 bits on
restricted input sets, not 256 bits, and cannot rule out a structural
property that appears only at full width.

Five-round Keccak-f[1600] is far from ideal: zero-sum and cube-type
distinguishers exist, and the differential collision attacks of
Section 10 exist. All of these need structured, chosen inputs (affine
input subspaces, a solved linear connector and a fixed trail). The
pseudo-random walk here never chooses such inputs, and we know of no
published property predicting that pseudo-random walks of f collide less
often than those of a random function; for one fixed function, that would
itself be a strong distinguisher on unstructured inputs.

Sensitivity: H-RF affects only the success probability. Near K0 the
contact probability 1 - exp(-c^2/2), with c = K0/2^128, rises at about
0.6065 per unit of c. If the true contact probability at K0 fell short by
a small delta, restoring 0.39 needs K0 larger by a factor of about
1 + 1.66*delta, i.e. about 2.4*delta more bits. Cost and memory bounds do
not change.

## 10. Literature status and limitations

Parent AR `0cd01934` claimed 128.13 with a 2× lane-level envelope (114.09375
ops/eval). This package keeps F-COST-ABI-1 discipline (bare PERM5) and the 2×
multiplier, but inventories state traffic in **256-bit words** (7-word clear,
single-word rate load/store) as the machine model requires.



Ticket c9e2bf8f (127.994) was AI-refuted for lane_cost/F-COST-ABI-1 (fused
PERM5_ABSORB32). This package deletes that ABI and recharges with a 2x
ordinary-op envelope. H-RF remains the only score-critical heuristic;
dossier notes F-HRF-EXTRAP-1 / F-HRF-FULLWIDTH-EVIDENCE are material
evidence gaps already disclosed in Section 9, not ABI fatals. GLL tickets
d1d4fd90 / 8effb252 are parked (generation omit / not_evaluable).



Classical collision attacks on five-round SHA3-256 far below the birthday
bound are published: J. Guo, G. Liao, G. Liu, M. Liu, K. Qiao and L. Song,
"Practical Collision Attacks against Round-Reduced SHA-3", Journal of
Cryptology 33 (2020), IACR ePrint 2019/147. This package does not use them
and claims nothing about them. It is the generic attack with exact
accounting, offered as a simple, fully checkable bound for this target;
its scalar is not a security level for five-round SHA3-256.

The certificate manifest is empty: no collision is claimed or computable
at this scale. No experiment manifest is declared, and nothing needs to be
executed by the organizer. Qualification and scoring require organizer
review; exploratory qualification (`plausible_not_refuted`) is neither a
mathematical proof nor human acceptance.

## Appendix A. Source of the reduced-output experiment program

Exact C source of every Section 9 row. SHA-256 of the file:
d7a017318aff589dd589fe63a9e0317d0a820cba2b5b2d69aca4a3da285fcb26.
Build: `cc -O2 vow5.c -o vow5 -lm -lpthread`. `./vow5 test` prints the
four f cross-check vectors of Section 1 (input, digest).

```c
// Reduced-output test of the DP collision search on the 5-round SHA3-256 map.
// Usage: ./vow5 test | ./vow5 n t trials threads seed rounds   (rounds 5 or 24)
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
static const int RHO[25] = {0,1,62,28,27,36,44,6,55,20,3,10,43,25,39,41,45,15,21,8,18,2,61,56,14};
static int ROUNDS, TB; static uint64_t NMASK, K0, LMAX;
static uint64_t rol(uint64_t v, int a){ return a ? (v<<a)|(v>>(64-a)) : v; }
static void perm(uint64_t *A){            // Keccak-f[1600] rounds 0..ROUNDS-1
  uint64_t C[5], D[5], B[25];
  for(int r=0;r<ROUNDS;r++){
    for(int x=0;x<5;x++) C[x]=A[x]^A[x+5]^A[x+10]^A[x+15]^A[x+20];
    for(int x=0;x<5;x++) D[x]=C[(x+4)%5]^rol(C[(x+1)%5],1);
    for(int y=0;y<5;y++) for(int x=0;x<5;x++){ int i=x+5*y; B[y+5*((2*x+3*y)%5)]=rol(A[i]^D[x],RHO[i]); }
    for(int y=0;y<5;y++) for(int x=0;x<5;x++) A[x+5*y]=B[x+5*y]^((~B[(x+1)%5+5*y])&B[(x+2)%5+5*y]);
    A[0]^=RC[r];
  }
}
// padded block of msg(x) = LE32(x): lanes 0..3 = x, lane 4 = 0x06, lane 16 = 2^63
static void f_full(const uint64_t in[4], uint64_t out[4]){
  uint64_t S[25]={0}; for(int j=0;j<4;j++) S[j]=in[j]; S[4]=6; S[16]=1ULL<<63;
  perm(S); for(int j=0;j<4;j++) out[j]=S[j];
}
// n-bit map on n-bit x; key (lane 5) is 0 for the target, random per trial for the control
static uint64_t fn(uint64_t x, uint64_t key){
  uint64_t S[25]={0}; S[0]=x; S[4]=6; S[5]=key; S[16]=1ULL<<63; perm(S); return S[0]&NMASK;
}
static uint64_t splitmix(uint64_t *s){ uint64_t z=(*s+=0x9E3779B97F4A7C15ULL);
  z=(z^(z>>30))*0xBF58476D1CE4E5B9ULL; z=(z^(z>>27))*0x94D049BB133111EBULL; return z^(z>>31); }
typedef struct { uint64_t *k, *s, *l, mask; } map_t;   // open addressing, stores key+1
static uint64_t hh(uint64_t k){ k^=k>>33; k*=0xff51afd7ed558ccdULL; return k^(k>>33); }
static int map_get(map_t *m, uint64_t key, uint64_t *s, uint64_t *l){
  for(uint64_t i=hh(key)&m->mask; m->k[i]; i=(i+1)&m->mask)
    if(m->k[i]==key+1){ *s=m->s[i]; *l=m->l[i]; return 1; }
  return 0; }
static void map_put(map_t *m, uint64_t key, uint64_t s, uint64_t l){
  uint64_t i=hh(key)&m->mask; while(m->k[i]) i=(i+1)&m->mask; m->k[i]=key+1; m->s[i]=s; m->l[i]=l; }
typedef struct { int trials; uint64_t seed; long succ, rh, budget; } job_t;
static int trial(uint64_t *rng, map_t *m){        // 1 = verified collision, 0 = budget, -1 = start on chain
  memset(m->k,0,(m->mask+1)*8);
  uint64_t key = (ROUNDS==24) ? splitmix(rng) : 0, g=0, dpm=(1ULL<<TB)-1;
  while(g<K0){
    uint64_t s=splitmix(rng)&NMASK, x=s, len=0; int dp=0;
    while(len<LMAX){ x=fn(x,key); len++; if((x&dpm)==0){ dp=1; break; } }
    g+=len; if(!dp) continue;                      // abandoned chain
    uint64_t s2, l2;
    if(!map_get(m,x,&s2,&l2)){ map_put(m,x,s,len); continue; }
    uint64_t a=s, b=s2, la=len, lb=l2;             // RELOCATE
    while(la>lb){ a=fn(a,key); la--; } while(lb>la){ b=fn(b,key); lb--; }
    if(a==b) return -1;
    for(;;){ uint64_t fa=fn(a,key), fb=fn(b,key);
      if(fa==fb) return (a!=b && fn(a,key)==fn(b,key)) ? 1 : 0;
      a=fa; b=fb; }
  }
  return 0;
}
static void *worker(void *p){ job_t *J=p; uint64_t rng=J->seed; map_t m;
  int bits=(int)ceil(log2((double)K0/(double)(1ULL<<TB)))+3; if(bits<8) bits=8;
  m.mask=(1ULL<<bits)-1; m.k=malloc(8<<bits); m.s=malloc(8<<bits); m.l=malloc(8<<bits);
  for(int t=0;t<J->trials;t++){ int r=trial(&rng,&m); if(r>0) J->succ++; else if(r<0) J->rh++; else J->budget++; }
  return 0; }
int main(int argc, char **argv){
  if(argc==2 && !strcmp(argv[1],"test")){ ROUNDS=5; uint64_t sd=12345;
    for(int i=0;i<4;i++){ uint64_t in[4], out[4]; for(int j=0;j<4;j++) in[j]=splitmix(&sd); f_full(in,out);
      for(int j=0;j<8;j++){ uint64_t w=j<4?in[j]:out[j-4]; for(int b=0;b<8;b++) printf("%02x",(unsigned)(w>>(8*b))&0xff); if(j==3) printf(" "); }
      printf("\n"); }
    return 0; }
  if(argc!=7) return 1;
  int n=atoi(argv[1]), trials=atoi(argv[3]), th=atoi(argv[4]); TB=atoi(argv[2]);
  uint64_t seed=strtoull(argv[5],0,0); ROUNDS=atoi(argv[6]);
  NMASK=(1ULL<<n)-1; K0=(uint64_t)ceil(0.9944*pow(2.0,n/2.0)); LMAX=1ULL<<(TB+5);
  pthread_t T[64]; job_t J[64]; memset(J,0,sizeof J); long su=0, rh=0, bu=0;
  for(int i=0;i<th;i++){ J[i].trials=trials/th+(i<trials%th); J[i].seed=seed*1000003ULL+i*0x1234567ULL+1;
    pthread_create(&T[i],0,worker,&J[i]); }
  for(int i=0;i<th;i++){ pthread_join(T[i],0); su+=J[i].succ; rh+=J[i].rh; bu+=J[i].budget; }
  printf("rounds=%d n=%d t=%d K0=%llu trials=%d success=%ld (%.4f) pred=%.4f start_on_chain=%ld budget=%ld\n",
    ROUNDS,n,TB,(unsigned long long)K0,trials,su,(double)su/trials,
    1-exp(-(double)K0*((double)K0+1)/pow(2.0,n+1)),rh,bu);
  return 0;
}
```
