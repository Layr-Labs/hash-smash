# Heuristic-free bit-sliced birthday search with a bijective early key for SHA-256 r37

## 1. Claim and scope

This package specifies a classical randomized algorithm for the exact
`sha256-r37-prefix-v1` target (standard IV, FIPS 180-4 padding, rounds 0..36 on
every padded block, standard feed-forward, full 256-bit big-endian digest). Under
`collision-frontier-v5` with `C = 2644`, its worst-case total charged time is

```
T  <  2^124.786   target-compression units,
```

its success probability is at least `0.3901` (claimed `0.39`), its peak memory is
below `2^135.6` bytes, its preprocessing is below `2^118` units, and it uses no
nonuniform advice.

The success bound is **distribution-free**: it holds for every fixed function
with a 256-bit output, and therefore for the exact reduced SHA-256, without any
random-oracle, balance, independence or differential premise. The claim's
`heuristics` list is empty. The two declared experiments check that the counted
batch program computes the exact target digest; no score-critical quantity is
estimated from them.

No collision witness is supplied and no full-scale execution is claimed. This is
a constant-factor improvement of the generic birthday search, not a weakness of
SHA-256. `baseline_improved` names the organizer nominal reference
(`sha256-r37-nominal-v2`, display value 128); it is a required identifier. For
comparison only: the organizer baseline package for this track is a merge-sort
birthday search with `time_log2 = 132`.

Where the constant factor comes from, in one line each:

1. **Bit-slicing.** One 256-bit word holds one bit position of 256 independent
   messages, so each XOR/AND/OR advances 256 messages; rotations are renamings.
2. **A bijective early key.** Instead of the digest, the algorithm sorts a
   256-bit key that is an explicit *bijective* re-encoding of the final state
   (Section 4). The key needs only part of rounds 31..36. Because the re-encoding
   is a bijection, key collisions are exactly digest collisions; nothing is
   truncated, so no false-positive or random-function argument is needed.
3. **A shared constant prefix.** Every message starts with the same 21 zero
   bytes, so rounds 0..4 are the same constant for all messages and are folded
   into the circuit. The 34 remaining bytes are uniform and independent, so the
   sampled messages are still iid from one fixed distribution.
4. **A linear-time distribution-free duplicate finder** (one stable counting
   sort on the high 128 key bits plus one scan with a last-seen table on the low
   128 bits) replacing comparison sorting.

## 2. Messages, padding and the target function

Let `d = 2^272`. Each message is the 55-byte string

```
m = 00^21 || r_0 || r_1 || ... || r_33          (r_i uniform independent bytes)
```

so messages are iid uniform on a fixed set D of exactly `d` strings, all of bit
length 440. Because `55 <= 55`, FIPS 180-4 padding gives exactly one 64-byte block:
byte 55 is `0x80`, and bytes 56..63 are the 64-bit big-endian value 440. In
32-bit big-endian words,

```
W0 = W1 = W2 = W3 = W4 = 0
W5  = 00 || r0 || r1 || r2
W6 .. W12 = r3 .. r30            (four bytes per word, big-endian)
W13 = r31 || r32 || r33 || 80
W14 = 0,  W15 = 0x000001b8       (= 440)
```

The complete hash `h(m)` starts at the standard IV, runs the standard schedule
and rounds 0..36 of this single block, adds the working state to the IV word by
word modulo 2^32, and serializes the eight words big-endian. No chaining value is
chosen and no output bit is discarded.

Random bit `j = 8*i + k` (byte `r_i`, bit `k`, `k = 0` least significant) of the
message in lane `l` of a batch is bit `l` of the batch's random word `R_j`.
Each batch draws `272` independent uniform 256-bit words `R_0..R_271`, so the
256 messages of a batch, and messages of different batches, are iid uniform on D.

## 3. Round notation

For `j = 0..36`, with message schedule words `W_j` (`W_t = s1(W_{t-2}) + W_{t-7} +
s0(W_{t-15}) + W_{t-16}` for `t >= 16`) and constants `K_j`:

