# Grouped partial-evaluation + 8-way SWAR birthday search for two-round BLAKE3

## 1. Claim and scope

Target: `blake3-r2-prefix-v1`. Lane: exploratory. Attack class: ordinary
collision. The selected hash is unkeyed BLAKE3-256 with the standard IV, the first
two compression rounds (0 and 1) with the standard message permutation between
them, the standard feed-forward, and the complete 256-bit root output. Neither the
round convention nor the hash domain is changed. Messages are exactly 64 bytes, so
each is a single chunk whose single block is the root block: one compression with
flags `CHUNK_START|CHUNK_END|ROOT` (= 11), `block_len` 64, `counter` 0, digest =
the first eight output words.

This package combines two public levers on this track: the **grouped
partial-evaluation** of jaazinn (`0a5b7ae8`, 127.481) and winglock (`3022205`,
127.252) — amortise the m15-invariant half of the compression over a group — and
our **8-way SWAR packing** of the 32-bit BLAKE3 word (our in-review
blake3-r2 independent-message package, 126.67). The m15-dependent inner body is
packed eight messages per 256-bit word.

Under `collision-frontier-v5`, with C = 430:

| Resource | Upper bound |
| --- | --- |
| Total computation | 2^125.98 target-compression equivalents |
| Peak memory (reported only) | 2^167 bytes |
| Preprocessing | no separate precomputed table; group setup is amortised inside the total |
| Probability of returning an ordinary collision | at least 0.39 |
| Nonuniform advice | zero bytes |

This is an analytical algorithm with astronomically large memory and work; it is
not a measured collision. Its improvement is implementation and accounting
(grouped amortisation + eight-way packing + an uninitialised table), not a new
differential attack on BLAKE3. The score-critical heuristic H1 (Sections 6-8) is
jaazinn's premise: the grouped digests behave like independent uniform values for
the events F1 (collision existence), F2' (table displacement) and Fcap
(confirmation cap). The identical-group-prefix event F3 is bounded exactly.

## 2. Exact messages, grouping, padding, and digest

Set n = 2^128 = 2^96 groups of g = 2^32. For each group, draw 15 fresh uniform
32-bit words m0..m14 (480 bits, the group prefix) and enumerate m15 = 0..2^32-1. A message
is the 64-byte string of m0..m15 (little-endian). Repeated messages are retained
and charged. There is one pass, no adaptive sampling, no restart.

Each message is a single 64-byte root block. Following `verifier/blake3.py`, the
hash is one compression

    v = cv(=IV[0..7]), IV[0..3], counter_lo(=0), counter_hi(=0), block_len(=64), flags(=11)

then two rounds of eight G calls with the message permutation
PERMUTATION = (2,6,3,10,7,0,4,13,1,11,12,5,9,14,15,8) between them, then the
feed-forward `o_i = v[i] XOR v[i+8]`. The digest is `struct.pack("<8I", o0..o7)`.
The words `v[i+8] XOR cv[i]` of the sixteen-word output are not part of the 256-bit
digest and are never computed. Each confirmation recomputes this complete hash
with the reference compression.

The round map is the BLAKE3 quarter-round in the fixed schedule of
`verifier/blake3.py`:

    G(a,b,c,d,x,y):
      v[a] = (v[a]+v[b]+x) mod 2^32 ; v[d] = ror32(v[d] XOR v[a], 16)
      v[c] = (v[c]+v[d]) mod 2^32   ; v[b] = ror32(v[b] XOR v[c], 12)
      v[a] = (v[a]+v[b]+y) mod 2^32 ; v[d] = ror32(v[d] XOR v[a], 8)
      v[c] = (v[c]+v[d]) mod 2^32   ; v[b] = ror32(v[b] XOR v[c], 7)

G uses only 32-bit modular addition, XOR, and right rotation; no AND, OR or NOT.
These are FIPS-public, organizer-fixed facts.

## 3. Eight independent lanes in one word (SWAR lemmas)

For eight 32-bit values define `pack(a0,...,a7) = sum_j a_j 2^{32 j}`. All attack
registers hold 256-bit values mod 2^256; there are no wider operations. Let

    H    = pack(2^31,...,2^31)          notH = pack(2^31-1,...,2^31-1)
    L_r  = pack((2^r-1)2^{32-r},...)    R_r  = pack(2^{32-r}-1,...)

be literal program constants (built in setup).

