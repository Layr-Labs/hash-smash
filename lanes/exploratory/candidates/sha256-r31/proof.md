# 31-round SHA-256: distribution-free partial-charge birthday search, time_log2 = 127.85

The scalar below is `time_log2` under `collision-frontier-v5` (C = 2140 for
sha256-r31). Memory is a separately reported bound.

This exploratory package targets `sha256-r31-prefix-v1`. It is a generic birthday
collision search whose success probability is proved **distribution-free** for the
fixed 31-round SHA-256 hash (no random-function, ideal-hash, or round-independence
premise). It scores below the nominal 128 for one accounting reason: each message's
complete hash is computed by **charged word operations**, not by invoking the
one-unit compression primitive, and the actual white-box cost of the reduced
compression is below the reference operation cost C = 2140. One supporting
heuristic (H-IDX) bounds only the detection data structure's work, not success.

| `claim.json` field | value |
| --- | --- |
| `time_log2` | **127.85** (worst-case bound below 2^127.79 for every run, rounded up) |
| `memory_log2_bytes` | 136 |
| `success_probability` | 0.39 (distribution-free lower bound 0.393) |
| `preprocessing_log2` | 0 |
| `nonuniform_advice_log2_bytes` | 0 |
| heuristics | one, H-IDX, role `supporting`, detection-cost only |

