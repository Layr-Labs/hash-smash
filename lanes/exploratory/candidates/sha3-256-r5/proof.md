# Connector-plus-trail collision attack on five-round SHA3-256 over byte strings

The scalar below is `time_log2` under `collision-frontier-v5`. Memory remains
a separately reported resource bound.

Declared bound: `time_log2 = 64`, success probability 0.5, peak memory at most
2^30 bytes, on target profile sha3-256-r5-prefix-v1. The bound is analytical
and depends on four declared heuristics (Section 8). No full-scale run was
performed and no certificate is supplied.

This revision addresses the fatal finding on the previous version of this
package (F1, algorithm not self-contained). Everything the algorithm needs
is now in this file: the state and bit conventions (Section 1), the
complete trail masks (Section 3), the exact connector constraint system and
how it is solved (Section 4), finite caps on every loop (Section 5), and a
cost ledger that charges trail search and every retry (Section 6). The
paper by Guo, Liao, Liu, Liu, Qiao and Song (JoC 2019, ePrint 2019/147;
GLL+19 below) is cited for provenance and for one published measurement.
The algorithm itself does not depend on reading it. Measurements made for
this package are kept separate from published figures and from
heuristics.

## 1. Target, encoding and message domain

H is the complete byte-string hash fixed by the profile. Pad
`m || 0x06 || 0x00* || 0x80` to a multiple of 136 bytes, XOR each block into
the first 17 lanes of the all-zero 1600-bit state, apply Keccak-f[1600]
prefix rounds 0..4 (round constants RC[0..4]) and output lanes 0..3,
little-endian. The FIPS 202 step mappings are exactly those of
`verifier/keccak.py`.

State bits. Lane (x,y) holds 64 bits. State bit index
`i = 64*(x + 5*y) + z` corresponds to bit z of lane (x,y). Message byte j
supplies state bits 8j..8j+7, with the least significant bit first. In
the hex grids below, row y = 0..4 lists lanes x = 0..4 as 16 hex digits
with the most significant digit first.

Messages. Every message is exactly 135 bytes. The padded block is the
single byte string `m || 0x86`: the 0x06 suffix and the final 0x80 bit
share byte 135. Byte 135 occupies state bits 1080..1087, and the LSB-first
values of 0x86 are `0,1,1,0,0,0,0,1`, so the four low bits are 0,1,1,0.
The free variables are the 1080 message bits (state bits 0..1079). Bits
1080..1087 are fixed to 0x86 and the capacity bits 1088..1599 are zero.
The fixed-bit count is therefore p = 8. GLL+19 used p = 4 with a different
tail (their witness ends in byte 0xEE). Section 4.4 measures why this
difference matters: the eight constant values change which connector
instances are feasible, not only how many bits are fixed. A 136-byte
message would need a second block, which is outside this construction.

Round notation. Let L = pi o rho o theta (linear), chi be the row S-box
`b_x = a_x XOR (NOT a_{x+1} AND a_{x+2})` on the 5 bits of a row (y,z), and
iota add RC. For a state difference, beta_r is the difference at the input
of chi in round r, and alpha_{r+1} is the difference at the output of chi,
so `beta_{r+1} = L(alpha_{r+1})`. Here iota does not affect differences.
The input difference is Delta_s0, the XOR of the two padded blocks, and
`beta0 = L(Delta_s0)`.

## 2. Attack outline

1. Fixed trail data (Section 3): alpha2 and the three-round tail
   beta2 -> beta3 -> beta4 -> zero digest difference.
2. Two-round connector (Section 4): find a difference d supported on the
   1080 message bits, and an affine space of 135-byte message values, such
   that every pair (m, m XOR d) in the space has chi-output difference
   exactly alpha2 after round 1. The message difference d is an output of
   each connector run, not a global constant.
3. Brute force (Section 5): for each message m in the space, test
   H(m) = H(m XOR d). The tail holds with probability about 2^-36.70 per
   pair.
4. Repeat steps 2 and 3 within fixed caps. Verify and return the first
   collision found.

## 3. Embedded trail data