```
T1_j    = E_{j-3} + S1(E_j) + Ch(E_j, E_{j-1}, E_{j-2}) + K_j + W_j
T2_j    = S0(A_j) + Maj(A_j, A_{j-1}, A_{j-2})
A_{j+1} = T1_j + T2_j
E_{j+1} = A_{j-3} + T1_j
```

All additions are modulo 2^32. `(A_0, A_{-1}, A_{-2}, A_{-3}) = (H0, H1, H2, H3)`
and `(E_0, E_{-1}, E_{-2}, E_{-3}) = (H4, H5, H6, H7)` are the IV words. This is
the standard round: before round j the working variables are
`a,b,c,d = A_j, A_{j-1}, A_{j-2}, A_{j-3}` and `e,f,g,h = E_j, E_{j-1}, E_{j-2}, E_{j-3}`.
After 37 rounds the state is

```
S(m) = (A37, A36, A35, A34, E37, E36, E35, E34)
```

and the digest is `S(m) + IV` word by word. Adding the fixed IV is a bijection of
256-bit strings, so `h(m) = h(m')` if and only if `S(m) = S(m')`.

## 4. The bijective key

Define, for each message, the 256-bit key

```
Key(m) = (A30, A31, Z32, T1_32, T1_33, T1_34, Y35, X36), where
Z32 = T1_31 + Maj(A31, A30, A29)
Y35 = E32 + Ch(E35, E34, E33) + W35
X36 = E33 + W36.
```

**Lemma 1 (key to state).** The following map `Psi` satisfies `Psi(Key(m)) = S(m)`
for every message m. Write `T2(x,y,z) = S0(x) + Maj(x,y,z)`.

```
A32 = Z32 + S0(A31)
A33 = T1_32 + T2(A32, A31, A30)
A34 = T1_33 + T2(A33, A32, A31)
A35 = T1_34 + T2(A34, A33, A32)
E34 = A30 + T1_33
E35 = A31 + T1_34
T1_35 = Y35 + S1(E35) + K35
A36 = T1_35 + T2(A35, A34, A33);   E36 = A32 + T1_35
T1_36 = X36 + S1(E36) + Ch(E36, E35, E34) + K36
A37 = T1_36 + T2(A36, A35, A34);   E37 = A33 + T1_36
```

*Proof.* Each line is a round equation of Section 3 for j = 31..36, with the
identities `A32 = T1_31 + T2_31 = Z32 + S0(A31)`,
`T1_35 = E32 + S1(E35) + Ch(E35,E34,E33) + K35 + W35 = Y35 + S1(E35) + K35` and
`T1_36 = E33 + S1(E36) + Ch(E36,E35,E34) + K36 + W36 = X36 + S1(E36) + Ch(E36,E35,E34) + K36`.
Every right-hand side uses only key words and values computed on earlier lines.

**Lemma 2 (state to key).** The following map `Phi` satisfies `Phi(S(m)) = Key(m)`.

```
T1_36 = A37 - T2(A36, A35, A34);   A33 = E37 - T1_36
T1_35 = A36 - T2(A35, A34, A33);   A32 = E36 - T1_35
T1_34 = A35 - T2(A34, A33, A32);   A31 = E35 - T1_34
T1_33 = A34 - T2(A33, A32, A31);   A30 = E34 - T1_33
T1_32 = A33 - T2(A32, A31, A30)
Z32 = A32 - S0(A31)
Y35 = T1_35 - S1(E35) - K35
X36 = T1_36 - S1(E36) - Ch(E36, E35, E34) - K36
```

*Proof.* These are the same equations solved for the other unknown, using
`A_{j+1} = T1_j + T2_j` and `E_{j+1} = A_{j-3} + T1_j`.

