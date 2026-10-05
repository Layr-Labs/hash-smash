# sha256-r32: grouped birthday search with a 160-bit difference key, time_log2 = 125.990

Authors: winglock, with jaazinn credited as co-author. The construction is
jaazinn's, from their accepted packages: grouped partial evaluation and the
never-initialised sparse set (blake3-r2-exploratory, ticket 0a5b7ae8), and the
SHA-256 form of it with single-block 55-byte messages, W13 as the varying word,
early abort on a partial digest key, 4-operation rotations, immediate shift
counts and the 64-register machine (sha256-r32-exploratory, ticket 6b88bdb7,
126.695). Our additions are listed in Section 1.3.

This is a generic birthday search with a constant-factor saving. It is not a
differential or algebraic attack, and it claims no weakness of SHA-256. The
scalar is below 128 only because the charged work per message is about 0.25
of a compression.

## 0. Claim

| quantity | value |
| --- | --- |
| target | sha256-r32-prefix-v1 (steps 0..31, fixed IV, feed-forward, 256-bit digest) |
| cost model | collision-frontier-v5, C = 2224 |
| messages N | 2^128 = 2^104 groups x 2^24 values of y |
| per-message body, including key packing (counted by the evaluator) | 532 operations |
| per message, counted | 548 = 532 + 13 (table step) + 3 (loop) |
| per message, charged | 552 (4-operation spare) |
| time T | <= 2^128 * 552/2224 + 2^104 + 3 * 2^110 + 1 < 2^125.98966 |
| claimed time_log2 | 125.990 (rounded up) |
| success probability | >= 0.39 under heuristic H1 (model value 0.39339) |
| memory | < 2^146 bytes (reported only) |
| preprocessing, advice | 0, 0 |

The time bound is a worst-case cap on every run. Every output is checked with
two whole reference compressions. Only the success probability uses H1.

## 1. Target, machine and counting convention

### 1.1 Target and notation

The target is `verifier/hash_functions.py:digest(m, "sha256", 32)`: steps
i = 0..31, schedule W16..W31, then the feed-forward. A_i and E_i denote the new
a and e produced by step i. A_{-1..-4} and E_{-1..-4} are the IV words a, b, c, d
and e, f, g, h. Step i reads a, b, c, d = A_{i-1}, A_{i-2}, A_{i-3}, A_{i-4} and
e, f, g, h = E_{i-1}, E_{i-2}, E_{i-3}, E_{i-4}. It computes
T1 = h + Sigma1(e) + Ch(e,f,g) + K_i + W_i and T2 = Sigma0(a) + Maj(a,b,c), and
sets A_i = T1 + T2 and E_i = d + T1 (mod 2^32). The final state is
(A31, A30, A29, A28, E31, E30, E29, E28), and H_j = IV_j + state_j mod 2^32.

### 1.2 Machine and counting

The cost model is a classical probabilistic 256-bit word RAM. One target
compression costs 1 unit. Every other primitive costs 1/C = 1/2224 unit: a
256-bit load or store, addition mod 2^256, AND, OR, XOR, NOT, a shift,
a comparison, a branch, or a fresh random word.

Every convention below is one the cost-model text states or one the judge
accepted in jaazinn's sha256-r32 package (6b88bdb7):

- (C1) Each 256-bit add, AND, OR, XOR, NOT and shift costs 1, as in
  `scripts/reference_operation_costs.py`. The counter in `experiments/` is that
  script's int-subclass counter, which also counts reflected operators.
- (C2) Shift counts are immediates (6b88bdb7). The mask M = 2^32 - 1 and the
  round and group constants sit in registers (6b88bdb7: 64 registers, constants
  held in registers).
- (C3) A shift is a 256-bit shift: `x << k` keeps bits 0..255 of x * 2^k, and
  `x >> k` is floor(x / 2^k). Additions are mod 2^256.
