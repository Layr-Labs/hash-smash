# A verified closed-form collision for 1-round BLAKE3 in 123 instructions

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is a
separately reported bound.

## 1. Claim

Target: `blake3-r1-prefix-v1`, ordinary collisions of complete messages, unkeyed
BLAKE3-256 with only round 0 kept in every compression.

A deterministic straight-line program of 123 instructions on the 256-bit word RAM
computes two distinct 64-byte messages M and M', evaluates the complete hash of
both, compares all 256 digest bits, checks that the messages differ, and halts.
It uses no search, no random coin, no heuristic and no stored collision.

- Two target compressions are charged, one for each verification hash: 2 units.
- Everything else is 121 primitive word operations at 1/C units, C = 222.
- The program is also charged one operation per instruction for placing its own
  code and two operations per table word for placing its constants. The cost
  model does not ask for this; it is included as a safety margin.

Total charged time is at most 2 + 254/222 = 3.1441 units, and log2(3.1441) =
1.6527. The claim is `time_log2 = 1.66`. Success probability is 1. Peak memory is
below 2^15 bytes. Section 9 lists the exact counts and Section 10 gives the same
count under other accounting conventions, including one under which this bound
does not hold.

## 2. The hash on 64-byte messages

A 64-byte message is one chunk with one full block. Its digest is the first eight
output words of one compression with chaining value IV, counter 0, block length
64 and flags CHUNK_START | CHUNK_END | ROOT = 11. There is no parent node and no
second compression. This matches `verifier/blake3.py:blake3(m, 1)`.

Decode the message into sixteen little-endian 32-bit words s[0..15]. The IV is

    IV0..IV3 = 6a09e667 bb67ae85 3c6ef372 a54ff53a
    IV4..IV7 = 510e527f 9b05688c 1f83d9ab 5be0cd19.

The state is v[0..7] = IV0..IV7, v[8..11] = IV0..IV3, v[12..15] = (0, 0, 64, 11).
All additions are modulo 2^32. ROTR and ROTL rotate a 32-bit word. G(a,b,c,d;x,y)
acts on four state words:

    a = a + b + x;   d = ROTR(d XOR a, 16)
    c = c + d;       b = ROTR(b XOR c, 12)
    a = a + b + y;   d = ROTR(d XOR a, 8)
    c = c + d;       b = ROTR(b XOR c, 7).

The single round is four column calls and then four diagonal calls:

    C0 = G(0,4,8,12; s0,s1)     C1 = G(1,5,9,13; s2,s3)
    C2 = G(2,6,10,14; s4,s5)    C3 = G(3,7,11,15; s6,s7)
    D0 = G(0,5,10,15; s8,s9)    D1 = G(1,6,11,12; s10,s11)
    D2 = G(2,7,8,13; s12,s13)   D3 = G(3,4,9,14; s14,s15).

The digest words are o[i] = v[i] XOR v[i+8] for i = 0..7, written little-endian.
No message permutation is applied because there is no second round.

Write F = ffffffff. Negation -u means 2^32 - u reduced modulo 2^32.

## 3. Two identities for G

**Lemma 1 (column).** Let (a,b,c,d) be any inputs. Put

    d1 = b - c,   a1 = d XOR ROTL(d1, 16),   x = a1 - a - b,
    A  = ROTL(-b, 8) XOR d1,                 y = A - a1.

Then G(a,b,c,d; x,y) = (A, 0, 0, -b).

Proof. Follow the eight assignments in order.

1. a becomes a + b + x = a1.
2. d becomes ROTR(d XOR a1, 16) = ROTR(ROTL(d1, 16), 16) = d1.
3. c becomes c + d1 = b.
4. b becomes ROTR(b XOR b, 12) = 0.
5. a becomes a1 + 0 + y = A.
6. d becomes ROTR(d1 XOR A, 8) = ROTR(ROTL(-b, 8), 8) = -b.
7. c becomes b + (-b) = 0.
8. b becomes ROTR(0 XOR 0, 7) = 0.

The output is (A, 0, 0, -b). No condition on the inputs is used.

**Lemma 2 (diagonal).** Let the inputs be (a, 0, 0, d), and let x = d - a. For any
y put g = y + d. Then

    G(a,0,0,d; x,y) = (g, ROTR(g, 15), ROTR(g, 8), ROTR(g, 8)).