The values below were recovered from GLL+19 trail core No. 3 and checked
with the implementation used for this package (Section 7).

beta2 (chi input of round 2; 10 active rows):

```
0000000000000001 0000000000000000 0000000000000004 0000000000000000 0000000000000000
0000000000000004 0000000000000004 0000000000000004 0000000000020000 0000000000000000
2000000000000000 0000000000000000 0000000000200000 0000000000000000 0000000000000000
2000000000000000 0000000000000000 0000000000000000 0000000000020000 0000000000000000
0000000000200001 0000000000000000 0000000000200000 0000000000000000 0000000000000001
```

beta3 (chi input of round 3; 9 active rows):

```
0000000000000001 0000000000000000 0000000000000001 0000004000000000 0000000000000000
0000000000000000 0000000000000000 0000000000000001 0000000000000000 0000000000040000
0000000000000000 0000000000000100 0000000000000000 0000000000000000 0000000000040000
0000000000000000 0000000000000000 0000000000000000 0000000000000000 0000000000000000
0000000000000001 0000000000000100 0000000000000000 0000004000000000 0000000000000000
```

beta4 (chi input of round 4; one representative final-round input):

```
0000000000000000 0000000000000000 0000000000000000 0000000000000000 0000000000000000
0000000010000004 0000004000000000 0000000000000000 0000000000000000 0000000000000000
0000008000000000 0000000000000040 0000000000000000 0000000000000000 0000000000040000
0000000000000000 0000001000000000 0000000000040000 0000000000000000 0100000040000000
4000000000000000 0000000000000000 0200000000000000 0000000000000000 0000010000000400
```

Connector target alpha2 = L^-1(beta2) (59 active rows):

```
A000001600000000 9000000A00000000 5000000E00800004 5000000A00000000 0000002200000000
A000001600000001 8000000A00000000 5000000E00000000 5000004A00000000 0000402600000000
2000001600000001 8000000A00000000 5000000E00800000 4000004A00000000 0000402600000000
A000001600000001 8000001A00000000 5000000E00000004 5000004A00000000 0000002600000000
A000001600000001 C000000A00000000 5000000E00000000 5000004A00000000 0000002600000000
```

Transition weights computed from the 5-bit chi DDT for these masks:

- beta2 -> alpha3 (where beta3 = L(alpha3)): weight 24, from 10 active S-boxes.
- beta3 -> alpha4 (where beta4 = L(alpha4)): weight 19, from 9 active S-boxes.
- Round 4: only the 256 digest bits (lanes 0..3 of row y = 0) must have
  zero difference. Several beta4 values and final-round transitions are
  compatible with this. GLL+19 report the aggregate tail probability over
  rounds 2..4 as 2^-36.70. This package uses that figure as heuristic h2.
  The published witness itself follows the beta2 and beta3 shown here
  exactly, but uses a sibling beta4 of weight 32 that also cancels on the
  digest. This illustrates the multi-trail aggregation.

## 4. Two-round connector

### 4.1 Unknowns

- d: 1080 bits, the message-bit difference. Delta_s0 = d, and bits 1080
  and above are zero.
- m: 1080 bits, the message-bit values of the first message. The first
  block is s0 = m | (0x86 << 1080).
- p: 1600 bits, the chi output of round 0 for the first message, before
  iota.

Derived linear forms over GF(2):

- beta0 = L(d). Each bit is a parity of d bits.
- x0 = L(s0) = L(m) XOR L(0x86 << 1080). This is the chi input value of
  round 0.
- x1 = L(p XOR RC[0]) = L(p) XOR L(RC[0]). This is the chi input value of
  round 1.
- beta1 = L(alpha1), where alpha1 is a constant fixed in step 4.2.

### 4.2 Choosing alpha1

Set alpha1 = L^-1(beta1). For every row (y,z) of round 1 with
dout1 = alpha2[y,z] nonzero, choose din1 = beta1[y,z] such that
DDT[din1][dout1] > 0, taking a maximal-DDT entry with probability 0.7 and
any compatible entry otherwise. Rows with dout1 = 0 get din1 = 0. With
the 59 active rows of alpha2, 50 of those rows have a unique best din1.
Alpha1 therefore usually has about 270 to 320 active rows in round 0. The
published witness has 318.

