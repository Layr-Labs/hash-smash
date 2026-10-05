# sha256-r32: 4-lane grouped birthday search, time_log2 = 124.60

This package is a generic birthday search. It is not a differential or algebraic
attack and it claims no weakness of SHA-256. The scalar is below 128 only
because each message is charged about 0.088 of a 32-step compression.

The construction starts from winglock's awaiting-review package 68ca8e4f
(125.990), which itself extends jaazinn's package 6b88bdb7 (126.695). Both are
unpromoted. Their single-block grouping, 160-bit digest key, uninitialised
sparse table, immediate shift counts and 64-register machine are reused.
What is new is Section 3: four messages share each arithmetic instruction of
the per-message body, in one 256-bit word, under the collision-frontier-v5
word RAM. jaazinn and winglock are co-authors of that reused construction.

## 0. Claim

| quantity | value |
| --- | --- |
| target | sha256-r32-prefix-v1, steps 0..31, fixed IV, feed-forward, 256-bit digest |
| cost model | collision-frontier-v5, C = 2224 |
| messages N | 2^128 = 2^104 groups x 2^24 values of y, in batches of 4 |
| packed body, machine-counted | 563 operations for 4 messages |
| extract, pack, table, loop | 71 + 52 + 3 = 126 operations for 4 messages |
| counted per message | 689/4 = 172.25 |
| charged per message | 196 (23.75 spare) |
| time T | <= 2^128 * 196/2224 + 2^104 + 3*2^110 + 1 < 2^124.5 |
| claimed time_log2 | 124.60 |
| success probability | >= 0.39 under heuristic H1 (model value 0.39339) |
| memory | < 2^146 bytes, reported only |
| preprocessing, advice | 0, 0 |

The time bound is a worst-case cap on every run. Every output is checked with
two whole reference compressions. Only the success probability uses H1.
The nominal identifier sha256-r32-nominal-v2 is metadata, not a baseline.

## 1. Target, machine and counting

### 1.1 Target

The target is `verifier/hash_functions.py:digest(m, "sha256", 32)`: steps
i = 0..31, the standard schedule, then feed-forward. A_i and E_i are the new
a and e produced by step i. Step i reads a, b, c, d = A_{i-1}..A_{i-4} and
e, f, g, h = E_{i-1}..E_{i-4}, computes
T1 = h + Sigma1(e) + Ch(e, f, g) + K_i + W_i and T2 = Sigma0(a) + Maj(a, b, c),
and sets A_i = T1 + T2, E_i = d + T1, mod 2^32. The final state is
(A31, A30, A29, A28, E31, E30, E29, E28). H_j = IV_j + state_j mod 2^32.

Every message is 55 bytes. The single padded block is W0..W12 (the 52-byte
group prefix), W13 = (y << 8) | 0x80, W14 = 0 and W15 = 440.

### 1.2 Machine

The model is a classical probabilistic 256-bit word RAM. One target
compression costs 1. Every other primitive costs 1/2224: a 256-bit load or
store, addition or subtraction mod 2^256, AND, OR, XOR, NOT, a shift, a
comparison, a branch, or one fresh uniform 256-bit word. Shift counts are
immediates. There are 64 registers. This is the same machine accepted in
6b88bdb7 and used by 68ca8e4f.

A packed instruction is still one primitive. The model prices
"addition/subtraction modulo 2^256", not a 32-bit addition. Encoding four
independent 32-bit sums into one 256-bit addition does not multiply the price,
any more than a 256-bit shift used to rotate a 32-bit lane costs more than one
shift. Section 3 proves the lanes do not interfere, so the results are the
four scalar results.

### 1.3 Inherited conventions

- Sigma and sigma use the doubling formulas of 68ca8e4f, plus one AND with the
  lane mask M4 so the output guards are clear (Section 3.2). Each is 8
  operations on a guard-clean input.
- Ch(e, f, g) = g ^ (e & (f ^ g)). Maj(a, b, c) = b ^ ((a ^ b) & (b ^ c)),
  and the previous step's a ^ b is this step's b ^ c.
- Values are reduced mod 2^32 only where Section 3 requires it. Low 32 bits of
  a sum of guard-clean words are the independent lane-wise sums.