In particular y = -d gives the output (0,0,0,0), and y = -d - 1 gives (F,F,F,F).

Proof. Follow the eight assignments.

1. a becomes a + 0 + x = d.
2. d becomes ROTR(d XOR d, 16) = 0.
3. c becomes 0 + 0 = 0.
4. b becomes ROTR(0 XOR 0, 12) = 0.
5. a becomes d + 0 + y = g.
6. d becomes ROTR(0 XOR g, 8) = ROTR(g, 8).
7. c becomes 0 + ROTR(g, 8) = ROTR(g, 8).
8. b becomes ROTR(0 XOR ROTR(g, 8), 7) = ROTR(g, 15).

If y = -d then g = 0 and every output word is 0. If y = -d - 1 then g = F, and F
is fixed by every rotation, so every output word is F.

## 4. The collision

**Construction.** For k = 0..3 apply Lemma 1 to column Ck. Its inputs are
(a,b,c,d) = (IVk, IV(k+4), IVk, rk) with (r0,r1,r2,r3) = (0,0,64,11). This fixes
s[2k] and s[2k+1], and the state after the columns is

    v[k] = Ak,   v[4+k] = 0,   v[8+k] = 0,   v[12+k] = -IV(4+k),   k = 0..3,

where Ak = ROTL(-IV(4+k), 8) XOR (IV(4+k) - IVk).

D0 then has inputs (v0, v5, v10, v15) = (A0, 0, 0, -IV7), and D2 has inputs
(v2, v7, v8, v13) = (A2, 0, 0, -IV5). Both have the form required by Lemma 2. Set

    s8  = -IV7 - A0,      s12 = -IV5 - A2,
    M :  s9 = IV7,        s13 = IV5,
    M':  s9 = IV7 - 1,    s13 = IV5 - 1.

Set s10 = s11 = s14 = s15 = F in both messages. Any fixed values would do. M and
M' share fourteen words and differ in s9 and s13.

**Theorem.** M and M' are distinct 64-byte messages with equal blake3-r1 digests.

Proof. The messages differ because IV7 - 1 is not IV7. The column words are the
same, so both messages reach the same state after the columns. D1 and D3 read
only state words 1,6,11,12 and 3,4,9,14, which D0 and D2 never write, and their
message words are the same in both messages. So v1, v6, v11, v12, v3, v4, v9 and
v14 are equal for M and M'.

By Lemma 2 with d = -IV7, message M has g = IV7 - IV7 = 0, so D0 outputs
v0 = v5 = v10 = v15 = 0. Message M' has g = F, so v0 = v5 = v10 = v15 = F. The
same holds for D2 with d = -IV5: v2 = v7 = v8 = v13 = 0 for M and F for M'.

Now compare digest words.

- o0 = v0 XOR v8 is 0 XOR 0 for M and F XOR F for M'. Both are 0.
- o2 = v2 XOR v10, o5 = v5 XOR v13 and o7 = v7 XOR v15 are 0 for the same reason.
- o1 = v1 XOR v9, o3 = v3 XOR v11, o4 = v4 XOR v12 and o6 = v6 XOR v14 use only
  words that are equal for M and M'.

All eight digest words agree. Both messages are 64 bytes, so they lie in the
target domain and their digests are the complete hash described in Section 2.
This is an ordinary collision. It is not free-start, compression-only or
truncated.

## 5. Lane arithmetic on 256-bit words

The program handles four 32-bit values in one 256-bit word. Lane i of a word is
its bits 64i..64i+63. A word is *clean* if every lane is below 2^32. Two constant
words are used: M has F in every lane, and GD = M shifted left by 32 has
ffffffff00000000 in every lane.

**S1 (addition).** If X and Y are clean, X + Y has lanes x_i + y_i < 2^33. No
carry leaves a lane.

**S2 (subtraction).** If X is clean and every lane of Y is below 2^34, then
((X OR GD) - Y) AND M is clean with lanes (x_i - y_i) mod 2^32. Proof: lane i of
X OR GD equals 2^64 - 2^32 + x_i, which is at least 2^64 - 2^32 and so larger
than y_i. Each lane difference is therefore between 0 and 2^64, the 256-bit
subtraction borrows nothing across lanes, and each lane is congruent to
x_i - y_i modulo 2^32. The mask keeps the low 32 bits. The same holds for
(GD - Y) AND M, which is the case X = 0.