### 4.3 Constraint system (exact)

The tables below are written for the 5-bit chi S-box S. V(a,b) denotes
the set {v : S(v) XOR S(v XOR a) = b}. Every nonempty V(a,b) is an affine
subspace of GF(2)^5 of size 2, 4 or 8. This was checked exhaustively: 20
entries of size 8, 120 of size 4 and 176 of size 2.

For each of the 320 rows (y,z) of round 0, let dout = alpha1[y,z]:

- If dout = 0: beta0[y,z] = 0 (5 linear equations), and
  (x0[y,z], p[y,z]) lies in {(v, S(v)) : v in GF(2)^5}.
- If dout is nonzero: the 15-bit tuple (beta0[y,z], x0[y,z], p[y,z]) lies
  in {(a, v, S(v)) : DDT[a][dout] > 0, v in V(a,dout)}.

For each of the 320 rows of round 1, let din1 = beta1[y,z] and
dout1 = alpha2[y,z]. If either is nonzero, x1[y,z] lies in
V(din1, dout1). Otherwise there is no constraint.

Any solution (d, m, p) gives two 135-byte messages m_a and m_b = m_a XOR d,
read off state bits 0..1079. By construction, their chi-output difference
after round 1 is exactly alpha2, and both pad to `|| 0x86`. Together with
Section 3, this is a complete statement of what the connector must
satisfy.

### 4.4 Solving

The connector solves this mixed linear/table system with GF(2) row
reduction combined with S-box linearization, as in GLL+19 Sections 4-5.
Equivalently, any complete SAT/CP solver can be used. An instance either
succeeds or is abandoned after its budget, and then a fresh alpha1 is
drawn (Section 5 caps).

Affine output space. Once d and all beta0 rows are fixed, each active
round-0 row constrains x0[y,z] to the affine set V(beta0[y,z], dout),
which gives linear equations on m. Where S is affine on that set (all
DDT-2 and DDT-4 sets; measured below), p[y,z] is an affine function of m.
The round-1 conditions then become linear in m. The remaining DDT-8 rows
are linearized by restricting to an affine 2-dimensional subset, as in
GLL+19 "non-full linearization". There are 6 such subsets inside V(01,01),
and 80 fully linearizable 2-flats exist in GF(2)^5. Both counts were
reproduced here. Rows that are inactive in round 0 but feed a
round-1 condition are linearized the same way. The output is the full
solution set of the resulting linear system on m: an affine space
S_i = m_i + span(B_i) of dimension DF_i. Every element of S_i satisfies
Section 4.3 with the same d.

Measurements on the exact profile, from a local implementation:

- The round-0 difference subproblem (beta0 rows in DDT-compatible sets,
  inactive rows zero) for the published alpha1 solves in 0.9 s.
- The full round-0 system with value constraints and p = 8 (0x86 tail,
  zero capacity) solves for the published alpha1 in about 100 s. The
  resulting 135-byte pair was checked with the reference permutation to
  produce chi-output difference exactly alpha1 (Section 7, item 5).
- In the published witness's round-0 pattern, 156 active rows are DDT-4,
  75 are DDT-2 and 87 are DDT-8. S is affine on V for all DDT-2 and DDT-4
  rows and on none of the DDT-8 rows. This matches the count of rows that
  need non-full linearization.
- Pad sensitivity. When the round-0 input differences are fixed to the
  published witness's pattern, the two-round system is satisfiable in
  3.5 s with the paper's tail byte 0xEE. It is unsatisfiable within 2 s
  with the byte-string tail 0x86. Fixing those same patterns from 25
  other round-0 solutions gave no two-round solution under 0x86 within
  60 s each. With the input differences left free, a 240-280 s solver
  budget on the published alpha1 ended without a decision. A complete
  two-round p = 8 connector instance has therefore not been produced
  locally. Connector success per instance at p = 8 is lower than at
  p = 4. The cost ledger charges a retry factor for this (Section 6),
  and heuristic h1 states the remaining premise.

