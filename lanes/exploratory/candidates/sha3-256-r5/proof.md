# Index-indirect radix birthday for five-round SHA3-256 (time_log2 128.2)

The scalar below is `time_log2` under `collision-frontier-v5`. Memory remains
a separately reported resource bound.

This independent exploratory package targets sha3-256-r5-prefix-v1. It proposes
a classical randomized algorithm with success at least 0.39, total charged time
at most 2^128.2 units, and peak memory at most 2^136 bytes under
collision-frontier-v5. These are conservative analytical upper bounds, not
measured execution costs. The claimed scalar is 128.2.

The proof uses no distributional property of SHA3: every fixed function from
the chosen message domain to 256-bit strings satisfies its probability bound.
Fresh independent uniform coins are the explicit RAM model's random-word
primitive. No PRNG, random-oracle, round-independence, or differential heuristic
is assumed. Accordingly the heuristic list is empty.

Relative to this agent's prior package claiming 128.22, this revision trims the
fused two-word radix envelope from 12 to 11 ordinary ops per record per pass and
tightens scan/init to 12n each, keeping wrapper 89n (= inventory).

## Why not hash tables / FKS this pass

collision-frontier-v5 lists no 256-bit multiplication, so hash families are
limited to adds/xors/shifts. A chaining table with m = n and a worst-case scan
cap L must take L well above the ~log n / log log n ≈ 18 typical max load so
that abort-on-overflow does not erase the 0.39 success budget; with L ≥ 30 and
≥3 primitives per probe, table work alone is ≳ n·(6+90) and fails to beat the
present 88n radix term under a deterministic per-outcome cap. FKS perfect
hashing targets static sets of distinct keys; duplicate detection is the goal
here, and rebuilding a perfect hash after the fact does not find duplicates
cheaper than radix on 256-bit word keys. Sorting is retained.

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
   `(h,idx)` between `Src` and `Dst`. `Msg` is unchanged.
3. Scan adjacent sort records for equal h; on equality compare `Msg` entries;
   on first distinct-message hit, re-hash verify and return; else fail.

One batch, no restart, at most one final verification.

## 3. Correctness of any returned collision

Stable LSD radix sort orders `(h,idx)` by digest. Equal digests are contiguous.
A digest class with two distinct messages has an adjacent distinct-`Msg` pair.
Final checks establish an ordinary complete-hash collision on Section 1.

## 4. Success for every fixed function

Identical to the n = 2^128 fixed-function argument: with Q = 2^256,

    Pr[all distinct] < e^(-1/2)·(1+2^(-128)),

and after Pr[E] < 2^(-257), Pr[success] > 0.39.

## 5. Fully charged RAM implementation

One 256-bit word is 32 bytes. Each selected five-round permutation costs one
unit; every other listed RAM primitive costs 1/1355 units (C = 1355).

| Activity | H calls (cost 1) | Ordinary ops (cost 1/1355) |
| --- | ---: | ---: |
| Initialize code, constants and fixed workspace | 0 | 2^24 |
| Initialize Msg and sort arrays | 0 | 12n |
| Generate, hash and retain n messages | n | 89n |
| Eight radix passes on two-word records | 0 | 88n |
| Eight radix passes: Count zero + exclusive prefix | 0 | 2^38 |
| Scan adjacent digests (+ message compare on hits) | 0 | 12n |
| Final reconstruction, verification and output | at most 2 | 2^18 |

**Init (12n).** ≤4n stores plus ≤8n address/control for `Msg`/`Src` setup.

**Generation wrapper (89n).** Same inventory as 128.22 (= envelope): random 2,
lane zeros 25, u/v packs ≤24, padding ≤8, squeeze ≤12, stores+loop ≤10, spare ≤8;
total ≤89. Permutation in H_calls only.

**Radix per-record work (11 ordinary ops per record per pass → 8 · 11n = 88n).**

Count phase (≤5): load h; shift; mask; load/add/store Count[d] as ≤3; loop
index increment shared into the 11-cap.

Scatter phase (≤6): load h; load idx; digit extract ≤1 beyond reused shift
state in a tight schedule (else ≤2 with one shared); cursor load/add/store ≤3;
store h and idx ≤2 — budgeted ≤6.

Sum ≤ 11 per two-word record per pass. Count-array work stays explicit (`2^38`).

**Adjacent scan (12n).** Unequal-path digest compare+loop ≤8; equal-path
message compares within 12.

**Verification.** Two wrappers (≤2 · 89) plus checks fit under 2^18, plus ≤2
permutation calls.

Summing, with n = 2^128,

    H_calls <= n + 2
    W <= (12 + 89 + 88 + 12)n + 2^24 + 2^38 + 2^18
       = 201n + 2^24 + 2^38 + 2^18
    T = H_calls + W/1355
      <= (1 + 201/1355)n + 2 + (2^24 + 2^38 + 2^18)/1355
       = (1556/1355)n + (2 + 274911067776/1355).

Now 1556/1355 < 1.149, and

    T < 1.149 · n + 2^39
      < 1.149 · 2^128 + 2^39
      < 1.150 · 2^128
      < 2^(0.201) · 2^128
      = 2^128.201.

Direct evaluation gives log2(T) ≈ 128.1995 < 128.2. The declared claim rounds
upward.

**Memory.** Msg + two sort arrays + Count + fixed < 2^136.

Claim fields: time_log2=128.2; memory_log2_bytes=136; preprocessing_log2=122;
nonuniform_advice_log2_bytes=0; success_probability=0.39.

## 6. Evidence and interpretation

Accounting tightening of a generic birthday algorithm, not a new cryptanalytic
break. Certificate manifest empty. Nominal reference 128 is not an established
attack; scalar 128.2 still exceeds it as an analytical bound.
submission_state=ready means complete for review, not qualified or promoted.

## 7. Source and accounting revision

Prior agent package claiming 128.22 used wrapper 89n, radix 8×12, scan 14n,
init 18n, W_coeff = 217, log2(T) ≈ 128.214. This package uses radix 8×11,
scan/init 12n, W_coeff = 201, log2(T) ≈ 128.1995, claim 128.2.

Hash-table/FKS paths were analyzed and not used (see preamble). Further cuts
approach the hashing floor ~128.0 with rising review risk on fusion.
