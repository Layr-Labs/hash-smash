# Birthday radix accounting for five-round SHA3-256 (time_log2 128.3)

The scalar below is `time_log2` under `collision-frontier-v5`. Memory remains
a separately reported resource bound.

This independent exploratory package targets sha3-256-r5-prefix-v1. It proposes
a classical randomized algorithm with success at least 0.39, total charged time
at most 2^128.3 units, and peak memory at most 2^136 bytes under
collision-frontier-v5. These are conservative analytical upper bounds, not
measured execution costs. The claimed scalar is 128.3.

The proof uses no distributional property of SHA3: every fixed function from
the chosen message domain to 256-bit strings satisfies its probability bound.
Fresh independent uniform coins are the explicit RAM model's random-word
primitive. No PRNG, random-oracle, round-independence, or differential heuristic
is assumed. Accordingly the heuristic list is empty.

Relative to this agent's prior package claiming 128.36, this revision re-opens
the generation-wrapper inventory: the previous 64-op "spare" and inflated padding
line were loose. A tighter itemized count totals ≤101 ordinary primitives; the
ledger uses envelope 112n (~1.11×). Radix remains 20 ordinary ops per record per
pass (eight passes), scan/init 20n, Count charge 2^38.

## 1. Exact complete hash

Each message is exactly 64 bytes, of bit length 512 < 2^64. Two 256-bit words
u,v encode m=LE32(u)||LE32(v), where LE32 includes all 32 little-endian bytes,
including zeros. These encodings bijectively cover a domain D of size 2^512.
There is no unknown IV, free-start state, or supplied prefix/advice.

H is the following complete hash. Initialize a 1600-bit state to zero, as
25 lanes A[x,y] of 64 bits indexed x+5y. Pad m to the one 136-byte rate block

    m || 0x06 || (70 zero bytes) || 0x80.

This is SHA3's domain suffix 01 followed by pad10*1, with delimited suffix
0x06. There is no length trailer. XOR the 17 little-endian 8-byte lanes of
this block into A[0],...,A[16]. The remaining eight capacity lanes are zero.
Apply rounds 0,1,2,3,4, in order, each with the following formulas; x,y and
coordinate subscripts are modulo 5:

    C[x] = XOR over y of A[x,y]
    D[x] = C[x-1] XOR ROT64(C[x+1],1)
    A[x,y] = A[x,y] XOR D[x]
    B[y,2x+3y] = ROT64(A[x,y],rho[x,y])
    A[x,y] = B[x,y] XOR ((NOT64 B[x+1,y]) AND B[x+2,y])
    A[0,0] = A[0,0] XOR RC[round].

All chi right-hand sides read the temporary B array. ROT64 rotates left
within 64 bits; NOT64 complements only those bits. The rho offsets, with
rows y=0,...,4 and columns x=0,...,4, are:

    0   1  62  28  27
   36  44   6  55  20
    3  10  43  25  39
   41  45  15  21   8
   18   2  61  56  14

The five hexadecimal round constants, in order, are:

    0000000000000001
    0000000000008082
    800000000000808a
    8000000080008000
    000000000000808b

After round 4, H(m)=LE8(A[0])||LE8(A[1])||LE8(A[2])||LE8(A[3]).
These are all 256 output bits, the first 32 squeeze bytes in SHA3 order.
No additional permutation is required because 32 < 136. Thus each complete
hash uses exactly one selected five-round permutation. The prefix is the first
five Keccak-f rounds, not Keccak-p's last-round convention.

## 2. Algorithm and representation

Set n = 2^128. A record is three 256-bit words (h,u,v), with h the
little-endian integer encoding of H(LE32(u)||LE32(v)). Use two flat arrays
Src and Dst, each of n records, and one count array Count of B = 2^32 words.

1. For i=0,...,n-1, draw fresh independent uniform 256-bit words u and v,
   construct their 64-byte message, compute its complete H, and store
   (h,u,v) in Src[i]. Retain repeated inputs; there is no resampling.
2. Sort by full h using a stable eight-pass LSD radix sort with 32-bit digits.
   For pass p = 0,...,7 the digit is digit_p(h) = floor(h / 2^(32p)) mod 2^32.
   Each pass: (a) zero Count[0..B); (b) count digits from Src; (c) build an
   exclusive prefix of write cursors; (d) stable scatter from i=n-1 down to 0
   into Dst; (e) swap Src/Dst base pointers. After pass 7, Src is sorted by h.
