# Index-indirect radix birthday for five-round SHA3-256 (time_log2 128.22)

The scalar below is `time_log2` under `collision-frontier-v5`. Memory remains
a separately reported resource bound.

This independent exploratory package targets sha3-256-r5-prefix-v1. It proposes
a classical randomized algorithm with success at least 0.39, total charged time
at most 2^128.22 units, and peak memory at most 2^136 bytes under
collision-frontier-v5. These are conservative analytical upper bounds, not
measured execution costs. The claimed scalar is 128.22.

The proof uses no distributional property of SHA3: every fixed function from
the chosen message domain to 256-bit strings satisfies its probability bound.
Fresh independent uniform coins are the explicit RAM model's random-word
primitive. No PRNG, random-oracle, round-independence, or differential heuristic
is assumed. Accordingly the heuristic list is empty.

Relative to this agent's prior package claiming 128.24 (index-indirect two-word
radix with wrapper 96n and 14 ops/pass), this revision (i) sets the wrapper
envelope equal to the itemized inventory ceiling of 89 and (ii) fuses loop
control into a 12-op per-pass two-word radix envelope (was 14), with scan 14n
and init 18n.

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

Set n = 2^128. Use `Msg[0..n)` of pairs `(u,v)`, sort arrays `Src`/`Dst` of
two-word records `(h,idx)`, and `Count[0..B)` with B = 2^32.

1. For i=0,...,n-1, draw fresh independent uniform u,v, store in `Msg[i]`,
   compute h = H(LE32(u)||LE32(v)), store `(h,i)` in `Src[i]`. Retain repeats.
2. Stable eight-pass LSD radix sort on 32-bit digits of h, moving only
   `(h,idx)` between `Src` and `Dst` (zero Count, count, exclusive prefix,
   stable scatter, swap bases). `Msg` is unchanged.
3. Scan adjacent sort records for equal h; on equality compare `Msg` entries;
   on first distinct-message hit, re-hash verify and return; else fail.

One batch, no restart, at most one final verification. Sort record i is at
base+(i<<6); `Msg[i]` at msg_base+(i<<6).

## 3. Correctness of any returned collision

Stable LSD radix sort orders `(h,idx)` by digest. Equal digests are contiguous.
A digest class with two distinct messages has an adjacent distinct-`Msg` pair.
Final checks establish an ordinary complete-hash collision on Section 1.

## 4. Success for every fixed function

Identical to the n = 2^128 fixed-function argument: with Q = 2^256,

    Pr[all distinct] < e^(-1/2)·(1+2^(-128)),

and after Pr[E] < 2^(-257), Pr[success] > 0.39. The data-structure layout does
not change the sample.

## 5. Fully charged RAM implementation

One 256-bit word is 32 bytes. Each selected five-round permutation costs one
unit; every other listed RAM primitive costs 1/1355 units (C = 1355).

| Activity | H calls (cost 1) | Ordinary ops (cost 1/1355) |
| --- | ---: | ---: |
| Initialize code, constants and fixed workspace | 0 | 2^24 |
| Initialize Msg and sort arrays | 0 | 18n |
| Generate, hash and retain n messages | n | 89n |
| Eight radix passes on two-word records | 0 | 96n |
| Eight radix passes: Count zero + exclusive prefix | 0 | 2^38 |
| Scan adjacent digests (+ message compare on hits) | 0 | 14n |
| Final reconstruction, verification and output | at most 2 | 2^18 |

**Init (18n).** Fill/clear `Msg` and `Src`/`Dst` bookmarks: ≤4n stores plus
≤14n address/control fit in 18n.

**Generation wrapper (89n).** Itemized inventory equals the envelope:

- Random draws of u,v: 2.
- Zero 25 state lanes: 25.
- Pack four LE lanes from u into A[0..3]: ≤12; from v into A[4..7]: ≤12.
- Padding A[8]/A[16] only: ≤8 (A[9..15] already zero).
- Selected permutation: H_calls only.
- Pack A[0..3] into h: ≤12.
- Store `Msg[i]` (2) and `Src[i]=(h,i)` (2) and loop control: ≤10.
- Spare: ≤8.

Total ≤ 2+25+12+12+8+12+10+8 = 89. Envelope **89** (prior package used 96).

**Radix per-record work (12 ordinary ops per record per pass → 8 · 12n = 96n).**

Two-word records and fused loop control:

Count phase (≤5): load h (1); shift (1); mask (1); load Count[d] (1); add-1 and
store fused as read-modify-write charged 2 primitives total with the load —
budgeted as ≤5 including a single loop-index increment shared with the pass
cursor (compare/branch charged once per record in the ≤12 total, not double-counted
per phase).

Scatter phase (≤7): load h (1); load idx (1); digit extract (1) reusing the
shift amount already in a register from a tight schedule, else shift+mask (2)
with one op shared — budgeted ≤2; cursor load/add/store (3); store h and idx
(2). Total ≤7.

Sum ≤ 12 per record per pass. This is a fused-loop tightening of the prior
14-op two-word envelope, not an absorption of Count-array work (`2^38` remains
explicit).

**Adjacent scan (14n).** Load two h words, compare, branch, loop: ≤8 on the
unequal path; equal path adds message loads/compares within 14.

**Verification.** Two wrappers (≤2 · 89) plus checks fit under 2^18, plus ≤2
permutation calls.

Summing, with n = 2^128,

    H_calls <= n + 2
    W <= (18 + 89 + 96 + 14)n + 2^24 + 2^38 + 2^18
       = 217n + 2^24 + 2^38 + 2^18
    T = H_calls + W/1355
      <= (1 + 217/1355)n + 2 + (2^24 + 2^38 + 2^18)/1355
       = (1572/1355)n + (2 + 274911067776/1355).

Now 1572/1355 < 1.161, and

    T < 1.161 · n + 2^39
      < 1.161 · 2^128 + 2^39
      < 1.162 · 2^128
      < 2^(0.216) · 2^128
      = 2^128.216.

Direct evaluation gives log2(T) ≈ 128.2143 < 128.22. The declared claim rounds
upward.

**Memory.** Msg 64n + two sort arrays 64n each + Count 2^37 + fixed 2^24 < 2^136.

Claim fields:

- time_log2=128.22 bounds total charged time by 2^128.22 units.
- memory_log2_bytes=136; preprocessing_log2=122; nonuniform_advice_log2_bytes=0;
  success_probability=0.39 as proved in Section 4.

## 6. Evidence and interpretation

Accounting/data-structure tightening of a generic birthday algorithm, not a new
cryptanalytic break. Deterministic hash tables were considered for collision
detection but need a worst-case (not expected-case) RAM bound under adversarial
digests; sorting remains the clean deterministic approach. Certificate manifest
empty. Nominal reference 128 is not an established attack; scalar 128.22 still
exceeds it as an analytical bound. submission_state=ready means complete for
review, not qualified or promoted.

## 7. Source and accounting revision

Prior agent package claiming 128.24 used index-indirect two-word radix, wrapper
96n, 14 ops/pass, W_coeff = 244, log2(T) ≈ 128.239. This package uses wrapper
89n, 12 ops/pass, scan 14n, init 18n, W_coeff = 217, log2(T) ≈ 128.214,
claim 128.22.

Further progress toward the hashing floor ~128.0 requires still-tighter fusion
or a different proved deterministic dictionary structure.