**Corollary.** For all messages m, m': `Key(m) = Key(m')` iff `S(m) = S(m')` iff
`h(m) = h(m')`. (If keys agree, apply Psi; if states agree, apply Phi.) In fact
Phi and Psi are mutually inverse permutations of `{0,1}^256`: each step adds or
subtracts a function of words already known on both sides.

So the algorithm may search for key collisions instead of digest collisions.
The key needs only: full rounds 5..30; round 31 without `S0(A31)` and with one
addition `T1_31 + Maj` instead of two; rounds 32..34 without `T2` and without `A33..A35`;
round 35 reduced to two additions and one Ch; round 36 reduced to one addition.
Rounds 0..4 are constant (Section 7.2). All 21 schedule words `W16..W36` are
computed because `W35` and `W36` are needed.

The experiment program contains `key_to_digest` (Psi followed by `+ IV`) and
`state_to_key` (Phi); trial 0 checks both on every lane of a batch against an
independent scalar implementation of the target. Locally `Phi(Psi(k)) = k` was
also checked on 20,000 uniformly random 256-bit k.

## 5. Algorithm

Parameters: `NB = 1321860456990702717723188087783627883` batches of 256 messages,
`n = 256*NB` messages; `n = 0.994457... * 2^128`. A message id is the address of
its key word. Tables are word arrays in a flat word-addressed memory:

| Region | Words | Content |
| --- | ---: | --- |
| `C1 = [0, 2^128)` | 2^128 | counters indexed by the high key half |
| `L = [2^128, 2^129)` | 2^128 | last-seen table indexed by the low key half |
| `A = [2^130, 2^130 + n)` | n | key words in generation order |
| `B = [2^131, 2^131 + n)` | n | ids in high-half order |
| `ARCH = [2^132, 2^132 + 512*NB)` | 2n | random words; batch b uses `2^132 + 512b + j`, j < 272 |
| `SP = [2^133, 2^133 + 2^12)` | < 2^12 | 8 transpose masks, register spill slots |

Pseudocode (inert; every operation is charged in Section 8):

```
P0  zero C1 and L                                   # preprocessing
P1  for b in 0..NB-1:                               # batch program, Section 7
        draw R_0..R_271; store them at ARCH + 512b
        compute the 256 key planes; transpose to 256 key words y_0..y_255
        for l in 0..255: A[256b+l] = y_l; C1[y_l >> 128] += 1
P2  s = 2^131; for i in 0..2^128-1: c = C1[i]; C1[i] = s; s = s + c
P3  for p in A (in address order):                  # stable counting sort
        y = mem[p]; pos = C1[y >> 128]; mem[pos] = p; C1[y >> 128] = pos + 1
P4  for x in B (in address order):                  # duplicate detection
        p = mem[x]; y = mem[p]; idx = (y AND (2^128-1)) OR 2^128
        q = mem[idx]; mem[idx] = p
        if q != 0 and mem[q] == y: goto P5 with (q, p)
    return FAILURE
P5  recover the two 34-byte random parts from ARCH (batch = (id - 2^130) >> 8,
    lane = id AND 255); if the complete messages are equal return FAILURE;
    otherwise recompute both complete hashes with the target compression,
    return the pair if they are distinct with equal digests, else FAILURE.
```

**Lemma 3 (P3 sorts stably).** After P2, `C1[v]` is the first B address of the
block of records whose high half is v, blocks in increasing v. P3 writes each id
into the next free slot of its block, visiting A in address order. Hence B lists
all n ids grouped by high half, and within a group in A order. This is the
standard counting sort; it is correct for every key multiset, including all keys
equal.

**Lemma 4 (P4 finds a key repeat if one exists).** Suppose two records have equal
keys. Let y be the first position in B that has an equal-key record before it in
B, and let x be such an earlier position. Every position between x and y has the
same high half as x and y (B is grouped by high half). When P4 reaches y,
`L[low(y)]` holds the id of the most recent earlier position z with
`low(z) = low(y)` (L was zeroed, ids are nonzero, and every visited record
overwrites its slot). Since x itself qualifies, z lies in `[x, y)`, so
`high(z) = high(y)` and `low(z) = low(y)`: the keys are equal and P4 stops. Before
y, no position has an equal-key predecessor, and `q != 0` occurs only for genuine
earlier ids, so P4 never stops on unequal keys. If no two keys are equal, P4 never
stops and returns FAILURE after the full scan.

**Lemma 5 (output correctness).** P5 returns only a pair of distinct complete
messages whose complete r37 hashes agree, because it recomputes both with the
target compression and compares messages and digests explicitly.

## 6. Success probability (distribution-free)

Let `k(.)` be the fixed function `m -> Key(m)` on D, with output set of size
`M = 2^256`, and let `p_y` be the probability of key value y under a uniform
message. The n keys are iid with distribution p.

**Lemma 6.** For `2 <= n <= M`, `Pr[all n keys distinct] = n! e_n(p_1..p_M)`, where
`e_n` is the elementary symmetric polynomial; this is at most its value at the
uniform distribution. *Proof.* Fix all coordinates but two, a and b; then
`e_n = U + (a+b) V + a b X` with `X >= 0`, so replacing a and b by their mean keeps
the sum and does not decrease `e_n`. Among maximizers of `e_n` on the compact
simplex pick one minimizing the sum of squares. If two coordinates differed,
averaging them would either increase `e_n` or keep it while reducing the sum of
squares; both are contradictions. So the uniform point is a maximizer, and

```
Pr[no key repeat] <= prod_{i<n} (1 - i/M) <= exp(-n(n-1)/(2M)).
```

Let `E_out` be "some two keys are equal" and `E_in` "some two sampled messages
are equal". By the union bound `Pr[E_in] <= n(n-1)/(2d)`. On `E_out` and not
`E_in`, Lemma 4 makes P4 stop on two records with equal keys, the two messages
differ, and by the Corollary of Section 4 their complete hashes agree, so P5
returns a valid collision. Hence

```
Pr[success] >= 1 - exp(-n(n-1)/(2*2^256)) - n(n-1)/(2*2^272).
```

For the stated n, `x = n(n-1)/2^257 = 0.49447...`, and the certificate in
Appendix A evaluates the bound with exact rational arithmetic, bounding `exp(x)`
below by its 30-term Taylor sum, giving `>= 0.3901`. The second term is below
`2^-17`. No property of SHA-256 is assumed: the bound holds for every function
from D to 256-bit strings.

## 7. The batch program

### 7.1 Machine model and conventions

The program runs on a 256-bit word RAM with 64 general registers. Every executed
instruction is one primitive operation charged `1/C`:

- `LD r,[b+i]` and `ST r,[b+i]` (base register plus small immediate offset);
- `XOR`, `AND`, `OR`, `ADD`, `SUB` with register or small immediate operand;
- `SHL`/`SHR` by an immediate or register-held count; comparison and
  conditional branch are two separate operations;
- `RAND r`, one independent uniform 256-bit word.

All loads and stores are charged, including spills, reloads, archive stores,
table accesses and constant loads. Four registers hold loop pointers (`AP`,
`ARCHP`, `SP`, `AEND`), so the allocator uses 60. The target compression itself
is executed only twice (P5); everything else is ordinary operations. This is the
same accounting basis as the cost model's C, which counts word operations of the
reference compression; here memory traffic and loop control are charged in
addition. Section 10 gives the counts under other register-file sizes.

### 7.2 Bit-sliced circuit

Each 32-bit word is 32 *planes*; plane i is a 256-bit register whose bit l is bit
i of that word in lane l. Rotations and shifts of words are renamings of planes;
the only gates are 2-input XOR, AND and OR on planes.

*Literals and complement flags.* Every circuit value is a literal: a gate output
with a complement flag, or a constant 0/1. XOR with a constant or a complemented
input changes the flag only. `AND(~x,~y) = ~OR(x,y)` costs one gate;
`AND(x,~y) = x XOR (x AND y)` costs two. Constants are propagated, identical
gates are shared (`x op y` is created once), and `x XOR x`, `x AND x` simplify.
These rewrites preserve the Boolean function.

*Adders.* Words are added by ripple carry, one bit column at a time, least
significant bit first. For a non-constant column `(a, b, c)` choose two inputs
`x, y` with equal complement flags (two of three always agree) and the third as
pivot `p`; then

```
t = x XOR p,  u = y XOR p,  sum = t XOR y,  carry = p XOR (t AND u)
```

which is 5 gates with no NOT in every flag pattern (`t` and `u` have equal flags,
so `t AND u` is one AND or one OR). Correctness: if `x = p` then `t = 0`,
carry `= p = maj`; if `x != p` then `t = 1`, carry `= p XOR u = y`, and indeed
`maj(x,y,p) = y` when `x != p`. A column with one constant input is a half adder
(XOR plus AND, or XNOR plus OR; 2 gates, 3 if flags differ). Bit 31 needs only
the two sum XORs.

*Round functions.* `S1`, `S0`, `s0`, `s1` are XORs of renamed planes (`s0`, `s1`
use zero planes for the shifted-in bits). `Ch(e,f,g) = g XOR (e AND (f XOR g))`;
`Maj(a,b,c) = b XOR ((a XOR b) AND (b XOR c))`, where `b XOR c` is the previous
round's `a XOR b` and is shared. Each round column evaluates, in order, the
schedule column (three chained adders: `W_{t-16} + W_{t-7}`, `+ s0`, `+ s1`),
`W_t + K_t`, `+ h`, `+ S1(e)`, `+ Ch` (giving `T1`), `d + T1` (giving E), and for
rounds up to 30 `S0(a) + Maj` and `T1 + T2` (giving A). Round 31 uses `T1 + Maj`
(giving Z32); rounds 32..34 compute T1 and E only; round 35 computes
`(E32 + W35) + Ch(E35,E34,E33)`; round 36 computes `E33 + W36`.

*Constant rounds.* Message words W0..W4 are zero and the IV is fixed, so rounds
0..4 fold to constants inside the builder; the first gate appears at round 5,
where W5 has 24 random bits. Constant folding also removes many gates in rounds
5..20 and in `W16..W20`.

The generated circuit (`build()` in the experiment program) has **46,151 gates**:
36,736 XOR, 4,350 AND and 5,065 OR, for 272 inputs and 256 output planes, of which
132 carry a complement flag. All gates are live. A flag on an output plane means
the stored key is `Key XOR F` for a fixed public constant F; this is a bijection,
so collisions are unchanged, and the program strips F before decoding.

### 7.3 Transpose and per-message emission

The 256 key planes are transposed into one 256-bit key word per lane with the
standard recursive delta swap: for `s = 128, 64, ..., 1` and every row pair
`(r, r+s)` with `r AND s = 0`,

```
t = ((x >> s) XOR y) AND mask_s;   y = y XOR t;   x = x XOR (t << s)
```

where `mask_s` has bit m set iff `m AND s = 0`. This is 1,024 swaps of 6
operations (the swap levels act on independent index bits, so their order is
free; the program does the three large levels on 8-row groups and the five small
levels on 32-row blocks). Each key word y is then stored to `A` and its high-half
counter is incremented: `ST`, `SHR 128`, `LD`, `ADD 1`, `ST` (5 operations).

### 7.4 Straight-line program, allocation and execution

`program()` emits the circuit gates in the round-column order above, with each
`RAND` (plus its archive store) placed just before the first use of that random
word, followed by the transpose and the emission. `allocate()` assigns the 60
registers by furthest-next-use eviction; an evicted value with a later use is
stored to a spill slot unless memory already holds it (random words are reloaded
from the archive, masks from the constant table), and every reload is an explicit
`LD`. The result is a fixed straight-line program of 67,405 instructions plus 4
loop-control operations per batch. Its operation count does not depend on data:
there are no branches inside the batch.

| Part (per batch of 256 messages) | Operations |
| --- | ---: |
| Circuit gates (XOR 36,736, AND 4,350, OR 5,065) | 46,151 |
| `RAND` 272 and archive stores 272 | 544 |
| Transpose: 1,024 swaps x 6 (SHR, SHL, AND 1,024 each; XOR 3,072) | 6,144 |
| Emission: 256 x (ST, SHR, LD, ADD, ST) | 1,280 |
| Allocator loads (8,639 spill, 1,106 archive, 8 mask) | 9,753 |
| Allocator stores (spill) | 3,533 |
| Loop: `AP += 256`, `ARCHP += 512`, compare, branch | 4 |
| **Total** | **67,409** |

That is `263.316` operations per message. In trial 0 of each experiment, the VM in
the program executes this allocated program on organizer-seeded random words,
counts every executed instruction (67,409), and checks all 256 stored key words:
against the direct gate evaluation, against an independent scalar `sha256-r37`
through Psi, and against Phi of the scalar state; it also checks the histogram
increments. Locally this check passed on several seeds with zero mismatches.

## 8. Operation ledger and total time

Loops in P0, P2, P3 and P4 are unrolled with immediate offsets.

| Phase | Count | Operations |
| --- | --- | ---: |
| P0 zero C1 and L | per 64 words: 64 ST, pointer ADD, compare, branch | `2 * 2^122 * 67` |
| P1 batches | per batch | `NB * 67,409` |
| P2 prefix | per 64 counters: 64 x (LD, ST, ADD), pointer ADD, compare, branch | `2^122 * 195` |
| P3 scatter | per 256 records: 256 x (LD y, SHR, LD pos, ADD id, ST id, ADD pos, ST pos) + 3 | `NB * 1,795` |
| P4 scan | per 256 records: 256 x (LD p, LD y, AND, OR, LD q, ST p, CMP+BR, LD, CMP+BR) + 3 | `NB * 2,819` |
| P5 and global setup | message recovery (< 3,000), checks, constants, registers | `< 2^14 + 2^12` |
| Target compressions | P5 only | 2 |

P4 is charged its worst case: both comparisons executed for every record. The
masks and `2^128 - 1`, `2^128` are constants loaded during setup. No phase has a
data-dependent loop length; the only data-dependent branch is the early stop.

Total ordinary operations: `W = NB * 72,023 + 329 * 2^122 + 2^14 + 2^12`, i.e.
`286.509` per message. Hence

```
T = 2 + W / 2644 < 2^124.786       (log2 T = 124.78591...)
```

which the certificate verifies exactly by comparing integer powers. `time_log2 =
124.786` is this bound rounded up. For reference, `n * 1` would be `2^127.992`:
the search costs about `0.1084` target compressions per sampled message.

## 9. Memory, preprocessing and advice

Words in use: C1 and L, `2^129`; A and B, `2n`; the archive region, `2n` (272 of
every 512 words are used; the rest is counted anyway); spill and mask area,
`< 2^12`; the straight-line batch program and the loop code, under `2^17` words
at one word per instruction. Total below `6 * 2^128` words, i.e. below
`192 * 2^128 < 2^135.6` bytes. No other storage is retained; random words are
stored once, in the archive. Addresses are below `2^134` and fit a word.

Preprocessing (P0 plus setup) is `(134 * 2^122 + 2^12)/2644 < 2^117.70` units; it
is included in T. The program is uniform: the only constants are the public
SHA-256 constants, the IV, the transpose masks and the fixed parameters above.
Nonuniform advice is zero (`nonuniform_advice_log2_bytes = 0` records the bound
of one byte). The 67,405-instruction batch program is generated deterministically
from those constants by the experiment source and is counted as code above.

## 10. Sensitivity

| Reading | Operations per message | log2 T |
| --- | ---: | ---: |
| 64 registers (claimed) | 286.51 | 124.786 |
| 48 registers | 291.92 | 124.813 |
| 32 registers | 301.27 | 124.858 |
| 128 registers (reference) | 273.02 | 124.716 |
| loads and stores of the batch free (reference only) | 234.61 | 124.498 |
| every batch memory access also charged one address addition | about 342.5 | about 125.04 |

All register rows were re-allocated and recounted by the same program. The
bound also does not change materially if P4's early stop is removed (it is
already charged as a full scan).

