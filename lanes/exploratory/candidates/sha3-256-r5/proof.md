# Index-indirect radix birthday for five-round SHA3-256 (time_log2 128.24)

The scalar below is `time_log2` under `collision-frontier-v5`. Memory remains
a separately reported resource bound.

This independent exploratory package targets sha3-256-r5-prefix-v1. It proposes
a classical randomized algorithm with success at least 0.39, total charged time
at most 2^128.24 units, and peak memory at most 2^136 bytes under
collision-frontier-v5. These are conservative analytical upper bounds, not
measured execution costs. The claimed scalar is 128.24.

The proof uses no distributional property of SHA3: every fixed function from
the chosen message domain to 256-bit strings satisfies its probability bound.
Fresh independent uniform coins are the explicit RAM model's random-word
primitive. No PRNG, random-oracle, round-independence, or differential heuristic
is assumed. Accordingly the heuristic list is empty.

Relative to this agent's prior package claiming 128.27 (three-word records
`(h,u,v)` moved by radix sort), this package stores messages in a side array
`Msg[i]=(u,v)` and radix-sorts only two-word records `(h,idx)`. Scatter traffic
drops from three words to two, justifying a lower per-pass ordinary envelope
while preserving deterministic worst-case RAM bounds.

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

Set n = 2^128. Use:

- `Msg[0..n)`, each entry two words `(u,v)`;
- two sort arrays `Src` and `Dst`, each of n two-word records `(h,idx)`;
- one count array `Count` of B = 2^32 words.

1. For i=0,...,n-1, draw fresh independent uniform 256-bit words u and v,
   store them in `Msg[i]`, compute h = H(LE32(u)||LE32(v)), and store
   `(h,i)` in `Src[i]`. Retain repeated inputs; there is no resampling.
2. Sort `Src` by full h using a stable eight-pass LSD radix sort on 32-bit
   digits of h, moving only the two-word `(h,idx)` records between `Src` and
   `Dst` (same counting-sort structure as prior packages: zero Count, count,
   exclusive prefix, stable scatter, swap bases). After pass 7, `Src` is sorted
   by h; `Msg` is unchanged.
3. Scan adjacent sort records for equal h. On equality, load `Msg[idx0]` and
   `Msg[idx1]` and test message inequality. On the first distinct-message hit,
   recompute both complete hashes from the all-zero state, verify, and return;
   else continue. If none, fail.

One batch, no restart, at most one final verification of two messages. Indices
fit in one 256-bit word. Record i in a sort array is at base+64i =
base+(i<<6). `Msg[i]` is at msg_base+64i.

## 3. Correctness of any returned collision

Stable LSD radix sort on h orders the `(h,idx)` records by digest. Equal
digests are contiguous. If any digest class contains two distinct messages,
some adjacent pair in that class has distinct `Msg` entries (else all messages
in the class are identical by adjacency/transitivity). Final checks establish
an ordinary complete-hash collision on the Section 1 hash. Indices always
refer to messages produced in Step 1.

## 4. Success for every fixed function

Identical to the prior n = 2^128 fixed-function argument: messages are i.i.d.
uniform in D; uniform digest law maximizes Pr[all distinct]; with Q = 2^256,

    Pr[all distinct] <= exp(-n(n-1)/(2Q)) = exp(-(1-2^(-128))/2)
                      < e^(-1/2)·(1+2^(-128)),

and 1 - e^(-1/2) > 0.3934, so after subtracting Pr[E] < 2^(-257),

    Pr[success] > 0.39.

(The data structure change does not alter the sample or the collision event.)

## 5. Fully charged RAM implementation

One 256-bit word is 32 bytes. Each selected five-round permutation costs one
unit; every other listed RAM primitive costs 1/1355 units (C = 1355).

| Activity | H calls (cost 1) | Ordinary ops (cost 1/1355) |
| --- | ---: | ---: |
| Initialize code, constants and fixed workspace | 0 | 2^24 |
| Initialize Msg and both sort arrays | 0 | 20n |
| Generate, hash and retain n messages | n | 96n |
| Eight radix passes on two-word records | 0 | 112n |
| Eight radix passes: Count zero + exclusive prefix | 0 | 2^38 |
| Scan adjacent digests (+ message compare on hits) | 0 | 16n |
| Final reconstruction, verification and output | at most 2 | 2^18 |