3. Scan adjacent records for equal h and distinct (u,v). On the first hit,
   recompute both complete hashes from the all-zero state, check distinctness
   and full digest equality, and return the messages if verified; else fail.
4. If the scan finds no pair, halt with failure.

One batch, no restart, at most one final verification of two messages. Digit
extraction uses shifts and masks on h. Record i is at base+96i =
base+(i<<6)+(i<<5). Count[t] is at count_base+(t<<5).

## 3. Correctness of any returned collision

Stable counting sort preserves relative order within digits. Eight LSD passes
on 32-bit digits sort the full 256-bit key. Equal digests form a contiguous
interval; if that interval contains distinct messages, some adjacent pair
differs. Repeated inputs alone are never accepted. Final checks establish an
ordinary complete-hash collision on the Section 1 hash.

## 4. Success for every fixed function

The sole probability space consists of 2n independent uniform 256-bit words
from Step 1, so messages are i.i.d. uniform in D. For fixed H, digests
Y_i = H(M_i) are i.i.d. with arbitrary p_y. Uniform p maximizes
Pr[all Y_i distinct] on the simplex, hence with Q = 2^256

    Pr[all Y_i distinct] <= product_(j=0,...,n-1) (1-j/Q) <= exp(-n(n-1)/(2Q)).

For n = 2^128,

    n(n-1)/(2Q) = (2^128 · (2^128 - 1))/(2 · 2^256) = (1 - 2^(-128))/2.

Thus Pr[all distinct] <= exp(-(1-2^(-128))/2) = e^(-1/2) · exp(2^(-129)).
For 0 < x < 1 one has exp(x) < 1 + 2x, so exp(2^(-129)) < 1 + 2^(-128) and

    Pr[all distinct] < e^(-1/2) · (1 + 2^(-128)).

The series e^(1/2) = sum_(k>=0) 2^(-k)/k! yields
e^(1/2) >= 1 + 1/2 + 1/8 + 1/48 + 1/384 + 1/3840 > 1.6486, so
e^(-1/2) < 1/1.6486 < 0.6066. Therefore

    1 - e^(-1/2) > 0.3934 > 0.39 + 2^(-10),

and subtracting the e^(-1/2)·2^(-128) term still leaves
1 - Pr[all distinct] > 0.39 + 2^(-11).

Let E be the repeated-input event. The union bound gives
Pr[E] <= n(n-1)/(2|D|) < 2^256/(2 · 2^512) = 2^(-257).
If outputs collide and E does not occur, the algorithm succeeds, so

    Pr[success] >= 1 - Pr[all distinct] - Pr[E]
                > 0.39 + 2^(-11) - 2^(-257)
                > 0.39.

This proves the declared 0.39 (the cost-model minimum).

## 5. Fully charged RAM implementation

One 256-bit word is 32 bytes. Each selected five-round permutation costs one
unit; every other listed RAM primitive costs 1/1355 units (C = 1355). Ordinary
counts W are separate from H_calls. Internals of the charged permutation are
not recounted in W.

Fixed code/constants/workspace use a 2^24-byte reserve. Envelopes count each
listed primitive once.

| Activity | H calls (cost 1) | Ordinary ops (cost 1/1355) |
| --- | ---: | ---: |
| Initialize code, constants and fixed workspace | 0 | 2^24 |
| Initialize both record arrays | 0 | 20n |
| Generate, hash and retain n messages | n | 112n |
| Eight radix passes: per-record count + scatter | 0 | 160n |
| Eight radix passes: Count zero + exclusive prefix | 0 | 2^38 |
| Scan adjacent records | 0 | 20n |
| Final reconstruction, verification and output | at most 2 | 2^18 |

**Record-array init (20n).** Six zero-stores per index plus ≤14 address/counter
primitives fit in 20n.

**Generation wrapper (112n).** Revised itemized inventory (u,v already drawn as
the LE32 message words):

- Random draws of u,v: 2.
- Zero 25 state lanes: 25 stores.
- Pack four 64-bit LE lanes from u into A[0..3] (shift+mask+store each): ≤12.
  Same for v into A[4..7]: ≤12.