- Group setup is charged 1 unit per group. Each key match is confirmed with
  two whole reference compressions, charged 3 units, and the number of matches
  is capped at 2^110.
- The table step is the 13-operation step of 68ca8e4f Section 4, run once per
  message after that message's key has been packed.

## 2. Algorithm

State: G[2^104] holds two random words per group; S[2^140] is an uninitialised
sparse index; D[2^128] holds one packed key per message; m is the message
counter; r = Dbase + m; v counts key matches.

1. For gid = 0 .. 2^104 - 1: draw two fresh uniform 256-bit words, store them
   in G[gid], unpack W0..W12 from their first 416 bits, and run the group setup
   (Section 4.1). Set the packed message word w to INIT_W, whose lanes are
   W13 for y = 0, 1, 2, 3.
2. For batch = 0 .. 2^22 - 1:
   a. Run the packed body (Section 4.2). It returns five packed words.
   b. For lane i = 0, 1, 2, 3, in that order: extract the five key fields,
      pack the 160-bit key, and run the table step. On MATCH, increment v and
      fail if v > 2^110. Otherwise rebuild the two messages and accept them
      only if they differ and both full digests are equal. A non-confirming
      match falls through to the store.
   c. If w equals the last-batch word, stop the group. Otherwise w = w + STEP.
3. If all N messages are processed without success, fail.

Message index m = gid * 2^24 + y. Record s names its message by
gid = s >> 24 and y = s & (2^24 - 1). Within a batch the four keys are
computed before any of them is stored, then stored from lane 0 to lane 3, so
a later lane can match an earlier lane of the same batch.

INIT_W = 0x80 | (0x180 << 64) | (0x280 << 128) | (0x380 << 192).
STEP = 0x400 in each lane. Lane 0 of w starts at 0x80 and increases by 0x400.
After 2^22 - 1 additions it is 0x80 + (2^22 - 1) * 0x400 = 2^32 - 0x380 < 2^32.
Lane 3 starts at 0x380 and ends at 2^32 - 0x80 < 2^32. So w stays guard-clean
with no per-batch mask. The last y in lane 0 is 2^24 - 4, and
W13 = ((2^24 - 4) << 8) | 0x80, which is that final lane-0 value.

## 3. Four-lane isolation

### 3.1 Packing

Lane i occupies bits 64i .. 64i+63. Its data field is bits 64i .. 64i+31 and
its guard is bits 64i+32 .. 64i+63. M4 has bits 64i .. 64i+31 set for
i = 0, 1, 2, 3 and every other bit clear. A word is guard-clean when it equals
its AND with M4.

### 3.2 Sigma on a guard-clean word

For guard-clean x and 0 < k < 32, z = x | (x << 32) copies lane i's data into
bits 64i+32 .. 64i+63 and does not enter lane i+1: the source bits are
64i .. 64i+31, and 64i+31+32 = 64i+63 is the last guard bit. Lane 3's copy
lands in bits 224 .. 255 and does not fall off the 256-bit word.

The formulas, then masked by M4, are:

```
Sigma1(x) = ((z ^ z>>5  ^ z>>19) >> 6)  & M4
Sigma0(x) = ((z ^ z>>11 ^ z>>20) >> 2)  & M4
sigma1(x) = ((((z ^ z>>2)  >> 7) ^ x) >> 10) & M4
sigma0(x) = ((((z ^ z>>11) >> 4) ^ x) >> 3)  & M4
```

For Sigma1, result data bit 64i+j, j <= 31, is read from source bits
64i+j+6, 64i+j+11 and 64i+j+25 of z. The highest source is bit 64i+56.
That bit is inside lane i's doubled copy (which ends at bit 64i+63), so it
does not depend on lane i+1. Lane 3's highest source is bit 248 < 256.
sigma1's highest source offset is 19 and sigma0's is 18; both are inside the
doubled copy. The final AND with M4 clears every guard. Each formula is 8
operations: two to build z, five to combine the shifts, and one mask.
No native rotation is used.

### 3.3 Additions do not cross lanes