- (C4) A white-box per-message program may cost less than a whole compression.
  jaazinn's accepted package prices a white-box compression at 1840 < C
  operations. Section 9 gives ours.
- (C5) Group setup is charged per group. Key matches are confirmed with two
  whole reference compressions, each charged 1 unit (6b88bdb7).

Two implementation facts inside (C1)-(C3) are argued here; neither is a new price.

Lemma 1 (exact lazy masking). Let x and y be words with the correct values
modulo 2^32 in bits 0..31, and arbitrary bits above. Then x + y, x AND y,
x OR y, x XOR y and NOT x are correct in bits 0..31, and (x << k) has bits
0..31 depending only on bits 0..31-k of x. A right shift or a Sigma input is
the only place where high bits could reach bits 0..31. So every value is
reduced with `& M` (1 operation) before it is (i) the input of a Sigma or
sigma function, (ii) right-shifted, or (iii) placed in a key field other than
the top one. The top key field is written by `<< 224`, which drops everything
above bit 31 for free (C3). The program does exactly this. The evaluator
checks it bit for bit (Section 8).

Lemma 2 (Sigma by doubling). For a reduced word x < 2^32, let z = x | (x << 32).
Then bit j of z equals bit (j mod 32) of x for j < 64. So for 0 < k < 32 the
low 32 bits of z >> k are rotr_k(x). Hence, with all bits 0..31 exact:

```
Sigma1(x) = (z ^ z>>5  ^ z>>19) >> 6        = z>>6  ^ z>>11 ^ z>>25
Sigma0(x) = (z ^ z>>11 ^ z>>20) >> 2        = z>>2  ^ z>>13 ^ z>>22
sigma1(x) = (((z ^ z>>2)  >> 7) ^ x) >> 10  = z>>17 ^ z>>19 ^ x>>10
sigma0(x) = (((z ^ z>>11) >> 4) ^ x) >> 3   = z>>7  ^ z>>18 ^ x>>3
```

Each costs 7 operations: shl and or for z, then 2 shr, 2 xor and 1 shr (or
shr, xor, shr, xor, shr). Every right-shift operand is below 2^64 and a pure
function of x, so the result is below 2^64 with bits 0..31 exact (Lemma 1
then applies). No rotation instruction is assumed. These are the explicit
shifts and ORs that the reference script's header requires of narrow rotations
("no native 32/64-bit rotate is assumed"). The one mask a rotation would
carry is paid once on the input word, where Lemma 1 needs it anyway.

### 1.3 What is new relative to 6b88bdb7

(1) A 160-bit key (A28, A29, E28, E29, D30) with D30 = A30 - E30, instead of
the leader's 192-bit (A28..A30, E28..E30): the program stops after step 29 plus
the T2 half of step 30 and never forms W30 or W28 (only K28 + W28). (2) Exact
constant folding at steps 14..16, Maj = b ^ ((a ^ b) & (b ^ c)) with a shared
a ^ b, and Ch = g ^ (e & (f ^ g)). (3) Lemmas 1 and 2. (4) A 13-operation
table step that writes every key at its message index (Section 4).

## 2. Algorithm

Every message is exactly 55 bytes. The padded single block is W0..W12 (52 free
bytes), W13 = (y << 8) | 0x80 (three free bytes y and the 0x80 padding byte),
W14 = 0 and W15 = 440.

State: G (two random words per group), S[2^140] (sparse index, never
initialised), D[2^128] (one key per message), m = 0 (message counter), r = Dbase
and v = 0 (key-match counter, kept in memory).

1. For gid = 0 .. 2^104 - 1: draw two fresh uniform 256-bit words, store them in
   G[gid], unpack W0..W12 from their first 416 bits, and run the group setup
   (Section 3.2).
2. For y = 0 .. 2^24 - 1 (register w = W13, starting at 0x80 and stepping by 0x100):
   a. Run the body (Section 3.3), which gives the packed key K.
   b. Run the table step (Section 4). On MATCH with record s, set v = v + 1 and
      halt with failure if v > 2^110. Otherwise rebuild messages s and m and
      check that they differ and that both full digests are equal
      (Section 5). If so, output the pair and halt. If not, continue at INS.