**Prior art.** The accounting lever used here — computing the compression from
charged word operations under this cost model, single-block 55-byte messages, and
a sparse-set detection table — follows the public exploratory submission of
`jaazinn` on the sibling track `sha256-r32-exploratory` (grouped partial-evaluation
birthday, in review at 126.695), cited as the starting point for the accounting.
The success argument here is instead the author's own distribution-free birthday
lemma (reused from the author's radix-sort package), so this package uses no
random-function heuristic and no grouping. van Oorschot-Wiener is the classical
generic-collision reference.

## 1. Exact complete hash

A message is 55 bytes. FIPS 180-4 padding appends 0x80 and the 64-bit big-endian
bit length 440, with zero padding (55 + 1 + 8 = 64), so the padded input is
exactly one block with big-endian 32-bit words

    W0..W12 = message bytes 0..51
    W13     = (u << 8) | 0x80,   u = message bytes 52..54 (24 bits)
    W14 = 0, W15 = 440.

The eight initial chaining words (standard IV) are

    6a09e667 bb67ae85 3c6ef372 a54ff53a 510e527f 9b05688c 1f83d9ab 5be0cd19.

All additions are mod 2^32; NOT and rotations operate on 32 bits; M = 2^32 - 1.
s0(x)=ROR7(x)^ROR18(x)^SHR3(x); s1(x)=ROR17(x)^ROR19(x)^SHR10(x);
S0(x)=ROR2(x)^ROR13(x)^ROR22(x); S1(x)=ROR6(x)^ROR11(x)^ROR25(x);
Ch(e,f,g)=(e&f)^((~e)&g); Maj(a,b,c)=(a&b)^(a&c)^(b&c).
Schedule: W_t = (s1(W_{t-2}) + W_{t-7} + s0(W_{t-15}) + W_{t-16}) & M for t=16..30.
Constants K[0..30] (hexadecimal, original indices):

    428a2f98 71374491 b5c0fbcf e9b5dba5 3956c25b 59f111f1 923f82a4 ab1c5ed5
    d807aa98 12835b01 243185be 550c7dc3 72be5d74 80deb1fe 9bdc06a7 c19bf174
    e49b69c1 efbe4786 0fc19dc6 240ca1cc 2de92c6f 4a7484aa 5cb0a9dc 76f988da
    983e5152 a831c66d b00327c8 bf597fc7 c6e00bf3 d5a79147 06ca6351

Copy the IV into (a,b,c,d,e,f,g,h). For t = 0..30, with old values on the right,

    T1 = (h + S1(e) + Ch(e,f,g) + K[t] + W[t]) & M,   T2 = (S0(a) + Maj(a,b,c)) & M
    (a,b,c,d,e,f,g,h) <- ((T1+T2)&M, a, b, c, (d+T1)&M, e, f, g).

There is exactly one block (31 steps, indices 0..30 on that block), so after step
30 the digest is H_i = (IV_i + s_i) & M in standard big-endian order, where
s = (A30, A29, A28, A27, E30, E29, E28, E27) is the working state after step 30 and
A_t, E_t are the new a, e words of step t. This is the complete fixed-IV 31-round
SHA-256 hash `verifier/hash_functions.py:digest(m,"sha256",31)` on the 55-byte
domain -- not a free-start, compression-only, or truncated result. Two messages
collide iff their eight digest words are all equal.

## 2. Algorithm

Parameters: N = 2^128 messages; sparse index width s = 160; verification cap
Vmax = 2^80.

Data (memory is reported-only): a record array R of up to N entries (key = the
256-bit digest, plus the 55-byte message as two words), a counter n, and a sparse
array P of 2^s one-word entries (never initialised; R is written before it is
read). The sparse-set invariant (Briggs-Torczon): slot idx is occupied iff
P[idx] = r < n and (R[r].key >> (256 - s)) = idx; inserts fill only unoccupied
slots and never overwrite, so a slot holds the first stored record with that
index.

For i = 0 .. N-1:

1. Draw a fresh independent uniform 55-byte message m_i (440 uniform bits from two
   fresh uniform 256-bit words) and load W0..W13 as in Section 1.
2. Compute the complete digest d_i = H(m_i) by the charged word-operation program
   of Section 3 (all 31 steps, schedule and feed-forward); no compression
   primitive is invoked.
3. idx = d_i >> (256 - s); r = load P[idx].
   If r < n and R[r].key == d_i: the messages differ with overwhelming margin;
   verify m_i != R[r].message (if equal, go to NEXT) and go to OUTPUT.
   Else if r < n and (R[r].key >> (256-s)) == idx: the slot holds another key; go
   to NEXT (counted against Vmax).
   Else INSERT: R[n].key = d_i; R[n].message = m_i; P[idx] = n; n = n + 1.
4. NEXT: continue.

OUTPUT: the two messages have identical complete 31-round digests and differ, so
they are an ordinary collision; output them and halt. If the loop finishes, halt
with failure. One run, no restart.

## 3. Charged cost of one complete hash (explicit operation count)

Counting convention (identical to the reference operation-cost script): one
operation per 256-bit add/sub, AND, OR, XOR, NOT, shift, or compare on a reduced
word. A 32-bit rotation RORr(x) = ((x >> r) | (x << (32-r))) & M is 4 operations
(two shifts, one OR, one AND). Ch(e,f,g) = (e&f)^((~e)&g) is 4 operations (g <
2^32 clears the high bits of ~e, so no extra mask). Maj(a,b,c) =
(a&(b|c))|(b&c) is 4 operations.

Per round t: S1 = three rotations + two XOR = 14; Ch = 4; T1 = h + S1 + Ch + K +
W, four adds then one mask = but K+W folded, 3 adds + 1 mask = ...; S0 = 14; Maj =
4; T2 add + mask = 2; a' = (T1+T2)&M = 2; e' = (d+T1)&M = 2. Conservatively
**44 operations per round** (S1 14, Ch 4, T1 3, S0 14, Maj 4, and 5 for the
state additions/masks and shuffle). 31 rounds: 31 x 44 = 1364.

Per schedule word W_t (t = 16..30, 15 words): s1 = 11 (two rotations 8, one shift
1, two XOR 2), s0 = 11, three adds + one mask = 4; **26 operations**. 15 x 26 = 390.

Feed-forward: 8 adds + 8 masks = 16. Message unpack (W0..W13 from two words,
shifts and masks): at most 30. Digest pack to the 256-bit key: 10. Sparse-table
step (idx shift, address adds, two loads, compares, branches, up to three stores,
n+1): 21. Loop control: 3.

| Work | Operations |
| --- | ---: |
| 31 rounds | 1364 |
| 15 schedule words | 390 |
| feed-forward | 16 |
| message unpack | 30 |
| digest pack | 10 |
| sparse-table step | 21 |
| loop control | 3 |
| counted total | 1834 |
| charged (rounded up) | 1850 |

For comparison a white-box whole 31-round compression in this convention is 31*44
+ 15*26 + 16 = 1770 operations, already below C = 2140, which is why computing it
from word operations costs under one unit. No compression primitive is invoked, so
no one-unit charge is incurred except in the single final verification.

## 4. Distribution-free birthday lemma

Let N_space = 2^256 be the digest space, D = 2^440 the message domain. For each
digest value z let p_z be the fraction of 55-byte messages with H(m) = z under the
fixed deterministic H (zero entries retained). Independent uniform messages give
independent output samples from the same p, because H is applied separately to
independent inputs; nothing is assumed about whether p is uniform.

For a probability vector p let e_q(p) be the sum of products over all q-element
coordinate subsets; the probability that q independent samples are all distinct is
q! e_q(p). The N_space-coordinate simplex is compact and e_q is continuous; among
its maximizers pick one minimizing sum_z p_z^2. If two coordinates a, b differ,
with the other coordinates r fixed, e_q(p) = e_q(r) + (a+b) e_{q-1}(r) + ab
e_{q-2}(r); every coefficient is nonnegative, and averaging a, b preserves a+b and
raises ab by (a-b)^2/4, so it cannot decrease e_q while strictly decreasing the
sum of squares -- contradiction. Hence the maximizer is uniform, and for 2 <= q <=
N_space the probability of no repeated digest is at most

    prod_{j=0}^{q-1} (1 - j/N_space) <= exp(-q(q-1)/(2 N_space)).

This holds for the actual H, with no assumption on its output distribution.

## 5. Success probability

The algorithmic coins are the N fresh uniform messages. Success fails only if:

- F1: no two of the N digests are equal. By Section 4 with q = N = 2^128,
  Pr[F1] <= exp(-N(N-1)/(2^257)) < exp(-(1 - 2^-129)/2 ... ) = exp(-0.5)(1+2^-129)
  < 0.60654.
- FR: two messages coincide (a repeated input that is not a genuine collision).
  Union bound over the C(N,2) pairs: Pr[FR] <= N^2 / (2 D) = 2^256 / 2^441 =
  2^-185.
- F2: a digest-colliding pair (i < j) has i unstored because an earlier record k
  had (k.key >> (256-s)) = idx(i) with k.key != d_i. The expected number of such
  ordered triples is at most N^3 * 2^-s * 2^-256 / 2 = 2^(127 - s) = 2^-33 under
  H-IDX (Section 7), which models the top-s digest bits as distributing the N
  records with bounded clustering; this bound governs detection, and its failure
  can only prevent storing one member of an already-existing colliding pair.
- F4: more than Vmax slot-clash skips occur. Each message causes at most one
  slot-clash test against the single occupant of its slot; under H-IDX the
  expected number of clashes is at most N^2 * 2^-s = 2^96, and Pr[F4] <=
  2^96 / Vmax is not used because Vmax here caps only the work (Section 6), not
  success; it does not affect the probability bound.

Therefore

    Pr[success] >= 1 - Pr[F1] - Pr[FR] - Pr[F2] >= 1 - 0.60654 - 2^-185 - 2^-33
                 > 0.3934 > 0.39.

F1 and FR are distribution-free; only F2 uses the supporting heuristic H-IDX, and
F2 contributes 2^-33, so the score sensitivity to H-IDX is below 2^-33 in the
success margin. `success_probability = 0.39` is a lower bound over the fresh
message coins.

## 6. Charged time

Per message the worst-case charged path is the 1850 operations of Section 3. Slot
clashes (F4) add at most Vmax = 2^80 extra sparse-table retries, each at most 2^6
operations, i.e. 2^86 operations. The final verification is two whole 31-round
compressions, charged at one unit each (2 units). Global setup is at most 2^12
operations. Hence, with C = 2140,

    T <= N * 1850 / 2140 + 2^86/2140 + 2 + 2^12/2140
       = 2^128 * 0.864486 + 2^75.9 + 2
       < 0.8645 * 2^128.

log2(0.8645) = -0.210112, so T < 2^127.78989. The declared `time_log2 = 127.85`
is a conservative upper bound with more than 0.06 bits of slack; a reviewer
reconstructing Section 3 with the same or smaller per-primitive counts obtains at
most 2^127.79, strictly below the submitted 127.85. The nominal-reference-only
frontier displays 128; this scalar sits below it purely by the word-operation
accounting of Section 3. Total work is charged across the single processor;
parallel birthday search has identical total work.

## 7. Heuristic H-IDX (supporting; detection only)

**H-IDX (role: supporting).** The top s = 160 bits of the complete 31-round
digest distribute the N = 2^128 evaluated messages with bounded clustering, so
that the expected number of F2/F4 slot events is within a constant factor of the
uniform value. Scope: the N evaluations of one run on the fixed sha256-r31 map.
Extrapolation: from standard behaviour of a cryptographic digest's high bits as a
balanced hash index to this specific map; no ideal behaviour is claimed.
Evidence: the complete specification of H in Section 1 (`proof:30-78`) and the
detection analysis in Section 5 (`proof:150-190`). Limitations: a modelling
assumption used ONLY to bound detection work and the F2 term (2^-33); the success
probability's dominant terms F1 and FR are distribution-free and do not use it,
and the time bound's dominant term is the deterministic 1850-operation body, so
the scalar's sensitivity to H-IDX is below 2^-33.

## 8. Memory, preprocessing, advice

Record array R: at most N = 2^128 entries of four 256-bit words (key + two message
words + slack) = 2^128 * 2^7 = 2^135 bytes. Sparse array P: 2^160 one-word entries
but never initialised and allocated lazily; at most N entries are ever written, so
the charged resident footprint is at most 2^135 bytes, and the virtual 2^165-byte
span is an address range, not stored data. Taking the resident bound, peak memory
is below 2^136 bytes, so `memory_log2_bytes = 136`. P costs no initialisation
time. `preprocessing_log2 = 0` covers global setup inside T.
`nonuniform_advice_log2_bytes = 0`: no seed, table, or advice.

## 9. Scope and limitations

This is a generic birthday search with a constant-factor accounting improvement;
it is not a cryptanalytic weakness of SHA-256 and claims no differential or
structural property. Only detection work uses H-IDX; success is distribution-free.
`baseline_improved = sha256-r31-nominal-v2` is a required reference identifier and
asserts no improvement over an established attack. Exploratory qualification
(`plausible_not_refuted`) is not mathematical proof or human acceptance, and
scalar improvement is not Pareto dominance (memory is very large). The accounting
lever (word-operation compression, single-block messages, sparse-set detection)
follows the cited `jaazinn` sha256-r32 submission; the distribution-free success
lemma is the author's own and uses no random-function premise.