Bitwise AND, OR and XOR of guard-clean words are guard-clean and act
independently on each data field. NOT is not used on a packed word.

A guard-clean word is < 2^32 in each lane. The sum of t such words is
< t * 2^32, so it occupies at most the data field plus floor(log2(t-1))+1
guard bits, and it does not reach bit 64 of that lane. The longest unmasked
add chain in the body is four terms (T1 = Sigma1 + Ch + h + KW, each
guard-clean after Section 3.2 and the stored-state masks). Four terms need
only 2 guard bits. The next lane starts 32 guard bits away. No carry enters
the next data field.

This is why every Sigma and sigma output is masked before it is added, and
why A_i and E_i are masked before they are reused, except E29, which is never
added after it is formed. E29 and D30 are masked when their lanes are
extracted. The same bound applies to the schedule sums KW28 and KW29, which
add at most three guard-clean terms.

### 3.4 Sentinel subtraction

D30 = A30 - E30 = T2_30 - A26 mod 2^32, because step 30 has d = A26,
A30 = T1 + T2_30 and E30 = A26 + T1. T1 cancels. T2_30 depends only on
A29, A28 and A27, so W30, W28, Sigma1(E29), Ch and h are never formed.

SENT has bit 64i+63 set and every other bit clear. For guard-clean a, b:

```
D = ((a | SENT) - b) mod 2^256
```

has lane i's data field equal to a_i - b_i mod 2^32.

Proof. b = b & M4 is < 2^224, because its top data field ends at bit 223 and
its top guard is clear. a | SENT has bit 255 set, so a | SENT >= 2^255 > b.
The subtraction does not wrap modulo 2^256. Inside lane i, if a_i >= b_i there
is no borrow and the data field is a_i - b_i. If a_i < b_i, the borrow
propagates through the zero guards at bits 64i+32 .. 64i+62 and is absorbed
by the sentinel at bit 64i+63. It does not borrow from bit 64(i+1). The data
field is the modular difference. Lane 3's sentinel is bit 255; absorbing the
borrow there does not wrap, by the inequality above.

The program uses a = T2 & M4 and b = A26 & M4. Both are guard-clean. The low
32 bits of each lane are therefore D30.

### 3.5 The key is a function of the digest

Key = (A28, A29, E28, E29, D30) =
(H3 - IV3, H2 - IV2, H7 - IV7, H6 - IV6, (H1 - IV1) - (H5 - IV5)),
all mod 2^32. Equal digests give equal keys. A uniform digest gives a uniform
160-bit key: H2, H3, H6 and H7 are uniform and independent of the uniform
difference (H1 - IV1) - (H5 - IV5), which takes each 32-bit value exactly
2^32 times as (H1, H5) varies. H0 and H4 do not appear.

The packed key word is

```
K = (A28 << 96) | (E28 << 128) | (A29 << 160) | (E29 << 192) | (D30 << 224)
```

idx = K >> 116 is 140 specific bits of this uniform key (A28 bits 20..31, then
E28, A29, E29 and D30), hence uniform under H1.

## 4. Program

### 4.1 Group setup, charged 1 unit

With W0..W12 fixed, steps 0..12 and W16, W17, W18, W19, W21, W23, W25 are
group constants. W13 enters step 13 only additively, and it enters the
schedule only through W20, W22, W24, W26, W27, W28 and W29. The setup computes
the scalar constants below and splats each into all four lanes
(x | (x << 64) | (x << 128) | (x << 192), six operations):

- cA13, cE13: step 13 without W13, so A13 = (cA13 + W13) and E13 = (cE13 + W13)
- bOc14 = A12 | A11, bAc14 = A12 & A11, fg14 = E12 ^ E11, g14 = E11,
  hKW14 = E10 + K14, d14 = A10
- c15 = A12, g15 = E12, hKW15 = E11 + K15 + W15, d15 = A11
- hKW16 = E12 + K16 + W16, d16 = A12
- KW_i = K_i + W_i for i in {17, 18, 19, 21, 23, 25}
- c20, c20K, c22, K22, c24, K24, c26, K26, c2027, c2027K, c28K, c29K,
  with the same pre-additions as 68ca8e4f Section 3.1