## 5. Algorithm with explicit caps

Constants: R = 2^13 connector successes required at most; A = 2^4
connector attempts budgeted per success. Each attempt has a fixed
work budget (Section 6). E = 2^33 messages enumerated per space at most.

```
for i in 1 .. R:
    for attempt in 1 .. A:                # finite
        draw alpha1 (4.2) from fresh coins
        run the connector (4.3/4.4) within its fixed budget
        if it returns (d_i, S_i): break
    if no space was returned: continue
    enumerate the first min(2^DF_i, E) elements m of S_i in Gray-code order:
        if H(m) == H(m XOR d_i) and m != m XOR d_i:
            recompute both hashes from the zero state over rounds 0..4
            if all 256 output bits are equal: return (m, m XOR d_i)
return failure
```

d_i is nonzero, so m != m XOR d_i automatically. Spaces may overlap, and
repeats are charged in full. No loop exists outside these caps.

## 6. Cost ledger (collision-frontier-v5)

Unit: one complete 5-round permutation is 1 unit. Every other 256-bit
word operation costs 1/1355 unit.

Trail-search precomputation. Section 3 embeds four masks. The cost model
charges any search that produced them. GLL+19 do not report a separately
measured trail-search cost, so this package charges a flat envelope of
2^60 units (about 2^70.4 word operations) for finding a three-round
trail core of this weight class and its alpha2. Checking the embedded
masks is cheap: one DDT lookup per active row.

Connector. The published p = 4 connector stage took 428.8 core-hours,
about 1.54 * 10^6 core-seconds (GLL+19, Table 6). At a generous 2^36
word operations per core-second, that is 2^56.6 operations, or 2^46.2
units per successful connector including its own internal retries.
Byte alignment lowers the success rate per attempt (Section 4.4). This
package therefore fixes the budget of one connector attempt at 2^46.8
units, slightly above the published per-success envelope, and allows
A = 2^4 attempts per success:

    connector total <= R * A * 2^46.8 = 2^13 * 2^4 * 2^46.8 = 2^63.8 units.

Brute force. At most E = 2^33 messages per space, 2 hashes per message,
and R spaces: 2^47 hash evaluations. Each carries at most 2^12 word
operations of overhead (XOR, padding, absorb/squeeze, comparison):
2^47 * (1 + 2^12/1355) < 2^49 units.

Verification: 2 hashes and fewer than 2^18 word operations.

Total:

    T <= 2^63.8 (connector) + 2^60 (trail search) + 2^49 (brute force) + small
      = 2^63.8 * (1 + 2^-3.8 + 2^-14.8) + small < 2^63.91 < 2^64.

Declared `time_log2 = 64`. `preprocessing_log2 = 64` covers trail search
plus connector work, both charged inside time. Memory: the GF(2) systems
have at most 4280 variables and about 3000 equations, which is under 2^22
bytes. Spaces are enumerated without being stored. The total is below
2^30 bytes. `nonuniform_advice_log2_bytes = 13` bounds the embedded masks
and tables, about 2 KB, and their search is charged above.

## 7. Evidence produced for this package

All checks are local CPU computations. None is a ranked benchmark run.

1. The linear layer L, its inverse L^-1, and chi were implemented on
   1600-bit integers and checked against the permutation of
   `verifier/keccak.py`.
2. The published Table 17 padded blocks, applied from the zero state with
   rounds 0..4 of `verifier/keccak.py`, both produce digest lanes
   65017C2E8B6040B4 344FF8BB933B4BD6 C6A3F13368BE2003 AB427B4B33435ACB.
   This confirms the round convention and encoding. These 1084-bit
   messages are not byte strings and are not a certificate.
3. The witness's chi input difference in round 2 equals the beta2 above
   bit for bit, and in round 3 equals the beta3 above. DDT weights are
   24 and 19, with 10 and 9 active rows.
4. The S-box linearization counts match GLL+19: 80 fully linearizable
   2-flats, 6 inside V(01,01), and V(03,02) = {14,17,1C,1F}.