**Rotation lemma.** For 0<r<32, with five operations,
`Y = ((X >> r) AND R_r) OR ((X << (32-r)) AND L_r)` gives
`Y = pack(ror32(a0,r),...,ror32(a7,r))`. In field j the first term contributes
source bits at positions k<32-r and the second at k>=32-r; `AND R_r`/`AND L_r`
discard every bit the global shift moved across a field boundary, and both
surviving supports come from field j. The four BLAKE3 amounts 16,12,8,7 lie in
(0,32), so each rotation costs five operations.

**Addition lemma (carry isolation).** With six operations,
`z = ((X AND notH) + (Y AND notH)) XOR ((X XOR Y) AND H)` gives field j equal to
`(a_j + b_j) mod 2^32`. Write a_j = 2^31 u_j + p_j, b_j = 2^31 w_j + q_j with
u_j,w_j in {0,1}, 0<=p_j,q_j<2^31. The masked operands have field j equal to
p_j, q_j < 2^31, so the field sum p_j+q_j < 2^32 and no carry crosses into field
j+1; its bit 31 is the carry c_j out of bit 30. The second term sets bit 32j+31 to
u_j XOR w_j. XORing, field j of z has bits 0..30 of p_j+q_j and bit 31 equal to
c_j XOR u_j XOR w_j = (u_j+w_j+c_j) mod 2, the true modular-sum bit. QED. A
three-input add `v[a]+v[b]+x` is two applications (12 operations); the intermediate
is already reduced, so the second application's precondition holds. No separate
`& 2^32-1` reduction is needed.

**Packed-round lemma.** Replacing each 32-bit XOR, addition and rotation by the
field-wise op, the addition lemma and the rotation lemma, and broadcasting each
fixed word to all eight fields, every field of every packed register equals the
corresponding ordinary BLAKE3 value after the same step; the message permutation
relabels registers. This is an algebraic identity (checked bit-for-bit, Section
10).

## 4. Grouped partial-evaluation and the packed inner body