That is 32 constants. A direct Word-counter run of this scalar setup plus the
32 splats, with W0..W12 and the IV presented as data, is 862 operations.
Drawing and storing two words, unpacking 13 words, setting w = INIT_W and the
group-loop test are under 40 more. The total is under 1000 < 2224, so 1 unit
per group is a valid charge: 2^104 units.

### 4.2 Packed body: 563 operations for four messages

S1, S0, s1 and s0 are Section 3.2 (8 each). M4-masks are one AND. The program
is `body4` in `experiments/grouped_swar.py`.

```
A13 = (cA13 + w) & M4 ; E13 = (cE13 + w) & M4          4
w20 = (c20 + w) & M4 ; KW20 = c20K + w                 3
w22 = (c22 + s1(w20)) & M4 ; KW22 = K22 + w22          2 + 8
w24 = (c24 + s1(w22)) & M4 ; KW24 = K24 + w24          2 + 8
w26 = (c26 + s1(w24)) & M4 ; KW26 = K26 + w26          2 + 8
w27 = (c2027 + w) & M4 ; KW27 = c2027K + w             3
KW28 = s1(w26) + s0(w) + c28K                          2 + 16
KW29 = s1(w27) + w22 + (w + c29K)                      3 + 8
step 14: T1 = S1(e) + (g14 ^ (e & fg14)) + hKW14       4 + 8
         A14 = (T1 + (S0(a) + ((a & bOc14) | bAc14))) & M4    5 + 8
         E14 = (T1 + d14) & M4                          2
step 15: T1 = S1(e) + (g15 ^ (e & (f ^ g15))) + hKW15   5 + 8
         x = a ^ b                                      1
         A15 = (T1 + (S0(a) + (b ^ (x & (b ^ c15))))) & M4    6 + 8
         E15 = (T1 + d15) & M4                          2
step 16: T1 = S1(e) + (g ^ (e & (f ^ g))) + hKW16       5 + 8
         x = a ^ b ; A16 uses xprev as b ^ c            1 + 5 + 8
         E16 = (T1 + d16) & M4                          2
steps 17..28, each: T1 = S1(e) + Ch + E_{i-4} + KW     6 + 8
         x = a ^ b ; A_i from S0 and xprev              1 + 5 + 8
         E_i = (T1 + d) & M4                            2
step 29: same arithmetic, but E29 = T1 + d is unmasked  13 + 16
D30: x = A29 ^ A28                                      1
     T2 = S0(A29) + (A28 ^ (x & xprev))                 3 + 8
     D30 = ((T2 & M4) | SENT) - (A26 & M4)              4
```

Sigma/sigma calls: five s1, one s0, sixteen S1 and seventeen S0, each 8
operations, total 312. The remaining operations listed above total 251.
312 + 251 = 563. The Word counter in the experiment returns 563 on every
input, including the four corners of the prefix and of y. On those inputs,
and on 30 further random groups, every lane matched
`digest(m, "sha256", 32)` in all five key fields. The organizer rechecks the
first batch of every group and every key match (Section 8).

Steps 16..29 are a fixed 14-iteration straight-line program in the RAM
accounting above. Charging 3 extra operations of loop control on each of
those 14 iterations would add 42 operations per batch, 10.5 per message,
which still fits in the spare of Section 6.

### 4.3 Extract, pack and table

Lane 0 is already in bits 0..31. Each of its five fields is one AND with
2^32-1, then the pack below, 14 operations. Lane i in {1, 2, 3} is
`(word >> 64i) & M32` per field, 10 operations, plus the same pack, 19
operations. Three such lanes cost 57. Extract-and-pack for the batch is
14 + 57 = 71.

```
K = (A28 << 96) | (E28 << 128)
K = K | (A29 << 160)
K = K | (E29 << 192)
K = K | (D30 << 224)
```

The table step, word-addressed, is exactly 68ca8e4f's, worst path 13:

```
idx = K >> 116
p = Sbase + idx ; s = load [p]
if s >= m goto INS
q = Dbase + s ; k2 = load [q]
if k2 == K goto MATCH
INS: store [r] = K ; store [p] = m
     m = m + 1 ; r = r + 1
```