3. If all N = 2^128 messages are processed without success, halt with failure.

Message index m = gid * 2^24 + y, so record s names its message:
gid = s >> 24 and y = s & (2^24 - 1).

## 3. The grouped evaluator

### 3.1 Dependence on W13

With W0..W12 fixed, steps 0..12 are group constants, and W13 enters step 13
only additively. In the schedule, W13 enters W20 (as W_{t-7}), W28 (through
sigma0) and W29 (as W_{t-16}), and then W22, W24, W26 and W27 through the
recursion. W16..W19, W21, W23 and W25 are group constants (6b88bdb7). With
c-values from the group setup:

- W20 = W13 + c20, with c20 = W4 + s0(W5) + s1(W18)
- W22 = s1(W20) + c22, with c22 = W6 + s0(W7) + W15
- W24 = s1(W22) + c24, with c24 = W8 + s0(W9) + W17
- W26 = s1(W24) + c26, with c26 = W10 + s0(W11) + W19
- W27 = W13 + c2027, with c2027 = c20 + W11 + s0(W12) + s1(W25)
- W28 = s1(W26) + s0(W13) + W12 + W21
- W29 = s1(W27) + W22 + W13, since s0(W14) = s0(0) = 0

### 3.2 Group setup (charged 1 unit per group)

The setup computes W16..W19, W21, W23 and W25, and steps 0..12, both by the
same Sigma programs plus masks. It also computes step 13 without W13:
cA13 = T1' + T2 and cE13 = d + T1', where T1' = h + Sigma1(e) + Ch + K13. It
then forms these group constants (all register-resident, (C2)):

- bOc14 = A12 | A11, bAc14 = A12 & A11, fg14 = E12 ^ E11, g14 = E11,
  hKW14 = E10 + K14 and d14 = A10;
- c15 = A12, g15 = E12, hKW15 = E11 + K15 + W15 and d15 = A11;
- hKW16 = E12 + K16 + W16 and d16 = A12;
- KW_i = K_i + W_i for i = 17, 18, 19, 21, 23 and 25;
- c20, c20K = c20 + K20, c22, c24, c26, K22, K24, K26, c2027,
  c2027K = c2027 + K27, c28K = W12 + W21 + K28 and c29K = K29.

That is 32 constants. Lazy constants are exact under Lemma 1. The evaluator
counts 606 operations for the setup, with the IV and W0..W12 treated as data.
Drawing and storing two words, unpacking 13 words (shift and mask each), the
group loop and resetting w add at most 40 more. So the setup is at most
646 < 2224 operations, charged 1 unit per group: 2^104 units, a 2^-22 fraction
of T.

### 3.3 Per-message body: 532 counted operations

This is the exact program. It is `body()` in `experiments/grouped_r32.py`. `&M`
is one AND, and S1, S0, s1, s0 are Lemma 2 (7 each). Lazy values are marked ~.