**Dependency on m15** (jaazinn's observation, verified here). In round 1, m15 is
the y input of the last G call G(3,4,9,14,m14,m15); it enters only at that call's
fifth line `v[3] = v[3]+v[4]+m15`. Its first four lines (using m14) and every
earlier G call are **m15-invariant group constants**. After round 1, only state
words v3, v4, v9, v14 depend on m15. The permutation sends m15 to index 14, so in
round 2 m15 is the x input of the last G call; and once the round-2 column calls
run, every state word depends on m15.

**Group setup (scalar, once per group, amortised).** Run round 1's first seven G
calls and the first half of the eighth, obtaining a base state in which the twelve
words v0,v1,v2,v5,v6,v7,v8,v10,v11,v12,v13,v15 hold their final round-1 values and
v3,v4,v9,v14 hold their pre-m15 half-values; additionally precompute the invariant
sum `S3 = (v3_half + v4_half) mod 2^32` (so the inner body's first line is a single
add of m15). Also form the permuted round-2 message words (all group constants
except index 14 = m15). This is at most a few hundred scalar operations; charged
<= 2^20 per group, i.e. <= 2^20 / 2^32 = 2^-12 per message.

**Packed inner body (per batch of eight m15 values).** Broadcast the group
constants to eight fields once per group. For a batch, pack eight consecutive m15
values and run:

| Step | Operations (8 lanes) |
| --- | ---: |
| round-1 tail: `v3 = padd(S3, m15)` | 6 |
| `v14 = pror(v14 XOR v3, 8)` | 6 |
| `v9 = padd(v9, v14)` | 6 |
| `v4 = pror(v4 XOR v9, 7)` | 6 |
| round 2: eight packed G calls, 60 each | 480 |
| feed-forward `o_i = v[i] XOR v[i+8]`, i=0..7 | 8 |
| **inner body total per batch of 8** | **512** |

= 64 operations per message. Each packed G call is
`12 + 6 + 6 + 6 + 12 + 6 + 6 + 6 = 60` (two three-input adds at 12 each = 24, two
single adds at 6 each = 12, four rotation-XORs at 6 each = 24). The 480 for round 2 counts every G call in full: once a
varying word enters a column call, the call's outputs are varying, so round 2 is
packed in full; only the strictly m15-invariant round-1 prefix is shared. This
count was reproduced mechanically by an operation-counting `int` subclass with the
convention of `scripts/reference_operation_costs.py` (C = 430 for one whole
compression): the inner body executes 512 counted operations for eight messages.

(A variant that additionally moves the two invariant column prefixes of round 2 —
columns 1 and 2, which receive their varying word in roles c and d — into group
setup saves about 18 operations per batch, ~0.3 extra bits; it is not used here, to
keep the shared/packed split simple and auditable.)

## 5. Generation, memory

Per group: 14 random words for the prefix and the group setup (amortised). Per
message: m15 is the enumeration counter; the packed m15 word for a batch is one
add of a broadcast base and a fixed lane-offset constant (charged in generation).
A group record is the stored prefix m0..m14 (480 bits, once per group) plus the
counter; its id = group*2^32 + m15. Charge 2 operations per message for
generation (counter, packed-m15 formation, store bookkeeping); the per-group
prefix draw and stores are amortised.

Memory (reported only): the sparse index at base 2^160 (addresses < 2^161 words),
the dense confirmation array (<= n records), and the per-group prefixes. Every
address is below 2^161 words = 2^166 bytes; we report 2^167. Fewer than 2^135
bytes are written.

## 6. Uninitialised sparse-set collision table

We adopt the **never-displaced Briggs-Torczon sparse-set structure and validity
test** of the prior-art packages (jaazinn `0a5b7ae8`, winglock `3022205`), cited as
prior art; the key here is o0..o4 (any 160 fixed digest bits work — a full-digest
collision has all words equal, so equal keys either way; winglock used o0..o3,o5).
It replaces a fully charged sort (whose radix passes cost ~176 ops/message at this
C and would exceed the frontier).

A *sparse* array S is indexed by the 160-bit key at `addr = 2^160 | K`; a *dense*
array `Dkey, Did` is indexed by an insertion counter `cnt`. A slot is **valid**
iff `p = S[addr]` satisfies `0 <= p < cnt` and `Dkey[p] == K`. An uninitialised
(garbage) slot cannot forge a match: either `p >= cnt` (range test) or `Dkey[p] !=
K` (key test). Per-message key extraction (lane j of o0..o4): `f_i = (o_i >> 32 j)
AND (2^32-1)` (2 ops each, 10) then `K = f0 | f1<<32 | ... | f4<<128` (8 ops) = 18
operations. Per-message table step (12 operations): `addr = 2^160 OR K` (1); `p =
load S[addr]` (1); range compare+branch (2); key load+compare+branch (3); on a
miss, `Dkey[cnt]=K`, `Did[cnt]=id`, `S[addr]=cnt`, `cnt+=1` (2 stores + 1 store +
1 add).

## 7. Recovering and checking a collision; table events

The table keeps the first entry for each key. A full-digest collision between
distinct messages y, z has K_y = K_z; when the second is processed its slot holds
the first message with that key, so the pair is confirmed unless an earlier
different-digest message squats the slot. On a confirmation, reconstruct both
messages from their stored group prefixes and counters, check they differ,
recompute both complete two-round digests with the reference compression (two
charged units), and return the pair if all 256 bits agree. Halt on the first
returned pair. At most 2^110 confirmations, each <= 2 units plus <= 128
reconstruction operations, total below 2^111.2 units.

Failure events (bounded under H1 in Section 8): **F2'** (the first colliding pair's
slot is squatted by an earlier different-digest message with the same 160-bit key);
**Fcap** (more than 2^110 key-colliding confirmations). A radix-sort variant
removes H1 from these events (+~176 ops/message, time_log2 ~127.74), and our
independent-message package removes H1 from F1 (time_log2 126.67); both are
distribution-free fallbacks below the 128 nominal reference.

## 8. Success probability under H1

The grouped messages are not independent (a group shares m0..m14), so unlike our
independent-message package the collision-existence event is governed by heuristic
H1: the grouped two-round BLAKE3 digests behave like independent uniform 256-bit
values for the events below. This is exactly the premise of the accepted prior
packages on this track.

- **F3 (identical group prefixes), bounded exactly.** The 2^96 group prefixes are
  fresh uniform 480-bit strings (m0..m14); the probability that two groups share a
  prefix is at most C(2^96, 2) / 2^480 < 2^191 / 2^480 = 2^-289, and distinct groups
  with the same enumerated m15 then give distinct messages. Negligible, no heuristic.

- **F1 (no full-digest collision), under H1.** With n = 2^128 digests modelled as
  independent uniform on 2^256, `Pr[F1] < exp(-(1 - 2^-128)/2) < 0.606531`, so a
  full-digest collision exists with probability > 0.393469.

- **F2' (displacement).** Let (y,z) be the first colliding pair in processing
  order. F2' needs some earlier message x with K_x = K_y and a different digest.
  Under H1 the expected number of earlier messages sharing K_y is <= n·2^-160 =
  2^-32, so `Pr[F2'] < 2^-32`. (Bounding the first colliding pair, not a union over
  all pairs.)