Four messages cost 52. The batch loop is one addition of STEP, one comparison
and one branch, 3 operations. Per batch: 563 + 71 + 52 + 3 = 689.
Per message: 172.25. We charge 196, a spare of 23.75 operations per message
(95 per batch).

Registers. The 32 splatted constants, M4, STEP, w, Sbase, Dbase, m, r and the
end word are 38. The body has at most 20 live temporaries, the same liveness
as 68ca8e4f, and the table step reuses those temporaries after the body
returns. That is at most 58 <= 64. SENT overwrites a dead temporary at D30.
The match counter v lives in memory and is touched only on MATCH.

## 5. Verification

On MATCH the program does the same work as 68ca8e4f Section 5: update v (5),
split s (2), load and unpack both prefixes (3 + 52), form both W13 words (4),
compare the 14 free words (28), and on inequality compute two reference
digests (2 units) and compare 8 words (16). Output stores are 28. At most
140 < 2224 ordinary operations plus two compressions, so 3 units per MATCH
suffice. A pair is returned only when the messages differ and all 256 digest
bits agree. That does not use H1.

## 6. Time, memory and preprocessing

T <= N * 196/2224 + 2^104 + 3 * 2^110 + 1.
Let U = 2^128 * 196/2224 + 2^104 + 3*2^110 + 1 and C = 2224.
Then C*U = 2^128 * 196 + C*(2^104 + 3*2^110 + 1).
U < 2^124.5 if and only if (C*U)^2 < C^2 * 2^249, because both sides are
positive. That integer comparison holds: the right side is larger by a factor
of about 1.0056. Therefore U < 2^124.5 < 2^124.60, which is the claimed bound.
The cap holds on every run because v is enforced.

The same comparison with 210 in place of 196 still gives log2 about 124.595,
so a reconstruction up to 210 operations per message remains under 124.60.
The counted figure is 172.25.

Memory is unchanged from 68ca8e4f. S is 2^140 words, 2^145 bytes, allocated
and never initialised. D is 2^133 bytes and G is 2^110 bytes. The total is
below 2^146 bytes. Uninitialised allocation is free in this RAM model, as in
that package. Preprocessing and advice are 0.

## 7. Success probability

Fix the 2^104 independent uniform 416-bit prefixes. The run succeeds if some
colliding pair u < v has no w with u < w < v and idx(w) = idx(u), and the cap
is not exceeded. When v arrives, S[idx(v)] = u and D[u] = Key(u) = Key(v), so
verification succeeds unless an earlier pair already did. Failure needs one of:

- F1: no colliding pair among the N digests;
- F2: every colliding pair is overwritten in its 140-bit slot;
- F3: two groups drew the same 416-bit prefix;
- F4: more than 2^110 MATCH events.

Under H1 (the N digests are independent uniform 256-bit values, so keys and
indices are the uniform images in Section 3.5):