## 11. Evidence

The proof above is complete without experiments; the experiments check the
implementation. Both use `python-message-pairs-v1` with the same program and 256
organizer seeds; each trial is one batch of 256 messages of the Section 2 family
derived from the trial seed by SHAKE-256 (a reproducibility device; the full
attack uses independent random words).

- `r37-keyed-batch-mask-a`: mask = bits 0 and 17 of each of the eight digest words.
- `r37-keyed-batch-mask-b`: mask = bits 9 and 30 of each digest word.

Each trial evaluates the gate list, transposes, decodes every key to a full digest
with Psi, and returns the first two distinct messages whose decoded digests agree
on the 16 masked bits. The organizer recomputes both digests with the trusted
reference; a wrong circuit plane, transpose, polarity or decoding on a masked
bit would make returned pairs fail. The model rate of a 16-bit match among 256
messages is 0.3927 per trial; it is not a score input. Trial 0 additionally
reports `batch_ops`, `vm_executed_ops` and `vm_lane_mismatches` (expected 67,409,
67,409 and 0); these are participant observations.

Local runs with my own seeds (not organizer evidence): 92/256 and 100/256
successes, and every returned pair (192 pairs) was re-checked with
`verifier/hash_functions.py: digest(m, "sha256", 37)` with no failure; each run
took under 3 seconds and about 72 MB.