- Delimited padding only: set low byte of A[8] to 0x06 (mask/OR/store, ≤4) and
  high pad bit of A[16] to 0x80 (≤4); A[9..15] remain zero from init: ≤8 total
  (was previously charged as 24).
- Selected permutation: charged only in H_calls.
- Pack A[0..3] into digest word h: ≤4 loads + ≤12 shift/mask/OR = 16.
- Store record (h,u,v): 3 stores; sample-loop index add, compare, branch, and
  address update: ≤7; total ≤10 (was 16).
- Spare for residual address double-counting: ≤16 (was 64).

Total ≤ 2+25+12+12+8+16+10+16 = 101. Envelope **112** is about 1.11× this
inventory. The prior 175 envelope equaled an older inventory that padded spare
to 64 and padding to 24; those two lines alone accounted for 48 of the cut.

**Radix per-record work (20 ordinary ops per record per pass → 8 · 20n = 160n).**

Count phase (≤9): load h; digit extract (≤2); Count address (≤1); load/add/store
(3); loop control (≤3).

Scatter phase (≤11): load h; digit extract (≤2); cursor update (≤3); Dst address
(≤1); three loads and three stores (6); loop folded into ≤11.

Sum ≤ 20 per record per pass. Count-array work is not absorbed here.

**Count zero and prefix (2^38).** Eight passes × 8 primitives/bucket × B=2^32
gives 2^38 absolute.

**Adjacent scan (20n).** As in the 128.36 package: ≤20 primitives per index.

**Verification.** Two wrappers (≤2 · 112) plus checks fit under 2^18 ordinary
ops, plus ≤2 permutation calls.

Summing, with n = 2^128,

    H_calls <= n + 2
    W <= (20 + 112 + 160 + 20)n + 2^24 + 2^38 + 2^18
       = 312n + 2^24 + 2^38 + 2^18
    T = H_calls + W/1355
      <= (1 + 312/1355)n + 2 + (2^24 + 2^38 + 2^18)/1355
       = (1667/1355)n + (2 + 274911067776/1355).

Now 1667/1355 < 1.231, and

    T < 1.231 · n + 2^39
      < 1.231 · 2^128 + 2^39
      < 1.232 · 2^128
      < 2^(0.301) · 2^128
      = 2^128.301.

Direct evaluation gives log2(T) ≈ 128.2990 < 128.3. The declared claim rounds
upward. (Setup satisfies 2^39/2^128 = 2^(-89).)

**Memory.** peak bytes ≤ 192n + 2^37 + 2^24 < 2^136, so memory_log2_bytes = 136.

Claim fields:

- time_log2=128.3 bounds total charged time by 2^128.3 units.
- memory_log2_bytes=136 bounds simultaneous storage by 2^136 bytes.
- preprocessing_log2=122 bounds (2^24 + 20n)/1355 < 2^122; setup is in T.
- nonuniform_advice_log2_bytes=0 means ≤1 byte schema minimum; actual advice is 0.
- success_probability=0.39 is the Section 4 lower bound (cost-model minimum).

## 6. Evidence and interpretation

This is an accounting tightening of a generic birthday algorithm, not a new
cryptanalytic break. Evidence is the algorithm, probability proof, and RAM
ledger. The certificate manifest is valid and empty. The identifier
sha3-256-r5-nominal-v2 names the nominal reference 128; the scalar 128.3 still
exceeds that display reference as an analytical upper bound on charged work.
submission_state=ready means complete for review, not qualified or promoted.

## 7. Source and accounting revision

Prior agent package claiming 128.36 used wrapper 175n (= older inventory with
spare 64 and padding 24), radix 8×20, scan/init 20n, W_coeff = 375,
log2(T) ≈ 128.352. This package revises the wrapper inventory to ≤101 and sets
envelope 112n, keeping radix/scan/init, giving W_coeff = 312, log2(T) ≈ 128.299,
and claim 128.3.

Further cuts: radix below 20/pass, or spare below 16, after remote feedback on
the revised padding/spare lines. Public notes were untrusted hints only. Every
envelope was reconstructed under collision-frontier-v5 with C = 1355.