- Pr[F1] = prod_{i<N} (1 - i/2^256) <= exp(-N(N-1)/2^257) < 0.6065307.
- Pr[F2 and not F1] <= (N^3/6) * 2^-140 * 2^-256 = 2^-12/6 < 4.07e-5.
- Pr[F4] <= E[#MATCH]/2^110 <= (N^2/2) * 2^-160 / 2^110 = 2^-15.
- Pr[F3] <= C(2^104, 2) * 2^-416 < 2^-208, with no heuristic. Messages in one
  group differ in y.

So Pr[success] > 0.39339. The claim is 0.39, an explicit 0.0034 allowance.
Batches do not change the bound: every pair is still stored in order, and a
pair is missed only by the overwrite event F2.

### 7.1 Heuristic H1

H1: for F1, F2 and F4, the 2^128 grouped digests behave like independent
uniform 256-bit values, up to a negligible amount. Reasons:

1. All but a 2^-104 fraction of pairs are cross-group pairs with independent
   uniform prefixes. They pass 13 full steps before W13 enters.
2. Within a group, messages differ only in 24 bits of W13, then 19 further
   steps. If those pairs never collided, Pr[F1] would grow by a factor of only
   1 + 2^-104. The low byte of W13 is the constant 0x80, so A13 and E13 share
   their low 8 bits inside a group. The single-group experiment targets this.
3. H1 is the random-function premise of every generic 256-bit collision bound,
   and it is the premise of the two grouped packages this one extends. Section
   3.5 gives uniformity of the key and the index once the digest is uniform.

Score sensitivity: multiplying N by 1.0108 adds 0.0155 to log2 T and lifts the
model success to about 0.3998. Two independent runs would repair any shortfall
below 0.39, at most +1.0 in log2 T.

## 8. Evidence

The declared experiments are `experiments/grouped_swar.py`. Both are scaled
copies of Section 2 on the exact target, with prefixes from SHAKE-256 of the
organizer seed and N_t = 2^10, so N_t^2/2^20 = 1 = N^2/2^256. Messages are
evaluated only by `body4`. The table keeps the latest message per scaled key
and inserts the four lanes in order. A key match is verified with two plain
compressions against the whole 20-bit mask. The first verified pair ends the
trial. The first batch of every group, and every key match, is recomputed with
the counting word type and compared lane by lane with a plain compression.
The observations body_ops_min and body_ops_max are expected to be 563, and
evaluator_mismatches is expected to be 0.

- `sha256r32-swar4-spread`: 32 groups x 32 y. The mask has 16 bits on H2, H3,
  H6 and H7, bit 0 on H1 and H5, and one bit each on H0 and H4. The scaled key
  is those 16 bits plus bit 0 of D30. Model value 0.3926, the same dynamic
  program as 68ca8e4f (k = 17, e = 3), because D30 bit 0 is the same equality
  predicate as that package's D' bit 0.
- `sha256r32-swar4-single-group`: one group, y = 0..1023, with 14 bits on
  H2, H3, H6 and H7, bits 0..1 on H1 and H5, and one bit each on H0 and H4.
  Model value 0.3918 (k = 16, e = 4).

Our checks, not organizer evidence: 30 random groups and the four corners
(zero and all-ones prefixes, y = 0 and y = 2^24-4) matched the trusted digest
in every lane, at 563 operations. A 32-trial local replay of each layout had
0 mismatches. Those replays are small and are not the organizer's seeds.

## 9. Sensitivity

| reading | charged per message | log2 T |
| --- | ---: | ---: |
| claimed, 196 | 196 | 124.60 |
| counted 172.25, rounded up | 173 | 124.32 |
| unrolled-step loop control added (42 per batch) | 184 | 124.40 |
| 2-lane fallback, 128-bit stride, no Sigma output mask, charge 304 | 304 | 125.13 |
| leader 68ca8e4f | 552 | 125.990 |

The 2-lane row is the same instruction stream with two lanes. A 128-bit stride
has 64 zero guards after a dirty Sigma output, so a carry cannot reach the
next lane even without the output mask. It still beats 125.990. It is not the
claimed algorithm. The claim is the 4-lane program at 196 operations per
message.

Reloading all 32 constants on every message, instead of keeping them in
registers, would add 32 loads per batch if they are splatted, or 128 if each
lane reloads its own copy. Even 128 extra operations per batch is 32 per
message, and 196 + 32 = 228 still has log2 about 124.71. We do not claim that
reading; the register machine is the one already used by 6b88bdb7. It is
recorded so the dependence is visible.

## 10. Limitations

- H1 is not proved. The experiments are 20-bit masked analogues at N_t = 2^10.
  They cannot exclude structure that appears only at full width or at 2^128
  messages. The organizer seeds are public. One standard error at 256 trials
  is about 0.03. The 0.0034 allowance is a judgement.
- Lane isolation is a finite bit-position argument, not a heuristic. A single
  counterexample lane would refute it. The organizer checks are the place that
  counterexample would appear. They do not, by themselves, price the attack.
- Memory is about 2^145 bytes. It is unscored and this is not a Pareto
  improvement over a constant-memory walk.
- No full-scale execution or stored collision is claimed. No improvement over
  the nominal reference identifier is asserted.
- The 64-register machine and the free uninitialised table are inherited from
  6b88bdb7 and 68ca8e4f. Section 9 records the stricter readings.