**S3 (rotation).** If X is clean and 0 < k < 32, then
(SHL(X,k) OR SHR(X,32-k)) AND M is clean with lanes ROTL(x_i, k). Proof: x_i
shifted left by k is below 2^(32+k) and stays inside lane i, and its low 32 bits
are the low bits of the rotation. SHR(X, 32-k) puts x_i shifted right by 32-k
into the low k bits of lane i. The bits it brings in from lane i+1 land at bit
32+k or higher of lane i. The mask removes everything at bit 32 and above.

**S4 (extraction).** For a clean X, SHR(X, 64j) AND F is lane j. For j = 3 the
AND is not needed, because nothing lies above lane 3. SHR(M, 192) = F.

## 6. Machine and program

The machine is the cost model's 256-bit word RAM, used as a load/store register
machine. Every instruction below is one listed primitive operation, except
COMPRESS, which is one target compression.

- `LD r, T[j]` loads one 256-bit word from the constant table.
- `ST cell, r` stores a register to a memory cell.
- `ADD`, `SUB`, `AND`, `OR`, `XOR` take two registers. Arithmetic is modulo 2^256.
- `SHL`, `SHR` shift a register by a fixed amount given in the instruction. This
  is how `scripts/reference_operation_costs.py` counts the reference shifts.
- `BNZ`, `BZ` are conditional branches. `HALT` stops.
- `COMPRESS buf, out` reads sixteen 32-bit message words from sixteen cells,
  evaluates the Section 2 compression with its fixed public inputs, and writes the
  eight digest words to eight cells.

There is no 32-bit rotate, no multiplication and no immediate operand other than
a shift amount. Each 32-bit word of a message or digest occupies its own cell.

The constant table has four 256-bit words, written lane 0 first:

    T[0] = M  = (F, F, F, F)
    T[1] = AV = (IV0, IV1, IV2, IV3)
    T[2] = BV = (IV4, IV5, IV6, IV7)
    T[3] = DV = (0, 0, 64, 11)