## 12. Relation to other work and credit

Bit-slicing SHA-256 across 256 messages, the delta-swap transpose to per-message
key words, and charging an explicitly register-allocated straight-line program on
a 64-register machine follow earlier public packages on this track, in particular
mitchuski's bit-sliced circuit (`abaa09ae`, `fca38c6d`), jaazinn's counted
64-register program (`817d444c`) and the delta-swap transpose lineage they
credit. Computing only what an early key needs follows jungjipdo (`383bad42`).
Those packages use truncated keys over grouped message sets and therefore declare
a random-function heuristic. The parts specific to this package are the
complete-domain iid design with a fixed shared prefix, the bijective key of
Section 4 with its explicit inverse, the distribution-free success argument
carried over to that key, the counting-sort plus last-seen-table duplicate finder,
and the circuit, allocation and counts given here.

Context sources: NIST FIPS 180-4 (SHA-256 padding, schedule and rounds);
M. Bellare and T. Kohno, *Hash Function Balance and Its Impact on Birthday
Attacks* (2004), for the fact that unbalanced fixed functions only increase
collision probability; P. Briggs and L. Torczon (1993) and standard counting-sort
analysis for the table techniques. All arguments needed here are given above.

## 13. Limitations

- No collision is exhibited; the search is infeasible to run in full.
- The circuit and allocation are checked by execution on random batches (local
  and organizer trials), not by formal verification of each gate; the round
  equations and gate identities they implement are stated in Sections 4 and 7.
- The score depends on the 64-register, base-plus-immediate addressing machine
  model; Section 10 lists other readings.
- Memory is about `2^135.6` bytes; it is reported, not scored.

## Appendix A. Certificate (inert text)

```python
from fractions import Fraction as F
NB = 1321860456990702717723188087783627883; n = 256 * NB
def exp_lower(x, terms=30):          # e^x >= partial Taylor sum for x >= 0
    s, t = F(0), F(1)
    for k in range(terms):
        s += t; t = t * x / (k + 1)
    return s
x = F(n * (n - 1), 2 * 2**256)
succ = 1 - 1 / exp_lower(x) - F(n * (n - 1), 2 * 2**272)
assert succ >= F(3901, 10000)
W = NB * (67409 + 7*256 + 3 + 11*256 + 3) + 2 * 2**122 * 67 + 2**122 * 195 + 2**14 + 2**12
T = 2 + F(W, 2644)
assert T.numerator ** 1000 < 2 ** 124786 * T.denominator ** 1000     # T < 2^124.786
P = F(2 * 2**122 * 67 + 2**12, 2644)
assert P < 2 ** 118
```

Output when run: all assertions pass; `succ >= 0.3901`, `log2 T = 124.78591...`,
`log2 P = 117.698...`.