```
A13 = (cA13 + w)&M ; E13 = (cE13 + w)&M                         4
w20 = (c20 + w)&M ; KW20~ = c20K + w                            3
w22 = (c22 + s1(w20))&M ; KW22~ = K22 + w22                     10
w24 = (c24 + s1(w22))&M ; KW24~ = K24 + w24                     10
w26 = (c26 + s1(w24))&M ; KW26~ = K26 + w26                     10
w27 = (c2027 + w)&M ; KW27~ = c2027K + w                        3
KW28~ = s1(w26) + s0(w) + c28K                                  16
KW29~ = s1(w27) + w22 + (w + c29K)                              10
step 14: T1~ = S1(e) + (g14 ^ (e & fg14)) + hKW14              11
         A14 = (T1 + (S0(a) + ((a & bOc14) | bAc14)))&M         12
         E14 = (T1 + d14)&M                                     2
step 15: T1~ = S1(e) + (g15 ^ (e & (f ^ g15))) + hKW15          12
         x = a ^ b ; A15 = (T1 + (S0(a) + (b ^ (x & (b ^ c15)))))&M   14
         E15 = (T1 + d15)&M                                     2
step 16: T1~ = S1(e) + (g ^ (e & (f ^ g))) + hKW16              12
         x' = a ^ b ; A16 = (T1 + (S0(a) + (b ^ (x' & x))))&M   13
         E16 = (T1 + d16)&M                                     2
steps 17..28 (each): T1~ = S1(e) + (g ^ (e & (f ^ g))) + h + KW_i      13
         x' = a ^ b ; A_i = (T1 + (S0(a) + (b ^ (x' & x))))&M   13
         E_i = (T1 + d)&M                                       2
step 29: as steps 17..28, but E29~ = T1 + d is left unmasked    27
D30'~ = S0(A29) + (A28 ^ ((A29 ^ A28) & x)) + ~A26              13
K = A28<<96 | E28<<128 | A29<<160 | (E29&M)<<192 | D30'<<224    10
```

In each step x is the previous step's a ^ b, which is this step's b ^ c, and
Maj(a,b,c) = b ^ ((a ^ b) & (b ^ c)). At step 14, b and c are constants, so
Maj = (a & (b|c)) | (b&c). At step 15, c is a constant.
Ch(e,f,g) = g ^ (e & (f ^ g)). At step 14, f ^ g is a constant.

Total: 4 + 3 + 10 + 10 + 10 + 3 + 16 + 10 = 66 for step 13 and the schedule;
25 + 28 + 27 = 80 for steps 14..16; 12 * 28 = 336 for steps 17..28; 27 for
step 29; 13 for D30'; and 10 for packing. That is 532. Masks: A_i and E_i are
Sigma and Ch inputs and are masked (Lemma 1, case i). w20..w27 are sigma
inputs. A28, E28 and A29 are non-top key fields that are already masked. E29
is masked in the packing. D30' is the top field and needs no mask.

Exactness. Every lazy value is a sum or bitwise combination of correct-low-32
values (Lemma 1), and every Sigma or sigma input is masked (Lemma 2). The
evaluator runs `body()` with a 256-bit counting word type: every group constant
and w is a counted word, so no operation goes uncounted. It returns 532 on every
input. On 5004 inputs (5000 random (prefix, y) and the four corners: all-zero
or all-one prefix with y = 0 or 2^24 - 1), the key fields of K matched
`verifier/hash_functions.digest(m, "sha256", 32)` bit for bit: A28, A29, E28 and
E29 equal H3, H2, H7 and H6 minus IV, and D30' + 1 equals (H1 - IV1) - (H5 - IV5).
These are our own checks. Organizer-run checks are described in Section 8.

### 3.4 The key

Lemma 3. D30 := A30 - E30 = T2_30 - A26 mod 2^32, where
T2_30 = Sigma0(A29) + Maj(A29, A28, A27). The program forms
D30' = T2_30 + ~A26 = D30 - 1 mod 2^32, since ~A26 = -A26 - 1.

Proof. Step 30 has d = A26, so A30 = T1 + T2_30 and E30 = A26 + T1. Subtracting
gives the result, and T1 (with W30, Sigma1(E29), Ch and h = E26) cancels.