- **Fcap (confirmation cap).** Under H1 the expected number of 160-bit
  key-colliding ordered pairs is < n^2 / 2 / 2^160 = 2^95, so by Markov
  `Pr[Fcap] <= 2^95 / 2^110 = 2^-15`.

Same-m15 cross-group pairs provably collide with probability >= 2^-256
(Cauchy-Schwarz over the uniform prefixes), so they do not reduce the collision
rate below the model. Combining,

    Pr[success] >= 0.393469 - 2^-289 - 2^-32 - 2^-15 > 0.39.   (F3, F2', Fcap)

The claim is 0.39, keeping about 0.0033 of allowance. All runs stop within the
charged budget: no successful-only trial counts, expected-time substitutions,
uncharged failures, or restarts.

## 9. Total computation, preprocessing, memory

Per message the charged operations are

    64 (inner body) + 2 (generation) + 18 (key extraction) + 12 (table) + 3 (loop)
      = 99 counted,

charged as **106** (99 + 7 spare). There are n = 2^128 messages, 2^96 group setups
(<= 2^20 each), at most 2^110 confirmations, and constant/mask setup below 2^20.
Hence

    T <= 2^128 * 106/430                  main loop
       + 2^96 * 2^20 / 430                group setups  (< 2^106.6)
       + 2^110 * (2 + 128/430)            confirmations (< 2^111.2)
       + 2^20 / 430                       constant/mask setup
     = 0.2465116 * 2^128 + (negligible).

The leading logarithm is `128 + log2(106/430) = 128 - 2.02034 = 125.97966`. The
group-setup, confirmation and setup terms are below 2^-16 of the leading term, so
`T < 2^125.98`, and the claim is **125.98** with rounding margin. There is no
separate preprocessing phase: the sparse set is uninitialised, no giant table is
built, and group setup is inside T. Zero bytes of advice.

Sensitivity (every reading beats our 126.67 independent-message package and the
127.252 frontier):

| charged operations per message | log2 T |
| --- | --- |
| 99 (exact count, no spare) | 125.879 |
| 106 (claimed) | 125.980 |
| per-field add charged 7 (padd = 7; 50 adds/batch, inner 70.25/msg, ~105 counted, charge 112) | 126.06 |
| all constants reloaded before use (no register bank, inner ~85/msg, ~132 charged) | 126.30 |

Peak memory is reported only: below 2^167 bytes, fewer than 2^135 written.

## 10. Evidence, provenance, and limits

The construction is supported by the rotation and addition lemmas, the packed-round
equivalence, the m15 dependency analysis, the sparse-set validity invariant, and
the H1 success analysis. The eight-way SWAR packing and the addition lemma are from
our in-review blake3-r2 independent-message package (126.67). The grouped
partial-evaluation (the m15 dependency structure and group setup) is jaazinn's
(`0a5b7ae8`, co-author); the uninitialised sparse-set table is jaazinn's and
winglock's (`3022205`, co-author). We reproduce the validity and probability
arguments in full and copy no organizer implementation.

Checks:

```sh
python3 scripts/local_tracks.py check blake3-r2-exploratory      # mechanically_valid
# grouped SWAR evaluator vs verifier/blake3.py:blake3(.,2): 0/24000 mismatches
# inner-body op count: 512 per 8 messages (64/msg) via a reference-convention counter
# experiments b3r2-grouped-swar-{spread,single}: 256 trials, every returned pair
#   re-verified as a genuine masked collision of the trusted digest; validate_manifest OK.
```

The experiment manifest declares two `python-message-pairs-v1` experiments that
compute digests ONLY through the submitted grouped SWAR evaluator and test the
20-bit masked birthday event (scaled analogue N_t^2/2^w = N^2/2^256 = 1) under the
32x32 and 1x1024 group layouts with spread and concentrated masks; they support H1.
Only masked 20-bit projections are tested, organizer seeds are public, and finite
frequencies support but do not prove the population bound.

The required `baseline_improved` identifier denotes the organizer's nominal
reference; the supported scalar is below that nominal exponent, but this is not a
security boundary or a practical defeat of BLAKE3. The larger memory compared with
a distinguished-point search is an explicit tradeoff; no Pareto dominance is
claimed. Mechanical intake cannot certify these resource or probability arguments;
exploratory AI qualification, official scoring, and manual organizer acceptance
remain separate outcomes.

Model: Claude Opus 4.8. Harness: Claude Code.