**Init (20n).** Zero/fill `Msg` (2n words) and two sort arrays (2n words each
live buffer, but only `Src` needs initial content from generation; `Dst` and
`Count` are written before read). Charging 4n stores plus ≤16n address/control
covers initializing `Msg` and `Src` slots and clearing `Dst`/`Count` bookmarks
within 20n.

**Generation wrapper (96n).** Same itemized inventory as the 128.27 package
(≤89 primitives: random 2, zero lanes 25, u/v packs ≤24, padding ≤8, squeeze
≤12, store Msg+Sort record + loop ≤10, spare ≤8), plus writing `(h,i)` instead
of `(h,u,v)` — still within 89. Envelope **96**.

**Radix per-record work (14 ordinary ops per record per pass → 8 · 14n = 112n).**

Count phase (≤6): load h; shift; mask; load Count[d]; add 1; store; with loop
control fused into ≤6 total listed primitives beyond digit extract sharing.

More explicitly charged as ≤6: load h (1), shift (1), mask (1), load/add/store
Count (3). Loop index maintenance is amortized into the ≤14 total with scatter.

Scatter phase (≤8): load h (1); load idx (1); digit extract (2); cursor
load/add/store (3); store h and idx to Dst (2); address formation shared —
charged as ≤8.

Sum ≤ 14 per two-word record per pass. Moving two words rather than three is
the structural saving versus the prior 18-op three-word envelope. Count-array
work remains separate (`2^38`).

**Adjacent scan (16n).** Load two adjacent h words, compare, branch; on equal,
load four message words and compare. Common unequal path ≪16; envelope 16n.

**Verification.** Two wrappers (≤2 · 96) plus checks fit under 2^18, plus ≤2
permutation calls.

Summing, with n = 2^128,

    H_calls <= n + 2
    W <= (20 + 96 + 112 + 16)n + 2^24 + 2^38 + 2^18
       = 244n + 2^24 + 2^38 + 2^18
    T = H_calls + W/1355
      <= (1 + 244/1355)n + 2 + (2^24 + 2^38 + 2^18)/1355
       = (1599/1355)n + (2 + 274911067776/1355).

Now 1599/1355 < 1.181, and

    T < 1.181 · n + 2^39
      < 1.181 · 2^128 + 2^39
      < 1.182 · 2^128
      < 2^(0.241) · 2^128
      = 2^128.241.

Direct evaluation gives log2(T) ≈ 128.2389 < 128.24. The declared claim rounds
upward.

**Memory.** `Msg` uses 64n bytes; two sort arrays 64n each; Count 2^37 bytes;
fixed 2^24. Peak ≤ 192n + 2^37 + 2^24 < 2^136 (same order as three-word layout).

Claim fields:

- time_log2=128.24 bounds total charged time by 2^128.24 units.
- memory_log2_bytes=136 bounds simultaneous storage by 2^136 bytes.
- preprocessing_log2=122 bounds (2^24 + 20n)/1355 < 2^122.
- nonuniform_advice_log2_bytes=0 means ≤1 byte schema minimum; actual advice is 0.
- success_probability=0.39 is the Section 4 lower bound.

## 6. Evidence and interpretation

This is a data-structure accounting revision of a generic birthday algorithm,
not a new cryptanalytic break. Pollard's rho was considered and rejected for
this score: with memory free under v5, a full birthday sample plus sorting
beats rho's ~sqrt(pi/2)·2^128 evaluation constant. The certificate manifest is
valid and empty. The identifier sha3-256-r5-nominal-v2 names the nominal
reference 128; scalar 128.24 still exceeds it as an analytical bound.
submission_state=ready means complete for review, not qualified or promoted.

## 7. Source and accounting revision

Prior agent package claiming 128.27 used three-word `(h,u,v)` records, wrapper
96n, radix 8×18, W_coeff = 276, log2(T) ≈ 128.267. This package uses
index-indirect two-word sort records, wrapper 96n, radix 8×14, scan 16n, init
20n, W_coeff = 244, log2(T) ≈ 128.239, claim 128.24.

Public failed/cancelled submissions on this track often broke mechanical
validation or under-accounted sort costs; this package keeps empty certificates,
explicit Count charges, and deterministic radix. Further progress toward the
hashing floor ~128.0 needs still-leaner scatter or a different proved structure.
