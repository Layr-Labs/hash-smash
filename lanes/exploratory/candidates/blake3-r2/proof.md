# Grouped partial-evaluation birthday search for 2-round BLAKE3

The scalar below is `time_log2` under `collision-frontier-v5` (C = 430 for
blake3-r2). Memory is a separately reported bound.

This exploratory package targets blake3-r2-prefix-v1. It is a generic birthday
search whose per-message cost is reduced by an exact structural property of
the 2-round compression: if a message varies only in word m15, then 7.5 of the
16 G calls (and small parts of the four round-2 column calls) are identical for
all such messages. We
evaluate 2^128 messages in 2^96 groups that share m0..m14, compute the
group-invariant half once per group, and evaluate each message with a counted
247-operation word-RAM program instead of a whole compression. Collisions are
detected with an uninitialised-memory sparse-set table at O(1) cost per
message. The claimed total is T < 2^127.4807 charged units, time_log2 =
127.481, with success probability 0.39 under one declared heuristic (H1).

This is not a differential or algebraic attack on BLAKE3. The improvement over
a whole-compression generic search is a constant factor (about 0.53 in log2),
obtained by not recomputing work that is provably identical across a group.

## 1. Exact complete hash

Each message is exactly 64 bytes, of bit length 512 < 2^64: sixteen 32-bit
little-endian words m0..m15. On these messages there is one chunk, one full
block, no parent, and exactly one compression with CHUNK_START | CHUNK_END |
ROOT = 11, true block length 64, chunk counter 0 and output counter 0. There is
no key, derivation flag, extra block, free-start state or supplied advice.

The eight-word IV is

    6a09e667 bb67ae85 3c6ef372 a54ff53a
    510e527f 9b05688c 1f83d9ab 5be0cd19.

Initialise v[0..7]=IV, v[8..11]=IV[0..3], v[12..15]=(0,0,64,11). Additions are
modulo 2^32 and ROR rotates right within a 32-bit lane. G(a,b,c,d,x,y) is

    v[a] = v[a]+v[b]+x; v[d] = ROR(v[d] XOR v[a],16)
    v[c] = v[c]+v[d];   v[b] = ROR(v[b] XOR v[c],12)
    v[a] = v[a]+v[b]+y; v[d] = ROR(v[d] XOR v[a],8)
    v[c] = v[c]+v[d];   v[b] = ROR(v[b] XOR v[c],7).

Round 1 calls, in order, with schedule s = m:

    G(0,4,8,12,s0,s1)  G(1,5,9,13,s2,s3)  G(2,6,10,14,s4,s5)  G(3,7,11,15,s6,s7)
    G(0,5,10,15,s8,s9) G(1,6,11,12,s10,s11) G(2,7,8,13,s12,s13) G(3,4,9,14,s14,s15)

Round 2 repeats these calls with s replaced by s[P[i]],
P=(2,6,3,10,7,0,4,13,1,11,12,5,9,14,15,8). Written in message words, round 2 is

    G(0,4,8,12,m2,m6)  G(1,5,9,13,m3,m10) G(2,6,10,14,m7,m0) G(3,7,11,15,m4,m13)
    G(0,5,10,15,m1,m11) G(1,6,11,12,m12,m5) G(2,7,8,13,m9,m14) G(3,4,9,14,m15,m8)

Only these two rounds are executed. The digest is LE4(o0)||...||LE4(o7) with
o[i] = v[i] XOR v[i+8], the first 32 root-output bytes. This is the ordinary
complete hash (verifier/blake3.py:blake3 with rounds=2) on the declared domain,
not a free-start, compression-only or truncated result. The final collision is
re-verified with two whole compressions of the reference function (Section 5).

## 2. Where m15 enters

In round 1, m15 is used only as the y input of the last call G(3,4,9,14,m14,m15).
Every earlier call, and the first half of that call (the lines using x = m14),
depend on m0..m14 only. In round 2, m15 is used only as the x input of the last
call G(3,4,9,14,m15,m8). Let S1 denote the state after round 1. For fixed
m0..m14, only the four words v3, v4, v9, v14 of S1 depend on m15; the other
twelve S1 words are group constants.

Each round-2 column call receives exactly one varying input word:

| Round-2 call | Inputs (a,b,c,d) | Varying input | Group-invariant prefix of the call |
| --- | --- | --- | --- |
| G(0,4,8,12,m2,m6) | v0,v4,v8,v12 | b = v4 | P0 = v0 + m2 |
| G(1,5,9,13,m3,m10) | v1,v5,v9,v13 | c = v9 | a' = v1+v5+m3, d' = ROR(v13 XOR a',16), Q1 = a'+m10 |
| G(2,6,10,14,m7,m0) | v2,v6,v10,v14 | d = v14 | a' = v2+v6+m7, Q2 = a'+m0 |
| G(3,7,11,15,m4,m13) | v3,v7,v11,v15 | a = v3 | P3 = v7 + m4 |

G uses its x input only through v[a]+v[b]+x, so any two of these three summands
can be pre-added; P0, P3, Q1 and Q2 are such pre-additions, kept unreduced
(< 2^33) and reduced by the single mask that follows the remaining addition.
Since (u mod 2^32 + w) mod 2^32 = (u + w) mod 2^32, the result is exact.

All four round-2 diagonal calls take varying inputs and are recomputed in full.

## 3. The two programs

Group setup, for prefix words m0..m14 (run once per group):

1. Initialise v as in Section 1 and execute the four round-1 column calls and
   the first three round-1 diagonal calls.
2. Execute the first half of G(3,4,9,14,m14,·): A1 = (v3+v4+m14) mod 2^32,
   D1 = ROR(v14 XOR A1,16), C1 = (v9+D1) mod 2^32, B1 = ROR(v4 XOR C1,12),
   and form AB = A1 + B1 (unreduced).
3. Form the round-2 pre-computations of the table in Section 2.
4. Keep the 27 group constants AB, D1, C1, B1, P0, v12, v8, m6, d', Q1, v5,
   a'(col 2), Q2, v10, v6, P3, v15, v11, v7, m13, m1, m11, m12, m5, m9, m14, m8.

Inner body, for y = m15 (run once per message). This is the exact program;
`experiments/grouped_birthday.py:inner` is the same code. Each line shows its
counted word operations (additions, XOR, AND, OR, shifts; ROR(x,r) for x < 2^32
is ((x>>r) OR (x<<(32-r))) AND MASK, four operations).

    a3  = (AB + y) & M;   d14 = ROR(D1 ^ a3, 8)         2 + 5
    c9  = (C1 + d14) & M; b4  = ROR(B1 ^ c9, 7)         2 + 5     = 14
    col 0: a=(P0+b4)&M 2, d=ROR(v12^a,16) 5, c=(v8+d)&M 2,
           b=ROR(b4^c,12) 5, a=(a+b+m6)&M 3, d=ROR(d^a,8) 5,
           c=(c+d)&M 2, b=ROR(b^c,7) 5                            = 29
    col 1: c=(c9+d')&M 2, b=ROR(v5^c,12) 5, a=(Q1+b)&M 2,
           d=ROR(d'^a,8) 5, c=(c+d)&M 2, b=ROR(b^c,7) 5           = 21
    col 2: d=ROR(d14^a',16) 5, c=(v10+d)&M 2, b=ROR(v6^c,12) 5,
           a=(Q2+b)&M 2, d=ROR(d^a,8) 5, c=(c+d)&M 2, b=ROR(b^c,7) 5 = 26
    col 3: a=(a3+P3)&M 2, then the remaining seven G lines with y=m13 = 29
    four full round-2 diagonal calls, 30 operations each           = 120
    o[i] = v[i] ^ v[i+8], i = 0..7                                 = 8
    total                                                          = 247

The count uses the organizer's counting convention from
`scripts/reference_operation_costs.py`: an int subclass that counts every add,
and, or, xor and shift. Applying that counter to this body gives exactly 247,
and to the group setup gives 241. In addition, 6,000 random (prefix, y)
evaluations of the body matched verifier/blake3.py:blake3(message, 2) bit for
bit. For comparison, the same convention charges 30 operations per G, so a
white-box whole compression costs 16*30 + 16 = 496 operations, which is more
than C = 430. Implementing whole compressions in word operations would
therefore cost more than one unit each; the saving here comes only from not
recomputing group-invariant work (the inner body is 247/496 = 0.498 of a
white-box compression).

Packing: K = o0; then K = (K<<32) | o[i] for i = 1..7 (14 operations). K is the
256-bit integer whose equality is full digest equality.

## 4. Complete algorithm

Parameters: L = 2^32 messages per group, G = 2^96 groups, N = G*L = 2^128
messages, sparse index width s = 140.

Memory: a prefix table PT of G records (two 256-bit words each), a record array
R of N records (K, id), and a sparse array P of 2^s one-word entries. P is never
initialised; R is written before it is read. n counts stored records.

For g = 0 .. G-1:

1. Draw two fresh independent uniform 256-bit words r0, r1; store them at
   PT[g]. Set m_k = (r0 >> 32k) & M for k = 0..7 and m_{8+k} = (r1 >> 32k) & M
   for k = 0..6 (m14 uses r1 bits 192..223; r1 bits 224..255 are unused).
2. Run group setup (Section 3). Set Gid = g << 32.
3. For y = 0 .. 2^32-1: run the inner body and packing to get K; set
   id = Gid | y; then the table step:

        idx = K >> (256-s); pa = Pbase + (idx << 5); r = load P[idx]
        if r < n:                               # R[r] is a real record
            ra = Rbase + (r << 6); k2 = load R[r].key
            if k2 == K: go to MATCH
            if (k2 >> (256-s)) == idx: go to NEXT   # slot held by another digest
        INSERT: ra = Rbase + (n << 6); store R[n].key = K;
                store R[n].id = id (address ra + 32); store P[idx] = n; n = n + 1
        NEXT:   y = y + 1; if y < 2^32 repeat

4. MATCH: decode both ids (g' = id >> 32, y' = id & M), reload PT[g'] and
   rebuild both messages, check the two 16-word messages differ, evaluate both
   with the reference complete hash (two whole root compressions), compare all
   eight output words. If all checks pass, output the pair and halt; otherwise
   halt with failure.

If the loops finish without MATCH, halt with failure. There is one pass, no
restart, at most one MATCH, and no adaptive stopping beyond halting early.

## 5. Correctness

Group messages are (m0..m14 from PT[g], m15 = y), so every evaluated message is
in the domain and ids decode uniquely to messages.

Sparse-set invariant (Briggs and Torczon). P may contain arbitrary values.
Records R[0..n-1] are always genuine. A slot idx is occupied iff P[idx] = r < n
and R[r].key >> (256-s) = idx. INSERT happens only for unoccupied slots, after
which P[idx] = n-1 makes it occupied; it is never overwritten later, since
every later visit to the slot finds the occupant. So each occupied slot holds
the first stored record with that index.

Lemma. If a record i is stored and a later message j has K_j = K_i, MATCH
occurs at or before j. Proof: idx(j) = idx(i) and that slot holds i, so r = i,
k2 = K_i = K_j.

A record i is not stored only if, when i arrived, its slot held a record k
with idx(k) = idx(i) and K_k != K_i (the K_k = K_i case is already a MATCH).
MATCH outputs a pair only after re-verifying distinct messages and equal
complete hashes with the reference function, so every output is an ordinary
full 256-bit collision of the selected 2-round hash.

## 6. Success probability

The algorithm's coins are the 2G uniform words r0, r1. Failure requires one of:

- F1: the N digests contain no equal pair;
- F2: some colliding pair (i < j, K_i = K_j) has i unstored, which requires an
  earlier k with idx(k) = idx(i) and K_k != K_i;
- F3: two groups draw identical 480-bit prefixes (then a MATCH can be between
  identical messages). Pr[F3] <= C(G,2) 2^-480 < 2^-287, exactly.

Heuristic H1 (declared in claim.json) treats the N grouped digests as N
independent uniform 256-bit values for these events. Under that model,
Pr[F1] <= exp(-N(N-1)/2^257) = exp(-(1 - 2^-128)/2) < 0.606531, by the standard
bound prod_{j<N}(1 - j/2^256) <= exp(-N(N-1)/2^257). For F2, the expected number
of triples (k, i, j) with k < i, j != i, idx(k) = idx(i) and K_i = K_j is at most
N^3 * 2^-s * 2^-256 / 2 = 2^(127-s) = 2^-13 < 0.000123. Hence under the model

    Pr[success] >= 1 - 0.606531 - 0.000123 - 2^-287 > 0.393345.

The claim is success_probability = 0.39, leaving an explicit allowance of
0.0033 for deviation of the grouped family from the model (H1). The value is
algorithmic success probability over r0, r1, not confidence in H1.

Some structure is provable. For two groups with independent uniform prefixes
and the same y, the digests collide with probability sum_z p_y(z)^2 >= 2^-256
for any fixed function, by Cauchy-Schwarz. Pairs with different y, and pairs
inside one group, are what H1 covers. Within-group pairs are a 2^-96 fraction
of all pairs, so the bound depends almost entirely on cross-group pairs whose
fifteen prefix words are independent and uniform.

## 7. Charged time

Per message, worst case path (insert after the full slot check):

| Work | Operations |
| --- | ---: |
| inner body (Section 3) | 247 |
| packing K | 14 |
| id = Gid OR y | 1 |
| table step: 5 shifts, 4 address adds, 2 loads, 3 compares, 3 branches, 3 stores, n+1 | 21 |
| loop: y+1, compare, branch | 3 |
| counted total | 286 |
| charged (adds 14 spare, e.g. for reloading group constants) | 300 |

The discard and early paths are shorter. Machine: 256-bit word RAM with 64
registers and three-address operations. Fourteen hold constants (MASK, shift
counts 16, 12, 20, 8, 24, 7, 25, 32, 116 = 256-s, the bound 2^32, and 1, 5, 6),
five hold Pbase, Rbase, n, y, Gid, 27 hold the group constants, and 18 hold the
16 working-state words and two rotation temporaries. Table temporaries reuse
state registers, which are dead after packing. Loads are charged wherever
memory is touched. Even if no group constant could stay in a register, the 27
reloads would raise the counted total to 313; the claim's 300 already covers
14 of them, and the bound with all 27 would be 2^127.5419 (Section 9).

Per group (2^96 times), at most 1024 operations are charged. The counted work
is 2 random draws, 28 unpacking operations, 5 to store PT[g], 241 for group
setup (measured with the same counter), Gid, y reset and 3 loop operations:
281 in total.

Once: global setup (constants, bases, n = 0, g = 0) at most 64 operations;
MATCH at most 2^10 operations plus two whole compressions (2 units).

Every operation outside the two verification compressions is charged at
1/C = 1/430 of a unit:

    T <= N*300/430 + G*1024/430 + 2 + (2^10 + 64)/430
      = 2^128 * 0.69767441860... + 2^96 * 2.38139... + 4.53...
      < 0.6976744192 * 2^128.

log2(0.6976744192) = -0.519374, so T < 2^127.48063 and the claim is
time_log2 = 127.481. This caps every run, successful or not. It covers random
draws, all failed and discarded messages, table work, verification and setup.
The "target compression costs one unit" price applies to the two compressions
that are invoked; all other computation, including the partial evaluations,
is charged per word operation. No compression's internals are charged twice
and none is omitted.

## 8. Memory and other resources

P: 2^140 words of 32 bytes = 2^145 bytes. R: 2^128 records of 64 bytes =
2^134 bytes. PT: 2^96 * 64 bytes = 2^102 bytes. Code, constants and registers
spill area < 2^24 bytes. Peak < 2^145 + 2^135 < 2^146 bytes; claimed
memory_log2_bytes = 146. Addresses stay below 2^147. P is never initialised,
so it costs no time; uninitialised contents cannot cause a wrong answer
(Section 5). preprocessing_log2 = 0 covers the global setup (< 1 unit). There
is no nonuniform advice (0; the schema cannot express log2 0).

## 9. Sensitivity

| Variation | Bound |
| --- | ---: |
| As claimed (300 operations per message) | 2^127.4807 |
| All 27 group constants reloaded every message (313) | 2^127.5419 |
| Charge a whole compression per message instead (rejects Section 3) | 2^128.1253 |

The claim stays below the current generic level (about 2^128) under any of
these readings except the last, which rejects partial evaluation altogether.

## 10. Evidence

Experiment b3r2-grouped-spread runs the exact grouped evaluator (Section 3)
with 32 groups of 32 consecutive y values per organizer seed: N_t = 1024 = 2^10
messages and a 20-bit masked event spread over all eight output words. N_t^2/2
equals 2^20/2, the same ratio as N^2/2 = 2^256/2 here. Experiment
b3r2-single-group puts all 1024 messages in one group with y = 0..1023, the most
structured case, under a different 20-bit mask. In both experiments the
organizer recomputes every returned pair with the trusted digest. This checks
the grouped evaluator, and so the 247-operation body, on genuine messages. The
random-model success rate is 1 - prod_{i<1024}(1 - i/2^20) = 0.3933; the
program also reports, as untrusted observations, how many masked-equal pairs it
saw per trial (expected 0.4995).

Local replay with locally chosen seeds (not organizer evidence), 4096 trials
per layout with the same `trial` function: the spread layout gave 1611
successes (random model 1610.8, z = 0.01) and 2071 masked pairs (expected
2046, sd 45), of which 48 first matches were within one group (model about 3%
of successes, i.e. 49); the single-group layout gave 1630 successes (z = 0.61)
and 2069 masked pairs. Individual 256-trial runs fluctuate with standard
deviation 7.8 around 100.7, as expected. A larger local run at width 32 used the same
`trial` function with N_t = 2^16 = 2^(32/2) and 300 seeds per configuration:
16 groups of 4096 consecutive y with the mask o0 (32 bits) gave 153 masked
pairs (expected 150.0) and 123/300 successes (expected 118.0); one group of
65536 consecutive y with a 32-bit mask spread over all words gave 155 pairs and
126/300 successes. All counts are within one standard deviation of the
random-function model.

## 11. Limitations

H1 is a heuristic. The experiments test 20-bit (and locally 32-bit) projections
of the digest, not the full 256-bit birthday event, which cannot be run.
Organizer seeds are public, not a blinded holdout. The 64-register machine is
a modelling assumption; Section 9 gives the bound without it. The improvement is a constant factor from amortising
group-invariant work; it is not a new cryptanalytic weakness of BLAKE3, and it
does not claim Pareto dominance (memory is much larger than a
distinguished-point walk's). The nominal reference identifier
blake3-r2-nominal-v2 is metadata and is not a claimed improvement over a
qualified baseline.