5. Byte-aligned round-0 connector instance (Section 4.4). The two 135-byte
   messages are listed in Appendix A. Each pads to `|| 0x86` with zero
   capacity, and their chi-output difference after round 0 equals the
   witness's alpha1 (318 active rows).
6. The negative and timed-out two-round results under 0x86 are reported
   in Section 4.4. They are the reason for the retry factor A.
7. `yukon setup` passed. `scripts/local_tracks.py check` reports the
   package as mechanically valid. No GPU is available, and `yukon run`
   was not executed.

## 8. Heuristics and limitations

- h1 (score-critical): a p = 8 two-round connector instance succeeds
  within A = 2^4 attempts at the per-attempt budget, and returns
  DF_i >= 25. Support: Sections 4.3-4.4. The round-0 layer is solved
  at p = 8. The DF loss from 4 more fixed bits is linear. The published
  DF is 37 at p = 4. Against: the measured pad sensitivity in Section
  4.4 and the absence of a local two-round p = 8 instance. If a p = 8
  success needs more than about 2^4.6 times the published per-success
  connector work, the bound fails.
- h2 (score-critical): each pair in S_i satisfies the rounds 2..4
  digest condition with probability at least 2^-36.70, the published
  multi-trail aggregate. Support: verified beta2/beta3 transition
  weights of 24 and 19, and the witness following them. Against: this
  is a published estimate, not a proof for the connector's output
  distribution.
- h3 (score-critical): collision events across the R spaces are
  approximately independent. Each space contributes at least 2^24 pairs,
  for at least 2^37 in total. The expected number of collisions is at
  least 2^0.30 = 1.23, which gives Pr >= 1 - e^-1.23 > 0.70 under a
  Poisson approximation. This is a counting heuristic and is not proven.
  Positive correlation between spaces reduces the effective count. The
  declared 0.5 still holds if the effective mean is at least 0.70,
  meaning a loss of up to about 0.8 bit. No larger tolerance is claimed.
- h4 (supporting): the core-hour to word-operation conversion (2^36 per
  core-second) and the trail-search envelope of 2^60 units are
  upper-bound conventions, not instruction traces.

## 9. Provenance

Trail core, connector method and witness: GLL+19, building on
Dinur-Dunkelman-Shamir (FSE 2012) and Song-Liao-Guo (CRYPTO 2017). This
package contributes the byte-string adaptation (p = 8 with the 0x86
tail), the explicit constraint system, local measurements, caps and cost
accounting. `baseline_improved` names `sha3-256-r5-nominal-v2` as a
required reference identifier only.

## Appendix A. Byte-aligned round-0 connector pair (135-byte messages, hex)

Each message is 135 bytes (270 hex digits, wrapped). Pad each with 0x86
(single block, zero capacity) and apply round 0 of `verifier/keccak.py`
(`permutation(..., rounds=1)`). The XOR of the two outputs equals the XOR of the
two published Table 17 blocks after the same round (alpha1, 318 active rows).
This was checked with the organizer verifier. The full 5-round digests differ:
this is a connector-layer witness, not a collision.

m_a:

```
cd8211d1e17678af3e4fb639259eefae75bc67519cd355d4fb1494e866002942b9c4394a
0dc3543f386cfcd017e7c10a65d55633cc9e451edc4294bc010db39b2f2f846a68d5b978
a2052cc2502a8f2b5889c7fccf0e42d030f730b638609ce647a7fa2d60160407dd50ee69
39a268dbf3cd5e15365c17d1ed3e5dac0a912ad491fd270c253c7b
```

m_b:

```
42524ab038fb0c82176326122cd20c84fefcd152be476c8949be60d63a5420af0dbdbf89
b09d764d50cb90efdc8706ac6e420313ee36166ed735ce3e0c21ad2ca1613f1e4e35118a
81e66f64f3f395cdda676d11ef05cde61f623d39f2c8d84f38e3485fdfb12cf0f127bcbf
a169c18cd4b1ca9a572d5739aa33136e2a9da4a77a0b3f4fac7660
```