These are the public constants of the target in a fixed layout. No value in the
table depends on any computation of the attack.

    001 LD  M, T[0]          002 LD  AV, T[1]
    003 LD  BV, T[2]         004 LD  DV, T[3]
    005 SHL GD, M, 32
    --- columns: Lemma 1 in four lanes ---
    006 OR  t, BV, GD        007 SUB t, t, AV         008 AND d1, t, M
    009 SHL p, d1, 16        010 SHR q, d1, 16        011 OR  p, p, q
    012 AND p, p, M          013 XOR a1, p, DV
    014 ADD S, AV, BV
    015 OR  t, a1, GD        016 SUB t, t, S          017 AND X, t, M
    018 SUB t, GD, BV        019 AND N, t, M
    020 SHL p, N, 8          021 SHR q, N, 24         022 OR  p, p, q
    023 AND p, p, M          024 XOR A, p, d1
    025 OR  t, A, GD         026 SUB t, t, a1         027 AND Y, t, M
    --- column message words ---
    028 SHR F, M, 192
    029 AND w0, X, F
    030 SHR t, X, 64         031 AND w2, t, F
    032 SHR t, X, 128        033 AND w4, t, F
    034 SHR w6, X, 192
    035 AND w1, Y, F
    036 SHR t, Y, 64         037 AND w3, t, F
    038 SHR t, Y, 128        039 AND w5, t, F
    040 SHR w7, Y, 192
    --- diagonal words: Lemma 2 ---
    041 SHL p, BV, 64        042 SHR q, BV, 192       043 OR  R, p, q
    044 ADD T, R, A          045 SUB T, GD, T
    046 AND w8, T, F
    047 SHR t, T, 128        048 AND w12, t, F
    049 AND w9, R, F
    050 SHR t, R, 128        051 AND w13, t, F
    052 SHR one, F, 31
    053 SUB w9p, w9, one     054 SUB w13p, w13, one
    --- output: 16 cells for M, 16 cells for M' ---
    055-070 ST bufM[i],  r_i    for i = 0..15
    071-086 ST bufM'[i], r'_i   for i = 0..15
    --- verification ---
    087 COMPRESS bufM,  dg       088 COMPRESS bufM', dg'
    089-112 for i = 0..7:  LD e, dg[i];  LD f, dg'[i];  XOR z_i, e, f
    113-119 OR acc, z_0, z_1;  then OR acc, acc, z_i  for i = 2..7
    120 BNZ acc, FAIL
    121 XOR t, w9, w9p       122 BZ t, FAIL
    123 HALT (success; the output is bufM and bufM')

The stored registers are r = (w0,w1,w2,w3,w4,w5,w6,w7,w8,w9,F,F,w12,w13,F,F).
r' is the same list with w9p in place of w9 and w13p in place of w13. FAIL is a
halting state that returns nothing. The theorem shows it is never reached.

## 7. The program computes the construction

Lines 006-027 are Lemma 1 for all four columns at once. Lane k carries column Ck,
with a = c = IVk from AV, b = IV(k+4) from BV and d = rk from DV.

- 006-008: d1 = b - c, by S2.
- 009-013: a1 = ROTL(d1, 16) XOR d, by S3. XOR of clean words is clean.
- 014: S = a + b, by S1. Its lanes are below 2^33.
- 015-017: X = a1 - S = a1 - a - b, by S2. This is the x word of each column.
- 018-019: N = -b, by S2 with X = 0.
- 020-024: A = ROTL(N, 8) XOR d1, by S3.
- 025-027: Y = A - a1, by S2. This is the y word of each column.

Lines 028-040 extract the lanes by S4: (w0,w2,w4,w6) are the lanes of X and
(w1,w3,w5,w7) are the lanes of Y, so w(2k) = s[2k] and w(2k+1) = s[2k+1].

Lines 041-043: SHL(BV, 64) has lanes (0, IV4, IV5, IV6) and SHR(BV, 192) has lanes
(IV7, 0, 0, 0), so R has lanes (IV7, IV4, IV5, IV6).

Lines 044-045: T = R + A has lane 0 equal to IV7 + A0 and lane 2 equal to
IV5 + A2, both below 2^33. By S2, GD - T has -(IV7 + A0) in the low 32 bits of
lane 0 and -(IV5 + A2) in the low 32 bits of lane 2.

- 046: w8 = -IV7 - A0 = s8. F selects the low 32 bits of lane 0.
- 047-048: w12 = -IV5 - A2 = s12.
- 049: w9 = IV7. 050-051: w13 = IV5.
- 052: one = F shifted right by 31 = 1.
- 053-054: w9p = IV7 - 1 and w13p = IV5 - 1. IV7 and IV5 are nonzero, so the
  256-bit subtraction does not wrap and both results are 32-bit values.

Every stored register is below 2^32. The stored cells are exactly the words of M
and M' from Section 4.

## 8. Verification step

Lines 087-123 evaluate the complete hash of each message with one compression
each, compare the eight digest words pairwise, and check that the messages differ
in s9. By the theorem, both checks pass, so the program always halts at line 123
with a valid pair. The check is not needed for correctness. It is included and
fully charged so that the claimed cost does not depend on whether a reviewer
requires an explicit collision check.

## 9. Cost

Charges under `collision-frontier-v5` with C = 222 for blake3-r1:

| Part | Lines | Instructions | Charge |
| --- | --- | ---: | ---: |
| Table loads | 001-004 | 4 | 4 ops |
| Arithmetic and logic | 005-054 | 50 | 50 ops |
| Stores of M and M' | 055-086 | 32 | 32 ops |
| Two compressions | 087-088 | 2 | 2 units |
| Digest loads | 16 of 089-112 | 16 | 16 ops |
| Digest XOR and OR | rest of 089-119 | 15 | 15 ops |
| Branches, distinctness, halt | 120-123 | 4 | 4 ops |

The 50 arithmetic operations are 16 AND, 13 SHR, 7 SUB, 6 OR, 4 SHL, 2 ADD and
2 XOR.

Executed work is 2 compressions plus 121 other operations. The two COMPRESS
instructions are also counted as one operation each for their dispatch, giving
123 operations beside the 2 units. This double-charges two instructions on
purpose.

Two further charges are added that the cost model lists under memory and not
under time: one operation per instruction to place the 123-instruction program,
and two operations per table word to place the 4-word table.

    W = 123 (execution) + 123 (program placement) + 8 (table placement) = 254
    T = 2 + 254/222 = 3.1441 units
    log2 T = 1.6527 < 1.66

The bound 1.66 holds for any W up to 257. There is no randomness, no failed
trial, no sorting, no lookup and no restart. The run is the same every time, so
this is a worst-case cost and the success probability is 1.

## 10. Other accounting conventions

The dominant term is the two verification compressions. The rest depends on
conventions that the cost model does not fix. The same program gives:

| Convention | W | T | log2 T |
| --- | ---: | ---: | ---: |
| A. Executed operations only | 123 | 2.5541 | 1.3528 |
| B. A plus program and table placement (claimed) | 254 | 3.1441 | 1.6527 |
| C. A, but the table may hold only 32-bit words | 148 | 2.6667 | 1.4150 |
| D. C plus program and table placement | 318 | 3.4324 | 1.7792 |
| E. A plus marshalling of compression parameters | 231 | 3.0405 | 1.6043 |
| F. C plus marshalling of compression parameters | 256 | 3.1532 | 1.6568 |

Convention C replaces the four wide table words by eleven 32-bit words (IV0..IV7,
64, 11, F) and builds M, AV, BV and DV with shifts and ORs: 19 more operations and
7 more loads, and line 028 is no longer needed. Conventions E and F add 27 loads
and 27 stores per compression for its chaining value, counter, length and flags,
in case a reviewer does not regard those as part of the compression unit.

The claim 1.66 holds under A, B, C, E and F. It does not hold under D, which
combines 32-bit-only table words with the voluntary placement surcharge; there
the bound is 1.78. The claim rests on the position that a 256-bit constant is one
word of a 256-bit word RAM, loaded by one "256-bit load", and that the cost model
charges code and constants as memory.

Without the verification step the program is lines 001-086 and a halt: 87
executed operations, 0.39 units. That reading is not claimed here.

## 11. Memory and claim fields

- Program: 123 instructions at four 256-bit words each, 15,744 bytes.
- Table: 4 words, 128 bytes.
- Registers: at most 32 named registers, 1,024 bytes.
- Message cells 32 and digest cells 16, one word each: 1,536 bytes.

The total is 18,432 bytes, below 2^15 = 32,768.

- `time_log2 = 1.66` bounds total charged time by 2^1.66 units (Section 9).
- `memory_log2_bytes = 15` bounds peak storage, code and constants included.
- `preprocessing_log2 = 0`: program and table placement is 131 operations, which
  is 0.59 units and below 2^0. It is already inside W.
- `nonuniform_advice_log2_bytes = 0`: there is no advice. The schema cannot
  express log2 of zero.
- `success_probability = 1`: Section 4 and Section 7; no coins are used.
- `heuristics` is empty because nothing in the argument is heuristic.

## 12. Evidence, prior work and limits

The certificate `blake3-r1-lane-pair` contains the two 64-byte messages the
program outputs. The organizer verifier recomputes both digests:

    M  = 1eae00b1b20691aa8cc89a63c6ee026b3716478a85d0f8b848f4aed6e079c2d1
         3145758d19cde05bffffffffffffffff9be3c7c58c68059bffffffffffffffff
    M' = 1eae00b1b20691aa8cc89a63c6ee026b3716478a85d0f8b848f4aed6e079c2d1
         3145758d18cde05bffffffffffffffff9be3c7c58b68059bffffffffffffffff
    digest = 0000000021fa412d00000000ef3de981afe12ffa00000000fb15a2c700000000

The certificate is evidence for a reviewer. It is not an input of the program and
is not stored advice: the program computes both messages from the four table
words.

The two G identities are not new. Inverting G in closed form goes back to the
analysis of BLAKE, and unpromoted public submissions on this track already use
the column identity of Lemma 1, the all-ones flip of Lemma 2 and four-lane
evaluation of the columns. What this package adds is the layout: the constants
enter as four lane-packed table words, the diagonal words come from one lane
rotation of BV, and no constant is assembled at run time. That brings the whole
verified program to 123 instructions.

The result is specific to one round. With two rounds every message word is used
twice and the identities no longer decouple. Nothing is claimed for blake3-r2.

The identifier `blake3-r1-nominal-v2` in `baseline_improved` names the
organizer's nominal reference 128, which is not an established attack or a
qualified baseline. `submission_state = ready` means the package is complete for
review. It does not assert a review outcome, a score, or human acceptance.