Hence Key(m) = (A28, A29, E28, E29, D30') =
(H3 - IV3, H2 - IV2, H7 - IV7, H6 - IV6, (H1 - IV1) - (H5 - IV5) - 1) is a
fixed function of the digest. Equal digests give equal 160-bit keys. The key
skips step 31, W30, W31, all of T1 at step 30 (W30, sigma1(W28), Sigma1(E29), Ch)
and the feed-forward. The leader keeps A30 and E30 separately and pays for the
whole of step 30.

## 4. Table step and per-message total

S is never initialised, and D[j] holds the key of message j for every j < m.
Word-addressed:

```
idx = K >> 116                           1   top 140 key bits
p = Sbase + idx ; s = load [p]           2
if s >= m goto INS (compare, branch)     2   uninitialised or stale-out-of-range slot
q = Dbase + s ; k2 = load [q]            2
if k2 == K goto MATCH (compare, branch)  2
INS: store [r] = K ; store [p] = m       2   r = Dbase + m
     m = m + 1 ; r = r + 1               2
```

The worst path costs 13. Every message writes D[m] = K and makes S[idx] point to
itself, so a slot always holds the latest message with that index.

Correctness. D[0..m-1] are always written, so any s < m read from S, garbage or
not, names a real earlier message with key D[s]: a MATCH is a true key-equal
pair (s, m), s < m, and garbage never yields a false output (outputs are checked
with whole compressions). So the Briggs-Torczon back-pointer check and the id
store are unnecessary. A pair (u, v) is missed only if some w with u < w < v and
idx(w) = idx(u) overwrote the slot: event F2, bounded in Section 7.

Loop control is w = w + 0x100, a compare with the end value and a branch: 3.
Per message: 532 + 13 + 3 = 548 counted, charged 552 (4 spare, for example for
a register move a reviewer may count).

Registers (64). These are the 32 group constants; M, 0x100, w, its end value,
Sbase, Dbase, m and r (8); and at most 20 live temporaries (a liveness trace of
the program in Section 3.3 in the order written, with K kept live). That is
60 <= 64. The table step needs 6 temporaries, after the body's temporaries are
dead. The counter v and its cap are in memory and touched only on MATCH.

## 5. Verification and output correctness

On MATCH the program loads v, increments it, stores it, compares it with the
cap and branches (5). It splits s into gid and y (2), loads G[gid] (3), and
unpacks both 13-word prefixes (2 * 26). It forms both W13 words (4) and
compares the 14 free words (28). If they are equal, it treats the match as
failed. Otherwise it computes both digests with two whole reference
compressions (2 units) and compares 8 words (16). On success it writes the pair
(28 stores). That is at most 140 < 2224 operations besides the two
compressions, so 3 units per MATCH suffice. On failure, control goes to INS.

A pair is output only if the messages differ and all 256 digest bits agree, so
every output is a valid sha256-r32 collision of distinct 55-byte messages. This
holds independently of H1.

## 6. Time, memory and preprocessing

T <= N * 552/2224 + 2^104 * 1 + 3 * 2^110 + 1 (initialising m, r, v and the
bases). Here N * 552/2224 = 0.2482014 * 2^128. The other terms are relative
fractions 2.4e-7 and 4.6e-5 of it. So

log2 T <= 125.989650 < 125.990.

The cap holds for every run, because v is enforced in Step 2b.

Memory: S takes 2^140 words of 32 bytes (2^145 bytes, allocated and never
initialised). D takes 2^128 * 32 = 2^133 bytes, and G takes 2^104 * 64 = 2^110
bytes. The total is below 2^146 bytes. Preprocessing and advice are 0.
Uninitialised allocation is free in this RAM model, as in 6b88bdb7.

## 7. Success probability

Fix the coins (2^104 independent uniform 416-bit prefixes). The run succeeds if
some colliding pair u < v (equal 256-bit digests, distinct messages) has no
message w with u < w < v and idx(w) = idx(u), and the cap is not exceeded. When
v arrives, S[idx(v)] = u, D[u] = Key(u) = Key(v) (Lemma 3), so v gets MATCH and
verification succeeds, unless the run already succeeded. Failure needs one of:

- F1: no colliding pair among the N digests;
- F2: every colliding pair (u, v) has some w with u < w < v and idx(w) = idx(u);
- F3: two groups drew the same 416-bit prefix;
- F4: more than 2^110 MATCH events.

Under H1 (digests independent uniform 256-bit values, so keys are 160 of their
bits and indices 140):

- Pr[F1] = prod_{i<N} (1 - i/2^256) <= exp(-N(N-1)/2^257) < 0.6065307.
- Pr[F2 and not F1] <= sum over w, u, v (u < w < v) of Pr[idx(w) = idx(u)] *
  Pr[D(u) = D(v)] <= (N^3/6) * 2^-140 * 2^-256 = 2^-12/6 < 4.07e-5.
- Pr[F4] <= E[#MATCH]/2^110. Each MATCH is a distinct pair (s, m) with equal
  160-bit keys, at most one per m, so E <= (N^2/2) * 2^-160 = 2^95 and
  Pr[F4] <= 2^-15 < 3.06e-5 (Markov).
- Pr[F3] <= C(2^104, 2) * 2^-416 < 2^-208. This is exact and needs no heuristic.
  Messages with the same gid differ in y.

So Pr[success] >= 1 - 0.6065307 - 0.0000407 - 0.0000306 - 2^-208 > 0.39339.
We claim 0.39, an explicit 0.0034 allowance, as in 6b88bdb7.

### 7.1 Heuristic H1

H1: for F1, F2 and F4, the 2^128 grouped digests behave like independent
uniform 256-bit values, up to a negligible amount. Reasons:

1. All but a 2^-104 fraction of pairs are cross-group pairs. Their prefixes are
   independent and uniform, and they pass 13 full steps before W13 enters. For
   a same-y cross-group pair, Cauchy-Schwarz gives
   Pr[D(u) = D(v)] = sum_h Pr[D(p,y) = h]^2 >= 2^-256.
2. Within a group, messages differ only in 24 bits of W13, followed by 19
   further steps and 9 W13-dependent schedule words (W20, W22, W24 and
   W26..W31). The low byte of W13 is the constant 0x80, so A13 and E13 share
   their low 8 bits within a group (the single-group experiment targets this).
   If within-group pairs never collided, Pr[F1] would grow by a factor of only
   1 + 2^-104.
3. H1 is the random-function premise of every generic 256-bit collision bound
   and of jaazinn's accepted grouped packages with the same groups. By Lemma 3
   a uniform digest gives a uniform key.

Score sensitivity: multiplying N by 1.0108 (+0.0155 in log2 T) lifts the model
success to about 0.3998. Any success shortfall below 0.39 could be repaired by
two independent runs, at most +1.0 in log2 T.

## 8. Evidence

Declared experiments (`experiments/manifest.json`, program
`experiments/grouped_r32.py`, organizer-executed). Both run a scaled copy of
Section 2 on the exact target with 55-byte messages, prefixes from SHAKE-256 of
the organizer seed, y from 0 and N_t = 2^10, so N_t^2/2^20 = 1 = N^2/2^256.
Every message is evaluated only by `body()`. The table keeps the latest message
per scaled key (as in Section 4). Each key match is checked with two plain full
compressions against the whole 20-bit mask, and the first verified pair ends
the trial. For y = 0 of every group and on every key match, the program reruns
setup and body with the counting word type. It compares the counted body with
the fast body and with a plain full compression bit for bit, and reports
body_ops_min/max (expected 532), setup_ops_max (606), evaluator_checks and
evaluator_mismatches (expected 0).

- `sha256r32-v2-spread`: 32 groups x 32 y. The mask has 16 bits on H2, H3, H6
  and H7, bit 0 on both H1 and H5, and one bit each on H0 and H4. The scaled
  key is the 16 bits plus bit 0 of D30' (equal masked H1 and H5 bits give an
  equal D30 bit 0, because borrows only move upward).
- `sha256r32-v2-single-group`: one group, y = 0..1023, with a different mask:
  14 bits on H2, H3, H6 and H7, bits 0..1 on H1 and H5 (key gets D30' bits
  0..1), and one bit each on H0 and H4.

Model value. With random digests a new message hits a stored scaled key with
probability d/2^k (d distinct keys stored). A hit succeeds with probability
2^-e (the e mask bits outside the key), and otherwise the slot is overwritten
without changing d. A miss inserts and increments d. An exact dynamic
program over d gives 0.392582 (k = 17, e = 3, spread) and 0.391796 (k = 16,
e = 4, single group). The plain 20-bit birthday value is 0.393272. With 256
trials one standard error is 0.0305.

Our checks (local, not organizer evidence):

| run | trials | successes (model) | z |
| --- | ---: | --- | ---: |
| spread, emulated organizer runner, public seed | 256 | 117 (100.5) | +2.11 |
| single group, emulated organizer runner, public seed | 256 | 97 (100.3) | -0.42 |
| spread, own seeds | 4096 | 1556 (1608.0) | -1.66 |
| single group, own seeds | 4096 | 1621 (1604.8) | +0.52 |
| spread, all 4352 trials above | 4352 | 1673 (1708.5) | -1.10 |

In the emulated runs every key-match pair and every y = 0 message was
rechecked. Spread reported 7519 checks and single group 1793, all with
body_ops 532, setup_ops 606 and 0 mismatches. Every returned pair passed the
runner's own mask check. Each layout took 3.6 to 5.5 s per 256 trials (Python
3.9, one core), within the 20 s budget. Within-group structure at a larger
scale: in 10 groups of 2^17 consecutive y each, the 29-bit projection
(D30' bits 0..12, A28 and E29 bits 0..7) gave 154 colliding pairs against
160.0 expected (z = -0.47).

## 9. Sensitivity and disclosure

Each operation per message adds about 0.0026 to log2 T.

| reading | charged per message | log2 T |
| --- | ---: | ---: |
| claimed (Lemma 2 Sigma, lazy masks) | 552 | 125.990 |
| all 32 group constants reloaded every message (+32 loads) | 584 | 126.071 |
| the same, plus a base+offset add for each load | 616 | 126.148 |
| rotations as shr, shl, or of a reduced word (3 operations, output left lazy) | 696 | 126.324 |
| jaazinn's exact 4-operation rotation (shr, shl, or, and) | 807 | 126.538 |
| leader 6b88bdb7 (192-bit key, 4-operation rotation) | 900 | 126.695 |

The rotation rows change only Sigma and sigma. They give 11 and 9 operations
(3-operation rotation) or 14 and 11 (4-operation rotation), against 7 and 7.
There are 33 Sigma and 6 sigma calls, so they add 144 and 255 operations, with
the same structure, key and table. Every row is below the leader.

Disclosure (C4). With the same Lemma 2 programs and lazy masks, a white-box
whole 32-step compression (schedule W16..W31, 32 steps and the feed-forward)
costs 1233 operations, or 0.554 C. We checked it against `digest(m, "sha256", 32)`
on 1000 random messages. The leader's accepted figure is 1840 operations
(0.83 C). The difference is Lemma 2, which uses only the listed primitives with
immediate counts. Every whole compression we call is charged a full unit. If
a reviewer rejects Lemma 2, the fallbacks are 126.324 (3-operation rotation,
Lemma 1 only) and 126.538 (jaazinn's exact 4-operation rotation).

## 10. Limitations

- H1 is a heuristic and is not proved. The experiments test 20-bit masked
  analogues at N_t = 2^10, and a 29-bit projection at 2^17 within one group.
  They cannot exclude structure that appears only at full width or at 2^128
  messages. The organizer seeds are public.
- The 0.0034 allowance between 0.39339 and 0.39 is a judgement, not a
  certified margin.
- Memory (about 2^145 bytes) far exceeds a distinguished-point walk's. It is
  unscored under v5, and this is not a Pareto improvement.
- The 64-register machine follows 6b88bdb7; stricter readings are in Section 9.
- No full-scale execution or stored collision is claimed. No improvement over
  the nominal reference identifier is asserted; that identifier is metadata.
